# -*- coding: utf-8 -*-

from os import path
#####################################
########### UI ELEMENTS #############
#####################################
# Values are relative to display size
# => pos 0.5,0.5 is the screen center
# pygame Rect format is (coord_x, coord_x, w, h)
DIR_PATH = path.dirname(path.realpath(__file__))
IMG_FOLDER = "%s/slides" % DIR_PATH
DEFAULT_RES = (1920,1080)
FPS = 30
FRAME_DURATION = int(1000/FPS)

########## START SCREEN #############
START_BACKGROUND_PATH = path.join(IMG_FOLDER, "start.png")
START_START_BUTTON_RECT = (0.55,0.49,0.36,0.21)

########## INSTRUCTION ##############
INSTRUCTION_BACKGROUND_PATH = path.join(IMG_FOLDER, "instructions.png")
INSTR_NEXT_BUTTON_RECT = (0.67,0.82,0.25,0.16)

######### GENDER SCREEN #############
GENDER_BACKGROUND_PATH = path.join(IMG_FOLDER, "gender.png")
GENDER_MAN_BUTTON_RECT = (0.09,0.17,0.33,0.74)
GENDER_WOMAN_BUTTON_RECT = (0.48,0.17,0.42, 0.74)

######### RECORDING SCREEN ##########
RECORDING_BACKGROUND_PATH = path.join(IMG_FOLDER, "recording.png")
LOGO_PATH = path.join(IMG_FOLDER, "linto_alpha.png")
LOGO_RECT = (0.25,0.25,0.5,0.5)
RECORDING_LOGO_RECT = (0.25,0.25,0.5,0.5)
RECORDING_WAIT_COORD = (0.25,0.5)
RECORDING_SPEAK_COORD = (0.35,0.8)

######### CONFIRM SCREEN ###########
CONFIRM_BACKGROUND_PATH = path.join(IMG_FOLDER, "confirm.png")
CONFIRM_YES_BUTTON_RECT = (0.20,0.34,0.58,0.30)
CONFIRM_NO_BUTTON_RECT = (0.20,0.69,0.58,0.27)

######### CONTINUE SCREEN ###########
CONTINUE_BACKGROUND_PATH = path.join(IMG_FOLDER, "continue.png")
CONTINUE_YES_BUTTON_RECT = (0.20,0.34,0.58,0.30)
CONTINUE_NO_BUTTON_RECT = (0.20,0.69,0.58,0.27)

########### CHECK SCREEN ############
CHECK_BACKGROUND_PATH = path.join(IMG_FOLDER, "check.png")
CHECK_OK_BUTTON_RECT =(0.02,0.53,0.44,0.41)
CHECK_KO_BUTTON_RECT = (0.50,0.53,0.44,0.40)
CHECK_REPLAY_BUTTON_RECT =  (0.7,0.009,0.26,0.2)

########### FAILED SCREEN ###########
FAILED_BACKGROUND_PATH = path.join(IMG_FOLDER, "failed.png")
FAILED_RETRY_BUTTON_RECT = (0.51, 0.51,0.42,0.29)
FAILED_QUIT_BUTTON_RECT = (0.51,0.72,0.42,0.29)


########### THANK SCREEN ############
THANK_BACKGROUND_PATH = path.join(IMG_FOLDER, "thank.png")

############### COLOR ###############
BLACK = (0,0,0)
WHITE = (255,255,255)
LIGHT_GRAY = (200,200,200)
