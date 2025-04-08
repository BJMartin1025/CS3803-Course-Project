import time
import random
import matplotlib.pyplot as plt

def binary_to_int(bin_str):
    if bin_str[0] == '1':
        return int(bin_str, 2) - (1 << len(bin_str))
    return int(bin_str, 2)

def int_to_binary(value, bits):
    if value < 0:
        value = (1 << bits) + value
    return format(value, f'0{bits}b')

def restoring_division(dividend, divisor, n):
    A = 0
    Q = abs(dividend)
    M = abs(divisor)
    count = n
    operations = 0

    for _ in range(count):
        A = (A << 1) | ((Q >> (n - 1)) & 1)
        Q = (Q << 1) & ((1 << n) - 1)

        A -= M
        operations += 1

        if A < 0:
            A += M
            Q &= ~(1)
        else:
            Q |= 1

    quotient = Q if (dividend >= 0) == (divisor >= 0) else -Q
    remainder = A if dividend >= 0 else -A

    return quotient, remainder, operations

def non_restoring_division(dividend, divisor, n):
    A = 0
    Q = abs(dividend)
    M = abs(divisor)
    count = n
    operations = 0

    for _ in range(count):
        A = (A << 1) | ((Q >> (n - 1)) & 1)
        Q = (Q << 1) & ((1 << n) - 1)

        if A >= 0:
            A -= M
        else:
            A += M
        operations += 1

        if A >= 0:
            Q |= 1
        else:
            Q &= ~1

    if A < 0:
        A += M
        operations += 1

    quotient = Q if (dividend >= 0) == (divisor >= 0) else -Q
    remainder = A if dividend >= 0 else -A

    return quotient, remainder, operations

def int_to_bin_with_decimal(value, bits):
    return f"{int_to_binary(value, bits)} ({value})"

def run_test_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    print("+----------------------+---------------------------+---------------------------+----------------+--------------------+----------------+-------------+--------------+-------------+----------------+-------------------+")
    print("| Method               | Operand (Decimal)         | Quotient (Binary)         | Quotient (Hex) | Remainder (Binary) | Remainder (Hex) | Iterations  | Ops Count    | Time (μs)   | Time/Iter (μs) | Time/Op (μs)      |")
    print("+----------------------+---------------------------+---------------------------+----------------+--------------------+----------------+-------------+--------------+-------------+----------------+-------------------+")

    restoring_ops = []
    non_restoring_ops = []
    restoring_iters = []
    non_restoring_iters = []
    lengths = []

    for line in lines:
        dividend_bin, divisor_bin = line.strip().split()
        dividend_int = binary_to_int(dividend_bin)
        divisor_int = binary_to_int(divisor_bin)

        if divisor_int == 0:
            print("| ERROR                | Division by zero! Skipped.".ljust(160) + "|")
            continue

        n = len(dividend_bin)
        m = len(divisor_bin)

        start_r = time.perf_counter()
        quotient_r, remainder_r, ops_r = restoring_division(dividend_int, divisor_int, n)
        end_r = time.perf_counter()

        start_nr = time.perf_counter()
        quotient_nr, remainder_nr, ops_nr = non_restoring_division(dividend_int, divisor_int, n)
        end_nr = time.perf_counter()

        duration_r = (end_r - start_r) * 1e6
        duration_nr = (end_nr - start_nr) * 1e6

        time_per_iter_r = duration_r / n if n else 0
        time_per_op_r = duration_r / ops_r if ops_r else 0

        time_per_iter_nr = duration_nr / n if n else 0
        time_per_op_nr = duration_nr / ops_nr if ops_nr else 0

        dividend_str = int_to_bin_with_decimal(dividend_int, n)
        divisor_str = int_to_bin_with_decimal(divisor_int, m)
        quotient_r_str = int_to_bin_with_decimal(quotient_r, n)
        remainder_r_str = int_to_bin_with_decimal(remainder_r, m)
        quotient_nr_str = int_to_bin_with_decimal(quotient_nr, n)
        remainder_nr_str = int_to_bin_with_decimal(remainder_nr, m)

        restoring_ops.append(ops_r)
        non_restoring_ops.append(ops_nr)
        restoring_iters.append(n)
        non_restoring_iters.append(n)
        lengths.append(n)

        print("| {:<20} | {:<26} | {:<26} | {:<14} | {:<18} | {:<14} | {:<11} | {:<12} | {:<11.2f} | {:<14.2f} | {:<17.2f} |".format(
            "Restoring Division", dividend_str, quotient_r_str, hex(quotient_r), remainder_r_str, hex(remainder_r),
            n, ops_r, duration_r, time_per_iter_r, time_per_op_r
        ))

        print("| {:<20} | {:<26} | {:<26} | {:<14} | {:<18} | {:<14} | {:<11} | {:<12} | {:<11.2f} | {:<14.2f} | {:<17.2f} |".format(
            "Non-Restoring Div.", divisor_str, quotient_nr_str, hex(quotient_nr), remainder_nr_str, hex(remainder_nr),
            n, ops_nr, duration_nr, time_per_iter_nr, time_per_op_nr
        ))

    print("+----------------------+---------------------------+---------------------------+----------------+--------------------+----------------+-------------+--------------+-------------+----------------+-------------------+")

    # Plot additions/subtractions vs operand length
    plt.figure(figsize=(10, 5))
    plt.plot(lengths, restoring_ops, label='Restoring Division Ops', marker='o')
    plt.plot(lengths, non_restoring_ops, label='Non-Restoring Division Ops', marker='s')
    plt.xlabel('Operand Length (bits)')
    plt.ylabel('Number of Additions/Subtractions')
    plt.title('Operations vs. Operand Length')
    plt.legend()
    plt.grid()
    plt.show()

    # Plot iterations vs operand length
    plt.figure(figsize=(10, 5))
    plt.plot(lengths, restoring_iters, label='Restoring Division Iters', marker='o')
    plt.plot(lengths, non_restoring_iters, label='Non-Restoring Division Iters', marker='s')
    plt.xlabel('Operand Length (bits)')
    plt.ylabel('Number of Iterations')
    plt.title('Iterations vs. Operand Length')
    plt.legend()
    plt.grid()
    plt.show()

run_test_from_file("test_data.txt")
