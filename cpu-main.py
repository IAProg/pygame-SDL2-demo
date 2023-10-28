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

		self.screen = pygame.display.set_mode(RESOLUTION)
		self.inputDir = pygame.Vector2(0,0)	
		self.bulletTimer = 0
		self.mineTimer = 0
		self.dt = 0

		tm.load()

		self.font = pygame.font.SysFont('Verdana', FONT_SIZE)

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
		self.screen.fill(BG_FILL)

		self.background.draw(self.screen)
		self.lagInducer.draw(self.screen)
		self.mineGroup.draw(self.screen)
		self.bulletGroup.draw(self.screen)
		self.player.draw(self.screen)
		self.draw_fps()
		
		pygame.display.flip()

	def mainloop(self):
		while True:
			dt = Game.clock.tick() / 1000 
			self.collisionDetect()
			self.eventHandle()
			self.update(dt)
			self.draw()
	
	def draw_fps(self):
		spriteCount = sum ((
			len(self.background.sprites()),
			len(self.lagInducer.sprites()),
			len(self.bulletGroup.sprites()),
			len(self.mineGroup.sprites()),
			len(self.background.sprites())
		))
		fps = f'{Game.clock.get_fps() :.0f} FPS | {spriteCount} SPRITES'
		tex = self.font.render(fps, False, "green")
		self.screen.blit(tex, (0,0))
		

if __name__ == "__main__":
	game = Game()
