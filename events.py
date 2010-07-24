#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
from constants import events

# Constantes


# Clases
# ---------------------------------------------------------------------

class Event:
	def __init__(self, id):
		self.id = id
		self.name = events[id]['name']
		self.type = events[id]['type']
		self.pos = events[id]['pos']
		self.map = events[id]['map']
		
		
# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------



# ---------------------------------------------------------------------

def main():
	pass

if __name__ == '__main__':
	main()
