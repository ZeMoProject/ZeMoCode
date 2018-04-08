from Probes.Sensors import Sensors
import pygame as pg
import pygame.gfxdraw
import time

class PH(Sensors):
    def __init__(self, jsonFile, piName, screen):
        self.screen = screen
        self.canvas = screen.canvas        
        self.setValues()
        super().__init__(jsonFile, piName)

    def setValues(self):
        super().setUnits("")
        super().setName("pH")
        super().seti2cAddress(99)
        super().setTag("ph")
        super().setProbeNumber(2)

    def refresh(self, jsonFile, piName):
        self.setValues()
        super().__init__(jsonFile, piName)

    #TODO change calibration to go straight into calibration, instead of clicking on calibrate and going into numpad
    def calibrate(self):
        try:
            color = pg.Color("yellow")
    
            midPt = ""
            lowPt = ""
            highPt = ""
            phPtCal = -1
            phStepNum = -1
            self.canvas.fill((0,0,0))
            if(1): #self.readingNow == False):
                while(1):
                    pg.gfxdraw.rectangle(self.canvas, self.screen.backBtn, color)
                    pg.draw.polygon(self.canvas, color, ((30,17),(30,25),(30,17),(10,17),(15,23),(10,17),(15,11),(10,17)), 1)
                    pg.gfxdraw.rectangle(self.canvas, self.screen.btmRight, color)
                    if phPtCal == -1:
                        pg.gfxdraw.rectangle(self.canvas, self.screen.btmLeft, color)
                        pg.gfxdraw.rectangle(self.canvas, self.screen.middleBtn, color)
                        myfont = pg.font.SysFont("monospace", 18)
                        self.screen.drawText("Single point", myfont, color, self.screen.middleBtn, 0, 0)
                        self.screen.drawText("Two point", myfont, color, self.screen.btmLeft, 0, 0)
                        self.screen.drawText("Three point", myfont, color, self.screen.btmRight, 0, 0)
                    else:
                        myfont = pg.font.SysFont("monospace", 18)
                        self.screen.drawText("Calibrate", myfont, color, self.screen.btmRight, 0, 0)
                    myfont = pg.font.SysFont("monospace", 20)
                    self.screen.drawTitle("Calibrate pH", myfont, color)
                    pg.event.clear()
                    pg.display.update()     
                    pg.event.wait()
                    if(1): #self.readingNow == False):
                        for event in pg.event.get():                
                                if event.type == pg.QUIT or self.screen.keys[pg.K_ESCAPE]:
                                    self.done = True
                                    return
                                elif event.type == pg.MOUSEBUTTONDOWN:
                                    # Determine the Pt Calibration
                                    if phPtCal == -1:
                                        if self.screen.btmRight.collidepoint(event.pos):
                                            phPtCal = 3
                                            self.canvas.fill((0,0,0))
                                        elif self.screen.btmLeft.collidepoint(event.pos):
                                            phPtCal = 2
                                            self.canvas.fill((0,0,0))
                                        elif self.screen.middleBtn.collidepoint(event.pos):
                                            phPtCal = 1
                                            self.canvas.fill((0,0,0))
                                    elif self.screen.btmRight.collidepoint(event.pos):
                                            if phStepNum == -1:
                                                    midPt = self.screen.numpad_event("Enter MidPt")
                                                    phStepNum = 1
                                                    self.canvas.fill((0,0,0))        
                                                    myfont = pg.font.SysFont("monospace", 18)                                                    
                                                    self.screen.drawText("Calibrate", myfont, color, self.screen.btmRight, 0, 0)
                                                    myfont = pg.font.SysFont("monospace", 15)
                                                    self.screen.drawText("1. Remove cap, rinse probe", myfont, color, self.screen.topLeft, 70, -30)
                                                    self.screen.drawText("2. Pour solution in cup", myfont, color, self.screen.topLeft, 70, -10)
                                                    self.screen.drawText("3. Sit probe in solution 1-2 min", myfont, color, self.screen.topLeft, 70, 10)
                                                    self.screen.drawText("4. Press the Calibrate button", myfont, color, self.screen.topLeft, 70, 30)
                                                    pg.display.update()
                                            elif phStepNum == 1:
                                                self.screen.drawMessage("Calibrating...")
                                                if super().tryThree('CAL,mid,' + str(midPt)):
                                                    if phPtCal == 1:
                                                        self.screen.drawMessage("Calibration Successful")
                                                        pg.display.update()
                                                        time.sleep(1)                                                                                                               
                                                        return                                                      
                                                    phStepNum = 2
                                                    self.screen.drawMessage("Cal. Step Successful")
                                                    pg.display.update()
                                                    time.sleep(1)
                                                    self.canvas.fill((0,0,0))        
                                            elif phStepNum == 2:
                                                    lowPt = self.screen.numpad_event("Enter LowPt")
                                                    phStepNum = 3
                                                    self.canvas.fill((0,0,0))
                                                    myfont = pg.font.SysFont("monospace", 18)                                                    
                                                    self.screen.drawText("Calibrate", myfont, color, self.screen.btmRight, 0, 0)
                                                    myfont = pg.font.SysFont("monospace", 15)
                                                    self.screen.drawText("1. Rinse off pH probe", myfont, color, self.screen.topLeft, 70, -30)
                                                    self.screen.drawText("2. Pour solution in cup", myfont, color, self.screen.topLeft, 70, -10)
                                                    self.screen.drawText("3. Sit probe in solution 1-2 min", myfont, color, self.screen.topLeft, 70, 10)
                                                    self.screen.drawText("4. Press the Calibrate button", myfont, color, self.screen.topLeft, 70, 30)
                                            elif phStepNum == 3:
                                                self.screen.drawMessage("Calibrating...")                                                    
                                                if super().tryThree('CAL,low,' + lowPt):
                                                    if phPtCal == 2: 
                                                        self.screen.drawMessage("Calibration Successful")
                                                        pg.display.update()
                                                        time.sleep(1)                                                                                                               
                                                        return                                                    self.screen.drawMessage("Cal. Step Successful")
                                                    pg.display.update()
                                                    time.sleep(1)
                                                    phStepNum = 4
                                                    self.canvas.fill((0,0,0))        
                                            elif phStepNum == 4:
                                                    highPt = self.screen.numpad_event("Enter HighPt")
                                                    phStepNum = 5
                                                    self.canvas.fill((0,0,0))
                                                    myfont = pg.font.SysFont("monospace", 18)                                                    
                                                    self.screen.drawText("Calibrate", myfont, color, self.screen.btmRight, 0, 0)
                                                    myfont = pg.font.SysFont("monospace", 15)
                                                    self.screen.drawText("2. Pour solution in cup", myfont, color, self.screen.topLeft, 70, -10)
                                                    self.screen.drawText("3. Sit probe in solution 1-2 min", myfont, color, self.screen.topLeft, 70, 10)
                                                    self.screen.drawText("1. Rinse off pH probe", myfont, color, self.screen.topLeft, 70, -30)
                                                    self.screen.drawText("4. Press the Calibrate button", myfont, color, self.screen.topLeft, 70, 30)
                                            elif phStepNum == 5:
                                                self.screen.drawMessage("Calibrating...")
                                                if super().tryThree('CAL,high,' + highPt):
                                                    self.screen.drawMessage("Calibration Successful")
                                                    pg.display.update()
                                                    time.sleep(1)
                                                    return
                                    elif self.screen.backBtn.collidepoint(event.pos):
                                        return
        except:
            self.screen.drawMessage("Calibration Failed")
            pg.display.update()
            time.sleep(1)
            return