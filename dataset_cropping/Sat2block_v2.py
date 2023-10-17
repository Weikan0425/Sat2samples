import os
import numpy as np
import rasterio

# 定义块大小
block_size = 512

# 打开影像
image_path = "../s2_nj.tif"
with rasterio.open(image_path) as src:
    # 获取地理坐标变换信息和影像数据
    transform = src.transform
    image_data = src.read()


# 创建一个新的遥感影像文件夹用于保存切割块
output_folder = "../nj_cropped/"
os.makedirs(output_folder, exist_ok=True)

# 获取原始尺寸
num_channels, image_height, image_width = image_data.shape

# 遍历块图像文件并切割成256x256块
for y in range(0, image_height, block_size):
    for x in range(0, image_width, block_size):
        y_end = min(y + block_size, image_height)
        x_end = min(x + block_size, image_width)

        block = image_data[:, y:y_end, x:x_end]

        # 如果块的尺寸不是256x256，填充到256x256
        if block.shape[1] != 512 or block.shape[2] != 512:
            padded_block = np.zeros((num_channels, 512, 512), dtype=image_data.dtype)
            padded_block[:, :block.shape[1], :block.shape[2]] = block
            block = padded_block

        # 保存块
        block_image_path = os.path.join(output_folder, f"block_{x}_{y}.tif")
        with rasterio.open(block_image_path, 'w', driver='GTiff', width=512, height=512, count=num_channels,
                           dtype=image_data.dtype, crs=src.crs, transform=src.transform) as dst:
            dst.write(block)
print("切割完成并保存到文件夹", output_folder)