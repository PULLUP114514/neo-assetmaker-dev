from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QScrollArea, QWidget, QListWidget,
    QListWidgetItem, QLabel, QPushButton, QHBoxLayout, QApplication
)
from PyQt6.QtCore import Qt
import sys
from qfluentwidgets import (
    SimpleCardWidget,
    SubtitleLabel, StrongBodyLabel, CaptionLabel,
    PrimaryPushButton, PushButton,
    ProgressBar, ListWidget, PlainTextEdit,
    FluentIcon, InfoBar, InfoBarPosition,
    setCustomStyleSheet,
)
from core import sshOperation
import paramiko
from scp import SCPClient
import logging
logger = logging.getLogger(__name__)

# 👂？ 我没对象 所以创建一个 :D
class FileItem:
    def __init__(self, name, type_):
        self.name = name
        self.type = type_

class RemoteFileManagerDialog(QDialog):
    def __init__(self, parent, mainwindow, sshIp, sshPort, sshUser, sshPassword, sshDefaultFolder):
        super().__init__()
        self.main_window = mainwindow
        self.host = sshIp
        self.port = sshPort
        self.sshUser = sshUser
        self.sshPassword = sshPassword
        self.sshDefaultFolder = sshDefaultFolder

        self.setWindowTitle("远程文件管理")
        self.resize(600, 400)

        # 主布局
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)


        # 顶部路径栏
        self.topPathGrid = QWidget()
        self.topPathLayout = QHBoxLayout(self.topPathGrid)
        self.topPathLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.addWidget(self.topPathGrid, 0, Qt.AlignmentFlag.AlignTop)

        # 路径
        self.lb_currentPathlb = QLabel("当前位置：")
        self.topPathLayout.addWidget(self.lb_currentPathlb)
        
        self.lb_currentPath = QLabel("当前12312312")
        self.topPathLayout.addWidget(self.lb_currentPath)

        # 挤占右边空间
        self.topPathLayout.addStretch()  

        # 文件浏览器滚动区域
        self.fileWarpper = QScrollArea()
        self.fileWarpper.setWidgetResizable(True)
        self.mainLayout.addWidget(self.fileWarpper)

        # 容器
        self.container = QWidget()
        self.containerLayout = QVBoxLayout(self.container)
        self.containerLayout.setSpacing(10)
        self.containerLayout.setContentsMargins(10, 10, 10, 10)
        self.fileWarpper.setWidget(self.container)

        # 列表控件
        self.fileManagerList = QListWidget()
        self.fileManagerList.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        setCustomStyleSheet(
            self.fileManagerList,
            "ListWidget { border: none; background: transparent; }",
            "ListWidget { border: none; background: transparent; }",
        )
        self.containerLayout.addWidget(self.fileManagerList)

        # 底部工具栏
        self.buttomGrid = QWidget()
        self.buttomLayout = QHBoxLayout(self.buttomGrid)
        self.buttomLayout.setContentsMargins(10, 10, 10, 10)
        self.containerLayout.addWidget(self.buttomGrid)

        # 挤占左边空间
        self.buttomLayout.addStretch()  

        buttonWidth = 150

        self.btn_goParentFolder = PushButton("上一级")
        self.btn_goParentFolder.setIcon(FluentIcon.UP)
        self.btn_goParentFolder.setMinimumWidth(buttonWidth)
        self.btn_goParentFolder.setContentsMargins(10, 10, 10, 10)
        self.btn_goParentFolder.clicked.connect(self._on_refresh)
        self.buttomLayout.addWidget(self.btn_goParentFolder, 0, Qt.AlignmentFlag.AlignRight)

        self.btn_refresh = PushButton("刷新")
        self.btn_refresh.setIcon(FluentIcon.UPDATE)
        self.btn_refresh.setMinimumWidth(buttonWidth)
        self.btn_refresh.setContentsMargins(10, 10, 10, 10)
        self.btn_refresh.clicked.connect(self._on_refresh)
        self.buttomLayout.addWidget(self.btn_refresh, 0, Qt.AlignmentFlag.AlignRight)

        self.btn_uploadFile = PushButton("上传")
        self.btn_uploadFile.setIcon(FluentIcon.SEND)
        self.btn_uploadFile.setMinimumWidth(buttonWidth)
        self.btn_uploadFile.setContentsMargins(10, 10, 10, 10)
        self.btn_uploadFile.clicked.connect(self._on_upload)
        self.buttomLayout.addWidget(self.btn_uploadFile, 0, Qt.AlignmentFlag.AlignRight)


        # 生成大量列表项
        self.LoadFiles()

    def LoadFiles(self):
        for i in range(10):  # 示例10个文件
            filename = f"示例文件_{i}.txt"
            
            item_widget = QWidget()
            layout = QHBoxLayout(item_widget)
            layout.setContentsMargins(10, 10, 10, 10)


            label = CaptionLabel(filename)
            layout.addWidget(label, 1, Qt.AlignmentFlag.AlignLeft)

            btn_Delete = PushButton("删除")
            btn_Delete.setIcon(FluentIcon.DELETE)
            layout.addWidget(btn_Delete, 0, Qt.AlignmentFlag.AlignRight)
            btn_Delete.clicked.connect(lambda _, f=filename: self._on_file_delete_clicked(f))

            btn_Download = PushButton("下载")
            btn_Download.setIcon(FluentIcon.DOWNLOAD)
            layout.addWidget(btn_Download, 0, Qt.AlignmentFlag.AlignRight)
            btn_Download.clicked.connect(lambda _, f=filename: self._on_file_download_clicked(f))

            list_item = QListWidgetItem(self.fileManagerList)
            list_item.setSizeHint(item_widget.sizeHint())
            self.fileManagerList.addItem(list_item)
            self.fileManagerList.setItemWidget(list_item, item_widget)
    
    def StartSSH(self) -> paramiko.SSHClient:
        ssh = paramiko.SSHClient()
        ssh.connect(host = self.host,
                    port = self.port,
                    username = self.sshUser, 
                    password = self.sshPassword,
                    timeout = 10, 
                    banner_timeout = 10, 
                    auth_timeout = 10)
        return ssh

    def _on_file_delete_clicked(self, filename):
        try:
            ssh = self.StartSSH()

            # 此处需要拼接路径


            sshOperation.DelRemoteFile(ssh, filename)
        except Exception as e:
            logger.error(f"刷新失败{e}")
        return

    def _on_file_download_clicked(self, filename):
        print(f"按钮点击: {filename}")
        return
    
    def _on_upload(self):
        return

    def _on_refresh(self):
        try:
            ssh = self.StartSSH()
            fileList = self.getFolder(ssh)
        except Exception as e:
            logger.error(f"刷新失败{e}")
        return

    def CalcCurrentPath(self) -> str:
        
        return ""
    
    # def getFolder(self, ssh : ) -> list:

    #     return [
    #         FileItem("file", "folder")
    #     ]
