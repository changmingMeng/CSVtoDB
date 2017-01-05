# coding: utf-8

import os
from os.path import join
import psycopg2

class Utils(object):
    def GetCellId(self, desc, str):
        return desc[desc.find(str)+len(str):]

    def IsStringLike(self, anobj):
        try:
            anobj.lower() + anobj + ''
        except:
            return False
        else:
            return True

    def GetDateAndTime(self, dateAndTime):
        dateTime = [int(dateAndTime[0:4]), int(dateAndTime[5:7]), int(dateAndTime[8:10]),
                    int(dateAndTime[11:13]), int(dateAndTime[14:16])]
        return dateTime

    def GetDateAndTimeForPostgresql(self, dateAndTime):
        timeNum = self.GetDateAndTime(dateAndTime)
        date = psycopg2.Date(timeNum[0], timeNum[1], timeNum[2])
        time = psycopg2.Time(timeNum[3], 0, 0)
        return [date, time]

    def GetDateAndTimeNormal(self, dateAndTime):
        date, time = self.GetDateAndTimeForPostgresql(dateAndTime)
        return [self.pgDateToStr(date), self.pgTimeToStr(time)]

    def pgDateToStr(self, date):
        return str(date)[1:11]

    def pgTimeToStr(self, time):
        return str(time)[1:9]

    def dateTimeIdNTToStr(self, dateTimeId):
        return dateTimeId[0] + dateTimeId[1] + dateTimeId[2] + dateTimeId[3]

    def StrToDateTimeIdNT(self, dateTimeId):
        return [dateTimeId[0:10], dateTimeId[10:18], dateTimeId[18:20], dateTimeId[20:]]

if __name__ == "__main__":
    # a = "测试RNC/BSC6900UCell:Label=W测试RNC基站1, CellID=9991"
    # a2 = "GZRNC15/BSC6900UCell:Label=W夏茅工业区1, CellID=26331"
    # b = "CellID="
    ut = Utils()
    # print ut.GetCellId(a, b)
    # print ut.GetCellId(a2, b)
    # dateAndTime = "2016-11-27 23:00"
    # print ut.GetDateAndTime(dateAndTime)
    #
    # print psycopg2.Time(16, 12, 14)
    # print str(psycopg2.Time(16, 12, 14))[1:9]
    # print ut.pgTimeToStr(psycopg2.Time(16, 12, 14))
    list = ['2016-11-28', '22:00:00', '2G','4600125046183']
    str = ut.dateTimeIdNTToStr(list)
    print str
    print ut.StrToDateTimeIdNT(str)