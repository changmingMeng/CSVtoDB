# coding: utf-8

import csv
import re

class csvManipulate(object):
    def __init__(self,
                 #filePath = 'E:/pythonTemp/20161128/',
                 fileName = r'F:\pythonTemp\20161128\pmresult_1275072526_60_201611281600_201611281700.csv'):
        #print "csvManipulate init from default data"
        #self.filePath = filePath
        self.fileName = fileName
        # self.csvFile = file(self.filePath + self.fileName, 'rb')
        self.dataNameDict = {
            "GSMErl": ["K3014:TCH话务量"],
            "GSMUpData": ["TL9023:上行GPRS RLC层吞吐量", "TL9237:上行EGPRS RLC层吞吐量"],
            "GSMDownData": ["TL9123:下行GPRS RLC层吞吐量", "TL9338:下行EGPRS RLC层吞吐量"],
        }
    # def __del__(self):
    #     self.csvFile.close()

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
        temp = 0
        colNums = self.GetColNumFromName(self.dataNameDict[workType])
        #print colNums
        #print self.fileName
        self.readCSV()
        self.csvReader.next()
        self.csvReader.next() #csv文件的第一行是表项名，第二行是单位，第三行开始是数据
        #i = 3
        for row in self.csvReader:
            for col in colNums:
                # 当需要计算的列是csv文件的最后一列时，若该列中的一个值是空，
                # 则会使得提取出的row长度小于col的值，从而导致列表下标越界。
                if len(row) > 26:
                    temp += float(row[col])
        return temp

    def GetGSMErl(self):
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

    def newGetGSMErl(self):
        erl = 0
        self.readCSV()
        self.csvReader.next()
        self.csvReader.next()
        for row in self.csvReader:
            erl += float(row[18])
        return erl

    def newnewGetGSMErl(self,):
        return self.CalculateNumsInColoum("GSMErl")

    def GetGSMUpdata(self):
        return self.CalculateNumsInColoum("GSMUpData")

    def GetGSMDowndata(self):
        return self.CalculateNumsInColoum("GSMDownData")

if __name__ == '__main__':
    print "run"
    cr = csvManipulate()
    #print cr.GetGSMErl()
    #print cr.GetGSMDowndata()
    cr.readCSV()
    row = cr.csvReader.next()
    row = cr.csvReader.next()
    row = cr.csvReader.next()
    print row[0]#.decode("gbk").encode("utf-8")
    print "end"
    # i = 0
    # while i < 5:
    #     print cr.csvReader.next()
    #     i+=1
    # for line in cr.csvReader:
    #     print line

