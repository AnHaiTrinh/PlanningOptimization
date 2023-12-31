from .solvers.solver_factory import SolverFactory
from .utils.parser import parse_args, read_input, read_output


if __name__ == '__main__':
    input_file, output_file, solver_name, return_time = parse_args()
    try:
        n, k, costs = read_input(input_file)
        optimal = read_output(output_file)
        solver_factory = SolverFactory(n, k, costs, optimal)
        solver = solver_factory.create_solver(solver_name)
        solver.evaluate(return_time)

        # Write log to file
        f = open('logs.txt', 'a')
        f.write("Solution: solve by [{}] for file [{}]\n".format(solver_name, os.path.basename(input_file)))
        f.close()
    except Exception as e:
        print(e)
        exit(1)
