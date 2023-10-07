from materials import *
import pygame
Fire = pygame.image.load("textures/fire.bmp")
jupiter = pygame.image.load("textures/Jupiter.bmp")
rock = pygame.image.load("textures/rock.bmp")
_wall = pygame.image.load("textures/wall.bmp")
_f = pygame.image.load("textures/floor.bmp")
Hard_ROCK = Material(diffuse=(0.5,0.5,0.5),texture=rock,spec=10,Ks=0.05)
wall = Material(diffuse=(0.5,0.5,0.5),texture=_wall,spec=10,Ks=0.05)
grass = Material(diffuse=(0.4,1,0.4),spec=32,Ks=0.1)
water = Material(diffuse=(0.4,0.4,1),spec=256,Ks=0.2)
mirror = Material(diffuse=(0.9,0.9,0.9),spec=64,Ks=0.2,matType=REFLECTIVE)
blueMirror = Material(diffuse=(0.4,0.4,0.9),spec=32,Ks=0.15,matType=REFLECTIVE)
earth = Material(texture = jupiter,spec=64,Ks=0.1,matType=OPAQUE)
floor = Material(texture = _f,spec=64,Ks=0.1,matType=OPAQUE)

glass = Material(diffuse=(0.9,0.9,0.9),spec=64,Ks=0.15,ior=1.5,matType=TRANSPARENT)
diamond = Material(diffuse=(0.9,0.9,0.9),spec=128,Ks=0.2,ior=2.417,matType=TRANSPARENT)
water = Material(diffuse=(0.4,0.4,0.9),spec=128,Ks=0.2,ior=1.33,matType=TRANSPARENT)
fire = Material(texture=Fire,spec=128,Ks=0.2,ior=1.33,matType=TRANSPARENT)