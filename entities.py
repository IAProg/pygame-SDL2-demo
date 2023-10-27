import pygame as pg
from pygame.locals import *
from config import *
from random import randint
from textureManager import TextureManager as tm

class Star(pg.sprite.Sprite):
	skins = ["Star1","Star2","Star3","Star4"]
	speed = 2

	def __init__(self, size):
		pg.sprite.Sprite.__init__(self)
		self.dir = pg.Vector2(0, 1)
		self.size = size
		self.image = tm.fetch(Star.skins[self.size])
		self.rect  = self.image.get_rect()

		self.pos = pg.Vector2(randint(0,SCR_W),randint(0,SCR_H))
		self.rect.center = self.pos.xy

	def reset(self):
		self.pos = pg.Vector2(randint(0,SCR_W),-10)
		self.rect.center = self.pos.xy

	def update(self, dt):
		self.pos += (self.dir * Star.speed * (pow(self.size,3)) * dt)
		self.rect.center = self.pos.xy
		if self.pos.y > SCR_H:
			self.reset()

class Mine(pg.sprite.Sprite):
	speed = 40
	reward = 10

	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = tm.fetch("mine")
		self.rect  = self.image.get_rect()
		self.dir = pg.Vector2(0, 1)
		self.pos = pg.Vector2( randint(0,SCR_W),-10 )
		self.rect.center = self.pos.xy


	def update(self, dt):
		self.pos += (self.dir * Mine.speed * dt)
		self.rect.center = self.pos.xy
		if self.pos.y > SCR_H:
			self.kill()

class Bullet(pg.sprite.Sprite):
	speed = -2500

	def __init__(self, pos, playerVel):
		pg.sprite.Sprite.__init__(self)
		self.image = tm.fetch("bullet")
		self.rect  = self.image.get_rect()
		self.vel = playerVel + pg.Vector2(0, Bullet.speed)
		self.rect.center = pos.xy
		self.pos = pos


	def update(self, dt):
		self.pos += (self.vel * dt)
		self.rect.center = self.pos.xy
		if self.pos.y < 0:
			self.kill()

class Player(pg.sprite.GroupSingle):
	moveForce = 4000
	friction = 5

	def __init__(self, pos):
		pg.sprite.GroupSingle.__init__(self)
		self.sprite = pg.sprite.Sprite()
		self.sprite.image = tm.fetch("ship")
		self.sprite.rect = self.sprite.image.get_rect()
		
		self.sprite.rect.center = pos.xy
		self.pos = pos
		self.vel = pg.Vector2()

	def update(self, dt, inputDir = pg.Vector2(0, 0)):
		self.vel += inputDir * Player.moveForce * dt
		self.vel -= self.vel * Player.friction * dt
		self.pos += self.vel * dt
		self.sprite.rect.center = self.pos.xy

