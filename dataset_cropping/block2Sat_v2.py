import os
import numpy as np
import rasterio
from tqdm import tqdm  # 导入tqdm

# 定义块大小
block_size = 512

# 获取切割块文件的文件夹路径
block_images_folder = "../nj_cropped"

# 获取所有块图像文件
block_image_files = [file for file in os.listdir(block_images_folder) if file.endswith('.tif')]

# 初始化tqdm进度条
progress_bar = tqdm(total=len(block_image_files), desc="Merging Blocks")

# 确定拼合后的影像的尺寸
image_height, image_width = 0, 0

# 从第一个块中获取通道数，数据类型和地理信息
with rasterio.open(os.path.join(block_images_folder, block_image_files[0])) as src:
    num_channels = src.count
    dtype = src.dtypes[0]
    crs = src.crs
    transform = src.transform

for file in block_image_files:
    with rasterio.open(os.path.join(block_images_folder, file)) as src:
        image_height += src.height
        image_width += src.width

# 创建一个新的遥感影像文件
merged_image_path = "merged_image.tif"
with rasterio.open(merged_image_path, 'w', driver='GTiff', width=image_width, height=image_height, count=num_channels, dtype=dtype, crs=crs, transform=transform) as dst:
    # 初始化一个数组来保存合并后的图像数据
    merged_image_data = np.zeros((num_channels, image_height, image_width), dtype=dtype)

    # 遍历块图像文件并将其拼合到合并图像中
    y_offset = 0
    for file in block_image_files:
        with rasterio.open(os.path.join(block_images_folder, file)) as src:
            block_data = src.read()

            # 确保拼接的块数据的尺寸是256x256，如之前所示
            if block_data.shape[1] != 512 or block_data.shape[2] != 512:
                raise ValueError("块的尺寸不是256x256")

            block_height, block_width = block_data.shape[1], block_data.shape[2]

            # 将块数据放入合并后的图像中对应位置
            merged_image_data[:, :, y_offset:y_offset + block_height, 0:block_width] = block_data
            y_offset += block_height

            # 更新进度条
            progress_bar.update(1)

# 关闭进度条
progress_bar.close()

# 写入合并后的数据到新的遥感影像文件
with rasterio.open(merged_image_path, 'r+') as dst:
    dst.write(merged_image_data)

print("拼合完成并保存为", merged_image_path)
