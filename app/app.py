from PySide2 import QtWidgets
import currency_converter


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.converter = currency_converter.CurrencyConverter()
        self.setWindowTitle("Currency converter")
        self.layout = QtWidgets.QHBoxLayout(self)
        self.cbb_currency_from = QtWidgets.QComboBox()
        self.cbb_currency_to = QtWidgets.QComboBox()
        self.spn_amount_from = QtWidgets.QSpinBox()
        self.spn_amount_to = QtWidgets.QDoubleSpinBox()
        self.btn_swap = QtWidgets.QPushButton("Swap")
        self.setup_ui()
        self.setup_css()
        self.set_default_values()
        self.setup_connections()

    def setup_ui(self):
        self.layout.addWidget(self.cbb_currency_from)
        self.layout.addWidget(self.spn_amount_from)
        self.layout.addWidget(self.cbb_currency_to)
        self.layout.addWidget(self.spn_amount_to)
        self.layout.addWidget(self.btn_swap)

    def set_default_values(self):
        self.cbb_currency_from.addItems(sorted(list(self.converter.currencies)))
        self.cbb_currency_to.addItems(sorted(list(self.converter.currencies)))
        self.cbb_currency_from.setCurrentText("EUR")
        self.cbb_currency_to.setCurrentText("EUR")
        self.spn_amount_from.setRange(1, 1000000000)
        self.spn_amount_to.setRange(1, 1000000000)
        self.spn_amount_from.setValue(100)
        self.spn_amount_to.setValue(100)

    def setup_connections(self):
        self.cbb_currency_from.activated.connect(self.compute)
        self.cbb_currency_to.activated.connect(self.compute)
        self.spn_amount_from.valueChanged.connect(self.compute)
        self.spn_amount_to.valueChanged.connect(self.compute)
        self.btn_swap.clicked.connect(self.swap_currencies)

    def setup_css(self):
        self.btn_swap.setStyleSheet(
            """
            background-color: rgb(75, 75, 75);
            color: rgb(240, 240, 240);
            """
        )

    def compute(self):
        try:
            self.spn_amount_to.setValue(
                self.converter.convert(
                    self.spn_amount_from.value(),
                    self.cbb_currency_from.currentText(),
                    self.cbb_currency_to.currentText())
            )
        except currency_converter.currency_converter.RateNotFoundError:
            print("An error occurred with one of the currency.")

    def swap_currencies(self):
        currency_from = self.cbb_currency_from.currentText()
        self.cbb_currency_from.setCurrentText(self.cbb_currency_to.currentText())
        self.cbb_currency_to.setCurrentText(currency_from)
        self.compute()


def main():
    app = QtWidgets.QApplication([])
    window = App()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
