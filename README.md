# raymarching_nspire_py
This project requires mycro python and ndless on your calculator. It draws a picture on your screen
------------------------------
Objects are defined as an array of arrays witch look like [lambda x,y,z:return distance from object, lambda x,y,z: return color(0b1111111111111111==white)]

commands are:<br>
<blockquote>poz: set camera pozition [x,y,z]<br>
dir: set camera direction in radians ([x direction in radians,y direction in radians])<br>
exe: execute code for debuging (i use exe >>>print(data))<br>
multi: how many pixels to draw per tick<br>
rez: set rezolution (how many pixels to skip)<br>
fov: set fov in radians (you can use toRad(degrees))<br>
g: exit<br></blockquote>
