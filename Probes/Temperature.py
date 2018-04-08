from Probes.Sensors import Sensors
import pygame as pg
import pygame.gfxdraw
import time

class Temperature(Sensors):
    def __init__(self, jsonFile, piName, screen):
        self.screen = screen
        self.canvas = screen.canvas
        self.setValues()
        super().__init__(jsonFile, piName)

    def setValues(self):
        super().setUnits("C")
        super().setName("Temperature")
        super().seti2cAddress(102)
        super().setTag("tp")
        super().setProbeNumber(0)

    def refresh(self, jsonFile, piName):
        self.setValues()
        super().__init__(jsonFile, piName)

    def calibrate(self):
        try:
            color = pg.Color("yellow")

            calNum = "-1111"
            if(1): #self.readingNow is False):
                stepNum = 0
                while(1):
                    self.canvas.fill((0,0,0))
                    pg.gfxdraw.rectangle(self.canvas, self.screen.backBtn, color)
                    pg.draw.polygon(self.canvas, color, ((30,17),(30,25),(30,17),(10,17),(15,23),(10,17),(15,11),(10,17)), 1)
                    pg.gfxdraw.rectangle(self.canvas, self.screen.btmRight, color)
                    myfont = pg.font.SysFont("monospace", 20)
                    self.screen.drawTitle("Calibrate Temperature", myfont, color)
                    self.screen.drawText("Calibrate", myfont, color, self.screen.btmRight, 0, 0)
                    if stepNum is 0:
                        myfont = pg.font.SysFont("monospace", 15)
                        self.screen.drawText("1. Put probe in solution", myfont, color, self.screen.topLeft, 60, -30)
                        self.screen.drawText("2. Enter solution temperature", myfont, color, self.screen.topLeft, 60, -10)
                        self.screen.drawText("3. Press calibrate", myfont, color, self.screen.topLeft, 60, 10)                                       
                    pg.event.clear()
                    pg.display.update()     
                    pg.event.wait()
                    if(1): #self.readingNow is False):
                        for event in pg.event.get():
                                if event.type is pg.QUIT or self.screen.keys[pg.K_ESCAPE]:
                                    self.done = True
                                    return
                                elif event.type is pg.MOUSEBUTTONDOWN:
                                    if self.screen.btmRight.collidepoint(event.pos):
                                            self.screen.drawMessage("Calibrating...")                                        
                                            if stepNum is 0:
                                                calNum = self.screen.numpad_event("Enter Calibration")
                                                self.canvas.fill((0,0,0))
                                                if calNum != "-1111" or calNum != "":                                                    
                                                    stepNum = 1
                                            elif stepNum is 1:
                                                if super().tryThree('CAL,clear'):
                                                    if super().tryThree('CAL,' + str(calNum)):
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
