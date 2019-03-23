from PIL import Image,ImageDraw
import math as m
loop=1
paintLoop=1
hit=1e-3
max_dist=10
toRad=lambda x:x/360*m.pi*2
toDeg=lambda x:x/(m.pi*2)*360
mod  =lambda x,y:(1 if x>=0 else -1)*(((1 if x>=0 else -1)*x)%y)
map  =lambda x,xmin,xmax,ymin,ymax:(x-xmin)/(xmax-xmin)*(ymax-ymin)+ymin

w=int(500)
h=int(w/2)

circle=lambda x,y,z,r:x**2+y**2+z**2-r**2
cube  =lambda x,y,z,r:x**10+y**10+z**10-r**10
more  =lambda v1,v2:(v2+v1)
less  =lambda v1,v2:-(v2+v1)

chess =lambda x,y,z,c1,c2:c1 if (m.floor(x*10)+m.floor(y*10)+m.floor(z*10))%2==0 else c2
mapC  =lambda c1,c2,p:(int(map(p,0,1,c1[0],c2[0])),int(map(p,0,1,c1[1],c2[1])),int(map(p,0,1,c1[2],c2[2])))

camera={"multi":w*h,"rez":1,"dir":[toRad(0),toRad(90)],"poz":[0,0,0],"fov":toRad(360)/2,"Sx":0,"Sy":0,
        "back":lambda x,y,z:(0,0,0),"maxStep":10}
objects=[
[lambda x,y,z:circle(x+2,y,z,1),
lambda x,y,z:(255,0,0)],#mapC((225,125,200),(125,240,225),(x**2+(y%2-1)**2+(z%2-1)**2)*.50)],

[lambda x,y,z:more(z,5),
lambda x,y,z:chess(x,y,z,(162,240,235),(94,144,78))],
[lambda x,y,z:less(z,-5),
lambda x,y,z:chess(x,y,z,(50,50,255),(120,120,255))],

[lambda x,y,z:more(y,5),
lambda x,y,z:chess(x,y,z,(25,167,31),(141,235,113))],
[lambda x,y,z:less(y,-5),
lambda x,y,z:chess(x,y,z,(226,66,168),(90,121,161))],

[lambda x,y,z:more(x,5),
lambda x,y,z:chess(x,y,z,(255,100,100),(255,150,150))],
[lambda x,y,z:less(x,-5),
lambda x,y,z:chess(x,y,z,(100,255,100),(150,255,150))]
]
'''
def matadd(a,b):
    a=a.copy()
    for y in range(len(b)):
        for x in range(len(b[0])):
            a[y][x]+=b[y][x]
    return a
def matmul(a,b):
    rez=[]
    for j in range(len(b)):
        rez[j]=[]
        for k in range(len(a[0])):
            sum=0
            for i in range(len(a)):
                sum+=a[i][k]*b[j][i]
            rez[j].push(sum)
    return rez
'''
class window:
    def __init__(self,w,h):
        self.width=w
        self.height=h
        self.g=Image.new("RGB",(w,h))
        self.gc=ImageDraw.Draw(self.g)
    def draw(self):
        global loop
        while loop>0:
            global paintLoop
            for x in range(paintLoop):
                paint(self.gc)
                self.g.save("render.png","PNG")
                self.g.save("render.jpg","JPEG")
                if loop==0:break
            inp=input("|")
            if inp=="lo":paintLoop=int(eval(input(">")))
            elif inp=="maxS":camera["maxStep"]=int(eval(input(">")))
            elif inp=="reset":
                camera["Sx"]=0
                camera["Sy"]=0
                paintLoop=0
                loop=2
                self.gc.rectangle((0,0),fill=(0,0,0))
            elif inp=="poz":camera["poz"]=eval(input(">"))
            elif inp=="dir":camera["dir"]=eval(input(">"))
            elif inp=="exe":eval(input(">>>"))
            elif inp=="multi":camera["multi"]=int(eval(input(">")))
            elif inp=="rez":camera["rez"]=int(eval(input(">")))
            elif inp=="fov":camera["fov"]=int(eval(input(">")))
            elif inp=="g":loop=0
            if loop == 1:loop=0

class ray:
    color=None
    isHit=0
    def __init__(self,poz,direc,back,maxStep):
        self.poz=poz
        self.direc=direc
        self.back=back
        self.maxStep=maxStep
        self.dist=0
    def getDist(self,objects):
        minL=100
        for ob in objects:
#            ob=objects[o]
            a=ob[0](self.poz[0],self.poz[1],self.poz[2])
            if a<minL :
                minL=a
                if a<hit:
                    self.isHit=1
                    self.color=ob[1](self.poz[0],self.poz[1],self.poz[2])
#                    if self.color[0]%1!=0 or self.color[1]%1!=0 or self.color[2]%1!=0:print(o)
                    break
        self.spd=minL
        self.dist+=minL
    def move(self,objects):
        for a in range(self.maxStep):
            self.getDist(objects)
            if self.dist>=max_dist:break
            if self.isHit: break
            direc=self.direc
            r=self.spd
            x=r*m.sin(self.direc[1])*m.cos(self.direc[0])
            y=r*m.sin(self.direc[1])*m.sin(self.direc[0])
            z=r*m.cos(self.direc[1])
            self.poz[0]+=x
            self.poz[1]+=y
            self.poz[2]+=z
        if not self.isHit: self.color=self.back(self.poz[0],self.poz[1],self.poz[2])

def render(gc,camera,objects):
    if camera["rez"]<1: camera["rez"]=1
    #if camera["Sy"]==0 and camera["Sx"]==0:gc.fill(0)
    yFov=h/w*camera["fov"]
#    yFov=toRad(180)
    for x in range(camera["multi"]):
        xDir=map(camera["Sx"],0,w,-camera["fov"],camera["fov"])+camera["dir"][0]
        yDir=map(camera["Sy"],0,h,-yFov,yFov)+camera["dir"][1]
        r=ray(camera["poz"].copy(),[xDir,yDir],camera["back"],camera["maxStep"])
        r.move(objects)
        gc.point((camera["Sx"],camera["Sy"]),fill=r.color)
        camera["Sx"]+=camera["rez"]
        if camera["Sx"]>= w:
            camera["Sx"]=0
            camera["Sy"]+=camera["rez"]
            if camera["Sy"]>=h:
                camera["Sx"]=0
                camera["Sy"]=0
                camera["rez"]=camera["rez"]//2
                if camera["rez"]==0:
                    global loop
                    loop=0
                break
        #print(x/camera["multi"]*100)

def __main__():
#    global screen
    screen=window(w,h)
    screen.draw()

def paint(gc):
    render(gc,camera,objects)


__main__()
