# Assignment 04 - Parallel matrix multiplication

[![Python 3.10.12](https://img.shields.io/badge/python-3.10.12-purple.svg)](https://www.python.org/downloads/release/python-31012/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-purple.svg)](https://conventionalcommits.org)
[![Static Badge](https://img.shields.io/badge/mpiexec_(OpenRTE)-4.1.2-purple)](https://www.open-mpi.org/software/ompi/v4.1/)

## Description

This is a simple Python program that library mpi4py to multiply two matrices using parallel computing. The program is using the `mpiexec` command to run the program in parallel.

---

## Quick start

Before running the script, make sure you have Python 3.10.12 installed.
Additionally install openmpi (`apt install libopenmpi-dev`).
Also install `mpi4py` module (`pip3 install mpi4py`).

## Assignment

1. Make program that will multiply two matrices using parallel computing.
2. The program should be able to run on multiple work nodes, not only matrices with number of rows divisible by number of nodes.
3. Use collective communication functions scatter and gather, instead of Point-to-point communication.
4. Experiment with different matrix sizes and number of nodes, and measure the time of execution. Which method of parallel computing is faster? (Point-to-point or collective communication)

## Implementation

My implementation has few components:

1. Parallel matrix multiplication using send and receive functions
2. Parallel matrix multiplication using scatter and gather functions
3. Experiment with both methods

### Parallel matrix multiplication using send and receive functions

Most of the code I am using is from the 7th seminar. I have modified the code to be able to work on any number of nodes and any size of matrices.
I used numpy method `numpy.array_split()` to split the matrices into equal parts for each node. Mostly exual, because the number of rows of the matrix doesnt have to be divisible by the number of nodes. I also changed variable `rows` to match the number of rows of the each submatrix using `len()` function.
ALso used `MPI.Wtime()` to measure the time of execution. The time is measured on the root node.

### Parallel matrix multiplication using scatter and gather functions

The code also mostly comes from the 7th seminar. I have modified the code to be able to work on any number of nodes and any size of matrices.
Similarly to the previous implementation, I used `numpy.array_split()` to split the matrices into equal parts for each node. I used `MPI.Scatter()` to send the submatrices to each node and `MPI.Gather()` to gather the results from each node. The time is measured on the root node.

### Experiment with both methods

In this part of the code, I am experimenting with both methods. I am multiplying different sizes of matrices. I am running both methods for 100 times on different number of work nodes. I am measuring the time of execution and comparing them using scatterplots.

As you can see from the scatterplots. The small matrices 32x15 multiplied by 15x7 is faster using Point-to-point communication. There is a bigger gap between the two methods when the matrices are smaller. It also interestingly has an increasing trend.
![matrix multiplication on A\[32\]\[15\] B\[15\]\[7\] with 4 proc](https://raw.githubusercontent.com/SamuelSirota/Sirota-111617-PPDS2024/04/comparison_plot_A%5B32%5D%5B15%5D_B%5B15%5D%5B7%5D_4_proc.png?token=GHSAT0AAAAAACMVXLHJ4APXJ2HXPQR764MSZQS7ITA)

The bigger matrices 100x100 is faster using collective communication. The gap between the two methods is smaller when the matrices are bigger. The scatter plots show that the time of execution is more stable when the matrices are bigger.
![matrix multiplication on A\[100\]\[100\] B\[100\]\[100\] with 2 proc](https://raw.githubusercontent.com/SamuelSirota/Sirota-111617-PPDS2024/04/comparison_plot_A%5B100%5D%5B100%5D_B%5B100%5D%5B100%5D_2_proc.png?token=GHSAT0AAAAAACMVXLHI6RULNHZSNLD5IBIGZQS7HUQ)

Suprisingly the biggest matrices 200x200 is faster using Point-to-point communication. It could be caused by cpu optimazation or the way the matrices are split. It is visible that some s/g times are way bigger. The very big matrix multiplication is therefore faster using Point-to-point communication. The scatter plots show that the time of execution is even more stable when the matrices are bigger.
![matrix multiplication on A\[200\]\[200\] B\[200\]\[200\] with 3 proc](https://raw.githubusercontent.com/SamuelSirota/Sirota-111617-PPDS2024/04/comparison_plot_A%5B200%5D%5B200%5D_B%5B200%5D%5B200%5D_3_proc.png?token=GHSAT0AAAAAACMVXLHJTM55Y5CRIAEVC5MIZQS7I4A)
