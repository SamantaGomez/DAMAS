from tkinter import *
_step = 80
_dim = 640
# damos las dimenciones al tablero como a la ventana
damas = Tk()
damas.title("JUEGO DE DAMAS")
tablero = Canvas(damas, width=_dim, height=_dim)
damas.geometry('640x640')
tablero.place(x=0, y=0)
ficharoja = PhotoImage(file='img1.png')
fichanegra = PhotoImage(file='img2.png')
# crear la lista para la posicion de las fichas
_list = []
_set = {} 
_index = 0 
_current_data = {"item":None,"px":0,"py":0}
_black_pos = [];
_red_pos = [];
obj = tablero.create_rectangle(0,0,_dim,_dim, outline="gray87", fill="gray32")
for i in range(8):#0,1,2,3,4,5,6,7 
	for j in range(8):#0,1,2,3,4,5,6,7
		pi = i*_step#posición en el indice i
		pj = j*_step#posición en el indice j 
		if _index % 2 == 0: 
			if j % 2==0:
				if _index<=2: 			
					obj = tablero.create_image(pj,pi, anchor = NW, image=fichanegra,tags=("fnegra","ficha")) 
					_set[str(pj)+"-"+str(pi)] = obj
					_set[str(obj)] = {"px":pj,"py":pi}
				else:
					if _index<=4: 	
						pass	
					else: 
						obj = tablero.create_image(pj,pi, anchor = NW, image=ficharoja,tags=("froja","ficha"))
						_set[str(pj)+"-"+str(pi)] = obj
						_set[str(obj)] = {"px":pj,"py":pi}
			else:
				obj = tablero.create_rectangle(pj,pi,pj+_step,pi+_step, outline="gray87", fill="gray87")
		else:
			if j % 2!=0:
				if _index<=2: 
					obj = tablero.create_image(pj,pi, anchor = NW, image=fichanegra,tags=("fnegra","ficha"))
					_set[str(pj)+"-"+str(pi)] = obj
					_set[str(obj)] = {"px":pj,"py":pi}
				else:
					if _index<=4: 	
						pass			
					else: 
						obj = tablero.create_image(pj,pi, anchor = NW, image=ficharoja,tags=("froja","ficha"))
						_set[str(pj)+"-"+str(pi)] = obj
						_set[str(obj)] = {"px":pj,"py":pi}
			else:
				obj = tablero.create_rectangle(pj,pi,pj+_step,pi+_step, outline="gray87", fill="gray87")
		 
		_list.append(obj)
	_index+=1 

for _key in _set:
	print(_key,_set[_key])
 
sign = lambda x: (1, -1)[x < 0]
#creamos funciones que nos serviran para lo que es el movimiento de la pieza y para que pueda la pieza comerse a la otra
def buttonClick(event):
	pass
def buttonPress(event):
	global _current_data
	_item = tablero.find_closest(event.x, event.y)[0] 
	_tags = tablero.gettags(_item)
	if "ficha" in _tags:
		_item_key = str(_item)
		_val = _set.get(_item_key,None)
		if _val is not None:
			_current_data["item"] = _item
			floorX = event.x - (event.x % _step)
			floorY = event.y - (event.y % _step) 
			_current_data["px"] = event.x
			_current_data["py"] = event.y  
			_current_data["fpx"] = floorX
			_current_data["fpy"] = floorY 
			_current_data["relativeOffsetX"] = event.x-_val["px"]
			_current_data["relativeOffsetY"] = event.y-_val["py"]
		else:
			pass
	else:
		_current_data["item"] = None 
def buttonRelease(event):
	global _set
	global _current_data
	global tablero
	_item = _current_data["item"]
	if _item is None:
		return
	_px = _current_data["px"]
	_py = _current_data["py"]
	
	#fpx y fpy determinan la posición de un cuadro en el tablero.
	#Cada cuadro tiene una posición base por ejemplo: 
	#(80,80);(160,160) y se crea un conjunto de datos identificados por una clave conformada por el valor del ejeX y ejeY = eX-eY para usarse en un dicccionario
	
	_fpx = _current_data["fpx"]
	_fpy = _current_data["fpy"]
	_item_key = str(_item)
	_last_pos = _set.get(_item_key,None) 
	_lpx = _last_pos["px"]
	_lpy = _last_pos["py"] 
	_tags = tablero.gettags(_item)
	_items = tablero.find_overlapping(event.x, event.y,event.x, event.y) 
	print(_items)
	if _items[1]!=1:
		floorX = event.x - (event.x % _step)
		floorY = event.y - (event.y % _step) 
		_key = str(floorX)+"-"+str(floorY)
		deltaFloorX = floorX - _fpx
		deltaFloorY = floorY - _fpy
		abs_deltaFloorX = abs(deltaFloorX)
		abs_deltaFloorY = abs(deltaFloorY)
		if(
			deltaFloorX==0 or 
			deltaFloorY==0 or 
			abs_deltaFloorX!=abs_deltaFloorY or 
			abs_deltaFloorX>160
		):
			#aqui realizamos que no se permite desplazamiento horizontal o vertical
			#como tambien restaurar posición
			_deltaX = _lpx - _px + _current_data["relativeOffsetX"]
			_deltaY = _lpy - _py + _current_data["relativeOffsetY"] 
			tablero.move(_item,_deltaX,_deltaY)
		else: 
			if abs_deltaFloorX>80:
				tfloorX = floorX - sign(deltaFloorX) * _step
				tfloorY = floorY - sign(deltaFloorY) * _step
				_tkey = str(tfloorX)+"-"+str(tfloorY) 
				_t1key = str(floorX)+"-"+str(floorY) 
				_val = _set.get(_tkey,None) 
				_val1 = _set.get(_t1key,None) 
				if _val is None:   
					#aqui damos la posición ocupada
					#y tambien para restaurar posición
					_deltaX = _lpx - _px + _current_data["relativeOffsetX"]
					_deltaY = _lpy - _py + _current_data["relativeOffsetY"] 
					tablero.move(_item,_deltaX,_deltaY) 
				else:  
					if _val1 is None:
						_otags = tablero.gettags(_val)
						if "ficha" in _otags:
							if ("fnegra" in _tags and "froja" in _otags) or ("fnegra" in _otags and "froja" in _tags):
								_deltaX = floorX -_px + _current_data["relativeOffsetX"]
								_deltaY = floorY - _py + _current_data["relativeOffsetY"]
								tablero.move(_item,_deltaX,_deltaY)
								_set[_key] = _item
								_last_item_key = str(_set[_item_key]["px"])+"-"+str(_set[_item_key]["py"])
								_set[_last_item_key] = None
								_set[_item_key]["px"]=floorX
								_set[_item_key]["py"]=floorY
								tablero.delete(_val);
								_set[str(_val)] = None
								_set[_tkey] = None 
							else:
								#posición ocupada
								#restaurar posición
								_deltaX = _lpx - _px + _current_data["relativeOffsetX"]
								_deltaY = _lpy - _py + _current_data["relativeOffsetY"] 
								tablero.move(_item,_deltaX,_deltaY) 
						else:
							#posición ocupada
							#restaurar posición
							_deltaX = _lpx - _px + _current_data["relativeOffsetX"]
							_deltaY = _lpy - _py + _current_data["relativeOffsetY"] 
							tablero.move(_item,_deltaX,_deltaY) 
					else:
						#posición ocupada
						#restaurar posición
						_deltaX = _lpx - _px + _current_data["relativeOffsetX"]
						_deltaY = _lpy - _py + _current_data["relativeOffsetY"] 
						tablero.move(_item,_deltaX,_deltaY) 
			else:
				_val = _set.get(_key,None) 
				if _val is not None:   
					#posición ocupada
					#restaurar posición
					_deltaX = _lpx - _px + _current_data["relativeOffsetX"]
					_deltaY = _lpy - _py + _current_data["relativeOffsetY"] 
					tablero.move(_item,_deltaX,_deltaY)  
				else:
					_deltaX = floorX -_px + _current_data["relativeOffsetX"]
					_deltaY = floorY - _py + _current_data["relativeOffsetY"]
					tablero.move(_item,_deltaX,_deltaY)
					_set[_key] = _item
					_last_item_key = str(_set[_item_key]["px"])+"-"+str(_set[_item_key]["py"])
					_set[_last_item_key] = None
					_set[_item_key]["px"]=floorX
					_set[_item_key]["py"]=floorY

def buttonMotion(event):
	global _current_data
	global tablero
	_item = _current_data["item"]
	_px = _current_data["px"]
	_py = _current_data["py"]
	_deltaX = event.x - _px
	_deltaY = event.y - _py
	_current_data["px"] = event.x
	_current_data["py"] = event.y
	if  _item is not None:
		_tags = tablero.gettags(_item)
		if "ficha" in _tags:
			tablero.tag_raise(_item)
			tablero.move(_item,_deltaX,_deltaY)

#llamamos a la funciones 
tablero.tag_bind("ficha","<Button-1>", buttonClick) 
tablero.tag_bind("ficha","<ButtonPress-1>", buttonPress) 
tablero.tag_bind("ficha","<ButtonRelease-1>", buttonRelease) 
tablero.tag_bind("ficha","<B1-Motion>", buttonMotion) 


damas.mainloop()

