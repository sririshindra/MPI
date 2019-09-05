from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()


if rank == 0:
    data = {'a': 7, 'b': 3.14}
    comm.isend(data, dest=1, tag=11)
    comm.isend(data, dest=2, tag=11)
    comm.isend(data, dest=3, tag=11)
elif rank == 1 or rank == 2 or rank == 3:
    data = comm.irecv(source=0, tag=11)
    print("my rank is ", rank, " ", data.wait(), "  \n")
    print("")
