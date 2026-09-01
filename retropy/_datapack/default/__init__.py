from ..datapack import *


class Default(DataPack):
    """ Retro Software Developpement Kit version 5"""
    type = "default"
    
    def __init__(self):
        super().__init__()

    def check_filepath(self, path:str) ->bool:
        return os.path.isfile(path)

    def load_text(self, path:str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        if not os.path.isfile(path):
            raise ValueError("Path must point to a file, not a directory.")
        
        if not os.access(path, os.R_OK):
            raise PermissionError(f"File is not readable: {path}")
        
        with open(path, mode='r') as wrapper: # b is important -> binary
            data = wrapper.read()
        wrapper.close()
        return data
    
    def load_datafile(self, path:str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        if not os.path.isfile(path):
            raise ValueError("Path must point to a file, not a directory.")
        
        if not os.access(path, os.R_OK):
            raise PermissionError(f"File is not readable: {path}")
        
        with open(path, mode='rb') as wrapper: # b is important -> binary
            data = wrapper.read()
        wrapper.close()
        return data

    def load_jsonfile(self, path:str) -> pygame.Surface:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        if not os.path.isfile(path):
            raise ValueError("Path must point to a file, not a directory.")
        
        if not os.access(path, os.R_OK):
            raise PermissionError(f"File is not readable: {path}")

        with open(path, 'r') as wrapper: data = json.load(wrapper)
        wrapper.close()
        return data

    def load_8b_imagefile(self, path:str) -> pygame.Surface:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        if not os.path.isfile(path):
            raise ValueError("Path must point to a file, not a directory.")
        
        if not os.access(path, os.R_OK):
            raise PermissionError(f"File is not readable: {path}")
        
        return pygame.image.load(path).convert(8)

    def load_imagefile(self, path:str) -> pygame.Surface:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        if not os.path.isfile(path):
            raise ValueError("Path must point to a file, not a directory.")
        
        if not os.access(path, os.R_OK):
            raise PermissionError(f"File is not readable: {path}")
        
        return pygame.image.load(path).convert()

    def load_soundfile(self, path:str) -> pygame.Surface:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        if not os.path.isfile(path):
            raise ValueError("Path must point to a file, not a directory.")
        
        if not os.access(path, os.R_OK):
            raise PermissionError(f"File is not readable: {path}")
        
        return pygame.mixer.Sound(path)

    def load_musicfile(self, path:str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        if not os.path.isfile(path):
            raise ValueError("Path must point to a file, not a directory.")
        
        if not os.access(path, os.R_OK):
            raise PermissionError(f"File is not readable: {path}")
        
        pygame.mixer.music.load(path)
