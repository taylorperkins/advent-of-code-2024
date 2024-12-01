from utils import time_it, read_input, input_path


@time_it
def main(data: str) -> str:
    return data


if __name__ == "__main__":
    print(main(read_input(input_path(__file__))))
