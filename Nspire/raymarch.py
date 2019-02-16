import nsp as n
import math as m
t=n.Texture
loop=2
paintLoop=0
hit=.1
toRad=lambda x:x/360*m.pi*2
toDeg=lambda x:x/(m.pi*2)*360
mod  =lambda x,y:(1 if x>=0 else -1)*(((1 if x>=0 else -1)*x)%y)
map  =lambda x,xmin,xmax,ymin,ymax:(x-xmin)/(xmax-xmin)*(ymax-ymin)+ymin


camera={"multi":1,"rez":2,"dir":[toRad(0),toRad(90)],"poz":[-3,0,.5],"fov":toRad(90),"Sx":0,"Sy":0,"back":lambda x,y,z:15,"maxStep":20}
objects=[
[lambda x,y,z:((x)**2+mod(y,2)**2+(z)**2)-1,
lambda x,y,z:2**11-1],
[lambda x,y,z:z+1,
lambda x,y,z:31 if (m.floor(x*10)+m.floor(y*10))%2==0 else 2**16-1]
]

def matadd(a,b):
	a=a.copy()
	for y in range(len(b)):
		for x in range(len(b[0])):
			a[y][x]+=b[y][x]
	return a
def matmul(a,b):
	rez=[]
	for i in range(len(b)):
		rez[j]=[]
		for k in range(len(a[0])):
			sum=0
			for i in range(len(a)):
				sum+=a[i][k]*b[j][i]
			rez[j].push(sum)
	return rez

class window:
	def __init__(self,w,h):
		self.width=w
		self.height=h
		self.gc=t(self.width,self.height,None)
		self.gc.fill(0)
	def draw(self):
		global loop
		while loop>0:
			global paintLoop
			for x in range(paintLoop):
				paint(self.gc)
				self.gc.display()
				if loop==0:break
			n.waitKeypress()
			inp=input()
			if inp=="lo":paintLoop=int(eval(input(">")))
			elif inp=="maxS":camera["maxStep"]=int(eval(input(">")))
			elif inp=="reset":
				camera["Sx"]=0
				camera["Sy"]=0
				paintLoop=0
				loop=2
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
	def getDist(self,objects):
		minL=100
		for o in objects:
			a=o[0](self.poz[0],self.poz[1],self.poz[2])
			if a<minL :
				minL=a
				if a<hit:
					self.isHit=1
					self.color=o[1](self.poz[0],self.poz[1],self.poz[2])
					break
		self.spd=minL
	def move(self,objects):
		for a in range(self.maxStep):
			self.getDist(objects)
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
	#if camera["Sy"]==0 and camera["Sx"]==0:gc.fill(0)
	for x in range(camera["multi"]):
		xDir=map(camera["Sx"],0,screen.width,-camera["fov"],camera["fov"])+camera["dir"][0]
		yFov=screen.height/screen.width*camera["fov"]
		yDir=map(camera["Sy"],0,screen.height,-yFov,yFov)+camera["dir"][1]
		r=ray(camera["poz"].copy(),[xDir,yDir],camera["back"],camera["maxStep"])
		r.move(objects)
		gc.setPx(camera["Sx"],camera["Sy"],635219 if r.color==None else r.color)
		camera["Sx"]+=camera["rez"]
		if camera["Sx"]>= screen.width:
			camera["Sx"]=0
			camera["Sy"]+=camera["rez"]
			if camera["Sy"]>=screen.height:
				camera["Sx"]=0
				camera["Sy"]=0
				camera["rez"]=camera["rez"]//2
				if camera["rez"]==0:
					global loop
					loop=0
				break

def main():
	global screen
	screen=window(320,240)
	screen.draw()

def paint(gc):
	render(gc,camera,objects)


main()