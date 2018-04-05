from Probes.Sensors import Sensors

class DissolvedOxygen(Sensors):
    def __init__(self, jsonFile, piName):
        self.setValues()
        super().__init__(jsonFile, piName)

    def setValues(self):
        super().setUnits("mg/L")
        super().setName("D. Oxygen")
        super().seti2cAddress(97)
        super().setTag("do")
        super().setProbeNumber(3)

    def refresh(self, jsonFile, piName):
        self.setValues()
        super().__init__(jsonFile, piName)

    def calibrate(self):
        pass
    """
    # Dissolved Oxygen Calibration
    def dOxygen_calibrate(self):
            try:
                myfont = pg.font.SysFont("monospace", 20)
                color = pg.Color("yellow")
                myfont.set_underline(True)
                titleScreen = myfont.render("Calibrate dOxygen", 1, color)
                myfont.set_underline(False)
                myfont = pg.font.SysFont("monospace", 18)
                calibText = myfont.render("Calibrate", 1, color)
                myfont = pg.font.SysFont("monospace", 15)
                step1 = myfont.render("1. Remove cap", 1, color)
                step2 = myfont.render("2. Let probe sit 30 seconds", 1, color)
                step3 = myfont.render("3. Press calibrate", 1, color)
                step4 = myfont.render("1. Stir probe in solution", 1, color)
                step5 = myfont.render("2. Sit probe in solution 90 sec", 1, color)
                step6 = myfont.render("3. Press calibrate", 1, color)
                singlePt = myfont.render("Single-pt", 1, color)
                dualPt = myfont.render("Dual-pt", 1, color)
                successfulCal = myfont.render("Calibration Successful", 1, color)
                failCal = myfont.render("Calibration Failed", 1, color)
                failRetry = myfont.render("Try Again", 1, color)
                part1Cal = myfont.render("Calibrate", 1, color)
                pointCal = ""

                titlepos = titleScreen.get_rect()
                titlepos.centerx = self.background.get_rect().centerx
                titlepos.centery = self.background.get_rect().top + 20
                singlePtpos = singlePt.get_rect()
                singlePtpos.centerx = self.btmLeft.centerx
                singlePtpos.centery = self.btmLeft.centery
                dualPtpos = dualPt.get_rect()
                dualPtpos.centerx = self.btmRight.centerx
                dualPtpos.centery = self.btmRight.centery
                step1pos = step1.get_rect()
                step1pos.centerx = self.topLeft.centerx + 60
                step1pos.centery = self.topLeft.centery - 30
                step2pos = step2.get_rect()
                step2pos.centerx = self.topLeft.centerx + 60
                step2pos.centery = self.topLeft.centery - 10
                step3pos = step3.get_rect()
                step3pos.centerx = self.topLeft.centerx + 60
                step3pos.centery = self.topLeft.centery + 10
                step4pos = step4.get_rect()
                step4pos.centerx = self.topLeft.centerx + 60
                step4pos.centery = self.topLeft.centery - 30
                step5pos = step5.get_rect()
                step5pos.centerx = self.topLeft.centerx + 60
                step5pos.centery = self.topLeft.centery - 10
                step6pos = step6.get_rect()
                step6pos.centerx = self.topLeft.centerx + 60
                step6pos.centery = self.topLeft.centery + 10
                successfulCalpos = successfulCal.get_rect()
                successfulCalpos.centerx = self.background.get_rect().centerx
                successfulCalpos.centery = self.background.get_rect().centery
                failurepos = failRetry.get_rect()
                failurepos.centerx = self.btmRight.centerx
                failurepos.centery = self.btmRight.centery
                failCalpos = failCal.get_rect()
                failCalpos.centerx = self.background.get_rect().centerx
                failCalpos.centery = self.background.get_rect().centery
                part1pos = part1Cal.get_rect()
                part1pos.centerx = self.btmRight.centerx
                part1pos.centery = self.btmRight.centery

                ptCals = -1
                stepNum = 0
                self.canvas.fill((0,0,0))
                while(1):                
                    if(self.readingNow == False):
                        if self.calNum != "1":
                                self.canvas.blit(singlePt, singlePtpos)
                                self.canvas.blit(dualPt, dualPtpos)
                        pg.gfxdraw.rectangle(self.canvas, self.backBtn, color)
                        pg.draw.polygon(self.canvas, color, ((30,17),(30,25),(30,17),(10,17),(15,23),(10,17),(15,11),(10,17)), 1)
                        pg.gfxdraw.rectangle(self.canvas, self.btmRight, color)
                        if ptCals == -1:
                                pg.gfxdraw.rectangle(self.canvas, self.btmLeft, color)
                        self.canvas.blit(titleScreen, titlepos)
                                       
                        pg.event.clear()
                        pg.display.update()     
                        pg.event.wait()
                        if(self.readingNow == False):
                            for event in pg.event.get():
                                        if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                                            self.done = True
                                            return
                                        elif event.type == pg.MOUSEBUTTONDOWN:
                                            # Dual Point Calibration
                                            if self.btmRight.collidepoint(event.pos):
                                                if self.dOxygen.i2cAddress != -1:
                                                    if stepNum == 0:
                                                        if self.tryThree('CAL,clear', self.dOxygen):
                                                            ptCals = 1
                                                            stepNum = 1
                                                            self.calNum = "1"
                                                            self.canvas.fill((0,0,0))
                                                            self.canvas.blit(part1Cal, part1pos)
                                                            self.canvas.blit(step1, step1pos)
                                                            self.canvas.blit(step2, step2pos)
                                                            self.canvas.blit(step3, step3pos)
                                                    elif stepNum == 1:
                                                        if self.tryThree('CAL', self.dOxygen):
                                                            stepNum = 2
                                                            self.canvas.fill((0,0,0))
                                                            self.canvas.blit(successfulCal, successfulCalpos)
                                                            pg.display.update()
                                                            time.sleep(1)
                                                            self.canvas.fill((0,0,0))
                                                            self.canvas.blit(part1Cal, part1pos)
                                                            self.canvas.blit(step4, step4pos)
                                                            self.canvas.blit(step5, step5pos)
                                                            self.canvas.blit(step6, step6pos)
                                                    elif stepNum == 2:
                                                        if self.tryThree('CAL,0', self.dOxygen):
                                                                self.canvas.fill((0,0,0))
                                                                self.canvas.blit(successfulCal, successfulCalpos)
                                                                pg.display.update()
                                                                time.sleep(1)
                                                                self.calNum = "-1111"
                                                                return
                                            # Single Point Calibration
                                            elif self.btmLeft.collidepoint(event.pos):
                                                    if stepNum == 0:
                                                        if self.tryThree('CAL,clear', self.dOxygen):
                                                            ptCals = 1
                                                            stepNum = 2
                                                            self.calNum = "1"
                                                            self.canvas.fill((0,0,0))
                                                            self.canvas.blit(part1Cal, part1pos)
                                                            self.canvas.blit(step1, step1pos)
                                                            self.canvas.blit(step2, step2pos)
                                                            self.canvas.blit(step3, step3pos)
                                                            pg.display.update()
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