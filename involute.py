#!/usr/bin/python
import math

dp = 16 # Diametral Pitch
teeth = 30
pa = 20 # Pressure Angle
bore=2/25.4 # Center bore radius 
printsvg=True
backlash=0.0   #backlash in degrees.  Use positive for exterior spur gears, negative for interior

scale=250.4

def conv(inches):
	return inches*25.4

pd = float(teeth/float(dp)) # Pitch Diameter
pr = pd/2 #Pitch Radius

addendum = 1.0/dp+.01
dedendum = 1.157/dp

rootradius = math.cos(pa*2*math.pi/360.0)*pr
rootcircum=2*math.pi*rootradius

roottan = math.sin(pa*2*math.pi/360.0)*pr
rootangle = pa - 360*roottan/rootcircum 

size= 2.2*(pr+addendum)*scale
offset=size/2

def calcpoint(rad,theta=0):
	global offset
	global scale
	angle,radius=rad
	angle=angle+theta
	return scale*radius*math.cos(angle*math.pi/180.0)+offset,scale*radius*math.sin(angle*math.pi/180.0)+offset

if (pr-dedendum) > rootradius:
	start=pr-dedendum
else:
	start=rootradius
delta= (pr+addendum-start)/float(30)
points=[]
points2=[]


for x in range(0,31):
	tanlength=math.sqrt(  (start+x*delta)**2 - rootradius**2)
	tanangle = rootangle+360*tanlength/rootcircum - 180*math.atan(tanlength/rootradius)/math.pi
	tanangle2 = rootangle-360*tanlength/rootcircum + 180*math.atan(tanlength/rootradius)/math.pi
	points.append((tanangle,start+x*delta))
	points2.append((tanangle2-2*rootangle-backlash+360/(teeth*2.0),start+x*delta))
	
if printsvg:
	print '<?xml version="1.0"?> <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
	print '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="%f" height="%f" >'%(size,size)


	#print '<circle cx="%f" cy="%f" r="%f" stroke="red" stroke-width="1" fill="none" />'%(offset,offset,pr*scale)
	#print '<circle cx="%f" cy="%f" r="%f" stroke="green" stroke-width="1" fill="none" />'%(offset,offset,rootradius*scale)
	print '<circle cx="%f" cy="%f" r="%f" stroke="black" stroke-width="1" fill="none" />'%(offset,offset,(bore)*scale)

	theta=360/float(teeth)
	for i in range(0,teeth):
		print '<path d="M %f,%f     C '%calcpoint(points[0],i*theta),
		for p in points[1:]:
			print "%f, %f "%calcpoint(p,i*theta),
		print '" fill="none" stroke="#000000" stroke-width="1" />'

		print '<path d="M %f,%f     C '%calcpoint(points2[0],i*theta),
		for p in points2[1:]:
			print "%f, %f "%calcpoint(p,i*theta),
		print '" fill="none" stroke="#000000" stroke-width="1" />'
		print '<path d="M%f,%f'%calcpoint(points[-1],i*theta), 
		print 'A %f %f '%((pr+addendum)*scale,(pr+addendum)*scale),
		print '0 0 1 %f %f" fill="none" stroke="#000000" stroke-width="1" />'%calcpoint(points2[-1],i*theta)

	dr=pr-dedendum #dedendum radius
	dedendumpoint1=(points[0][0],dr)
	dedendumpoint2=(points2[0][0],dr)
	for i in range(0,teeth):
		print '<path d="M%f,%f'%calcpoint(dedendumpoint1,(i+1)*theta), 
		print 'A %f %f '%((dr)*scale,(dr)*scale),
		print '0 0 1 %f %f" fill="none" stroke="#000000" stroke-width="1" />'%calcpoint(dedendumpoint2,i*theta)
		print '<line x1="%f" y1="%f" x2="%f" y2="%f" '%(calcpoint(dedendumpoint1,i*theta)+calcpoint(points[0],i*theta))
		print 'style="stroke:#000000;stroke-width:1" />'
		print '<line x1="%f" y1="%f" x2="%f" y2="%f" '%(calcpoint(dedendumpoint2,i*theta)+calcpoint(points2[0],i*theta))
		print 'style="stroke:#000000;stroke-width:1" />'


	print  "</svg>"



else:
	print pr
