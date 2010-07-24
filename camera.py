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
		self.centro = (player.rect.left, player.rect.top+map.size_tiles[1])
		self.scrollx = self.centro[0] - WIDTH/2
		self.scrolly = self.centro[1] - HEIGHT/2
		if self.scrollx < 0:
			self.scrollx = 0
		if self.scrollx > map.width*map.size_tiles[0] - WIDTH:
			self.scrollx = map.width*map.size_tiles[0] - WIDTH
		if self.scrolly < 0:
			self.scrolly = 0
		if self.scrolly > map.height*map.size_tiles[1] - HEIGHT:
			self.scrolly = map.height*map.size_tiles[1] - HEIGHT
			
		inicial = self.mouse_map(map, 0, 0)
		lim_right = self.mouse_map(map, 640, 0)
		lim_bottom = self.mouse_map(map, 0, 480)
		
		if lim_right[1] >= map.width:
			lim_right[1] -= 1
		if lim_bottom[0] >= map.height:
			lim_bottom[0] -= 1
			
		for f in range(inicial[0], lim_bottom[0]+1):
			for c in range(inicial[1], lim_right[1]+1):
				for i in range(len(map.tiles[f][c].priority)):
					if map.tiles[f][c].priority[i] == 0:
						if map.tiles[f][c].images[i]:
							screen.blit(map.tiles[f][c].images[i], self.plot(map, f, c))
		
		for f in range(inicial[0], lim_bottom[0]+1):
			for c in range(inicial[1], lim_right[1]+1):
				for i in range(len(map.tiles[f][c].priority)):
					if player.pos == [f, c]:
						screen.blit(player.image, (player.rect.left-self.scrollx, player.rect.top-self.scrolly))
					if map.tiles[f][c].priority[i] == 1:
						if map.tiles[f][c].images[i]:
							screen.blit(map.tiles[f][c].images[i], self.plot(map, f, c))
				
		for f in range(inicial[0], lim_bottom[0]+1):
			for c in range(inicial[1], lim_right[1]+1):
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
