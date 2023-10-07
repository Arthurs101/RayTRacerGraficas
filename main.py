import pygame
from pygame.locals import *

from rt import RayTracer
from figures import *
from lights import *
from materials import *
from constants import *

width = 500
height = 400

pygame.init()

screen = pygame.display.set_mode((width,height),pygame.DOUBLEBUF|pygame.HWACCEL|pygame.HWSURFACE)
screen.set_alpha(None)

raytracer = RayTracer(screen)
raytracer.envMap = pygame.image.load("textures/sword.bmp")

raytracer.lights.append(AmbientLight(color=(1,1,1),intensity=0.2))
raytracer.lights.append(DirectionalLight(direction=(1,0,0),intensity=0.5,color=(1,1,1)))
raytracer.lights.append(DirectionalLight(direction=(-1,0,0),intensity=0.5,color=(1,1,1)))
raytracer.lights.append(DirectionalLight(direction=(0,0,1),intensity=0.5,color=(1,1,1)))
raytracer.lights.append(DirectionalLight(direction=(0,1,0),intensity=0.5,color=(1,1,1)))
raytracer.scene.append(Plane(position=(-3,0,-9),normal=(-1,0,0),material=wall))
raytracer.scene.append(Plane(position=(3,0,-9),normal=(1,0,0),material=wall))
raytracer.scene.append(Plane(position=(0,0,-9),normal=(0,0,1),material=wall))
raytracer.scene.append(Plane(position=(0,3,-9),normal=(0,1,0),material=wall))
raytracer.scene.append(Plane(position=(0,-3,-9),normal=(0,-1,0),material=floor))

raytracer.scene.append(Disc((0, -1, -7),(0,1,0),3,material=diamond))
raytracer.scene.append(Cube((1, -2, -7), (1, 1, 1), material=earth))
raytracer.scene.append(Cube((-1, -2, -7), (1, 1, 1), material=fire))



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
pygame.image.save(sub,"Render_outuput.jpg")

pygame.quit()