"""This program implements parallel matrix multiplication using MPI4py
for the assigment 04.

It is inspired by the code from the course Parallel and Distributed Systems
by Matus Jokay, 2024-03-27. He uses codes from https://kurzy.kpi.fei.tuke.sk/pp/labs/pp_mm.c.

It does has both methods of parallel matrix multiplication, scatter-gather and point-to-point.
Compares the average time of 100 iterations of both methods.
It creates a scatter plot of the time of each iteration and the average time of both methods.
"""

__author__ = "Samuel Martin Sirota"
__email__ = "xsirotas@stuba.sk"

import matplotlib.pyplot as plt
import numpy as np
from mpi4py import MPI

NRA = 20  # number of rows in matrix A
NCA = 20  # number of columns in matrix A
NCB = 20  # number of columns in matrix B
MASTER = 0

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nproc = comm.Get_size()


def parallel(times):
    """This function performs parallel matrix multiplication using
    the point-to-point communication model.
    """
    
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
        times.append(MPI.Wtime() - start)
    else:
        comm.send(C_loc, dest = MASTER)

def parallelScatter(times):
    """This function performs parallel matrix multiplication using
    the scatter-gather communication model.
    """
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
        times.append(MPI.Wtime() - start)


def main():
    """This function compares the average time of 100 iterations of both methods.
    It creates a scatter plot of the time of each iteration and the average time of both methods.
    """
    a=[]
    b=[]
    for i in range(100):
        parallel(a)
        parallelScatter(b)

    if rank==MASTER:
        a_avg = sum(a) / len(a)
        b_avg = sum(b) / len(b)

        # Scatter plot
        plt.scatter(range(len(a)), a, label='Parallel')
        plt.scatter(range(len(b)), b, label='Parallel s/g')
        plt.hlines(a_avg, 0, len(a), colors='blue', linestyles='dashed', label='Average Parallel')
        plt.hlines(b_avg, 0, len(b), colors='orange', linestyles='dashed', label='Average Parallel s/g')

        # Graph customization
        plt.xlabel('Iteration')
        plt.ylabel('Time (seconds)')
        plt.title(f'Comparison of Parallel and Parallel s/g A[{NRA}][{NCA}]_B[{NCA}][{NCB}] on {nproc} proc')
        plt.legend()

        # Show plot
        plt.savefig(f'comparison_plot_A[{NRA}][{NCA}]_B[{NCA}][{NCB}]_{nproc}_proc.png')
    
if __name__ == "__main__":
    main()