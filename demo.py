import sys
import id_processing
import ml
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Mainwindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle("This is a demo")
        prod_id = QLabel(u"product_id")

        self.prod_idEdit = QLineEdit()  # setting LineEdit

        grid = QGridLayout()

        grid.addWidget(prod_id, 1, 0)
        grid.addWidget(self.prod_idEdit, 1, 1)

        self.ok = QPushButton(u"run")  # setting button
        grid.addWidget(self.ok, 5, 0)

        self.setLayout(grid)

        self.resize(500, 400)
        self.ok.clicked.connect(self.show_status)

    def show_status(self):
        output = self.prod_idEdit.text()
        output = self.processing_id(output)
        if output[1] != "":
            machine = id_processing.machine_type(output[0]) + "\n" + id_processing.machine_type(output[1])
        else:
            machine = id_processing.machine_type(output[0])
        output = "Two_status_sequence: " + output[0] + "\n" + output[1] + "\n" + "Machine_sequence: " + "\n" + machine


        QMessageBox.information(self, "status and machine type", output)  # print the output

    def processing_id(self, id):  # processing product_id
        output = id_processing.id_processing(id) + ml.ml_output(id)
        if output[-1] == "-":
            output = output[:-1]
        status_list = output.split("-")
        status_list = list(set(status_list))  # drop duplicates
        output = id_processing.time_order(status_list)
        #output = id_processing.machine_type(output)
        return output

    # def on_ok_clicked(self):
    #	QMessageBox.information(self,"sad","output")


app = QApplication(sys.argv)
main = Mainwindow()
main.show()
sys.exit(app.exec_())
