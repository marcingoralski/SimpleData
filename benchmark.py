import timeit
from simplecsv import serialize_c
import csv
import io


def serialize_py(serializable):
    return [",".join([str(key), str(value)]) for key, value in serializable.items()]


def serialize_csv(serializable):
    output = io.StringIO()
    writer = csv.writer(output)
    [writer.writerow(row) for row in serializable.items()]
    return output.getvalue()


def timed(func, *args, number=100):
    timer = timeit.Timer(lambda: func(*args))
    elapsed_time = timer.timeit(number=number) / number
    return elapsed_time * 1000

 
def benchmark():
    size = 100000
    tries = 20

    print("Benchmarking...")
    print(f"Serializable: {size} elements")
    print(f"Tries: {tries}\n")

    serializable = {i: i for i in range(size)}

    py_miliseconds = timed(serialize_py, serializable, number=tries)
    print(f"Py function: {py_miliseconds:.3f} ms")

    csv_miliseconds = timed(serialize_csv, serializable, number=tries)
    print(f"csv writer: {csv_miliseconds:.3f} ms")

    c_csv_miliseconds = timed(serialize_c, serializable, number=tries)
    print(f"simplecsv using c module : {c_csv_miliseconds:.3f} ms")

if __name__ == "__main__":
    benchmark()
