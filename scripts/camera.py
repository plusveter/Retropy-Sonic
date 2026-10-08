from scripts.macro import * 

UNREACHABLE_VALUE = 10**6 

class Camera:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.mode = 0
		self.tiled_objectid = -1
		
		self.look_timer = 0
		self.look_shift = 0

		self.target_x = 0 
		self.target_y = 0

		self.rect = pygame.Rect(0, 0, 0, 0)
		self.view_size = vec2(0)
		
		# Camera boundaries
		self.bound_data_left  	= [None, 8, UNREACHABLE_VALUE , 0]
		self.bound_data_right 	= [None, 8, -UNREACHABLE_VALUE, 0]
		self.bound_data_up    	= [None, 4, UNREACHABLE_VALUE , 0] # Ypos (or Xpos), Speed, old_decrease_value, enable_decrease
		self.bound_data_down  	= [None, 4, -UNREACHABLE_VALUE, 0]

		self.bound_side_left  	= UNREACHABLE_VALUE
		self.bound_side_right 	= -UNREACHABLE_VALUE
		self.bound_side_up    	= UNREACHABLE_VALUE
		self.bound_side_down  	= -UNREACHABLE_VALUE

		self.bound_Yaxis = False
		self.bound_Xaxis = False

		self.old_level_position = vec2(0)
		self.is_mouse_on_screen = False
		self.mouse_position = vec2(0)
	
	@property
	def resolution_x(self):
		return self.app.screen_resolution[0]

	@property
	def size(self): return self.view_size

	@property
	def position(self): return vec2(self.x, self.y)

	@position.setter
	def position(self, position): self.x, self.y = position
		
	@property
	def top(self): return self.y
	
	@property
	def bottom(self): return self.y + self.view_size.y

	@property
	def right(self): return self.x + self.view_size.x
	
	@property
	def left(self): return self.x
	
	@property
	def screen_rect(self): return pygame.Rect(self.x, self.y, self.view_size.x, self.view_size.y)
	def has_collided_with_screen(self, rect:pygame.Rect): return rect.colliderect(self.screen_rect)

	@property
	def center_x(self): return self.x + (self.view_size.x/2)

	@center_x.setter
	def center_x(self, x): self.x = x - (self.view_size.x/2)

	@property
	def center_y(self): return self.y + (self.view_size.y/2)
	
	@center_y.setter
	def center_y(self, y): self.y = y - (self.view_size.y/2)

	@property
	def center(self): return vec2(self.center_x, self.center_y)

	@center.setter
	def center(self, position): 
		self.center_x = position.x
		self.center_y = position.y

	def handle_new_bound(self):
		
		
		# top
		y, speed, old_decrease_value, enable_decrease = self.bound_data_up
		if not y is None: # verified if "Ypos" value does exist
			self.bound_data_up[2] = old_decrease_value = old_decrease_value+speed
			if self.target_y < y:
				self.bound_side_up = min((self.bottom)+max((y-(self.view_size.y))-self.y, -speed), old_decrease_value)
			self.bound_data_up[0] = None 
		else:
			
			if not enable_decrease: self.bound_side_up = UNREACHABLE_VALUE
			else: self.bound_side_up += speed # Check current speed
			self.bound_data_up[2] = UNREACHABLE_VALUE
			

		# down
		y, speed, old_decrease_value, enable_decrease = self.bound_data_down
		if not y is None:
			self.bound_data_down[2] = old_decrease_value = old_decrease_value-speed
			if self.target_y > y:
				self.bound_side_down = max((self.top)+min(y-self.y, speed), old_decrease_value)
			self.bound_data_down[0] = None
		else:
			if not enable_decrease: self.bound_side_down = -UNREACHABLE_VALUE
			else: self.bound_side_down -= speed
			self.bound_data_down[2] = -UNREACHABLE_VALUE
			

		# left
		x, speed, old_decrease_value, enable_decrease = self.bound_data_left
		if not x is None:
			self.bound_data_left[2] = old_decrease_value = old_decrease_value+speed # Check current speed

			if self.target_x < x:
				self.bound_side_left = min(self.right+max((x-self.view_size.x)-self.x,-speed), old_decrease_value)
			self.bound_data_left[0] = None
		else: 
			if not enable_decrease: self.bound_side_left = UNREACHABLE_VALUE
			else: self.bound_side_left += speed
			self.bound_data_left[2] = UNREACHABLE_VALUE
			

		#right
		x, speed, old_decrease_value, enable_decrease = self.bound_data_right
		if not self.bound_data_right[0] is None:
			self.bound_data_right[2] = old_decrease_value = old_decrease_value-speed
			if self.target_x > x:
				self.bound_side_right = max(self.left+min(x-self.x, speed), old_decrease_value)
			self.bound_data_right[0] = None
		else:
			if not enable_decrease: self.bound_side_right = -UNREACHABLE_VALUE
			else: self.bound_side_right -= speed
			self.bound_data_right[2] = -UNREACHABLE_VALUE
	
	def handle_mouse(self):
		# normalize mouse position to [0,1]
		window_w, window_h = kernel.window.size
		tex_w, tex_h = kernel.window.size

		mouse = vec2(pygame.mouse.get_pos())
		
		u = mouse.x / window_w
		v = mouse.y / window_h

		window_aspect = window_w / window_h
		texture_aspect = tex_w / tex_h

		inside = True

		if window_aspect > texture_aspect:
			# letterboxing (bars left/right)
			scale = texture_aspect / window_aspect
			x_offset = (1.0 - scale) / 2.0

			u = (u - x_offset) / scale
			inside = (u >= 0.0 and u <= 1.0)

		else:
			# pillarboxing (bars top/bottom)
			scale = window_aspect / texture_aspect
			y_offset = (1.0 - scale) / 2.0

			v = (v - y_offset) / scale
			inside = (v >= 0.0 and v <= 1.0)


		self.mouse_position.x = u * kernel.window.size.x
		self.mouse_position.y = v * kernel.window.size.y
		self.is_mouse_on_screen = inside

	def get_scale_position(self, mouse:vec2):
		# normalize mouse position to [0,1]
		window_w, window_h = kernel.window.size
		tex_w, tex_h = kernel.size

		
		u = mouse.x / window_w
		v = mouse.y / window_h

		window_aspect = window_w / window_h
		texture_aspect = tex_w / tex_h

		if window_aspect > texture_aspect:
			# letterboxing (bars left/right)
			scale = texture_aspect / window_aspect
			x_offset = (1.0 - scale) / 2.0
			u = (u - x_offset) / scale

		else:
			# pillarboxing (bars top/bottom)
			scale = window_aspect / texture_aspect
			y_offset = (1.0 - scale) / 2.0
			v = (v - y_offset) / scale

		return vec2(u * kernel.size.x, v * kernel.size.y)

	def pre_update(self):
		
		self.handle_new_bound()
		self.handle_mouse()

	def handle_current_bound(self):
		self.y += max(self.bound_side_down - self.y, 0)
		self.y += min((self.bound_side_up-self.view_size.y)-self.y, 0)
		
		self.x += max(self.bound_side_right - self.x, 0)
		self.x += min((self.bound_side_left-self.view_size.x)-self.x, 0)

	def update(self):
		self.handle_current_bound()
		
	def set_bound(self, 
			   rect:list[int], 
			   side:int,
			   set_speed=None, 
			   enable_decrease=None, 
			   disable_screen_focus=None, 
			   disable_player_focus=None
			   ):

		x, y, width, height = rect
		
		if side == CAMERA_BOUND_TOP:
			if (0-width < x - self.x < self.view_size.x) or disable_screen_focus:
				if (0 < (self.target_x - x) < width) or disable_player_focus:
					if self.target_y+10 < y:
						
						self.bound_data_up[2] = self.bound_side_up
						if not set_speed is None: self.bound_data_up[1] = set_speed
						if not enable_decrease is None: self.bound_data_up[3] = bool(enable_decrease)
						if not self.bound_data_up[0] is None:
							if self.bound_data_up[0] > y: self.bound_data_up[0] = y
						else:
							self.bound_data_up[0] = y

		elif side == CAMERA_BOUND_BOTTOM:
			if (0-width < x - self.x < self.view_size.x) or disable_screen_focus:
				if (0 < (self.target_x - x) < width) or disable_player_focus:
					if self.target_y+10 > y+height:
						self.bound_data_down[2] = self.bound_side_down
						if not set_speed is None: self.bound_data_down[1] = set_speed
						if not enable_decrease is None: self.bound_data_down[3] = bool(enable_decrease)
						if not self.bound_data_down[0] is None:
							if self.bound_data_down[0] < y+height: self.bound_data_down[0] = y+height
						else:
							self.bound_data_down[0] = y+height

		elif side == CAMERA_BOUND_LEFT:
			if (0-height < y - self.y < self.view_size.y) or disable_screen_focus:
				if (0 < (self.target_y - y) < height) or disable_player_focus:
					if self.target_x < x:
						self.bound_data_left[2] = self.bound_side_left
						if not set_speed is None: self.bound_data_left[1] = set_speed
						if not enable_decrease is None: self.bound_data_left[3] = bool(enable_decrease)
						if not self.bound_data_left[0] is None:
							if self.bound_data_left[0] > x: self.bound_data_left[0] = x
						else:
							self.bound_data_left[0] = x

		elif side == CAMERA_BOUND_RIGHT:
			if (0-height < y - self.y < self.view_size.y) or disable_screen_focus:
				if (0 < (self.target_y - y) < height) or disable_player_focus:
					if self.target_x > x+width:
						self.bound_data_right[2] = self.bound_side_right
						if not set_speed is None: self.bound_data_right[1] = set_speed
						if not enable_decrease is None: self.bound_data_right[3] = bool(enable_decrease)
						if not self.bound_data_right[0] is None:
							if self.bound_data_right[0] < x+width: self.bound_data_right[0] = x+width
						else:
							self.bound_data_right[0] = x+width
		
	