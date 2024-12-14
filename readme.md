打开anaconda，执行以下命令：
```python
# 创建虚拟环境
conda create -n checkerbot_gui python=3.8
# 进入虚拟环境
conda activate checkerbot_gui
# 通过cd进入到项目路径下
# 下载相关包
pip install -r requirements.txt
# 如果下载太慢，可执行下面命令：
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# 运行脚本
python test.py
```