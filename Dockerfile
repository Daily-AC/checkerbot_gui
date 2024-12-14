# FROM ubuntu:22.04

# RUN apt-get update
# RUN apt install -y libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6
# RUN apt-get install -y wget
# RUN wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
# RUN sh -c '/bin/echo -e "\nyes\n\nyes" | sh Anaconda3-2022.10-Linux-x86_64.sh'
# RUN echo "export PATH=~/anaconda3/bin:$PATH" >> ~/.bashrc
# RUN echo "source ~/anaconda3/bin/activate" >> ~/.bashrc
# RUN /bin/bash -c "source ~/.bashrc"
# RUN bash ~/anaconda3/etc/profile.d/conda.sh 
# ENV PATH ~/anaconda3/bin:$PATH
# RUN conda create -n checkerbot_gui -y python=3.8
# RUN conda activate checkerbot_gui
# RUN mkdir ~/checkerbot_gui
# RUN cd ~/checkerbot_gui
# COPY . ~/checkerbot_gui
# RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# RUN export QT_QPA_PLATFORM=xcb
# RUN apt-get install -y libxcb1 libxcb-util1 libx11-xcb1 libxrender1 libxrandr2 libxi6
# RUN apt install -y libxcb-*

# CMD ["python", "test.py"]

FROM ubuntu:22.04

# 基础系统更新与必要依赖安装
RUN apt-get update && apt-get install -y \
    libglib2.0-dev \
    wget \
    libgl1-mesa-glx \
    libegl1-mesa \
    libxrandr2 \
    libxss1 \
    libxcursor1 \
    libxcomposite1 \
    libasound2 \
    libxi6 \
    libxtst6 \
    libxcb1 \
    libxcb-util1 \
    libx11-xcb1 \
    libxrender1 \
    libxrandr2 \
    libxi6 \
    && apt-get clean

# 下载并安装 Anaconda
RUN wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh -O /tmp/Anaconda3.sh && \
    bash /tmp/Anaconda3.sh -b -p /opt/anaconda && \
    rm -f /tmp/Anaconda3.sh

# 配置 PATH 环境变量
ENV PATH="/opt/anaconda/bin:$PATH"

# 创建 conda 虚拟环境
RUN conda create -n checkerbot_gui -y python=3.8 && \
    conda clean -a

# 激活环境并安装依赖
COPY requirements.txt /opt/checkerbot_gui/requirements.txt
RUN /bin/bash -c "source activate checkerbot_gui && pip install -r /opt/checkerbot_gui/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple"

# 复制项目文件
COPY . /opt/checkerbot_gui

# 设置工作目录
WORKDIR /opt/checkerbot_gui

# 配置运行时环境变量
ENV QT_QPA_PLATFORM=xcb

RUN apt-get install -y openssh-server \
    xorg

# 启动容器时运行的命令
CMD ["/bin/bash", "-c", "source activate checkerbot_gui && python test.py"]
