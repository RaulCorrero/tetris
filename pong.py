import os
import pygame as pg
from numpy.random import randint
from numpy import sin,cos,pi,sqrt,abs

goles_jugador = 0
goles_rival = 0
gol = False

class Oponente(pg.sprite.Sprite):
	
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface([10,100])
		self.image.fill((255,255,255))
		self.rect = self.image.get_rect()
		self.rect.topleft = 40, 200
		self.vel = 0
	
	def update(self):
		a = self.rect.topleft[1]
		b = self.vel
		
		if a+b>10 and a+b<390:
			self.rect = self.rect.move((0,self.vel))

class Jugador(pg.sprite.Sprite):
	
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface([10,100])
		self.image.fill((255,255,255))
		self.rect = self.image.get_rect()
		self.rect.topleft = 750, 200
		self.vel = 0
		
	def update(self):
		a = self.rect.topleft[1]
		b = self.vel
		
		if a+b>10 and a+b<390:
			self.rect = self.rect.move((0,self.vel))

class Pelota(pg.sprite.Sprite):
	
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface([10,10])
		self.image.fill((255,255,255))
		self.rect = self.image.get_rect()
		self.rect.topleft = 395, 245
		self.vel = 8
		self.dire = randint(-50,51)+randint(2)*180
		self.velx = self.vel*cos(self.dire*2*pi/360)
		self.vely = self.vel*sin(self.dire*2*pi/360)
		self.derecha = False
		self.izquierda = False
	
	def update(self):
		global goles_jugador, goles_rival, gol
		if self.rect.topleft[1]+self.vely>480 or self.rect.topleft[1]+self.vely<10: self.vely=-self.vely
		elif self.rect.topleft[0]<0:
			goles_jugador+=1
			gol = True
			self.dire = randint(-50,51)+randint(2)*180
			self.velx = self.vel*cos(self.dire*2*pi/360)
			self.vely = self.vel*sin(self.dire*2*pi/360)
			self.rect.topleft = 395, 245
		elif self.rect.topleft[0]>800:
			goles_rival+=1
			gol = True
			self.dire = randint(-50,51)+randint(2)*180
			self.velx = self.vel*cos(self.dire*2*pi/360)
			self.vely = self.vel*sin(self.dire*2*pi/360)
			self.rect.topleft = 395, 245
		if self.derecha:
			self.velx = -abs(self.velx)
			self.derecha = False
		elif self.izquierda:
			self.velx = abs(self.velx)
			self.izquierda = False
		self.rect = self.rect.move((self.velx,self.vely))
	
	def golpear(self,c):
		self.derecha = True
		ax,ay = self.velx,self.vely
		by=ay+c
		b = sqrt(ax**2+by**2)
		self.vely = self.vel*by/b
		self.velx = self.vel*ax/b
		

def main():
	
	global gol, goles_jugador, goles_rival
	
	pg.init()
	screen = pg.display.set_mode((800,500),pg.SCALED)
	pg.mouse.set_visible(False)
	pg.display.set_caption("Pong")
	
	background = pg.Surface(screen.get_size())
	background = background.convert()
	background.fill((0,102,255))
	borde = pg.Surface((800,10))
	borde.fill((255,255,255))
	background.blit(borde,(0,0))
	background.blit(borde,(0,490))
	
	font = pg.font.Font(None, 64)
	text = font.render("0 : 0", True, (255, 255, 255))
	textpos = text.get_rect(centerx=background.get_width() / 2, y=30)
	background.blit(text, textpos)
	
	
	screen.blit(background, (0,0))
	pg.display.flip()
	
	player = Jugador()
	enemy = Oponente()
	ball = Pelota()
	allsprites = pg.sprite.RenderPlain((player,enemy,ball))
	
	clock = pg.time.Clock()
	going = True
	while going:
		clock.tick(60)
		
		
		for event in pg.event.get():
			if event.type == pg.QUIT: going = False
			if event.type == pg.KEYDOWN and event.key == pg.K_w: player.vel=-5
			elif event.type == pg.KEYDOWN and event.key == pg.K_s: player.vel=5
			if event.type == pg.KEYUP and event.key == pg.K_w and player.vel!=5: player.vel=0
			elif event.type == pg.KEYUP and event.key == pg.K_s and player.vel!=-5: player.vel=0
		
		if ball.rect.colliderect(player.rect): ball.golpear(player.vel)
		elif ball.rect.colliderect(enemy.rect): ball.izquierda = True
		
		if ball.rect.topleft[1]<enemy.rect.topleft[1]: enemy.vel=-5
		elif ball.rect.topleft[1]+100>enemy.rect.topleft[1]: enemy.vel=5
		else: enemy.vel=0
		
		if gol:
			gol = False
			background.fill((0,102,255))
			background.blit(borde,(0,0))
			background.blit(borde,(0,490))
			text = font.render(str(goles_rival)+" : "+str(goles_jugador), True, (255, 255, 255))
			textpos = text.get_rect(centerx=background.get_width() / 2, y=30)
			background.blit(text, textpos)
		
		allsprites.update()
		screen.blit(background, (0,0))
		allsprites.draw(screen)
		pg.display.flip()
	
	pg.quit()

if __name__=="__main__": main()