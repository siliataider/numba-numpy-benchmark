import numba
import numpy as np
import ROOT
import sys

def count_muons_loop(ptr):
    arr = numba.carray(ptr, 10)
    count = 0
    for i in range(len(arr)):
        if arr[i] > 1. and abs(arr[i]) < 7. and arr[i] > 0.:
            count += 1
    return count

def count_muons(ptr):
    arr = numba.carray(ptr, 10)
    return np.count_nonzero((arr > 1.) & (np.abs(arr) < 7.) & (arr > 0.))


if __name__ == "__main__":
    num_threads = int(sys.argv[1])

    loop_func = numba.cfunc(numba.int32(numba.types.CPointer(numba.float32)), nopython=True)(count_muons_loop)
    numpy_func = numba.cfunc(numba.int32(numba.types.CPointer(numba.float32)), nopython=True)(count_muons)

    ROOT.gInterpreter.Declare(f"""
const auto N_THREADS = {num_threads};;
auto *loopf = reinterpret_cast<int(*)(float*)>({loop_func.address});
auto *npf = reinterpret_cast<int(*)(float*)>({numpy_func.address});
""")

    ROOT.gInterpreter.Calc("""
ROOT::TThreadExecutor t{N_THREADS};
float arr[10]{};
std::vector<float*> args(1'000'000'000, arr);
TStopwatch s;
s.Start();
auto res = t.Map(loopf, args);
s.Stop();
s.Print();

s.Reset();
s.Start();
res = t.Map(npf, args);
s.Stop();
s.Print();
    """)
