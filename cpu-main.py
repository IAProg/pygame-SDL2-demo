import pygame, sys
from pygame.locals import *
from entities import *
from config import *
from random import randint
from textureManager import TextureManager as tm

class Game:
	clock = pygame.time.Clock()
	def __init__(self):
		pygame.init()
		pygame.display.set_caption(TITLE)
		flags = pygame.SCALED
		self.surface = pygame.display.set_mode(RESOLUTION, flags)

		self.inputDir = pygame.Vector2(0,0)	
		self.bulletTimer = 0
		self.mineTimer = 0
		self.dt = 0

		tm.load()

		self.player = Player( pygame.Vector2(SCR_W // 2, SCR_H // 2) )
		self.bulletGroup = pygame.sprite.Group()
		self.mineGroup = pygame.sprite.Group()
		self.starGroup = pygame.sprite.Group()
		
		dist = [0] * 1000
		dist = dist + [1] * 5
		dist = dist + [2] * 312
		dist = dist + [3] * 50
		for i in range(len(dist)):
			self.starGroup.add(Star(dist[i]))

		self.mainloop()

	def eventHandle(self):
		for e in pygame.event.get():
			if e.type == QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
				pygame.quit()
				sys.exit()

		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_SPACE] and self.bulletTimer <= 0:
			self.bulletGroup.add(Bullet(self.player.pos.copy(), self.player.vel.copy()))
			self.bulletTimer = COOLDOWN_BULLET
		
		self.inputDir *= 0
		if pressed[pygame.K_a]:
			self.inputDir.x -= 1
		if pressed[pygame.K_d]:
			self.inputDir.x += 1
		if pressed[pygame.K_w]:
			self.inputDir.y -= 1
		if pressed[pygame.K_s]:
			self.inputDir.y += 1
		if abs(self.inputDir.length()) > 0:
			self.inputDir.normalize_ip()

	def spawnMine(self):
		self.mineGroup.add( Mine() )

	def collisionDetect(self):
		for c in pygame.sprite.groupcollide(self.bulletGroup, self.mineGroup, True, True):
			pass #self.score+=Mine.reward
		
		for c in pygame.sprite.groupcollide(self.player, self.mineGroup, False, True):
			pass #self.playerHealth -= 1


	def update(self, dt):
		self.player.update(dt, self.inputDir)
		self.mineGroup.update(dt)
		self.starGroup.update(dt)
		self.bulletGroup.update(dt)

		self.bulletTimer -= dt
		self.mineTimer -= dt

		if self.mineTimer <= 0:
			self.mineTimer = COOLDOWN_MINE
			self.spawnMine()

	def draw(self):
		self.surface.fill(BG_FILL)

		self.starGroup.draw(self.surface)
		self.mineGroup.draw(self.surface)
		self.bulletGroup.draw(self.surface)
		self.player.draw(self.surface)
		
		pygame.display.flip()

	def mainloop(self):
		while True:
			dt = Game.clock.tick() / 1000 
			self.collisionDetect()
			self.eventHandle()
			self.update(dt)
			self.draw()
			print(Game.clock.get_fps())

if __name__ == "__main__":
	game = Game()
