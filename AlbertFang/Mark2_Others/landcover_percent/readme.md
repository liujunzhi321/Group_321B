# Readme

## 1 功能概述
本代码的功能实现的功能是：在点位缓冲区内土里利用数据。
## 2 数据准备
（1）土地利用数据， 栅格数据（.tif,...）
</br>
这里利用的是宫鹏老师生产的10m分辨率的土地利用数据，可以利用代码`downloadLCGoongpeng.py`生成所需数据的下载链接。在完成下载之后，数据可能需要拼接，这里提供了拼接的[方法](https://github.com/liujunzhi321/Group_321B/blob/main/AlbertFang/Mark2_Others/landcover_percent/merge_data.py)。
</br>
（2）点位数据，矢量数据（.shp）
</br>
如果提供的数据为矢量数据则可以直接使用，但是需是投影坐标，如Albers投影。若提供的数据为文本格式，如.xlsx，这里提供了转换的[方法](https://github.com/liujunzhi321/Group_321B/blob/main/AlbertFang/Mark2_Others/mk_features.py), 得到了会是矢量的点位数据。
## 3 制作过程
实现这一过程的主要代码为`landcover_percent.py`。包括制作缓冲区、计算土地利用比例，生成后的数据整理。