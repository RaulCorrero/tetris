import os, time
import pygame as pg
from numpy.random import randint

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

velocidad_bichos = 1
contador_bichos = 0
direccion_bichos = True ##True es izquierda

total_disparos = 0
nivel = 1
total_vidas = 3 ##maximo para no salir de la pantalla = 6

class Corazon(pg.sprite.Sprite):
	
	def __init__(self,x):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface([50,25])
		self.image.fill((0,51,102))
		player_body = pg.Surface([50,20])
		player_body.fill((255,255,255))
		self.image.blit(player_body,(0,5))
		player_cannon = pg.Surface([10,5])
		player_cannon.fill((255,255,255))
		self.image.blit(player_cannon,(20,0))
		self.rect = self.image.get_rect()
		self.number = x
		self.rect.topleft = 25+x*60, 555
	
	def update(self):
		pass

class Disparo(pg.sprite.Sprite):
	
	def __init__(self,x,y,z):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface([8,25])
		self.image.fill((255,255,255))
		self.rect = self.image.get_rect()
		self.rect.topleft = x, y
		self.z=z
		self.speed = 15
	
	def update(self):
		global total_disparos
		self.rect.y += self.z*self.speed
		if self.rect.y > 520:
			self.kill()
		elif self.rect.y < -20:
			self.kill()
			total_disparos-=1

class Jugador(pg.sprite.Sprite):
	
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface([50,25])
		self.image.fill((0,51,102))
		player_body = pg.Surface([50,20])
		player_body.fill((255,255,255))
		self.image.blit(player_body,(0,5))
		player_cannon = pg.Surface([10,5])
		player_cannon.fill((255,255,255))
		self.image.blit(player_cannon,(20,0))
		self.rect = self.image.get_rect()
		self.rect.topleft = 175, 465
		self.movex = 0
		self.speed = 4
	
	def update(self):
		a = self.rect.x + self.movex
		if a>10 and a<340:
			self.rect.x = a
		
	
	# def draw(self):
		# self.screen.blit(self.image, self.rect)
	
	def mover(self,x):
		self.movex = x*self.speed

class Enemigo(pg.sprite.Sprite):
	
	def __init__(self,x,y,z):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.image.load(os.path.join(data_dir, "alien.png")).convert()
		self.image.set_colorkey(self.image.get_at((0,0)),pg.RLEACCEL)
		self.rect = self.image.get_rect()
		self.rect.topleft= x,y
		self.original = z
	
	def update(self):
		global velocidad_bichos, direccion_bichos
		if direccion_bichos:
			self.rect = self.rect.move([-velocidad_bichos,0])
		else:
			self.rect = self.rect.move([velocidad_bichos,0])

	def reinicializar(self):
		self.rect.topleft= 75+self.original[0]*45,25+self.original[1]*45

class Bloque(pg.sprite.Sprite):

	def __init__(self,x,y):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface([25,25])
		self.image.fill((255,255,255))
		self.rect = self.image.get_rect()
		self.rect.topleft = x,y
	
	def update(self):
		pass

def main():
	global nivel, contador_bichos, velocidad_bichos, total_disparos, direccion_bichos, total_vidas

	pg.init()
	screen = pg.display.set_mode((400,650))
	pg.display.set_caption("Invasores Espaciales")
	
	background = pg.Surface(screen.get_size())
	background = background.convert()
	background.fill((0,51,102))
	borde_inferior = pg.Surface((400,10))
	borde_inferior.fill((255,255,255))
	background.blit(borde_inferior,(0,500))
	background.blit(borde_inferior,(0,300))
	if pg.font:
		font = pg.font.Font(None,32)
		text = font.render("Invasores espaciales | Nivel",True,(255,255,255))
		background.blit(text,(10,520))
		text = font.render("Puntuacion",True,(255,255,255))
		background.blit(text,(10,590))
	screen.blit(background, (0,0))
	pg.display.flip()
	
	player = Jugador()
	
	allsprites = pg.sprite.RenderPlain((player))
	muros = pg.sprite.Group(())
	disparos = pg.sprite.Group(())
	enemigos = pg.sprite.Group(())
	
	
	##DISTINTAS VARIABLES QUE NECESITO
	def niveles(x):
		return(int(1+(int(x))/2), int(2+int(x-1)/2))
	
	puntuacion = 0
	velocidad_bichos = niveles(nivel)[0]
	k = 0
	bajar = False
	perdido = False
	ganado = False
	clock = pg.time.Clock()
	going = True
	reinicia = False
	probabilidad = 180
	
	for i in range(3):
		for j in range(2):
			wall = Bloque(25+20*(i+1),400+20*j)
			wall.add(muros,allsprites)
	
	for i in range(3):
		for j in range(2):
			wall = Bloque(350-20*(i+1),400+20*j)
			wall.add(muros,allsprites)
	
	for i in range(3):
		for j in range(2):
			wall = Bloque(170+20*i,400+20*j)
			wall.add(muros,allsprites)
	
	
	for i in range(6):
		for j in range(3):
			enemy = Enemigo(75+i*45,25+j*45,(i,j))
			enemy.add(enemigos,allsprites)
			contador_bichos+=1
	
	vidas = pg.sprite.Group(())
	for i in range(total_vidas):
		vida = Corazon(i)
		vida.add(vidas,allsprites)
	
	while going: ##AQUI EMPIEZA EL BUCLE DEL JUEGO
		clock.tick(45)
		k+=1
		
		for event in pg.event.get():
			if event.type == pg.QUIT: going = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_LEFT: player.mover(-1)
				if event.key == pg.K_RIGHT: player.mover(1)
				if event.key == pg.K_SPACE:
					if total_disparos<3:
						total_disparos+=1
						shoot = Disparo(player.rect.x+21,player.rect.y,-1)
						shoot.add(disparos,allsprites)
			elif event.type == pg.KEYUP:
				if event.key == pg.K_LEFT and player.movex<0: player.mover(0)
				if event.key == pg.K_RIGHT and player.movex>0: player.mover(0)
		
		for m in muros:
			for j in disparos:
				if j.rect.colliderect(m):
					if j.z==-1: total_disparos-=1
					m.kill()
					j.kill()
		
		for j in disparos:
			if j.rect.colliderect(player) and j.z==1:
				total_vidas-=1
				if total_vidas:
					for corazon in vidas:
						if corazon.number == total_vidas: corazon.kill()
					for d in disparos:
						if d.z==-1: total_disparos-=1
						d.kill()
					for e in enemigos: e.reinicializar()
					time.sleep(2)
					reinicia = True
				else:
					going = False ##TERMINA EL JUEGO CUANDO MUERES
					perdido = True
					if pg.font:
						font = pg.font.Font(None,40)
						text = font.render("HAS SIDO DESTRUIDO",True,(255,255,255))
						background.blit(text,(75,330))
						screen.blit(background,(0,0))
						allsprites.draw(screen)	
						pg.display.flip()
					time.sleep(2)
			for m in enemigos:
				if j.rect.colliderect(m) and j.z==-1:
					m.kill()
					j.kill()
					contador_bichos-=1
					velocidad_bichos = niveles(nivel)[0]*(contador_bichos>9)+niveles(nivel)[1]*(contador_bichos<10)
					total_disparos-=1
					puntuacion+= 10*nivel
		
		izquierda = 500
		derecha = 0
		arriba = 500
		abajo = 0
		for enemigo in enemigos:
			a1,b1 = enemigo.rect.topleft
			a2,b2 = enemigo.rect.bottomright
			if a1<izquierda: izquierda=a1
			if a2> derecha: derecha=a2
			if b1<arriba: arriba = b1
			if b2>abajo: abajo = b2
		
		if direccion_bichos:
			izquierda-=velocidad_bichos
			derecha-=velocidad_bichos
			if izquierda<25:
				izquierda+=velocidad_bichos
				derecha+=velocidad_bichos
				direccion_bichos = False
				bajar = True
		else:
			izquierda+=velocidad_bichos
			derecha+=velocidad_bichos
			if derecha>375:
				izquierda-=velocidad_bichos
				derecha-=velocidad_bichos
				direccion_bichos = True
				bajar = True
		
		if randint(probabilidad)<2 and contador_bichos>0: ##Disparos enemigos
			xs = [i for i in enemigos if all([i.original[1]>=j.original[1] for j in [x for x in enemigos if x.original[0]==i.original[0]]])]
			l1 = xs[randint(len(xs))]
			shoot = Disparo(l1.rect.bottomleft[0]+11,l1.rect.bottomleft[1],1)
			shoot.add(disparos,allsprites)
		
		if bajar:
			bajar = False
			for enemy in enemigos:
				enemy.rect.y+=5
		
		allsprites.update()
		screen.blit(background,(0,0))
		
		##esto es debug para ver el rectangulo que ocupan los enemigos:
		#pg.draw.rect(screen,(0,255,0),(izquierda,arriba,derecha-izquierda,abajo-arriba))
		
		if pg.font:
			font = pg.font.Font(None,32)
			text = font.render(str(nivel),True,(255,255,255))
			screen.blit(text,(310,520))
			text = font.render(str(puntuacion),True,(255,255,255))
			screen.blit(text,(200,590))
		
		allsprites.draw(screen)	
		pg.display.flip()
		
		if abajo>300:
			
			if pg.font:
				font = pg.font.Font(None,32)
				text = font.render("HAS SIDO INVADIDO",True,(255,255,255))
				background.blit(text,(75,330))
				screen.blit(background,(0,0))
				allsprites.draw(screen)	
				pg.display.flip()
				time.sleep(2)
			going = False
			perdido = True
		
		if reinicia:
			reinicia = False
			time.sleep(2)
		
		if contador_bichos==0:
			nivel+=1
			puntuacion += 100*nivel
			for disp in disparos: disp.kill()
			if pg.font:
				font = pg.font.Font(None,32)
				text = font.render("NIVEL {0} COMPLETADO".format(nivel-1),True,(255,255,255))
				screen.blit(background,(0,0))
				allsprites.draw(screen)	
				screen.blit(text,(75,330))
				pg.display.flip()
				time.sleep(2)
			for i in range(6):
				for j in range(3):
					enemy = Enemigo(75+i*45,25+j*45,(i,j))
					enemy.add(enemigos,allsprites)
					contador_bichos+=1
			allsprites.draw(screen)	
			pg.display.flip()
			time.sleep(2)
			total_disparos = 0
			probabilidad = 180-10*nivel
			velocidad_bichos = niveles(nivel)[0]*(contador_bichos>9)+niveles(nivel)[1]*(contador_bichos<10)

	if perdido:
		print("Has perdido")
	elif ganado:
		print("Has ganado")
	
	print("Has completado {0} niveles.\nTu puntuación final ha sido {1}.".format(nivel-1,puntuacion))
	
	pg.quit()

if __name__=="__main__": main()