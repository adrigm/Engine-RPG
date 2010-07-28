#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import pygame
from pygame.locals import *

# Constantes


# Clases
# ---------------------------------------------------------------------



# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------

# Carga una imagen transparencia y color tranasparente opcionales.
def load_image(filename, transparent=False, pixel=(0,0)):
        try: image = pygame.image.load(filename)
        except pygame.error, message:
                raise SystemExit, message
        image = image.convert()
        if transparent:
                color = image.get_at(pixel)
                image.set_colorkey(color, RLEACCEL)
        return image

def create_text(texto, posx, posy, color=(255, 255, 255), size=14, font=""):
	"Crea un  sprite y su rect de un texto pasado"
	fuente = pygame.font.Font(font, size)
	salida = pygame.font.Font.render(fuente, texto, 1, color)
	salida_rect = salida.get_rect()
	salida_rect.centerx = posx + salida_rect.w / 2
	salida_rect.centery = posy + salida_rect.h / 2
	return salida, salida_rect

# ---------------------------------------------------------------------

def main():
	pass

if __name__ == '__main__':
	main()
