# coding: utf-8

import utils
import dbManip

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton#使DataDict类成为单例类
class DataDict(object):
    def __init__(self):
        self.workTypeToDBEntry = {
            "GSMErl": self.AddGSMErl,
            "GSMUpData": self.AddGSMUpdata,
            "GSMDownData": self.AddGSMDowndata,

            "WCDMAErl": self.AddWCDMAErl,
            "WCDMAUpData": self.AddWCDMAUpdata,
            "WCDMADownData": self.AddWCDMADowndata
        }
        self.dict = {}#这个字典用来存放数据，它的key是[ID, date, time],vlaue是一个key是dataType，vlaue是data的字典
        self.db = dbManip.dbManipulate()

    def ClearDict(self):
        self.dict = {}

    def SaveToDict(self, workType, data, dateAndTime, ID):
        #print "workType = ", workType, "data = ", data, "dateAndTime = ", dateAndTime, "ID = ", ID
        self.workTypeToDBEntry[workType](data, dateAndTime, ID)

    def AddData(self, data, dateAndTime, ID, dataType, GetID, netType):
        cell_id = GetID(ID)
        #print cell_id
        ut = utils.Utils()
        date, time = ut.GetDateAndTimeNormal(dateAndTime)#这里返回的date，time均为psycopg2的格式
        dateTimeIdNT = ut.dateTimeIdNTToStr([date, time, netType, cell_id]) # 用(cell_id, date, time)元组来代替dateTimeId
                                                                # 可少量提升性能，有空再做。。。
        if dateTimeIdNT in self.dict:
            # 如果dict的key中存在该ID日期时间，且dict的value的key中存在该dataType
            # 则把要存储的数据加上原数据再存储
            oldData = self.dict[dateTimeIdNT][dataType]
            newData = data + oldData
            #print newData,
            #self.writer.writerow([data, oldData, newData])
            self.dict[dateTimeIdNT][dataType] = newData
            #print dataType
            if not dataType == "erl":
                #若更新的数据类型是updata或downdata则同时要更新alldata
                alldata = data + self.dict[dateTimeIdNT]['alldata']
                self.dict[dateTimeIdNT]['alldata'] = alldata
            else:
                pass

        else:
            self.dict[dateTimeIdNT] = {}
            self.dict[dateTimeIdNT][dataType] = data
            for type in ['erl', 'updata', 'downdata', 'alldata']:
                if not type == dataType:
                    self.dict[dateTimeIdNT][type] = 0
            if not dataType == "erl":
                self.dict[dateTimeIdNT]['alldata'] = data

    def AddGSMErl(self, data, dateAndTime, ID):
        self.AddData(data, dateAndTime, ID, "erl", self.Get2GID, "2G")

    def AddGSMUpdata(self, data, dateAndTime, ID):
        self.AddData(data, dateAndTime, ID, "updata", self.Get2GID, "2G")

    def AddGSMDowndata(self, data, dateAndTime, ID):
        self.AddData(data, dateAndTime, ID, "downdata", self.Get2GID, "2G")

    def AddWCDMAErl(self, data, dateAndTime, ID):
        self.AddData(data, dateAndTime, ID, "erl", self.Get3GID, "3G")

    def AddWCDMAUpdata(self, data, dateAndTime, ID):
        self.AddData(data, dateAndTime, ID, "updata", self.Get3GID, "3G")

    def AddWCDMADowndata(self, data, dateAndTime, ID):
        self.AddData(data, dateAndTime, ID, "downdata", self.Get3GID, "3G")

    def Get2GID(self, ID):
        ut = utils.Utils()
        return ut.GetCellId(ID, "CGI=")

    def Get3GID(self, ID):
        ut = utils.Utils()
        return ut.GetCellId(ID, "CellID=")

    def GET4GID(self, ID):
        pass

    def ConnectToDB(self,
                    database="testdb",
                    user="postgres",
                    password="123456",
                    host="127.0.0.1",
                    port="5432"):
        self.db = dbManip.dbManipulate(database, user, password, host, port)

    def SaveToDB(self):
        ut = utils.Utils()
        for dateTimeId in self.dict.keys():
            date, time, nettype, ID = ut.StrToDateTimeIdNT(dateTimeId)
            self.db.Insert(ID,
                           date,
                           time,
                           self.dict[dateTimeId]["erl"],
                           self.dict[dateTimeId]["updata"]/8000,
                           self.dict[dateTimeId]["downdata"]/8000,
                           self.dict[dateTimeId]["alldata"]/8000,
                           nettype)
        self.db.Commit()

if __name__ == "__main__":
    # a = DataDict()
    # b = DataDict()
    # print id(a)
    # print id(b)
    li = [1,2,3,4,5]
    print len(li)
    print li.index(5)
