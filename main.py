from PyQt5 import uic, QtWidgets
import sys
from ModifiedEcdsa import ModifiedECDSA
from BasePoint import BasePoint
from CurveConfig import GenCurveConfig


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('MainWindow.ui', self)
        self.GenKeys.clicked.connect(self.generate_keys)

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


app = QtWidgets.QApplication([])
window = MyWindow()
window.show()
sys.exit(app.exec())
