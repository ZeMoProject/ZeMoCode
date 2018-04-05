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
        #TESTING
        #pg.display.toggle_fullscreen()
        self.canvas = pg.display.get_surface()
        self.background = pygame.Surface(self.canvas.get_size())
        self.keys = pg.key.get_pressed()
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
    def settings_event_screen(self, eth0, wlan0, readsPerDay, daysToKeep):
            self.canvas.fill((0,0,0))
            color = pg.Color("yellow")

            myfont = pg.font.SysFont("monospace", 18)            
            self.drawText(str(wlan0), myfont, color, self.topLeft, 0, 30)
            self.drawText(str(eth0), myfont, color, self.topLeft, 0, 0)

            myfont = pg.font.SysFont("monospace", 20)
            self.drawText("ip Address:", myfont, color, self.topLeft, 0, -30)
            self.drawText("Refresh", myfont, color, self.topRight, 0, -10)
            self.drawText("Sensors", myfont, color, self.topRight, 0, 10)
            self.drawText("Days Kept:", myfont, color, self.btmLeft, 0, -10)
            self.drawText("Reads/Day:", myfont, color, self.btmRight, 0, -10)
            self.drawText(str(readsPerDay), myfont, color, self.btmRight, 0, 10)
            self.drawText(str(daysToKeep), myfont, color, self.btmLeft, 0, 10)           

            pg.gfxdraw.rectangle(self.canvas, self.settingsBtn, color)
            pg.draw.circle(self.canvas, color, (297,22), 17, 10)
            self.drawTitle("Settings", myfont, color)            

            tLeft = pg.gfxdraw.rectangle(self.canvas, self.topLeft, color)
            bLeft = pg.gfxdraw.rectangle(self.canvas, self.btmLeft, color)
            tRight = pg.gfxdraw.rectangle(self.canvas, self.topRight, color)
            bRight = pg.gfxdraw.rectangle(self.canvas, self.btmRight, color)
            pg.gfxdraw.rectangle(self.canvas, self.backBtn, color)
            pg.draw.polygon(self.canvas, color, ((30,17),(30,25),(30,17),(10,17),(15,23),(10,17),(15,11),(10,17)), 1)
            pg.display.update()

    # Screen shows "Taking Reads..."
    def taking_reads_loop(self):
        color = pg.Color("steelblue1")
        myfont = pg.font.SysFont("monospace", 15)
        #add while loop starting here, for when threading occurs
        self.drawText("Taking Reads   ", myfont, color, self.background.get_rect(), 0, 0)                   
        self.drawText("Taking Reads   ", myfont, color, self.background.get_rect(), 0, 0)                   
        self.drawText("Taking Reads   ", myfont, color, self.background.get_rect(), 0, 0)                   
        pg.display.update()
        time.sleep(2)
        self.drawText("Taking Reads.  ", myfont, color, self.background.get_rect(), 0, 0)                   
        pg.display.update()
        time.sleep(2)                  
        self.drawText("Taking Reads.. ", myfont, color, self.background.get_rect(), 0, 0)                   
        pg.display.update()
        time.sleep(2)
        self.drawText("Taking Reads...", myfont, color, self.background.get_rect(), 0, 0)                   
        pg.display.update()
        time.sleep(2)
        self.canvas.fill((0,0,0))

    # Advanced Settings screen
    def advanced_settings_event_screen(self):
            self.canvas.fill((0,0,0))

            myfont = pg.font.SysFont("monospace", 20)
            color = pg.Color("plum1")
            self.drawText("EXIT", myfont, color, self.btmRight, 0, 0)
            self.drawText("Email Data", myfont, color, self.middleBtn, 0, 0)
            self.drawText("Re-Register", myfont, color, self.btmLeft, 0, 0)

            pg.gfxdraw.rectangle(self.canvas, self.btmLeft, color)
            pg.gfxdraw.rectangle(self.canvas, self.btmRight, color)
            pg.gfxdraw.rectangle(self.canvas, self.middleBtn, color)

            self.drawTitle("Advanced Settings", myfont, color)            

            pg.gfxdraw.rectangle(self.canvas, self.backBtn, color)
            pg.draw.polygon(self.canvas, color, ((30,17),(30,25),(30,17),(10,17),(15,23),(10,17),(15,11),(10,17)), 1)       
            pg.display.update()

    # Update range values screen
    def update_event_screen(self, sensor):
            self.canvas.fill((0,0,0))
            myfont = pg.font.SysFont("monospace", 20)
            color = pg.Color("orange")
            self.drawTitle(str(sensor.getName()) + " Range", myfont, color)                        
            pg.draw.polygon(self.canvas, color, ((30,17),(30,25),(30,17),(10,17),(15,23),(10,17),(15,11),(10,17)), 1)

            #TODO move getLowRange and High range into sensor class
            self.drawText(str(sensor.getCurrRead()), myfont, color, self.middleBtnSmall, 0, 0)
            self.drawText("Low", myfont, color, self.btmLeftSmall, 0, -10)
            self.drawText("High", myfont, color, self.btmRightSmall, 0, -10)
            self.drawText(str(sensor.getLowRange()), myfont, color, self.btmLeftSmall, 0, +10)
            self.drawText(str(sensor.getHighRange()), myfont, color, self.btmRightSmall, 0, +10)
            self.drawText("Calibrate", myfont, color, self.topLeft, 0, 0)
            self.drawText("Refresh", myfont, color, self.topRight, 0, 0)

            pg.gfxdraw.rectangle(self.canvas, self.backBtn, color)
            pg.gfxdraw.rectangle(self.canvas, self.topLeft, color)
            pg.gfxdraw.rectangle(self.canvas, self.btmLeftSmall, color)
            pg.gfxdraw.rectangle(self.canvas, self.btmRightSmall, color)
            pg.gfxdraw.rectangle(self.canvas, self.middleBtnSmall, color)
            pg.gfxdraw.rectangle(self.canvas, self.topRight, color)

            pg.display.update()     

    # Numpad screen
    def numpad_event_screen(self):
            self.canvas.fill((0,0,0))
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
            title = myfont.render("Enter Calibration", 1, color)
            newRangeText = myfont.render("Cal. Value:", 1, color)
 
            myfont = pg.font.SysFont("monospace", 15)
            self.drawText("Submit", myfont, color, self.submitBtn, 0, 0)
            pg.draw.polygon(self.canvas, color, ((305,21),(265,21),(275,27),(265,21),(275,14),(265,21)), 2)

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

            self.canvas.blit(newRangeText, (5,195))
            self.canvas.blit(title, (50,10))
            pg.display.update()

    def main_menu_screen(self, condRead, dORead, phRead, tempRead):
            self.canvas.fill((0,0,0))
            myfont = pg.font.SysFont("monospace", 20)
            color = pg.Color("green")
            self.drawTitle("Current Reads", myfont, color)
            self.drawText("pH:", myfont, color, self.btmLeft, 0, -10)
            self.drawText("Cond:", myfont, color, self.topLeft, 0, -10)
            self.drawText("DO:", myfont, color, self.topRight, 0, -10)
            self.drawText("Temp:", myfont, color, self.btmRight, 0, -10)
            self.drawText(str(condRead), myfont, color, self.topLeft, 0, 10)
            self.drawText(str(phRead), myfont, color, self.btmLeft, 0, 10)
            self.drawText(str(dORead), myfont, color, self.topRight, 0, 10)
            self.drawText(str(tempRead), myfont, color, self.btmRight, 0, 10)            
                       
            pg.gfxdraw.rectangle(self.canvas, self.topLeft, color)
            pg.gfxdraw.rectangle(self.canvas, self.btmLeft, color)
            pg.gfxdraw.rectangle(self.canvas, self.topRight, color)
            pg.gfxdraw.rectangle(self.canvas, self.btmRight, color)
            pg.gfxdraw.rectangle(self.canvas, self.settingsBtn, color)
            pg.draw.circle(self.canvas, color, (297,22), 17, 10)
            pg.display.update()

    def register_screen(self):
        self.canvas.fill((0,0,0))        
        color = pg.Color("steelblue1")
        myfont = pg.font.SysFont("monospace", 15)
        self.drawTitle("Register Your Pi", myfont, color)
        self.drawText("You must click \"Accept\" on the", myfont, color, self.centerBtn, 0, -95) 
        self.drawText("\"Manage Your Connections\" screen", myfont, color, self.centerBtn, 0, -80)
        self.drawText("before clicking on \"Register\"", myfont, color, self.centerBtn, 0, -65)         
        self.drawText("Register", myfont, color, self.centerBtn, 0, 0)
        pg.gfxdraw.rectangle(self.canvas, self.centerBtn, color)   
        pg.display.update()
        while(1):
            pg.event.clear()
            pg.event.wait()
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN: 
                    if self.centerBtn.collidepoint(event.pos):
                        return
    
    def reregister(self):
        self.canvas.fill((0,0,0))        
        color = pg.Color("steelblue1")
        myfont = pg.font.SysFont("monospace", 15)
        self.drawTitle("Re-Register Your Pi", myfont, color)
        self.drawText("Are you sure?", myfont, color, self.centerBtn, 0, -95)         
        myfont = pg.font.SysFont("monospace", 24)        
        self.drawText("Yes", myfont, color, self.midLeft, 0, 0)
        self.drawText("No", myfont, color, self.midRight, 0, 0)        
        pg.gfxdraw.rectangle(self.canvas, self.midRight, color) 
        pg.gfxdraw.rectangle(self.canvas, self.midLeft, color)             
        pg.display.update()
        while(1):
            pg.event.clear()
            pg.event.wait()
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN: 
                    if self.midLeft.collidepoint(event.pos):
                        return True
                    elif self.midRight.collidepoint(event.pos):
                        return False

    # Draws normal text
    def drawText(self, text, myfont, color, location, xOffset, yOffset):
        textPrint = myfont.render(text, 1, color)        
        textpos = textPrint.get_rect()
        textpos.centerx = location.centerx + xOffset
        textpos.centery = location.centery + yOffset
        self.canvas.blit(textPrint, textpos)

    # Draws the titles
    def drawTitle(self, titleScreen, myfont, color):
        myfont.set_underline(True)
        textPrint = myfont.render(titleScreen, 1, color)                
        textpos = textPrint.get_rect()
        textpos.centerx = self.background.get_rect().centerx
        textpos.centery = self.background.get_rect().top + 20
        self.canvas.blit(textPrint, textpos)
        myfont.set_underline(False)       

    def drawMessage(self, text):
        self.canvas.fill((0,0,0))        
        color = pg.Color("steelblue1")
        myfont = pg.font.SysFont("monospace", 20)         
        textPrint = myfont.render(text, 1, color)        
        textpos = textPrint.get_rect()
        textpos.centerx = self.background.get_rect().centerx
        textpos.centery = self.background.get_rect().centery
        self.canvas.blit(textPrint, textpos)
        pg.display.update()                
    
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
        else:
            return 0
    
    def checkCollisionSmallBtns(self, eventPos):
        if self.btmLeftSmall.collidepoint(eventPos):
            return 1
        elif self.middleBtnSmall.collidepoint(eventPos):
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

    def quit(self):
        pg.quit()
