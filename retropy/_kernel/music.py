import pygame as pg
from .macro import *
from retropy._datapack import datapack

class Music:
    def __init__(self, kernel):
        self.kernel = kernel

        self.id             = 0
        self.lists          = {}
        self.volume         = 0
        
        self.media        = 0
        self.media_volume = 0

        self.transition_active      = 1
        self.transition_first       = 0 
        self.transition_last        = 0
        self.transition_delays      = dict(start=0, end=0)
        self.transition_frame       = 0
        self.transition_flag        = 0

        pg.mixer.music.set_volume(0)

    def get_data(self, id:int):
        return self.lists[id]

    def add(self, filename:str, start_end:list[int], volume:int, author:str):
        self.id += 1
        self.lists[self.id] = dict(
            filename=filename, 
            volume=volume, 
            start_end=start_end, 
            author = author,
            pos=0, 
            isactive=False,
            repeated =0
        )
        return self.id
   
    def refresh(self):
        self.handle_transition()

        # handle music continuity
        mixerscale = self.kernel.mixerscale

        if not self.volume*self.media_volume == int(pg.mixer.music.get_volume()*mixerscale):
            pg.mixer.music.set_volume(min(self.volume*self.media_volume/ mixerscale+0.001, 10)) # volume state max set to 10


        if self.media > 0 and len(self.lists) != 0:
            music_pos = self.lists[self.media]["pos"]
            start_end = self.lists[self.media]["start_end"]
            pos = (pg.mixer.music.get_pos()/1000)+music_pos

            if pos >= start_end[1]:
                self.lists[self.media]["repeated"] += 1
                pg.mixer.music.play()
                pg.mixer.music.set_pos(start_end[0])
                self.lists[self.media]["pos"] = start_end[0]

    def select_by_id(self, id:int=-1, fade_out:int = 0, fade_in:int=0, flag:int=SELECTMUSIC_RESET, debug=False):
        if debug: print(f"[{self.__class__.__name__} | selected ]", "| id : ", id, "| fadeout :",fade_out, "| fadein :", fade_in, "| flag :", flag)
        self.transition_active  = 1, 
        self.transition_first   = self.media
        self.transition_last    = id
        self.transition_delays  = dict(start=fade_out, end=fade_in)
        self.transition_frame   = self.kernel.frames
        self.transition_flag    = flag

 
    def handle_transition(self):
        frames = self.kernel.frames
        if self.transition_active:
            startframe  = self.transition_frame
            start_delay = self.transition_delays["start"]
            end_delay   = self.transition_delays["end"]
            music1_id   = self.transition_first
            music2_id   = self.transition_last
            musicflag   = self.transition_flag
            SELECTMUSIC_CONTINUE
            if (self.media == music1_id) and (end_delay >= 0):
                if end_delay == 0:
                    self.media_volume = 0
                elif music1_id != 0:
                    self.media_volume -= 1/(end_delay/self.lists[music1_id]["volume"])

                if (frames - startframe) >= end_delay:
                    pos = 0
                    if self.media != 0 and self.media != music2_id:
                        music_pos = self.lists[self.media]["pos"]
                        pos = (pg.mixer.music.get_pos()/1000)+music_pos
                        self.lists[self.media]["pos"] = pos

                    if self.media != music2_id:
                        pg.mixer.music.unload()
                        pg.mixer.music.stop()

                    if music2_id > 0:
                        if musicflag == SELECTMUSIC_RESET: 
                            pos = 0
                            if self.media != 0 :self.lists[self.media]["repeated"] = 0 
                        elif musicflag == SELECTMUSIC_CONTINUE: pos = self.lists[music2_id]["pos"]
                        elif musicflag == SELECTMUSIC_FOLLOW: 
                            if music1_id != 0 and music2_id != 0:
                                new_start_end   = self.lists[music2_id]["start_end"]
                                old_start_end   = self.lists[music1_id]["start_end"]
                                old_repeated    = self.lists[music1_id]["repeated"]

                                if old_repeated > 0 or pos >= old_start_end[0]:
                                    old_deltatime = old_start_end[1] - old_start_end[0]
                                    new_deltatime = new_start_end[1] - new_start_end[0]

                                    new_pos = max(pos-old_start_end[0], 0)
                                    pos = new_start_end[0] + (((old_repeated*old_deltatime)+new_pos) % new_deltatime)
                                    self.lists[music1_id]["repeated"] = (((old_repeated*old_deltatime)+new_pos) // new_deltatime)
                                else:
                                    pos = pos % new_start_end[1]


                        if self.media != music2_id:
                            loading_music = self.lists[music2_id]
                            datapack.load_musicfile(loading_music["filename"])
                            pg.mixer.music.play()
                            pg.mixer.music.set_pos(pos)
                            self.lists[music2_id]["pos"] = pos

                    self.media = music2_id
                    self.transition_frame = frames
                    self.transition_delays["end"] = -1
                    
            
            elif self.media == music2_id:

                if music2_id > 0:
                    if start_delay == 0:
                        self.media_volume = self.lists[music2_id]["volume"]
                        self.transition_active = False
                    elif (frames - startframe) <= start_delay: 
                        self.media_volume = ((frames - startframe)/max(start_delay, 1))*self.lists[music2_id]["volume"]
                    else:
                        self.transition_active = False
                else:
                    self.transition_active = False

    def stop(self):
        self.select_by_id()
        pg.mixer.music.unload()
        pg.mixer.music.stop()

    def pause(self):
        pg.mixer.music.pause()

    def unpause(self):
        pg.mixer.music.unpause()