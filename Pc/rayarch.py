from PIL import Image, ImageDraw
import math as m
import time as t
from funct import *
hit = 1e-3
max_dist = 30
max_step = 200

w = int(10000)
h = int(w/2)


camera = {"dir": [toRad(0), toRad(90)], "poz": [2, 2, 2], "fovX": toRad(360), "fovY": toRad(180),
          "back": lambda ray: mapC((150,10,150),(0,0,0),const(ray.absMinDist,0,1))}

objects = [
    [lambda ray:circle((ray.poz[0]+2) % 4-2, (ray.poz[1]+2) % 4-2, (ray.poz[2]+2) % 4-2, 1),
     lambda ray:mapC((225, 125, 200), (125, 240, 225), (m.sin(ray.poz[0]*10)*m.sin(ray.poz[1]*10)*m.sin(ray.poz[2]*10))/2+.5)]

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

    def __init__(self, poz, direc, back):
        self.poz = poz
        self.direc = direc
        self.Vx = m.sin(direc[1])*m.cos(direc[0])
        self.Vy = m.sin(direc[1])*m.sin(direc[0])
        self.Vz = m.cos(direc[1])
        self.back = back

    def getDist(self, objects):
        minL = 100
        for ob in objects:
            a = ob[0](self)
            if a < self.absMinDist:self.absMinDist=a
            if a < minL:
                minL = a
                if a < hit:
                    self.isHit = 1
                    self.color = ob[1](self)
                    break
        self.spd = minL

    def move(self, objects):
        for a in range(max_step):
            self.getDist(objects)
            if self.dist >= max_dist:
                break
            if self.isHit:
                break
            r = self.spd
            self.poz[0] += self.Vx*r
            self.poz[1] += self.Vy*r
            self.poz[2] += self.Vz*r
            self.stepsDone += 1
            self.dist += self.spd
        if self.isHit:
            self.color = mapC(self.color, (0, 0, 0),
                              self.stepsDone/300)
        if not self.isHit:
            self.color = self.back(self)


def main():
    g = Image.new("RGB", (w, h))
    gc = ImageDraw.Draw(g)
    startT=t.time()
    for y in range(h):
        for x in range(w):
            xDir = map(x, 0, w, -camera["fovX"]/2,
                       camera["fovX"]/2)+camera["dir"][0]
            yDir = map(y, 0, h, -camera["fovY"]/2,
                       camera["fovY"]/2)+camera["dir"][1]
            r = ray(camera["poz"].copy(), [xDir, yDir], camera["back"])
            r.move(objects)
            gc.point((x, y), fill=r.color)
        print(y, "/", h,"  ~",((t.time()-startT)/(y+1)*(h-y+1)/60))
        if y % (h//10) == 0:
            g.save("render.png", "PNG")
    g.save("render.png", "PNG")
    g.save("render.jpg", "JPEG")


main()
