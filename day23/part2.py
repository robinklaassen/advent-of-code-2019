from concurrent.futures.thread import ThreadPoolExecutor
from queue import Queue
from time import sleep
from typing import List, Tuple

from day23.intcode_computer import IntcodeComputer
from day23.puzzle_input import NIC_PROGRAM


class Network:
    """A network of Intcode computers"""

    def __init__(self, program: List[int], num_computers: int = 50):
        self.queue = Queue()
        self.computers = [IntcodeComputer(i, program, self.queue) for i in range(num_computers)]
        self.last_nat_packet = None
        self.sent_nat_packets = []

    def start(self):
        executor = ThreadPoolExecutor(max_workers=len(self.computers) + 2)
        executor.map(lambda c: c.start(), self.computers)
        executor.submit(self._handle_queue)
        executor.submit(self._handle_nat)

    def _handle_queue(self):
        while True:
            packet = self.queue.get()
            print(f"Network is processing packet: {packet}")
            if packet[0] == 255:
                self._send_packet_to_nat(packet[1:])
            else:
                target_computer = self.computers[packet[0]]
                target_computer.pass_inputs(list(packet[1:]))

    def _send_packet_to_nat(self, packet: Tuple[int, int]):
        print(f"NAT received packet: {packet}")
        self.last_nat_packet = packet
        # self.nat_packets.append(packet)

    def _handle_nat(self):
        while True:
            if all([c.is_idle() for c in self.computers]) and self.last_nat_packet is not None:
                print(f"Network seems idle, passing last NAT packet {self.last_nat_packet} to computer at address 0")
                self.computers[0].pass_inputs(list(self.last_nat_packet))
                self.sent_nat_packets.append(self.last_nat_packet)
            else:
                sleep(0.3)


def main():
    network = Network(NIC_PROGRAM, num_computers=50)
    network.start()


if __name__ == "__main__":
    main()
