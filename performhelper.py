# -*- coding: utf-8 -*-
import os
import sys
import time
import datetime
import re
import pygame
from pyhooked import Hook, KeyboardEvent#, MouseEvent

class performHelper():
    def __init__(self):
        self.settings = self.get_settings()
        self.wavs = {val: pygame.mixer.Sound("wav/{}.wav".format(key)) \
                for key, val in self.settings.items()}
        self.before_wav = datetime.datetime.now()
        self.hk = None
        self.wav_margin = 0.05

    def get_settings(self, setting_name="settings.txt"):
        with open(setting_name, "r") as f:
            lines = f.readlines()

        splitlines = []
        for line in lines:
            if line != "" and line[0] != "#":
                tmp = re.sub(r"[ \r\n]", "", line)
                tmp = tmp.split("=")
                splitlines.append(tmp)

        settings = {}
        for splitline in splitlines:
            if len(splitline) > 1:
                settings[splitline[0]] = splitline[1]
        return settings

    def mainLoop(self):
        # create a hook manager
        self.hk = Hook()
        # watch for all mouse events
        self.hk.handler = self.handle_events
        #hm.handler = self.OnKeyboardEvent
        # set the hook
        self.hk.hook()

    def handle_events(self, args):
        if isinstance(args, KeyboardEvent):
            self.now = datetime.datetime.now()
            diff = self.now - self.before_wav
            self.audio_contoroler(diff, args)
    
        # if isinstance(args, MouseEvent):
        #     print(args.mouse_x, args.mouse_y)
 
    def audio_contoroler(self, diff, args):
        if diff.total_seconds() < self.wav_margin or args.event_type != "key down":
            return

        key = args.current_key
        if 'Lmenu' in args.pressed_key or 'Rmenu' in args.pressed_key:
            key = "alt+" + key
        if 'Lcontrol' in args.pressed_key or 'Rcontrol' in args.pressed_key:
            key = "ctrl+" + key
        if 'Lshift' in args.pressed_key or 'Rshift' in args.pressed_key:
            key = "shift+" + key
        key = key.lower()

        if key not in self.wavs.keys():
            #print("Invalid key: {}".format(key))
            return
        
        print("push {}".format(key))
        # audio
        self.wavs[key].play()
        self.before_wav = self.now

if __name__ == "__main__":
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    pygame.mixer.set_num_channels(32)
    screen = pygame.display.set_mode((100, 100))
    ph = performHelper()
    ph.mainLoop()
