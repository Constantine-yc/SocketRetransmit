from PyQt5.QtCore import QObject, QByteArray, pyqtSignal, pyqtSlot
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QUdpSocket, QHostAddress
from setting import appsetting


class TransPipe(QObject):
    sig_data_arrived = pyqtSignal(QByteArray)
    sig_Transing_state = pyqtSignal(int, bool)

    def __init__(self, pipe, parent=None):
        super(TransPipe, self).__init__(parent=parent)
        self.pipe = pipe
        self.SocketClient = None

    @pyqtSlot(int)
    def start_trans(self, pipe):
        if self.pipe != pipe:
            return

        print('start_trans %d' % self.pipe)

        if self.SocketClient:
            self.SocketClient.readyRead.disconnect(self.on_readyRead)
            self.SocketClient.connected.disconnect(self.on_connected)
            self.SocketClient.disconnected.disconnect(self.on_disconnected)
            self.SocketClient.error.disconnect(self.on_error)
            self.SocketClient.close()
            self.SocketClient.deleteLater()
            self.SocketClient = None

        if appsetting.trans_protocol(pipe) == 'tcp':
            self.SocketClient = QTcpSocket()
        else:
            self.SocketClient = QUdpSocket()

        self.SocketClient.readyRead.connect(self.on_readyRead)
        self.SocketClient.connected.connect(self.on_connected)
        self.SocketClient.disconnected.connect(self.on_disconnected)
        self.SocketClient.error.connect(self.on_error)

        self.SocketClient.bind(QHostAddress(appsetting.trans_localip(pipe)))
        self.sig_Transing_state.emit(self.pipe, False)
        if appsetting.trans_enable(self.pipe) != '0':
            self.SocketClient.connectToHost(appsetting.trans_ip(pipe), int(appsetting.trans_port(pipe)))

    @pyqtSlot()
    def on_connected(self):
        print('on_connected %d' % self.pipe)
        self.sig_Transing_state.emit(self.pipe, True)

    @pyqtSlot()
    def on_disconnected(self):
        print('on_disconnected %d' % self.pipe)
        self.sig_Transing_state.emit(self.pipe, False)

    @pyqtSlot()
    def on_error(self):
        print('%s on_error %d:%s' % (self.__class__.__name__, self.pipe, self.SocketClient.errorString()))

    @pyqtSlot(QByteArray)
    def on_data_arrived(self, data):
        print("%s on_data_arrived %d" % ( self.__class__.__name__, self.pipe))
        if self.SocketClient:
            self.SocketClient.write(data)

    @pyqtSlot()
    def on_readyRead(self):
        print("%s on_readyRead %d" % (self.__class__.__name__, self.pipe))
        if self.SocketClient:
            data = self.SocketClient.readAll()
            self.sig_data_arrived.emit(data)

