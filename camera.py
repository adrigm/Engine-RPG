#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import copy

# Constantes


# Clases
# ---------------------------------------------------------------------

# Clase que gestiona la pantalla visible.
class Camera:
	def __init__(self, map):
		pass
		
						
	def update(self, screen, map, player):
			for f in range(map.height):
				for c in range(map.width):
					for i in range(len(map.tiles[f][c].priority)):
						if map.tiles[f][c].priority[i] == 0:
							if map.tiles[f][c].images[i]:
								screen.blit(map.tiles[f][c].images[i], (map.size_tiles[0]*c, map.size_tiles[1]*f))
			
			for f in range(map.height):
				for c in range(map.width):
					for i in range(len(map.tiles[f][c].priority)):
						if player.pos == [f, c]:
							player.draw(screen)
						if map.tiles[f][c].priority[i] == 1:
							if map.tiles[f][c].images[i]:
								screen.blit(map.tiles[f][c].images[i], (map.size_tiles[0]*c, map.size_tiles[1]*f))
					
			for f in range(map.height):
				for c in range(map.width):
					for i in range(len(map.tiles[f][c].priority)):
						if map.tiles[f][c].priority[i] > 1:
							if map.tiles[f][c].images[i]:
								screen.blit(map.tiles[f][c].images[i], (map.size_tiles[0]*c, map.size_tiles[1]*f))


# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------



# ---------------------------------------------------------------------

def main():
	pass

if __name__ == '__main__':
	main()
