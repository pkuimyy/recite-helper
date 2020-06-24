# recite-helper

使用腾讯tts api将文本转化为音频

## 依赖

```
pip install tencentcloud-sdk-python
```

## 注意

1. 使用这个项目的时候，请自行获取腾讯tts api的`SecretId`与`SecretKey`
2. tts api的文档为[文档链接](https://cloud.tencent.com/document/product/1073)

## 使用方法

1. 将要转化为音频的文本写入`./input/input.txt`
2. 进入`src`目录，运行`python ReciteHelper.py`
3. 进入`./output/`目录查看结果
