import pathlib
import pygame as pg
from config import *
from pygame._sdl2.video import Texture

class TextureManager:
	textures = {}

	def load():
		paths = [item for item in pathlib.Path(TEXTURE_PATH).rglob('*.png') if item.is_file()]
		for path in paths:
			image = pg.image.load(str(path)).convert_alpha()
			TextureManager.textures[path.stem] = image

	def loadSDL2(renderer):
		paths = [item for item in pathlib.Path(TEXTURE_PATH).rglob('*.png') if item.is_file()]
		for path in paths:
			image = pg.image.load(str(path))
			image = Texture.from_surface(renderer, image)
			TextureManager.textures[path.stem] = image

	def fetch( textureName ):
		if textureName in TextureManager.textures:
			return TextureManager.textures[textureName]

