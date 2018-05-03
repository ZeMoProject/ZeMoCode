from Probes.Sensors import Sensors
import pygame as pg
import pygame.gfxdraw
import time

class Conductivity(Sensors):
    def __init__(self, jsonFile, piName, screen):
        self.screen = screen
        self.canvas = screen.canvas 
        self.setValues()
        self.setProbeType(100, "K," + str(jsonFile["settings"]["cdProbeType"]))
        super().__init__(jsonFile, piName)       

    def setValues(self):
        super().setUnits("uS")
        super().setName("Conductivity")
        super().seti2cAddress(100)
        super().setTag("cd")
        super().setProbeNumber(1)

    def refresh(self, jsonFile, piName):
        self.setValues()
        super().__init__(jsonFile, piName)

    def setProbeType(self, addr, query):
        maxTries = 3
        for i in range (0, maxTries):
            super().i2sensor.set_i2c_address(addr)
            data = super().i2sensor.query(query)  

    # Conductivity Calibration - currently only has single point calibration, 2-pt cal exists and may be added in the future
    def calibrate(self):
        try:
            color = pg.Color("yellow")
            condCal = ""
            stepNum = 0
            self.canvas.fill((0,0,0))
            if(1): #self.readingNow == False):
                while(1):
                    self.screen.drawImage("back_btn.png", self.screen.backBtn, 35, 35)            
                    pg.gfxdraw.rectangle(self.canvas, self.screen.btmRight, color)
                    self.screen.drawTitle("Calibrate pH", 20, color) 
                    self.screen.drawText("Calibrate", 18, color, self.screen.btmRight, 0, 0)
                    pg.event.clear()
                    pg.display.update()     
                    pg.event.wait()
                    if(1): #self.readingNow == False):
                        for event in pg.event.get():
                                if event.type == pg.QUIT or self.screen.keys[pg.K_ESCAPE]:
                                    self.done = True
                                    return
                                elif event.type == pg.MOUSEBUTTONDOWN:
                                    if self.screen.btmRight.collidepoint(event.pos):
                                            if stepNum == 0:
                                                        condCal = self.screen.numpad_event("Cal Value")
                                                        self.canvas.fill((0,0,0))
                                                        if super().tryThree('CAL,clear'):
                                                            stepNum = 1
                                                            self.canvas.fill((0,0,0))
                                                            self.screen.drawText("1. Starts with dry calibration", 15, color, self.screen.topLeft, 60, -30)
                                            elif stepNum == 1:
                                                if super().tryThree('CAL,dry'):
                                                    stepNum = 2
                                                    self.screen.drawMessage("Cal. Step Successful")
                                                    pg.display.update()
                                                    time.sleep(1)
                                                    self.canvas.fill((0,0,0))
                                                    self.screen.drawText("1. Pour solution in cup", 15, color, self.screen.topLeft, 60, -30)
                                                    self.screen.drawText("2. Shake probe", 15, color, self.screen.topLeft, 60, -10)
                                                    self.screen.drawText("3. Sit probe in solution", 15, color, self.screen.topLeft, 60, 10)
                                                    pg.display.update()                 
                                            elif stepNum == 2:
                                                    self.canvas.fill((0,0,0))
                                                    self.screen.drawMessage("*This will take some time...")
                                                    pg.display.update()
                                                    highCal = int(condCal) * 1.4
                                                    lowCal = int(condCal) * .6
                                                    hCal = 0.0
                                                    lCal = 0.0
                                                    lCal = float(lowCal)
                                                    hCal = float(highCal)
                                                    tempRead = 0.0
                                                    # Takes reads until 2 consecutive
                                                    # reads within the 40% variance are
                                                    # less than 10 apart
                                                    for i in range(0,15):
                                                        if(stepNum != 3):
                                                            calRead = super().getRead()
                                                            if tempRead < hCal and tempRead > lCal:
                                                                if((float(calRead) - tempRead) < 10):
                                                                    stepNum = 3 
                                                            tempRead = float(calRead)
                                                    self.canvas.fill((0,0,0))
                                            if stepNum == 3:
                                                if super().tryThree('CAL,' + condCal):
                                                    stepNum = 4
                                                    self.canvas.fill((0,0,0))
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