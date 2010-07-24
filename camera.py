#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import copy

from constants import *

# Constantes


# Clases
# ---------------------------------------------------------------------

# Clase que gestiona la pantalla visible.
class Camera:
	def __init__(self, map, player):
		pass
		
	def plot(self, map, f, c):
		x = map.size_tiles[0]*c - self.scrollx
		y = map.size_tiles[1]*f - self.scrolly
		return (x, y)
		
	def mouse_map(self, map, x, y):
		f = (y + self.scrolly) / map.size_tiles[1]
		c = (x + self.scrollx) / map.size_tiles[0]
		return [f, c]
		
						
	def update(self, screen, map, player):
		self.centro = (player.rect.left, player.rect.top)
		self.scrollx = self.centro[0] - WIDTH/2
		self.scrolly = self.centro[1] - HEIGHT/2
		for f in range(map.height):
			for c in range(map.width):
				for i in range(len(map.tiles[f][c].priority)):
					if map.tiles[f][c].priority[i] == 0:
						if map.tiles[f][c].images[i]:
							screen.blit(map.tiles[f][c].images[i], self.plot(map, f, c))
		
		for f in range(map.height):
			for c in range(map.width):
				for i in range(len(map.tiles[f][c].priority)):
					if player.pos == [f, c]:
						screen.blit(player.image, (player.rect.left-self.scrollx, player.rect.top-self.scrolly))
					if map.tiles[f][c].priority[i] == 1:
						if map.tiles[f][c].images[i]:
							screen.blit(map.tiles[f][c].images[i], self.plot(map, f, c))
				
		for f in range(map.height):
			for c in range(map.width):
				for i in range(len(map.tiles[f][c].priority)):
					if map.tiles[f][c].priority[i] > 1:
						if map.tiles[f][c].images[i]:
							screen.blit(map.tiles[f][c].images[i], self.plot(map, f, c))


# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------



# ---------------------------------------------------------------------

def main():
	pass

if __name__ == '__main__':
	main()
