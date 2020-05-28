from mpi4py import MPI
import cv2
import os
cv2path = os.path.dirname(cv2.__file__)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
def find(name, path):
    st = "../xml/"
    st+=name
    return st

cascade= [
    "haarcascade_frontalface_alt2.xml",
    "haarcascade_fullbody.xml",
    "haarcascade_lowerbody.xml",
    "haarcascade_upperbody.xml"
]

def dec(i):
    return i-1
def oper():
    global size
    img = cv2.imread("./../data/imageTeste01.jpg")
    comm.bcast(img,root=0)
    rec = []
    for i in range(1,size):
        rec.append(comm.recv(source=i,tag=11))
    for r in rec:
        x,y,w,h =(0,0,0,0)
        if len(r) >= 1: 
            x,y,w,h = r[0]
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255))
    cv2.imwrite("./../data/imageFinal.jpg",img)
def proc():
    global rank
    img = comm.bcast(0,root=0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    xml = find(cascade[dec(rank)],cv2path)
    cfl = cv2.CascadeClassifier(xml)
    detec = cfl.detectMultiScale(gray)
    req= comm.send(detec,dest=0,tag=11)
switc = {
    0: oper,
    1: proc,
    2: proc,
    3: proc,
    4: proc,
}
switc[rank]()
