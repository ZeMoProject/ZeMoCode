#!/usr/bin/python3.4

import RPi.GPIO as GPIO
import serial # Required for communication with boards
import socket, struct, fcntl
import time

import os, sys, re
import requests

import csv
import json
import urllib.request
import urllib

from i2c import AtlasI2C

class Sensors(object):
    i2sensor = AtlasI2C()
    units = ""
    lowRange = "-1"
    highRange = "-1"
    i2cAddress = -1
    name = ""
    tag = ""
    currRead = "-1"
    probe = -1

    def __init__(self, jsonFile, piName):
        try:
            self.getRead()
            read2 = self.getRead()
            self.currRead = str(read2)        
            self.setFilename(piName)
            self.jsonFile = jsonFile
            self.lowRange = jsonFile["settings"][self.tag][0]
            self.highRange = jsonFile["settings"][self.tag][1]
            self.data = []
            self.daysToKeep = jsonFile["settings"]["days"]
            self.readsPerDay = jsonFile["settings"]["reads"]     
        except:
            self.currRead = "-1"
            self.lowRange = "-1"
            self.highRange = "-1"

    def getData(self):
        return self.data

    def setProbeNumber(self, probe):
        self.probe = probe

    def getCurrRead(self):
        return self.currRead

    def setFilename(self, piName):
        self.filename = "/home/pi/ZeMoCode/Data/" + piName + "_" + self.getTag() + "_data.csv"

    def setUnits(self, units):
        self.units = units

    def setName(self, name):
        self.name = name

    def seti2cAddress(self, addr):
        self.i2cAddress = addr

    def setTag(self, tag):
        self.tag = tag

    def getFilename(self):
        return self.filename

    def getName(self):
        return self.name

    def getTag(self):
        return self.tag

    def geti2cAddress(self):
        return self.i2cAddress

    def getLowRange(self):
        if self.lowRange is not "-1":
            return self.lowRange
        else:
            return self.jsonFile['settings'][self.getTag()][0]

    def getHighRange(self):
        if self.highRange is not "-1":
            return self.highRange
        else:
            return self.jsonFile['settings'][self.getTag()][1]

    # Only reads sensor data, doesn't write to file
    def getRead(self):
        try:
            if self.i2cAddress != -1:
                maxTries = 3
                line = ""
                for i in range (0, maxTries):
                    self.i2sensor.set_i2c_address(self.i2cAddress)
                    data = self.i2sensor.query('R')
                    if data != "":
                        read2 = float(data.split(",")[0])
                        retRead = round(read2, 1)
                        data = str(retRead)
                        return data
                return data
            else:
                return "-1"
        except:
            return "-1"

	# Take reads and write to file
    def takeRead(self, conn):
        try:
            if(self.i2cAddress != -1):
                    #TESTING
                    maxTries = 4
                    #maxTries = 10
                    reads = []
                    reads2 = []	 
                    avgRead = 0
                    #try:
                    for i in range(0, maxTries):
                        t = int(time.time())
                        try:
                            self.i2sensor.set_i2c_address(self.i2cAddress)
                            read = self.getRead()
                            read2 = float(read.split(",")[0])
                            if(read2 != -1 and read2 != 0):
                                reads.append(float(round(read2, 1)))
                                reads2.append(str(round(read2, 1)))
                        except Exception as y:
                            errorstring = ": Error: %s" % str(y)
                            #print(errorstring)
                            try:
                                self.i2sensor.set_i2c_address(self.i2cAddress)
                                read = self.getRead()
                                read2 = read.split(",")[0]
                                if(read2 != -1 and read2 != 0):
                                    reads.append(float(round(read2, 1)))
                                    reads2.append(str(round(read2, 1)))
                            except Exception as y:
                                errorstring = ": Error: %s" % str(y)
                                #print(errorstring)
                    if len(reads) > 2:
                        try:
                            #Does a trimmed reading
                            highestRead = max(reads)
                            lowestRead = min(reads)
                            reads.remove(max(reads))
                            reads.remove(min(reads))
                        except:
                            pass
                            #print("Failed to trim readings")
                    if(sum(reads) != 0 and len(reads) > 0):                    
                        avgRead = float(sum(reads))/len(reads)
                    else:
                        avgRead = 0
                    self.currRead = str(round(avgRead,1))    
                    outFile = open(self.filename, 'a')
                    file2 = self.filename[:-4]
                    outFileLog = open(file2 + "_log.csv", 'a')
                    if self.units != None:
                        reads.append(str(self.probe) + ": " + str(round(avgRead, 1)) + " " + self.units)
                    else:
                        reads.append(str(self.probe) + ": " + str(round(avgRead, 1)))
                    outFile.write(str(t * 1000) + "," + str(self.lowRange) + ";" + str(round(avgRead, 1)) + ";" + str(self.highRange))
                    outFile.write("\n")
                    outFile.close()
                    outFileLog.write(str(t * 1000) + "," + str(self.lowRange) + ";" + str(round(avgRead, 1)) + ";" + str(self.highRange))
                    outFileLog.write("\n")
                    outFileLog.close()
                    s = ""
                    with open(self.filename) as f:
                        s = f.read() + '\n'
                    values = {
                    'data' : {
                        self.tag : s
                        }
                    }
                    conn.sendReadings(values)
                    return_data = "\t".join(str(reads2))
                    self.limitLines()
                    self.data = return_data
                    #except Exception as e:
                    #t = int(time.time())
                    #errorstring = time.ctime(t) + ": Error: %s" % str(e)
                    #print(errorstring)        
                    return reads
        except:
            return reads

    def calibrateSensor(self, query):
        try:
            maxTries = 3
            for i in range (0, maxTries):
                self.i2sensor.set_i2c_address(self.i2cAddress)
                data = self.i2sensor.query(query)
                if data is "Success":
                    return data
                if (maxTries - 1) is i:
                    return data
        except:
            pass

    # Limits file size to 1 MB
    def limitFileSize(self):
        limitSize = 1
        csv.field_size_limit(limitSize)
    
    # Limits the number of lines recorded in the csv file
    def limitLines(self):
        try:
            f = open(self.filename)
            test = f.readlines()
            if int(self.readsPerDay) > 0 and int(self.daysToKeep) > 0:
                daysKept = int(self.daysToKeep)
                # if limiting to 6 months regardless of amount reads per day, add next two lines:
                #if daysKept > 183:
                #    daysKept = 183
                lines = (int(self.readsPerDay) * daysKept)
                # Limits file to the server size of 6 months worth of data
                if lines > 4400:
                    lines = 4400
                if len(test) > lines:
                    deleteLines = len(test) - lines
                    del test[:deleteLines]
                    testout = open(self.filename, "w")
                    testout.writelines(test)
                    testout.close()
            f.close()
        except:
            pass

    # Attempts to do a command 3 times before failing
    def tryThree(self, command):
        try:
            maxTries = 3
            for i in range(0, maxTries):
                if self.calibrateSensor(command) is "Success":
                    return True       
            return False
        except:
            return False

    # Removes data files
    def deleteHistory(self):
        try:
            os.remove(self.filename)
        except:
            pass