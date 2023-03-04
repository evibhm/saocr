# 集成OCR服务

本项目基于TencentOCR API 和 PaddleOCR 开发，集成了两种API的使用方法，并在Docker中部署，部署过程简单方便。

## 配置腾讯云密钥

修改目录`ocrapi/config.example.py` 修改完内容后，将文件名改为`config.py`

## 编译Docker镜像

如果你没有安装Docker，请参考[官方文档](https://docs.docker.com/engine/install/)

在本项目根目录，使用以下命令就可以编译镜像

```bash
docker build -t saocr .
```

此命令会自动下载相关依赖，并且在任何环境下都不会报错，不过，可能需要等待一会......


## 启动Docker容器

使用以下命令

```bash
docker run -d -p 8000:8000 saocr
```

至此，集成OCR服务API部署完成。