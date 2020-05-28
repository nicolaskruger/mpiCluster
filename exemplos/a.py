from mpi4py import MPI
import cv2 
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
#img = cv2.imread("./../data/imageTeste00.jpg")
print(rank)