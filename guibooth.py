#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
######################################################################
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
######################################################################

import sys, os, time
import threading
import re

import argparse
import pygame
import pyaudio
import wave

from pgelement import PGAction, PGEmptyButton, PGImage, PGLabel, PGBackground, drawElements
from gui_elements import *
from utils import bytestoint, energy, generate_file_name
from audiotools import AudioParams, init_audio_input, play_audio, save_audio
class Condition:
    """ 
    Simple condition to be shared between threads
    """
    state = True

def init_gui(resolution):
    pygame.init()
    pygame.font.init()
    print("using resolution: ",resolution)
    return pygame.display.set_mode(resolution,pygame.NOFRAME)

def start_screen(screen):
    background = PGBackground(START_BACKGROUND_PATH)
    button_start = PGEmptyButton(START_START_BUTTON_RECT, absolute=False)
    
    elements = [background,
                button_start]
    escape_counter = 0
    while True:
        drawElements(screen, elements)
        events = pygame.event.get()
        if button_start.event_check(events) is PGAction.CLICKED:
            return
        for event in events:
            if event.type == pygame.KEYUP :
                if event.key == pygame.K_ESCAPE:
                    escape_counter += 1
                    if escape_counter >= 3:
                        exit(0)
                if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    return
        pygame.time.wait(40)
        
def instruction_screen(screen):
    background = PGBackground(INSTRUCTION_BACKGROUND_PATH)
    button_next = PGEmptyButton(INSTR_NEXT_BUTTON_RECT, absolute=False)
    
    elements = [background,
                button_next]
    while True:
        drawElements(screen, elements)
        events = pygame.event.get()
        if button_next.event_check(events) is PGAction.CLICKED:
            return
        for event in events:
            if event.type == pygame.KEYUP and event.key in [pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE]:
                return
        pygame.time.wait(40)

def gender_screen(screen):
    background = PGBackground(GENDER_BACKGROUND_PATH)
    button_man = PGEmptyButton(GENDER_MAN_BUTTON_RECT, absolute=False)
    button_woman = PGEmptyButton(GENDER_WOMAN_BUTTON_RECT, absolute=False)

    elements = [background,
                button_man,
                button_woman]
    while True:
        drawElements(screen, elements)
        events = pygame.event.get()
        if button_man.event_check(events) is PGAction.CLICKED:
            return True
        if button_woman.event_check(events) is PGAction.CLICKED:
            return False
        for event in events:
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_RETURN, pygame.K_RIGHT, pygame.K_f]:
                    return False
                if event.key in [pygame.K_LEFT, pygame.K_SPACE, pygame.K_h]:
                    return False
        pygame.time.wait(40)

def recording(screen, channels=4): 
    background = PGBackground(RECORDING_BACKGROUND_PATH)
    logo = PGImage(LOGO_PATH, LOGO_RECT, absolute=False)
    logo.visible = False
    text_wait = PGLabel(RECORDING_WAIT_COORD, "Attendez ... (Soyez prêt !)", 100)
    text_wait.visible = True

    text_speak = PGLabel(RECORDING_SPEAK_COORD, "Dites LinTo ! ", 100)
    text_speak.visible = False

    elements = [background,
                logo,
                text_wait,
                text_speak]

    drawElements(screen, elements)
    pygame.time.wait(1000)

    params = AudioParams()
    params.channels = channels

    condition = Condition()
    frames = []
    t = threading.Thread(target=record, args=(params, frames, condition,))
    t.start()
    pygame.time.wait(1000)
    
    logo.visible = True
    text_wait.visible = False
    text_speak.visible = True

    drawElements(screen, elements)
    clock = pygame.time.Clock()
    while condition.state:  
        for event in pygame.event.get():
            if event.type in [pygame.MOUSEBUTTONUP, pygame.KEYUP]:
                condition.state = False
                break
        clock.tick(FPS)
    t.join()
    if len(frames) == 0:
        return None
    return b''.join(frames)
    
def record(params, frames, condition, timeout=5):
    """ Record the audio until:
    - condition is set to false
    or
    - timeout is reached
    or
    - a separate word is detected (at least 3 frames higher than the threshold followed by 2 frames of silence)
    """
    sil_frame_to_end = 2
    stream = init_audio_input(params)
    start_time = time.time()
    is_timeout = False
    #silence frames to compute average silence energy
    for _ in range(10):
        frames.append(stream.read(params.chunk_size * params.channels, exception_on_overflow=False))
    en_frames = [energy(bytestoint(frame, params.channels)) for frame in frames]
    av_sil_en = max(en_frames)
    is_speech = False
    end_frame_sil = 0 # Number of frame of silence after speech
    speech_frames = 0
    #print("threshold",av_sil_en) #debug
    while condition.state:
        frames.append(stream.read(params.chunk_size * params.channels, exception_on_overflow=False))
        en = energy(bytestoint(frames[-1], params.channels))
        #print("enframe", en) #debug
        if  en > av_sil_en * 2:
            speech_frames+=1
            if speech_frames >=3:
                is_speech = True
            end_frame_sil = 0
        elif is_speech:
            speech_frames
            end_frame_sil+=1
            if end_frame_sil >= sil_frame_to_end:
                condition.state = False
        else:
            speech_frames = 0
        if time.time() > start_time + timeout:
            print("Timeout")
            is_timeout = True
            condition.state = False

    if is_timeout:
        frames.clear()
    else:
        frames = frames[:sil_frame_to_end-1]
    stream.stop_stream()
    stream.close()

def confirm_screen(screen, gender):
    background = PGBackground(CONFIRM_BACKGROUND_PATH)
    button_yes = PGEmptyButton(CONFIRM_YES_BUTTON_RECT, absolute=False)
    button_no = PGEmptyButton(CONFIRM_NO_BUTTON_RECT, absolute=False)

    elements = [background,
                button_yes, 
                button_no]
    while True:
        drawElements(screen, elements)
        events = pygame.event.get()
        if button_yes.event_check(events) is PGAction.CLICKED:
            return True
        if button_no.event_check(events) is PGAction.CLICKED:
            return False
        for event in events:
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_ESCAPE, pygame.K_n]:
                    return False
                if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_o]:
                    return True
        pygame.time.wait(40)

def continue_screen(screen, nb_sample):
    background = PGBackground(CONTINUE_BACKGROUND_PATH)
    button_yes = PGEmptyButton(CONTINUE_YES_BUTTON_RECT, absolute=False)
    button_no = PGEmptyButton(CONTINUE_NO_BUTTON_RECT, absolute=False)
    label_counter = PGLabel((0.67,0.035), text=str(nb_sample), font_size=270,color=(230,230,0))

    elements = [background,
                button_yes, 
                button_no,
                label_counter]
    while True:
        drawElements(screen, elements)
        events = pygame.event.get()
        if button_yes.event_check(events) is PGAction.CLICKED:
            return True
        if button_no.event_check(events) is PGAction.CLICKED:
            return False
        for event in events:
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_ESCAPE, pygame.K_n]:
                    return False
                if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_o]:
                    return True
        pygame.time.wait(40)

def check_screen(screen, folder, gender, buffer, channels=4):
    params = AudioParams()
    params.channels = channels
    
    background = PGBackground(CHECK_BACKGROUND_PATH)
    button_yes = PGEmptyButton(CHECK_OK_BUTTON_RECT, absolute=False)
    button_no = PGEmptyButton(CHECK_KO_BUTTON_RECT, absolute=False)
    button_replay = PGEmptyButton(CHECK_REPLAY_BUTTON_RECT, absolute=False)

    elements = [background,
                button_yes, 
                button_no,
                button_replay]

    drawElements(screen, elements)
    
    play_audio(buffer, params)
    
    while True:    
        events = pygame.event.get()
        if button_yes.event_check(events) is PGAction.CLICKED:
            save_audio(params, os.path.join(folder,generate_file_name(folder, gender)), buffer)
            return True
        if button_no.event_check(events) is PGAction.CLICKED:
            return False
        if button_replay.event_check(events) is PGAction.CLICKED:
             play_audio(buffer, params)

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_ESCAPE, pygame.K_n, pygame.K_RIGHT]:
                    return False
                if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_o, pygame.K_LEFT]:
                    return True
                if event.key in [pygame.K_r, pygame.K_UP]:
                     play_audio(buffer, params)
        pygame.time.wait(40)

def failed_screen(screen):
    background = PGBackground(FAILED_BACKGROUND_PATH)
    button_continue = PGEmptyButton(FAILED_RETRY_BUTTON_RECT, absolute=False)
    button_quit = PGEmptyButton(FAILED_QUIT_BUTTON_RECT, absolute=False)
    elements = [background,
                button_continue,
                button_quit]
    drawElements(screen, elements)

    while True:    
        events = pygame.event.get()
        if button_continue.event_check(events) is PGAction.CLICKED:
            return True
        if button_quit.event_check(events) is PGAction.CLICKED:
            return False
        for event in events:
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_ESCAPE]:
                    return False
                if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_c]:
                    return True
        pygame.time.wait(40)

    

def thank_screen(screen, nb_sample):
    background = PGBackground(THANK_BACKGROUND_PATH)
    elements = [background]
    while True:
        drawElements(screen, elements)
        events = pygame.event.get()
        for event in events:
            if event.type in [pygame.KEYUP, pygame.MOUSEBUTTONUP]:
                return
        pygame.time.wait(40)

def main(folder, channels, resolution):
    screen = init_gui(resolution)
    while True: #main loop
        start_screen(screen)
        nb_sample = 0
        instruction_screen(screen)
        gender = gender_screen(screen)
        doContinue = confirm_screen(screen, gender)
        while doContinue == True:
            buffer = recording(screen, channels=channels)
            if buffer is None:
                doContinue = failed_screen(screen)
            else:
                added = check_screen(screen, folder, gender, buffer, channels=channels)
                if added: nb_sample += 1
                doContinue = continue_screen(screen, nb_sample)
        if nb_sample > 0:
            thank_screen(screen, nb_sample)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GUI interface to record audio samples for wake word corpus building')
    parser.add_argument('folder', default='/tmp', help='the folder where the sample are saved')
    parser.add_argument('-c', dest='channels', help="Input device number of channel", type=int, default=2)
    parser.add_argument('-r', dest='resolution',default=DEFAULT_RES, type=int, nargs=2, help="Screen resolution")
    args = parser.parse_args()
    main(args.folder, args.channels, args.resolution)