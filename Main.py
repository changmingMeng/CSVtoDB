# coding: utf-8

import datetime
import csvManip
import re
import os
import DataDict

class MainControl(object):
    def __init__(self, dataRoot = "F:\\pythonTemp\\20161128"):
        self.dataRoot = dataRoot
        self.erl = 0
        self.upData = 0
        self.downData = 0
        self.erl3G = 0
        self.upData3G = 0
        self.downData3G = 0
        self.switch = {
            1275071435: self.GSMErl,
            1275072525: self.GSMUpData,
            1275072527: self.GSMUpData,
            1275072526: self.GSMDownData,
            1275072528: self.GSMDownData,

            67109378: self.WCDMAErl,
            67109508: self.WCDMADataDoWith67109508,
            67109471: self.WCDMAUpdata,#这个文件只包含VS.HSUPA.MeanChThroughput.TotalBytes这项，可以使用公用的逻辑
            #67109508: self.WCDMADowndata,
            67109390: self.WCDMADowndata#这个文件只包含VS.HSDPA.MeanChThroughput.TotalBytes这项，可以使用公用的逻辑
        }



    def oldMainExecute(self):
        '''循环遍历文件名并处理'''
        for root, dirs, files in os.walk(self.dataRoot):
            for name in files:
                for key in self.switch:
                    if re.search(str(key), name) != None:
                        self.switch[key](os.path.join(root, name))
        dict = DataDict.DataDict()
        dict.SaveToDB()

    def MainExecute(self):
        self.ClassifyFiles()
        fileName2G = [1275071435, 1275072525, 1275072527, 1275072526, 1275072528]
        fileName3G = [67109378, 67109508, 67109471, 67109390]
        self.Execute(fileName2G)
        self.Execute(fileName3G)

    def Execute(self, fileName):
        for fileKeyNum in fileName:
            for name in self.fileDict[fileKeyNum]:
                for key in self.switch:
                    if re.search(str(key), name) != None:
                        self.switch[key](os.path.join(self.dataRoot, name))
        dict = DataDict.DataDict()
        #dict.ConnectToDB()
        dict.SaveToDB()
        dict.ClearDict()

    def ClassifyFiles(self):
        self.fileDict = {key:[] for key in self.switch.keys()}
        for root, dirs, files in os.walk(self.dataRoot):
            for name in files:
                for key in self.fileDict.keys():
                    if re.search(str(key), name) != None:
                        self.fileDict[key].append(name)
        # for key in self.fileDict.keys():
        #     print key, self.fileDict[key]

    def GSMErl(self, filePath):
        '''计算GSM通话话务量'''
        #print "GSMErl: " + filePath
        csv = csvManip.csvManipulate(filePath)
        self.erl += csv.GetGSMErl()
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

    def WCDMAErl(self, filePath):
        '''计算3G-WCDMA话务量'''
        csv = csvManip.csvManipulate(filePath)
        self.erl3G += csv.GetWCDMAErl()

    def WCDMAUpdata(self, filePath):
        '''计算3G-WCDMA上行流量'''
        csv = csvManip.csvManipulate(filePath)
        self.upData3G += csv.GetWCDMAUpdata()

    def WCDMADowndata(self, filePath):
        '''计算3G-WCDMA上行流量'''
        csv = csvManip.csvManipulate(filePath)
        self.downData3G += csv.GetWCDMADowndata()

    def WCDMADataDoWith67109508(self, filePath):
        '''处理文件名中含有67109508的特殊函数，该文件中同时包含上下行的流量信息'''
        csv = csvManip.csvManipulate(filePath)
        self.upData3G += csv.GetWCDMAUpdata()
        self.downData3G += csv.GetWCDMADowndata()

    def printAll(self):
        print "Erl = " + str(self.erl)
        print "UpData = " + str(self.upData)
        print "DownData = " + str(self.downData)

        print "Erl3G = " + str(self.erl3G)
        print "UpData3G = " + str(self.upData3G)
        print "DownData3G = " + str(self.downData3G)

if __name__ == "__main__":
    startTime = datetime.datetime.now()
    print "start time:", startTime
    ctrl = MainControl()
    #ctrl.MainExecute()
    ctrl.oldMainExecute()
    ctrl.printAll()
    endTime = datetime.datetime.now()
    print "end time:", endTime
    print "run time:", (endTime - startTime)
    #print re.search(r"1275071435", "pmresult_1275069419_1440_201611270000_201611280000.csv") != None


    #print {key:[] for key in switch.keys()}