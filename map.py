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
	LOCK_NONE=0
	LOCK_ALL=2
	LOCK_U=25
	LOCK_R=26
	LOCK_D=27
	LOCK_L=28
	LOCK_RDL=29
	LOCK_UDL=30
	LOCK_URL=31
	LOCK_RD=32
	LOCK_RL=33
	LOCK_UD=34
	LOCK_RD=35
	LOCK_UR=36
	LOCK_DL=37
	LOCK_UL=38
	LOCK_URDL=39
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
					# Las listas estan definidas así:
					# 1: Paso
					# 0: Bloqueo
					# [Arriba, Derecha, Abajo, Izquierda]
					# Las constantes usan la abreviatura en inglés y en ese orden.
						for j in range(len(layer)):
							if layer[j] == self.__class__.LOCK_NONE:
								layer[j] = [1, 1, 1, 1]
							elif layer[j] == self.__class__.LOCK_ALL:
								layer[j] = [0, 0, 0, 0]
							elif layer[j] == self.__class__.LOCK_U:
								layer[j] = [0, 1, 1, 1]
							elif layer[j] == self.__class__.LOCK_R:
								layer[j] = [1, 0, 1, 1]
							elif layer[j] == self.__class__.LOCK_D:
								layer[j] = [1, 1, 0, 1]
							elif layer[j] == self.__class__.LOCK_L:
								layer[j] = [1, 1, 1, 0]
							elif layer[j] == self.__class__.LOCK_RDL:
								layer[j] = [1, 0, 0, 0]
							elif layer[j] == self.__class__.LOCK_UDL:
								layer[j] = [0, 1, 0, 0]
							elif layer[j] == self.__class__.LOCK_URL:
								layer[j] = [0, 0, 1, 0]
							elif layer[j] == self.__class__.LOCK_RD:
								layer[j] = [1, 0, 0, 1]
							elif layer[j] == self.__class__.LOCK_RL:
								layer[j] = [1, 0, 1, 0]
							elif layer[j] == self.__class__.LOCK_UD:
								layer[j] = [0, 1, 0, 1]
							elif layer[j] == self.__class__.LOCK_RD:
								layer[j] = [1, 0, 0, 1]
							elif layer[j] == self.__class__.LOCK_UR:
								layer[j] = [0, 0, 1, 1]
							elif layer[j] == self.__class__.LOCK_DL:
								layer[j] = [1, 1, 0, 0]
							elif layer[j] == self.__class__.LOCK_UL:
								layer[j] = [0, 1, 1, 0]
							elif layer[j] == self.__class__.LOCK_URDL:
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
