from PyQt5 import QtWidgets
from PyQt5.QtCore import QByteArray, pyqtSignal, pyqtSlot
from ui_mainwindow import Ui_MainWindow
from setting import appsetting
from listenpipe import ListenPipe
from transpipe import TransPipe


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    data_arrived = pyqtSignal(QByteArray)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.edtIPListen.setText(appsetting.listen_ip)
        self.edtPortListen.setText(appsetting.listen_port)
        self.btnTCPListen.setChecked(True)
        self.btnUDPListen.setEnabled(False)

        self.edtLocalIPTrans1.setText(appsetting.trans_localip(1))
        self.edtIPTrans1.setText(appsetting.trans_ip(1))
        self.edtPortTrans1.setText(appsetting.trans_port(1))
        if appsetting.trans_protocol(1) == 'tcp':
            self.btnTCPTrans1.setChecked(True)
        else:
            self.btnUDPTrans1.setChecked(True)

        self.edtLocalIPTrans2.setText(appsetting.trans_localip(2))
        self.edtIPTrans2.setText(appsetting.trans_ip(2))
        self.edtPortTrans2.setText(appsetting.trans_port(2))
        if appsetting.trans_protocol(2) == 'tcp':
            self.btnTCPTrans2.setChecked(True)
        else:
            self.btnUDPTrans2.setChecked(True)

        self.listenpipe = ListenPipe()
        self.listenpipe.sig_data_arrived.connect(self.on_data_arrived)
        self.listenpipe.sig_listening_state.connect(self.on_listening_state)
        appsetting.sig_listen_changed.connect(self.listenpipe.start_listen)

        self.transpipes = {}
        self.transpipes[1] = TransPipe(1)
        self.data_arrived.connect(self.transpipes[1].on_data_arrived)
        self.transpipes[1].sig_Transing_state.connect(self.on_transing_state)
        appsetting.sig_trans_changed.connect(self.transpipes[1].start_trans)

        self.transpipes[2] = TransPipe(2)
        self.data_arrived.connect(self.transpipes[2].on_data_arrived)
        self.transpipes[2].sig_Transing_state.connect(self.on_transing_state)
        appsetting.sig_trans_changed.connect(self.transpipes[2].start_trans)

        appsetting.sig_listen_changed.emit()
        appsetting.sig_trans_changed.emit(1)
        appsetting.sig_trans_changed.emit(2)


    @pyqtSlot()
    def on_btnListenStart_clicked(self):
        print("on_btnListenStart_clicked")
        appsetting.listen(self.edtIPListen.text()
                          , self.edtPortListen.text()
                          , 'tcp' if self.btnTCPListen.isChecked() else 'udp'
                          , '1')

    @pyqtSlot()
    def on_btnListenStop_clicked(self):
        print("on_btnListenStop_clicked")
        appsetting.listen(self.edtIPListen.text()
                          , self.edtPortListen.text()
                          , 'tcp' if self.btnTCPListen.isChecked() else 'udp'
                          , '0')

    @pyqtSlot()
    def on_btnTrans1Start_clicked(self):
        print("on_btnTrans1Start_clicked")
        appsetting.trans(1
                         , self.edtLocalIPTrans1.text()
                         , self.edtIPTrans1.text()
                         , self.edtPortTrans1.text()
                         , 'tcp' if self.btnTCPTrans1.isChecked() else 'udp'
                         , '1')

    @pyqtSlot()
    def on_btnTrans1Stop_clicked(self):
        print("on_btnTrans1Stop_clicked")
        appsetting.trans(1
                         , self.edtLocalIPTrans1.text()
                         , self.edtIPTrans1.text()
                         , self.edtPortTrans1.text()
                         , 'tcp' if self.btnTCPTrans1.isChecked() else 'udp'
                         , '0')

    @pyqtSlot()
    def on_btnTrans2Start_clicked(self):
        print("on_btnTrans2Start_clicked")
        appsetting.trans(2
                         , self.edtLocalIPTrans2.text()
                         , self.edtIPTrans2.text()
                         , self.edtPortTrans2.text()
                         , 'tcp' if self.btnTCPTrans2.isChecked() else 'udp'
                         , '1')

    @pyqtSlot()
    def on_btnTrans2Stop_clicked(self):
        print("on_btnTrans2Stop_clicked")
        appsetting.trans(2
                         , self.edtLocalIPTrans2.text()
                         , self.edtIPTrans2.text()
                         , self.edtPortTrans2.text()
                         , 'tcp' if self.btnTCPTrans2.isChecked() else 'udp'
                         , '0')

    @pyqtSlot(QByteArray)
    def on_data_arrived(self, data):
        print("%s on_data_arrived" % self.__class__.__name__)
        self.data_arrived.emit(data)

    @pyqtSlot(bool)
    def on_listening_state(self, listening):
        print("on_listening_state")
        self.btnListenStart.setEnabled(not listening)
        self.btnListenStop.setEnabled(listening)

    @pyqtSlot(int, bool)
    def on_transing_state(self, pipe, transing):
        print("on_transing_state %d" % pipe)
        if pipe == 1:
            self.btnTrans1Start.setEnabled(not transing)
            self.btnTrans1Stop.setEnabled(transing)
        elif pipe == 2:
            print(transing)
            self.btnTrans2Start.setEnabled(not transing)
            self.btnTrans2Stop.setEnabled(transing)

