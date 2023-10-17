from osgeo import osr, gdal
import numpy as np
import os
from PIL import Image
import time
from skimage import io
import gdal
import cv2
import imageio

def get_file_names(data_dir, file_type=['tif', 'tiff']):
    result_dir = []
    result_name = []
    for maindir, subdir, file_name_list in os.walk(data_dir):
        for filename in file_name_list:
            apath = maindir + '/' + filename
            ext = apath.split('.')[-1]
            if ext in file_type:
                result_dir.append(apath)
                result_name.append(filename)
            else:
                pass
    return result_dir, result_name


def get_same_img(img_dir, img_name):
    result = {}
    for idx, name in enumerate(img_name):
        temp_name = ''
        for idx2, item in enumerate(name.split('_')[:-4]):
            if idx2 == 0:
                temp_name = temp_name + item
            else:
                temp_name = temp_name + '_' + item

        if temp_name in result:
            result[temp_name].append(img_dir[idx])
        else:
            result[temp_name] = []
            result[temp_name].append(img_dir[idx])
    return result


def assign_spatial_reference_byfile(src_path, dst_path):
    src_ds = gdal.Open(src_path, gdal.GA_ReadOnly)
    sr = osr.SpatialReference()
    sr.ImportFromWkt(src_ds.GetProjectionRef())
    geoTransform = src_ds.GetGeoTransform()
    dst_ds = gdal.Open(dst_path, gdal.GA_Update)
    dst_ds.SetProjection(sr.ExportToWkt())
    dst_ds.SetGeoTransform(geoTransform)
    dst_ds = None
    src_ds = None

def match_brightness(source, target):
    # 计算原始图像和目标图像的平均亮度
    source_mean = np.mean(source)
    target_mean = np.mean(target)

    # 计算亮度差
    diff = target_mean - source_mean

    # 将裁剪后的图像的亮度调整为与原始图像一致
    matched_image = (source.astype(np.float64) + diff).clip(0, 65535)
    matched_image = (matched_image * (255.0 / 65535.0)).astype(np.uint8)

    return matched_image

def stretch_2_percent_linear(image):
    # 计算2%拉伸的最小和最大像素值
    min_percentile = np.percentile(image, 0.5)
    max_percentile = np.percentile(image, 99.5)

    # 线性拉伸
    stretched_image = np.clip((image - min_percentile) / (max_percentile - min_percentile) * 255, 0, 255).astype(np.uint8)

    return stretched_image

def cut(in_dir, out_dir, file_type=['tif', 'tiff'], out_type='png', out_size=1024):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    data_dir_list, _ = get_file_names(in_dir, file_type)
    count = 0
    print('Cut begining for ', str(len(data_dir_list)), ' images.....')
    for each_dir in data_dir_list:
        time_start = time.time()
        image = np.array(io.imread(each_dir))
        # image = np.array(Image.open(each_dir))
        print(image.shape)

        cut_factor_row = int(np.ceil(image.shape[0] / out_size))
        cut_factor_clo = int(np.ceil(image.shape[1] / out_size))
        for i in range(cut_factor_row):
            for j in range(cut_factor_clo):

                if i == cut_factor_row - 1:
                    i = image.shape[0] / out_size - 1
                else:
                    pass

                    if j == cut_factor_clo - 1:
                        j = image.shape[1] / out_size - 1
                    else:
                        pass

                start_x = int(np.rint(i * out_size))
                start_y = int(np.rint(j * out_size))
                end_x = int(np.rint((i + 1) * out_size))
                end_y = int(np.rint((j + 1) * out_size))

                temp_image = image[start_x:end_x, start_y:end_y, :]

                print('temp_image:', temp_image.shape)
                out_dir_images = out_dir + '/' + each_dir.split('/')[-1].split('.')[0] \
                                 + '_' + str(start_x) + '_' + str(end_x) + '_' + str(start_y) + '_' + str(
                    end_y) + '.' + out_type

                # out_image = Image.fromarray(temp_image)
                # out_image.save(out_dir_images)
                # 灰度拉伸到0-255范围内
                # 执行直方图匹配
                # 执行直方图匹配
                # cv2.normalize(temp_image , temp_image , 0, 255, cv2.NORM_MINMAX)
                # temp_image = stretch_2_percent_linear(temp_image)
                # # 使用OpenCV保存图像
                # cv2.imwrite(out_dir_images, np.uint8(temp_image))
                imageio.imsave(out_dir_images,temp_image)
                src_path = 'F:/带地理坐标.tif'  # 带地理影像
                # assign_spatial_reference_byfile(src_path, out_dir_images)

        count += 1
        print('End of ' + str(count) + '/' + str(len(data_dir_list)) + '...')
        time_end = time.time()
        print('Time cost: ', time_end - time_start)
    print('Cut Finsh!')
    return 0


def combine(data_dir, w, h, c, out_dir, out_type='tif', file_type=['tif', 'tiff']):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    img_dir, img_name = get_file_names(data_dir, file_type)
    print('Combine begining for ', str(len(img_dir)), ' images.....')
    dir_dict = get_same_img(img_dir, img_name)
    count = 0
    for key in dir_dict.keys():
        temp_label = np.zeros(shape=(w, h, c), dtype=np.uint8)
        dir_list = dir_dict[key]
        for item in dir_list:
            name_split = item.split('_')
            x_start = int(name_split[-4])
            x_end = int(name_split[-3])
            y_start = int(name_split[-2])
            y_end = int(name_split[-1].split('.')[0])
            img = Image.open(item)
            img = np.array(img)
            temp_label[x_start:x_end, y_start:y_end, :] = img

        img_name = key + '.' + out_type
        new_out_dir = out_dir + '/' + img_name

        label = Image.fromarray(temp_label)
        label.save(new_out_dir)
        # src_path = 'F:/带地理坐标.tif'  # 带地理坐标影像
        # assign_spatial_reference_byfile(src_path, new_out_dir)
        count += 1
        print('End of ' + str(count) + '/' + str(len(dir_dict)) + '...')
    print('Combine Finsh!')

    return 0


if __name__ == '__main__':
    ##### cut
    data_dir = 'D:/mmdataset/Nanjing_s2'
    out_dir = 'D:/mmdataset/dataset_cropping'
    file_type = ['tif']
    out_type = 'tif'
    cut_size = 512

    cut(data_dir, out_dir, file_type, out_type, cut_size)
    ##### combine
#    data_dir='F:/Level1/cut_960'
#    h=3072
#    w=1792
#    c=3
#    out_dir='F:/Level1'
#    out_type='tif'
#    file_type=['tif']
#    
#    combine(data_dir, w, h, c, out_dir, out_type, file_type)