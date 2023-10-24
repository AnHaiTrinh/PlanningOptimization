import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str, default='',
                        help='Input and output file name. Will read from stdin if left blank')
    parser.add_argument('--solver', type=str, default='bnb', choices=['bnb'],
                        help='Solver name')
    cmd_args = parser.parse_args()

    filename = cmd_args.filename
    if filename:
        input_file = os.path.join(os.getcwd(), '..', 'data', 'input', filename)
        output_file = os.path.join(os.getcwd(), '..', 'data', 'output', filename)
    else:
        input_file = output_file = None

    return input_file, output_file, cmd_args.solver
