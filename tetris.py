import os, time
import pygame as pg
from numpy.random import randint
import numpy as np

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

colocadas = np.zeros((30,20))
colores = {1:(0,255,255),2:(0,0,255),3:(255,127,0),4:(255,255,0),
5:(0,255,0),6:(255,0,0),7:(128,0,128)}
piezas = [1,2,3,4,5,6,7]
modo = 'marathon'
#posibles_giros = [(1,0),(-1,0),(0,-1),(0,1),(1,-1),(-1,-1),(1,1),(-1,1)]
posibles_giros = [(1,0),(-1,0),(0,-1),(1,-1),(-1,-1)]
preview_fichas = 6 #MIN 0, MAX 6
hold_ficha = True
prevent_hold_abuse = True #si se puede usar shift muchas veces seguidas
nivel = 1
nivel_inicial = 1

boton_abajo = pg.K_DOWN
boton_derecha = pg.K_RIGHT
boton_izquierda = pg.K_LEFT
boton_hold = pg.K_LSHIFT
boton_bajada = pg.K_SPACE
boton_giro_izquierda = pg.K_a
boton_giro_derecha = pg.K_d

formas = {
	  1 : np.array([[0,0,0,0],
					[1,1,1,1],
					[0,0,0,0],
					[0,0,0,0]]),
	  2 : np.array([[1,0,0],
					[1,1,1],
					[0,0,0]]),
	  3 : np.array([[0,0,1],
					[1,1,1],
					[0,0,0]]),
	  4 : np.array([[1,1],
					[1,1]]),
	  5 : np.array([[0,1,1],
					[1,1,0],
					[0,0,0]]),
	  6 : np.array([[1,1,0],
					[0,1,1],
					[0,0,0]]),
	  7 : np.array([[0,1,0],
					[1,1,1],
					[0,0,0]])}

class Mensaje(pg.sprite.Sprite):
	
	def __init__(self,mensaje,contador):
		pg.sprite.Sprite.__init__(self)
		self.mens = mensaje
		self.k = contador
	
	def update(self):
		self.k-=1

class Tetromino(pg.sprite.Sprite):
	
	def __init__(self,forma):
		global colores, formas
		pg.sprite.Sprite.__init__(self)
		self.forma = forma
		self.color = colores[forma]
		self.matriz = formas[forma]
		self.shape = np.shape(self.matriz)[0]
		self.x, self.y = 10-int(self.shape/2),5-self.shape
	
	def update(self):
		self.y+=1
	
	def clockwise(self):
		self.matriz = np.rot90(self.matriz,k=-1)
	
	def anticlockwise(self):
		self.matriz = np.rot90(self.matriz)

class Marco(pg.sprite.Sprite):
	
	def __init__(self,posicion,forma,x,y,mantener):
		global colores, formas
		pg.sprite.Sprite.__init__(self)
		self.mantener = mantener
		self.forma = forma
		self.posicion = posicion
		self.matriz = formas[forma]
		self.color = colores[forma]
		self.shape = np.shape(self.matriz)[0]
		self.image = pg.Surface([65,65])
		self.image.fill((0,0,0))
		self.horizontal = pg.Surface([45,1])
		self.horizontal.fill((100,100,100))
		self.vertical = pg.Surface([1,45])
		self.vertical.fill((100,100,100))
		for i in range(5):
			self.image.blit(self.horizontal,(10,10+11*i))
			self.image.blit(self.vertical,(10+11*i,10))
		self.cuadro = pg.Surface([10,10])
		self.cuadro.fill(self.color)
		if not mantener:
			for i in range(self.shape):
				for j in range(self.shape):
					if self.matriz[i,j]:
						self.image.blit(self.cuadro,(11*(j+1),11*(i+1)))
		
		self.rect = self.image.get_rect()
		self.rect.topleft = x,y
	
	def update(self,forma):
		global colores, formas
		self.forma = forma
		self.color = colores[forma]
		self.matriz = formas[forma]
		self.shape = np.shape(self.matriz)[0]
		self.image.fill((0,0,0))
		for i in range(5):
			self.image.blit(self.horizontal,(10,10+11*i))
			self.image.blit(self.vertical,(10+11*i,10))
		self.cuadro.fill(self.color)
		for i in range(self.shape):
			for j in range(self.shape):
				if self.matriz[i,j]:
					self.image.blit(self.cuadro,(11*(j+1),11*(i+1)))

def main():
	
	global colocadas, modo, posibles_giros, preview_fichas, hold_ficha, nivel, nivel_inicial
	
	if modo=='marathon': colocadas = np.zeros((30,20))
	
	def rellenar(): #funcion para randomizar el orden de las fichas
		xs = []
		lista=[1,2,3,4,5,6,7]
		for i in range(7,0,-1):
			x = lista.pop(randint(i))
			xs+=[x]
		return(xs)
	
	pg.init()
	pg.display.set_caption("Tetris")
	
	'''
	CREAR LA REJILLA DE JUEGO
	'''
	
	b,s=30,1 #al principio iba a poner todas las dimensiones dependiendo de esto
			 #pero salian demasiadas cuentas y he acabado calculandolas, la cuenta comentada
	rejilla = pg.Surface((309,619)) #(10*b+9*s,20*b+19*s)
	rejilla.fill((0,0,0))
	horizontal = pg.Surface((309,1)) #(10*b+9*s,s)
	vertical = pg.Surface((1,629)) #(s,20*b+19*s)
	horizontal.fill((100,100,100))
	vertical.fill((100,100,100))
	for i in range(9):rejilla.blit(vertical,(30+31*i,0)) #(b+(b+s)*i
	for i in range(19):rejilla.blit(horizontal,(0,30+31*i)) #b+(b+s)*i
	
	#CREAR LA PANTALLA (depende de b y s)
	screen = pg.display.set_mode((589, 739),pg.SCALED) #(16*b+9*s, 24*b+19*s)
	
	#CREAR EL FONDO
	background = pg.Surface(screen.get_size())
	background = background.convert()
	background.fill((0,0,0))
	
	cuadro = pg.Surface((319,629))
	cuadro.fill((255,255,255))
	background.blit(cuadro,(85,55))
	
	background.blit(rejilla,(90,60)) #(3*b,2*b)
	
	'''
	INICIALIZAR DISTINTAS VARIABLES
	'''
	
	allsprites = pg.sprite.RenderPlain(())
	
	bolsa1 = rellenar() #creacion del orden aleatorio
	bolsa2 = rellenar()
	bolsa_total = bolsa1+bolsa2
	tetro = Tetromino(bolsa1.pop(0)) #y sacamos el primero
	tetro.add(allsprites)

	clock = pg.time.Clock()
	going = True
	speed = 25
	caer = speed
	tocando = False
	tocando_old = False
	tiempo_colocada = 40
	tc = tiempo_colocada
	tiempo_colocada_maxima = 150
	tcm = tiempo_colocada_maxima
	colocada = False
	mover_izq = False
	mover_der = False
	mover_aba = False
	primer_movimiento_izq = False
	primer_movimiento_der = False
	primer_movimiento_aba = False
	velocidad_contador = {'izq':6,'der':6,'aba':5}
	contador = 0
	bajada = False
	cambio = False
	recambio = False
	recambiada = False
	pausa = False
	contador_lineas = 0
	puntuacion = 0
	mensajes = pg.sprite.Group()
	combo = False
	contador_combo = 0
	mensaje_combo = Mensaje("combo",30)
	mayor_combo = 0
	
	nivel=nivel_inicial
	speed=[25,20,17,14,11,9,7,5,4,3,2,0][nivel]
	caer = speed
	sonido_colocada = pg.mixer.Sound(os.path.join(data_dir, "colocada.wav"))
	sonido_linea = pg.mixer.Sound(os.path.join(data_dir, "linea.wav"))
	sonido_combo = pg.mixer.Sound(os.path.join(data_dir, "combo.wav"))
	sonido_shift = pg.mixer.Sound(os.path.join(data_dir, "shift.wav"))
	pg.mixer.music.load(os.path.join(data_dir, "tetris_background.mp3"))
	pg.mixer.music.play(-1)
	
	'''
	INICIALIZAR PREVIEW DE FICHAS
	'''
	
	previews = pg.sprite.RenderPlain()
	for i in range(preview_fichas):
		preview_i=Marco(i, bolsa_total[i+1],409,60+80*i,False)
		preview_i.add(previews)
	
	'''
	INICIALIZAR CAMBIO DE FICHAS
	'''
	
	if hold_ficha:
		mantener = pg.sprite.RenderPlain()
		cuadro_mantener = Marco(0,1,15,60,True)
		cuadro_mantener.add(mantener)
	
	'''
	BUCLE PRINCIPAL DEL JUEGO
	'''
	
	while going:
		clock.tick(60) #con esto se puede variar la dificultad del juego
		caer -=1
		
		'''
		RELLENAR BOLSA DE TETROMINOS
		'''
		
		bolsa_total = bolsa1+bolsa2
		
		if len(bolsa1)==0:#rellenar los tetrominoes si están vacíos
			bolsa1 = bolsa2.copy()
			bolsa2 = rellenar()
		
		if not tetro.alive():#sacar un nuevo tetromino
			tetro = Tetromino(bolsa1.pop(0))
			tetro.add(allsprites)
			if tetro.shape==2:tetro.y-=1
			elif tetro.shape==4:tetro.y+=1
			for pre in previews:
				pre.update(bolsa_total[pre.posicion+1])
		
		'''
		TECLAS Y EVENTOS PRINCIPALES
		'''
		
		for event in pg.event.get():
			if event.type == pg.QUIT: going = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					pausa = True
				if event.key == boton_izquierda:
					mover_izq = True
					primer_movimiento_izq = True
				if event.key == boton_derecha:
					mover_der = True
					primer_movimiento_der = True
				if event.key == boton_giro_izquierda:
					tc_old,tc=tc,tiempo_colocada
					tetro.anticlockwise()
					mover = False
					for j in range(tetro.shape): #mirar si nuestra pieza choca
						for i in range(tetro.shape):
							if tetro.matriz[i,j] and (tetro.y+i>=25 or tetro.x+j>=15 or tetro.x+j<=4 or colocadas[tetro.y+i,tetro.x+j]): mover = True
					for (sx,sy) in posibles_giros:
						if mover:
							mover = False
							tetro.x+=sx
							tetro.y+=sy
							for j in range(tetro.shape): #mirar si nuestra pieza choca
								for i in range(tetro.shape):
									if tetro.matriz[i,j] and (tetro.y+i>=25 or tetro.x+j>=15 or tetro.x+j<=4 or colocadas[tetro.y+i,tetro.x+j]): mover = True
							if mover:
								tetro.x-=sx
								tetro.y-=sy
					if mover:
						tetro.clockwise()
						tc = tc_old
				if event.key == boton_giro_derecha:
					tc_old,tc=tc,tiempo_colocada
					tetro.clockwise()
					mover = False
					for j in range(tetro.shape): #mirar si nuestra pieza choca
						for i in range(tetro.shape):
							if tetro.matriz[i,j] and (tetro.y+i>=25 or tetro.x+j>=15 or tetro.x+j<=4 or colocadas[tetro.y+i,tetro.x+j]): mover = True
					for (sx,sy) in posibles_giros:
						if mover:
							mover = False
							tetro.x+=sx
							tetro.y+=sy
							for j in range(tetro.shape): #mirar si nuestra pieza choca
								for i in range(tetro.shape):
									if tetro.matriz[i,j] and (tetro.y+i>=25 or tetro.x+j>=15 or tetro.x+j<=4 or colocadas[tetro.y+i,tetro.x+j]): mover = True
							if mover:
								tetro.x-=sx
								tetro.y-=sy
					if mover:
						tetro.anticlockwise()
						tc = tc_old
				if event.key == boton_abajo:
					mover_aba = True
					primer_movimiento_aba = True
				if event.key == boton_bajada:
					bajada = True
					tetro.y -= 1
					while bajada:
						tetro.y+=1
						for j in range(tetro.shape): #mirar si nuestra pieza choca
							for i in range(tetro.shape):
								if tetro.matriz[i,j]:
									if colocadas[tetro.y+i+1,tetro.x+j]:
										bajada = False
									elif tetro.y+i+1>24:
										bajada = False
					bajada = True
				if event.key == boton_hold:
					cambio = True
				# if event.key == pg.K_r:
					# contador_lineas+=1
					##debug
			if event.type == pg.KEYUP:
				if event.key == boton_izquierda:
					mover_izq = False
					primer_movimiento_izq = False
				if event.key == boton_derecha:
					mover_der = False
					primer_movimiento_der = False
				if event.key == boton_abajo:
					mover_aba = False
					primer_movimiento_aba = False


		'''
		COMPROBAR SI SE PAUSA
		'''
		
		if pausa:
			pg.mixer.music.pause()
			cuadro = pg.Surface((303,42))
			cuadro.fill((255,255,255))
			cuadro2 = pg.Surface((293,32))
			cuadro2.fill((0,0,0))
			cuadro.blit(cuadro2,(5,5))
			if pg.font:
				font = pg.font.Font(None,48)
				text = font.render("JUEGO PAUSADO",True,(255,255,255))
				cuadro.blit(text,(6,6))
			screen.blit(cuadro,(100,90))
			pg.display.flip()
		
		while pausa:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					going = False
					pausa = False
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						pausa = False
						pg.mixer.music.unpause()
		
		
		'''
		MOVIMIENTO DE LA PIEZA ACTUAL
		'''
		
		if mover_izq:
			mover = True
			for j in range(tetro.shape): #mirar si nuestra pieza choca
				for i in range(tetro.shape):
					if tetro.matriz[i,j] and (tetro.x+j==5 or colocadas[tetro.y+i,tetro.x+j-1]): mover = False
			if mover:
				if primer_movimiento_izq:
					tetro.x-=1
					primer_movimiento_izq = False
					contador = velocidad_contador['izq']*3
				else:
					contador-=1
					if not contador:
						tetro.x-=1
						contador = velocidad_contador['izq']
		elif mover_der:
			mover = True
			for j in range(tetro.shape): #mirar si nuestra pieza choca
				for i in range(tetro.shape):
					if tetro.matriz[i,j] and  (tetro.x+j==14 or colocadas[tetro.y+i,tetro.x+j+1]): mover = False
			if mover:
				if primer_movimiento_der:
					tetro.x+=1
					primer_movimiento_der = False
					contador = velocidad_contador['der']*3
				else:
					contador-=1
					if not contador:
						tetro.x+=1
						contador = velocidad_contador['der']
		elif mover_aba and not tocando:
			if primer_movimiento_aba:
				allsprites.update()
				primer_movimiento_aba = False
				contador = velocidad_contador['aba']
			else:
				contador-=1
				if not contador:
					allsprites.update()
					contador = velocidad_contador['aba']
		
		'''
		COMPROBAR SI HAY QUE COLOCAR LA PIEZA
		'''
		
		tocando = False
		for j in range(tetro.shape): #mirar si nuestra pieza choca
			for i in range(tetro.shape):
				if tetro.matriz[i,j]:
					if colocadas[tetro.y+i+1,tetro.x+j]:
						tocando = True
					elif tetro.y+i+1>24:
						tocando = True
		
		if not caer:
			if not tocando and not mover_aba:
				allsprites.update()
			caer = speed
		
		if tocando and not tocando_old:
			colocada = True
		
		if colocada:
			if tocando:
				tcm-=1
				tc-=1
			else:
				colocada, tocando_old = False, False
				
		if (not tc or not tcm) and tocando:
			tcm,tc=tiempo_colocada_maxima,tiempo_colocada
			for j in range(tetro.shape): #dibujar nuestra pieza
				for i in range(tetro.shape):
					if tetro.matriz[i,j]:
						colocadas[tetro.y+i,tetro.x+j]=tetro.forma
			
			tetro.kill()
			colocada = False
			recambiada = False
			combo = False
			pg.mixer.Sound.play(sonido_colocada)
		
		if tcm<0 and tocando:
			tcm,tc=tiempo_colocada_maxima,tiempo_colocada
			for j in range(tetro.shape): #dibujar nuestra pieza
				for i in range(tetro.shape):
					if tetro.matriz[i,j]:
						colocadas[tetro.y+i,tetro.x+j]=tetro.forma
			
			tetro.kill()
			colocada = False
			recambiada = False
			combo = False
			pg.mixer.Sound.play(sonido_colocada)
		
		if bajada:
			tcm,tc,bajada=tiempo_colocada_maxima,tiempo_colocada,False
			for j in range(tetro.shape): #dibujar nuestra pieza
				for i in range(tetro.shape):
					if tetro.matriz[i,j]:
						colocadas[tetro.y+i,tetro.x+j]=tetro.forma
			tetro.kill()
			colocada = False
			recambiada = False
			combo = False
			pg.mixer.Sound.play(sonido_colocada)
		
		'''
		COMPROBAR SI HAY QUE ALMACENAR LA PIEZA
		'''
		
		if cambio and hold_ficha:
			cambio = False
			if (not prevent_hold_abuse) or (prevent_hold_abuse and not recambiada):
				pg.mixer.Sound.play(sonido_shift)
				if recambio:
					forma_guardada = cuadro_mantener.forma
					cuadro_mantener.update(tetro.forma)
					tetro.kill()
					tetro = Tetromino(forma_guardada)
					tetro.add(allsprites)
					if tetro.shape==2:tetro.y-=1
					elif tetro.shape==4:tetro.y+=1
					recambiada = True
					combo = False
				else:
					recambio = True
					cuadro_mantener.update(tetro.forma)
					tetro.kill()
					recambiada = True
					combo = False
		
		'''
		DIBUJAR PIEZAS Y FONDO
		'''
		
		screen.blit(background, (0, 0)) #Dibujar fondo
		
		for j in range(tetro.shape): #dibujar nuestra pieza
			for i in range(tetro.shape):
				if tetro.matriz[i,j]:
					cuadro = pg.Surface((30,30)) #(b,b)
					cuadro.fill(tetro.color)
					screen.blit(cuadro,(59+(tetro.x+j-4)*31,91+(tetro.y+i-6)*31))
		
		
		for j in range(10):#Dibujar piezas colocadas
			for i in range(20):
				x = colocadas[5+i,5+j]
				if x:
					cuadro = pg.Surface((30,30)) #(b,b)
					cuadro.fill(colores[x])
					screen.blit(cuadro,(59+(j+1)*31,91+(i-1)*31)) #(3*b+i*b+(i-1)*s,2*b+j*b+(j-1)*s)
		
		previews.draw(screen)
		if hold_ficha: mantener.draw(screen)
		
		'''
		COMPROBAR SI SE HAN COMPLETADO LINEAS
		'''
		
		lineas_completadas = []
		for i in range(20):
			if not 0 in colocadas[i+5,5:15]:lineas_completadas+=[i+5]
		
		completadas = len(lineas_completadas)
		contador_lineas+=completadas
		lineas_vacias = [i for i in range(30) if i not in lineas_completadas]
		if completadas:
			combo = True
			contador_combo+=1
			puntuacion+=[100,300,500,800][completadas-1]*nivel*contador_combo
			mensaje = Mensaje(['Single','Double','Triple','TETRIS'][completadas-1],30)
			mensaje.add(mensajes)
			for j in lineas_completadas:
				rectangulo = pg.Surface((309,30))
				rectangulo.fill((100,100,100))
				screen.blit(rectangulo,(90,91+(j-6)*31))
			nuevo_colocadas = np.zeros((30,20))
			nuevo_colocadas[completadas:,:] = colocadas[lineas_vacias,:].copy()
			colocadas = nuevo_colocadas.copy()
			for j in range(10):#Dibujar piezas colocadas
				for i in range(20):
					x = colocadas[5+i,5+j]
					if x:
						cuadro = pg.Surface((30,30)) #(b,b)
						cuadro.fill(colores[x])
						screen.blit(cuadro,(59+(j+1)*31,91+(i-1)*31)) #(3*b+i*b+(i-1)*s,2*b+j*b+(j-1)*s)
			lineas_completadas,completadas=[],0
			if contador_combo>=2:
				mensaje_combo = Mensaje("Combo x",30)
				mensaje_combo.add(mensajes)
				if mayor_combo<contador_combo: mayor_combo=contador_combo
				pg.mixer.Sound.play(sonido_combo)
			else:
				pg.mixer.Sound.play(sonido_linea)
			
			'''
			SUBIDA DE NIVEL SOLO SE COMPRUEBA AL HACER LINEAS
			'''
			nivel_old = nivel
			if nivel<10: nivel = nivel_inicial+int(contador_lineas/10)
			if nivel_old<nivel:
				speed=[25,20,17,14,11,9,7,5,4,3,2,0][nivel]
				mensaje = Mensaje("Speed up",30)
				mensaje.add(mensajes)
		
		if not tetro.alive() and not combo:
			contador_combo=0
			if mensaje_combo.alive():
				mensaje_combo.kill()

		
		if pg.font:
			font = pg.font.Font(None,64)
			for mensaje in mensajes:
				if mensaje.mens=='Speed up':
					text = font.render(mensaje.mens,True,(100+5*mensaje.k,100+5*mensaje.k,100+5*mensaje.k))
					screen.blit(text,(200,300+mensaje.k))
				elif mensaje.mens=="Combo x":
					text = font.render(mensaje.mens+str(contador_combo),True,(100+5*mensaje.k,100+5*mensaje.k,100+5*mensaje.k))
					screen.blit(text,(200,400+mensaje.k))
				else:
					text = font.render(mensaje.mens,True,(100+5*mensaje.k,100+5*mensaje.k,100+5*mensaje.k))
					screen.blit(text,(200,200+mensaje.k))
				mensaje.update()
				if not mensaje.k:
					mensaje.kill()
				
			font = pg.font.Font(None,32)
			text = font.render("Nivel:",True,(255,255,255))
			screen.blit(text,(408,535))
			text = font.render(str(nivel),True,(255,255,255))
			screen.blit(text,(408,555))
			text = font.render("Líneas:",True,(255,255,255))
			screen.blit(text,(408,580))
			text = font.render(str(contador_lineas),True,(255,255,255))
			screen.blit(text,(408,600))
			text = font.render("Puntuación:",True,(255,255,255))
			screen.blit(text,(408,625))
			text = font.render(str(puntuacion),True,(255,255,255))
			screen.blit(text,(408,645))
		
		pg.display.flip()
		tocando_old = tocando
		
		'''
		COMPROBAR SI SE PIERDE
		'''
		
		if sum([1 for i in list(colocadas[4,5:15]) if i!=0]):
			going = False
		
	
	'''
	INFORMACION FINAL DE PARTIDA
	'''
	
	if tetro.alive():
		for j in range(tetro.shape): #dibujar nuestra pieza
			for i in range(tetro.shape):
				if tetro.matriz[i,j]:
					cuadro = pg.Surface((30,30)) #(b,b)
					cuadro.fill(tetro.color)
					background.blit(cuadro,(59+(tetro.x+j-4)*31,91+(tetro.y+i-6)*31))
	
	for j in range(10):#Dibujar piezas colocadas
		for i in range(20):
			x = colocadas[5+i,5+j]
			if x:
				cuadro = pg.Surface((30,30)) #(b,b)
				cuadro.fill(colores[x])
				background.blit(cuadro,(59+(j+1)*31,91+(i-1)*31)) #(3*b+i*b+(i-1)*s,2*b+j*b+(j-1)*s)
	
	going = True ##hay que cambiar esto para que al darle a la cruz salga del todo
	if modo=='marathon':
		previews.draw(background)
		if hold_ficha: mantener.draw(background)
		cuadro = pg.Surface((353,373))
		cuadro.fill((255,255,255))
		cuadro2 = pg.Surface((343,363))
		cuadro2.fill((0,0,0))
		cuadro.blit(cuadro2,(5,5))
		if pg.font:
			font = pg.font.Font(None,64)
			text = font.render("GAME OVER",True,(255,255,255))
			cuadro.blit(text,(20,20))
			font = pg.font.Font(None,32)
			text = font.render("MODO: MARATHON",True,(255,255,255))
			cuadro.blit(text,(20,78))
			text = font.render("NIVEL ALCANZADO",True,(255,255,255))
			cuadro.blit(text,(20,136))
			text = font.render("NUMERO DE LINEAS",True,(255,255,255))
			cuadro.blit(text,(20,194))
			text = font.render("MAYOR COMBO",True,(255,255,255))
			cuadro.blit(text,(20,252))
			text = font.render("PUNTUACION TOTAL",True,(255,255,255))
			cuadro.blit(text,(20,310))
			font = pg.font.Font(None,24)
			text = font.render(str(nivel),True,(255,255,255))
			cuadro.blit(text,(20,158))
			text = font.render(str(contador_lineas),True,(255,255,255))
			cuadro.blit(text,(20,216))
			text = font.render(str(mayor_combo),True,(255,255,255))
			cuadro.blit(text,(20,274))
			text = font.render(str(puntuacion),True,(255,255,255))
			cuadro.blit(text,(20,332))
		background.blit(cuadro,(100,90))
		while going:
			clock.tick(60)
			
			for event in pg.event.get():
				if event.type == pg.QUIT: going = False
			
			screen.blit(background, (0, 0))
			
			pg.display.flip()
			
	
	pg.quit()

#IDEA: hacer con tkinter un menu para editar las opciones
if __name__=="__main__": main()

#input('Presiona enter para salir')















