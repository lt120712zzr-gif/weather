# 天气数据分析可视化系统

基于 Django 的天气数据采集、存储、分析与可视化展示平台。支持多城市天气数据爬取、历史数据查询、数据可视化分析和天气预测功能。

## 📋 项目简介

本项目是一个完整的天气数据分析系统，主要功能包括：

- **数据采集**：自动爬取多个城市的历史天气数据
- **数据存储**：使用 Django ORM 进行数据持久化存储
- **数据查询**：支持按城市、日期、星期等多维度查询
- **数据可视化**：提供折线图、柱状图、地图、词云图等多种可视化方式
- **天气预测**：基于历史同期数据的简单天气预测算法

## ✨ 功能特性

### 1. 首页地图展示
- 可视化展示全国多城市的气温分布
- 支持按日期切换查看不同日期的气温数据
- 鼠标悬停查看详细信息

### 2. 详情信息查询
- 按城市查询详细天气数据
- 支持数据分页展示
- 表格化展示温度、天气、风向等信息

### 3. 数据可视化
- **月份气温统计**：展示不同城市某月份的日高温/日低温趋势
- **月份空气统计**：展示不同城市某月份的最高/最低/平均空气质量

### 4. 数据词云图
- 基于城市历史天气数据生成词云
- 支持多城市切换
- 爱心形状展示，直观呈现天气分布

### 5. 天气预测
- 基于历史同期数据的预测算法
- 预测未来7天天气
- 显示温度趋势图
- 自动考虑季节和日期因素

## 🛠️ 技术栈

- **后端框架**：Django 6.0
- **前端框架**：Bootstrap + jQuery
- **可视化库**：ECharts 5.4.3
- **数据采集**：Requests + lxml
- **数据库**：MySQL（使用 Django ORM）
- **数据处理**：Pandas

## 📦 安装依赖

```bash
pip install django
pip install requests
pip install lxml
pip install pandas
pip install pymysql
```

或使用 requirements.txt（如有）：

```bash
pip install -r requirements.txt
```

## 🚀 快速启动

### 1. 克隆项目

```bash
git clone https://github.com/你的用户名/你的仓库名.git
cd Wheater_DjangoProject
```

### 2. 配置数据库

#### 导入 SQL 文件

1. 下载并解压数据库文件：
   - 网盘链接：https://pan.baidu.com/s/1z10wQ1736YTliWGd-u8MJw
   - 提取码：`0712`

2. 创建数据库：
   ```sql
   CREATE DATABASE weatherdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. 导入数据：
   ```bash
   mysql -u root -p weatherdb < weatherdata2.sql
   ```


### 3. 启动项目

```bash
python manage.py runserver
```

### 4. 访问系统

打开浏览器访问：`http://127.0.0.1:8000`

## 📁 项目结构

```
Wheater_DjangoProject/
├── myApp/                    # 主应用目录
│   ├── models.py             # 数据模型
│   ├── views.py             # 视图函数
│   ├── urls.py              # URL 配置
│   └── admin.py            # 后台管理
├── templates/               # HTML 模板
│   ├── index.html          # 首页（地图展示）
│   ├── detailInfo.html      # 详情信息
│   ├── dataVisualization.html  # 数据可视化
│   ├── wordCloud.html      # 词云图
│   └── weatherForecast.html # 天气预测
├── spider/                 # 爬虫模块
│   ├── spiderCity.py       # 爬取城市列表
│   ├── spiderMain.py       # 爬取天气数据
│   ├── city.csv           # 城市数据
│   └── tempData.csv      # 临时数据文件
├── utils/                  # 工具模块
│   ├── getChartData.py     # 数据获取与处理
│   └── import_data.py     # 数据导入工具
├── static/                 # 静态资源
│   ├── css/              # 样式文件
│   ├── js/               # JavaScript 文件
│   └── picture/          # 图片资源
├── Wheater_DjangoProject/  # 项目配置
│   ├── settings.py        # 全局设置
│   └── urls.py          # 主路由配置
└── manage.py             # Django 管理脚本
```

## 🗄️ 数据模型

### User（用户）
- `id`：主键
- `username`：用户名
- `password`：密码
- `create_time`：创建时间

### WeatherInfo（天气信息）
- `city`：城市
- `date`：日期
- `weekDay`：星期
- `mastHeightDay`：日高温
- `mastSmallDay`：日低温
- `wearther`：天气状况
- `wind`：风向
- `windOrder`：风力
- `averageHeight`：月平均高温
- `averageSmall`：月平均低温
- `averageAir`：平均空气质量
- `mastAir`：最高空气质量
- `lostAir`：最低空气质量

### City（城市）
- `city`：城市名
- `url`：城市参数

## 📊 算法说明

### 天气预测算法

采用**历史同期对比法**：

1. 查找历史上相同月份和日期的天气数据
2. 计算同期平均温度
3. 统计历史同期天气类型频率
4. 选择出现频率最高的天气作为预测结果

**公式**：
```
预测温度 = 历史同期平均温度
预测天气 = 历史同期出现频率最高的天气
```

## 🔧 配置说明

### 数据库配置

编辑 `Wheater_DjangoProject/settings.py` 中的 `DATABASES` 配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '数据库名',
        'USER': '用户名',
        'PASSWORD': '密码',
        'HOST': '主机地址',
        'PORT': '端口',
    }
}
```

### 允许的主机

在生产环境，需要修改 `settings.py`：

```python
ALLOWED_HOSTS = ['你的域名', '你的IP地址']
```

## 📝 功能说明

### 数据爬虫

爬虫模块自动从 [历史天气网](https://lishi.tianqi.com) 获取天气数据：

- `spiderCity.py`：爬取支持的城市列表
- `spiderMain.py`：爬取指定城市的历史天气数据

### 数据可视化

使用 ECharts 实现多种可视化图表：

- **折线图**：温度趋势、空气质量趋势
- **柱状图**：平均温度对比、平均空气质量对比
- **地图**：全国气温分布
- **词云图**：天气类型分布

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件

## 📮 联系方式

如有问题，请提交 Issue 或联系项目维护者。

## 🙏 致谢

- [Django](https://www.djangoproject.com/) - Web 框架
- [ECharts](https://echarts.apache.org/) - 可视化库
- [历史天气网](https://lishi.tianqi.com/) - 数据来源
