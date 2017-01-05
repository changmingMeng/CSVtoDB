# coding: utf-8

import datetime
import csv
import re
import control
import DataDict

class csvManipulate(object):
    def __init__(self,
                 #filePath = 'E:/pythonTemp/20161128/',
                 fileName = r'F:\pythonTemp\test3G\pmresult_67109471_30_201611282200_201611282230.csv'):
        #print "csvManipulate init from default data"
        #self.filePath = filePath
        self.fileName = fileName
        # self.csvFile = file(self.filePath + self.fileName, 'rb')
        self.dataNameDict = {
            "GSMErl": ["K3014:TCH话务量"],
            "GSMUpData": ["TL9023:上行GPRS RLC层吞吐量", "TL9237:上行EGPRS RLC层吞吐量"],
            "GSMDownData": ["TL9123:下行GPRS RLC层吞吐量", "TL9338:下行EGPRS RLC层吞吐量"],

            "WCDMAErl": ["VS.RB.AMR.DL.12.2", "VS.RB.AMR.DL.10.2", "VS.RB.AMR.DL.7.95",
                         "VS.RB.AMR.DL.7.4", "VS.RB.AMR.DL.6.7", "VS.RB.AMR.DL.5.9",
                         "VS.RB.AMR.DL.5.15", "VS.RB.AMR.DL.4.75", "VS.RB.CS.Conv.DL.64"],
            "WCDMAUpData": ["VS.PS.Bkg.UL.8.Traffic", "VS.PS.Bkg.UL.16.Traffic","VS.PS.Bkg.UL.32.Traffic",
                            "VS.PS.Bkg.UL.64.Traffic", "VS.PS.Bkg.UL.128.Traffic", "VS.PS.Bkg.UL.144.Traffic",
                            "VS.PS.Bkg.UL.256.Traffic", "VS.PS.Bkg.UL.384.Traffic", "VS.PS.Int.UL.8.Traffic",
                            "VS.PS.Int.UL.16.Traffic", "VS.PS.Int.UL.32.Traffic", "VS.PS.Int.UL.64.Traffic",
                            "VS.PS.Int.UL.128.Traffic", "VS.PS.Int.UL.144.Traffic", "VS.PS.Int.UL.256.Traffic",
                            "VS.PS.Int.UL.384.Traffic", "VS.PS.Str.UL.8.Traffic", "VS.PS.Str.UL.16.Traffic",
                            "VS.PS.Str.UL.32.Traffic", "VS.PS.Str.UL.64.Traffic", "VS.PS.Str.UL.128.Traffic",
                            "VS.PS.Conv.UL.Traffic", "VS.HSUPA.MeanChThroughput.TotalBytes",],
            "WCDMADownData": ["VS.PS.Bkg.DL.8.Traffic", "VS.PS.Bkg.DL.16.Traffic", "VS.PS.Bkg.DL.32.Traffic",
                              "VS.PS.Bkg.DL.64.Traffic", "VS.PS.Bkg.DL.128.Traffic", "VS.PS.Bkg.DL.144.Traffic",
                              "VS.PS.Bkg.DL.256.Traffic", "VS.PS.Bkg.DL.384.Traffic", "VS.PS.Int.DL.8.Traffic",
                              "VS.PS.Int.DL.16.Traffic", "VS.PS.Int.DL.32.Traffic", "VS.PS.Int.DL.64.Traffic",
                              "VS.PS.Int.DL.128.Traffic", "VS.PS.Int.DL.144.Traffic", "VS.PS.Int.DL.256.Traffic",
                              "VS.PS.Int.DL.384.Traffic", "VS.PS.Str.DL.8.Traffic", "VS.PS.Str.DL.16.Traffic",
                              "VS.PS.Str.DL.32.Traffic", "VS.PS.Str.DL.64.Traffi", "VS.PS.Str.DL.128.Traffic",
                              "VS.PS.Str.DL.144.Traffic", "VS.PS.Str.DL.256.Traffic", "VS.PS.Str.DL.384.Traffic",
                              "VS.PS.Conv.DL.Traffic", "VS.HSDPA.MeanChThroughput.TotalBytes"]
        }
        #self.ctrl = control.Controler()
        self.dict = DataDict.DataDict()
        self.SP = 1

    def __del__(self):
        print self.fileName, " executing complete!"

    def readCSV(self):
        csvFile = file(self.fileName, 'rb')
        self.csvReader = csv.reader(csvFile)
        return self.csvReader
        # self.csvFile = file(self.filePath + self.fileName, 'rb')
        # self.reader = csv.reader(self.csvFile)

    def GetColNumFromName(self, dataNames):
        '''根据列中含的字符串，找到列的序号'''
        colNumbers = []
        self.readCSV()
        colNames = self.csvReader.next()
        #print colNames
        for colName in colNames:
            for dataName in dataNames:
                #print dataName, "?=", colName.decode("gbk").encode("utf-8")
                if re.search(dataName, colName.decode("gbk").encode("utf-8")):
                    colNumbers.append(colNames.index(colName))
        return colNumbers

    def CalculateNumsInColoum(self, workType):
        '''计算选中列的每行的值之和'''
        totalData = 0
        colNums = self.GetColNumFromName(self.dataNameDict[workType])
        #ctrl = control.Controler()
        #print colNums
        #print self.fileName
        self.readCSV()
        self.csvReader.next()
        self.csvReader.next() #csv文件的第一行是表项名，第二行是单位，第三行开始是数据
        #i = 3
        for row in self.csvReader:
            rowSum = 0
            for col in colNums:
                # 当需要计算的列是csv文件的最后一列时，若该列中的一个值是空，
                # 则会使得提取出的row长度小于col的值，从而导致列表下标越界。
                if len(row) > col:
                    rowSum += float(row[col])
                    if colNums.index(col) == (len(colNums) - 1):
                        #print workType, len(colNums)
                        if workType == "WCDMAErl":
                            #如果是计算3G话务量，则最后一列要乘以2，总数再除以60
                            rowSum += float(row[col])
                            #rowSum *= self.SP
                            rowSum /= 60
                        elif workType == "WCDMAUpData" or workType == "WCDMADownData":
                            #如果是计算3G上下行数据，则分两种情况
                            #1）若是从67109508文件中读入的则正常计算各列值之和
                            #2）若是从67109471或67109390文件中读入，则只有一列，且该列的值要乘以8
                            #下面的if条件，利用2）中只有一列这个特性来区分两种情况
                            if not len(colNums) > 1:
                                rowSum += 7*float(row[col])
                                #print "7*", float(row[col])
                            #rowSum /= 8000
                        else:
                            pass
                    else:
                        pass
                else:
                    #这里输出“脏”数据到log
                    pass
            totalData += rowSum
            #self.dict.SaveToDict(workType, float(row[col]), row[0], row[2])
            self.dict.SaveToDict(workType, rowSum, row[0], row[2])
        return totalData

    def SaveToDB(self, workType, data):
        pass


    def oldoldGetGSMErl(self):
        erl = 0
        self.readCSV()
        self.csvReader.next()
        self.csvReader.next()
        while True:
            try:
                temp = self.csvReader.next()
                if temp:
                    print temp[18]
                    erl += float(temp[18])
            except StopIteration:
                return erl
        #return erl

    def oldGetGSMErl(self):
        erl = 0
        self.readCSV()
        self.csvReader.next()
        self.csvReader.next()
        for row in self.csvReader:
            erl += float(row[18])
        return erl

    def GetGSMErl(self,):
        return self.CalculateNumsInColoum("GSMErl")

    def GetGSMUpdata(self):
        return self.CalculateNumsInColoum("GSMUpData")

    def GetGSMDowndata(self):
        return self.CalculateNumsInColoum("GSMDownData")

    def GetWCDMAErl(self):
        return self.CalculateNumsInColoum("WCDMAErl")

    def GetWCDMAUpdata(self):
        return self.CalculateNumsInColoum("WCDMAUpData")

    def GetWCDMADowndata(self):
        return self.CalculateNumsInColoum("WCDMADownData")


if __name__ == '__main__':
    startTime = datetime.datetime.now()
    print "start time:", startTime
    cr = csvManipulate()
    print cr.GetWCDMAUpdata()
    endTime = datetime.datetime.now()
    print "end time:", endTime
    print "run time:", (endTime - startTime)
    #print cr.GetGSMDowndata()
    # cr.readCSV()
    # row = cr.csvReader.next()
    # row = cr.csvReader.next()
    # row = cr.csvReader.next()
    #print row[0]#.decode("gbk").encode("utf-8")
    #print "end"
    # i = 0
    # while i < 5:
    #     print cr.csvReader.next()
    #     i+=1
    # for line in cr.csvReader:
    #     print line

