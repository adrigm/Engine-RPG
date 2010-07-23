#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import base64
import gzip
import StringIO
import copy
from xml.dom import minidom, Node

from constants import *
from images import load_image

# Constantes

# Clases
# ---------------------------------------------------------------------

class Tile:
	def __init__(self):
		self.images = []
		self.priority = []
		self.lock = []
		self.event = 0

class Map:
	def __init__(self, name):
		self.name = name
		self.layers = []
		
		self.load_map()
		
		self.load_tileset()
		
		self.create_map()
		
		self.tiles()
		print self.tiles[0][0].lock
		
	def tiles(self):
		self.tiles = range(self.height)
		for i in range(self.height):
			self.tiles[i] = range(self.width)
		
		for f in range(self.height):
			for c in range(self.width):
				self.tiles[f][c] = Tile()
				for i in range(len(self.layers)):
					self.tiles[f][c].images.append(self.map[i][f][c])
					self.tiles[f][c].priority.append(self.priority[self.layers[i][f][c]])
				if self.lock[self.layers[-1][f][c]]:
					self.tiles[f][c].lock = self.lock[self.layers[-1][f][c]]
				else:
					self.tiles[f][c].lock = [1, 1, 1, 1]
		
	# Convierte coordenadas globales a unidades de mapa
	def convert_unit(self, pos):
		f = pos[0]/self.size_tiles[1]
		c = pos[1]/self.size_tiles[0]
		return [f, c]
	
	# Extrae la información del tileset y su archivo de configuración
	def load_tileset(self):
		
		self.tileset = cut_tileset("resources/graphics/tilesets/"+self.name_tileset, self.size_tiles)
		
		xmlMap = minidom.parse("resources/graphics/tilesets/config_"+quit_extension(self.name_tileset)+".tmx")
		mainNode = xmlMap.childNodes[0]
		
		for i in range(len(mainNode.childNodes)):
			if mainNode.childNodes[i].nodeType == 1:
				if mainNode.childNodes[i].nodeName == "layer" and mainNode.childNodes[i].attributes.get("name").value != "tileset":
					layer = mainNode.childNodes[i].childNodes[1].childNodes[0].data.replace("\n", "").replace(" ", "")
					layer = decode(layer) # Decodifica la lista
					layer = [None] + layer
					if mainNode.childNodes[i].attributes.get("name").value == "lock":
						for j in range(len(layer)):
							if layer[j] == 0:
								layer[j] = [1, 1, 1, 1]
							elif layer[j] == 2:
								layer[j] = [0, 0, 0, 0]
							elif layer[j] == 25:
								layer[j] = [0, 1, 1, 1]
							elif layer[j] == 26:
								layer[j] = [1, 0, 1, 1]
							elif layer[j] == 27:
								layer[j] = [1, 1, 0, 1]
							elif layer[j] == 28:
								layer[j] = [1, 1, 1, 0]
							elif layer[j] == 29:
								layer[j] = [1, 0, 0, 0]
							elif layer[j] == 30:
								layer[j] = [0, 1, 0, 0]
							elif layer[j] == 31:
								layer[j] = [0, 0, 1, 0]
							elif layer[j] == 32:
								layer[j] = [1, 0, 0, 1]
							elif layer[j] == 33:
								layer[j] = [1, 0, 1, 0]
							elif layer[j] == 34:
								layer[j] = [0, 1, 0, 1]
							elif layer[j] == 35:
								layer[j] = [1, 0, 0, 1]
							elif layer[j] == 36:
								layer[j] = [0, 0, 1, 1]
							elif layer[j] == 37:
								layer[j] = [1, 1, 0, 0]
							elif layer[j] == 38:
								layer[j] = [0, 1, 1, 0]
							elif layer[j] == 39:
								layer[j] = [1, 1, 1, 1]
						self.lock = layer
					if mainNode.childNodes[i].attributes.get("name").value == "priority":
						for j in range(len(layer)):
							if layer[j] == 17:
								layer[j] = 1
							elif layer[j] == 18:
								layer[j] = 2
							elif layer[j] == 19:
								layer[j] = 3
							elif layer[j] == 20:
								layer[j] = 4
							elif layer[j] == 21:
								layer[j] = 5
						self.priority = layer
		
	# Extrae valores mapa desde XML.	
	def load_map(self):
		xmlMap = minidom.parse("maps/"+self.name)
		mainNode = xmlMap.childNodes[0]
		
		# Tamaño mapa
		self.width = int(mainNode.attributes.get("width").value)
		self.height = int(mainNode.attributes.get("height").value)
		self.size_map = (self.width, self.height)
		
		for i in range(len(mainNode.childNodes)):
			if mainNode.childNodes[i].nodeType == 1:
				if mainNode.childNodes[i].nodeName == "tileset":
					width = mainNode.childNodes[i].attributes.get("tilewidth").value
					height = mainNode.childNodes[i].attributes.get("tileheight").value
					name = mainNode.childNodes[i].childNodes[1].attributes.get("source").value
					name = extract_name(name)
					self.name_tileset = name
					self.size_tiles = (int(width), int(height))
				if mainNode.childNodes[i].nodeName == "layer":
					layer = mainNode.childNodes[i].childNodes[1].childNodes[0].data.replace("\n", "").replace(" ", "")
					layer = decode(layer) # Decodifica la lista
					layer = convert(layer, self.width) # Convierta en array bidimensional
					self.layers.append(layer)
				if mainNode.childNodes[i].nodeName == "objectgroup":
					for j in range(len(mainNode.childNodes[i].childNodes)):
						event = {}
						event['map'] = quit_extension(self.name)
						if mainNode.childNodes[i].childNodes[j].nodeType == 1:
							for attrib in mainNode.childNodes[i].childNodes[j].attributes.keys():
								if attrib == 'name' or attrib == 'type':
									event[attrib] = mainNode.childNodes[i].childNodes[j].attributes.get(attrib).value
								else:
									event[attrib] = int(mainNode.childNodes[i].childNodes[j].attributes.get(attrib).value)
							f = event['y']
							c = event['x']
							event['pos'] = self.convert_unit((f, c))
							del event['x']
							del event['y']
						if mainNode.childNodes[i].childNodes[j].childNodes:
							for k in range(len(mainNode.childNodes[i].childNodes[j].childNodes[1].childNodes)):
								if mainNode.childNodes[i].childNodes[j].childNodes[1].childNodes[k].nodeType == 1:
									key = mainNode.childNodes[i].childNodes[j].childNodes[1].childNodes[k].attributes.get('name').value
									value = mainNode.childNodes[i].childNodes[j].childNodes[1].childNodes[k].attributes.get('value').value
									event[key] = value
						if len(event) > 1:
							events.append(event)
	
	# Crea el mapa.			
	def create_map(self):
		self.map = copy.deepcopy(self.layers)
		for i in range(len(self.layers)):
			for f in range(self.height):
				for c in range(self.width):
					if self.layers[i][f][c]:
						self.map[i][f][c] = self.tileset[self.layers[i][f][c]]
					else:
						self.map[i][f][c] = None
						
	def dibujar_mapa(self, screen):
		for i in range(len(self.layers)):
			for f in range(self.height):
				for c in range(self.width):
					if self.map[i][f][c]:
						screen.blit(self.map[i][f][c], (self.size_tiles[0]*c, self.size_tiles[1]*f))

# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------

# Decodifica una cadena en base64 y luego la descomprime.
def decode(cadena):
	# Decodificar.
	cadena = base64.decodestring(cadena)
	
	# Descomprimir.
	copmressed_stream = StringIO.StringIO(cadena)
	gzipper = gzip.GzipFile(fileobj=copmressed_stream)
	cadena = gzipper.read()
	
	# Convertir.
	salida = []
	for idx in xrange(0, len(cadena), 4):
		val = ord(str(cadena[idx])) | (ord(str(cadena[idx + 1])) << 8) | \
		(ord(str(cadena[idx + 2])) << 16) | (ord(str(cadena[idx + 3])) << 24)
		salida.append(val)
		
	return salida

# Convierta una array unidimensional en una bidimensional.
def convert(lista, col):
	nueva = []
	for i in range(0, len(lista), col):
		nueva.append(lista[i:i+col])
	return nueva

# Extra el name de un archivo de una ruta.	
def extract_name(ruta):
	a = -1
	for i in range(len(ruta)):
		if ruta[i] == "/" or ruta[i] == "\\":
			a = i
	if a == -1:
		return ruta
	return ruta[a+1:]

# Quita la extensión a un archivo.	
def quit_extension(archivo):
	for i in range(len(archivo)):
		if archivo[i] == ".":
			a = i
	return archivo[:a]

# Corta un tilest y lo almacena en un array unidimensional.  
def cut_tileset(ruta, (w, h)):
	image = load_image(ruta, True)
	rect = image.get_rect()
	col = rect.w / w
	fil = rect.h / h
	sprite = [None]
		
	for f in range(fil):
		for c in range(col):
			sprite.append(image.subsurface((rect.left, rect.top, w, h)))
			rect.left += w
		rect.top += h
		rect.left = 0
		
	return sprite

# ---------------------------------------------------------------------

def main():
	return 0

if __name__ == '__main__':
	main()
