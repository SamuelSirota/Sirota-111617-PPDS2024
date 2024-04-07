"""This program implements parallel matrix multiplication using MPI4py
for the assigment 04.

It is inspired by the code from the course Parallel and Distributed Systems
by Matus Jokay, 2024-03-27. He uses codes from https://kurzy.kpi.fei.tuke.sk/pp/labs/pp_mm.c.

It does matrix multiplication of two matrices A and B and stores the result in matrix C.
It uses the Point-to-Point communication model to distribute the matrices A and B.
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

#Initialize matrices A and B and distribute them
if rank == MASTER:
    start = MPI.Wtime()
    A = np.array([i+j for j in range(NRA) for i in range(NCA)]).reshape(NRA, NCA)
    B = np.array([i*j for j in range(NCA) for i in range(NCB)]).reshape(NCA, NCB)

    split = np.array_split(A, nproc)
    for proc in range(nproc):
        if proc == MASTER:
            A_loc = split[proc]
            continue
        comm.send(split[proc], dest = proc)
else:
    A_loc = comm.recv()
    B = None

B = comm.bcast(B, root = MASTER)

# Perform sequential matrix multiplication
rows = len(A_loc)
C_loc = np.zeros((rows, NCB), dtype = int)
for i in range(rows):
    for j in range(NCB):
        for k in range(NCA):
            C_loc[i][j] += A_loc[i][k] * B[k][j]

# Combine results into matrix C
C = np.zeros((NRA, NCB), dtype = int)
if rank == MASTER:
    for proc in range(nproc):
        if proc == MASTER:
            C[proc*rows:proc*rows+rows] = C_loc
            C_loc_len = len(C_loc)
            continue
        C_loc = comm.recv(source = proc)
        C[C_loc_len:C_loc_len+len(C_loc)] = C_loc
        C_loc_len = C_loc_len + len(C_loc)
    #print(C)
    print(MPI.Wtime() - start)
else:
    comm.send(C_loc, dest = MASTER)

    

