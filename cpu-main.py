import pygame, sys
from pygame.locals import *
from entities import *
from config import *
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

		self.background = Background()
		self.lagInducer = LagInducer()
		self.player = Player( pygame.Vector2(SCR_W // 2, SCR_H // 2) )
		self.bulletGroup = pygame.sprite.Group()
		self.mineGroup = pygame.sprite.Group()

		self.mainloop()

	def eventHandle(self):
		for e in pygame.event.get():
			if e.type == QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
				pygame.quit()
				sys.exit()

		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_SPACE] and self.bulletTimer <= 0:
			Bullet(self.bulletGroup, self.player.pos.copy(), self.player.vel.copy())
			self.bulletTimer = COOLDOWN_BULLET

		if pressed[pygame.K_b]:
			self.lagInducer.addSprite()
		
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

	def collisionDetect(self):
		for c in pygame.sprite.groupcollide(self.bulletGroup, self.mineGroup, True, True):
			pass #self.score+=Mine.reward
		
		for c in pygame.sprite.groupcollide(self.player, self.mineGroup, False, True):
			pass #self.playerHealth -= 1


	def update(self, dt):
		self.background.update(dt)
		self.lagInducer.update(dt)
		self.player.update(dt, self.inputDir)
		self.mineGroup.update(dt)
		self.bulletGroup.update(dt)

		self.bulletTimer -= dt
		self.mineTimer -= dt

		if self.mineTimer <= 0:
			self.mineTimer = COOLDOWN_MINE
			Mine(self.mineGroup)

	def draw(self):
		self.surface.fill(BG_FILL)

		self.background.draw(self.surface)
		self.lagInducer.draw(self.surface)
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
