import argparse
import numpy as np

def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", action="store_true")
    return parser

def read_data(day: int, sample: bool = False):
    if sample:
        with open(f"day{day}_test_input.txt") as f:
            data = f.read().splitlines()
    else:
        with open(f"day{day}_input.txt") as f:
            data = f.read().splitlines()
    return data