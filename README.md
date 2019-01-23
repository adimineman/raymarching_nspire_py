# raymarching_nspire_py
This project requires mycro python and ndless on your calculator. It draws a picture on your screen
------------------------------
Objects are defined as an array of arrays witch look like [lambda x,y,z:return distance from object, lambda x,y,z: return color(0b1111111111111111==white)]

commands are:
  poz: set camera pozition [x,y,z]
  dir: set camera direction in radians ([x direction in radians,y direction in radians])
  exe: execute code for debuging (i use exe >>>print(data))
	multi: how many pixels to draw per tick
  rez: set rezolution (how many pixels to skip)
	fov: set fov in radians (you can use toRad(degrees))
	g: exit
