from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel,QLineEdit,QMessageBox, QSlider, QSplitter, QPushButton, QMainWindow, QHBoxLayout, QWidget, QVBoxLayout, QSizePolicy


from src.ViedoWidgetc import VideoWidget, VideoThread
from src.OpenCvPro import *
from src.dbmanage import *
from src.QrGenerate import QRCode
from src.Barcode_generator import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dbObject=dbmanage()
        self.dbObject.createTable("productTbl1")
        self.main_widget = QWidget()
        self.layout = QVBoxLayout(self.main_widget)
        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout(self.right_widget)
        self.old_id=""
        self.color=(0, 0, 255)
        self.product=""
        self.tot_price=0

        # Generate the splitter
        self.splitter = QSplitter()
        self.setWindowTitle("Barcode Reader")

        self.video_widget = VideoWidget(self)
        self.opcv_o = OpenCvPro()
        self.qr_generater=QRCode()

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
        self.lb_s_price = QLabel("Price: ")
        self.lb_s_id = QLabel("Id: ")
        
        self.lb_reuslt=QLabel()
        self.lb_total=QLabel()
        

        self.lb_name = QLineEdit()
        self.lb_price = QLineEdit()
        self.lb_id = QLineEdit()
        
        self.lb_name.setPlaceholderText("Type value")
        self.lb_price.setPlaceholderText("Type value")
        self.lb_id.setPlaceholderText("Type value")
        
        self.lb_name.setMinimumWidth(200)
        self.lb_price.setMinimumWidth(200)
        self.lb_id.setMinimumWidth(200)

        self.btn_add = QPushButton("Add")
        self.btn_delete = QPushButton("Delete")
        self.btn_update = QPushButton("Update")
        self.btn_get_qr = QPushButton("Get OR Code")
        self.btn_get_barcode = QPushButton("Get Barcode")
        
        
        self.sldr_resol=QSlider()

        self.btn_add.clicked.connect(self.btn_add_clicked)
        self.btn_delete.clicked.connect(self.btn_delete_clicked)
        self.btn_update.clicked.connect(self.bth_update_clicked)
        self.btn_get_qr.clicked.connect(self.bth_btn_get_qrf)
        self.btn_get_barcode.clicked.connect(self.btn_get_barcodef)
        
        


        self.s_vbox.addWidget(self.lb_s_name)
        self.s_vbox.addWidget(self.lb_s_price)
        self.s_vbox.addWidget(self.lb_s_id)
        self.s_vbox.stretch(1)
        
        self.a_vbox.addWidget(self.lb_name)
        self.a_vbox.addWidget(self.lb_price)
        self.a_vbox.addWidget(self.lb_id)

        self.lb_h_box.addLayout(self.s_vbox)
        self.lb_h_box.addLayout(self.a_vbox)
        
        self.sldr_resol.setOrientation(Qt.Orientation.Horizontal)
        self.sldr_resol.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.sldr_resol.setTickInterval(2)
        self.sldr_resol.setMinimum(1)
        self.sldr_resol.setMaximum(10)
        self.sldr_resol.valueChanged.connect(self.changeSlide)

        self.btn_v_box.addWidget(self.lb_reuslt)
        self.btn_v_box.addWidget(self.lb_total)
        self.btn_v_box.addWidget(self.sldr_resol)
        self.btn_v_box.addWidget(self.btn_add)
        self.btn_v_box.addWidget(self.btn_delete)
        self.btn_v_box.addWidget(self.btn_update)
        self.btn_v_box.addWidget(self.btn_get_qr)
        self.btn_v_box.addWidget(self.btn_get_barcode)
        self.btn_v_box.stretch(10)

        self.right_layout.addLayout(self.lb_h_box)
        #self.right_layout.addSpacing(20)
        self.right_layout.addLayout(self.btn_v_box)

    def btn_get_barcodef(self):
        id_ = self.lb_id.text()
        if self.dbObject.isThere("productTbl1",id_):
            price = self.dbObject.get("productTbl1",id_,"price")
            name = self.dbObject.get("productTbl1",id_,"name")
            vals=str(id_)
            print("val "+ vals)
            generate_barcode(vals,"code128",f"image/{vals}")
            self.opcv_o.show_image(f"image/{vals}.png")
        else:
            dialog=QMessageBox.warning(self,"Warning",f"There is no such a product like that id = {id_} in database.\nYou can add it")
            

    def bth_btn_get_qrf(self):
        id_ = self.lb_id.text()
        if self.dbObject.isThere("productTbl1",id_):
            price = self.dbObject.get("productTbl1",id_,"price")
            name = self.dbObject.get("productTbl1",id_,"name")
            vals=str(id_)
            print("val "+ vals)
            self.qr_generater.generate_qr_code(vals)
            self.opcv_o.show_image(f"image/{vals}.png")
        else:
            dialog=QMessageBox.warning(self,"Warning",f"There is no such a product like that id = {id_} in database.\nYou can add it")
            

    def add_to_splitte(self):
        self.splitter.addWidget(self.video_widget)
        self.splitter.addWidget(self.right_widget)

    def process_frame(self, frame):
        self.opcv_o.barcode_read(frame, self.color)
        self.video_widget.show_frame(frame)
        try:
            id_=self.opcv_o.data.split()[0]
            if self.old_id != id_:
                self.old_id=id_
                if self.dbObject.isThere("productTbl1",id_):
                    self.color=(0, 255, 0)
                    #print("name",self.opcv_o.data.split()[1],"price",self.opcv_o.data.split()[2],"id",self.opcv_o.data.split()[0])
                    name=self.dbObject.get("productTbl1",id_,"name")
                    price=self.dbObject.get("productTbl1",id_,"price")
                    self.lb_name.setText(name)
                    self.lb_price.setText(str(price))
                    self.lb_id.setText(id_)
                    self.add_to_basket(price,name+ " " + str(price))
                else:
                    #print("burada")
                    self.color=(0, 0, 255)
                    self.lb_id.setText(str(id_))
                    self.lb_price.setText("")
                    self.lb_name.setText("")
                    dialog=QMessageBox.warning(self,"Warning",f"There is no such a product like that id = {id_} in database.\nYou can add it")
        except Exception as e:
            #print(e)
            pass
    def add_to_basket(self,price,data):
        self.product+="\n"+data
        self.tot_price+=price
        
        self.lb_reuslt.setText("Products Cart \n" + self.product)
        self.lb_total.setText("Total Price\n"+str(self.tot_price))

    def btn_add_clicked(self):
        self.qr_generater.generate_qr_code((self.lb_id.text()))
        self.dbObject.addProduct("productTbl1", self.lb_id.text(), self.lb_name.text(),self.lb_price.text())
        
        print("ekle")
        

    def btn_delete_clicked(self):
        self.dbObject.deleteProduct("productTbl1",self.lb_id.text())
        self.lb_name.setText("")
        self.lb_price.setText("")
        self.lb_id.setText("")
        print("sil")

    def bth_update_clicked(self):
        
        self.dbObject.updateProduct("productTbl1",self.lb_id.text(), self.lb_name.text(),self.lb_price.text())  
        print("güncelle")
    
    def changeSlide(self):
        print(str(self.sldr_resol.value()))
        self.opcv_o.thickness=self.sldr_resol.value()



app = QApplication([])
main_window = MainWindow()
main_window.show()
app.exec()