import pygame
from pygame.locals import *

from rt import RayTracer
from figures import *
from lights import *
from materials import *
from constants import *
from obj import *
width = 400
height = 400

pygame.init()

screen = pygame.display.set_mode((width,height),pygame.DOUBLEBUF|pygame.HWACCEL|pygame.HWSURFACE)
screen.set_alpha(None)

raytracer = RayTracer(screen)
raytracer.envMap = pygame.image.load("textures/hell.bmp")
vpWith= raytracer.envMap.get_width()
vpHeigt= raytracer.envMap.get_height()
raytracer.lights.append(AmbientLight(color=(1,1,1),intensity=0.1))
raytracer.lights.append(DirectionalLight(direction=(0,0,-1),intensity=0.3,color=(1,1,1)))
raytracer.lights.append(DirectionalLight(direction=(-1,-1,-1),intensity=0.4,color=(1,1,0)))
raytracer.lights.append(DirectionalLight(direction=(1,-1,-1),intensity=0.4,color=(1,0,0)))
raytracer.lights.append(DirectionalLight(direction=(0,-1,0),intensity=0.4,color=(1,0,0)))
raytracer.lights.append(PointLight(point=(0,0,-7),intensity=500,color=(0,0,1)))
raytracer.camPosition = [0,0,3]
hex = Obj3D('skull_low.obj',material=glass,scale=(0.2,0.2,0.2),translate=(0,0,-10))
raytracer.scene.append(hex)
raytracer.scene.append(Cube(position=(0,-6,-8),size=(8,4,4),material=Hard_ROCK))
raytracer.scene.append(Cube(position=(0,-4,-10),size=(1,4,1),material=GOLD))
raytracer.scene.append(Sphere(material=earth,position=(-4,0,-7),radius=1))
raytracer.scene.append(Sphere(material=diamond,position=(-2,4,-7),radius=1))
raytracer.scene.append(Sphere(material=fire,position=(4,0,-7),radius=1))
raytracer.scene.append(Sphere(material=mirror,position=(2,4,-7),radius=1))
raytracer.scene.append(Triangle(material=blueMirror,vertices=[(4,4,-9),(4,-4,-9),(0,0,-10)]))
raytracer.rtClear()
raytracer.rtRender()

print("\nRender Time:",pygame.time.get_ticks()/1000,"secs")

isRunning = True
while isRunning:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False

rect = pygame.Rect(0,0,width,height)
sub = screen.subsurface(rect)
pygame.image.save(sub,"temple_skull_3.jpg")

pygame.quit()