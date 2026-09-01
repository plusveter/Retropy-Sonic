from typing import overload, TypeVar
import numpy as np
import pygame as pg


TDataMask = TypeVar("DataMask", bound="DataMask")
new_objectid = 0
num_objectid = 0


class DataMask:
	"""
	DataMask
	=======
	Reworked in 2026
	
	Structured dmask:
	---------------

	 ** **
	    - convert surface and array (or list) to make a **DataMask**:
	>>> box = RectBox(surface, [60, 25, 1, 2, 5, 6, 0, 0]) 
	>>> box = RectBox(surface, position_offset_size, 20) 
	>>> #=> DataMask(surface, (array|list)=>[parentx, parenty, offsetx, offsety, width, height], loopmax[int]=32)

		 
	Credit
	------

	 ** **
		- @PlusVeter (or Ucstorm)
		 
	"""
	__slots__ = ("mask", "arraydata", "loopmax")
	
	mask: pg.Mask
	arraydata: np.ndarray
	loopmax: int

	def __init__(self, mask, arraydata, loopmax=4):
		self.mask = mask
		self.arraydata = arraydata
		self.loopmax = loopmax
		

	@property
	def parentx(self) -> int: return self.arraydata[0]

	@parentx.setter
	def parentx(self, value: int): self.arraydata[0] = value


	@property
	def parenty(self) -> int: return self.arraydata[1]

	@parenty.setter
	def parenty(self, value: int): self.arraydata[1] = value


	@property
	def x(self) -> int: return  self.arraydata[2] + self.arraydata[0]

	@x.setter
	def x(self, value: int): self.arraydata[2] = value - self.arraydata[0]


	@property
	def y(self) -> int: return self.arraydata[3]+self.arraydata[1]

	@y.setter
	def y(self, value: int): self.arraydata[3] = value - self.arraydata[1]


	@property
	def offsetx(self) -> int: return self.arraydata[2]

	@offsetx.setter
	def offsetx(self, value: int): self.arraydata[2] = value


	@property
	def offsety(self) -> int: return self.arraydata[3]

	@offsety.setter
	def offsety(self, value: int): self.arraydata[3] = value


	@property
	def width(self) -> int: return self.arraydata[4]

	@width.setter
	def width(self, value: int): self.arraydata[4] = value


	@property
	def height(self) -> int: return self.arraydata[5]

	@height.setter
	def height(self, value: int): self.arraydata[5] = value


	@property
	def rect(self) -> pg.Rect: return pg.Rect(self.x, self.y, self.width, self.height)

	def collide(self, dmask:TDataMask): return self.mask.overlap(dmask.mask, [dmask.x-self.x, dmask.y-self.y])

	def colliderect(self, dmask:TDataMask): return self.rect.colliderect(dmask.rect)
	
	def draw_rect(self, surface:pg.Surface, color, offset:list[int]=[0, 0]): 
		pg.draw.rect(surface, color, [self.x-offset[0], self.y-offset[1], self.width, self.height])

	def draw_surface(self, surface:pg.Surface, offset:list[int]=[0, 0]): 
		surface.blit(self.mask.to_surface(), (self.x-offset[0], self.y-offset[1]))

	def rotate_by_90degrees(self, MODE, parentpostion:list=None):
		""" MODE: 0 ,1, 2, 3"""

		if not parentpostion is None:	parentx, parenty = parentpostion[0], parentpostion[1]
		else: 							parentx, parenty = self.parentx, self.parenty

		if MODE == 0: 
			return self
		elif MODE == 1: 
			return DataMask(
				pg.mask.from_surface(pg.transform.rotate(self.mask.to_surface(), 90)),
				np.array([parentx, parenty, self.offsety+1, -(self.offsetx + self.width-1), self.height, self.width], dtype=np.int64)
			)
		elif MODE == 2: 
			return DataMask(
				pg.mask.from_surface(pg.transform.rotate(self.mask.to_surface(), 180)),
				np.array([parentx, parenty, -(self.offsetx + self.width+1), -(self.offsety + self.height+1), self.width, self.height], dtype=np.int64)
			)
		elif MODE == 3: 
			return DataMask(
				pg.mask.from_surface(pg.transform.rotate(self.mask.to_surface(), 90)),
				np.array([parentx, parenty, -(self.offsety + self.height+1), self.offsetx, self.height, self.width], dtype=np.int64)
			)
		else:
			return self



	def repel_floor(self, dmask:TDataMask):
		running = True
		LOOP = 0

		if self.loopmax <= 0: return 0
		while running:
			if self.mask.overlap(dmask.mask, [dmask.x-self.x, dmask.y-(self.y-LOOP)]):

				LOOP += 1
			else: running = False
			if LOOP >= self.loopmax: running = False
		return LOOP

	def attract_floor(self, dmask:TDataMask):
		running = True
		LOOP = 0

		if self.loopmax <= 0: return 0
		while running:
			if not self.mask.overlap(dmask.mask, [dmask.x-self.x, dmask.y-(self.y+LOOP)]):
				LOOP += 1
			else:running = False
			if LOOP >= self.loopmax: running = False
		return LOOP

	def repel_rightside(self, dmask:TDataMask):
		running = True
		LOOP = 0

		if self.loopmax <= 0: return 0
		while running:
			if self.mask.overlap(dmask.mask, [dmask.x-(self.x-LOOP), dmask.y-self.y]): 
				LOOP += 1
			else: running = False
			if LOOP >= self.loopmax:running = False
		return LOOP


	def attract_rightside(self, dmask:TDataMask):
		running = True
		LOOP = 0

		if self.loopmax <= 0: return 0
		while running:
			if not self.mask.overlap(dmask.mask, [dmask.x-(self.x+LOOP), dmask.y-self.y]):
				LOOP += 1
			else:running = False
			if LOOP >= self.loopmax: running = False
		return LOOP


	def repel_ceiling(self, dmask:TDataMask):
		running = True
		LOOP = 0

		if self.loopmax <= 0: return 0
		while running:
			if self.mask.overlap(dmask.mask, [dmask.x-self.x, dmask.y-(self.y+LOOP)]):
				LOOP += 1
			else: running = False
			if LOOP >= self.loopmax:running = False
		return -LOOP


	def attract_ceiling(self, dmask:TDataMask):
		running = True
		LOOP = 0

		if self.loopmax <= 0: return 0
		while running:
			if not self.mask.overlap(dmask.mask, [dmask.x-self.x, dmask.y-(self.y-LOOP)]):
				LOOP += 1
			else:running = False
			if LOOP >= self.loopmax: running = False
		return -LOOP


	def repel_leftside(self, dmask:TDataMask):
		running = True
		LOOP = 0

		if self.loopmax <= 0: return 0
		while running:
			if self.mask.overlap(dmask.mask, [dmask.x-(self.x+LOOP), dmask.y-self.y]):
				LOOP += 1
			else: running = False
			if LOOP >= self.loopmax:running = False
		return -LOOP


	def attract_leftside(self, dmask:TDataMask):
		running = True
		LOOP = 0

		if self.loopmax <= 0: return 0
		while running:
			if not self.mask.overlap(dmask.mask, [dmask.x-(self.x-LOOP), dmask.y-self.y]):
				LOOP += 1
			else:running = False
			if LOOP >= self.loopmax: running = False
		return -LOOP