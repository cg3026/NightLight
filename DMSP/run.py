# encoding: utf-8
# @Author : GaoCG
# @File : run.py

from DMSP.DMSP_Correct_City import clearWrong, getPara, city


def run():
    root_path = "E:/GCG_storage/storage_dataset/backdown/result_clip/"
    std_path = r"E:/GCG_storage/storage_dataset/NPPpython/test/all/HeiLongJiang/JiXi/"
    clearWrong(std_path)
    data_esti = getPara(std_path, std_path + "clear/" + '鸡西市_F162007.tif')
    city(data_esti, root_path)
