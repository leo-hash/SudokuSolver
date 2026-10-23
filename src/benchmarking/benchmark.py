import dataclasses
import time
import tracemalloc
from dataclasses import dataclass

from src.engine import SudokuGrid, SudokuSolver


@dataclass
class Measurement:
    elapsed_time: float
    peak_memory: int
    current_memory: int

    def __str__(self):
        return (
            f'elapsed time: {self.elapsed_time:.3f} s, \t '
            f'peak memory: {self.peak_memory / 1024:.3f} KB, \t '
            f'current memory: {self.current_memory / 1024:.3f} KB'
        )


def run_benchmark(solver: SudokuSolver, sudoku: SudokuGrid = None) -> float:
    if sudoku is None:
        sudoku = SudokuGrid()

    start_time = time.perf_counter()
    sol = solver.solve(sudoku)
    end_time = time.perf_counter()

    del sol
    return end_time - start_time


def run_benchmark_memory(solver: SudokuSolver, sudoku: SudokuGrid = None) -> Measurement:
    tracemalloc.start()
    tracemalloc.reset_peak()

    used_time = run_benchmark(solver, sudoku)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return Measurement(elapsed_time=used_time, peak_memory=peak, current_memory=current)


def run_n_benchmarks(solver: SudokuSolver, run_n_times: int, sudoku_list: list[SudokuGrid] = None):
    pass



def both_benchmarks(solver: SudokuSolver, sudoku: SudokuGrid = None):
    measure = run_benchmark_memory(solver)
    print(measure)

    elapsed_time = run_benchmark(solver)
    print(f"Elapsed time: {elapsed_time:.3f} seconds")



if __name__ == '__main__':
    solver1 = SudokuSolver()
    solver2 = SudokuSolver(mrv=False)
    solver3 = SudokuSolver(afc=True)

    print("Solver with mrv")
    both_benchmarks(solver1)


    print()
    print("Solver without mrv")
    both_benchmarks(solver2)


    print()
    print("Solver with mrv and afc")
    both_benchmarks(solver3)





