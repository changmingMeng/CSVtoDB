# coding: utf-8

import dbManip
import utils
import csv

class Controler(object):
    def __init__(self):
        self.workTypeToDBEntry = {
            "GSMErl": self.AddGSMErl,
            "GSMUpData": self.AddGSMUpdata,
            "GSMDownData": self.AddGSMDowndata,
        }
        self.dbm = dbManip.dbManipulate()

        # self.csvfile = file('E:\csv_test.csv', 'wb')
        # self.writer = csv.writer(self.csvfile)
    # def __del__(self):
    #     self.csvfile.close()

    def closeTestOutput(self):
        #self.csvfile.close()
        pass

    def Commit(self):
        self.dbm.Commit()

    def SaveToDB(self, workType, data, dateAndTime, ID):
        #print "workType = ", workType, "data = ", data, "dateAndTime = ", dateAndTime, "ID = ", ID
        self.workTypeToDBEntry[workType](data, dateAndTime, ID)

    def AddData(self, data, dateAndTime, ID, dataType, GetID):
        cell_id = GetID(ID)
        #print cell_id
        ut = utils.Utils()
        date, time = ut.GetDateAndTimeForPostgresql(dateAndTime)#这里返回的date，time均为psycopg2的格式
        if self.dbm.IsHaveRow(cell_id, ut.pgDateToStr(date), ut.pgTimeToStr(time)):
            # 如果数据库中存在该ID，则把要存储的数据加上原数据再存储
            oldData = float(self.dbm.SelectDataByCondition(dataType, cell_id, ut.pgDateToStr(date), ut.pgTimeToStr(time)))
            newData = data + oldData
            #print newData,
            #self.writer.writerow([data, oldData, newData])
            self.dbm.UpdateByCondition(dataType, newData, ID=cell_id, date=ut.pgDateToStr(date), time=ut.pgTimeToStr(time))
            #print dataType
            if not dataType == "erl":
                #若更新的数据类型是updata或downdata则同时要更新alldata
                Alldata = data + float(self.dbm.SelectDataByCondition("alldata", cell_id, ut.pgDateToStr(date), ut.pgTimeToStr(time)))
                self.dbm.UpdateByCondition("alldata", Alldata, ID=cell_id, date=ut.pgDateToStr(date), time=ut.pgTimeToStr(time))
        else:
            if dataType == "erl":
                self.dbm.Insert(cell_id, date, time, data, 0, 0, 0, "2G")
            elif dataType == "updata":
                self.dbm.Insert(cell_id, date, time, 0, data, 0, data, "2G")
            elif dataType == "downdata":
                self.dbm.Insert(cell_id, date, time, 0, 0, data, data, "2G")
            else:
                pass

    def AddGSMErl(self, data, dateAndTime, ID):
        self.AddData(data, dateAndTime, ID, "erl", self.Get2GID)

    def oldAddGSMErl(self, data, dateAndTime, ID):
        cell_id = self.Get2GID(ID)
        #print cell_id
        #dbm = dbManip.dbManipulate()
        ut = utils.Utils()
        date, time = ut.GetDateAndTimeForPostgresql(dateAndTime)
        if self.dbm.IsHaveID(cell_id):
            #如果数据库中存在该ID，则把要存储的数据加上原数据再存储
            newDate = data + float(self.dbm.SelectItemByID(cell_id, "erl"))
            self.dbm.Update(cell_id, "erl", newDate)
        else:
            self.dbm.Insert(cell_id, date, time, data, 0, 0, 0, "2G")

    def AddGSMUpdata(self, data, dateAndTime, ID):
        self.AddData(data, dateAndTime, ID, "updata", self.Get2GID)

    def AddGSMDowndata(self, data, dateAndTime, ID):
        self.AddData(data, dateAndTime, ID, "downdata", self.Get2GID)

    def Get2GID(self, ID):
        ut = utils.Utils()
        return ut.GetCellId(ID, "CGI=")

    def Get3GID(self, ID):
        pass

    def GET4GID(self, ID):
        pass