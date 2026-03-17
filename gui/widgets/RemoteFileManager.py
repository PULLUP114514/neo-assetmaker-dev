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

enableDebug = True

# 👂？ 我没对象 所以创建一个 :D
class FileItem:
    def __init__(self, name, type_):
        self.name = name
        self.type = type_

class RemoteFileManagerDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("远程文件管理")
        self.resize(600, 400)

        # 主布局
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

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
    
    def _on_file_delete_clicked(self, filename):
        print(f"按钮点击: {filename}")
        return
    

    def _on_file_download_clicked(self, filename):
        print(f"按钮点击: {filename}")
        return
    
    def _on_upload(self):
        return

    def _on_refresh(self):
        return




if __name__ == "__main__" and enableDebug == True:
    app = QApplication(sys.argv)
    dlg = RemoteFileManagerDialog()
    dlg.show()
    sys.exit(app.exec())