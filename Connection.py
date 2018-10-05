#!/usr/bin/python3.4
import socket
import struct
import fcntl
import time
import os
import sys
import re
import logging
import requests
from subprocess import check_output
import json
import urllib
import urllib.request
from Screen import Screen

class Connection(object):
    def __init__(self):
        logging.basicConfig(filename="/home/pi/ZeMoCode/Data/ZeMo.log", level=logging.INFO)
        self.screen = Screen()
        self.eth0 = self.get_ip("eth0", 3)
        self.wlan0 = self.get_ip("wlan0", 3)
        registered = False
        try:
            with open("/home/pi/ZeMoCode/account") as f:
                acnt = f.read()
                self.account = acnt.strip('\n')
                self.logInfo("ACCOUNT " + self.account)                
        except:
            # Occurs if the account file did not create properly from SetupZeMo.sh file
            self.account = "NULL_ACCOUNT_NAME"
        if(self.account is "NULL_ACCOUNT_NAME"):
            self.screen.drawMessage("No Account Found, Please Retry")
            self.logInfo("No account found")
            time.sleep(30)
        self.piName = socket.gethostname()
        try:
            # Tries to load an existing account
            self.accountJSON = json.load(open('/home/pi/ZeMoCode/account.json'))
            self.secret = self.accountJSON["secret"]  
            try:    
                self.jsonConfig = self.getConfigData()
            except:
                self.logInfo("Did not grab config file")      
        except:
            # Registers if no existing account is found
            self.secret = "none"
            # Loops until registration is completed
            while registered is False:
                registered = self.register()
        self.screen.drawImage("logo.png", self.screen.background.get_rect(), 223, 57)            

    # Resets account info
    def resetAccount(self):
        try:
            os.remove("/home/pi/ZeMoCode/account.json")
        except Exception as e:
            self.logError(e)        
        self.account = ""
        self.secret = ""
        self.piName = ""

    def getaccountJSON(self):
        return self.accountJSON

    def getJSONconfig(self):
        return self.jsonConfig

    def getAccount(self):
        return self.account

    def getPiName(self):
        return self.piName

    def getSecret(self):
        return self.secret

    def getEth0(self):
        return self.eth0

    def getWlan0(self):
        return self.wlan0

    # Emails ip address
    def sendIP(self):
        message = "zfish1 is up and running at (wired, wireless): " + self.getWlan0()
        self.sendEmail(message)

    # Emails the sensors that are not working
    def warning(self, sensors):
        message = "These sensors are not working: " + " ".join(sensors.getName())
        self.sendEmail(message)
    
    # Emails Log Data from pi
    def sendLogData(self, files):
        try:
            s1 = ""
            s3 = ""
            s4 = ""
            s2 = ""
            with open(files[0]) as f:
                s1 = f.read() + '\n'
            with open(files[1]) as f:
                s2 = f.read() + '\n'
            with open(files[2]) as f:
                s3 = f.read() + '\n'
            with open(files[3]) as f:
                s4 = f.read() + '\n'                        

            values = {
                "body" : "Log Data",
                "attachments" : [
                    { 
                        "filename" : files[0],
                        "content" : s1 
                    },
                    { 
                        "filename" : files[1],
                        "content" : s2 
                    },
                    { 
                        "filename" : files[2],
                        "content" : s3 
                    },
                    { 
                        "filename" : files[3],
                        "content" : s4 
                    }
                ]       
            }
            url = 'https://zemoproject.org/notifications/' + self.account + '/' + self.piName
            params = json.dumps(values)

            bearer = 'Bearer ' + self.secret 
            headers={'content-type': 'application/json', 'Authorization': bearer}            
            req = requests.post(url=url, json=values,headers=headers)
            self.screen.drawMessage("Log Data Sent!")
            time.sleep(2)
        except Exception as e:
            self.logError(e)
            self.screen.drawMessage("Did not send email")
            time.sleep(2)

    # Returns the user settings from the website
    def getConfigData(self):
        try:
            url = 'https://zemoproject.org/settings/' + self.account + '/' + self.piName
            bearer = 'Bearer ' + self.secret 
            headers={'content-type': 'application/json', 'Authorization': bearer}            
            req = requests.get(url=url, headers=headers)
            return req.json() 
        except Exception as e:
            self.logInfo("In getConfigData")
            self.logInfo("account: " + str(self.account))
            self.logInfo("piName: " + str(self.piName))
            self.logInfo("ip: " + str(self.getWlan0()))            
            self.logError(e)

    # Sends the hourly readings
    def sendReadings(self, values):
        try:
            params = json.dumps(values).encode('utf8')
            emailEndPoint = "https://zemoproject.org/data/" + self.account + "/" + self.piName
            bearer = 'Bearer ' + self.secret 
            req = urllib.request.Request(emailEndPoint, data=params,
                        headers={'content-type': 'application/json', 'Authorization': bearer})
            response = urllib.request.urlopen(req)   
        except Exception as e:
            self.logError(e)  

    def sendEmail(self, message):
        try:
            values = {
                    'body' : message
                    }

            params = json.dumps(values).encode('utf8')
            emailEndPoint = 'https://zemoproject.org/notifications/' + self.account + '/' + self.piName
            bearer = 'Bearer ' + self.secret 
            req = urllib.request.Request(emailEndPoint, data=params,
                        headers={'content-type': 'application/json', 'Authorization': bearer})
            response = urllib.request.urlopen(req)
        except Exception as e:
            self.logError(e)

    # Sends an email of the probes out of range with the associated data
    def sendOutofRange(self, sensors):
        try:
            compiledMsg = "These sensors are out of range:"
            message = ""
            for probe in sensors:
                message = message + "\n" + probe.getName() + ": " + probe.getData()
            compiledMsg = compiledMsg + message + " \nThe data here includes the trimmed readings."
            values = {
                    'body' : compiledMsg
                    }

            params = json.dumps(values).encode('utf8')
            emailEndPoint = 'https://zemoproject.org/notifications/' + self.account + '/' + self.piName
            bearer = 'Bearer ' + self.secret 
            req = urllib.request.Request(emailEndPoint, data=params,
                        headers={'content-type': 'application/json', 'Authorization': bearer})
            response = urllib.request.urlopen(req)   
        except Exception as e:
            self.logError(e)     

    # Sends registration info, pi should appear on website afterwards
    def sendRegister(self):
        try:
            values = {
                    "account" : self.account,
                    "name" : self.piName,
                    "ip_address" : self.getWlan0()
                    }

            url = 'https://zemoproject.org/register'
            params = json.dumps(values)
            headers={'content-type': 'application/json'}            
            req = requests.post(url=url, json=values,headers=headers)
            sec = req.json() 
            self.secret = sec["secret"]
            return True
        except:
            self.logInfo(str(values))
            self.logInfo("rec: " + str(req))
            return False   

    # Draws the registration screen and responds to user input
    def screenRegisterResend(self):
        resend = self.screen.register_screen()
        if resend is False:
            self.screen.drawMessage("Attempting to Register")
        elif resend is True:
            self.sendRegister()
            self.screen.drawMessage("New Request Sent")
        time.sleep(2)        

    # Waits for user to push accept on the website
    def waitForAccept(self):
        try:    
            self.jsonConfig = self.getConfigData()
            if self.jsonConfig is None:
                self.screenRegisterResend()
                return False           
            return True            
        except:
            self.screenRegisterResend()
            return False             

    # Registers pi
    def register(self):
        try:
            self.sendRegister()
            accepted = False
            while accepted is False:
                accepted = self.waitForAccept()            
            cfg = {
                "secret" : self.secret,
                "account" : self.account,
                "piName" : self.piName
            }
            with open("/home/pi/ZeMoCode/account.json", "w") as g:
                json.dump(cfg, g)
            self.accountJSON = json.load(open('/home/pi/ZeMoCode/account.json'))
            self.screen.canvas.fill((0,0,0))
            self.screen.drawImage("logo.png", self.screen.background.get_rect(), 223, 57)                
            return True               
        except Exception as e:
            self.logInfo("In Register Function")
            self.logInfo("account: " + str(self.account))
            self.logInfo("piName: " + str(self.piName))
            self.logInfo("ip: " + str(self.getWlan0()))
            self.logError(e)     
            self.screen.drawMessage("Failed to grab Settings")
            time.sleep(2)     
            self.screen.drawMessage("Make sure to \"Accept\"")
            time.sleep(2)
            return False

    # Returns IP address of pi
    def get_ip(self, network, countdown):
        try:
            countdown = countdown - 1
            if(countdown is not 0):
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                return socket.inet_ntoa(fcntl.ioctl(
                    s.fileno(),
                    0x8915,
                    struct.pack('256s', bytes(network[:15], 'utf-8'))
                )[20:24])
        except:
            self.get_ip(network, countdown)

    # Logging errors
    def logError(self, info):
        try:
            logging.exception(str(info))
        except:
            pass

    # Logging Info
    def logInfo(self, info):
        try:
            logging.info(str(info))
        except:
            pass
