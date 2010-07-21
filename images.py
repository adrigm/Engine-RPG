#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import sys, pygame
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

# ---------------------------------------------------------------------

def main():
	pass

if __name__ == '__main__':
	main()
