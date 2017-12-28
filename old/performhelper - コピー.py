# -*- coding: utf-8 -*-
import os
import sys
import time
import datetime
import re
import pygame
from pyhooked import Hook, KeyboardEvent#, MouseEvent
print(os.getenv('SDL_AUDIODRIVER'))
print(os.getenv('SDL_AUDIODEV'))

class performHelper():
    def __init__(self):
        self.settings = self.get_settings()
        self.wavs = {val: pygame.mixer.Sound("wav/{}.wav".format(key)) \
                for key, val in self.settings.items()}
        # self.wavs = {val: SoundLoader.load("wav/{}.wav".format(key)) \
        #         for key, val in self.settings.items()}
        #signal.signal(signal.SIGINT, self.handler)
        self.ths = []
        self.before_wav = datetime.datetime.now()
        self.hk = None
        self.wav_margin = 0.07

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

    # def handler(self, signal, frame):
    #     self.end_flag = True
    #     for t in self.ths:
    #         t.join()

    # def playAudio(self, wf_name):
    #     self.wf = wave.open(wf_name, "rb")
    # 
    #     p = pyaudio.PyAudio() # PyAudioのインスタンスを生成 (1)

    #     # Streamを生成(3)
    #     stream = p.open(format=p.get_format_from_width(self.wf.getsampwidth()),
    #                     channels=self.wf.getnchannels(),
    #                     rate=self.wf.getframerate(),
    #                     output=True,
    #                     stream_callback=self.callback)
    # 
    #     # Streamをつかって再生開始 (4)
    #     stream.start_stream()
    # 
    #     # 再生中はひとまず待っておきます (5)
    #     while stream.is_active():
    #         time.sleep(0.1)
    # 
    #     # 再生が終わると、ストリームを停止・解放 (6)
    #     stream.stop_stream()
    #     stream.close()
    #     self.wf.close()
    # 
    #     # close PyAudio (7)
    #     #p.terminate()
    
    # # 再生用のコールバック関数を定義
    # def callback(self, in_data, frame_count, time_info, status):
    #     data = self.wf.readframes(frame_count)
    #     return (data, pyaudio.paContinue)
    
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
        #self.ths.append(threading.Thread(target=self.playAudio, args=(self.wavs[key],)))
        # if self.wavs[key].status != 'stop':
        #     self.wavs[key].stop()
        self.wavs[key].play()
        # wav play start
        #self.ths[-1].start()
        self.before_wav = self.now

if __name__ == "__main__":
    pygame.mixer.pre_init(44100, -16, 1, 512)
    #pygame.mixer.init()
    pygame.init()
    pygame.mixer.set_num_channels(32)
    screen = pygame.display.set_mode((100, 100))
    ph = performHelper()
    ph.mainLoop()
