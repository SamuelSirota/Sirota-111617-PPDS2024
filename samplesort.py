"""This program impements a parallel version of the samplesort
algorithm using CUDA for the assignment 05.

It uses the insertion sort algorithm to sort the subarrays
of the input array in parallel.
The code is based on insertion sort algorithm from 
website https://www.geeksforgeeks.org/insertion-sort/.

Samplesort algorithm splits the input array into buckets
and sorts them recursively. The algorithm uses insertion
sort to sort the subarrays in parallel.
"""

__author__ = "Samuel Martin Sirota"
__email__ = "xsirotas@stuba.sk"

import random, sys, time
import numpy as np
from numba import cuda

def insertionSortSerial(data):
    """This function sorts the input array using the insertion sort algorithm.
    """
    for i in range(1, data.size):
        key = data[i]
        j = i - 1
        while j >= 0 and key < data[j]:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key
    return data

@cuda.jit
def insertion_sort(data):
    """This function is cuda kernel. It sorts the input array 
    using the insertion sort algorithm in parallel.
    """
    for i in range(1, data.size):
        key = data[i]
        j = i - 1
        while j >= 0 and key < data[j]:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key

def sampleSort(A, k, p, threshold):
    """This function sorts the input array using the samplesort algorithm.
    It splits the input array into buckets and sorts them recursively.
    The algorithm uses insertion sort to sort the subarrays in parallel.
    """
    if len(A) / k < threshold:
        data = cuda.to_device(A)
        insertion_sort[1, 32](data)
        A = data.copy_to_host()
        return A

    S = random.sample(list(A), k * (p - 1))
    data = cuda.to_device(np.array(S))
    insertion_sort[1, 32](data)
    S = data.copy_to_host()
    splitters = [-float('inf')] + [S[i * k] for i in range(1, p-1)] + [float('inf')]

    buckets = [[] for _ in range(p)]
    for a in A:
        for j in range(p):
            if splitters[j] < a <= splitters[j + 1]:
                buckets[j].append(a)
                break

    sorted_buckets = []
    for bucket in buckets:
        if bucket:
            sorted_bucket = sampleSort(bucket, k, p, threshold)
            sorted_buckets.extend(sorted_bucket)
    return sorted_buckets
     
def main():
    """This function tests the samplesort algorithm.
    It generates a random array and sorts it using the samplesort algorithm.
    It also sorts the array using the insertion sort algorithm in serial.
    It prints the times needed to sort the array in both methods.
    Lastly, it checks if the arrays sorted by both methods are equal.
    """
    sys.setrecursionlimit(100000)
    array_len = 15000
    A = np.random.randint(0, 1000, array_len)
    k = 2
    p = 7
    threshold = 100
    start = time.perf_counter()
    sorted_A_par = sampleSort(A.copy(), k, p, threshold)
    end = time.perf_counter()
    #print(sorted_A_par)
    print(f"Array length: {array_len}")
    print(f"Time to sort parallel: {end - start} s")

    start = time.perf_counter()
    sorted_A_serial = insertionSortSerial(A.copy())
    end = time.perf_counter()
    #print(sorted_A_serial)
    print(f"Time to sort serial: {end - start} s")
    for gpu_array, array in zip(sorted_A_par, sorted_A_serial):
        assert(np.allclose(gpu_array, array))

if __name__ == "__main__":
    main()