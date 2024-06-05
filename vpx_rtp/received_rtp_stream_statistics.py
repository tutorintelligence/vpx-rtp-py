import time
from dataclasses import dataclass, replace
from typing import Optional

from vpx_rtp.codecs.vpx import VIDEO_CLOCK_RATE
from vpx_rtp.rtp import RtpPacket
from vpx_rtp.utils import uint16_gt

# From https://github.com/aiortc/aiortc/blob/22699ea879f93b6d6dd1af4a200d37b9ff560870/src/aiortc/rtcrtpreceiver.py


@dataclass(frozen=True)
class ReceivedRtpStreamStatistics:
    base_seq: int
    max_seq: int
    cycles: int
    packets_received: int

    # jitter
    _jitter_q4: int
    _last_arrival: int
    _last_timestamp: int

    @property
    def jitter(self) -> int:
        """
        An estimate of the statistical variance of the RTP data packet
        interarrival time, measured in timestamp units and expressed as an
        unsigned integer.
        """
        return self._jitter_q4 >> 4

    @property
    def packets_expected(self) -> int:
        """
        Number of packets expected since the beginning of reception.
        """
        return self.cycles + self.max_seq - self.base_seq + 1

    @property
    def packets_lost(self) -> int:
        """
        Number of packets lost since the beginning of reception, where the number of packets received
        includes any which are late or duplicates.
        """
        return self.packets_expected - self.packets_received


def _get_arrival_number() -> int:
    return int(time.time() * VIDEO_CLOCK_RATE)


def _update_statistics(
    old_stats: ReceivedRtpStreamStatistics, packet: RtpPacket
) -> ReceivedRtpStreamStatistics:
    in_order = uint16_gt(packet.sequence_number, old_stats.max_seq)

    if in_order:
        arrival = _get_arrival_number()
        cycles_increment = 1 << 16 if packet.sequence_number < old_stats.max_seq else 0
        if packet.timestamp != old_stats._last_timestamp:
            diff = abs(
                (arrival - old_stats._last_arrival)
                - (packet.timestamp - old_stats._last_timestamp)
            )
            jitter_q4_increment = diff - ((old_stats._jitter_q4 + 8) >> 4)
        else:
            jitter_q4_increment = 0

        return ReceivedRtpStreamStatistics(
            base_seq=old_stats.base_seq,
            max_seq=packet.sequence_number,
            cycles=old_stats.cycles + cycles_increment,
            packets_received=old_stats.packets_received + 1,
            _jitter_q4=old_stats._jitter_q4 + jitter_q4_increment,
            _last_arrival=arrival,
            _last_timestamp=packet.timestamp,
        )
    else:
        return replace(old_stats, packets_received=old_stats.packets_received + 1)


class ReceivedRtpStreamStatiticsAccumulator:
    def __init__(self) -> None:
        self.stats: Optional[ReceivedRtpStreamStatistics] = None

        # fraction lost
        self._expected_prior = 0
        self._received_prior = 0

    def add(self, packet: RtpPacket) -> None:
        self.stats = (
            _update_statistics(self.stats, packet)
            if self.stats is not None
            else ReceivedRtpStreamStatistics(
                base_seq=packet.sequence_number,
                max_seq=packet.sequence_number,
                cycles=0,
                packets_received=1,
                _jitter_q4=0,
                _last_arrival=_get_arrival_number(),
                _last_timestamp=packet.timestamp,
            )
        )

    def get_fraction_lost_and_reset(self) -> int:
        """
        Fraction of packets lost since last call to this method, multiplied by 256.
        """
        if self.stats is None:
            return 0
        expected_interval = self.stats.packets_expected - self._expected_prior
        self._expected_prior = self.stats.packets_expected
        received_interval = self.stats.packets_received - self._received_prior
        self._received_prior = self.stats.packets_received
        lost_interval = expected_interval - received_interval
        if expected_interval == 0 or lost_interval <= 0:
            return 0
        else:
            return (lost_interval << 8) // expected_interval
