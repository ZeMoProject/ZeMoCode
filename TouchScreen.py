#!/usr/bin/python3.4

import os
import sys
import pygame as pg
import pygame.gfxdraw
import serial # Required for communication with boards
import time # Used for timestamps, delays
import RPi.GPIO as GPIO
from datetime import datetime
import logging
import subprocess
import socket
import yaml
from threading import Thread
from threading import Lock as lock
import Screen
from Screen import *
import requests
import json
import urllib.request
import urllib

class App(object):
    def __init__(self):
        print("ZēMō Initializing")
        self.screen = Screen()
        self.done = False

    def checkQuit(self, eventType):
        if eventType == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
            self.done = True
            self.screen.quit()
            sys.exit()        

    def settings_loop(self):
        while not self.done:
            self.screen.settings_event_screen()
            pg.display.update()
            pg.event.clear()
            pg.event.wait()
            for event in pg.event.get():
                self.checkQuit(event.type)
                if event.type == pg.MOUSEBUTTONDOWN:
                    pok = self.screen.checkCollision(event.pos)
                    if(pok is 5):
                        return          

    # Switches between the event loops depending on button pressed  
    def main_loop(self):
            while not self.done:
                    #try:
                    self.screen.main_menu_screen()
                    pg.display.update()
                    pg.event.clear()  
                    pg.event.wait() 
                    for event in pg.event.get():
                            self.checkQuit(event.type)
                            if event.type == pg.MOUSEBUTTONDOWN:
                                button = self.screen.checkCollision(event.pos)
                                if(button is 7):
                                    self.settings_loop()
                    #except:
                    #pass

    # Initializes pygame and starts touchscreen loop
    def main():
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pg.init()
        App().main_loop()
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    main()
