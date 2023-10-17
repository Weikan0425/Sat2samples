from osgeo import gdal
import json
import os

# 读取研究区域的JSON文件
with open("../南京市.json", "r", encoding="utf-8") as json_file:
    study_area = json.load(json_file)

# 打开要切割的图像文件
input_image_path = "../s2_nj.tif"
ds = gdal.Open(input_image_path)

if ds is None:
    print(f"Error: Unable to open {input_image_path}")
    exit(1)

# 获取图像的地理信息
transform = ds.GetGeoTransform()

# 获取图像的波段
band = ds.GetRasterBand(1)

# 定义子图大小
subimage_width = 100  # 子图宽度
subimage_height = 100  # 子图高度

# 切割图像并保持地理信息
for feature in study_area["features"]:
    geometry = feature["geometry"]
    for i in range(0, ds.RasterXSize, subimage_width):
        for j in range(0, ds.RasterYSize, subimage_height):
            subimage = band.ReadAsArray(i, j, subimage_width, subimage_height)
            subimage_geotransform = (
                transform[0] + i * transform[1],
                transform[1],
                transform[2],
                transform[3] + j * transform[5],
                transform[4],
                transform[5],
            )

            # 创建一个新的GeoTIFF文件以保存子图
            output_image_path = f"output_subimage_{i}_{j}.tif"
            driver = gdal.GetDriverByName("GTiff")
            output_ds = driver.Create(
                output_image_path,
                subimage_width,
                subimage_height,
                1,
                band.DataType,
            )

            if output_ds is None:
                print(f"Error: Unable to create {output_image_path}")
                exit(1)

            output_ds.SetGeoTransform(subimage_geotransform)
            output_ds.SetProjection(ds.GetProjection())
            output_band = output_ds.GetRasterBand(1)
            output_band.WriteArray(subimage)
            output_ds = None

# 关闭输入图像
ds = None
