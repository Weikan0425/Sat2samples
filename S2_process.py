from dataset_cropping.float2int16 import process_tiff_files
from dataset_cropping.compress import compress_tiff_images
from dataset_cropping.cov_compress import process_and_compress_tiff

if __name__ == '__main__':
    input_directory = r'D:\mmdataset\Wuhan'  # 替换为输入目录的路径
    output_directory = r'D:\mmdataset\Wuhan_s2'  # 替换为输出目录的路径
    # # float32 转 uint16
    # process_tiff_files(input_directory, output_directory)

    # 无损压缩
    compress_tiff_images(input_directory, output_directory)

    # # float32 转 uint16 并无损压缩
    # process_and_compress_tiff(input_directory, output_directory)