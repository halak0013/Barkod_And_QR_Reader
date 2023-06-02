from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QSpacerItem, QSplitter, QPushButton, QMainWindow, QHBoxLayout, QWidget, QVBoxLayout, QSizePolicy


from src.ViedoWidgetc import VideoWidget, VideoThread
from src.OpenCvPro import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_widget = QWidget()
        self.layout = QVBoxLayout(self.main_widget)
        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout(self.right_widget)

        # Generate the splitter
        self.splitter = QSplitter()
        self.setWindowTitle("Barcode Reader")

        self.video_widget = VideoWidget(self)
        self.opcv_o = OpenCvPro()

        # Generate a QLabel
        self.label = QLabel("Barcode Data:", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(10, 10, 300, 30)

        self.video_thread = VideoThread(self.opcv_o.camera_capture())
        self.video_thread.frame_available.connect(self.process_frame)
        self.video_thread.start()

        self.add_right_side()
        self.add_to_splitte()  # Adding widgets to splitter
        self.layout.addWidget(self.splitter)
        self.setCentralWidget(self.main_widget)

    def add_right_side(self):
        self.s_vbox = QVBoxLayout()
        self.a_vbox = QVBoxLayout()
        self.lb_h_box = QHBoxLayout()  # Horizontal layout
        self.btn_v_box = QVBoxLayout()  # Vertical layout

        self.lb_s_name = QLabel("Name: ")
        self.lb_s_cost = QLabel("Cost: ")
        self.lb_s_code = QLabel("Code: ")

        self.lb_name = QLabel("Null")
        self.lb_cost = QLabel("Null")
        self.lb_code = QLabel("Null")

        self.btn_add = QPushButton("Add")
        self.btn_delete = QPushButton("Delete")
        self.btn_update = QPushButton("Update")

        self.btn_add.clicked.connect(self.btn_add_clicked)
        self.btn_delete.clicked.connect(self.btn_delete_clicked)
        self.btn_update.clicked.connect(self.bth_update_clicked)

        self.s_vbox.addWidget(self.lb_s_name)
        self.s_vbox.addWidget(self.lb_s_cost)
        self.s_vbox.addWidget(self.lb_s_code)
        self.s_vbox.stretch(1)
        
        self.a_vbox.addWidget(self.lb_name)
        self.a_vbox.addWidget(self.lb_cost)
        self.a_vbox.addWidget(self.lb_code)

        self.lb_h_box.addLayout(self.s_vbox)
        self.lb_h_box.addLayout(self.a_vbox)

        self.btn_v_box.addWidget(self.btn_add)
        self.btn_v_box.addWidget(self.btn_delete)
        self.btn_v_box.addWidget(self.btn_update)
        self.btn_v_box.stretch(10)

        self.right_layout.addLayout(self.lb_h_box)
        #self.right_layout.addSpacing(20)
        self.right_layout.addLayout(self.btn_v_box)

    def add_to_splitte(self):
        self.splitter.addWidget(self.video_widget)
        self.splitter.addWidget(self.right_widget)

    def process_frame(self, frame):
        self.opcv_o.barcode_read(frame, (0, 0, 255))
        self.video_widget.show_frame(frame)

    def btn_add_clicked(self):
        print("ekle")

    def btn_delete_clicked(self):
        print("sil")

    def bth_update_clicked(self):
        print("güncelle")



app = QApplication([])
main_window = MainWindow()
main_window.show()
app.exec()