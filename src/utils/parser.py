import os
import argparse
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str, default='',
                        help='Input and output file name. Will read from stdin if left blank')
    parser.add_argument('--solver', type=str, default='bnb',
                        choices=['bnb', 'ip', 'cp', 'ls'],
                        help='Solver name')
    parser.add_argument('--return-time', action='store_true', help='Return time taken to solve')
    cmd_args = parser.parse_args()

    filename = cmd_args.filename
    if filename:
        input_file = os.path.join(os.getcwd(), 'data', 'input', filename)
        output_file = os.path.join(os.getcwd(), 'data', 'output', filename)
    else:
        input_file = output_file = None

    return input_file, output_file, cmd_args.solver, bool(cmd_args.return_time)


def read_input(input_file):
    if input_file:
        try:
            with open(input_file, 'r') as f:
                n, k = map(int, f.readline().split())
                costs = np.array([list(map(int, f.readline().split())) for _ in range(2 * n + 1)])
        except Exception as e:
            raise e
    else:
        try:
            n, k = map(int, input().split())
            costs = np.array([list(map(int, input().split())) for _ in range(2 * n + 1)])
        except Exception as e:
            raise e

    return n, k, costs


def read_output(output_file):
    optimal = None
    if output_file:
        try:
            with open(output_file, 'r') as f:
                optimal = int(f.readline())
        except Exception as e:
            print(e)

    return optimal
