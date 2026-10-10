from ..datapack import *

from .tools.reader import Reader

def fix_path(path:str):
	return path.replace("\\", "/").replace("//", "/")

class RSDKv5(DataPack):
	""" Retro Software Developpement Kit version 5"""
	type = "rsdkv5"
	
	def __init__(self, path:str):
		super().__init__()
		self.data_bytes = 0
		self.reader = Reader()
		self.datapack_pointers = {}
		self.reader.pos = 0

		with open(path, mode='rb') as wrapper: 
			self.data_bytes = wrapper.read()
			signature = self.reader.read_string_selectbytes(self.data_bytes, 6)
			if signature != "RSDKv5": raise EncodingWarning(f"This file isn't a RSDKv5 DataPack(Current Signature: {signature})")

			file_ammount = self.reader.read_Uint_2bytes(self.data_bytes)
			for i in range(file_ammount):
				hashed_filename = self.reader.read_selectbytes(self.data_bytes, 16)
				self.datapack_pointers[hashed_filename] = [
					self.reader.read_Uint_4bytes(self.data_bytes), 
					self.reader.read_Uint_3bytes(self.data_bytes), 
					self.reader.read_Uint_1bytes(self.data_bytes)]
		wrapper.close()
	def check_filepath(self, path:str) ->bool:
		path = fix_path(path)
		# This function is also used to generate hashkeys

		# check if file does exist with in the datafile
		if self.datapack_pointers.get(path, -1) == -1: 
			hash_list = [0] * 16
			filename_upper = path.lower().encode("ascii")
			md5_buf = hashlib.md5(filename_upper).digest()

			for y in range(0, 16, 4):
				hash_list[y + 3] = md5_buf[y + 0]
				hash_list[y + 2] = md5_buf[y + 1]
				hash_list[y + 1] = md5_buf[y + 2]
				hash_list[y + 0] = md5_buf[y + 3]

			if self.datapack_pointers.get(bytes(hash_list), -1) == -1: 
				print("File not found:", path)
				return False
			
			self.datapack_pointers[path] = self.datapack_pointers[bytes(hash_list)]
			self.datapack_pointers.pop(bytes(hash_list))
		return True

	def load_text(self, path:str):
		path = fix_path(path)

		self.check_filepath(path) # 
		current_pos = self.reader.pos
		self.reader.pos, size, encrypted = self.datapack_pointers[path]
		data = self.reader.read_string_selectbytes(self.data_bytes, size)
		self.reader.pos =  current_pos
		return data
	
	def load_datafile(self, path:str):
		path = fix_path(path)

		self.check_filepath(path)
		current_pos = self.reader.pos
		self.reader.pos, size, encrypted = self.datapack_pointers[path]
		data = self.reader.read_selectbytes(self.data_bytes, size)
		self.reader.pos =  current_pos
		return data

	def load_XMLfile(self, path:str) -> xmlET.ElementTree:
		path = fix_path(path)

		self.check_filepath(path)
		current_pos = self.reader.pos
		self.reader.pos, size, encrypted = self.datapack_pointers[path]
		data = xmlET.parse(io.BytesIO(self.reader.read_selectbytes(self.data_bytes, size)))
		self.reader.pos =  current_pos

		return data

	def load_jsonfile(self, path:str) -> dict:
		path = fix_path(path)

		self.check_filepath(path)
		current_pos = self.reader.pos
		self.reader.pos, size, encrypted = self.datapack_pointers[path]
		data = json.load(io.BytesIO(self.reader.read_selectbytes(self.data_bytes, size)))
		self.reader.pos =  current_pos
		return data

	def load_8b_imagefile(self, path:str) -> pygame.Surface:
		path = fix_path(path)

		self.check_filepath(path)
		current_pos = self.reader.pos
		self.reader.pos, size, encrypted = self.datapack_pointers[path]
		image = pygame.image.load(io.BytesIO(self.reader.read_selectbytes(self.data_bytes, size))).convert(8)
		self.reader.pos =  current_pos
		return image

	def load_imagefile(self, path:str) -> pygame.Surface:
		path = fix_path(path)

		self.check_filepath(path)
		current_pos = self.reader.pos
		self.reader.pos, size, encrypted = self.datapack_pointers[path]
		image = pygame.image.load(io.BytesIO(self.reader.read_selectbytes(self.data_bytes, size))).convert()
		self.reader.pos =  current_pos
		return image

	def load_soundfile(self, path:str) -> pygame.Sound:
		path = fix_path(path)

		self.check_filepath(path)
		current_pos = self.reader.pos
		self.reader.pos, size, encrypted = self.datapack_pointers[path]
		sound = pygame.mixer.Sound(io.BytesIO(self.reader.read_selectbytes(self.data_bytes, size)))
		self.reader.pos =  current_pos
		return sound

	def load_musicfile(self, path:str):
		path = fix_path(path)

		self.check_filepath(path)
		current_pos = self.reader.pos
		self.reader.pos, size, encrypted = self.datapack_pointers[path]
		pygame.mixer.music.load(io.BytesIO(self.reader.read_selectbytes(self.data_bytes, size)))
		self.reader.pos =  current_pos
