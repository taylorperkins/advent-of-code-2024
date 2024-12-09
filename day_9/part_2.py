from __future__ import annotations

from dataclasses import dataclass
from typing import List

from utils import time_it, read_input, input_path


@dataclass
class File:
    # start of the id
    id: int
    span: range

    @property
    def size(self):
        return self.span.stop - self.span.start

    def move(self, block: int):
        self.span = range(block, block + self.size)

    def distance(self, other: File):
        if other > self:
            return other.distance(self)
        return other.span.start - self.span.stop

    # since files should never be split, and should never overlap,
    # we can just use the start property for a direct comparison
    def __gt__(self, other: File):
        return other.span.start > self.span.start

    def __lt__(self, other: File):
        return other.span.start < self.span.start

    def __eq__(self, other: File):
        return self.id == other.id

    def __le__(self, other: File):
        return self == other or other < self

    def __ge__(self, other: File):
        return self == other or other > self

    def __repr__(self):
        return f'{self.size * str(self.id)}@{self.span.start}'


def clean_input(data) -> List[File]:
    file_blocks: List[File] = []

    id_number = 0
    block_index = 0
    for i, v in enumerate(data):
        v = int(v)
        if i % 2 == 0:
            file_blocks.append(File(id=id_number, span=range(block_index, block_index+v)))
            id_number += 1

        block_index += v

    return file_blocks


@time_it
def main(data: str) -> int:
    # represent the files and free space through
    # sorting all file blocks, sorted based on spans and
    # file location
    file_blocks = sorted(clean_input(data), reverse=True)
    size = len(file_blocks)

    # should represent the "next" file to check
    current_file = size - 1
    considered = 0
    while considered < size:
        file = file_blocks[current_file]
        considered += 1

        # iterate through all the files (in theory)
        for i in range(size):
            left = file_blocks[i]

            # we have found the file we are checking against, stop
            if left == file:
                current_file -= 1
                break

            right = file_blocks[i+1]

            # check if the span between left and right can fit the
            # current file
            if left.distance(right) >= file.size:
                file.move(left.span.stop)
                file_blocks.insert(i+1, file_blocks.pop(current_file))
                break

    total = 0
    for file in file_blocks:
        for block in file.span:
            total += (block * file.id)

    return total


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
