import time
from typing import Optional

from vpx_rtp.codecs.vpx import VIDEO_CLOCK_RATE
from vpx_rtp.rtp import RtpPacket
from vpx_rtp.utils import uint16_gt

# From https://github.com/aiortc/aiortc/blob/22699ea879f93b6d6dd1af4a200d37b9ff560870/src/aiortc/rtcrtpreceiver.py


class ReceivedRtpStreamStatistics:
    def __init__(self) -> None:
        self.base_seq: Optional[int] = None
        self.max_seq: Optional[int] = None
        self.cycles = 0
        self.packets_received = 0

        # jitter
        self._jitter_q4 = 0
        self._last_arrival: Optional[int] = None
        self._last_timestamp: Optional[int] = None

        # fraction lost
        self._expected_prior = 0
        self._received_prior = 0

    def add(self, packet: RtpPacket) -> None:
        in_order = self.max_seq is None or uint16_gt(
            packet.sequence_number, self.max_seq
        )
        self.packets_received += 1

        if self.base_seq is None:
            self.base_seq = packet.sequence_number

        if in_order:
            arrival = int(time.time() * VIDEO_CLOCK_RATE)

            if self.max_seq is not None and packet.sequence_number < self.max_seq:
                self.cycles += 1 << 16
            self.max_seq = packet.sequence_number

            if packet.timestamp != self._last_timestamp and self.packets_received > 1:
                diff = abs(
                    (arrival - self._last_arrival)
                    - (packet.timestamp - self._last_timestamp)
                )
                self._jitter_q4 += diff - ((self._jitter_q4 + 8) >> 4)

            self._last_arrival = arrival
            self._last_timestamp = packet.timestamp

    @property
    def fraction_lost(self) -> int:
        """
        Fraction of packets lost since last access of this property, multiplied by 256.
        """
        expected_interval = self.packets_expected - self._expected_prior
        self._expected_prior = self.packets_expected
        received_interval = self.packets_received - self._received_prior
        self._received_prior = self.packets_received
        lost_interval = expected_interval - received_interval
        if expected_interval == 0 or lost_interval <= 0:
            return 0
        else:
            return (lost_interval << 8) // expected_interval

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
