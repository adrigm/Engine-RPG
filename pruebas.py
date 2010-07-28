#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import pygame

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

# ---------------------------------------------------------------------

def main():
	pass
	
	
if __name__ == '__main__':
	pygame.init()
	main()
