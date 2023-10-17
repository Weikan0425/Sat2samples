import numpy as np
import rasterio
import os
from tqdm import tqdm

# 打开影像
image_path = "../s2_nj.tif"
with rasterio.open(image_path) as src:
    # 获取地理坐标变换信息和影像数据
    transform = src.transform
    image_data = src.read()


# 定义块大小
block_size = 512

# 获取原始尺寸
image_height, image_width = image_data.shape[1], image_data.shape[2]

# 循环切割图像
for y in range(0, image_height, block_size):
    for x in range(0, image_width,block_size):
        y_end = min(y + block_size, image_height)
        x_end = min(x + block_size, image_width)

        # 切割图像块
        block = image_data[:, y:y_end,x:x_end]

        # 创建一个新的遥感影像来保存块
        block_image_path = f"../nj_cropped/block_{x}_{y}.tif"
        with rasterio.open(block_image_path, 'w', driver='GTiff', width=block.shape[2], height=block.shape[1],count=block.shape[0], dtype=block.dtype, crs=src.crs, transform=transform) as dst:
            dst.write(block)

        # 处理块坐标以便下一次迭代
        x += block_size
    y += block_size
