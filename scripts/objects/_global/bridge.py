from scripts.base import *


# I don't have anything to say, except for the fact that this function is at least more than 4 years old
def build_bridgedata(lenght, size=16):
	"""
	This is use to cache the ammount of data that the bridge require, it is necessary to do that to prevent lag
	"""
	size = lenght*size
	SegmentAmount = int(size/size)
	array = numpy.arange(size*SegmentAmount).reshape([size, SegmentAmount])

	for C in range(size):
		number_rect = (C / size) + 1
		if number_rect <= SegmentAmount/2: MaxDepression = number_rect*2
		else: MaxDepression = ((SegmentAmount - number_rect) + 1) * 2

		for i in range(0, SegmentAmount):
			difference = abs((i + 1) - number_rect)

			if i < number_rect:log_distance = 1 - (difference / number_rect)
			else: log_distance = 1 - (difference / ((SegmentAmount - number_rect) + 1))

			Log = math.floor(MaxDepression * math.sin(math.radians(90 * log_distance)))
			array[C, i] = Log
	return array



class Bridge(TiledObjectEntity):
	namedatas = dict(
		bridge_9_log = dict(size=vec2(9, 1), data=build_bridgedata(9))
	)

	def __init__(self, parent):
		super().__init__(parent)
		self.value = 0
		self.entity_position = vec2(0)
		self.other_entity_id = vec2(0)
		self.general_hitbox = rect(0, 0, 0, 0)

	
	def update(self):
		super().update()
		graphic.palette = P_OBJECTS
		
		bridge_data = self.namedatas.get(self.tiled_name, -1)
		self.hitbox = rect(self.tiled_offset.x, self.tiled_offset.y, self.tiled_width, self.tiled_height)

		if bridge_data == -1:
			prerender_rect(self.hitbox, 4)
			self.draw()
			return     

		log_diameter = 16
		size = bridge_data["size"] * log_diameter
		array = bridge_data["data"]

		
		segment_amount = int(size.x/log_diameter)
		

		# return collision
		RectX =  (numpy.arange(segment_amount)*log_diameter)+ self.position.x
		number_rect = max(0, min((log_diameter*segment_amount)-1, int((self.entity_position.x - self.position.x) - 1)))

		log_list = array[number_rect]
		log_id = int(number_rect/log_diameter)
		
		RectY = log_list + self.position.y
		C = log_list + self.position.y
		
		C[C==0] = 0
		C[C!=0] = ((((self.position.y/C[C!=0])-1)*1000)*(self.value/100))
		RectY = (RectY*(C/1000))+RectY

		self.general_hitbox = rect([0, RectY[log_id] , size.x, size.y])

		dynamic_sprites = general.dynamic_sprites
		animationlenght = len(dynamic_sprites.animation_names["Bridge"].frames) -1

		if self.value > 95: RectY[RectY!=self.position.y] = self.position.y

		for i in range(0, segment_amount):
			frame = animationlenght-min(abs(((i*log_diameter)+self.position.x)-self.entity_position.x)/8, animationlenght)+1
			new_animation_tracker = AnimationTracker(frame=max(0, animationlenght-int(frame*(1-((self.value)/100)))))
			prerender_name_sprite(dynamic_sprites, "Bridge", new_animation_tracker)
			self.draw(vec2((RectX[i]+8), (RectY[i]+8)))

		self.refresh_each_log_position(log_diameter, segment_amount, array)

		
	def refresh_each_log_position(self, log_diameter, segment_amount, array, size):
		"""
		This fonction was litteraly create to manage Entity other than the player
		"""

		entity_distance = size.x*2
		for player in check_object_by_classname("Player"): # It is necesary to test on player before, but I'm wondering if these are something to be aware of 

			# TODO: Huge probleme in terms of collision and repartition of code for the bridge to update
			# I think the possibility of using the old methode of collision is litteraly a bad idea, since I was made to support only one player
			# My best idea would be to copy from someone else, I guess this solution might require less time than trying to figuring by myself

			# Update the entity position, if it is standing on the hitbox
			if player.platform_standing == self.entity_id:
				player.Stand_on_Platform(player.hitbox, self, self.general_hitbox)

				distance = abs((self.x + self.general_hitbox.centerx) - (player.x + player.hitbox.centerx))
				if entity_distance > distance:
					entity_distance = distance
					self.other_entity_id = player.entity_id
				
			if player.Check_Object_Collision_Platform(player.hitbox, self, self.general_hitbox, 0):
				player.Stand_on_Platform(player.hitbox, self, self.general_hitbox)

			# Change position of each log
			if self.other_entity_id != player.entity_id: continue

			player_bottomrect = player.hitbox.bottom
			number_rect = max(0, min((log_diameter*segment_amount)-1, int((player.position.x - self.position.x) - 1)))

			log_list = array[number_rect]
			log_id = int(number_rect/log_diameter)

			# Update Segment
			y_axis = self.position.y - player_bottomrect-8
			if ((y_axis < 0) and ((log_diameter * segment_amount) - 1 > number_rect > 0) and (log_list[log_id] != 0) and (y_axis + log_list[log_id] > -log_diameter)): 
				y_axis = (-y_axis)/log_list[log_id]
			else:
				y_axis = 0

			if player.platform_standing == self.entity_id: 
				self.value += -20
			else: 
				self.value +=10
			
			self.value = max(0, min(100-int(y_axis*100), self.value))