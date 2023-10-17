import os
import gdal
from tqdm import tqdm

def compress_tiff_images(input_dir, output_dir, compression="LZW"):
    # 获取输入目录中的所有 TIFF 影像文件
    tiff_files = [f for f in os.listdir(input_dir) if f.endswith('.tif')]

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 遍历 TIFF 影像文件并进行无损压缩
    for tiff_file in tqdm(tiff_files, desc="Compressing TIFF images"):
        input_path = os.path.join(input_dir, tiff_file)
        output_path = os.path.join(output_dir, tiff_file)

        # 打开输入 TIFF 影像
        input_ds = gdal.Open(input_path, gdal.GA_ReadOnly)

        if input_ds is None:
            print(f"无法打开输入 TIFF 影像: {input_path}")
            continue

        # 获取输入影像的驱动
        driver = gdal.GetDriverByName("GTiff")

        # 创建输出 TIFF 影像
        output_ds = driver.CreateCopy(output_path, input_ds, options=["COMPRESS=" + compression])

        if output_ds is None:
            print(f"无法创建输出 TIFF 影像: {output_path}")
            continue

        # 关闭数据集
        input_ds = None
        output_ds = None

if __name__ == '__main__':
    input_directory = 'D:\mmdataset\Chongqing_s2'  # 替换为输入目录的路径
    output_directory = 'D:\mmdataset\Chongqing_s2_c'  # 替换为输出目录的路径
    compression_method = "LZW"  # 可根据需要选择压缩方法，如 "LZW", "DEFLATE", "JPEG", 等

    compress_tiff_images(input_directory, output_directory, compression=compression_method)
