from typing import overload, TypeVar
import numpy as np
import pygame as pg


TRectBox = TypeVar("TRectBox", bound="RectBox")

class RectBox(np.ndarray):
	"""
	RectBox
	=======
	Reworked in 2026
	
	Structured box:
	---------------

	 ** **
	    - convert array (or list) into a **RectBox**:
	>>> box = RectBox([60, 25, 1, 2, 5, 6, 0, 0]) 
	>>> #=> RectBox((array|list)=>[parentx, parenty, offsetx, offsety, width, height, id, key])

		 
	Macro Keys:
	-----------

	 ** **
	 	- Zero side enable
	``RBOX_NONE_COLLISION``                
	
	  ** **
	 	- One side enable
	``RBOX_BOTTOM_COLLISION``                 
	``RBOX_TOP_COLLISION``                    
	``RBOX_RIGHT_COLLISION``                  
	``RBOX_LEFT_COLLISION``                   

	 ** **
	 	- Two side enable
	``RBOX_VERTICAL_COLLISION``               
	``RBOX_HORIZONTAL_COLLISION``             

	 ** **
	 	- Three side enable
	``RBOX_RIGHT_VERTICAL_COLLISION``         
	``RBOX_LEFT_VERTICAL_COLLISION``           
	``RBOX_TOP_HORIZONTAL_COLLISION``         
	``RBOX_BOTTOM_HORIZONTAL_COLLISION``      

	 ** **
	 	- Four side enable
	``RBOX_ALL_COLLISION``                    	 


		 
	Credit
	------

	 ** **
		- @PlusVeter(or Ucstorm)
		 
	"""
	def __new__(cls, listarray:list|np.ndarray):
		return np.asarray(listarray, dtype=np.int64).view(cls)
	
	def __bool__(self): return True

	@property
	def parentx(self) -> int: return self[0]

	@parentx.setter
	def parentx(self, value: int): self[0] = value


	@property
	def parenty(self) -> int: return self[1]

	@parenty.setter
	def parenty(self, value: int): self[1] = value


	@property
	def x(self) -> int: return self[0] + self[2]

	@x.setter
	def x(self, value: int): self[2] = value - self[0]


	@property
	def y(self) -> int: return self[1] + self[3]

	@y.setter
	def y(self, value: int): self[3] = value - self[1]

	@property
	def offsetx(self) -> int: return self[2]

	@offsetx.setter
	def offsetx(self, value: int):self[2] = value

	@property
	def offset(self) -> pg.Vector2: return pg.Vector2(self.offsetx, self.offsety)

	@property
	def offsety(self) -> int: return self[3]

	@offsety.setter
	def offsety(self, value: int): self[3] = value


	@property
	def width(self) -> int: return self[4]

	@width.setter
	def width(self, value: int): self[4] = value


	@property
	def height(self) -> int: return self[5]

	@height.setter
	def height(self, value: int): self[5] = value


	@property
	def objectid(self) -> int: return self[6]

	@objectid.setter
	def objectid(self, value: int): self[6] = value


	@property
	def rbox_key(self) -> int: return self[7]

	@rbox_key.setter
	def rbox_key(self, value: int): self[7] = value

	# others
	@property
	def enable_right(self) -> bool: 	return bool(int(str(self.rbox_key)[1]))

	@property
	def enable_left(self) -> bool: 		return bool(int(str(self.rbox_key)[2]))

	@property
	def enable_up(self) -> bool: 		return bool(int(str(self.rbox_key)[3]))

	@property
	def enable_bottom(self) -> bool: 	return bool(int(str(self.rbox_key)[4]))

	@property
	def position(self): return pg.Vector2(self.x, self.y)

	@property
	def parentposition(self): return pg.Vector2(self[0], self[1])

	@property
	def offsetrect(self): return [self.offsetx, self.offsety, self.width, self.height]

	@property
	def top(self): return self.y

	@property
	def left(self): return self.x
	
	@property
	def right(self): return (self.x) + (self.width)
	
	@property
	def bottom(self): return (self.y) + (self.height)

	@property
	def centerx(self): 
		return int((self.x) + (self.width/2))

	@property
	def centery(self): return int((self.y) + (self.height/2))

	@property
	def rect(self) -> pg.Rect: return pg.Rect(self.x, self.y, self.width, self.height)

	def offset_to_zero(self): 
		return RectBox([
			self.x, self.y, 
			0, 0, 
			self.width, self.height, 
			self.objectid, self.rbox_key
			]) 

	def outlined(self, value:int) -> TRectBox: 
		return RectBox([
			self.parentx, self.parenty, 
			self.offsetx-value, self.offsety-value, 
			self.width+(value*2), self.height+(value*2), 
			self.objectid, self.rbox_key
			])

	def outlinedy(self, value:int) -> TRectBox: 
		return RectBox([
			self.parentx, self.parenty, 
			self.offsetx, self.offsety-value, 
			self.width, self.height+(value*2), 
			self.objectid, self.rbox_key
			])

	def outlinedx(self, value:int) -> TRectBox: 
		return RectBox([
			self.parentx, self.parenty, 
			self.offsetx-value, self.offsety, 
			self.width+(value*2), self.height, 
			self.objectid, self.rbox_key
			])

	def overlap(self, box:TRectBox) -> bool: return self.rect.colliderect(box.rect)

	def slope_height(self, positionx, array) -> TRectBox:
		j = int(min(max(0, positionx-self.x), len(array)-1))
		return RectBox([
			self.parentx, self.parenty, 
			self.offsetx, self.offsety+array[j], 
			self.width, self.height,
			self.objectid, self.rbox_key
			])
	
	def check_axis(self, box:TRectBox) -> list[int]:
		if (self.centerx - box.centerx) <= 0:    coordx = self.right - box.left
		else:                                   coordx = self.left - box.right

		if (self.centery - box.centery) <= 0:    coordy = self.bottom - box.top
		else:                                   coordy = self.top - box.bottom

		return [int(coordx), int(coordy)]

if __name__ == "__main__":
	box = RectBox([1, 2, 5, 6], [20, 20], 0)
	box1 = RectBox([60, 25, 1, 2, 5, 6, 0, 0])
	print(box.check_axis(box1), box1.objectid, box.objectid)


