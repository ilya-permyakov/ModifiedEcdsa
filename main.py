from PyQt5 import uic, QtWidgets
import sys
from ModifiedEcdsa import ModifiedECDSA
from BasePoint import BasePoint
from CurveConfig import GenCurveConfig
from Point import Point


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('MainWindow.ui', self)
        self.GenKeys.clicked.connect(self.generate_keys)
        self.ShowPrivateKey.clicked.connect(self.toggle_visibility)
        self.Sign.clicked.connect(self.create_sign)
        self.Verify.clicked.connect(self.verify_sign)

    def generate_keys(self):
        params = GenCurveConfig().generate_params()
        G = BasePoint(params).find_base_point()
        ecdsa = ModifiedECDSA(params, G)
        keys = ecdsa.gen_keys()
        self.Parameters.setText(f"a = {str(params['a'])}\nb = {str(params['b'])}\np = {str(params['p'])}\n\n"
                                f"Базовая точка:\nx = {str(G['base_point'].x)}\ny = {str(G['base_point'].y)}\n\n"
                                f"Порядок подгруппы: {str(G['subgroup_order'])}")
        self.PrivateKeyLine.setText(str(keys['d']))
        self.PublicKeyLine.setText(f"x = {str(keys['Q'].x)}\ny = {str(keys['Q'].y)}")
        QtWidgets.QApplication.processEvents()

    def toggle_visibility(self):
        if self.PrivateKeyLine.echoMode() == QtWidgets.QLineEdit.Normal:
            self.PrivateKeyLine.setEchoMode(QtWidgets.QLineEdit.Password)
            self.ShowPrivateKey.setText("Показать")
        else:
            self.PrivateKeyLine.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.ShowPrivateKey.setText("Скрыть")

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

        message = self.InputMessage.toPlainText()

        ecdsa = ModifiedECDSA(curve, G)
        sign = ecdsa.gen_sign(private_key, message)

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

        message = self.InputMessageVerify.toPlainText()

        ecdsa = ModifiedECDSA(curve, G)
        result = ecdsa.verification(message, sign_to_verify, public_key)

        self.ResultVerify.setText(result)


app = QtWidgets.QApplication([])
window = MyWindow()
window.show()
sys.exit(app.exec())
