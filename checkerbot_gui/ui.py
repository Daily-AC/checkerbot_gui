import time
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLineEdit, QFileDialog, QLabel
from PyQt5.QtCore import Qt
from checkerbot_gui.checker import send_chat_request, get_chat_messages, change_api_token, change_proxy
from checkerbot_gui.utils import extract_text_from_word

class CheckerBotApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("checkerbot")
        self.setGeometry(100, 100, 800, 600)
        
        self.chat_history = []  # 用于保存聊天记录
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 聊天记录框
        self.chat_box = QTextEdit(self)
        self.chat_box.setReadOnly(True)
        layout.addWidget(self.chat_box)

        # 输入框
        self.input_line = QLineEdit(self)
        self.input_line.setPlaceholderText("输入问题...")
        layout.addWidget(self.input_line)

        # 上传文件按钮
        self.upload_button = QPushButton("上传文本或Word文件", self)
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button)

        # 查询按钮
        self.query_button = QPushButton("查询", self)
        self.query_button.clicked.connect(self.query_chat)
        layout.addWidget(self.query_button)

        # 日志框
        self.log_box = QTextEdit(self)
        self.log_box.setReadOnly(True)
        layout.addWidget(self.log_box)

        # 代理设置
        self.proxy_label = QLabel("代理地址:", self)
        self.proxy_input = QLineEdit(self)
        self.proxy_input.setPlaceholderText("如: http://127.0.0.1:8080")
        self.proxy_button = QPushButton("设置代理", self)
        self.proxy_button.clicked.connect(self.set_proxy)

        # 代理设置布局
        proxy_layout = QHBoxLayout()
        proxy_layout.addWidget(self.proxy_label)
        proxy_layout.addWidget(self.proxy_input)
        proxy_layout.addWidget(self.proxy_button)

        layout.addLayout(proxy_layout)

        # token设置
        self.api_token_label = QLabel("token:", self)
        self.api_token_input = QLineEdit(self)
        self.api_token_input.setPlaceholderText("如: pat_yAx5UFur58gr8ILl6aNbWNJeXlA4gxqbTDm1S3FvtOzybUOPXatiYI4NiqPn9ot8")
        self.api_token_input.setText("pat_yAx5UFur58gr8ILl6aNbWNJeXlA4gxqbTDm1S3FvtOzybUOPXatiYI4NiqPn9ot9")
        self.api_token_button = QPushButton("设置token", self)
        self.api_token_button.clicked.connect(self.set_api_token)

        # token设置布局
        api_token_layout = QHBoxLayout()
        api_token_layout.addWidget(self.api_token_label)
        api_token_layout.addWidget(self.api_token_input)
        api_token_layout.addWidget(self.api_token_button)

        layout.addLayout(api_token_layout)

        self.setLayout(layout)

    def upload_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "Text Files (*.txt);;Word Files (*.docx);;All Files (*)")
        if file_name:
            if file_name.endswith(".txt"):
                try:
                    with open(file_name, "r", encoding="utf-8") as file:
                        content = file.read()
                        self.input_line.setText(content)
                        self.log_box.append(f"已加载文件: {file_name}")
                except Exception as e:
                    self.log_box.append(f"文件加载失败: {str(e)}")
            elif file_name.endswith(".docx"):
                try:
                    content = extract_text_from_word(file_name)
                    self.input_line.setText(content)
                    self.log_box.append(f"已加载Word文件: {file_name}")
                except Exception as e:
                    self.log_box.append(f"Word文件加载失败: {str(e)}")

    def set_proxy(self):
        proxy_address = self.proxy_input.text()
        if proxy_address:
            change_proxy(proxy_address)
            self.log_box.append(f"已设置代理: {proxy_address}")
        else:
            change_proxy(proxy_address)
            self.log_box.append("已取消代理设置")
    
    def set_api_token(self):
        api_token = self.api_token_input.text()
        if api_token:
            change_api_token(api_token=api_token)
            self.log_box.append(f"已设置token")
            self.api_token_input.clear()
        else:
            change_api_token(api_token=None)
            self.log_box.append("已取消token设置，目前无token")

    def query_chat(self):
        question = self.input_line.text()
        if not question:
            self.log_box.append("请输入问题或上传文件！")
            return

        # 显示用户的输入
        self.chat_history.append(f"用户: {question}")
        self.chat_box.append(f"用户: {question}")
        self.input_line.clear()

        try:
            # 发送聊天请求
            chat_response = send_chat_request(question)
            
            if "code" in chat_response and chat_response["code"] == 0 and "data" in chat_response:
                chat_id = chat_response["data"].get("id")
                conversation_id = chat_response["data"].get("conversation_id")
                
                if chat_id and conversation_id:
                    # 尝试获取聊天消息，最多重试5次
                    for attempt in range(5):
                        self.log_box.append(f"尝试获取消息，第 {attempt + 1} 次")
                        messages = get_chat_messages(chat_id, conversation_id)
                        
                        if "code" in messages and messages["code"] == 0 and "data" in messages and messages["data"]:
                            for message in messages["data"]:
                                if message["role"] == "assistant" and message["type"] == "answer":
                                    answer = message['content']
                                    self.chat_history.append(f"智能体: {answer}")
                                    self.chat_box.append(f"智能体: {answer}")
                                    return
                            self.log_box.append("未找到智能体的回答，等待5秒后重试")
                        else:
                            self.log_box.append("获取聊天消息失败或返回格式不正确，等待5秒后重试")
                        
                        time.sleep(5)  # 等待5秒后重试
                    
                    self.log_box.append("所有重试都失败，无法获取智能体的回答")
                else:
                    self.log_box.append("chat_id 或 conversation_id 未在响应中找到")
            else:
                self.log_box.append("发送聊天请求失败或返回格式不正确")
        
        except Exception as e:
            self.log_box.append(f"发生错误: {str(e)}")
            self.log_box.append("继续运行程序。")
