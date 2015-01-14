#!/usr/bin/python
import math

dp = 16 # Diametral Pitch
teeth = 8
pa = 20 # Pressure Angle


pd = float(teeth/float(dp)) # Pitch Diameter
pr = pd/2 #Pitch Radius

addendum = 1.0/dp
dedendum = 1.157/dp

rootradius = math.cos(pa*2*math.pi/360.0)*pr



print "Pitch Radius: %f"%pr
print "Addendum: %f"%addendum
print "Dedendum: %f"%dedendum
print "Root Radius: %f"%rootradius






