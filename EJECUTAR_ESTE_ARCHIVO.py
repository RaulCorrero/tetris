'''
el código más interesante es el del tetris,
el pong es el más sencillo, el space invaders ya tiene
alguna complejidad

lo más interesante que hay aquí es el uso de pygame para
obtener una tecla y cambiar los controles (funcion pedir_tecla)
'''

import tetris, pong, space_invaders
import tkinter as tk
from tkinter import ttk
import pygame as pg
import pickle

def pedir_tecla(tec):
	#esta función me valdrá más tarde para pedir una tecla por si se
	#quiere cambiar los controles del tetris
	pg.init()
	screen = pg.display.set_mode((200, 50))
	font = pg.font.Font(None,16)
	text = font.render("Presiona una tecla para cambiarla",True,(255,255,255))
	screen.blit(text,(10,10))
	text = font.render("o ESC para cancelar",True,(255,255,255))
	screen.blit(text,(10,26))
	pg.display.flip()
	tecla = None
	while not tecla:
		for event in pg.event.get():
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					tecla = tec
				else:
					tecla = event.key
	pg.quit()
	return(tecla)


raiz = tk.Tk()
raiz.title('Juegos con pygame')

'''INFO'''

label1 = tk.Label(raiz, text='Estos son los juegos que he creado con pygame')
label1.grid(row=0,column=0,columnspan=3)

label1 = tk.Label(raiz, text='para el proyecto de Python de la asignatura')
label1.grid(row=1,column=0,columnspan=3)

label1 = tk.Label(raiz, text='de Software en Matemáticas.')
label1.grid(row=2,column=0,columnspan=3)

label1 = tk.Label(raiz, text=' ')
label1.grid(row=3,column=0,columnspan=3)

label1 = tk.Label(raiz, text='Los juegos están ordenados según los he ido haciendo,')
label1.grid(row=4,column=0,columnspan=3)

label1 = tk.Label(raiz, text='de más simples a más complejos.')
label1.grid(row=5,column=0,columnspan=3)

label1 = tk.Label(raiz, text=' ')
label1.grid(row=6,column=0,columnspan=3)

label1 = tk.Label(raiz, text='Haz clic en un juego para empezar a jugar,')
label1.grid(row=7,column=0,columnspan=3)

label1 = tk.Label(raiz, text='dale a info para más información de cada juego')
label1.grid(row=8,column=0,columnspan=3)

label1 = tk.Label(raiz, text='o a config para cambiar valores/modos/controles.')
label1.grid(row=9,column=0,columnspan=3)

label1 = tk.Label(raiz, text=' ')
label1.grid(row=10,column=0,columnspan=3)

'''JUEGOS'''

#funciones para los botones

previews = tk.IntVar(raiz)
previews.set(3)
nv_inicial = tk.IntVar(raiz)
nv_inicial.set(1)
hold = tk.IntVar()
hold.set(1)
prevent = tk.IntVar()
prevent.set(1)


def ventana_info_pong():
	info_pong = tk.Toplevel(raiz)
	info_pong.title("Información sobre Pong")
	info_pong.geometry("400x180")
	tk.Label(info_pong,text =
'''
El "Pong" es el primer juego que hice.

El jugador controla la pala de la derecha mediante W y S,
para moverte hacia arriba o abajo respectivamente.

El objetivo del juego es marcarle goles al oponente consiguiendo
que la pelota de salga hacia la izquierda mientras tratas que
no lo haga hacia la derecha.
''').pack()

def ventana_info_space():
	info_space = tk.Toplevel(raiz)
	info_space.title("Información sobre Space Invaders")
	info_space.geometry("400x200")
	tk.Label(info_space,text =
'''
El "Space Invaders" es el segundo juego que hice.

El jugador controla la nave que hay debajo de las defensas,
mediante las flechas derecha e izquierda. Además, puede disparar
mediante la tecla de espacio.

Usa las protecciones para defenderte de los disparos enemigos, pero
ten cuidado porque las irán destruyendo poco a poco.

El objetivo es destruir a todos los "Invasores espaciales" evitando
que ellos te quiten todas tus vidas y se acerquen demasiado a ti.
''').pack()

def ventana_info_tetris():
	info_tetris = tk.Toplevel(raiz)
	info_tetris.title("Información sobre Tetris")
	info_tetris.geometry("450x500")
	tk.Label(info_tetris,text =
'''
El "Tetris" es el tercer y más complejo juego que he hecho.

El objetivo del juego es colocar los bloques que caen para ir
formando líneas completas, que se eliminan, evitando así que
los bloques alcancen la parte superior de la pantalla.

Los bloques se pueden girar a izquierda y derecha con A y D.
Con las flechas derecha e izquierda, la ficha se puede mover, y con la
flecha hacia abajo se puede dejar caer.
Con el Espacio se deja caer el bloque hasta abajo de forma definitiva.
El Shift (Mayus) se usa para  dejar piezas en reserva.

Si el bloque no puede girar en su posición actual, buscará una
posición cercana en la que pueda girar, como el juego real.

Los tres movimientos tienen el primer toque instantáneo y luego
irán moviéndose si se deja pulsado el botón.

Una pieza se queda en reserva mientras la que ya esté en
reserva sale. Esto solo se puede hacer una vez antes de colocar pieza (para
prevenir el abuso de esta característica).

El juego base es el modo Marathon en el que irán cayendo más rápido las piezas
cuantas más líneas se hagan (se irá aumentando el nivel).

Se consiguen puntos al hacer líneas. Si se hacen varias en un solo movimiento, se
hace un combo (usar piezas sucesivas para hacer líneas con cada una) o el nivel
es mayor, se consiguen más puntos.

En la ventana de configuración se pueden cambiar los controles, el nivel inicial,
si se pueden reservar piezas y si se previene el abuso de la reserva o no.
''').pack()

def config_tetris():
	global previews
	'''
	Esta ventana permite configurar el tetris:
		preview_fichas <- [0, 1,... 6]
		hold_ficha
		prevent_hold_abuse
		nivel_inicial
	'''
	config_tetris = tk.Toplevel(raiz)
	config_tetris.title("Configuración del Tetris")
	config_tetris.geometry("405x580")
	
	label_config = tk.Label(config_tetris, text = 'Configuración del Tetris', font='Helvetica 10 bold')
	
	'''
	opciones del juego
	'''
	
	label_previews = tk.Label(config_tetris, text='Nº de previews:')
	combobox_previews = ttk.Combobox(config_tetris,textvariable=previews,state='readonly')
	combobox_previews['values'] = list(range(7))
	
	label_nivel = tk.Label(config_tetris, text='Nivel inicial:')
	combobox_nivel = ttk.Combobox(config_tetris,textvariable=nv_inicial,state='readonly')
	combobox_nivel['values'] = list(range(1,11))
	
	label_guardar = tk.Label(config_tetris, text='Guardar pieza:')
	hold1 = tk.Radiobutton(config_tetris, text = 'Activo',variable=hold,value=1)
	hold2 = tk.Radiobutton(config_tetris, text = 'Desactivo',variable=hold,value=0)
	
	label_prevent = tk.Label(config_tetris, text='Prevención del abuso del guardado:')
	prevent1 = tk.Radiobutton(config_tetris, text = 'Activo',variable=prevent,value=1)
	prevent2 = tk.Radiobutton(config_tetris, text = 'Desactivo',variable=prevent,value=0)
	
	label_config.grid(row=0, column=0,columnspan=3)
	
	label_previews.grid(row=1,column=0,columnspan=2)
	combobox_previews.grid(row=1,column=2)
	
	label_nivel.grid(row=2,column=0,columnspan=2)
	combobox_nivel.grid(row=2,column=2)
	
	label_guardar.grid(row=3,column=0)
	hold1.grid(row = 3, column = 1)
	hold2.grid(row = 3, column = 2)
	
	label_prevent.grid(row=4,column=0)
	prevent1.grid(row = 4, column = 1)
	prevent2.grid(row = 4, column = 2)
	
	'''
	opciones de teclas
	'''
	
	labelh = tk.Label(config_tetris, text = '')
	labelh.grid(row = 5, column = 0)
	
	label_controles = tk.Label(config_tetris, text = 'Configuración de teclas', font='Helvetica 10 bold')
	label_controles.grid(row = 6, column = 0,columnspan=3)
	
	def func_boton_shift():
		tetris.boton_hold = pedir_tecla(tetris.boton_hold)
		boton_shift.config(text=pg.key.name(tetris.boton_hold))
	label_shift = tk.Label(config_tetris, text = 'Guardar pieza:')
	boton_shift = tk.Button(config_tetris, text = pg.key.name(tetris.boton_hold), command = func_boton_shift)
	label_shift.grid(row = 7, column = 0)
	boton_shift.grid(row = 7, column = 1,columnspan=2)
	
	def func_boton_caer():
		tetris.boton_bajada = pedir_tecla(tetris.boton_bajada)
		boton_caer.config(text=pg.key.name(tetris.boton_bajada))
	label_caer = tk.Label(config_tetris, text = 'Dejar caer pieza:')
	boton_caer = tk.Button(config_tetris, text = pg.key.name(tetris.boton_bajada), command = func_boton_caer)
	label_caer.grid(row = 8, column = 0)
	boton_caer.grid(row = 8, column = 1,columnspan=2)
	
	def func_boton_giro_der():
		tetris.boton_giro_derecha = pedir_tecla(tetris.boton_giro_derecha)
		boton_giro_der.config(text=pg.key.name(tetris.boton_giro_derecha))
	label_giro_der = tk.Label(config_tetris, text = 'Girar a la derecha:')
	boton_giro_der = tk.Button(config_tetris, text = pg.key.name(tetris.boton_giro_derecha), command = func_boton_giro_der)
	label_giro_der.grid(row = 10, column = 0)
	boton_giro_der.grid(row = 10, column = 1,columnspan=2)
	
	def func_boton_giro_izq():
		tetris.boton_giro_izquierda = pedir_tecla(tetris.boton_giro_izquierda)
		boton_giro_izq.config(text=pg.key.name(tetris.boton_giro_izquierda))
	label_giro_izq = tk.Label(config_tetris, text = 'Girar a la izquierda:')
	boton_giro_izq = tk.Button(config_tetris, text = pg.key.name(tetris.boton_giro_izquierda), command = func_boton_giro_izq)
	label_giro_izq.grid(row = 9, column = 0)
	boton_giro_izq.grid(row = 9, column = 1,columnspan=2)
	
	def func_boton_izq():
		tetris.boton_izquierda = pedir_tecla(tetris.boton_izquierda)
		boton_izq.config(text=pg.key.name(tetris.boton_izquierda))
	label_izq = tk.Label(config_tetris, text = 'Mover hacia la izquierda:')
	boton_izq = tk.Button(config_tetris, text = pg.key.name(tetris.boton_izquierda), command = func_boton_izq)
	label_izq.grid(row = 11, column = 0)
	boton_izq.grid(row = 11, column = 1,columnspan=2)
	
	def func_boton_der():
		tetris.boton_derecha = pedir_tecla(tetris.boton_derecha)
		boton_der.config(text=pg.key.name(tetris.boton_derecha))
	label_der = tk.Label(config_tetris, text = 'Mover hacia la derecha:')
	boton_der = tk.Button(config_tetris, text = pg.key.name(tetris.boton_derecha), command = func_boton_der)
	label_der.grid(row = 12, column = 0)
	boton_der.grid(row = 12, column = 1,columnspan=2)
	
	def func_boton_abajo():
		tetris.boton_abajo = pedir_tecla(tetris.boton_abajo)
		boton_aba.config(text=pg.key.name(tetris.boton_abajo))
	label_aba = tk.Label(config_tetris, text = 'Mover hacia abajo:')
	boton_aba = tk.Button(config_tetris, text = pg.key.name(tetris.boton_abajo), command = func_boton_abajo)
	label_aba.grid(row = 13, column = 0)
	boton_aba.grid(row = 13, column = 1,columnspan=2)
	
	'''
	Confirmar / Valores predeterminados
	'''
	
	labelh2 = tk.Label(config_tetris, text = '')
	labelh2.grid(row = 15, column = 0)
	
	boton_restaurar = tk.Button(config_tetris, text = 'Guardar y salir',command=config_tetris.destroy)
	boton_restaurar.grid(row = 16, column = 0,columnspan=3)
	
	labelh3 = tk.Label(config_tetris, text = '')
	labelh3.grid(row = 17, column = 0)
	
	def valores_predeterminados():
		previews.set(3)
		nv_inicial.set(1)
		hold.set(1)
		prevent.set(1)
		tetris.boton_abajo = pg.K_DOWN
		tetris.boton_derecha = pg.K_RIGHT
		tetris.boton_izquierda = pg.K_LEFT
		tetris.boton_hold = pg.K_LSHIFT
		tetris.boton_bajada = pg.K_SPACE
		tetris.boton_giro_izquierda = pg.K_a
		tetris.boton_giro_derecha = pg.K_d
		boton_shift.config(text=pg.key.name(tetris.boton_hold))
		boton_caer.config(text=pg.key.name(tetris.boton_bajada))
		boton_giro_der.config(text=pg.key.name(tetris.boton_giro_derecha))
		boton_giro_izq.config(text=pg.key.name(tetris.boton_giro_izquierda))
		boton_izq.config(text=pg.key.name(tetris.boton_izquierda))
		boton_der.config(text=pg.key.name(tetris.boton_derecha))
		boton_aba.config(text=pg.key.name(tetris.boton_abajo))
	
	boton_restaurar = tk.Button(config_tetris, text = 'Restaurar valores predeterminados',command=valores_predeterminados)
	boton_restaurar.grid(row = 18, column = 0,columnspan=3)
	
	labelh4 = tk.Label(config_tetris, text = '')
	labelh4.grid(row = 19, column = 0)
	
	label_archivo = tk.Label(config_tetris, text = 'Guardar/cargar en un archivo:')
	label_archivo.grid(row = 20, column = 0, columnspan=3)
	
	nombre_archivo = tk.StringVar()
	nombre_archivo.set('Nombre_del_archivo.txt')
	
	entry_archivo = tk.Entry(config_tetris, textvariable = nombre_archivo,width=50)
	entry_archivo.grid(row = 21,column=0,columnspan=3)
	
	def cargar_archivo():
		var_arch = nombre_archivo.get()
		try:
			archivo_pickle = open(var_arch,'rb')
		except:
			print('Error al cargar: El archivo no existe')
		else:
			print('Archivo cargado: Configuración aplicada.')
			objetos = pickle.load(archivo_pickle)
			previews.set(objetos[0])
			nv_inicial.set(objetos[1])
			hold.set(objetos[2])
			prevent.set(objetos[3])
			tetris.boton_abajo = objetos[4]
			tetris.boton_derecha = objetos[5]
			tetris.boton_izquierda = objetos[6]
			tetris.boton_hold = objetos[7]
			tetris.boton_bajada = objetos[8]
			tetris.boton_giro_izquierda = objetos[9]
			tetris.boton_giro_derecha = objetos[10]
			boton_shift.config(text=pg.key.name(tetris.boton_hold))
			boton_caer.config(text=pg.key.name(tetris.boton_bajada))
			boton_giro_der.config(text=pg.key.name(tetris.boton_giro_derecha))
			boton_giro_izq.config(text=pg.key.name(tetris.boton_giro_izquierda))
			boton_izq.config(text=pg.key.name(tetris.boton_izquierda))
			boton_der.config(text=pg.key.name(tetris.boton_derecha))
			boton_aba.config(text=pg.key.name(tetris.boton_abajo))
			archivo_pickle.close()
	
	def guardar_archivo():
		var_arch = nombre_archivo.get()
		try:
			archivo_pickle = open(var_arch,'r')
		except:
			archivo_pickle = open(var_arch,'wb')
			pickle.dump([previews.get(),nv_inicial.get(),hold.get(),prevent.get(),tetris.boton_abajo,tetris.boton_derecha,tetris.boton_izquierda,tetris.boton_hold,tetris.boton_bajada,tetris.boton_giro_izquierda,tetris.boton_giro_derecha],archivo_pickle)
			archivo_pickle.close()
			print('Archivo guardado correctamente.')
		else:
			pregunta = tk.Toplevel(config_tetris)
			def guarda():
				archivo_pickle = open(var_arch,'wb')
				pickle.dump([previews.get(),nv_inicial.get(),hold.get(),prevent.get(),tetris.boton_abajo,tetris.boton_derecha,tetris.boton_izquierda,tetris.boton_hold,tetris.boton_bajada,tetris.boton_giro_izquierda,tetris.boton_giro_derecha],archivo_pickle)
				archivo_pickle.close()
				pregunta.destroy()
				print('Archivo guardado correctamente.')
			pregunta.title("¿Sobreescribir el archivo?")
			pregunta.geometry("300x100")
			label_sobre = tk.Label(pregunta, text = 'El archivo '+var_arch+' ya existe.')
			label_sobre2 = tk.Label(pregunta, text = '¿Quieres sobreescribirlo?')
			boton_si = tk.Button(pregunta, text = 'Sí',command=guarda,width=20)
			boton_no = tk.Button(pregunta, text = 'No',command=pregunta.destroy,width=20)
			label_sobre.grid(row=0,column=0,columnspan=2)
			label_sobre2.grid(row=1,column=0,columnspan=2)
			boton_si.grid(row=2,column=0)
			boton_no.grid(row=2,column=1)
			
	
	boton_cargar_archivo = tk.Button(config_tetris, text = 'Cargar archivo',command=cargar_archivo)
	boton_cargar_archivo.grid(row=22,column=0)
	
	boton_guardar_archivo = tk.Button(config_tetris, text = 'Guardar archivo',command=guardar_archivo)
	boton_guardar_archivo.grid(row=22,column=2)
	
	label_archivo2 = tk.Label(config_tetris, text = 'Pueden ser necesarios permisos para guardar')
	label_archivo3 = tk.Label(config_tetris, text = 'en algunas carpetas del ordenador.')
	label_archivo2.grid(row=23,column=0,columnspan=3)
	label_archivo3.grid(row=24,column=0,columnspan=3)
	

def jugar_al_tetris():
	tetris.nivel_inicial = nv_inicial.get()
	tetris.preview_fichas = previews.get()
	tetris.hold_ficha = hold.get()==1
	tetris.prevent_hold_abuse = prevent.get()==1
	tetris.main()

#botones

label1 = tk.Label(raiz, text='Pong')
label1.grid(row=11,column=0)

label1 = tk.Label(raiz, text='Invasores espaciales')
label1.grid(row=11,column=1)

label1 = tk.Label(raiz, text='Tetris', font='Helvetica 10 bold')
label1.grid(row=11,column=2)

boton_pong = tk.Button(raiz, text = 'Jugar', command = pong.main)
boton_pong.grid(row=12,column=0)

boton_space_invaders = tk.Button(raiz, text = 'Jugar', command = space_invaders.main)
boton_space_invaders.grid(row=12,column=1)

boton_tetris = tk.Button(raiz, text = 'Jugar', command = jugar_al_tetris)
boton_tetris.grid(row=12,column=2)

boton_info_pong = tk.Button(raiz, text = 'Info', command = ventana_info_pong)
boton_info_pong.grid(row=13,column=0)

boton_info_space_invaders = tk.Button(raiz, text = 'Info', command = ventana_info_space)
boton_info_space_invaders.grid(row=13,column=1)

boton_info_tetris = tk.Button(raiz, text = 'Info', command = ventana_info_tetris)
boton_info_tetris.grid(row=13,column=2)

boton_config_tetris = tk.Button(raiz, text = 'Config', command = config_tetris)
boton_config_tetris.grid(row=14,column=2)

label1 = tk.Label(raiz, text='El objetivo del proyecto era hacer el Tetris ↑\n pero he añadido el resto de juegos\npara que puedan probarse', font='Helvetica 8 bold')
label1.grid(row=15,column=0,columnspan=3)

raiz.mainloop()