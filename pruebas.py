#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import sys, pygame
from pygame.locals import *
import pytweener

# Constantes
WIDTH = 640
HEIGHT = 480

# Clases
# ---------------------------------------------------------------------

class Chara:
	def __init__(self, x , y):
		self.fil = 4
		self.col = 4
		self.name_chara = 4
		
		self.chara = cut_charaset("resources/graphics/charasets/chara.png", self.fil, self.col)
		self.image = self.chara[0][0]
		
		self.x = x
		self.y = y
		
	def draw(self, screen):
		screen.blit(self.image, (self.x, self.y))
		

# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------

# Corta un chara en las fil y col indicadas. Array Bidimensional.
def cut_charaset(ruta, fil, col):
	image = load_image(ruta, True)
	rect = image.get_rect()
	w = rect.w / col
	h = rect.h / fil
	sprite = range(fil)
	for i in range(fil):
		sprite[i] = range(col)

	for f in range(fil):
		for c in range(col):
			sprite[f][c] = image.subsurface((rect.left, rect.top, w, h))
			rect.left += w
		rect.top += h
		rect.left = 0

	return sprite

def load_image(filename, transparent=False):
        try: image = pygame.image.load(filename)
        except pygame.error, message:
                raise SystemExit, message
        image = image.convert()
        if transparent:
                color = image.get_at((0,0))
                image.set_colorkey(color, RLEACCEL)
        return image
        
def salir():
	keys = pygame.key.get_pressed()
	for eventos in pygame.event.get():
		if eventos.type == QUIT:
			sys.exit(0)
		if keys[K_ESCAPE]:
			sys.exit(0)

# ---------------------------------------------------------------------

def main():
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	
	tweener = pytweener.Tweener()
	
	pygame.display.set_caption("Pruebas Pygame")
	background_image = load_image('fondo.jpg');
	chara = Chara(100, 100)
	x= chara.x
	tweener.addTween(chara, x= x+32)
	
	clock = pygame.time.Clock()
	
	while True:
		time = clock.tick(60)
		tweener.update(time / 1000.0)
		salir()
		screen.blit(background_image, (0, 0))
		chara.draw(screen)
		pygame.display.flip()
	return 0

if __name__ == '__main__':
	pygame.init()
	main()
