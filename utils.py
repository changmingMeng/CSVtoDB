# coding: utf-8

import os
from os.path import join


class Utils(object):
    def GetCellId(self,desc, str):
        return desc[desc.find(str)+len(str):]

if __name__ == "__main__":
    a = "测试RNC/BSC6900UCell:Label=W测试RNC基站1, CellID=9991"
    a2 = "GZRNC15/BSC6900UCell:Label=W夏茅工业区1, CellID=26331"
    b = "CellID="
    ut = Utils()
    print ut.GetCellId(a, b)
    print ut.GetCellId(a2, b)
