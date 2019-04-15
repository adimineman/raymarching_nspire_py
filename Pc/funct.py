import math as m


def toRad(x): return x/360*m.pi*2


def toDeg(x): return x/(m.pi*2)*360


def mod(x, y): return (1 if x >= 0 else -1)*(((1 if x >= 0 else -1)*x) % y)


def map(x, xmin, xmax, ymin, ymax): return (
    x-xmin)/(xmax-xmin)*(ymax-ymin)+ymin


def const(x, minX, maxX): return min(maxX, max(x, minX))


def circle(x, y, z, r): return m.sqrt(x**2+y**2+z**2)-r


def cube(x, y, z, r, a): return (x**a+y**a+z**a)**(1/a)-r


def more(v1, v2): return (v2+v1)


def less(v1, v2): return -(v2+v1)


def chess(x, y, z, c1, c2): return c1 if (
    m.floor(x*10)+m.floor(y*10)+m.floor(z*10)) % 2 == 0 else c2


def mapC(c1, c2, p):
    p = const(p, 0, 1)
    return (int(map(p, 0, 1, c1[0], c2[0])), int(map(p, 0, 1, c1[1], c2[1])), int(map(p, 0, 1, c1[2], c2[2])))
