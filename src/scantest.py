import time

start = time.time()


from mpi4py import MPI
import sys

# from scipy import *

import random


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

total_processors = int(sys.argv[1])
_len = int(sys.argv[2])
_list_of_numbers_original = [x * random.choice([-1, -1, 1, 1, -1, 1, -1, -1, 1, 1]) for x in range(rank * _len, (rank + 1) * _len)]
_list_of_numbers = _list_of_numbers_original[:]  # range(rank * _len, (rank + 1) * _len)


# print(_list_of_numbers)


def compute_sum():
    for i in range(0, _len):
        if i != 0:
            _list_of_numbers[i] = _list_of_numbers[i-1] + _list_of_numbers[i]


compute_sum()

# print(_list_of_numbers)

last_sum = _list_of_numbers[-1]
# print("last_sum is ", last_sum)

for i in range(rank + 1, total_processors):
    comm.isend(last_sum, dest=i, tag=11)

global_dict = {}

# print("entered line 36")
for i in range(0, rank):
    global_dict[i] = comm.irecv(source=i, tag=11)

prefix_sum = 0

for i in range(0, rank):
    prefix_sum = prefix_sum + global_dict[i].wait()

_list_of_numbers_prefix = []

count = 0
for i in _list_of_numbers:
    _list_of_numbers_prefix.append(prefix_sum + i)

# print(str(last_sum) + " " + str(prefix_sum) + "  " + str(_list_of_numbers) + "  " + str(_list_of_numbers_prefix))


maximum = max(_list_of_numbers_prefix)
index_maximum = max(range(len(_list_of_numbers_prefix)), key=_list_of_numbers_prefix.__getitem__) + rank * _len


for i in range(0, rank):
    comm.isend((maximum, index_maximum), dest=i, tag=10)

# print("entered line 61")
dict_maximum = {}
for i in range(rank + 1, total_processors):
    dict_maximum[i] = comm.irecv(source=i, tag=10)

max_after_me = (maximum, index_maximum)
if rank != total_processors - 1:
    max_after_me = (-1000000000000000000000, None)


if rank != total_processors - 1:
    for i in range(rank + 1, total_processors):
        result = dict_maximum[i].wait()
        if result[0] > max_after_me[0]:
            max_after_me = result
else:
    # print("entered line 71")
    """
    This is essentially to fix the config for data
    """
    max_after_me = (_list_of_numbers_prefix[-1], _len - 1 + rank * _len)

# print(str(last_sum) + " " + str(prefix_sum) + "  " + str(_list_of_numbers) + "  " + str(_list_of_numbers_prefix)
#       + " " + str(max_after_me))


counter = _len
_list_u_a_p = []

while counter > 0:
    u = counter - 1 + (rank * _len)
    x = _list_of_numbers_original[counter - 1]
    p = _list_of_numbers_prefix[counter - 1]
    a = max_after_me[1]
    if p > max_after_me[0]:
        # print("entered line 90 ", p, rank)
        max_after_me = (p, u)
        a = u

    b = max_after_me[0] - p + x

    _list_u_a_p.append((u, a, max_after_me[0], p, x, b))

    counter = counter - 1

# print(str(rank) + " " + str(last_sum) + " " + str(prefix_sum) + "  " + str(_list_of_numbers) + "  " + str(_list_of_numbers_prefix)
#       + " " + str(max_after_me) + " " + str(_list_u_a_p) )

# print(str(rank) + " " +str(_list_u_a_p) + "   " + str(max(_list_u_a_p, key=lambda x: x[5])) )

ans = max(_list_u_a_p, key=lambda _li : _li[5])
# print(ans)

_final_dict = {}


# print("entered line 117")
if rank != 0:
    comm.isend(ans, dest=0, tag=8)
else:
    for i in range(rank + 1, total_processors):
        _final_dict[i] = comm.irecv(source=i, tag=8)

end = time.time()


if rank == 0:
    for i in range(rank + 1, total_processors):
        ans = max(ans, _final_dict[i].wait(), key=lambda _li : _li[5])

    print("total_processors is ", total_processors)
    print("length of the list is ", _len)
    print("Final answer in zero is ", (ans[0], ans[1], ans[-1]))
    print("time elapsed is ", end - start)
