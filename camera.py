#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import copy

# Constantes


# Clases
# ---------------------------------------------------------------------

class Camera:
	def __init__(self, map):
		self.width = map.width
		self.height = map.height
		self.size_tiles = map.size_tiles
		
		self.level0 = copy.deepcopy(map.layers)
		self.level1 = copy.deepcopy(map.layers)
		
		for i in range(len(map.layers)):
			for f in range(map.height):
				for c in range(map.width):
					if map.priority[map.layers[i][f][c]] != 0:
						self.level1[i][f][c] = map.map[i][f][c]
						self.level0[i][f][c] = None
					else:
						self.level1[i][f][c] = None
						self.level0[i][f][c] = map.map[i][f][c]
						
	def update(self, screen, player):
		for i in range(len(self.level0)):
			for f in range(self.height):
				for c in range(self.width):
					if self.level0[i][f][c]:
						screen.blit(self.level0[i][f][c], (self.size_tiles[0]*c, self.size_tiles[1]*f))
		player.draw(screen)
		
		for i in range(len(self.level0)):
			for f in range(self.height):
				for c in range(self.width):
					if self.level1[i][f][c]:
						screen.blit(self.level1[i][f][c], (self.size_tiles[0]*c, self.size_tiles[1]*f))


# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------



# ---------------------------------------------------------------------

def main():
	pass

if __name__ == '__main__':
	main()
