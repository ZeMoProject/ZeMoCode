from Probes.Sensors import Sensors

class PH(Sensors):
    def __init__(self, jsonFile, piName, screen):
        self.screen = screen
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

    def calibrate(self):
        pass

    """
    # pH Calibration
    def pH_calibrate(self):
        try:
            myfont = pg.font.SysFont("monospace", 20)
            color = pg.Color("yellow")
            myfont.set_underline(True)
            titleScreen = myfont.render("Calibrate pH", 1, color)
            myfont.set_underline(False)
            myfont = pg.font.SysFont("monospace", 15)
            step1 = myfont.render("1. Remove cap, rinse probe", 1, color)
            step2 = myfont.render("2. Pour solution in cup", 1, color)
            step3 = myfont.render("3. Sit probe in solution 1-2 min", 1, color)
            step4 = myfont.render("1. Rinse off pH probe", 1, color)
            step5 = myfont.render("4. Press the Calibrate button", 1, color)
            myfont = pg.font.SysFont("monospace", 18)
            singlePt = myfont.render("Single point", 1, color)
            dualPt = myfont.render("Two point", 1, color)
            triPt = myfont.render("Three point", 1, color)
            successfulCal = myfont.render("Calibration Successful", 1, color)
            failCal = myfont.render("Calibration Failed", 1, color)
            failRetry = myfont.render("Try Again", 1, color)
            part1Cal = myfont.render("Calibrate", 1, color)
            pointCal = ""

            titlepos = titleScreen.get_rect()
            titlepos.centerx = self.background.get_rect().centerx
            titlepos.centery = self.background.get_rect().top + 20
            singlePtpos = singlePt.get_rect()
            singlePtpos.centerx = self.middleBtn.centerx
            singlePtpos.centery = self.middleBtn.centery
            dualPtpos = dualPt.get_rect()
            dualPtpos.centerx = self.btmLeft.centerx
            dualPtpos.centery = self.btmLeft.centery
            triPtpos = triPt.get_rect()
            triPtpos.centerx = self.btmRight.centerx
            triPtpos.centery = self.btmRight.centery
            step1pos = step1.get_rect()
            step1pos.centerx = self.topLeft.centerx + 70
            step1pos.centery = self.topLeft.centery - 30
            step2pos = step2.get_rect()
            step2pos.centerx = self.topLeft.centerx + 70
            step2pos.centery = self.topLeft.centery - 10
            step3pos = step3.get_rect()
            step3pos.centerx = self.topLeft.centerx + 70
            step3pos.centery = self.topLeft.centery + 10
            step4pos = step4.get_rect()
            step4pos.centerx = self.topLeft.centerx + 70
            step4pos.centery = self.topLeft.centery - 30
            step5pos = step5.get_rect()
            step5pos.centerx = self.topLeft.centerx + 70
            step5pos.centery = self.topLeft.centery + 30
            successfulCalpos = successfulCal.get_rect()
            successfulCalpos.centerx = self.background.get_rect().centerx
            successfulCalpos.centery = self.background.get_rect().centery
            failCalpos = failCal.get_rect()
            failCalpos.centerx = self.background.get_rect().centerx
            failCalpos.centery = self.background.get_rect().centery
            failurepos = failRetry.get_rect()
            failurepos.centerx = self.btmRight.centerx
            failurepos.centery = self.btmRight.centery
            part1pos = part1Cal.get_rect()
            part1pos.centerx = self.btmRight.centerx
            part1pos.centery = self.btmRight.centery

            midPt = ""
            lowPt = ""
            highPt = ""
            phPtCal = -1
            phStepNum = -1
            self.canvas.fill((0,0,0))
            if(self.readingNow == False):
                while(1):
                    pg.gfxdraw.rectangle(self.canvas, self.backBtn, color)
                    pg.draw.polygon(self.canvas, color, ((30,17),(30,25),(30,17),(10,17),(15,23),(10,17),(15,11),(10,17)), 1)
                    pg.gfxdraw.rectangle(self.canvas, self.btmRight, color)
                    if phPtCal == -1:
                        pg.gfxdraw.rectangle(self.canvas, self.btmLeft, color)
                        pg.gfxdraw.rectangle(self.canvas, self.middleBtn, color)
                        self.canvas.blit(singlePt, singlePtpos)
                        self.canvas.blit(dualPt, dualPtpos)
                        self.canvas.blit(triPt, triPtpos)
                    else:
                        self.canvas.blit(part1Cal, part1pos)
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
                                    # Determine the Pt Calibration
                                    if phPtCal == -1:
                                        if self.btmRight.collidepoint(event.pos):
                                            phPtCal = 3
                                            self.canvas.fill((0,0,0))
                                        elif self.btmLeft.collidepoint(event.pos):
                                            phPtCal = 2
                                            self.canvas.fill((0,0,0))
                                        elif self.middleBtn.collidepoint(event.pos):
                                            phPtCal = 1
                                            self.canvas.fill((0,0,0))
                                    elif self.btmRight.collidepoint(event.pos):
                                        if self.ph.i2cAddress != -1:
                                            if phStepNum == -1:
                                                    self.numpad_event("Enter MidPt","",1)
                                                    midPt = self.calNum
                                                    self.calNum = "-1111"
                                                    phStepNum = 1
                                                    self.canvas.fill((0,0,0))
                                                    self.canvas.blit(part1Cal, part1pos)
                                                    self.canvas.blit(step1, step1pos)
                                                    self.canvas.blit(step2, step2pos)
                                                    self.canvas.blit(step3, step3pos)
                                                    self.canvas.blit(step5, step5pos)
                                                    pg.display.update()
                                            elif phStepNum == 1:
                                                if self.tryThree('CAL,mid,' + str(midPt), self.ph):
                                                    phStepNum = 2
                                                    self.canvas.fill((0,0,0))
                                                    self.canvas.blit(successfulCal, successfulCalpos)
                                                    pg.display.update()
                                                    time.sleep(1)
                                                    if phPtCal == 1:
                                                        self.calNum = "-1111"
                                                        return
                                            elif phStepNum == 2:
                                                    self.numpad_event("Enter LowPt","",1)
                                                    lowPt = self.calNum
                                                    self.calNum = "-1111"
                                                    phStepNum = 3
                                                    self.canvas.fill((0,0,0))
                                                    self.canvas.blit(part1Cal, part1pos)
                                                    self.canvas.blit(step4, step4pos)
                                                    self.canvas.blit(step2, step2pos)
                                                    self.canvas.blit(step3, step3pos)
                                                    self.canvas.blit(step5, step5pos)
                                            elif phStepNum == 3:
                                                if self.tryThree('CAL,low,' + lowPt, self.ph):
                                                    self.canvas.fill((0,0,0))
                                                    self.canvas.blit(successfulCal, successfulCalpos)
                                                    pg.display.update()
                                                    time.sleep(1)
                                                    phStepNum = 4
                                                    if phPtCal == 2:
                                                        self.calNum = "-1111"
                                                        return
                                            elif phStepNum == 4:
                                                    self.numpad_event("Enter HighPt","",1)
                                                    highPt = self.calNum
                                                    self.calNum = "-1111"
                                                    phStepNum = 5
                                                    self.canvas.fill((0,0,0))
                                                    self.canvas.blit(part1Cal, part1pos)
                                                    self.canvas.blit(step4, step4pos)
                                                    self.canvas.blit(step2, step2pos)
                                                    self.canvas.blit(step3, step3pos)
                                                    self.canvas.blit(step5, step5pos)
                                            elif phStepNum == 5:
                                                if self.tryThree('CAL,high,' + highPt, self.ph):
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