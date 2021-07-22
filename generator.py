# This is the code used to visualize the giant impact simulation ran on a modified Athena++
# using VisIt's command line.  Note that this will only work on VisIt versions 3.1.4 and greater.
# The code assumes there are 677 dump files of just the density, labeled impact.d.%05d.athdf.xdmf,
# and 3 dump files of all primative variables, labeled impact.f.%05d.athdf.xdmf, and that the simulation
# was run over a time of 2700 seconds.



# A result of the timestep of the dump files being close to the timestep of the simulation is
# that the dump files are outputted at irregular intervals.  The following functions fit the 
# dump files to a linear time progression.
def closer(in1, in2, in3):
  if (abs(in1-in2) < abs(in1-in3)):
  	return False
  return True

array = []
for i in range(0,677): 
    f = open("FILE\\LOCATION\\impact.d.{:05d}.athdf.xdmf".format(i), "r")
    for position, line in enumerate(f):
        if position ==5:
            l = line
    array.append(float(l.split('"')[1]))
array2 = []    
for i in range(1,1351):
	j = 0
	while(closer(2*i-1, array[j], array[j+1])):
		j += 1
	array2.append(j)


# Initialization of the volume plot, magnetic field lines, and annotations.
OpenDatabase("FILE\\LOCATION\\impact.f.00000.athdf.xdmf")
DeleteAllPlots()
AddPlot("Volume", "rho")
vv = VolumeAttributes()
vv.colorControlPoints.AddControlPoints(ColorControlPoint())
vv.colorControlPoints.AddControlPoints(ColorControlPoint())
vv.colorControlPoints.GetControlPoints(0).colors = (0, 0, 0, 0)
vv.colorControlPoints.GetControlPoints(0).position = .2
vv.colorControlPoints.GetControlPoints(1).colors = (30, 20, 0, 3)
vv.colorControlPoints.GetControlPoints(1).position = 0.6
vv.colorControlPoints.GetControlPoints(2).colors = (50, 30, 0, 10)
vv.colorControlPoints.GetControlPoints(2).position = 0.65
vv.colorControlPoints.GetControlPoints(3).colors = (100, 50, 0, 50)
vv.colorControlPoints.GetControlPoints(3).position = 0.8
vv.colorControlPoints.GetControlPoints(4).colors = (255, 255, 100, 100)
vv.colorControlPoints.GetControlPoints(4).position = 0.86
vv.colorControlPoints.GetControlPoints(5).colors = (255, 255, 100, 230)
vv.colorControlPoints.GetControlPoints(5).position = 0.9
vv.colorControlPoints.GetControlPoints(6).colors = (190, 50, 10, 253)
vv.colorControlPoints.GetControlPoints(6).position = 0.92
vv.opacityMode = vv.ColorTableMode
vv.scaling = vv.Log
vv.resampleTarget = 10000000
vv.useColorVarMin = 1
vv.useColorVarMax = 1
vv.colorVarMin = .00000001
vv.colorVarMax = 7.5
vv.lightingFlag = 0
SetActivePlots(0)
SetPlotOptions(vv)
DefineVectorExpression("bfield", "{Bcc1,Bcc2,Bcc3}")
AddPlot("Pseudocolor", "bfield")
AddOperator("IntegralCurve")
ic = IntegralCurveAttributes()
ic.sourceType = ic.SpecifiedSphere
ic.radius = 2000000000
ic.sphereOrigin = (512000000, -121000000, 0)
ic.sampleDensity0 = 3
ic.sampleDensity1 = 3
ic.sampleDensity2 = 3
ic.integrationDirection = ic.Both
ic.dataValue = ic.Solid
SetOperatorOptions(ic)
c = PseudocolorAttributes()
c.colorTableName = "xray"
c.opacityType = c.Constant	
c.opacity = 0
SetPlotOptions(c)
a = AnnotationAttributes()
a.gradientColor1 = (71, 71, 71, 255)
a.gradientColor2 = (0, 0, 0, 255)
a.backgroundMode = a.Gradient
a.axes3D.visible = 0
a.userInfoFlag = 0
a.databaseInfoFlag = 0
a.timeInfoFlag = 0
a.axesArray.visible = 0
a.axes3D.bboxFlag = 0
a.axes3D.triadFlag = 0
a.legendInfoFlag = 0
a.foregroundColor = (255, 255, 255, 255)
SetAnnotationAttributes(a)
DrawPlots()

# camera initialization
# The way the camera angle was set throughout this visualization was through setting the normal vector
# in spherical coordinates, with the variable p being phi and t being theta. p maintains a constant
# speed as the camera pans around, while t oscillates up and down following a sinusoid defined by the
# variable tt, which increases at constant speeds. The sinusoid changes throughout the visualization to
# fit the intended camera motion.  The zoom functions in a similar way to theta.
import math
SetActivePlots(1)
ResetView()
v = GetView3D()
v.focus = (512251000, -121864000, 0)
v.viewUp = (0, 0, 1)
swatts = SaveWindowAttributes()
swatts.resConstraint = swatts.NoConstraint
swatts.family = 0
swatts.width = 1024
swatts.height = 768
z=0
file_idx = 0
p = -.35*math.pi
tt = 00
t = math.pi/2 - .5*math.cos(tt)
c = PseudocolorAttributes()
c.opacityType = c.Constant		
c.colorTableName = "xray"
c.opacity = 0.01
SetPlotOptions(c)
HideActivePlots()
# Initial panning of camera
TimeSliderSetState(1)
for i in range(0,751):
	p += math.pi/400
	z += math.pi/400
	tt += math.pi/800
	t = math.pi/2 - .5*math.cos(tt)
	v.imageZoom = 2.8 + .5*math.cos(z)
	v.viewNormal = (math.cos(p)*math.sin(t), math.sin(p)*math.sin(t), math.cos(t))
	SetView3D(v)
	swatts.fileName = "giant_impact_%04d.png" % file_idx
	SetSaveWindowAttributes(swatts)
	SaveWindow()
	file_idx +=1
HideActivePlots()
for i in range(0,49):
	p += math.pi/400
	z += math.pi/400
	tt += math.pi/800
	t = math.pi/2 - .5*math.cos(tt)
	v.imageZoom = 2.8 + .5*math.cos(z)
	v.viewNormal = (math.cos(p)*math.sin(t), math.sin(p)*math.sin(t), math.cos(t))
	c.opacity += .007
	SetPlotOptions(c)
	SetView3D(v)	
	swatts.fileName = "giant_impact_%04d.png" % file_idx
	SetSaveWindowAttributes(swatts)
	SaveWindow()
	file_idx +=1
for i in range(0,951):
	p += 5*math.pi/1951
	z += 2*math.pi/1951
	tt += 2*math.pi/1951
	t = (math.pi/2+.5-.95) - .95*math.cos(tt)
	v.imageZoom = 2.8 + .5*math.cos(z)
	v.viewNormal = (math.cos(p)*math.sin(t), math.sin(p)*math.sin(t), math.cos(t))
	SetView3D(v)
	swatts.fileName = "giant_impact_%04d.png" % file_idx
	SetSaveWindowAttributes(swatts)
	SaveWindow()
	file_idx +=1
for i in range(0,49):
	p += 5*math.pi/1951*(1-i/48)
	z += 2*math.pi/1951*(1-i/48)
	tt += 2*math.pi/1951*(1-i/48)
	t = (math.pi/2+.5-.95) - .95*math.cos(tt)
	v.imageZoom = 2.8 + .5*math.cos(z)
	v.viewNormal = (math.cos(p)*math.sin(t), math.sin(p)*math.sin(t), math.cos(t))
	c.opacity -= .007	
	SetPlotOptions(c)
	SetView3D(v)
	swatts.fileName = "giant_impact_%04d.png" % file_idx
	SetSaveWindowAttributes(swatts)
	SaveWindow()
	file_idx +=1
SetActivePlots(1)
HideActivePlots()
SetView3D(v)
for i in range(0,10):
	swatts.fileName = "giant_impact_%04d.png" % file_idx
	SetSaveWindowAttributes(swatts)
	SaveWindow()
	file_idx +=1
DeleteAllPlots()

# Time Evolution
OpenDatabase("FILE\\LOCATION\\impact.d.*.athdf.xdmf database")
AddPlot("Volume", "rho")
SetPlotOptions(vv)
DrawPlots()
SetView3D(v)
for i in range(1,len(array2)):
	if file_idx > 2072:
		TimeSliderSetState(array2[i])
		swatts.fileName = "giant_impact_%04d.png" % file_idx
		SetSaveWindowAttributes(swatts)
		SaveWindow()
	file_idx +=1
TimeSliderSetState(675)
swatts.fileName = "giant_impact_%04d.png" % file_idx
SetSaveWindowAttributes(swatts)
SaveWindow()
file_idx +=1
z = 0
tt = 0
DeleteAllPlots()

#Final panning of camera
OpenDatabase("FILE\\LOCATION\\impact.f.00002.athdf.xdmf")
AddPlot("Volume", "rho")
SetPlotOptions(vv)
AddPlot("Pseudocolor", "bfield")
SetActivePlots(1)
AddOperator("IntegralCurve")
SetOperatorOptions(ic)
SetPlotOptions(c)
DrawPlots()
for i in range(0,49):
	p += math.pi/400*i/98
	tt += math.pi/400
	t = (math.pi/2-.3) - 1.1 * math.cos(tt)
	z += math.pi/500
	v.imageZoom = 2+.3*math.cos(z)
	v.viewNormal = (math.cos(p)*math.sin(t), math.sin(p)*math.sin(t), math.cos(t))
	c.opacity += .007
	SetPlotOptions(c)
	SetView3D(v)	
	swatts.fileName = "giant_impact_%04d.png" % file_idx
	SetSaveWindowAttributes(swatts)
	SaveWindow()
	file_idx +=1
for i in range(49,98):
	p += math.pi/400*i/98
	tt += math.pi/400
	t = (math.pi/2-.3) - 1.1 * math.cos(tt)
	z += math.pi/500
	v.imageZoom = 2+.3*math.cos(z)
	v.viewNormal = (math.cos(p)*math.sin(t), math.sin(p)*math.sin(t), math.cos(t))
	SetView3D(v)	
	swatts.fileName = "giant_impact_%04d.png" % file_idx
	SetSaveWindowAttributes(swatts)
	SaveWindow()
	file_idx +=1
for i in range(0,302):
	p += math.pi/400
	tt += math.pi/400
	t = (math.pi/2-.3) -1.1 * math.cos(tt)
	v.viewNormal = (math.cos(p)*math.sin(t), math.sin(p)*math.sin(t), math.cos(t))
	SetView3D(v)
	swatts.fileName = "giant_impact_%04d.png" % file_idx
	SetSaveWindowAttributes(swatts)
	SaveWindow()
	file_idx +=1
for i in range(0,400):
	p += math.pi/400
	tt += math.pi/600
	t = math.pi/2 - .8*math.cos(tt)
	v.viewNormal = (math.cos(p)*math.sin(t), math.sin(p)*math.sin(t), math.cos(t))
	SetView3D(v)
	swatts.fileName = "giant_impact_%04d.png" % file_idx
	SetSaveWindowAttributes(swatts)
	SaveWindow()
	file_idx +=1

# While most parts of this code are easily editable to change the speed of rotation or extrema of the angles,
# this next part smoothly transitions the camera up to view the XY plane and was written in a way that only fits
# the conditions specific to the simulation.  It's pretty sloppy and unsalvageable but got the job done :)
pi = p
while pi > 0:
	pi -= 2*math.pi
pi += 2*math.pi
num = math.ceil((-t)/(.8*math.pi/600*math.sin(tt)))
af = -.0081700430336318*(pi-3.4400439)
zm = v.imageZoom
zm = 1.69 - zm
print(p)
print(t)
print(tt)
print(num)
ttt = t
for i in range(0,50):
	p += (af*(math.exp(-(2*(i-num/2)/num*2*(i-num/2)/num))-math.exp(-1)) + math.pi/800*(1+math.cos(i*math.pi/num)))
	t += (-ttt)/num
	v.focus = (512251000*(1-i/(2*num-2)), -121864000*(1-i/(2*num-2)), 0)
	v.imageZoom += zm/num
	v.viewNormal = (math.cos(p)*math.sin(t), math.sin(p)*math.sin(t), math.cos(t))
	c.opacity -= .007
	SetPlotOptions(c)
	SetView3D(v)	
	swatts.fileName = "giant_impact_%04d.png" % file_idx
	SetSaveWindowAttributes(swatts)
	SaveWindow()
	file_idx +=1
SetActivePlots(1)
HideActivePlots()
for i in range(50,int(num)):
	p += (af*(math.exp(-(2*(i-num/2)/num*2*(i-num/2)/num))-math.exp(-1)) + math.pi/800*(1+math.cos(i*math.pi/num)))
	t += (-ttt*.999)/num
	v.focus = (512251000*(1-i/(num-1)), -121864000*(1-i/(num-1)), 0)
	v.imageZoom += zm/num
	v.viewNormal = (math.cos(p)*math.sin(t), math.sin(p)*math.sin(t), math.cos(t))
	SetView3D(v)	
	swatts.fileName = "giant_impact_%04d.png" % file_idx
	SetSaveWindowAttributes(swatts)
	SaveWindow()
	file_idx +=1
print(p)
print(t)
z = v.imageZoom
ResetView()
v = GetView3D()
v.imageZoom = z
SetView3D(v)
for i in range (0,20):
	swatts.fileName = "giant_impact_%04d.png" % file_idx
	SetSaveWindowAttributes(swatts)
	SaveWindow()
	file_idx +=1
swatts.fileName = "giant_impact_%04d.png" % file_idx
SetSaveWindowAttributes(swatts)
SaveWindow()
file_idx +=1

#Transition to the 2d plot
AddPlot("Pseudocolor", "rho")
AddOperator("Slice")
s = SliceAttributes()
s.normal = (0,0,1)
s.theta = 0
s.phi = 90
s.axisType = s.ZAxis
s.project2d = 0
SetActivePlots(2)
SetOperatorOptions(s)
c2 = PseudocolorAttributes()
c2.colorTableName = "inferno"
c2.minFlag = 1
c2.min = .00001
c2.maxFlag = 1
c2.max = 10
c2.scaling = c2.Log
c2.opacityType = c2.Constant
c2.opacity = 1
SetPlotOptions(c2)
DrawPlots()
for i in range (0,200):
	c2.opacity = float(i*i*i)/200/200/200
	print(c2.opacity)
	SetPlotOptions(c2)
	swatts.fileName = "giant_impact_%04d.png" % file_idx
	SetSaveWindowAttributes(swatts)
	SaveWindow()
	file_idx +=1
c2.opacity = 1
SetPlotOptions(c2)
swatts.fileName = "giant_impact_%04d.png" % file_idx
SetSaveWindowAttributes(swatts)
SaveWindow()
