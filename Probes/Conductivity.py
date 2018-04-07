from Probes.Sensors import Sensors

class Conductivity(Sensors):
    def __init__(self, jsonFile, piName, screen):
        self.screen = screen
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

    def calibrate(self):
        pass

    def setProbeType(self, addr, query):
        maxTries = 3
        for i in range (0, maxTries):
            super().i2sensor.set_i2c_address(addr)
            data = super().i2sensor.query(query)  

    """
    # Conductivity Calibration - currently only has single point calibration, 2-pt cal exists and may be added in the future
    def cond_calibrate(self):
        try:
            myfont = pg.font.SysFont("monospace", 20)
            color = pg.Color("yellow")
            myfont.set_underline(True)
            titleScreen = myfont.render("Calibrate Conductivity", 1, color)
            myfont.set_underline(False)
            myfont = pg.font.SysFont("monospace", 18)
            calibText = myfont.render("Calibrate", 1, color)
            myfont = pg.font.SysFont("monospace", 15)
            step1 = myfont.render("1. Pour solution in cup", 1, color)
            step2 = myfont.render("2. Shake probe", 1, color)
            step3 = myfont.render("3. Sit probe in solution", 1, color)
            step4 = myfont.render("1. Starts with dry calibration", 1, color)
            step5 = myfont.render("4. Press Calibrate", 1, color)
            step6 = myfont.render("This will take some time...", 1, color)
            successfulCal = myfont.render("Calibration Successful", 1, color)
            failCal = myfont.render("Calibration Failed", 1, color)
            failRetry = myfont.render("Try Again", 1, color)
            pointCal = ""

            titlepos = titleScreen.get_rect()
            titlepos.centerx = self.background.get_rect().centerx + 20
            titlepos.centery = self.background.get_rect().top + 20
            calibTextpos = calibText.get_rect()
            calibTextpos.centerx = self.btmRight.centerx
            calibTextpos.centery = self.btmRight.centery
            step1pos = step1.get_rect()
            step1pos.centerx = self.topLeft.centerx + 60
            step1pos.centery = self.topLeft.centery - 30
            step4pos = step4.get_rect()
            step4pos.centerx = self.topLeft.centerx + 60
            step4pos.centery = self.topLeft.centery - 30
            step2pos = step2.get_rect()
            step2pos.centerx = self.topLeft.centerx + 60
            step2pos.centery = self.topLeft.centery - 10
            step3pos = step3.get_rect()
            step3pos.centerx = self.topLeft.centerx + 60
            step3pos.centery = self.topLeft.centery + 10
            step6pos = step6.get_rect()
            step6pos.centerx = self.background.get_rect().centerx
            step6pos.centery = self.background.get_rect().centery
            successfulCalpos = successfulCal.get_rect()
            successfulCalpos.centerx = self.background.get_rect().centerx
            successfulCalpos.centery = self.background.get_rect().centery
            failCalpos = failCal.get_rect()
            failCalpos.centerx = self.background.get_rect().centerx
            failCalpos.centery = self.background.get_rect().centery
            failurepos = failRetry.get_rect()
            failurepos.centerx = self.btmRight.centerx
            failurepos.centery = self.btmRight.centery

            condCal = ""
            stepNum = 0
            self.canvas.fill((0,0,0))
            if(self.readingNow == False):
                while(1):
                    pg.gfxdraw.rectangle(self.canvas, self.backBtn, color)
                    pg.draw.polygon(self.canvas, color, ((30,17),(30,25),(30,17),(10,17),(15,23),(10,17),(15,11),(10,17)), 1)
                    pg.gfxdraw.rectangle(self.canvas, self.btmRight, color)
                    self.canvas.blit(titleScreen, titlepos)
                    self.canvas.blit(calibText, calibTextpos)
                    pg.event.clear()
                    pg.display.update()     
                    pg.event.wait()
                    if(self.readingNow == False):
                        for event in pg.event.get():
                                if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                                    self.done = True
                                    return
                                elif event.type == pg.MOUSEBUTTONDOWN:
                                    if self.btmRight.collidepoint(event.pos):
                                        if self.conductivity.i2cAddress != -1:
                                            if stepNum == 0:
                                                        self.numpad_event("Cal Value","",1)
                                                        self.canvas.fill((0,0,0))
                                                        if self.tryThree('CAL,clear', self.conductivity):
                                                            stepNum = 1
                                                            condCal = str(self.calNum)
                                                            self.canvas.fill((0,0,0))
                                                            self.canvas.blit(step4, step4pos)
                                            elif stepNum == 1:
                                                if self.tryThree('CAL,dry', self.conductivity):
                                                    stepNum = 2
                                                    self.canvas.fill((0,0,0))
                                                    self.canvas.blit(successfulCal, successfulCalpos)
                                                    pg.display.update()
                                                    time.sleep(1)
                                                    self.canvas.fill((0,0,0))
                                                    self.canvas.blit(step2, step2pos)
                                                    self.canvas.blit(step3, step3pos)
                                                    self.canvas.blit(step1, step1pos)
                                                    pg.display.update()                 
                                            elif stepNum == 2:
                                                    self.canvas.fill((0,0,0))
                                                    self.canvas.blit(step6, step6pos)
                                                    pg.display.update()
                                                    highCal = int(self.calNum) * 1.4
                                                    lowCal = int(self.calNum) * .6
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
                                                            calRead = self.conductivity.getRead()
                                                            if tempRead < hCal and tempRead > lCal:
                                                                if((float(calRead) - tempRead) < 10):
                                                                    stepNum = 3 
                                                            tempRead = float(calRead)
                                                    self.canvas.fill((0,0,0))
                                            if stepNum == 3:
                                                if self.tryThree('CAL,' + condCal, self.conductivity):
                                                    stepNum = 4
                                                    self.canvas.fill((0,0,0))
                                                    self.canvas.blit(successfulCal, successfulCalpos)
                                                    pg.display.update()
                                                    time.sleep(1)
                                                    self.calNum = "-1111"
                                                    return
                                    elif self.backBtn.collidepoint(event.pos):
                                        self.calNum = "-1111"
                                        return
        except:
            self.canvas.fill((0,0,0))
            self.canvas.blit(failCal, failCalpos)
            pg.display.update()
            time.sleep(1)
            self.calNum = "-1111"
            return
    """          