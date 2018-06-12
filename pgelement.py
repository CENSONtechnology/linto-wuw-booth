# -*- coding: utf-8 -*-

import pygame
from enum import Enum

class PGAction(Enum):
    CLICKED = 1
    OVER = 0

class PGElement:
    priority = 0
    surface = None
    rect = pygame.Rect((0,0,0,0))
    visible = True
    overed = False

    def event_check(self, events: list):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1: 
                if self.rect.collidepoint(event.pos):
                    return PGAction.CLICKED
                if event.type == pygame.MOUSEMOTION:
                    if self.rect.collidepoint(event.pos):
                        self.overed = True
                    else:
                        self.overed = False
        return None

    def draw(self, screen: pygame.Surface, frame_count: int):
        if self.visible:
            screen.blit(self.surface, (self.rect[0], self.rect[1]))
    
    def _relative_to_absolute(self, rel_rect):
        """ Return absolute coordinate based on relative coordinate and display size"""
        display_info = pygame.display.Info()
        current_w = display_info.current_w
        current_h = display_info.current_h
        transform_v = (current_w, current_h,current_w, current_h)
        abs_rect = pygame.Rect(tuple((ratio * transform_v[i] for i, ratio in enumerate(rel_rect))))
        return abs_rect

    def _resize(self, new_size, absolute = True):
        display_info = pygame.display.Info()
        current_w = display_info.current_w
        current_h = display_info.current_h
        if not absolute:
            new_w = int(new_size[0] * current_w)
            new_h = int(new_size[1] * current_h)
            new_size = (new_w, new_h)
        self.surface = pygame.transform.scale(self.surface, new_size)

class PGEmptyButton(PGElement):
    def __init__(self, rect, absolute = True):
            self.rect = pygame.Rect(rect)
            if not absolute:
                self.rect = pygame.Rect((self._relative_to_absolute(rect)))
            self.visible = False
    
    def draw(self, screen, frame_count):
        if self.visible:
            pygame.draw.rect(screen, (0,0,0), self.rect, 3)

class PGImage(PGElement):
    priority = 1
    def __init__(self, path: str, rect, absolute: bool = True):
        self.surface = pygame.image.load(path)
        self.rect = pygame.Rect(rect)
        if not absolute:
            self.rect = pygame.Rect((self._relative_to_absolute(rect)))
        self._resize((rect[2], rect[3]), absolute)
        

class PGLabel(PGElement):
    priority = 2
    def __init__(self, location: tuple, text: str = "", font_size: int = 8, font = None, color=(0,0,0), absolute: bool = False):
        font = pygame.font.Font(font, font_size)
        self.surface = font.render(text, 1, color)
        self.rect = location + (self.surface.get_size())
        if not absolute:
            self.rect = pygame.Rect(self._relative_to_absolute(self.rect))

class PGBackground(PGElement):
    def __init__(self, location):
        self.surface = pygame.image.load(location)
        displayInfo = pygame.display.Info()
        self.surface = pygame.transform.scale(self.surface, (displayInfo.current_w, displayInfo.current_h))
        self.rect = (0,0) + (displayInfo.current_w, displayInfo.current_h)


def drawElements(screen, elements, frame_count: int = 0):
    """ Draw given element on screen base on their priority value """
    screen.fill((255,255,255))
    for element in sorted(elements, key=lambda x: x.priority):
        element.draw(screen, frame_count)
    pygame.display.flip()