import sys
import id_processing
import ml
import pandas as pd
import data_processing_functions
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
        [d_size, l_size] = id_processing.product_id_to_size(output)
        machine_size_type = ml.ml_on_machine_size((l_size, d_size))
        # print(machine_size_type[0])
        # print(machine_size_type[1])
        output = self.processing_id(output)
        if output[1] != "":  # if there are two popular status sequence
            machine_sequence1 = id_processing.machine_type(output[0])[:-1]
            machine_sequence2 = id_processing.machine_type(output[1])[:-1]
            if machine_sequence1 == machine_sequence2:  # if two most popular machine sequence are the same
                machine = data_processing_functions.machine_sequence_to_machine_name(
                    machine_sequence1, int(machine_size_type[0]), int(machine_size_type[1]))
                machine += "\n" + "Corresponding sequence:" + "\n" + \
                    data_processing_functions.status_to_usefulstatus(output[0])
            else:
                machine = data_processing_functions.machine_sequence_to_machine_name(
                    machine_sequence1, int(machine_size_type[0]), int(machine_size_type[1])) + "\n"
                machine += data_processing_functions.machine_sequence_to_machine_name(
                    machine_sequence2, int(machine_size_type[0]), int(machine_size_type[1]))
                machine += "\n" + "Corresponding sequence:" + "\n" + \
                    data_processing_functions.status_to_usefulstatus(output[0])
                machine += "\n" + \
                    data_processing_functions.status_to_usefulstatus(output[1])
        else:  # if there is only one status sequence
            machine_sequence1 = id_processing.machine_type(output[0])[:-1]
            machine = data_processing_functions.machine_sequence_to_machine_name(
                machine_sequence1, machine_size_type[0], machine_size_type[1])
            machine += "\n" + \
                data_processing_functions.status_to_usefulstatus(output[0])

        output = "The_two_most_popular_status_sequence: " + "\n" + output[0] + "\n" + output[1] + "\n" + "Machine_sequence: " + \
            "\n" + machine  # The final output

        QMessageBox.information(
            self,
            "status and machine type",
            output)  # print the output

    def processing_id(self, id) -> str:   # processing product_id into status_list
        output = id_processing.id_processing(id) + ml.ml_on_status(id)

        if output[-1] == "-":
            output = output[:-1]
        status_list = output.split("-")
        status_list = list(set(status_list))  # drop duplicates
        output = id_processing.time_order(status_list)
        return output


app = QApplication(sys.argv)
main = Mainwindow()
main.show()
sys.exit(app.exec_())
