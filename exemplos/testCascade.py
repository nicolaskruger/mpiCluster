import cv2
import os
def find(name, path):
    # for root, dirs, files in os.walk(path):
    #     if (name in files) or (name in dirs):
    #         return os.path.join(root, name)
    #         # Caso nao encontre, recursao para diretorios anteriores
    # return find(name, os.path.dirname(path))
    st = "../xml/"
    st+=name
    return st
cv2path = os.path.dirname(cv2.__file__)
img = cv2.imread("./../data/imageTeste00.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
xml = find("haarcascade_upperbody.xml",cv2path)
cfl = cv2.CascadeClassifier(xml)
detec = cfl.detectMultiScale(gray)
x,y,w,h =(0,0,0,0)
if len(detec) >= 1: 
    x,y,w,h = detec[0]
cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255))
cv2.imwrite("../data/imageFinal.jpg",img)