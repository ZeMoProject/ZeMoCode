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
from threading import Thread
from threading import Lock
from Screen import Screen
from Connection import Connection
from Probes.pH import PH
from Probes.Conductivity import Conductivity
from Probes.DissolvedOxygen import DissolvedOxygen
from Probes.Temperature import Temperature

class App(object):
    def __init__(self):
        print("ZēMō Initializing")
        self.screen = Screen()
        self.conn = Connection()
        self.screen.drawImage("logo.png", self.screen.background.get_rect(), 223, 57)
        self.done = False
        self.takeReadFlag = True
        self.readingNow = False
        self.waitTime = 0
        jsonFile = self.conn.getJSONconfig()
        self.daysToKeep = jsonFile["settings"]["days"]
        self.readsPerDay = jsonFile["settings"]["reads"]
        self.timeList = []
        piName = self.conn.getPiName()
        self.phSensor = PH(jsonFile, piName, self.screen)
        self.condSensor = Conductivity(jsonFile, piName, self.screen)
        self.dOSensor = DissolvedOxygen(jsonFile, piName, self.screen)
        self.tempSensor = Temperature(jsonFile, piName, self.screen)
        self.sensorList = []
        self.sensorList.append(self.condSensor)
        self.sensorList.append(self.dOSensor)
        self.sensorList.append(self.tempSensor)
        self.sensorList.append(self.phSensor)
        self.t2 = Thread(target=App.checkTime_loop, args=(self,))
        self.t2.start()
        self.update_reads_per_day()        

    def checkQuit(self, eventType):
        if eventType == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
            self.done = True
            self.screen.quit()
            sys.exit()

	# Checks the values and opens notify() if values are out of range, the ooR occurs here
    def takeReads_checkAlarms(self):
        sensors = []
        jsonFile = self.conn.getConfigData()
        self.daysToKeep = jsonFile["settings"]["days"]
        self.readsPerDay = jsonFile["settings"]["reads"] 
        self.update_reads_per_day()           
        piName = self.conn.getPiName()        
        for sensor in self.sensorList:
            sensor.refresh(jsonFile, piName)            
            sensor.takeRead(self.conn)
            read = float(sensor.getCurrRead())
            if read > float(sensor.getHighRange()) or read < float(sensor.getLowRange()):
                sensors.append(sensor)
        if len(sensors) > 0:
            self.conn.sendOutofRange(sensors)

    # Updates the list of times checked in the CheckTime() function
    def update_reads_per_day(self):
        if int(self.readsPerDay) > 96:
            self.readsPerDay = "96"
        self.timeList = []
        hours = 24 / int(self.readsPerDay)
        i = 0.00
        j = 0.00
        while i < 24:
            i = hours + i
            if i < 24:
                addHour = int(i)
                y = i % 1
                j = (y * 60) / 100
                addTime = addHour + round(j, 2)
                addThis = str(round(addTime, 2))
                self.timeList.append(addThis)

    # A constantly running loop that has an individual thread
    # Checks the time for taking automated reads
    def checkTime_loop(self):
        while(self.done != True):
            try:
                currMin = datetime.now().minute
                currHour = datetime.now().hour
                if int(currHour) < 1:
                    currHour = "0"
                else:
                    currHour = str(round(int(currHour), 0))
                if currMin > 9:
                    uCurrTime = currHour + "." + str(round(currMin, 0))
                elif currMin < 1:
                    uCurrTime = currHour + ".0"
                else:
                    uCurrTime = currHour + ".0" + str(round(currMin, 0))
                currTime = str(uCurrTime)
                #potential increase to speed, try:
                #self.timeList.index(currTime)
                if(currTime in self.timeList and self.takeReadFlag is True) or currTime == "0.0":  
                    self.takeReadFlag = False
                    self.waitTime = currMin + 1
                    if(self.waitTime > 59):
                        self.waitTime = 0
                    self.readingNow = True
                    #try:
                    takingReads = Thread(target=App.taking_reads_loop, args=(self,))
                    takingReads.start()
                    #    #screens = {0 : self.main_menu_screen(),
                    #    #           1 : self.update_event_screen("Temperature", "tp", self.temperature),
                    #    #           2 : self.numpad_event_screen("Low", "lowRange", 0),
                    #    #           3 : self.settings_event_screen(),
                    #    #           4 : self.advanced_settings_event_screen(),
                    #    #}
                    #    #screens[self.currScreen]()
                    #except:
                    #    self.readingNow = False
                    #    pass
                    self.takeReads_checkAlarms()
                    pg.event.clear()
                    self.readingNow = False
                    time.sleep(2)
                elif self.waitTime < int(currMin) and self.waitTime != 0:
                    self.takeReadFlag = True
            except Exception as e:
                self.readingNow = False
                pass

    # Advanced Settings
    def advanced_settings_event(self):
        while not self.done:
            if not self.readingNow:
                self.screen.advanced_settings_event_screen()
                pg.display.update()
                pg.event.clear()
                pg.event.wait()
                if not self.readingNow:
                    for event in pg.event.get():
                        self.checkQuit(event.type)
                        if event.type == pg.MOUSEBUTTONDOWN:
                            button = self.screen.checkCollision(event.pos)
                            if button is 5:
                                return
                            elif button is 3:
                                #re-register - clears all the input data of piName, secret key, and account
                                if self.screen.reregister() is True:
                                    self.conn.resetAccount()
                                    jsonFile = self.conn.getConfigData()
                                    piName = self.conn.getPiName()
                                    for sensor in self.sensorList:
                                        sensor.refresh(jsonFile, piName)
                                    self.screen.drawMessage("Re-download the software")
                                    time.sleep(4)
                                    self.done = True
                                else:
                                    self.screen.advanced_settings_event_screen()
                                    pg.display.update()
                            elif button is 4:
                                self.done = True
                                return
                            else:
                                button = self.screen.checkCollisionSmallBtns(event.pos)
                                if button is 4:
                                    files = []
                                    for item in self.sensorList:
                                        file2 = item.getFilename()[:-4]
                                        files.append(file2 + "_log.csv")
                                    self.conn.sendLogData(files)                                                             

    def settings_event(self):
        while not self.done:
            if not self.readingNow:
                self.screen.settings_event_screen(self.conn.getEth0(), self.conn.getWlan0(),
                    self.readsPerDay, self.daysToKeep)
                pg.display.update()
                pg.event.clear()
                pg.event.wait()
                if not self.readingNow:
                    for event in pg.event.get():
                        self.checkQuit(event.type)
                        if event.type == pg.MOUSEBUTTONDOWN:
                            button = self.screen.checkCollision(event.pos)
                            if button is 5:
                                return
                            elif button is 7:
                                self.advanced_settings_event()
                            elif button is 2:
                                #refresh all sensors
                                jsonFile = self.conn.getConfigData()
                                piName = self.conn.getPiName()
                                for sensor in self.sensorList:
                                    sensor.refresh(jsonFile, piName)


    # Screen shows "Taking Reads..."
    def taking_reads_loop(self):
        while(self.readingNow):
            self.screen.drawMessage("Taking Reads   ")
            pg.display.update()
            if(self.readingNow):
                time.sleep(1)
                self.screen.drawMessage("Taking Reads.  ")
                pg.display.update()
                if(self.readingNow):    
                    time.sleep(1)                  
                    self.screen.drawMessage("Taking Reads.. ")
                    pg.display.update()
                    if(self.readingNow):
                        time.sleep(1)
                        self.screen.drawMessage("Taking Reads...")
                        pg.display.update()
                        if(self.readingNow):
                            time.sleep(1)
            self.screen.canvas.fill((0,0,0))
        self.screen.canvas.fill((0,0,0))

    # Update Probe
    def update_event(self, sensor):
        while(1):
            if not self.readingNow:
                    #try:
                    self.screen.update_event_screen(sensor)
                    pg.display.update()
                    pg.event.clear()
                    pg.event.wait()
                    if not self.readingNow:
                        for event in pg.event.get():
                                self.checkQuit(event.type)
                                if event.type == pg.MOUSEBUTTONDOWN:
                                    button = self.screen.checkCollision(event.pos)
                                    if button is 1:
                                        sensor.calibrate()
                                    elif button is 2:
                                        jsonFile = self.conn.getConfigData()
                                        piName = self.conn.getPiName()                                        
                                        sensor.refresh(jsonFile, piName)
                                    elif button is 5:
                                        return
                                    elif button is 8 or button is 4 or button is 3:
                                        #try:
                                        self.readingNow = True
                                        takingReads = Thread(target=App.taking_reads_loop, args=(self,))
                                        takingReads.start()
                                        jsonFile = self.conn.getConfigData()
                                        piName = self.conn.getPiName()
                                        sensor.refresh(jsonFile, piName)                                              
                                        sensor.takeRead(self.conn)
                                        self.readingNow = False
                                        #except:
                                        #pass"""
                                        time.sleep(1)
                                        self.screen.update_event_screen(sensor)                                                                            
                    #except:
                    #pass

    # Switches between the event loops depending on button pressed  
    def main_event_loop(self):
            while not self.done:
                    #try:
                    if not self.readingNow:
                        self.screen.main_menu_screen(self.condSensor.getCurrRead(), 
                            self.dOSensor.getCurrRead(), self.phSensor.getCurrRead(), 
                            self.tempSensor.getCurrRead())
                        pg.display.update()
                        pg.event.clear()  
                        pg.event.wait()
                        if not self.readingNow:
                            for event in pg.event.get():
                                self.checkQuit(event.type)
                                if event.type == pg.MOUSEBUTTONDOWN:
                                    button = self.screen.checkCollision(event.pos)
                                    if button is 7:
                                        self.settings_event()
                                    elif button is 1:
                                        self.update_event(self.condSensor)
                                    elif button is 2:
                                        self.update_event(self.dOSensor)
                                    elif button is 3:
                                        self.update_event(self.phSensor)
                                    elif button is 4:
                                        self.update_event(self.tempSensor)
                    #except:
                    #pass

# Initializes pygame and starts touchscreen loop
def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    App().main_event_loop()
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()

""" Urgent """
#TODO - reinstitute try/catch to all portions of code
""" Screen """
#TODO - global variable with the current screen on it, so the checktime loop can 
#   redraw the screen after taking scheduled readings
""" Other """
#TODO - timeout thread, returns to main screen and blacks out