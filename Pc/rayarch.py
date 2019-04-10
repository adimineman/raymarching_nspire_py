from PIL import Image,ImageDraw
import math as m
hit=1e-1
max_dist=20
max_step=50
toRad=lambda x:x/360*m.pi*2
toDeg=lambda x:x/(m.pi*2)*360
mod  =lambda x,y:(1 if x>=0 else -1)*(((1 if x>=0 else -1)*x)%y)
map  =lambda x,xmin,xmax,ymin,ymax:(x-xmin)/(xmax-xmin)*(ymax-ymin)+ymin

w=int(720)
h=int(w/2)

circle=lambda x,y,z,r:(x**2+y**2+z**2)-r**2
cube  =lambda x,y,z,r:x**4+y**4+z**4-r**4
more  =lambda v1,v2:(v2+v1)
less  =lambda v1,v2:-(v2+v1)

chess =lambda x,y,z,c1,c2:c1 if (m.floor(x*10)+m.floor(y*10)+m.floor(z*10))%2==0 else c2
mapC  =lambda c1,c2,p:(int(map(p,0,1,c1[0],c2[0])),int(map(p,0,1,c1[1],c2[1])),int(map(p,0,1,c1[2],c2[2])))

camera={"dir":[toRad(0),toRad(90)],"poz":[0,0,1],"fovX":toRad(360),"fovY":toRad(180),"back":lambda x,y,z:(0,0,0)}
objects=[
[lambda x,y,z:circle(x-2,((y+1)%2)-1,0,1),
lambda x,y,z:mapC((225,125,200),(125,240,225),(y+.5)%1)
],

[lambda x,y,z:more(z,5),
lambda x,y,z:int(x*x+y*y)*100
#chess(x,y,z,(162,240,235),(94,144,78))
],
[lambda x,y,z:less(z,-5),
lambda x,y,z:chess(x,y,z,(50,50,255),(120,120,255))],

[lambda x,y,z:more(y,.5),
lambda x,y,z:chess(x,y,z,(25,167,31),(141,235,113))],
[lambda x,y,z:less(y,-.5),
lambda x,y,z:chess(x,y,z,(226,66,168),(90,121,161))],

[lambda x,y,z:more(x,5),
lambda x,y,z:chess(x,y,z,(255,100,100),(255,150,150))],
[lambda x,y,z:less(x,-5),
lambda x,y,z:chess(x,y,z,(100,255,100),(150,255,150))]
]

class window:
    def __init__(self):
        self.width=w
        self.height=h
        self.g=Image.new("RGB",(w,h))
        self.gc=ImageDraw.Draw(self.g)
    def draw(self):
        render(self.gc,camera,objects)
        self.g.save("render.png","PNG")
        self.g.save("render.jpg","JPEG")

class ray:
    color=None
    isHit=0
    def __init__(self,poz,direc,back):
        self.poz=poz
        self.direc=direc
        self.back=back
        self.dist=0
    def getDist(self,objects):
        minL=100
        for ob in objects:
            a=ob[0](self.poz[0],self.poz[1],self.poz[2])
            if a<minL :
                minL=a
                if a<hit:
                    self.isHit=1
                    self.color=ob[1](self.poz[0],self.poz[1],self.poz[2])
                    break
        self.spd=minL
        self.dist+=minL
    def move(self,objects):
        for a in range(max_step):
            self.getDist(objects)
            if self.dist>=max_dist:break
            if self.isHit: break
            r=self.spd
            x=r*m.sin(self.direc[1])*m.cos(self.direc[0])
            y=r*m.sin(self.direc[1])*m.sin(self.direc[0])
            z=r*m.cos(self.direc[1])
            self.poz[0]+=x
            self.poz[1]+=y
            self.poz[2]+=z
        if not self.isHit: self.color=self.back(self.poz[0],self.poz[1],self.poz[2])

def render(gc,camera,objects):
    for x in range(w):
        for y in range(h):
            xDir=map(x,0,w,-camera["fovX"]/2,camera["fovX"]/2)+camera["dir"][0]
            yDir=map(y,0,h,-camera["fovY"]/2,camera["fovY"]/2)+camera["dir"][1]
            r=ray(camera["poz"].copy(),[xDir,yDir],camera["back"])
            r.move(objects)
            gc.point((x,y),fill=r.color)
        print(x)

def __main__():
    screen=window()
    screen.draw()
__main__()
