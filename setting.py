from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QObject, QByteArray, pyqtSignal, pyqtSlot


class AppSettings(QObject):
    sig_listen_changed = pyqtSignal()
    sig_trans_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super(AppSettings, self).__init__(parent=parent)

        self.settings = QSettings('config.ini', QSettings.IniFormat)
        self.sig_listen_changed.connect(self.on_changed)
        self.sig_trans_changed.connect(self.on_changed)

    @property
    def listen_ip(self):
        return str(self.settings.value('LISTEN/IP', '127.0.0.1'))

    @property
    def listen_port(self):
        return str(self.settings.value('LISTEN/PORT', '8555'))

    @property
    def listen_protocol(self):
        return str(self.settings.value('LISTEN/PROTOCOL', 'tcp'))

    @property
    def listen_enable(self):
        return str(self.settings.value('LISTEN/ENABLE', '0'))

    def listen(self, ip, port, protocol, enable):
        self.settings.setValue('LISTEN/IP', str(ip))
        self.settings.setValue('LISTEN/PORT', str(port))
        self.settings.setValue('LISTEN/PROTOCOL', str(protocol))
        self.settings.setValue('LISTEN/ENABLE', str(enable))
        self.sig_listen_changed.emit()

    def trans_localip(self, pipe):
        return str(self.settings.value('TRANS%d/LOCALIP' % pipe, '127.0.0.1'))

    def trans_ip(self, pipe):
        return str(self.settings.value('TRANS%d/IP' % pipe, '127.0.0.1'))

    def trans_port(self, pipe):
        if pipe == 1:
            return str(self.settings.value('TRANS%d/PORT' % pipe, '8550'))
        else:
            return str(self.settings.value('TRANS%d/PORT' % pipe, '8001'))

    def trans_protocol(self, pipe):
        return str(self.settings.value('TRANS%d/PROTOCOL' % pipe, 'tcp'))

    def trans_enable(self, pipe):
        return str(self.settings.value('TRANS%d/ENABLE' % pipe, '0'))

    def trans(self, pipe, localip, ip, port, protocol, enable):
        self.settings.setValue('TRANS%d/LOCALIP' % pipe, str(localip))
        self.settings.setValue('TRANS%d/IP' % pipe, str(ip))
        self.settings.setValue('TRANS%d/PORT' % pipe, str(port))
        self.settings.setValue('TRANS%d/PROTOCOL' % pipe, str(protocol))
        self.settings.setValue('TRANS%d/Enable' % pipe, str(enable))
        self.sig_trans_changed.emit(pipe)

    @pyqtSlot()
    def on_changed(self):
        print('%s on_changed' % self.__class__.__name__)
        self.settings.sync()


appsetting = AppSettings()
