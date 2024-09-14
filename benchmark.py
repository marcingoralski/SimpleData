import timeit
from simplecsv import serialize_c
import csv
import io


def serialize_py(serializable):
    return "\n".join(f"{key},{value}" for key, value in serializable.items())


def serialize_csv(serializable):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(serializable.items())
    return output.getvalue()


def timed(func, *args, number=100):
    timer = timeit.Timer(lambda: func(*args))
    elapsed_time = timer.timeit(number=number) / number
    return elapsed_time * 1000

 
def benchmark():
    size_small = 100000
    size_large = 1000000
    tries = 20

    print("Benchmarking...\n")
    
    print(f"{'Test Case':<20} | {'Size':<10} | {'Tries':<6} | {'Py Time (ms)':<12} | {'CSV Time (ms)':<13} | {'C Time (ms)':<12}")
    print("-" * 80)

    serializable_small = {i: i for i in range(size_small)}
    py_small = timed(serialize_py, serializable_small, number=tries)
    csv_small = timed(serialize_csv, serializable_small, number=tries)
    c_csv_small = timed(serialize_c, serializable_small, number=tries)
    
    print(f"{'Small Dataset':<20} | {size_small:<10} | {tries:<6} | {py_small:12.3f} | {csv_small:13.3f} | {c_csv_small:12.3f}")

    serializable_large = {i: i for i in range(size_large)}
    py_large = timed(serialize_py, serializable_large, number=tries)
    csv_large = timed(serialize_csv, serializable_large, number=tries)
    c_csv_large = timed(serialize_c, serializable_large, number=tries)

    print(f"{'Large Dataset':<20} | {size_large:<10} | {tries:<6} | {py_large:12.3f} | {csv_large:13.3f} | {c_csv_large:12.3f}")


if __name__ == "__main__":
    benchmark()
