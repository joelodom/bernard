# Copyright (c) 2013-2015 by Joel Odom & Alex Odom, Marietta, GA All Rights Reserved

import pygame

PLAYER_HIT_SOUND = None
FIRE_SOUND = None
BOMB_COUNTDOWN_SOUND = None
DYNAMITE_SOUND = None
ATOM_BOMB_SOUND = None
SONG = None

def pre_init():
    pygame.mixer.pre_init(22050, -8, 1, 512) # prevents sounds delay

def init():
  global PLAYER_HIT_SOUND, FIRE_SOUND, BOMB_COUNTDOWN_SOUND, DYNAMITE_SOUND, ATOM_BOMB_SOUND
  PLAYER_HIT_SOUND = pygame.mixer.Sound(r'resources\hit.wav')
  FIRE_SOUND = pygame.mixer.Sound(r'resources\fire.wav')
  BOMB_COUNTDOWN_SOUND = pygame.mixer.Sound(r'resources\countdown.wav')
  DYNAMITE_SOUND = pygame.mixer.Sound(r'resources\dynamite.wav')
  ATOM_BOMB_SOUND = pygame.mixer.Sound(r'resources\atom_bomb.wav')

def play_a_song():
  global SONG
  if SONG == None:
    SONG = pygame.mixer.Sound(r'resources\bernard.wav')
  else:
    SONG.stop()
  SONG.play()

def stop_all_sounds():
  PLAYER_HIT_SOUND.stop()
  FIRE_SOUND.stop()
  BOMB_COUNTDOWN_SOUND.stop()
  DYNAMITE_SOUND.stop()
  ATOM_BOMB_SOUND.stop()
