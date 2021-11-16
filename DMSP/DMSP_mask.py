import arcpy
import os
from arcpy.sa import *
arcpy.CheckOutExtension("spatial")
arcpy.gp.overwriteOutput=1
filepath = "D:/NPP/DMSP"
arcpy.env.workspace = filepath #所有栅格影像所在文件夹
os.chdir(filepath)
rasters = arcpy.ListRasters("*", "tif")
arcpy.AddMessage(rasters)
mask= r"F:\NPPpython\chinaborder/province.shp"  #用于提取的矢量掩膜
for raster in rasters:
    print(raster)
    out = "F:/NPPpython/test/province/"+raster
    # out = ExtractByMask(raster,mask)
    # out.save("F:/NPPpython/test/shi/"+raster.split(".")[0]+'.tif')
    arcpy.gp.ExtractByMask_sa(raster, mask, out)
print("OK")