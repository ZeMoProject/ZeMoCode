#!/usr/bin/python3.4
import os, sys, re
import pygame as pg
import pygame.gfxdraw
import time

class Screen(object):
    def __init__(self):
        CAPTION = "Current Reads"
        pg.display.set_caption(CAPTION)
        screenInfo = pg.display.Info()
        self.SCREEN_SIZE = (screenInfo.current_w, screenInfo.current_h)
        self.SCREEN_WIDTH = screenInfo.current_w
        self.SCREEN_HEIGHT = screenInfo.current_h        
        pg.display.set_mode(self.SCREEN_SIZE)
        #pg.display.toggle_fullscreen()
        self.canvas = pg.display.get_surface()
        self.background = pygame.Surface(self.canvas.get_size())
        self.keys = pg.key.get_pressed()
        # Hides Mouse, still allows click events
        pg.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        
        leftOffset = self.convertWidth(5)
        rightOffset = self.convertWidth(162.5)
        height = self.convertHeight(92.5)
        widthNormal = self.convertWidth(152.5)
        widthSmall = self.convertWidth(100)
        topTop = self.convertHeight(45)
        topBtm = self.convertHeight(142.5)
        topMid = self.convertHeight(92.5)
        backBtnW = self.convertWidth(35)
        backBtnH = self.convertHeight(35) 
        numHeight = self.convertWidth(70)
        numWidth = self.convertWidth(58)
        numTop =self.convertHeight(120) 
        numBtmTop = self.convertHeight(195) 
        btmBtnTop = self.convertHeight(5) 
        midLeftOffset = self.convertWidth(83.75)
        leftTwo = self.convertWidth(68)
        leftThree = self.convertWidth(131)
        leftFour = self.convertWidth(194)
        leftFive = self.convertWidth(257)

        self.topLeft = pg.Rect(leftOffset,topTop,widthNormal,height)
        self.btmLeftSmall = pg.Rect(leftOffset,topBtm,widthSmall,height)
        self.btmMidSmall = pg.Rect(self.convertWidth(110),topBtm,widthSmall,height)
        self.btmRightSmall = pg.Rect(self.convertWidth(215),topBtm,widthSmall,height)
        self.btmLeft = pg.Rect(leftOffset,topBtm,widthNormal,height)
        self.topRight = pg.Rect(rightOffset,topTop,widthNormal,height)
        self.btmBar = pg.Rect(leftOffset, topBtm, self.convertWidth(310), height)

        self.midLeft = pg.Rect(leftOffset,topMid,widthNormal,height)
        self.midRight = pg.Rect(rightOffset,topMid,widthNormal,height)
        self.centerBtn = pg.Rect(midLeftOffset,topMid,widthNormal,height)

        self.btmRight = pg.Rect(rightOffset,topBtm,widthNormal,height)
        self.backBtn = pg.Rect(leftOffset,btmBtnTop,backBtnW,backBtnH)
        self.middleBtn = pg.Rect(midLeftOffset,topTop,widthNormal,height)
        self.settingsBtn = pg.Rect(self.convertWidth(280),btmBtnTop,backBtnW,backBtnH)

        self.one = pg.Rect(leftOffset,topTop,numWidth,numHeight)
        self.two = pg.Rect(leftTwo,topTop,numWidth,numHeight)
        self.three = pg.Rect(leftThree,topTop,numWidth,numHeight)
        self.four = pg.Rect(leftFour,topTop,numWidth,numHeight)
        self.five = pg.Rect(leftFive,topTop,numWidth,numHeight)
        self.six = pg.Rect(leftOffset,numTop,numWidth,numHeight)
        self.seven = pg.Rect(leftTwo,numTop,numWidth,numHeight)
        self.eight = pg.Rect(leftThree,numTop,numWidth,numHeight)
        self.nine = pg.Rect(leftFour,numTop,numWidth,numHeight)
        self.zero = pg.Rect(leftFive,numTop,numWidth,numHeight)
        self.period = pg.Rect(leftFive,numBtmTop,numWidth,backBtnH)
        self.submitBtn = pg.Rect(leftFour,numBtmTop,numWidth,backBtnH)
        self.deleteBtn = pg.Rect(leftFive,btmBtnTop,numWidth,backBtnH)

    def convertWidth(self, size):
        try:
            width = (size/320) * self.SCREEN_WIDTH
            return width
        except:
            return 10

    def convertHeight(self, size):
        try:
            height = (size/240) * self.SCREEN_HEIGHT
            return height
        except:
            return 10

    # Settings screen
    def settings_event_screen(self, eth0, wlan0, readsPerDay, daysToKeep):
        try:
            self.canvas.fill((0,0,0))
            color = pg.Color("yellow")

            self.drawText(str(wlan0), 18, color, self.topLeft, 0, 30)
            self.drawText(str(eth0), 18, color, self.topLeft, 0, 0)

            self.drawText("ip Address:", 20, color, self.topLeft, 0, -30)
            self.drawText("Refresh", 20, color, self.topRight, 0, -10)
            self.drawText("Sensors", 20, color, self.topRight, 0, 10)
            self.drawText("Days Kept:", 20, color, self.btmLeft, 0, -10)
            self.drawText("Reads/Day:", 20, color, self.btmRight, 0, -10)
            self.drawText(str(readsPerDay), 20, color, self.btmRight, 0, 10)
            self.drawText(str(daysToKeep), 20, color, self.btmLeft, 0, 10)           

            self.drawImage("settings_icon.png", self.settingsBtn, 35, 35)
            self.drawTitle("Settings", 20, color)            

            pg.gfxdraw.rectangle(self.canvas, self.topLeft, color)
            pg.gfxdraw.rectangle(self.canvas, self.btmLeft, color)
            pg.gfxdraw.rectangle(self.canvas, self.topRight, color)
            pg.gfxdraw.rectangle(self.canvas, self.btmRight, color)
            self.drawImage("back_btn.png", self.backBtn, 35, 35)            
            pg.display.update()
        except:
            pass

    # Screen shows "Taking Reads..."
    def taking_reads_loop(self):
        try:
            color = pg.Color("steelblue1")
            #add while loop starting here, for when threading occurs
            self.drawText("Taking Reads   ", 15, color, self.background.get_rect(), 0, 0)                   
            self.drawText("Taking Reads   ", 15, color, self.background.get_rect(), 0, 0)                   
            self.drawText("Taking Reads   ", 15, color, self.background.get_rect(), 0, 0)                   
            pg.display.update()
            time.sleep(2)
            self.drawText("Taking Reads.  ", 15, color, self.background.get_rect(), 0, 0)                   
            pg.display.update()
            time.sleep(2)                  
            self.drawText("Taking Reads.. ", 15, color, self.background.get_rect(), 0, 0)                   
            pg.display.update()
            time.sleep(2)
            self.drawText("Taking Reads...", 15, color, self.background.get_rect(), 0, 0)                   
            pg.display.update()
            time.sleep(2)
            self.canvas.fill((0,0,0))
        except:
            pass

    # Advanced Settings screen
    def advanced_settings_event_screen(self):
        try:
            self.canvas.fill((0,0,0))

            color = pg.Color("plum1")
            self.drawText("EXIT", 20, color, self.btmRight, 0, 0)
            self.drawText("Email", 20, color, self.topLeft, 0, -10)
            self.drawText("History", 20, color, self.topLeft, 0, +10)            
            self.drawText("Re-Register", 20, color, self.btmLeft, 0, 0)
            self.drawText("Remove", 20, color, self.topRight, 0, -10)
            self.drawText("History", 20, color, self.topRight, 0, +10)

            pg.gfxdraw.rectangle(self.canvas, self.btmLeft, color)
            pg.gfxdraw.rectangle(self.canvas, self.btmRight, color)
            pg.gfxdraw.rectangle(self.canvas, self.topRight, color)
            pg.gfxdraw.rectangle(self.canvas, self.topLeft, color)

            self.drawTitle("Advanced Settings", 20, color)            

            self.drawImage("back_btn.png", self.backBtn, 35, 35)            
            pg.display.update()
        except:
            pass

    # Update range values screen
    def update_event_screen(self, sensor):
        try:
            self.canvas.fill((0,0,0))
            color = pg.Color("orange")
            self.drawTitle(str(sensor.getName()), 20, color)                        
            self.drawImage("back_btn.png", self.backBtn, 35, 35)            

            self.drawText(str(sensor.getCurrRead()), 20, color, self.btmMidSmall, 0, 25)
            self.drawText("Low", 20, color, self.btmLeftSmall, 0, 5)
            self.drawText("High", 20, color, self.btmRightSmall, 0, 5)
            self.drawText("Take Read", 20, color, self.btmMidSmall, 0, -25)
            self.drawText("Current", 20, color, self.btmMidSmall, 0, 5)
            self.drawText(str(sensor.getLowRange()), 20, color, self.btmLeftSmall, 0, 25)
            self.drawText(str(sensor.getHighRange()), 20, color, self.btmRightSmall, 0, 25)
            self.drawText("Calibrate", 20, color, self.topLeft, 0, 0)
            self.drawText("Refresh", 20, color, self.topRight, 0, 0)

            pg.gfxdraw.rectangle(self.canvas, self.topLeft, color)
            pg.gfxdraw.rectangle(self.canvas, self.btmBar, color)
            pg.gfxdraw.rectangle(self.canvas, self.topRight, color)

            pg.display.update()     
        except:
            pass

    # Numpad screen
    def numpad_event_screen(self, title):
        try:
            self.canvas.fill((0,0,0))
            color = pg.Color("yellow")
            self.drawText("1", 60, color, self.one, 0, 0)
            self.drawText("2", 60, color, self.two, 0, 0)
            self.drawText("3", 60, color, self.three, 0, 0)
            self.drawText("4", 60, color, self.four, 0, 0)
            self.drawText("5", 60, color, self.five, 0, 0)
            self.drawText("6", 60, color, self.six, 0, 0)
            self.drawText("7", 60, color, self.seven, 0, 0)
            self.drawText("8", 60, color, self.eight, 0, 0)
            self.drawText("9", 60, color, self.nine, 0, 0)
            self.drawText("0", 60, color, self.zero, 0, 0)
            self.drawText(".", 60, color, self.period, 0, -10)

            myfont = pg.font.SysFont("monospace", int(round(self.convertHeight(20))))
            title2 = myfont.render(str(title), 1, color)
            newRangeText = myfont.render("Cal. Value:", 1, color)
 
            self.drawText("Submit", 15, color, self.submitBtn, 0, 0)
            self.drawImage("back_btn.png", self.backBtn, 35, 35)            

            pg.gfxdraw.rectangle(self.canvas, self.one, color)
            pg.gfxdraw.rectangle(self.canvas, self.two, color)
            pg.gfxdraw.rectangle(self.canvas, self.three, color)
            pg.gfxdraw.rectangle(self.canvas, self.four, color)
            pg.gfxdraw.rectangle(self.canvas, self.five, color)
            pg.gfxdraw.rectangle(self.canvas, self.six, color)
            pg.gfxdraw.rectangle(self.canvas, self.seven, color)
            pg.gfxdraw.rectangle(self.canvas, self.eight, color)
            pg.gfxdraw.rectangle(self.canvas, self.nine, color)
            pg.gfxdraw.rectangle(self.canvas, self.period, color)
            pg.gfxdraw.rectangle(self.canvas, self.zero, color)
            pg.gfxdraw.rectangle(self.canvas, self.submitBtn, color)
            pg.gfxdraw.rectangle(self.canvas, self.deleteBtn, color)

            self.canvas.blit(newRangeText, (self.convertWidth(5),self.convertHeight(195)))
            self.canvas.blit(title2, (self.convertWidth(50),self.convertHeight(10)))
            pg.display.update()
        except:
            pass

    def main_menu_screen(self, condRead, dORead, phRead, tempRead):
        try:
            self.canvas.fill((0,0,0))
            color = pg.Color("green")
            self.drawTitle("Current Reads", 20, color)
            self.drawText("pH:", 20, color, self.btmLeft, 0, -10)
            self.drawText("Cond:", 20, color, self.topLeft, 0, -10)
            self.drawText("DO:", 20, color, self.topRight, 0, -10)
            self.drawText("Temp:", 20, color, self.btmRight, 0, -10)
            self.drawText(condRead, 20, color, self.topLeft, 0, 10)
            self.drawText(phRead, 20, color, self.btmLeft, 0, 10)
            self.drawText(dORead, 20, color, self.topRight, 0, 10)
            self.drawText(tempRead, 20, color, self.btmRight, 0, 10)            
                       
            pg.gfxdraw.rectangle(self.canvas, self.topLeft, color)
            pg.gfxdraw.rectangle(self.canvas, self.btmLeft, color)
            pg.gfxdraw.rectangle(self.canvas, self.topRight, color)
            pg.gfxdraw.rectangle(self.canvas, self.btmRight, color)
            self.drawImage("settings_icon.png", self.settingsBtn, 35, 35)
            pg.display.update()
        except:
            pass

    def register_screen(self):
        try:
            self.canvas.fill((0,0,0))        
            color = pg.Color("steelblue1")
            self.drawTitle("Register Your Pi", 15, color)
            self.drawText("You must click \"Accept\" on the", 15, color, self.centerBtn, 0, -95) 
            self.drawText("\"Manage Your Connections\" screen", 15, color, self.centerBtn, 0, -80)
            self.drawText("before clicking on \"Register\"", 15, color, self.centerBtn, 0, -65)         
            self.drawText("Register", 15, color, self.midLeft, 0, 0)
            self.drawText("Request Again", 15, color, self.midRight, 0, 0)
            pg.gfxdraw.rectangle(self.canvas, self.midLeft, color) 
            pg.gfxdraw.rectangle(self.canvas, self.midRight, color)   
            pg.display.update()
            while(1):
                pg.event.clear()
                pg.event.wait()
                for event in pg.event.get():
                    if event.type is pg.MOUSEBUTTONDOWN:
                        if self.midLeft.collidepoint(event.pos):                         
                            return 1
                        elif self.midRight.collidepoint(event.pos):
                            return 2
        except:
            pass
    
    def reregister(self):
        try:
            self.canvas.fill((0,0,0))        
            color = pg.Color("steelblue1")
            self.drawTitle("Re-Register Your Pi", 15, color)
            self.drawText("Are you sure?", 15, color, self.centerBtn, 0, -95)         
            self.drawText("Yes", 24, color, self.midLeft, 0, 0)
            self.drawText("No", 24, color, self.midRight, 0, 0)        
            pg.gfxdraw.rectangle(self.canvas, self.midRight, color) 
            pg.gfxdraw.rectangle(self.canvas, self.midLeft, color)             
            pg.display.update()
            while(1):
                pg.event.clear()
                pg.event.wait()
                for event in pg.event.get():
                    if event.type is pg.MOUSEBUTTONDOWN: 
                        if self.midLeft.collidepoint(event.pos):
                            return True
                        elif self.midRight.collidepoint(event.pos):
                            return False
        except:
            pass

    def drawImage(self, imageName, location, width, height):
        try:
            image = pg.image.load("/home/pi/ZeMoCode/images/" + str(imageName))
            imageTransform = pg.transform.scale(image, (int(round(self.convertWidth(width))),int(round(self.convertHeight(height)))))
            imageRect = imageTransform.get_rect()
            imageRect.centerx = location.centerx
            imageRect.centery = location.centery        
            self.canvas.blit(imageTransform, imageRect)
            pg.display.update()
        except:
            pass

    # Draws normal text
    def drawText(self, text, textSize, color, location, xOffset, yOffset):
        try:
            myfont = pg.font.SysFont("monospace", int(round(self.convertHeight(textSize))))
            textPrint = myfont.render(text, 1, color)        
            textpos = textPrint.get_rect()
            textpos.centerx = location.centerx + self.convertWidth(xOffset)
            textpos.centery = location.centery + self.convertHeight(yOffset)
            self.canvas.blit(textPrint, textpos)
        except:
            pass

    # Draws the titles
    def drawTitle(self, title, textSize, color):
        try:
            myfont = pg.font.SysFont("monospace", int(round(self.convertHeight(textSize))))              
            myfont.set_underline(True)
            textPrint = myfont.render(title, 1, color)                
            textpos = textPrint.get_rect()
            textpos.centerx = self.background.get_rect().centerx
            textpos.centery = self.background.get_rect().top + self.convertHeight(20)
            self.canvas.blit(textPrint, textpos)
            myfont.set_underline(False)  
        except:
            pass     

    def drawMessage(self, text):
        try:
            self.canvas.fill((0,0,0))        
            color = pg.Color("steelblue1")
            myfont = pg.font.SysFont("monospace", int(round(self.convertHeight(20))))         
            textPrint = myfont.render(text, 1, color)        
            textpos = textPrint.get_rect()
            textpos.centerx = self.background.get_rect().centerx
            textpos.centery = self.background.get_rect().centery
            self.canvas.blit(textPrint, textpos)
            pg.display.update()                
        except:
            pass
    # For all screens except numpad
    def checkCollision(self, eventPos):
        if self.topLeft.collidepoint(eventPos):
            return 1
        elif self.topRight.collidepoint(eventPos):
            return 2
        elif self.btmLeft.collidepoint(eventPos):
            return 3
        elif self.btmRight.collidepoint(eventPos):
            return 4
        elif self.backBtn.collidepoint(eventPos):
            return 5
        elif self.settingsBtn.collidepoint(eventPos):
            return 7
        elif self.btmBar.collidepoint(eventPos):
            return 8
        else:
            return 0
    
    def checkCollisionSmallBtns(self, eventPos):
        if self.btmLeftSmall.collidepoint(eventPos):
            return 1
        elif self.btmMidSmall.collidepoint(eventPos):
            return 2
        elif self.btmRightSmall.collidepoint(eventPos):
            return 3
        elif self.middleBtn.collidepoint(eventPos):
            return 4            
        else:
            return 0        

    def checkNumpad(self, eventPos):
        if self.one.collidepoint(eventPos):
            return "1"
        elif self.two.collidepoint(eventPos):
            return "2"
        elif self.three.collidepoint(eventPos):
            return "3"
        elif self.four.collidepoint(eventPos):
            return "4"
        elif self.five.collidepoint(eventPos):
            return "5"
        elif self.six.collidepoint(eventPos):
            return "6"
        elif self.seven.collidepoint(eventPos):
            return "7"
        elif self.eight.collidepoint(eventPos):
            return "8"
        elif self.nine.collidepoint(eventPos):
            return "9"
        elif self.zero.collidepoint(eventPos):
            return "0"
        elif self.period.collidepoint(eventPos):
            return "."
        elif self.deleteBtn.collidepoint(eventPos):
            return "d"
        elif self.backBtn.collidepoint(eventPos):
            return "b"
        elif self.submitBtn.collidepoint(eventPos):
            return "s"
        return "none"

    # Numpad
    def numpad_event(self, title):
        newValue = ""
        self.numpad_event_screen(title)
        color = pg.Color("yellow")
        while(1):
            if(1): #self.readingNow is False):
                try:
                    pg.display.update() 
                    myfont = pg.font.SysFont("monospace", int(round(self.convertHeight(15))))
                    value = myfont.render(newValue, 1, color)
                    self.canvas.blit(value, (self.convertWidth(5),self.convertHeight(215)))
            
                    pg.display.update()
                    pg.event.clear()
                    pg.event.wait()
                    if(1): #self.readingNow is False):
                        for event in pg.event.get():
                                if event.type is pg.MOUSEBUTTONDOWN:
                                    button = self.checkNumpad(event.pos)
                                    if button is "d":
                                        newValue = newValue[:-1]
                                        self.canvas.fill((0,0,0))
                                        self.numpad_event_screen(title)
                                    elif button is "s":
                                        return newValue
                                    elif button is "b":
                                        return
                                    elif button is not "none":
                                        newValue = newValue + button
                except:
                    pass
            else:
                self.numpad_event_screen(title)

    def quit(self):
        pg.quit()
