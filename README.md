# Assignment 05 - Parallel samplesort for Numba CUDA

[![Python 3.10.12](https://img.shields.io/badge/python-3.10.12-purple.svg)](https://www.python.org/downloads/release/python-31012/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-purple.svg)](https://conventionalcommits.org)
[![Static Badge](https://img.shields.io/badge/CUDA_Toolkit-12.4-purple)](https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exe_local)

## Description

This is a simple Python program that uses python library numba and cuda to sort lists of numbers. The program is using the CUDA Toolkit 12.4  run the program in parallel on GPU.

---

## Quick start

Before running the script, make sure you have Python 3.10.12 installed.
Additionally check if you have CUDA Toolkit 12.4 installed.
Also install `numba` module (`pip install numba`) and `cuda-python` (`pip install cuda-python`).

## Assignment

1. Implement algoritm samplesort for Numba CUDA.
2. Compare the performance of the algorithm with the serial version on three inputs with different orders.
3. Explain implementation and explain choices for number of threads and blocks.

## Implementation

My implementation has few components:

1. Serial sort algorithm (Insertion sort)
2. Parallel samplesort algorithm
3. Comparing performance of both algorithms

### Serial sort algorithm

As a serial sort algorithm I choose insertion sort. It is simple and good for small arrays.
It doesnt use recursion and it is stable. It has time complexity O(n^2) and space complexity O(1).
I didnt need to change much for it to work as cuda kernel.
I just added `@cuda.jit` and I use  `cuda.to_device(np.array(S))` to make it work on GPU.
Also I had to change the way I was returning the array. I use `data.copy_to_host()` to return the sorted array.
As parameters I used block per grid as 1 because I had issues with it. The resulting array had different values than the input array.
Number of threads per block I choose 32 as it is not too small and i can be scaled up if needed.

### Parallel samplesort algorithm

#### Function Parameters

- `A`: The input array to be sorted.
- `k`: Oversampling factor for load balancing
- `p`: The number of spliters to be used.
- `threshold`: A threshold value to determine when to switch to a different sorting algorithm (in this case, insertion sort).

#### Code has 4 main parts

1. Check if the input array is small enough to use insertion sort. In case it is, it uses insertion sort.
2. Randomly select samples from the input array, sort them, and use them as splitters to divide the input data into buckets.
3. Assign each element of the input array to its corresponding bucket based on the splitters.
4. Recursively apply samplesort to each bucket and concatenate the sorted results.

### Comparing performance of both algorithms

I used `time.perf_counter()` to measure the time it takes for both *parallel samplesort with insertion sort* and *insertion sort* to sort the array.
From smallest to the largest array size I used 100, 2000, 2500, 15000 and 100 000.

| Array length | Parellel |  Serial   |
| ------------ | -------- |---------- |
| 100          | 0.3465 s | 000.0005 s |
| 2 000        | 0.4180 s | 000.3578 s |
| 2 500        | 0.4185 s | 000.5250 s |
| 15 000       | 0.6910 s | 017.3968 s |
| 100 000      | 2.1158 s | 902.9224 s|

The results are as expected. In smaller arrays of size 100, the parallel version is slower than the serial version. This is because of the overhead of using the GPU. However, as the array size increases, the parallel version becomes faster than the serial version. This happens between array sizes of 2000 and 2500. The parallel version is significantly faster than the serial version for larger arrays of size 15000. For curiosity I tested the algorithm on array of size 100 000 and the parallel version is 400+ times faster than the serial version.
