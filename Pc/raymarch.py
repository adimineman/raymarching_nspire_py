from PIL import Image, ImageDraw
import math as m
import time as t
import numpy as np
from funct import *
hit = 1e-5
max_dist = 8
max_step = 200

w = int(2**12)
h = int(w)
global tmp

camera = {"dir": [m.radians(0), m.radians(90)], "poz": [0, 0, 0], "fovX": m.radians(360), "fovY": m.radians(180),
          "back": lambda ray: mapC((150,10,150),(0,0,0),ray.absMinDist)}

objects = [
    [lambda ray:cube(rZm(m.radians(tmp))@np.array(Ladd(Lmod(Ladd(ray.poz,(4,4,1.1)),(0,0,2.2)),(0,0,-1.1))), (1,1,1)),
     lambda ray:chess(rXm(m.radians(45))@np.array(ray.poz),(0,0,0),(200,200,200))],
    #[lambda ray:circle(Ladd(Lmod(Ladd(ray.poz,(-2,1,0)),(0,2,0)),(0,-1,0)), 1),
    # lambda ray:mapC((225, 125, 200), (125, 240, 225), (m.sin(ray.poz[0]*10)*m.sin(ray.poz[1]*10)*m.sin(ray.poz[2]*10))/2+.5)],

    # [lambda ray:more(ray.poz[2], 5+m.cos(ray.poz[0])*m.cos(ray.poz[1])),
    #lambda ray:(int(ray.poz[0]*ray.poz[0]+ray.poz[1]*ray.poz[1])*10,)*3
    # chess(ray.poz[0],ray.poz[1],ray.poz[2],(162,240,235),(94,144,78))
    # ],
    # [lambda ray:less(ray.poz[2], -5),
    # lambda ray:chess(ray.poz[0], ray.poz[1], ray.poz[2], (50, 50, 255), (120, 120, 255))],

    # [lambda ray:more(ray.poz[1], 5),
    # lambda ray:chess(ray.poz[0], ray.poz[1], ray.poz[2], (25, 167, 31), (141, 235, 113))],
    # [lambda ray:less(ray.poz[1], -5),
    # lambda ray:chess(ray.poz[0], ray.poz[1], ray.poz[2], (226, 66, 168), (90, 121, 161))],

    # [lambda ray:more(ray.poz[0], 5),
    # lambda ray:chess(ray.poz[0], ray.poz[1], ray.poz[2], (255, 100, 100), (255, 150, 150))],
    # [lambda ray:less(ray.poz[0], -5),
    # lambda ray:chess(ray.poz[0], ray.poz[1], ray.poz[2], (100, 255, 100), (150, 255, 150))]
]

class ray:
    color = None
    isHit = 0
    dist = 0
    stepsDone = 0
    absMinDist = max_dist

    def __init__(self, poz, vel, back):
        self.poz = poz
        self.vel = vel
        self.back = back

    def getDist(self, objects, mids_d=False):
        minL = 100
        for ob in objects:
            a = ob[0](self)
            if not mids_d and a < self.absMinDist:self.absMinDist=a
            if a < minL:
                minL = a
                if a < hit:
                    self.isHit = 1
                    self.color = ob[1](self)
                    break
        self.spd = minL

    def getNorm(self,objects):
        ppoz=self.poz.copy()
        self.getDist(objects)
        d = self.spd
        e = .001
        n=[]
        for x in range(len(ppoz)):
            self.poz=ppoz.copy()
            self.poz[x]-=e
            self.getDist(objects,True)
            n.append(self.spd)
        n = Laddn(Lmuln(n,-1),d)
        self.poz=ppoz
        return norm(n)

    def move(self, objects):
        for a in range(max_step):
            self.getDist(objects)
            if self.dist >= max_dist:
                break
            if self.isHit:
                break
            r = self.spd
            self.poz=Ladd(self.poz,Lmuln(self.vel,r))
            self.stepsDone += 1
            self.dist += self.spd
        if self.isHit:
            self.color = mapC(self.color, (0, 0, 0),
                              self.stepsDone/200)
        else:
            self.color = self.back(self)


def main(filename:str):
    g = Image.new("RGB", (w, h))
    gc = ImageDraw.Draw(g)
    startT=t.time()
    for y in range(h):
        for x in range(w):
            u = mapr(x, 0, w, -1, 1)
            v = mapr(y, 0, h, -1, 1)
            rotmat=rXm(camera["dir"][1])@rYm(camera["dir"][0])
            r = ray(camera["poz"].copy(), norm(rotmat@np.array((u,v,1))), camera["back"])
            r.move(objects)
            gc.point((x, y), fill=r.color)
        print(filename,y, "/", h,"  ~",((t.time()-startT)/(y+1)*(h-y+1)))
        #if y % (h//10) == 0:
        #    g.save("render.png", "PNG")
    g=g.resize((max(512,w),max(512,h)),resample=Image.NEAREST)
    g.save(filename, "PNG")
    #g.save("render.jpg", "JPEG")


for x in range(0,90,10):
    #global tmp
    camera["dir"][0]=m.radians(-45)
    #camera["dir"][1]=m.radians(90)
    tmp=x
    main("Pc/render/r{:0>5}.png".format(x))