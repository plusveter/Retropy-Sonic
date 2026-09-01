import pygame



class SoundFX:
    def __init__(self, kernel):
        self.kernel = kernel
        self.id = 0
        self.volume = 0
        self.channels:dict[str, dict[str:"channels", pygame.mixer.Channel]] = {}
        self.pre_volume = -1

        self.current_channel = -1

    def refresh(self):
        MIXERSCALE = self.kernel.mixerscale
        if self.pre_volume != self.volume:
            for channel_name in self.channels:
                self.channels[channel_name]["channel"].set_volume(self.volume/ (MIXERSCALE)+0.001)

        self.pre_volume = self.volume


    def new_channel(self, name:str):
        if self.channels.get(name): return 1

        self.channels[name] = dict(
            channel = pygame.mixer.Channel(self.id),
            volumes = dict(left=1, right=1)
        )

        self.channels[name]["channel"].set_volume(self.volume/ (self.kernel.mixerscale)+0.001)
        self.id += 1

    def select_channel(self, name):
        if self.channels.get(name):     self.current_channel = name
        else:                           self.current_channel = -1

    def play(self, sound:pygame.mixer.Sound, loop = False, name:str=None):
        MIXERSCALE = self.kernel.mixerscale
        if name is None: name = self.current_channel
        if self.current_channel == -1: 
            sound.set_volume(self.volume/ (MIXERSCALE)+0.001)
            sound.play(loops=loop)
        else: self.channels[name]["channel"].play(sound, loops=loop)
    
    def stop(self, channel_name):
        self.channels[channel_name]["channel"].stop()
    
    def set_channel_volumes(self, volume_:int|list):
        if self.current_channel != -1:
            if isinstance(volume_, int):
                self.channels[self.current_channel]["volumes"] = dict(left=volume_, right=volume_)
            elif isinstance(volume_, list):
                self.channels[self.current_channel]["volumes"] = dict(left=volume_[0], right=volume_[0])

    def get_channel(self):
        if self.current_channel == -1: return -1
        return self.channels[self.current_channel]["channel"]