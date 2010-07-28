#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
from images import create_text
from constants import *

# Constantes


# Clases
# ---------------------------------------------------------------------

# Clase que gestiona el dibujado en pantalla. (todo lo debe dibujar esta clase).
class Camera:
	def __init__(self, map, player):
		pass

	# Devuelve las coedenadas de pantalla de un tile.
	def plot(self, map, f, c):
		x = map.size_tiles[0]*c - self.scrollx
		y = map.size_tiles[1]*f - self.scrolly
		return (x, y)

	# Duvuelve el tile de un punto (x, y) del mapa.
	def mouse_map(self, map, x, y):
		f = (y + self.scrolly) / map.size_tiles[1]
		c = (x + self.scrollx) / map.size_tiles[0]
		return [f, c]

	# Dibuja en pantalla todo lo necesario.
	def update(self, screen, map, player):
		# Centro como referencia para el scroll apartir de la esquina inferior izquierda del tile del player.
		self.centro = (player.rect.left, player.rect.top+map.size_tiles[1])
		# Definimos el scroll en los dos ejes.
		self.scrollx = self.centro[0] - WIDTH/2
		self.scrolly = self.centro[1] - HEIGHT/2

		# Comprobamos que el scroll no se sale del mapa.
		if self.scrollx < 0:
			self.scrollx = 0
		if self.scrollx > map.width*map.size_tiles[0] - WIDTH:
			self.scrollx = map.width*map.size_tiles[0] - WIDTH
		if self.scrolly < 0:
			self.scrolly = 0
		if self.scrolly > map.height*map.size_tiles[1] - HEIGHT:
			self.scrolly = map.height*map.size_tiles[1] - HEIGHT

		# Buscamos el cuadro superior-izquierdo, superior-derecho e inferior derecho de la pantalla.
		# con esto definimos el rango que debe de tiles que debe ser dibujado.
		inicial = self.mouse_map(map, 0, 0)
		lim_right = self.mouse_map(map, WIDTH, 0)
		lim_bottom = self.mouse_map(map, 0, HEIGHT)

		# Corrección de los límites del mapa para que no dibuje el siguiente tile (no existe).
		if lim_right[1] >= map.width:
			lim_right[1] -= 1
		if lim_bottom[0] >= map.height:
			lim_bottom[0] -= 1

		# Dibujamos todo lo que tiene prioridad inferior a los eventos.
		for f in range(inicial[0], lim_bottom[0]+1):
			for c in range(inicial[1], lim_right[1]+1):
				for i in range(len(map.tiles[f][c].priority)):
					if map.tiles[f][c].priority[i] == 0:
						if map.tiles[f][c].images[i]:
							screen.blit(map.tiles[f][c].images[i], self.plot(map, f, c))

		# Dibujamos los eventos y los tiles con su misma prioridad.
		for f in range(inicial[0], lim_bottom[0]+1):
			for c in range(inicial[1], lim_right[1]+1):
				draw = 1
				for i in range(len(map.tiles[f][c].priority)):
					if player.pos == [f, c]:
						if draw: # Necesario para que los eventos solo se dibujen una vez
							screen.blit(player.image, (player.rect.left-self.scrollx, player.rect.top-self.scrolly))
							draw = 0
						# Fix redibujando el tile de la izquierda del heroe.
						if map.tiles[f][c-1].priority[i] == 1:
							screen.blit(map.tiles[f][c-1].images[i], self.plot(map, f, c-1))
					if map.tiles[f][c].priority[i] == 1:
						screen.blit(map.tiles[f][c].images[i], self.plot(map, f, c))

		# Dibujamos los tiles de mayor prioridad.
		for f in range(inicial[0], lim_bottom[0]+1):
			for c in range(inicial[1], lim_right[1]+1):
				for i in range(len(map.tiles[f][c].priority)):
					if map.tiles[f][c].priority[i] > 1:
						screen.blit(map.tiles[f][c].images[i], self.plot(map, f, c))

	def show_fps(self, screen, fps):
		ifps, ifps_r = create_text(str("FPS: "+str(fps)), 5, 5, font="resources/graphics/DroidSans.ttf")
		screen.blit(ifps, ifps_r)

# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------

def main():
	pass

if __name__ == '__main__':
	main()
