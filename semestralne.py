"""This application implements the PageRank algorithm
using MPI4py for the semestral project.

I used https://snap.stanford.edu/data/wiki-Vote.html 
as source for oriented graph.
"""

__author__ = "Samuel Martin Sirota"
__email__ = "xsirotas@stuba.sk"

from mpi4py import MPI
import numpy as np
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
MASTER = 0


def read_graph(file_path):
    """This function reads the graph from the file
    and returns the adjacency matrix.
    """
    node_index_map = {}
    num_nodes = 0
    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("#"):
                continue
            line_data = line.strip().split()
            if len(line_data) != 2:
                continue
            src_node = int(line_data[0])
            dest_node = int(line_data[1])
            if src_node not in node_index_map:
                node_index_map[src_node] = num_nodes
                num_nodes += 1
            if dest_node not in node_index_map:
                node_index_map[dest_node] = num_nodes
                num_nodes += 1
    adj_matrix = np.zeros((num_nodes, num_nodes), dtype=int)

    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("#"):
                continue
            line_data = line.strip().split()
            if len(line_data) != 2:
                continue
            src_node = int(line_data[0])
            dest_node = int(line_data[1])
            src_index = node_index_map[src_node]
            dest_index = node_index_map[dest_node]
            adj_matrix[src_index, dest_index] = 1
    return adj_matrix


def topology_driven_pagerank(graph, damping_factor=0.85, max_iterations=100):
    """This function calculates the PageRank of the graph"""
    if rank == MASTER:
        start = time.perf_counter()
    num_nodes = len(graph)
    pagerank = np.full(num_nodes, 1 / num_nodes)
    local_pagerank_new = np.zeros(num_nodes)

    graph = np.array(graph)
    row_indices, col_indices = np.nonzero(graph)
    out_degree = np.sum(graph, axis=1)

    nodes = np.array_split(range(num_nodes), size)
    local_nodes = nodes[rank]

    for _ in range(max_iterations):
        for v in local_nodes:
            sum_pr = np.sum(
                pagerank[row_indices[col_indices == v]]
                / out_degree[row_indices[col_indices == v]]
            )
            local_pagerank_new[v] = (
                1 - damping_factor
            ) / num_nodes + damping_factor * sum_pr
        total_pagerank_new = np.zeros(num_nodes)
        comm.Allreduce(local_pagerank_new, total_pagerank_new, op=MPI.SUM)

        pagerank = total_pagerank_new
    if rank == MASTER:
        print("PageRank:", np.array(pagerank))
        print("Time:", time.perf_counter() - start)
    return pagerank


def main():
    """Main function of the program.
    It reads the graph from the file and calculates the PageRank."""
    graph = None
    if rank == MASTER:
        graph = read_graph("kruznica.txt")
    graph = comm.bcast(graph, root=MASTER)
    topology_driven_pagerank(graph, max_iterations=1000)


if __name__ == "__main__":
    main()