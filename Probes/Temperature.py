from Probes.Sensors import Sensors

class Temperature(Sensors):
    def __init__(self, jsonFile, piName):
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
        pass
    """
    # Temperature Calibration
    def temp_calibrate(self):
        try:
            self.canvas.fill((0,0,0))
            pg.display.update()
            myfont = pg.font.SysFont("monospace", 20)
            color = pg.Color("yellow")
            myfont.set_underline(True)
            titleScreen = myfont.render("Calibrate Temperature", 1, color)
            myfont.set_underline(False)
            myfont = pg.font.SysFont("monospace", 18)
            calibText = myfont.render("Calibrate", 1, color)
            myfont = pg.font.SysFont("monospace", 15)
            step1 = myfont.render("1. Put probe in solution", 1, color)
            step2 = myfont.render("2. Enter solution temperature", 1, color)
            step3 = myfont.render("3. Press calibrate", 1, color)
            successfulCal = myfont.render("Calibration Successful", 1, color)
            failCal = myfont.render("Calibration Failed", 1, color)
            failRetry = myfont.render("Try Again", 1, color)

            titlepos = titleScreen.get_rect()
            titlepos.centerx = self.background.get_rect().centerx + 20
            titlepos.centery = self.background.get_rect().top + 20
            calibTextpos = calibText.get_rect()
            calibTextpos.centerx = self.btmRight.centerx
            calibTextpos.centery = self.btmRight.centery
            step1pos = step1.get_rect()
            step1pos.centerx = self.topLeft.centerx + 60
            step1pos.centery = self.topLeft.centery - 30
            step2pos = step2.get_rect()
            step2pos.centerx = self.topLeft.centerx + 60
            step2pos.centery = self.topLeft.centery - 10
            step3pos = step3.get_rect()
            step3pos.centerx = self.topLeft.centerx + 60
            step3pos.centery = self.topLeft.centery + 10
            successfulCalpos = successfulCal.get_rect()
            successfulCalpos.centerx = self.background.get_rect().centerx
            successfulCalpos.centery = self.background.get_rect().centery
            failCalpos = failCal.get_rect()
            failCalpos.centerx = self.background.get_rect().centerx
            failCalpos.centery = self.background.get_rect().centery
            if(self.readingNow == False):
                stepNum = 0
                while(1):
                    self.canvas.fill((0,0,0))
                    pg.gfxdraw.rectangle(self.canvas, self.backBtn, color)
                    pg.draw.polygon(self.canvas, color, ((30,17),(30,25),(30,17),(10,17),(15,23),(10,17),(15,11),(10,17)), 1)
                    pg.gfxdraw.rectangle(self.canvas, self.btmRight, color)
                    self.canvas.blit(titleScreen, titlepos)
                    self.canvas.blit(calibText, calibTextpos)
                    if self.calNum != "-1111":
                        self.canvas.blit(step1, step1pos)
                        self.canvas.blit(step2, step2pos)
                        self.canvas.blit(step3, step3pos)                                       
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
                                        if self.temperature.i2cAddress != -1:
                                            if stepNum == 0:
                                                if self.calNum == "-1111":
                                                    self.numpad_event("Cal Value","",1)
                                                    self.canvas.fill((0,0,0))
                                                    stepNum = 1
                                            elif stepNum == 1:
                                                if self.tryThree('CAL,clear', self.temperature):
                                                    if self.tryThree('CAL,' + str(self.calNum), self.temperature):
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