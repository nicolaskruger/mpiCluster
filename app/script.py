from mpi4py import MPI #importando pacate MPI
import cv2 #importando openCV2 parta processamento de imagem
cv2path = ""
comm = MPI.COMM_WORLD #pacote que permite comunicação
rank = comm.Get_rank() #numero do processo rodando
size = comm.Get_size() #quantos processos estão rodando
def find(name, path): #função que indica o caminho do xml
    st = "../xml/"
    st+=name
    return st
cascade= [
    "haarcascade_frontalface_alt2.xml",
    "haarcascade_fullbody.xml",
    "haarcascade_lowerbody.xml",
    "haarcascade_upperbody.xml"
]#indica qual xml a aplicação deve pegar baseada no seu rank

def dec(i):
    return i-1#tranforma o rank no endereç certo dentro do cascade
def oper():#função da aplicação do mestre
    global size
    img = cv2.imread("./../data/imageTeste02.jpg")#le a imagem exemplo
    comm.bcast(img,root=0)#envia ela para todo os nós via broad cast
    rec = []#vetor onde armazena os resultados
    for i in range(1,size):
        rec.append(comm.recv(source=i,tag=11))#recebe os resultados de cada nó
    for r in rec:
        x,y,w,h =(0,0,0,0)
        if len(r) >= 1: 
            x,y,w,h = r[0]
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255))#desenha os resultados na imagem
    cv2.imwrite("./../data/imageFinal.jpg",img)#salva os ressultados em uma outra imagem
def proc():#função dos nós escravos
    global rank
    img = comm.bcast(0,root=0)#rescebe a imagem do mestre
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#muda para tons de sinza
    xml = find(cascade[dec(rank)],cv2path)#pega o xml refente a parte do corpo que cabe a ele
    cfl = cv2.CascadeClassifier(xml)#pega a classificaçao
    detec = cfl.detectMultiScale(gray)#detecta o que se procura na imagem
    req= comm.send(detec,dest=0,tag=11)#envia o resultado para o mestre
switc = {
    0: oper,
    1: proc,
    2: proc,
    3: proc,
    4: proc,
}
switc[rank]()#switch que funciona de acordo com o número da aplicação
