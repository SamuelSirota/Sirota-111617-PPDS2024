"""This program implements parallel matrix multiplication using MPI4py
for the assigment 04.

It is inspired by the code from the course Parallel and Distributed Systems
by Matus Jokay, 2024-03-27. He uses codes from https://kurzy.kpi.fei.tuke.sk/pp/labs/pp_mm.c.

It does matrix multiplication of two matrices A and B and stores the result in matrix C.
It uses the scatter() and gather() collective operations to distribute the matrices A and B.
"""

__author__ = "Samuel Martin Sirota"
__email__ = "xsirotas@stuba.sk"

import numpy as np
from mpi4py import MPI

NRA = 32  # number of rows in matrix A
NCA = 15  # number of columns in matrix A
NCB = 7   # number of columns in matrix B
MASTER = 0

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nproc = comm.Get_size()

A = None
B = None

#Initialize matrices A and B
if rank == MASTER:
    start = MPI.Wtime()
    A = np.array([i+j for j in range(NRA) for i in range(NCA)]).reshape(NRA, NCA)
    A = np.array_split(A, nproc)
    B = np.array([i*j for j in range(NCA) for i in range(NCB)]).reshape(NCA, NCB)

# Distributing matrix A and broadcast matrix B
A_loc = comm.scatter(A, root = MASTER)
B = comm.bcast(B, root = MASTER)
rows = len(A_loc)

# Perform sequential matrix multiplication
C_loc = np.zeros((rows, NCB), dtype = int)
for i in range(rows):
    for j in range(NCB):
        for k in range(NCA):
            C_loc[i][j] += A_loc[i][k] * B[k][j]

# Combine results into matrix C
C = comm.gather(C_loc, root = MASTER)
if rank == MASTER:
    C = np.array([ss for s in C for ss in s])
    #print(C)
    print(MPI.Wtime() - start)

