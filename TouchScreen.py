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

#TODO - create try-catch in functions to prevent crashing
#TODO - screen sleeps after a minute of time unused
#           add a thread that is a timer, somehow combine with main and go into this function:
#           add a black screen that tests if user has hit the screen (one button), return to previous activity if it has
#           creates a new thread timer when screen is touched
#TODO - check if website updates, update sensor objects (this should work now)
#TODO - limit character size for number input
#TODO - clean up code

#tODO - create an error log, remove all print statements
#TODO create classes
#TODO create linear reading for calibration screens (simpler to understand)
#TODO boot on start (redo, no longer works...)
#TODO move all screen references into screen class, easier to read TouchScreen class
#TODO determine information that needs to be passed and add that to function passing rather than global

#TODO Thanksgiving
#TODO - Calibration - add all variations of calibration, test that current ones work still, split all calibrations into screen and loop
# temp functions, could be cleaner, still needs refresh of screen returning from checktime taking reads
# ph
# do
# cond
#TODO overhaul the numpad self.calNum to just return the calNum instead of passing it globally, easier in some parts

#TODO - create note that our server will only take up to 6 months worth of data if taking one read an hour
#  ask about if we should do a limit to 6 months size if they change reads per day less than 24
#  if the user changes the reads per day to be less than 24, could they still have data loaded onto the 
#  server for the amount of 6 months, or should I limit the data to be whatever 6 months is worth
#TODO - check login and post readings to website correctly
#TODO - Take pictures with instructions
#TODO - ask about putting in a minimum for the number of reads per day at 1 per hour
