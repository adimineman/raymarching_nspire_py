from PIL import Image, ImageDraw
import random as rand
import math as m
hit = 1e-2
max_dist = 10
max_step = 50

def toRad(x): return x/360*m.pi*2
def toDeg(x): return x/(m.pi*2)*360
def mod(x, y): return (1 if x >= 0 else -1)*(((1 if x >= 0 else -1)*x) % y)
def map(x, xmin, xmax, ymin, ymax): return (x-xmin)/(xmax-xmin)*(ymax-ymin)+ymin

w = int(720)
h = int(w/2)

def circle(x, y, z, r): return m.sqrt(x**2+y**2+z**2)-r
def cube(x, y, z, r,a): return (x**a+y**a+z**a)**(1/a)-r
def more(v1, v2): return (v2+v1)
def less(v1, v2): return -(v2+v1)

def chess(x, y, z, c1, c2): return c1 if (m.floor(x*10)+m.floor(y*10)+m.floor(z*10)) % 2 == 0 else c2
def mapC(c1, c2, p): return (int(map(p, 0, 1, c1[0], c2[0])), int(map(p, 0, 1, c1[1], c2[1])), int(map(p, 0, 1, c1[2], c2[2])))

camera = {"dir": [toRad(0), toRad(90)], "poz": [0, 0, 0], "fovX": toRad(360), "fovY": toRad(180), "back": lambda x, y, z: (int(rand.random())*255,)*3}
objects = [
    [lambda x, y, z:circle(x-2, ((y+1)%2)-1, z, 1),
     lambda x, y, z:mapC((225, 125, 200), (125, 240, 225), (y+1) % 2)
     ],

    [lambda x, y, z:more(z, 5),
     lambda x, y, z:(int(x*x+y*y)*10,)*3
     # chess(x,y,z,(162,240,235),(94,144,78))
     ],
    [lambda x, y, z:less(z, -5),
     lambda x, y, z:chess(x, y, z, (50, 50, 255), (120, 120, 255))],

    [lambda x, y, z:more(y, 5),
     lambda x, y, z:chess(x, y, z, (25, 167, 31), (141, 235, 113))],
    [lambda x, y, z:less(y, -5),
     lambda x, y, z:chess(x, y, z, (226, 66, 168), (90, 121, 161))],

    [lambda x, y, z:more(x, 5),
     lambda x, y, z:chess(x, y, z, (255, 100, 100), (255, 150, 150))],
    [lambda x, y, z:less(x, -5),
     lambda x, y, z:chess(x, y, z, (100, 255, 100), (150, 255, 150))]
]

class ray:
    color = None
    isHit = 0

    def __init__(self, poz, direc, back):
        self.poz = poz
        self.Vx = m.sin(direc[1])*m.cos(direc[0])
        self.Vy = m.sin(direc[1])*m.sin(direc[0])
        self.Vz = m.cos(direc[1])
        self.back = back
        self.dist = 0

    def getDist(self, objects):
        minL = 100
        for ob in objects:
            a = ob[0](self.poz[0], self.poz[1], self.poz[2])
            if a < minL:
                minL = a
                if a < hit:
                    self.isHit = 1
                    self.color = ob[1](self.poz[0], self.poz[1], self.poz[2])
                    break
        self.spd = minL
        self.dist += minL

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
        if not self.isHit:
            self.color = self.back(self.poz[0], self.poz[1], self.poz[2])

def __main__():
    g = Image.new("RGB", (w, h))
    gc = ImageDraw.Draw(g)
    for x in range(w):
        for y in range(h):
            xDir = map(x, 0, w, -camera["fovX"]/2,
            camera["fovX"]/2)+camera["dir"][0]
            yDir = map(y, 0, h, -camera["fovY"]/2,
            camera["fovY"]/2)+camera["dir"][1]
            r = ray(camera["poz"].copy(), [xDir, yDir], camera["back"])
            r.move(objects)
            gc.point((x, y), fill=r.color)
        print(x)
    g.save("render.png", "PNG")
    g.save("render.jpg", "JPEG")


__main__()
