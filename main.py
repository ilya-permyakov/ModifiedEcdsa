from PyQt5 import uic, QtWidgets, QtCore
import sys
from ModifiedEcdsa import ModifiedECDSA
from BasePoint import BasePoint
from CurveConfig import GenCurveConfig
from Point import Point


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('NewMainWindow.ui', self)
        self.setWindowTitle("Цифровая подпись")
        self.GenParams.clicked.connect(self.prepare_gen_params)
        self.ShowPrivateKey.clicked.connect(self.show_pr_key)
        self.FileGenSign.clicked.connect(self.open_file_dialog)
        self.FileVerifySign.clicked.connect(self.open_file_dialog)
        self.Sign.clicked.connect(self.create_sign)
        self.Verify.clicked.connect(self.verify_sign)
        self.progressBar.hide()
        self.statusLabel.hide()

    def prepare_gen_params(self):
        self.progressBar.setMaximum(0)
        self.progressBar.show()
        self.statusLabel.show()
        QtCore.QTimer.singleShot(10, self.gen_params)

    def gen_params(self):
        params = GenCurveConfig().generate_params()
        G = BasePoint(params).find_base_point()
        ecdsa = ModifiedECDSA(params, G)
        keys = ecdsa.gen_keys()

        self.fill_gen_params_fields(params, G, keys)

        if self.UseGenParams.isChecked():
            data = {"params": params, "G": G, "keys": keys}
            self.fill_gen_sign_fields(data)
        self.progressBar.hide()
        self.statusLabel.hide()

    def fill_gen_params_fields(self, params, G, keys):
        self.Parameters.setText(f"a = {str(params['a'])}\nb = {str(params['b'])}\n"
                                f"p = {str(params['p'])}\n\n"f"Базовая точка:\nx = {str(G['base_point'].x)}\n"
                                f"y = {str(G['base_point'].y)}\n\n"
                                f"Порядок подгруппы: {str(G['subgroup_order'])}")
        self.PrivateKeyLine.setText(str(keys['d']))
        self.PublicKeyLine.setText(f"x = {str(keys['Q'].x)}\ny = {str(keys['Q'].y)}")

    def show_pr_key(self):
        if self.PrivateKeyLine.echoMode() == QtWidgets.QLineEdit.Normal:
            self.PrivateKeyLine.setEchoMode(QtWidgets.QLineEdit.Password)
            self.ShowPrivateKey.setText("Показать")
        else:
            self.PrivateKeyLine.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.ShowPrivateKey.setText("Скрыть")

    def fill_gen_sign_fields(self, data=None):
        if self.UseGenParams.isChecked() and data is not None:
            self.InputA.setText(str(data['params']['a']))
            self.InputB.setText(str(data['params']['b']))
            self.InputP.setText(str(data['params']['p']))
            self.InputBasePoint.setPlainText(f"{str(data['G']['base_point'].x)}\n{str(data['G']['base_point'].y)}")
            self.InputSubgroupOrder.setText(str(data['G']['subgroup_order']))
            self.InputPrivateKeyLine.setText(str(data['keys']['d']))

    def open_file_dialog(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        if file_name:
            sender = self.sender()
            if sender == self.FileGenSign:
                self.InputFile.setText(file_name)
            elif sender == self.FileVerifySign:
                self.InputFileVerifySign.setText(file_name)

    def create_sign(self):
        base_point_text = self.InputBasePoint.toPlainText()
        x, y = map(int, base_point_text.split('\n'))
        base_point = Point(x, y)

        curve = {
            'a': int(self.InputA.text()),
            'b': int(self.InputB.text()),
            'p': int(self.InputP.text())
        }

        G = {
            'base_point': base_point,
            'subgroup_order': int(self.InputSubgroupOrder.text())
        }

        private_key = {
            'd': int(self.InputPrivateKeyLine.text())
        }

        file = self.InputFile.text()

        ecdsa = ModifiedECDSA(curve, G)
        sign = ecdsa.gen_sign(private_key, file)

        self.YourSign.setText(f"r = {str(sign['r'])}\ns = {str(sign['s'])}")

    def verify_sign(self):
        base_point_text = self.InputBasePointVerify.toPlainText()
        x, y = map(int, base_point_text.split('\n'))
        base_point = Point(x, y)

        sign = self.InputSignVerify.toPlainText()
        r, s = map(int, sign.split('\n'))

        curve = {
            'a': int(self.InputAVerify.text()),
            'b': int(self.InputBVerify.text()),
            'p': int(self.InputPVerify.text())
        }

        public_key_text = self.InputPublicKeyVerify.toPlainText()
        x, y = map(int, public_key_text.split('\n'))
        public_key = Point(x, y, curve)

        G = {
            'base_point': base_point,
            'subgroup_order': int(self.InputSubgroupOrderVerify.text())
        }

        sign_to_verify = {
            'r': r,
            's': s
        }

        file = self.InputFileVerifySign.text()

        ecdsa = ModifiedECDSA(curve, G)
        result = ecdsa.verification(file, sign_to_verify, public_key)

        self.ResultVerify.setText(result)


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec_())
