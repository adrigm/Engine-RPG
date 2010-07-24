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

def ordenar(a, b):
	intercambios=1
	pasada=1
	while pasada<len(a) and intercambios==1:
		intercambios=0
		for i in range(0,len(a)-pasada):
			if a[i] > a[i+1]:
				a[i], a[i+1] = a[i+1], a[i]
				b[i], b[i+1] = b[i+1], b[i]
				intercambios=1
		pasada += 1
	return b


# ---------------------------------------------------------------------

def main():
	a = [2, 5, 1, 4, 3]
	b = ['e', 'u', 'a', 'o', 'i']
	a = ordenar(a, b)
	print a

if __name__ == '__main__':
	main()
