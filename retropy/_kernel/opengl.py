import moderngl, pygame, numpy

errors = dict(
	not_setup = LookupError(f"[ModernGL] The module the module wasn't setup.")
)

def check_enable(func):
	def wrapper(self, *args, **kwargs):
		if not self.enable:
			raise errors['not_setup']
		return func(self, *args, **kwargs)
	return wrapper

def skip_enable(func):
	def wrapper(self, *args, **kwargs):
		if not self.enable: return
		return func(self, *args, **kwargs)
	return wrapper

class OpenGL:
	buffer_array:numpy.ndarray
	vertex_shader:str
	fragment_shader:str

	def __init__(self, kernel):
		self.kernel = kernel
		self.enable = False

	def setup(self, buffer_array:numpy.ndarray, vertex_shader:str, fragment_shader:str):
		self.enable = True
		self.kernel.window.flags = self.kernel.window.flags| pygame.OPENGL | pygame.DOUBLEBUF
		self.kernel.window.does_update = False

		self.buffer_array = buffer_array
		self.vertex_shader = vertex_shader
		self.fragment_shader = fragment_shader

	@skip_enable
	def create(self):
		print("[OpenGL] is going to setup")
		self.ctx            = moderngl.create_context()
		self.program        = self.ctx.program( vertex_shader=  self.vertex_shader,fragment_shader=self.fragment_shader)
		self.render_object  = self.ctx.vertex_array(self.program, [(self.ctx.buffer(data=self.buffer_array), '2f 2f', 'vert', 'texcoord')])
		self.textureid = 0
		print("[OpenGL] has been setup")

	@check_enable
	def prepare_texture(self, size, depth=4) -> moderngl.Texture:
		tex          = self.ctx.texture([int(value) for value in size], depth)
		tex.filter   = (moderngl.NEAREST, moderngl.NEAREST)
		tex.swizzle  = 'BGRA'
		return tex

	@check_enable
	def create_texture(self, size, depth=1, dtype=None):
		index_tex = self.ctx.texture([int(value) for value in size], depth, dtype=dtype)
		index_tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
		index_tex.repeat_x = False
		index_tex.repeat_y = False
		return index_tex

	@check_enable
	def surf_to_texture(self, surface:pygame.Surface, depth=4) -> moderngl.Texture:
		tex = self.ctx.texture(surface.get_size(), depth)
		tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
		tex.swizzle = 'BGRA'
		tex.write(surface.get_view('1'))
		return tex

	@check_enable
	def update_texture(self, tex:moderngl.Texture, surface:pygame.Surface):
		tex.write(surface.get_view('1'))

	@check_enable
	def use_texture(self, texture:moderngl.Texture, name:str) -> None:
		texture.use(self.textureid)
		self.program[name] = self.textureid
		self.textureid += 1

	@skip_enable
	def refresh(self):
		self.render_object.render(mode=moderngl.TRIANGLE_STRIP)
