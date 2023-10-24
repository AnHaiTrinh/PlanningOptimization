from solvers.SolverFactory import SolverFactory
from utils import ArgsParser


if __name__ == '__main__':
    input_file, output_file, solver_name = ArgsParser.parse_args()
    solver_factory = SolverFactory(input_file, output_file)
    solver = solver_factory.create_solver(solver_name)
    solver.evaluate()

