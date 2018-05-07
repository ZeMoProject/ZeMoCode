#!/usr/bin/python3.4
import socket
import struct
import fcntl
import time
import os
import sys
import re
import requests
from subprocess import check_output
import json
import urllib
import urllib.request
from Screen import Screen

class Connection(object):
    def __init__(self):
        self.screen = Screen()
        self.eth0 = self.get_ip("eth0")
        self.wlan0 = self.get_ip("wlan0")
        try:
            with open("/home/pi/ZeMoCode/ACCOUNT") as f:
                self.account = f.read()
        except:
            self.account = "NULL"
        self.piName = socket.gethostname()
        try:
            self.accountJSON = json.load(open('/home/pi/ZeMoCode/account.json'))
            self.secret = self.accountJSON["secret"]        
        except:
            self.register()
        self.jsonConfig = self.getConfigData()

    def resetAccount(self):
        try:
            os.remove("/home/pi/ZeMoCode/account.json")
        except:
            pass
        try:
            os.remove("/home/pi/ZeMoCode/ACCOUNT")
        except:
            pass
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
        message = "zfish1 is up and running at (wired, wireless): " + self.get_ip("wlan0")
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
            self.screen.drawMessage("Did not send email")
            time.sleep(2)

    def getConfigData(self):
        try:
            url = 'https://zemoproject.org/settings/' + self.account + '/' + self.piName
            bearer = 'Bearer ' + self.secret 
            headers={'content-type': 'application/json', 'Authorization': bearer}            
            req = requests.get(url=url, headers=headers)
            return req.json()
              
        except:
            self.screen.drawMessage("Failed to grab Settings")
            time.sleep(2)     

    def sendReadings(self, values):
        try:
            params = json.dumps(values).encode('utf8')
            emailEndPoint = "https://zemoproject.org/data/" + self.account + "/" + self.piName
            bearer = 'Bearer ' + self.secret 
            req = urllib.request.Request(emailEndPoint, data=params,
                        headers={'content-type': 'application/json', 'Authorization': bearer})
            response = urllib.request.urlopen(req)   
        except:
            pass   

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
        except:
            pass

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
        except:
            pass     

    def register(self):
        try:
            f = open("/home/pi/ZeMoCode/log.txt", "a")
            f.write("\nTesting:")
            values = {
                    "account" : self.account,
                    "name" : self.piName,
                    "ip_address" : self.get_ip("wlan0")
                    }
            f.write("ip")
            f.write(self.get_ip("wlan0"))
            f.write("\naccount:")
            f.write(self.account)
            f.write("\npiName:")
            f.write(self.piName)

            url = 'https://zemoproject.org/register'
            params = json.dumps(values)
            headers={'content-type': 'application/json'}            
            req = requests.post(url=url, json=values,headers=headers)
            f.write("\nposted reqs")
            f.write("\nattempt print screen")

            self.screen.register_screen()
            f.write("\nprinted screen")

            sec = req.json()   
            f.write("\nsecret:")
            #f.write(sec)
            self.secret = sec["secret"]
            
            cfg = { 
                "secret" : self.secret,
                "account" : self.account,
                "piName" : self.piName
            }
            f.write("\nopen file cfg")
            f.close()
            with open("/home/pi/ZeMoCode/account.json", "w") as g:
                json.dump(cfg, g)
            f = open("/home/pi/ZeMoCode/log.txt", "a")                
            f.write("\nclose cfg")
                            
            self.accountJSON = json.load(open('/home/pi/ZeMoCode/account.json'))
            f.write("\nend write")
            
            f.close()
        except:
            f.close()
            self.screen.drawMessage("Unable to Register") 
            time.sleep(2)
            self.register()

    # Returns IP address of pi
    def get_ip(self, network):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,
                struct.pack('256s', bytes(network[:15], 'utf-8'))
            )[20:24])
        except:
            pass
