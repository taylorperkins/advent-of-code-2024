import re

from utils import time_it, read_input, input_path


FREE_SPACE_PATTERN = re.compile(r'\.')
FILE_BLOCK_PATTERN = re.compile(r'\d')


def clean_input(data) -> str:
    blocks = ""
    id_number = 0
    for i, v in enumerate(data):
        v = int(v)

        # even represents a "file"
        if i % 2 == 0:
            blocks += (v * str(id_number))
            id_number += 1
        # odd represents "free space"
        else:
            blocks += (v * ".")

    return blocks


def compact(blocks: str) -> str:
    size = len(blocks)

    # idx to search the blocks from beginning and from end
    start_i, end_i = 0, size
    while True:
        next_free_space_match = FREE_SPACE_PATTERN.search(blocks, start_i)
        free_space_idx, _ = next_free_space_match.span()

        last_file_block_match = FILE_BLOCK_PATTERN.search(blocks[::-1], size - end_i)
        # note inverse since searching the reverse string
        _, file_block_idx = last_file_block_match.span()
        file_block_idx = size - file_block_idx
        file_block = blocks[file_block_idx]

        if free_space_idx > file_block_idx:
            return blocks

        blocks = (
                blocks[:free_space_idx]
                + file_block
                + blocks[free_space_idx + 1:file_block_idx]
                + "."
                + blocks[file_block_idx + 1:]
        )

        start_i = free_space_idx - 1
        end_i = file_block_idx + 1


@time_it
def main(data: str) -> int:
    blocks = clean_input(data)
    blocks = compact(blocks)

    dot_product = sum(
        i * int(v)
        for i, v in enumerate(blocks[:blocks.index(".")])
    )

    return dot_product


if __name__ == "__main__":
    print(main(read_input(input_path(__file__).replace(".txt", "_practice.txt"))))
    print(main(read_input(input_path(__file__))))
