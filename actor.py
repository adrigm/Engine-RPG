#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import sys, pygame
from pygame.locals import *

from constants import events
from images import load_image

# Constantes


# Clases
# ---------------------------------------------------------------------

class Actor:
	def __init__(self, map):
		# Buscamos el evento player.
		for i in range(len(events)):
			if events[i]['type'] == 'player':
				event = events[i]
				
		self.pos = event['pos']
		self.fil = int(event['fil'])
		self.col = int(event['col'])
		self.name_chara = event['image']
		
		self.chara = cut_charaset("resources/graphics/charasets/"+self.name_chara, self.fil, self.col)
		self.image = self.chara[0][0]
		self.rect = self.image.get_rect()
		self.rect.centerx = self.pos[1] * map.size_tiles[0] + (map.size_tiles[0]/2) #240
		self.rect.bottom = self.pos[0] * map.size_tiles[1] + map.size_tiles[1]#320
		
		self.unlock = 1
		self.count = 0
		self.look = 0
		self.mov = 0
		self.graph = 0
		self.wait = 0
	
	def mover(self):
		keys = pygame.key.get_pressed()
		if self.unlock:
			if keys[K_LEFT]:
				self.count = 8
				self.unlock = 0
				self.mov = 1
				self.pos[1] -= 1
				return 1
			if keys[K_RIGHT]:
				self.count = 8
				self.unlock = 0
				self.mov = 2
				self.pos[1] += 1
				return 2
			if keys[K_UP]:
				self.count = 8
				self.unlock = 0
				self.mov = 3
				self.pos[0] -= 1
				return 3
			if keys[K_DOWN]:
				self.count = 8
				self.unlock = 0
				self.mov = 0
				self.pos[0] += 1
				return 0
		return -1
	
	def update(self, id):
		# Si no esta mirando para la direccion a caminar, cambiala!
		if self.look != id and id != -1:
			self.image = self.chara[id][0]
			self.look = id
			self.graph = 0
			return 0
		if self.count != 0:
			if self.count % 2 == 0:
				if self.mov == 1:
					self.rect.x -= 8
				elif self.mov == 2:
					self.rect.x += 8
				elif self.mov == 3:
					self.rect.y -= 8
				elif self.mov == 0:
					self.rect.y += 8
			self.count -= 1
		if self.count == 0 and self.unlock == 1:
			if self.wait == 0:
				self.image = self.chara[self.mov][0]
			self.wait -= 1
		if self.count == 0 and self.unlock == 0:
			if self.graph < 3:
				self.graph += 1
			else:
				self.graph = 0
			self.image = self.chara[self.mov][self.graph]
			self.unlock = 1
			self.wait = 4
		
			
		
	def draw(self, screen):
		screen.blit(self.image, self.rect)
		

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

# ---------------------------------------------------------------------

def main():
	heroe = Actor()

if __name__ == '__main__':
	main()
