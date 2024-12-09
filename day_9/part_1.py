from dataclasses import dataclass
from collections import deque
from typing import List, Deque

from utils import time_it, read_input, input_path


@dataclass
class File:
    # start of the id
    id: int
    size: int


def clean_input(data) -> (List[int], Deque[File]):
    # size of the free space
    free_space: List[int] = []
    file_blocks: Deque[File] = deque()

    id_number = 0
    for i, v in enumerate(data):
        v = int(v)
        if i % 2 == 0:
            file_blocks.append(File(id_number, v))
            id_number += 1
        else:
            free_space.append(v)

    return free_space, file_blocks


@time_it
def main(data: str) -> int:
    free_space_refs, file_block_refs = clean_input(data)
    free_space_refs: List[int]
    file_block_refs: Deque[File]

    total = 0
    free_space = 0
    compression_idx = 0
    while file_block_refs:
        if not free_space:
            file = file_block_refs.popleft()
            if not file.size:
                free_space = free_space_refs.pop(0)
            else:
                total += (compression_idx * file.id)
                file_block_refs.appendleft(File(id=file.id, size=file.size-1))
                compression_idx += 1
        else:
            file = file_block_refs.pop()
            if not file.size:
                continue
            total += (compression_idx * file.id)
            file_block_refs.append(File(id=file.id, size=file.size - 1))
            free_space -= 1
            compression_idx += 1

    return total


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    # 91337315408, failure
    # 6448989155953
    print(main(read_input(input_path(__file__))))
