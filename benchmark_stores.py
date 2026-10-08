"""
benchmark_stores.py
===================
Time the same four queries against the HDF5 store (itch.h5) and the Parquet
store (itch_parquet/) built in Question 1.

For each case, write the two one-line queries marked TODO -- one for HDF5
(pd.read_hdf) and one for Parquet (pd.read_parquet). Each must return a
pandas DataFrame. Everything else (timing, checking, the results table) is
done for you.

Usage (from the directory containing itch.h5 and itch_parquet/):
    python benchmark_stores.py
"""

from pathlib import Path
from time import perf_counter

import pandas as pd

H5 = 'itch.h5'                      # HDF5 store from create_ITCH_HDF5_store.py
PQ = Path('itch_parquet')           # Parquet store from create_ITCH_parquet_store.py
REPEAT = 3                          # run each query this many times; report the best


# Look up PACK's stock_locate code in the stock directory (message type R).
# PACK is a thinly traded stock: about 100 add orders on this day.
R = pd.read_parquet(PQ / 'msg_type=R')
PACK = int(R.loc[R.stock == 'PACK', 'stock_locate'].iloc[0])


# ---------------------------------------------------------------------------
# Case 1. Read an entire table: all rows and all columns of the
#         non-cross trade messages (type P).
# ---------------------------------------------------------------------------
def case1_hdf5():
    return None     # TODO

def case1_parquet():
    return None     # TODO


# ---------------------------------------------------------------------------
# Case 2. Read two columns: only `timestamp` and `executed_shares`
#         of every order-executed message (type E).
# ---------------------------------------------------------------------------
def case2_hdf5():
    return None     # TODO

def case2_parquet():
    return None     # TODO


# ---------------------------------------------------------------------------
# Case 3. Filter on stock_locate: all columns of the add-order messages
#         (type A) for PACK, i.e. rows with stock_locate == PACK.
# ---------------------------------------------------------------------------
def case3_hdf5():
    return None     # TODO

def case3_parquet():
    return None     # TODO


# ---------------------------------------------------------------------------
# Case 4. Filter on another column: all columns of the order-executed
#         messages (type E) with executed_shares >= 10,000.
# ---------------------------------------------------------------------------
def case4_hdf5():
    return None     # TODO

def case4_parquet():
    return None     # TODO


# ---------------------------------------------------------------------------
# Benchmark harness -- no changes needed below this line
# ---------------------------------------------------------------------------
def best_time(fn):
    """Run fn() REPEAT times; return (best wall-clock seconds, result)."""
    times = []
    for _ in range(REPEAT):
        t0 = perf_counter()
        result = fn()
        times.append(perf_counter() - t0)
    return min(times), result


CASES = [
    ('1. full table (P)',            case1_hdf5, case1_parquet),
    ('2. two columns (E)',           case2_hdf5, case2_parquet),
    ('3. PACK rows (A)',             case3_hdf5, case3_parquet),
    ('4. executed_shares >= 10k (E)', case4_hdf5, case4_parquet),
]

if __name__ == '__main__':
    rows = []
    for label, f_hdf5, f_parquet in CASES:
        t_h, out_h = best_time(f_hdf5)
        t_p, out_p = best_time(f_parquet)
        if out_h is None or out_p is None:
            print(f'{label}: not implemented yet')
            continue
        if len(out_h) != len(out_p):
            print(f'{label}: WARNING - row counts differ '
                  f'(HDF5 {len(out_h):,}, Parquet {len(out_p):,})')
        rows.append({'case': label, 'rows': len(out_p), 'cols': out_p.shape[1],
                     'HDF5 (s)': round(t_h, 3), 'Parquet (s)': round(t_p, 3),
                     'faster': 'HDF5' if t_h < t_p else 'Parquet',
                     'ratio': round(max(t_h, t_p) / min(t_h, t_p), 1)})
        print(f'{label}: HDF5 {t_h:.3f}s   Parquet {t_p:.3f}s')

    print()
    print(pd.DataFrame(rows).to_string(index=False))
