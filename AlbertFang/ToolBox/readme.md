# readme
> 一些可能会用到的实用的、可能会用到的小工具代码
## 1 工具介绍
### 1.1 SiteWithEnvs.py:
  - 简述：/t
    将站点数据所在区域内的湖泊属性，添加到站点数据中，具体使用的方法是`lake_with_envs = gpd.sjoin(lakeDOC_data, lake_data, how='left', op='within')`
  - 来源：/t
    在进行湖泊DOC分析的过程中，需要将提取的湖泊统计属性（面积、降雨、辐射等）合并到DOC点数据中去。
    
