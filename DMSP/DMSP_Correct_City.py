# encoding: utf-8
# @Author : GaoCG
# @File : DMSP_Correct_City.py

import os
import arcpy
import xlwt
import xlrd
from xlutils.copy import copy
import numpy as np
import sympy

arcpy.CheckOutExtension("Spatial")


# 清除异常值
# 清除策略：将DN值小于0的设定为0
# 实施阶段：前期对异常值数据进行处理
# 实施对象：源数据或被分割后的标准市数据
# 实施结果：初步去除异常后的数据
def clearWrong(path):
    path_map = path + "clear/"
    if not os.path.exists(path_map):
        os.makedirs(path_map)
    if not len(os.listdir(path_map)) == 0:
        files_re = os.listdir(path_map)
        for file_re in files_re:
            os.remove(path_map + file_re)
    files = os.listdir(path)
    for file in files:
        if os.path.isdir(path + file):
            continue
        if not file.endswith(".tif"):
            continue
        rr = arcpy.Raster(path + file)
        out = arcpy.sa.Con(rr < 0, 0, rr)  # 如果像元值小于0，置为0
        out.save(path_map + file)


# 求解R2的值
# 输入：参数a, b, c, y均值, 需校正影像，标准影像
# 输出：R2
def R2(a_y, b_y, c_y, y_m, array, array_std, filename):
    numx_y = np.long(0)
    numy_y = np.long(0)
    if not os.path.exists("E:/GCG_storage/storage_dataset/NPPpython/test/para.xls"):
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('para')
        worksheet.write(0, 0, label='年份')
        worksheet.write(0, 1, label='传感器')
        worksheet.write(0, 2, label='a')
        worksheet.write(0, 3, label='b')
        worksheet.write(0, 4, label='c')
        worksheet.write(0, 5, label='R2')
        workbook.save("E:/GCG_storage/storage_dataset/NPPpython/test/para.xls")
    for row in range(array.shape[0]):
        for colum in range(array.shape[1]):
            if (array[row][colum] > 0) & (array_std[row][colum] > 0):
                m = a_y * np.long(array[row][colum]) * np.long(array[row][colum]) + b_y * np.long(
                    array[row][colum]) + c_y - np.long(array_std[row][colum])
                numx_y = numx_y + m * m
                n = np.long(array_std[row][colum]) - y_m
                numy_y = numy_y + n * n
    r = 1 - numx_y / numy_y

    workbook = xlrd.open_workbook("E:/GCG_storage/storage_dataset/NPPpython/test/para.xls")
    worksheet = workbook.sheet_by_name("para")
    currentrows = worksheet.nrows
    cp = copy(workbook)
    sheet = cp.get_sheet(0)
    sheet.write(currentrows, 0, label=filename.split("_")[1][3:7])
    sheet.write(currentrows, 1, label=filename.split("_")[1][0:3])
    sheet.write(currentrows, 2, label=float(a_y))
    sheet.write(currentrows, 3, label=float(b_y))
    sheet.write(currentrows, 4, label=float(c_y))
    sheet.write(currentrows, 5, label=float(r))
    os.remove("E:/GCG_storage/storage_dataset/NPPpython/test/para.xls")
    cp.save("E:/GCG_storage/storage_dataset/NPPpython/test/para.xls")
    return r


# 求解多项式回归参数
# 求解策略：通过sympy包中的方程组求解函数求解
# 实施阶段：待定，需优化流程以提高R2
# 实施对象：鸡西市数据（是否需先进行优化处理，有待商榷）
# 实施结果：以字典形式存储的回归参数和R2
def getPara(path, path_07):
    path_map = path + "clear/"
    # 存放所有求得的回归参数，格式为:{year} -> {satellite} -> {a, b, c}
    data = {}
    # 定义变量a, b, c
    a = sympy.symbols("a", real=True)
    b = sympy.symbols("b", real=True)
    c = sympy.symbols("c", real=True)

    # 遍历文件夹
    file = os.listdir(path_map)
    for filename in file:
        # 定义方程所需值
        if os.path.isdir(path + filename):
            continue
        if not filename.endswith('.tif'):
            continue
        sumx = np.int64(0)
        sumx2 = np.int64(0)
        sumx3 = np.int64(0)
        sumx4 = np.int64(0)
        sumy = np.int64(0)
        sumxy = np.int64(0)
        sumx2y = np.int64(0)
        print("当前文件：" + path + filename)
        # 文件打开
        inputRaster = arcpy.Raster(path + filename)
        stdRaster = arcpy.Raster(path_07)
        # 转化为numpy数组
        arr_std = arcpy.RasterToNumPyArray(stdRaster)
        arr = arcpy.RasterToNumPyArray(inputRaster)
        # 统计有效值
        total = 0
        count = 0
        # 循环计算数值
        for row in range(arr.shape[0]):
            for colum in range(arr.shape[1]):
                if arr_std[row][colum] >= 0:
                    count = count + 1
                if (arr[row][colum] > 0) & (arr_std[row][colum] > 0):
                    total = total + 1
                    sumx = sumx + np.int64(arr[row][colum])
                    sumy = sumy + np.int64(arr_std[row][colum])
                    sumx2 = sumx2 + np.int64(arr[row][colum]) * np.int64(arr[row][colum])
                    sumx3 = sumx3 + np.int64(arr[row][colum]) * np.int64(arr[row][colum]) * np.int64(
                        arr[row][colum])
                    sumx4 = sumx4 + np.int64(arr[row][colum]) * np.int64(arr[row][colum]) * np.int64(
                        arr[row][colum]) * np.int64(arr[row][colum])
                    sumxy = sumxy + np.int64(arr[row][colum]) * np.int64(arr_std[row][colum])
                    sumx2y = sumx2y + np.int64(arr[row][colum]) * np.int64(arr[row][colum]) * np.int64(
                        arr_std[row][colum])
        # 求y均值
        ymean = np.long(sumy / total)
        # 定义三个方程组
        f1 = (np.long(sumx2y) - np.long(sumx3) * b - np.long(sumx2) * c) / np.long(sumx4) - a
        f2 = (np.long(sumxy) - np.long(sumx) * c - np.long(sumx3) * a) / np.long(sumx2) - b
        f3 = (np.long(sumy) - np.long(sumx2) * a - np.long(sumx) * b) / np.long(total) - c
        # 求解方程组
        result = sympy.solve([f1, f2, f3], [a, b, c])
        # 获得结果
        m1 = result[a]
        m2 = result[b]
        m3 = result[c]
        # 求取当前影像回归的R2
        r2 = R2(sympy.Float(m1, 5), sympy.Float(m2, 5), sympy.Float(m3, 5), ymean, arr, arr_std, filename)
        # 保存回归参数和R2到par
        par = {"a": sympy.Float(m1, 5), "b": sympy.Float(m2, 5), "c": sympy.Float(m3, 5), "R2": r2}
        # 将par链接到某卫星下
        sat = {filename.split("_")[2][0:3]: par}
        # 判断当前年份是否已保存数据
        if data.get(filename.split("_")[2][3:7]):
            # 组合同年异星数据
            data.get(filename.split("_")[2][3:7]).update(sat)
        else:
            # 直接保存
            data[filename.split("_")[2][3:7]] = sat
    # 输出全部data数据
    print(data)
    return data


# 同景校正
# 校正策略：通过多项式线性回归方程进行逐年校正
# 实施阶段：对选定的标准地市数据进行多项式回归估值并取得校正参数之后
# 实施对象：每年的不同卫星下的选定的地市数据（已进行异常值去除）
# 实施结果：校正后的逐年逐卫星中国全境数据
# 备注：暂未进行数据的真实处理！！
def mapCorrect(path, data_dict, path_07):
    path_sat = path + "satCorrect/"
    path_map = path + "clear/"
    stdRaster = arcpy.Raster(path_07)
    if not os.path.exists(path_sat):
        os.makedirs(path_sat)
    if not len(os.listdir(path_sat)) == 0:
        files_re = os.listdir(path_sat)
        for file_re in files_re:
            os.remove(path_sat + file_re)
    files_map = os.listdir(path_map)
    for file in files_map:
        if os.path.isdir(path + file):
            continue
        if not file.endswith('.tif'):
            continue
        staName = file.split("_")[2][0:3]
        staYear = file.split("_")[2][3:7]
        rr = arcpy.Raster(path + file)
        # 计算方法为 aDN^2+bDN+c
        # out_map_correct = arcpy.sa.Con(rr >= 0, arcpy.sa.Con(stdRaster > 0, float(data_dict[staYear][staName]["a"]) * rr * rr + float(data_dict[staYear][staName]["b"]) * rr + float(data_dict[staYear][staName]["c"]), rr), rr)
        # out_map_correct = arcpy.sa.Con(rr >= 0, arcpy.sa.Con(stdRaster > 0, float(data_dict[staYear][staName]["a"]) * rr * rr + float(data_dict[staYear][staName]["b"]) * rr + float(data_dict[staYear][staName]["c"]), rr), rr)
        # out_map_correct = arcpy.sa.Con(rr > 0, float(data_dict[staYear][staName]["a"]) * rr * rr + float(
        #     data_dict[staYear][staName]["b"]) * rr + float(data_dict[staYear][staName]["c"]), rr)
        # out_map_correct.save(path_sat + file)
        rr.save(path_sat + file)


# 同年异星校正
# 校正策略：遍历年份字典，对每一年份根据其卫星数量进行校正判断
# 实施阶段：同景校正完毕之后后
# 实施对象：在同年份下之多只有两颗卫星的前提下，进行不同卫星之间校正
# 实施结果：消除卫星间差异，同年只保留一份卫星灯光数据
def satCorrect(path, province, cityname, data_dict):
    path_map = path + "satCorrect/" + province + '_' + cityname + '_'
    path_year = path + "yearCorrect/"
    if not os.path.exists(path_year):
        os.makedirs(path_year)
    if not len(os.listdir(path_year)) == 0:
        files_re = os.listdir(path_year)
        for file_re in files_re:
            os.remove(path_year + file_re)
    path_year = path + "yearCorrect/" + province + '_' + cityname + '_'
    for years in data_dict:
        set = []
        length = len(data_dict[years])
        if length == 2:  # 同一年有两个卫星的进行校正
            for sat in data_dict[years]:
                if not os.path.exists(path_map + sat + years + '.tif'):
                    continue
                if os.path.exists(path_map + sat + years + '.tif'):
                    set.append(path_map + sat + years + '.tif')
                else:
                    print("！")
            if len(set) == length:
                raster_pre = arcpy.Raster(set[0])
                raster_next = arcpy.Raster(set[1])
                out_sat_correct = arcpy.sa.Con((raster_pre != 0) & (raster_next != 0),
                                               (raster_pre + raster_next) / float(2),
                                               0)  # 判别条件和校正值见论文
                out_sat_correct.save(path_year + years + '.tif')
        else:  # 同一年只有一颗卫星的不进行校正
            for sat in data_dict[years]:
                if not os.path.exists(path_map + sat + years + '.tif'):
                    continue
                out_sat_correct = arcpy.Raster(path_map + sat + years + '.tif')
                out_sat_correct.save(path_year + years + '.tif')


# 异年校正
# 校正策略：遍历年份字典，对每一年根据其前后年份进行校正判断
# 实施阶段：已完成异星间校正，同年份数据唯一
# 实施对象：相邻三年间的灯光卫星数据
# 实施结果：全部校正完毕，输出最终结果
def yearCorrect(path, province, cityname, data_dict):
    path_result = path + "result/"
    path_year = path + "yearCorrect/" + province + '_' + cityname + '_'
    path_result_mor = path + "result/mor/"
    if os.path.exists(path_result_mor):
        if not len(os.listdir(path_result_mor)) == 0:
            files_re = os.listdir(path_result_mor)
            for file_re in files_re:
                os.remove(path_result_mor + file_re)
        os.rmdir(path_result_mor)
    if os.path.exists(path_result):
        if not len(os.listdir(path_result)) == 0:
            files_re = os.listdir(path_result)
            for file_re in files_re:
                os.remove(path_result + file_re)
        os.rmdir(path_result)
    os.makedirs(path_result_mor)
    path_result_mor = path_result_mor + province + '_' + cityname + '_'
    path_result = path_result + province + '_' + cityname + '_'
    year_set = []
    for years in data_dict:
        if os.path.exists(path_year + str(years) + '.tif'):
            year_set.append(str(years))
    for yearshift in range(len(year_set)):
        year = 1992 + len(year_set) - yearshift - 1
        if (year == 1992) | (yearshift == len(year_set) - 1):
            raster_current = arcpy.Raster(path_year + str(year) + '.tif')
            raster_current.save(path_result_mor + str(year) + '_mor.tif')
        else:
            raster_current = arcpy.Raster(path_year + str(year) + '.tif')  # 当前年份灯光数据
            raster_pre = arcpy.Raster(path_year + year_set[yearshift - 1] + '.tif')  # 前一年份灯光数据
            raster_next = arcpy.Raster(path_year + year_set[yearshift + 1] + '.tif')  # 后一年份灯光数据
            out_result = arcpy.sa.Con((raster_next == 0), 0,
                                      arcpy.sa.Con((raster_next > 0), raster_current, 0))  # 判断条件和校正值见论文，此处采用CON嵌套
            out_result.save(path_result_mor + str(year) + '_mor.tif')
    for yearshift in range(len(year_set)):
        year = 1992 + yearshift
        if (year == 1992) | (yearshift == len(year_set) - 1):
            raster_current = arcpy.Raster(path_result_mor + str(year) + '_mor.tif')
            raster_current.save(path_result + str(year) + '.tif')
        else:
            raster_current = arcpy.Raster(path_result_mor + str(year) + '_mor.tif')  # 当前年份灯光数据
            raster_pre = arcpy.Raster(path_result + year_set[yearshift - 1] + '.tif')  # 前一年份灯光数据
            raster_next = arcpy.Raster(
                path_result_mor + year_set[yearshift + 1] + '_mor.tif')  # 后一年份灯光数据
            out_result = arcpy.sa.Con((raster_next > 0),
                                      arcpy.sa.Con((raster_pre > 0.8 * raster_current), raster_pre, raster_current),
                                      0)  # 判断条件和校正值见论文，此处采用CON嵌套
            out_result.save(path_result + str(year) + '.tif')


# 将灯光相关数据写入xls文件
def writeexcel(path, root_path):
    path_result = path + "result/"
    if not os.path.exists(root_path + "/result.xls"):
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('data')
        worksheet.write(0, 0, label='province')
        worksheet.write(0, 1, label='city')
        worksheet.write(0, 2, label='year')
        worksheet.write(0, 3, label='value')
        worksheet.write(0, 4, label='count')
        worksheet.write(0, 5, label='DNsum')
        workbook.save(root_path + "/result.xls")
    files = os.listdir(path_result)
    for filename in files:
        if not filename.endswith(".tif"):
            continue
        sumx = np.int64(0)
        tif = arcpy.Raster(path_result + filename)
        numpy_tif = arcpy.RasterToNumPyArray(tif, nodata_to_value=-1)
        # 统计有效值
        total = 0
        count = 0
        # 循环计算数值
        for row in range(numpy_tif.shape[0]):
            for colum in range(numpy_tif.shape[1]):
                if numpy_tif[row][colum] >= 0:
                    if not numpy_tif[row][colum] == 0:
                        count = count + 1
                    total = total + 1
                    sumx = sumx + np.int64(numpy_tif[row][colum])
        # 求x均值
        xmean = round(float(sumx) / float(total), 4)
        workbook = xlrd.open_workbook(root_path + "/result.xls")
        worksheet = workbook.sheet_by_name("data")
        currentrows = worksheet.nrows
        cp = copy(workbook)
        sheet = cp.get_sheet(0)
        sheet.write(currentrows, 0, label=filename.split("_")[0])
        sheet.write(currentrows, 1, label=filename.split("_")[1])
        sheet.write(currentrows, 2, label=filename.split("_")[2][0:4])
        sheet.write(currentrows, 3, label=xmean)
        sheet.write(currentrows, 4, label=count)
        sheet.write(currentrows, 5, label=int(sumx))
        os.remove(root_path + "/result.xls")
        cp.save(root_path + "/result.xls")


# 省份内循环
def province(data_esti, root_path):
    len_pro = len(os.listdir(root_path))
    current_pro = 1
    for proname in os.listdir(root_path):
        if not os.path.isdir(root_path + proname):
            print("!isdir")
            continue
        if len(os.listdir(root_path + proname)) == 0:
            print("!no data")
            continue
        print("当前省份：%s, %d/%d" % (proname, current_pro, len_pro))
        city(data_esti, root_path + proname + "/", proname, len_pro, current_pro)
        current_pro = current_pro + 1


# 城市内循环
def city(data_esti, province_path, proname, len_pro, current_pro):
    len_city = len(os.listdir(province_path))
    cunrrent_city = 1
    for cityname in os.listdir(province_path):
        if not os.path.isdir(province_path + cityname):
            print("!isdir")
            continue
        if len(os.listdir(province_path + cityname)) == 0:
            print("当前位置：%s_%s, %d/%d, %d/%d" % (proname, cityname, cunrrent_city, len_city, current_pro, len_pro))
            print("!no data")
            cunrrent_city = cunrrent_city + 1
            continue
        print("当前位置：%s_%s, %d/%d, %d/%d" % (proname, cityname, cunrrent_city, len_city, current_pro, len_pro))
        Correct(data_esti, province_path + cityname + "/", proname, cityname)
        cunrrent_city = cunrrent_city + 1


# 校正函数
def Correct(data_esti, city_path, proname, cityname):
    # 执行过程
    # Step.1  清除异常值
    if not cityname == '鸡西市':  # 鸡西已处理，跳过
        clearWrong(city_path)
    # Step.2  同景校正
    mapCorrect(city_path, data_esti, city_path + proname + "_" + cityname + "_F162007.tif")
    # Step.3  同年异星校正
    satCorrect(city_path, proname, cityname, data_esti)
    # Step.4  异年校正
    yearCorrect(city_path, proname, cityname, data_esti)
    # Step.5  读取文件指数输出到表格
    root = os.path.dirname(os.path.dirname(os.path.dirname(city_path)))
    writeexcel(city_path, root)


def process():
    root_path = "E:/GCG_storage/storage_dataset/city_res/"
    std_path = root_path + "黑龙江省/鸡西市/"
    # 鸡西市校正
    clearWrong(std_path)
    # 检查标准文件存在
    if not os.path.exists(std_path + "clear/黑龙江省_鸡西市_F162007.tif"):
        print("缺乏鸡西市F162007校正文件，程序结束...")
        return
    # 获得校正参数
    data_esti = getPara(std_path, std_path + "clear/黑龙江省_鸡西市_F162007.tif")
    # 准备完毕，执行校正
    province(data_esti, root_path)


process()
