import random
import time
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
from av import VideoFrame

from vpx_rtp.clock import current_ntp_time
from vpx_rtp.codecs.vpx import (
    VIDEO_CLOCK_RATE,
    VIDEO_TIME_BASE,
    Vp8Decoder,
    Vp8Encoder,
    VpxCodec,
    vp8_depayload,
)
from vpx_rtp.jitterbuffer import JitterBuffer
from vpx_rtp.rtp import RtpPacket
from vpx_rtp.utils import random16, random32, uint16_add

DUCK_JPEG_PATH = Path(__file__).parent / "duck.jpg"

VIDEO_PTIME = 1 / 30  # 30fps
DROPPED_PACKET_PERCENTAGE = 0


def generate_flag_frames() -> list[VideoFrame]:
    height, width = 480, 640

    duck_np_array = cv2.imread(str(DUCK_JPEG_PATH))
    data_bgr = cv2.resize(duck_np_array, (width, height))

    # shrink and center it
    M = np.array([[0.5, 0, width / 4], [0, 0.5, height / 4]])
    data_bgr = cv2.warpAffine(data_bgr, M, (width, height))

    # compute animation
    omega = 2 * np.pi / height
    id_x = np.tile(np.array(range(width), dtype=np.float32), (height, 1))
    id_y = np.tile(np.array(range(height), dtype=np.float32), (width, 1)).transpose()

    frames = []
    for k in range(30):
        phase = 2 * k * np.pi / 30
        map_x = id_x + 10 * np.cos(omega * id_x + phase)
        map_y = id_y + 10 * np.sin(omega * id_x + phase)
        frames.append(
            VideoFrame.from_ndarray(
                cv2.remap(data_bgr, map_x, map_y, cv2.INTER_LINEAR).astype(np.uint8),
                format="bgr24",
            )
        )

    return frames


DUCK_FLAG_FRAMES = generate_flag_frames()

codec = VpxCodec.VP9

video_encoder = Vp8Encoder(codec)
video_decoder = Vp8Decoder(codec)

pts_timestamp = 0
_ssrc = random32()
sequence_number = random16()

_jitter_buffer = JitterBuffer(capacity=128, is_video=True)

received_frame_num = 0
max_simulated_time = 5
FORCE_KEYFRAME_EVERY_N = 100

script_start_time = time.perf_counter()
for send_frame_num in range(500):
    if time.perf_counter() - script_start_time > max_simulated_time:
        break

    video_frame = DUCK_FLAG_FRAMES[send_frame_num % len(DUCK_FLAG_FRAMES)]
    video_frame.pts = pts_timestamp
    video_frame.time_base = VIDEO_TIME_BASE

    start = time.perf_counter()

    force_keyframe = (send_frame_num % FORCE_KEYFRAME_EVERY_N) == 0
    if force_keyframe:
        print("Forcing keyframe")

    _mid_encoding_video_packets, timestamp = video_encoder.encode(
        video_frame, force_keyframe=force_keyframe
    )
    print(f"Encoding took {1000*(time.perf_counter() - start):0.2f} ms")

    start = time.perf_counter()
    wire_packet_bytes = []
    for i, payload in enumerate(_mid_encoding_video_packets):
        outgoing_packet = RtpPacket(
            payload_type=codec.value.payloadType,
            sequence_number=sequence_number,
            timestamp=timestamp,
        )
        outgoing_packet.ssrc = _ssrc
        outgoing_packet.payload = payload
        outgoing_packet.marker = (i == len(_mid_encoding_video_packets) - 1) and 1 or 0

        # set header extensions
        outgoing_packet.extensions.abs_send_time = (
            current_ntp_time() >> 14
        ) & 0x00FFFFFF

        outgoing_packet_bytes = outgoing_packet.serialize()
        wire_packet_bytes.append(outgoing_packet_bytes)

        sequence_number = uint16_add(sequence_number, 1)

    print(f"Outgoing serialization took {1000*(time.perf_counter() - start):0.2f} ms")
    print(
        f"Total frame size kb: {(sum(len(packet) for packet in wire_packet_bytes))/1000:0.2f}"
    )

    start = time.perf_counter()
    received_video_frames: list[VideoFrame] = []
    for incoming_packet_bytes in wire_packet_bytes:
        if random.random() < DROPPED_PACKET_PERCENTAGE:
            print("\n\n\nSIMULATED DROPPED PACKET\n\n\n")
            continue
        incoming_rtp_packet = RtpPacket.parse(incoming_packet_bytes)
        try:
            if incoming_rtp_packet.payload:
                incoming_rtp_packet._data = vp8_depayload(incoming_rtp_packet.payload)
            else:
                print("PACKET HAS NO PAYLOAD")
                incoming_rtp_packet._data = b""
        except ValueError as exc:
            raise ValueError(f"x RTP payload parsing failed: {exc}")

        # try to re-assemble encoded frame
        pli_flag, encoded_frame = _jitter_buffer.add(incoming_rtp_packet)

        # if we have a complete encoded frame, decode it
        if encoded_frame is not None:
            received_video_frames.extend(video_decoder.decode(encoded_frame))
            received_frame_num += 1

    print(f"Decoding took {1000*(time.perf_counter() - start):0.2f} ms")

    start = time.perf_counter()
    for frame in received_video_frames:
        plt.clf()
        plt.imshow(frame.to_ndarray(format="rgb24"))
    print(f"Plotting took {1000*(time.perf_counter() - start):0.2f} ms")

    start = time.perf_counter()
    plt.pause(VIDEO_PTIME / 100)
    plt.draw()
    print(f"Drawing took {1000*(time.perf_counter() - start):0.2f} ms")

    pts_timestamp += int(VIDEO_PTIME * VIDEO_CLOCK_RATE)
