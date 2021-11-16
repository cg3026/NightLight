# encoding: utf-8
# @Author : GaoCG
# @File : test.py

import os
import arcpy
import numpy as np
import sympy
import Spyder.run

path = r"E:/GCG_storage/storage_dataset/city_res/海南省/"

# for cityname in os.listdir(path):
#     len_city = len(os.listdir(path))
#     cunrrent_city = 1
#     for cityname in os.listdir(path):
#         if not os.path.isdir(path + cityname):
#             print("!isdir")
#             continue
#         if len(os.listdir(path + cityname)) == 0:
#             print("!no data")
#             continue
#         print(os.listdir(path + cityname))
#         print("当前位置：%s_%s, %d/%d" % ('海南省', cityname, cunrrent_city, len_city))
#         cunrrent_city = cunrrent_city + 1
Spyder.run.run()
