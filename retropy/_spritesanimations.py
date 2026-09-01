

class FrameData: 
	def __init__(self, raw_data:dict):
		self.id                 = raw_data["id"]
		self.array              = raw_data["array"]
		self.size               = raw_data["size"]
		self.pivot              = raw_data["pivot"]
		self.duration           = raw_data["duration"]


class AnimationData: 
	def __init__(self, raw_data:dict):
		self.id                 = raw_data["id"]
		self.name               = raw_data["name"]
		self.rotation           = raw_data["rotation"]
		self.speed              = raw_data["speed"]
		self.loop               = raw_data["loop"]
		self.frames             = [FrameData(data) for data in raw_data["frames"]]
		self.length             = len(self.frames)

	   
class SpritesAnimations:
	def __init__(self, raw_data:dict):
		self.signature          = raw_data["signature"]
		self.imagespath         = raw_data["imagespath"]

		self.animation_ids:dict[int, AnimationData]      = {}
		self.animation_names:dict[str, AnimationData]    = {}

		for data in raw_data["datas"]:
			animation = AnimationData(data)
			self.animation_ids[animation.id]        = animation
			self.animation_names[animation.name]    = animation

	def does_Animation_exist(self, animation_name:str) -> bool:
		return animation_name in self.animation_names

	def base_on_by_names(self, spriteanimations):
		animation_names:dict[str, AnimationData] = spriteanimations.animation_names
		last_id = max(self.animation_ids) + 1
		for key in animation_names.keys():
			animation = animation_names[key]

			if not self.animation_names.get(animation.name):
				last_id += 1
				self.animation_ids[last_id]        		= animation
				self.animation_names[animation.name]    = animation
				
		






class AnimationTracker:
	def __init__(self, timer:int = 0, frame:int = 0, old:int = 0, loop:int = 0, has_looped:int = 0):
		self.timer              = timer
		self.frame              = frame
		self.old                = old
		self.loop               = loop
		self.has_looped = has_looped
		
	def handle_animation_by_id(self, animation_package:SpritesAnimations, animation_id:int):
		current_animation = animation_package.animation_ids[animation_id]
		
		self.has_looped         = 0
		if self.old != current_animation.id:
			self.frame          = 0
			self.timer          = 0
			self.loop           = 0
		
		# reset Frame
		if self.frame >= current_animation.length:
			self.frame = current_animation.loop
			self.has_looped     = 1
			self.loop           += 1

		# timer update
		if self.timer >= 65535: self.timer = 0 
		self.timer += current_animation.speed
		current_frame = current_animation.frames[self.frame]

		if self.timer > current_frame.duration:
			self.timer -= current_frame.duration
			self.frame          += 1

		if self.frame >= current_animation.length:
			self.frame = current_animation.loop
			self.has_looped     = 1
			self.loop           += 1
		
		self.old = current_animation.id

	def handle_animation_by_name(self, animation_package:SpritesAnimations, animation_name:str):
		current_animation = animation_package.animation_names[animation_name]
		
		self.has_looped         = 0
		if self.old != current_animation.id:
			self.frame          = 0
			self.timer          = 0
			self.loop           = 0
		
		# reset Frame
		if self.frame >= current_animation.length:
			self.frame = current_animation.loop
			self.has_looped     = 1
			self.loop           += 1

		# timer update
		if self.timer >= 65535: self.timer = 0 
		self.timer += current_animation.speed
		current_frame = current_animation.frames[self.frame]

		if self.timer > current_frame.duration:
			self.timer -= current_frame.duration
			self.frame          += 1

		if self.frame >= current_animation.length:
			self.frame = current_animation.loop
			self.has_looped     = 1
			self.loop           += 1
		
		self.old = current_animation.id