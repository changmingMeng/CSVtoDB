# coding: utf-8

import datetime
import csvManip
import re
import os


class Control(object):
    def __init__(self, dataRoot = "F:\\pythonTemp\\20161128"):
        self.dataRoot = dataRoot
        self.erl = 0
        self.upData = 0
        self.downData = 0

    def MainExecute(self):
        for root, dirs, files in os.walk(self.dataRoot):
            for name in files:
                #print name
                if re.search(r"1275071435", name) != None:
                   self.GSMErl(os.path.join(root, name))
                elif re.search(r"1275072525", name) != None or re.search(r"1275072527", name) != None:
                   self.GSMUpData(os.path.join(root, name))
                elif re.search(r"1275072526", name) != None or re.search(r"1275072528", name) != None:
                   self.GSMDownData(os.path.join(root, name))

    def newMainExecute(self):
        '''循环遍历文件名并处理'''
        switch = {
            1275071435: self.GSMErl,
            1275072525: self.GSMUpData,
            1275072527: self.GSMUpData,
            1275072526: self.GSMDownData,
            1275072528: self.GSMDownData,
        }
        for root, dirs, files in os.walk(self.dataRoot):
            for name in files:
                for key in switch:
                    if re.search(str(key), name) != None:
                        switch[key](os.path.join(root, name))


    def GSMErl(self, filePath):
        '''计算GSM通话话务量'''
        #print "GSMErl: " + filePath
        csv = csvManip.csvManipulate(filePath)
        self.erl += csv.newnewGetGSMErl()
        #self.erl += 1


    def GSMUpData(self, filePath):
        '''计算GSM上行流量'''
        #print "GSMUpData: " + filePath
        csv = csvManip.csvManipulate(filePath)
        self.upData += csv.GetGSMUpdata()
        #self.upData += 1

    def GSMDownData(self, filePath):
        '''计算GSM下行流量'''
        #print "GSMDownData: " + filePath
        csv = csvManip.csvManipulate(filePath)
        self.downData += csv.GetGSMDowndata()
        #self.downData += 1


    def printAll(self):
        print "Erl = " + str(self.erl)
        print "UpData = " + str(self.upData)
        print "DownData = " + str(self.downData)

if __name__ == "__main__":
    startTime = datetime.datetime.now()
    print "start time:", startTime
    ctrl = Control()
    #ctrl.MainExecute()
    ctrl.newMainExecute()
    ctrl.printAll()
    endTime = datetime.datetime.now()
    print "end time:", endTime
    print "run time:", (endTime - startTime)
    #print re.search(r"1275071435", "pmresult_1275069419_1440_201611270000_201611280000.csv") != None