import os
from osgeo import gdal, gdalconst
import numpy as np
from tqdm import tqdm

def process_tiff_files(input_directory, output_directory):
    # 获取输入目录中的所有TIFF文件
    tiff_files = [file for file in os.listdir(input_directory) if file.endswith('.tif')]

    # 创建输出目录
    os.makedirs(output_directory, exist_ok=True)

    for tiff_file in tqdm(tiff_files, desc="Processing TIFF files"):
        input_tiff_path = os.path.join(input_directory, tiff_file)
        output_geotiff_path = os.path.join(output_directory, os.path.splitext(tiff_file)[0] + '.tif')

        # 打开TIFF文件
        dataset = gdal.Open(input_tiff_path, gdalconst.GA_ReadOnly)

        # 获取地理信息
        geotransform = dataset.GetGeoTransform()
        projection = dataset.GetProjection()

        # 读取三个波段的数据为int16数据类型
        band1 = dataset.GetRasterBand(1).ReadAsArray()
        band1 = band1 * 10000
        band1 = band1.astype(np.int16)
        band2 = dataset.GetRasterBand(2).ReadAsArray()
        band2 = band2 * 10000
        band2 = band2.astype(np.int16)
        band3 = dataset.GetRasterBand(3).ReadAsArray()
        band3 = band3 * 10000
        band3 = band3.astype(np.int16)

        # 创建输出GeoTIFF文件
        driver = gdal.GetDriverByName('GTiff')
        out_dataset = driver.Create(output_geotiff_path, band1.shape[1], band1.shape[0], 3, gdal.GDT_Int16)

        # 写入数据到输出文件的各个波段
        out_dataset.GetRasterBand(1).WriteArray(band1)
        out_dataset.GetRasterBand(2).WriteArray(band2)
        out_dataset.GetRasterBand(3).WriteArray(band3)

        # 设置地理信息和投影
        out_dataset.SetGeoTransform(geotransform)
        out_dataset.SetProjection(projection)

        # 释放资源
        out_dataset = None
        dataset = None

    print("All TIFF files processed.")

if __name__ == '__main__':
    input_directory = r'D:\mmdataset\Chongqing'  # 替换为输入目录的路径
    output_directory = r'D:\mmdataset\Chongqing_s2'  # 替换为输出目录的路径

    process_tiff_files(input_directory, output_directory)
