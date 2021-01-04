from PyQt5.QtCore import QObject, QByteArray, pyqtSignal, pyqtSlot
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QUdpSocket, QHostAddress
from setting import appsetting


class ListenPipe(QObject):
    sig_data_arrived = pyqtSignal(QByteArray)
    sig_listening_state = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(ListenPipe, self).__init__(parent=parent)

        self.tcpServer = QTcpServer()
        self.socketClients = []

        self.tcpServer.newConnection.connect(self.on_newconnection)

    @pyqtSlot()
    def start_listen(self):
        print('start_listen:%s %s' % (appsetting.listen_ip, appsetting.listen_port))
        self.tcpServer.close()
        for socketClient in self.socketClients:
            socketClient.close()
            socketClient.deleteLater()

        if appsetting.listen_enable != '0':
            self.tcpServer.listen(QHostAddress(appsetting.listen_ip), int(appsetting.listen_port))

        self.sig_listening_state.emit(self.tcpServer.isListening())

    @pyqtSlot()
    def on_newconnection(self):
        print('on_newconnection')
        socketClient = self.tcpServer.nextPendingConnection()
        socketClient.readyRead.connect(self.on_readyRead)
        socketClient.connected.connect(self.on_connected)
        socketClient.disconnected.connect(self.on_disconnected)
        socketClient.error.connect(self.on_error)
        self.socketClients.append(socketClient)
        print('self.socketClients size=%d' % len(self.socketClients))

    @pyqtSlot()
    def on_readyRead(self):
        print("%s on_readyRead" % self.__class__.__name__)
        socketClient = self.sender()
        data = socketClient.readAll()
        #print(data)
        self.sig_data_arrived.emit(data)

    @pyqtSlot(QByteArray)
    def on_data_arrived(self, data):
        print("%s on_data_arrived" % self.__class__.__name__)
        for socketClient in self.socketClients:
            socketClient.write(data)

    @pyqtSlot()
    def on_connected(self):
        print('on_connected')

    @pyqtSlot()
    def on_disconnected(self):
        print('on_disconnected')
        socketClient = self.sender()
        self.socketClients.remove(socketClient)
        socketClient.deleteLater()
        print('self.socketClients size=%d' % len(self.socketClients))

    @pyqtSlot()
    def on_error(self):
        socketClient = self.sender()
        print('%s on_error:%s' % (self.__class__.__name__, socketClient.errorString()))

