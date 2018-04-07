from Probes.Sensors import Sensors
import pygame as pg
import pygame.gfxdraw
import time

class DissolvedOxygen(Sensors):
    def __init__(self, jsonFile, piName, screen):
        self.screen = screen
        self.canvas = screen.canvas
        self.setValues()
        super().__init__(jsonFile, piName)

    def setValues(self):
        super().setUnits("mg/L")
        super().setName("Dissolved Oxygen")
        super().seti2cAddress(97)
        super().setTag("do")
        super().setProbeNumber(3)

    def refresh(self, jsonFile, piName):
        self.setValues()
        super().__init__(jsonFile, piName)

    def calibrate(self):
        try:
            color = pg.Color("yellow")
            ptCals = -1
            stepNum = 0
            self.canvas.fill((0,0,0))
            #TODO change self.readingNow to true and block on the checktime thread
            #TODO add timeout thread for ten minutes of no activity, goes back to home screen and unblocks thr
            while(1):                
                if(1): #self.readingNow is False):
                    if stepNum is 0:
                        myfont = pg.font.SysFont("monospace", 20)                
                        self.screen.drawText("Single-pt", myfont, color, self.screen.btmLeft, 0, 0)
                        self.screen.drawText("Dual-pt", myfont, color, self.screen.btmRight, 0, 0)
                    pg.gfxdraw.rectangle(self.canvas, self.screen.backBtn, color)
                    pg.draw.polygon(self.canvas, color, ((30,17),(30,25),(30,17),(10,17),(15,23),(10,17),(15,11),(10,17)), 1)
                    pg.gfxdraw.rectangle(self.canvas, self.screen.btmRight, color)
                    if ptCals is -1:
                            pg.gfxdraw.rectangle(self.canvas, self.screen.btmLeft, color)
                    myfont = pg.font.SysFont("monospace", 20)
                    self.screen.drawTitle("Calibrate dOxygen", myfont, color)                                       
                    pg.event.clear()
                    pg.display.update()     
                    pg.event.wait()
                    myfont = pg.font.SysFont("monospace", 15)                                    
                    if(1): #self.readingNow is False):
                        for event in pg.event.get():
                            if event.type is pg.QUIT or self.screen.keys[pg.K_ESCAPE]:
                                self.done = True
                                return
                            elif event.type is pg.MOUSEBUTTONDOWN:
                                # Dual Point Calibration
                                if self.screen.btmRight.collidepoint(event.pos):
                                    self.screen.drawMessage("Calibrating...")                                                                            
                                    if stepNum is 0:
                                        if super().tryThree('CAL,clear'):
                                            ptCals = 1
                                            stepNum = 1
                                            self.canvas.fill((0,0,0))
                                            myfont = pg.font.SysFont("monospace", 15)                
                                            self.screen.drawText("Calibrate", myfont, color, self.screen.btmRight, 0, 0)
                                            self.screen.drawText("1. Remove cap", myfont, color, self.screen.topLeft, 60, -30)
                                            self.screen.drawText("2. Let probe sit 30 seconds", myfont, color, self.screen.topLeft, 60, -10)
                                            self.screen.drawText("3. Press calibrate", myfont, color, self.screen.topLeft, 60, 10)
                                    elif stepNum is 1:
                                        if super().tryThree('CAL'):
                                            stepNum = 2
                                            self.screen.drawMessage("Cal. Step Successful")
                                            pg.display.update()
                                            time.sleep(1)
                                            self.canvas.fill((0,0,0))
                                            myfont = pg.font.SysFont("monospace", 15)                
                                            self.screen.drawText("Calibrate", myfont, color, self.screen.btmRight, 0, 0)
                                            self.screen.drawText("1. Stir probe in solution", myfont, color, self.screen.topLeft, 60, -30)
                                            self.screen.drawText("2. Sit probe in solution 90 sec", myfont, color, self.screen.topLeft, 60, -10)
                                            self.screen.drawText("3. Press calibrate", myfont, color, self.screen.topLeft, 60, 10)
                                    elif stepNum is 2:
                                        if super().tryThree('CAL,0'):
                                            self.screen.drawMessage("Calibration Successful")
                                            pg.display.update()
                                            time.sleep(1)
                                            return
                                # Single Point Calibration
                                elif self.screen.btmLeft.collidepoint(event.pos):
                                    self.screen.drawMessage("Calibrating...")                                                                            
                                    if stepNum is 0:
                                        if super().tryThree('CAL,clear'):
                                            ptCals = 1
                                            stepNum = 2
                                            self.canvas.fill((0,0,0))
                                            self.screen.drawText("Calibrate", myfont, color, self.screen.btmRight, 0, 0)
                                            self.screen.drawText("1. Remove cap", myfont, color, self.screen.topLeft, 60, -30)
                                            self.screen.drawText("2. Let probe sit 30 seconds", myfont, color, self.screen.topLeft, 60, -10)
                                            self.screen.drawText("3. Press calibrate", myfont, color, self.screen.topLeft, 60, 10)
                                            pg.display.update()
                                elif self.screen.backBtn.collidepoint(event.pos):
                                    return
        except:
            self.screen.drawMessage("Calibration Failed")
            pg.display.update()
            time.sleep(1)
            return