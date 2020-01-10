from concurrent.futures.thread import ThreadPoolExecutor
from queue import Queue
from typing import List

from day23.intcode_computer import IntcodeComputer
from day23.puzzle_input import NIC_PROGRAM


class Network:
    """A network of Intcode computers"""

    def __init__(self, program: List[int], num_computers: int = 50):
        self.queue = Queue()
        self.computers = [IntcodeComputer(i, program, self.queue) for i in range(num_computers)]

    def start(self):
        executor = ThreadPoolExecutor(max_workers=len(self.computers))
        executor.map(lambda c: c.start(), self.computers)

        while True:
            packet = self.queue.get()

            print(f"Network is processing packet: {packet}")

            if packet[0] == 255:
                print(f"A packet was sent to address 255 with x, y: {packet[1:]}")
                exit(0)

            target_computer = self.computers[packet[0]]
            target_computer.pass_inputs(list(packet[1:]))


def main():
    network = Network(NIC_PROGRAM, num_computers=50)
    network.start()


if __name__ == "__main__":
    main()
