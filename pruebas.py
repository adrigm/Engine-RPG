#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import os

# Constantes


# Clases
# ---------------------------------------------------------------------



# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------

def quit_extension(archivo):
	for i in range(len(archivo)):
		if archivo[i] == ".":
			a = i
	return archivo[:a]

# ---------------------------------------------------------------------

def main():
	print quit_extension("prueba.png")

if __name__ == '__main__':
	main()
