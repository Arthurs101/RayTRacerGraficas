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
raytracer.lights.append(DirectionalLight(direction=(-1,-1,-1),intensity=0.5,color=(1,1,1)))

raytracer.scene.append(Sphere((-0.1,1,-7),1,earth))
raytracer.scene.append(Triangle(material=diamond,vertices=[(-0.2,0.2,-5),(0.2,0.2,-5),(0.0,0.4,-5)]))

raytracer.scene.append(Triangle(material=grass,vertices=[(-0.2,-0.2,-5),(0.2,-0.2,-5),(0.0,-0.4,-5)]))
raytracer.scene.append(Triangle(material=grass,vertices=[(-1,-2,-6),(1,-2,-6),(0.0,0,-5)]))


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