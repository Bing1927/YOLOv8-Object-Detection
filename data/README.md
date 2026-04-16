# Pascal VOC 2007 数据集说明

当前目录是存放 Pascal VOC 数据集流水线的标准根目录。以下是针对组成员的说明：

## 1. 结构说明

执行完成员 3 (如果脚本是由成员 3 代劳运行的) 的流水线后，本目录将会如下分布：
- `VOCdevkit/`: 原始下载的文件和解压缩后的 XML 结构。
- `raw_tar/`: VOC 原版的 tar 包存放处（可以随时删除省空间）。
- `yolo_format/`: **这就是模型需要的最终目录**！里面包含了 `images` 和 `labels` 两个子文件夹，均被分为 `train` 和 `val` 结构。

## 2. 怎么跑转换流水线？(Member 3 专属操作)

请按照顺序在控制台 `YOLOv8-Object-Detection` 根目录下执行：
1. `python scripts/download_voc.py` （自动拉取大约 450MB 的压缩包并解压）
2. `python scripts/voc2yolo.py` （将 VOCdevkit 里的 xml 转成 yolo_format 里的 txt）
3. `python scripts/validate_yolo.py` （抽取验证集画框，生成的校验图在 `results/validation_samples/` 检查坐标有无偏移）

## 3. 模型同学如何使用？(Member 4 & 5 专属操作)

你不需要理会那些凌乱的数据包。在进行 YOLOv8 训练时，直接挂载我为你写好的 `pascal_voc.yaml` 即可。

示例命令：
```bash
yolo task=detect mode=train model=yolov8n.pt data=data/pascal_voc.yaml epochs=50 imgsz=640 batch=16
```
> [!NOTE]
> 运行以上命令时，请确保你的终端是在 `YOLOv8-Object-Detection` 根目录下，由 YAML 自己处理相对路径。
