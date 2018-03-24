#!/usr/bin/python3.4
import os, sys, re
import pygame as pg
import pygame.gfxdraw

# Configures parameters
CAPTION = "Current Reads"
SCREEN_SIZE = (320, 240)
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240

class Screen(object):
    def __init__(self):
        pg.display.set_caption(CAPTION)
        pg.display.set_mode(SCREEN_SIZE)
        pg.display.toggle_fullscreen()
        self.viewScreen = pg.display.get_surface()
        self.background = pygame.Surface(self.viewScreen.get_size())
        # The program will exit once this is set to 'True'
        self.keys = pg.key.get_pressed()
        self.color = pg.Color("black")
        # Hides Mouse, still allows click events
        pg.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        self.topLeft = pg.Rect(5,45,152.5,92.5)
        self.btmLeftSmall = pg.Rect(5,142.5,100,92.5)
        self.middleBtnSmall = pg.Rect(110,142.5,100,92.5)
        self.btmRightSmall = pg.Rect(215,142.5,100,92.5)
        self.btmLeft = pg.Rect(5,142.5,152.5,92.5)
        self.topRight = pg.Rect(162.5,45,152.5,92.5)

        self.midLeft = pg.Rect(5,92.5,152.5,92.5)
        self.midRight = pg.Rect(162.5,92.5,152.5,92.5)
        self.centerBtn = pg.Rect(83.75,92.5,152.5,92.5)

        self.btmRight = pg.Rect(162.5,142.5,152.5,92.5)
        self.backBtn = pg.Rect(5,5,35,35)
        self.middleBtn = pg.Rect(83.75,45,152.5,92.5)
        self.settingsBtn = pg.Rect(280,5,35,35)

        self.one = pg.Rect(5,45,58,70)
        self.two = pg.Rect(68,45,58,70)
        self.three = pg.Rect(131,45,58,70)
        self.four = pg.Rect(194,45,58,70)
        self.five = pg.Rect(257,45,58,70)
        self.six = pg.Rect(5,120,58,70)
        self.seven = pg.Rect(68,120,58,70)
        self.eight = pg.Rect(131,120,58,70)
        self.nine = pg.Rect(194,120,58,70)
        self.zero = pg.Rect(257,120,58,70)
        self.period = pg.Rect(257,195,58,35)
        self.submitBtn = pg.Rect(194,195,58,35)
        self.deleteBtn = pg.Rect(257,5,58,35)

    # Settings screen
    def settings_event_screen(self):
            self.viewScreen.fill((0,0,0))

            myfont = pg.font.SysFont("monospace", 20)
            color = pg.Color("yellow")
            self.drawText("ip Address:", myfont, color, self.topLeft, 0, -30)
            self.drawText("Refresh", myfont, color, self.topRight, 0, -10)
            self.drawText("Sensors", myfont, color, self.topRight, 0, +10)
            self.drawText("Days Kept:", myfont, color, self.btmLeft, 0, -10)
            self.drawText("Reads/Day:", myfont, color, self.btmRight, 0, -10)
            
            #ipEth0 = myfont.render(str(self.eth0), 1, color)
            #ipwlan0 = myfont.render(str(self.wlan0), 1, color)
            pg.gfxdraw.rectangle(self.viewScreen, self.settingsBtn, color)
            pg.draw.circle(self.viewScreen, color, (297,22), 17, 10)
            myfont.set_underline(True)
            self.drawTitle("Settings", myfont, color)            
            myfont.set_underline(False)            
            try:
                daysKept = myfont.render(str(self.daysToKeep), 1, color)
            except Exception as e:
                self.drawText("Unknown", myfont, color, self.btmLeft, 0, +10)
            try:
                readsPerDay = myfont.render(str(self.readsPerDay), 1, color)
            except Exception as e:
                readsPerDay = myfont.render("Unknown", 1, color)
            tLeft = pg.gfxdraw.rectangle(self.viewScreen, self.topLeft, color)
            bLeft = pg.gfxdraw.rectangle(self.viewScreen, self.btmLeft, color)
            tRight = pg.gfxdraw.rectangle(self.viewScreen, self.topRight, color)
            bRight = pg.gfxdraw.rectangle(self.viewScreen, self.btmRight, color)
            pg.gfxdraw.rectangle(self.viewScreen, self.backBtn, color)
            pg.draw.polygon(self.viewScreen, color, ((30,17),(30,25),(30,17),(10,17),(15,23),(10,17),(15,11),(10,17)), 1)

            """textpos = ipEth0.get_rect()
            textpos.centerx = self.topLeft.centerx 
            textpos.centery = self.topLeft.centery
            self.viewScreen.blit(ipEth0, textpos)
            textpos = ipwlan0.get_rect()
            textpos.centerx = self.topLeft.centerx 
            textpos.centery = self.topLeft.centery + 30
            self.viewScreen.blit(ipwlan0, textpos)
            textpos = readsPerDay.get_rect()
            textpos.centerx = self.btmRight.centerx
            textpos.centery = self.btmRight.centery + 10
            self.viewScreen.blit(readsPerDay, textpos)"""

    # Advanced Settings screen
    def advanced_settings_event_screen(self):
            self.viewScreen.fill((0,0,0))

            myfont = pg.font.SysFont("monospace", 20)
            color = pg.Color("plum1")
            self.drawText("EXIT", myfont, color, self.btmRight, 0, 0)
            self.drawText("Email Data", myfont, color, self.middleBtn, 0, 0)
            self.drawText("Re-Register", myfont, color, self.btmLeft, 0, 0)

            pg.gfxdraw.rectangle(self.viewScreen, self.btmLeft, color)
            pg.gfxdraw.rectangle(self.viewScreen, self.btmRight, color)
            pg.gfxdraw.rectangle(self.viewScreen, self.middleBtn, color)

            myfont.set_underline(True)
            self.drawTitle("Advanced Settings", myfont, color)            
            myfont.set_underline(False)

            pg.gfxdraw.rectangle(self.viewScreen, self.backBtn, color)
            pg.draw.polygon(self.viewScreen, color, ((30,17),(30,25),(30,17),(10,17),(15,23),(10,17),(15,11),(10,17)), 1)       

    # Numpad screen
    def numpad_event_screen(self, lowUp, ulrange, cal):
            self.viewScreen.fill((0,0,0))
            self.calNum = -1111
            myfont = pg.font.SysFont("monospace", 60)
            color = pg.Color("yellow")
            self.drawText("1", myfont, color, self.one, 0, 0)
            self.drawText("2", myfont, color, self.two, 0, 0)
            self.drawText("3", myfont, color, self.three, 0, 0)
            self.drawText("4", myfont, color, self.four, 0, 0)
            self.drawText("5", myfont, color, self.five, 0, 0)
            self.drawText("6", myfont, color, self.six, 0, 0)
            self.drawText("7", myfont, color, self.seven, 0, 0)
            self.drawText("8", myfont, color, self.eight, 0, 0)
            self.drawText("9", myfont, color, self.nine, 0, 0)
            self.drawText("0", myfont, color, self.zero, 0, 0)
            self.drawText(".", myfont, color, self.period, 0, -10)

            myfont = pg.font.SysFont("monospace", 20)
            myfont.set_underline(True)

            if cal is 0:
                title = myfont.render("Enter New Range", 1, color)
                newRangeText = myfont.render("New " + lowUp + " Range:", 1, color)
                pg.gfxdraw.rectangle(self.viewScreen, self.backBtn, color)
                pg.draw.polygon(self.viewScreen, color, ((30,17),(30,25),(30,17),(10,17),(15,23),(10,17),(15,11),(10,17)), 1)
            elif cal is 1:
                title = myfont.render("Enter Calibration", 1, color)
                newRangeText = myfont.render(lowUp + ":", 1, color)
            elif cal is 2:
                title = myfont.render("Enter Code", 1, color)
                newRangeText = myfont.render(lowUp + ":", 1, color)
                pg.gfxdraw.rectangle(self.viewScreen, self.backBtn, color)
                pg.draw.polygon(self.viewScreen, color, ((30,17),(30,25),(30,17),(10,17),(15,23),(10,17),(15,11),(10,17)), 1)
            elif cal is 3:
                title = myfont.render("Enter Reads/Day", 1, color)
                newRangeText = myfont.render("Reads/Day:", 1, color)
                pg.gfxdraw.rectangle(self.viewScreen, self.backBtn, color)
                pg.draw.polygon(self.viewScreen, color, ((30,17),(30,25),(30,17),(10,17),(15,23),(10,17),(15,11),(10,17)), 1)
            elif cal is 4:
                title = myfont.render("Enter Days Kept", 1, color)
                newRangeText = myfont.render("Days Kept:", 1, color)
                pg.gfxdraw.rectangle(self.viewScreen, self.backBtn, color)
                pg.draw.polygon(self.viewScreen, color, ((30,17),(30,25),(30,17),(10,17),(15,23),(10,17),(15,11),(10,17)), 1)

            myfont = pg.font.SysFont("monospace", 15)
            self.drawText("Submit", myfont, color, self.submitBtn, 0, 0)
            pg.draw.polygon(self.viewScreen, color, ((305,21),(265,21),(275,27),(265,21),(275,14),(265,21)), 2)

            pg.gfxdraw.rectangle(self.viewScreen, self.one, color)
            pg.gfxdraw.rectangle(self.viewScreen, self.two, color)
            pg.gfxdraw.rectangle(self.viewScreen, self.three, color)
            pg.gfxdraw.rectangle(self.viewScreen, self.four, color)
            pg.gfxdraw.rectangle(self.viewScreen, self.five, color)
            pg.gfxdraw.rectangle(self.viewScreen, self.six, color)
            pg.gfxdraw.rectangle(self.viewScreen, self.seven, color)
            pg.gfxdraw.rectangle(self.viewScreen, self.eight, color)
            pg.gfxdraw.rectangle(self.viewScreen, self.nine, color)
            pg.gfxdraw.rectangle(self.viewScreen, self.period, color)
            pg.gfxdraw.rectangle(self.viewScreen, self.zero, color)
            pg.gfxdraw.rectangle(self.viewScreen, self.submitBtn, color)
            pg.gfxdraw.rectangle(self.viewScreen, self.deleteBtn, color)

            self.viewScreen.blit(submit, textpos)
            self.viewScreen.blit(newRangeText, (5,195))
            self.viewScreen.blit(title, (50,10))

    def main_menu_screen(self):
            self.viewScreen.fill((0,0,0))
            myfont = pg.font.SysFont("monospace", 20)
            color = pg.Color("green")
            myfont.set_underline(True)
            self.drawTitle("Current Reads", myfont, color)
            myfont.set_underline(False)
            self.drawText("pH:", myfont, color, self.btmLeft, 0, -10)
            self.drawText("Cond:", myfont, color, self.topLeft, 0, -10)
            self.drawText("DO:", myfont, color, self.topRight, 0, -10)
            self.drawText("Temp:", myfont, color, self.btmRight, 0, -10)
                       
            pg.gfxdraw.rectangle(self.viewScreen, self.topLeft, color)
            pg.gfxdraw.rectangle(self.viewScreen, self.btmLeft, color)
            pg.gfxdraw.rectangle(self.viewScreen, self.topRight, color)
            pg.gfxdraw.rectangle(self.viewScreen, self.btmRight, color)
            pg.gfxdraw.rectangle(self.viewScreen, self.settingsBtn, color)
            pg.draw.circle(self.viewScreen, color, (297,22), 17, 10)

    # Draws normal text
    def drawText(self, text, myfont, color, location, xOffset, yOffset):
        textPrint = myfont.render(text, 1, color)        
        textpos = textPrint.get_rect()
        textpos.centerx = location.centerx + xOffset
        textpos.centery = location.centery + yOffset
        self.viewScreen.blit(textPrint, textpos)

    # Draws the titles
    def drawTitle(self, titleScreen, myfont, color):
        textPrint = myfont.render(titleScreen, 1, color)                
        textpos = textPrint.get_rect()
        textpos.centerx = self.background.get_rect().centerx
        textpos.centery = self.background.get_rect().top + 20
        self.viewScreen.blit(textPrint, textpos)        

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
        elif self.middleBtn.collidepoint(eventPos):
            return 6
        elif self.settingsBtn.collidepoint(eventPos):
            return 7
        elif self.centerBtn.collidepoint(eventPos):
            return 8
        elif self.midLeft.collidepoint(eventPos):
            return 9
        elif self.midRight.collidepoint(eventPos):
            return 10
        elif self.btmLeftSmall.collidepoint(eventPos):
            return 11
        elif self.middleBtnSmall.collidepoint(eventPos):
            return 12
        elif self.btmRightSmall.collidepoint(eventPos):
            return 13  
        else:
            return 0

    def checkNumpad(self, eventPos):
        return "not implemented"

    def quit(self):
        pg.quit()
