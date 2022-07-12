import math
import os
import sys
from platform import uname

import psutil
from PyQt5 import QtWidgets
from PyQt5.QtGui import *

import main_win


class ExampleApp(QtWidgets.QMainWindow, main_win.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.butReceive.clicked.connect(self.get_info)  # Выполнить функцию get_info
                                                            # при нажатии кнопки
        self.le_Mb.editingFinished.connect(self.change_leMB)
        self.le_Gb.editingFinished.connect(self.change_leGB)
        self.butGetBigFiles.clicked.connect(self.GetBigFiles)

        self.le_Mb_2.editingFinished.connect(self.change_leMB_2)
        self.le_Gb_2.editingFinished.connect(self.change_leGB_2)
        self.butGetBigFolders.clicked.connect(self.GetBigFolders)

        self.but_GetDir.clicked.connect(self.getDirectory)
        self.but_GetDir_2.clicked.connect(self.getDirectory_2)
        
    def getDirectory(self):
        dirlist = QtWidgets.QFileDialog.getExistingDirectory(self,"Выбрать папку",".")
        self.le_PuthDir.setText(dirlist)

    def getDirectory_2(self):
        dirlist = QtWidgets.QFileDialog.getExistingDirectory(self,"Выбрать папку",".")
        self.le_PuthDir_2.setText(dirlist)

    def GetAnInteger(self, fl):
        x = fl.find(".")
        for i in range(0, len(fl), x):
            return fl[i:i+x]

    def change_leMB(self):
        # print (round(int(self.le_Mb.text()) / 1024, 2))
        if self.le_Mb.text().find(".") <= 0:
            if int(self.le_Mb.text()) > 0:
                self.le_Gb.setText(str(round(int(self.le_Mb.text()) / 1024, 2)))
            else:
                self.le_Gb.setText("0")
        else:
            celMb = int(self.GetAnInteger(self.le_Mb.text()))
            self.le_Mb.setText(str(celMb))
            self.le_Gb.setText(str(round(celMb / 1024, 2)))
    
    def change_leGB(self):
        # print (self.le_Gb.text())
        if self.le_Gb.text().find(".") <= 0:
            if int(self.le_Gb.text()) > 0:
                self.le_Mb.setText(str(round(int(self.le_Gb.text()) * 1024, 2)))
            else:
                self.le_Mb.setText("0")
        else:
            celGb = int(self.GetAnInteger(self.le_Gb.text()))
            self.le_Gb.setText(str(celGb))
            self.le_Mb.setText(str(round(celGb * 1024, 2)))

    def change_leMB_2(self):
        # print (round(int(self.le_Mb.text()) / 1024, 2))
        if self.le_Mb_2.text().find(".") <= 0:
            if int(self.le_Mb_2.text()) > 0:
                self.le_Gb_2.setText(str(round(int(self.le_Mb_2.text()) / 1024, 2)))
            else:
                self.le_Gb_2.setText("0")
        else:
            celMb = int(self.GetAnInteger(self.le_Mb_2.text()))
            self.le_Mb_2.setText(str(celMb))
            self.le_Gb_2.setText(str(round(celMb / 1024, 2)))
    
    def change_leGB_2(self):
        # print (self.le_Gb.text())
        if self.le_Gb_2.text().find(".") <= 0:
            if int(self.le_Gb_2.text()) > 0:
                self.le_Mb_2.setText(str(round(int(self.le_Gb_2.text()) * 1024, 2)))
            else:
                self.le_Mb_2.setText("0")
        else:
            celGb = int(self.GetAnInteger(self.le_Gb_2.text()))
            self.le_Gb_2.setText(str(celGb))
            self.le_Mb_2.setText(str(round(celGb * 1024, 2)))
            
    def convert_size(self, size_bytes):
        # print (size_bytes)
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def GetBigFiles(self):
        # var = self.tableWidget_BigFiles.set
        if self.le_Mb.text() == "":
            if self.le_Gb.text() != "":
                self.le_Mb.setText(str(round(int(self.le_Gb.text()) * 1024, 2)))

        # if self.tableWidget_BigFiles.rowCount() > 0:
        #     self.tableWidget_BigFiles.remo.clear()
        for i in range(self.tableWidget_BigFiles.rowCount(), -1, -1):
            self.tableWidget_BigFiles.removeRow(i)

        path = os.path.abspath(self.le_PuthDir.text())
        max_size = (int(round(int(self.le_Mb.text()))) * 1024) * 1024
        for folder, subfolders, files in os.walk(path):
            for file in files:
                # print(folder, file)
                if not os.path.islink(file):
                    if os.path.exists( os.path.join( folder, file ) ):
                        size = os.stat(os.path.join( folder, file  )).st_size
          
                        if size>max_size:
                            max_file = os.path.join( folder, file  )
                            rowPosition = self.tableWidget_BigFiles.rowCount()  # +++
                            self.tableWidget_BigFiles.insertRow(rowPosition)
                            self.tableWidget_BigFiles.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(file))
                            self.tableWidget_BigFiles.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(self.convert_size(size)))
                            self.tableWidget_BigFiles.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(folder))
                            # self.tableWidget_BigFiles.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(str(size)))
                            # self.tableWidget_BigFiles.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem("%s %s %s %s" % ("(", self.convert_size(size), ") -", max_file)))
                    else:
                        if self.checkBox_noFiles.isChecked():
                            self.tableWidget_BigFiles.addItem("%s %s" % ("( не доступен ) -", os.path.join( folder, file)))

    def get_size(self, start_path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        return total_size

    def GetBigFolders(self):
        if self.le_Mb_2.text() == "":
            if self.le_Gb_2.text() != "":
                self.le_Mb_2.setText(str(round(int(self.le_Gb_2.text()) * 1024, 2)))

        # if self.tableWidget_BigFolders.count() > 0:
        #     self.tableWidget_BigFolders.clear()
        for i in range(self.tableWidget_BigFolders.rowCount(), -1, -1):
            self.tableWidget_BigFolders.removeRow(i)

        path = os.path.abspath(self.le_PuthDir_2.text())
        max_size = (int(round(int(self.le_Mb_2.text()))) * 1024) * 1024

        for filename in os.listdir(path):
            f = os.path.join(path, filename)
            if not os.path.isfile(f):
                size = self.get_size(f)
                if max_size < size:
                    rowPosition = self.tableWidget_BigFolders.rowCount()  # +++
                    self.tableWidget_BigFolders.insertRow(rowPosition)
                    self.tableWidget_BigFolders.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(filename))
                    self.tableWidget_BigFolders.setItem(rowPosition, 1,
                                                      QtWidgets.QTableWidgetItem(self.convert_size(size)))
                    self.tableWidget_BigFolders.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(path))
                    # self.tableWidget_BigFolders.addItem("%s %s %s %s" % ("(", self.convert_size(size), ") -", f))

    def get_info(self):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Наименование', 'Информация'])
        rootNode = model.invisibleRootItem()
        parentSys = QStandardItem("Информация о системе")
        parentSys.appendRow([QStandardItem("Имя компьютера"), QStandardItem(uname().node)])
        parentSys.appendRow([QStandardItem("Операционная система"), QStandardItem(f"{uname().system} {uname().release}")])
        parentSys.appendRow([QStandardItem("Версия ОС"), QStandardItem(uname().version)])
        parentSys.appendRow([QStandardItem("Разрядность"), QStandardItem(uname().machine)])
        # parentSys.appendRow([QStandardItem(""), QStandardItem()])
       
        parentProc = QStandardItem("Процессор")
        parentProc.appendRow([QStandardItem("Имя"), QStandardItem(uname().processor)])
        parentProc.appendRow([QStandardItem("Физических ядер"), QStandardItem(str(psutil.cpu_count(logical=False)))])
        parentProc.appendRow([QStandardItem("Всего ядер"), QStandardItem(str(psutil.cpu_count(logical=True)))])
        parentProc.appendRow([QStandardItem("Частота"), QStandardItem(f"{psutil.cpu_freq().max:.2f} Мгц")])
        # parentProc.appendRow([QStandardItem(""), QStandardItem()])
        
        parentRam = QStandardItem("Оперативная память")
        parentRam.appendRow([QStandardItem("Всего"), QStandardItem(self.convert_size(psutil.virtual_memory().total))])
        parentRam.appendRow([QStandardItem("Свободно"), QStandardItem(self.convert_size(psutil.virtual_memory().available))])
        parentRam.appendRow([QStandardItem("Занято"), QStandardItem(self.convert_size(psutil.virtual_memory().used))])
        # parentRam.appendRow([QStandardItem(""), QStandardItem()])
       
        parentDisks = QStandardItem("Диски")
        for partition in psutil.disk_partitions():
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue
            parentDisk = QStandardItem(partition.device)
            parentDisks.appendRow([ parentDisk, None ])
            parentDisk.appendRow([QStandardItem("Файловая система"), QStandardItem(partition.fstype)])
            parentDisk.appendRow([QStandardItem("Всего"), QStandardItem(self.convert_size(partition_usage.total))])
            parentDisk.appendRow([QStandardItem("Свободно"), QStandardItem(self.convert_size(partition_usage.free))])
            parentDisk.appendRow([QStandardItem("Занято"), QStandardItem(self.convert_size(partition_usage.used))])
            parentDisk.appendRow([QStandardItem("Процент"), QStandardItem(f'{partition_usage.percent}')])

        parentNet = QStandardItem("Сеть")
        for interface_name, interface_address in psutil.net_if_addrs().items():
            if interface_name == 'Loopback Pseudo-Interface 1':
                continue
            else:
                parentIface = QStandardItem(interface_name)
                parentNet.appendRow([ parentIface, None ])
                if uname().system != "Darwin":
                    parentIface.appendRow([QStandardItem("MAC"), QStandardItem(interface_address[0].address.replace("-", ":"))])
                    parentIface.appendRow([QStandardItem("ipv4"), QStandardItem(interface_address[1].address)])
                    parentIface.appendRow([QStandardItem("ipv6"), QStandardItem(interface_address[2].address)])
                else:
                    parentIface.appendRow([QStandardItem("MAC/ipv4/ipv6"), QStandardItem(interface_address[0].address)])


        #parentDiskC = QStandardItem("Диск C")
        #parentDisks.appendRow([ parentDiskC, None ])
        #parentDiskC.appendRow([QStandardItem("Размер"), QStandardItem("121")])
        # parentDisks.appendRow([QStandardItem(""), QStandardItem()])


        rootNode.appendRow([ parentSys, None ])
        rootNode.appendRow([ parentProc, None ])
        rootNode.appendRow([ parentRam, None ])
        rootNode.appendRow([ parentDisks, None ])
        rootNode.appendRow([ parentNet, None ])
        
        self.treeView.setModel(model)
        self.treeView.setColumnWidth(0, 200)

 
def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
