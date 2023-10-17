# Sat2samples
A collection of tools to easliy acquire and crop large-scale satellite imagery into samples for machine/deep learning.

**Attention**: Make sure you have access to Google Earth Engine API.
## 1. Description

 &emsp; This is an easy-to-use project for acquiring and cutting **large-scale satellite imagery** into samples for machine/deep learning. This project is mainly based on `geemap`, `gdal`, `colab` and `QGIS desktop`.

## 2. Usage
- Step 1: Prepare your region of interest (**ROI**) shapefiles. If your ROI is located in China, please try this link: [Get shapefile of ROI](http://datav.aliyun.com/portal/school/atlas/area_selector).
  [![2023-10-17-16-51-31.png](https://i.postimg.cc/tT0nXBfM/2023-10-17-16-51-31.png)](https://postimg.cc/qtLvwxps)
- Step 2: Use QGIS desktop to create the grid of your ROI. If you don't familar with this processing, please explore more in this link: [QGIS operation](https://zhuanlan.zhihu.com/p/374960641).
[![2023-10-17-16-53-44.png](https://i.postimg.cc/BvP19rhF/2023-10-17-16-53-44.png)](https://postimg.cc/VS1NXVPs)
- Step 3: Upload the shapefile of the grids followed by last step to your GEE assets.
- Step 4: Use the `notebooks` in this project to download  **Sentinel 1/2** satelite images with preprocessing.
- Step 5: Use the `.py` files in this project to crop the satelite images to samples.

## 3. Contact 
&emsp; If you encounter any problem in using the Sat2samples or have any feedback, please contact:
-  E-mail: 2309162135@geemail.one

## 4. Reference
- GEE: [Awesome-GEE](https://github.com/opengeos/Awesome-GEE).
- Sentinel 1: [Google-Sentinel-1](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD#description).
- Sentinel 2: [Google-Sentinel-2](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED).
- Mapshaper: [Mapshaper](https://mapshaper.org/).
