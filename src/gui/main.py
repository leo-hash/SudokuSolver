import sys
from pathlib import Path

from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from src.engine.grid import SudokuGrid
from src.engine.generator import SudokuGenerator


class SudokuFrontend(QObject):

    # signal to update GUI (row, colum, value)
    cellChanged = Signal(int, int, int)

    # error message (row, column, err_message)
    invalidNumberInput = Signal(int, int, str)


    def __init__(self):
        super().__init__()

        self._sudoku: SudokuGrid | None = None
        self._generator = SudokuGenerator()


    def generate_new_sudoku(self):
        self._sudoku = self._generator.generate()


    @Slot(int, int, result=int)
    def getValue(self, row, column):
        if self._sudoku.grid[row][column].number is None:
            return 0
        return self._sudoku.grid[row][column].number


    @Slot(int, int, result=bool)
    def isFixed(self, row, column):
        return self._sudoku.grid[row][column].is_fixed


    @Slot(int, int, int, result=bool)
    def setValue(self, row, column, value):

        if self._sudoku.grid[row][column].is_fixed:
            print("Can't set Field, because it is fixed")
            self.invalidNumberInput.emit(row, column, "Can't set Field, because it is fixed")
            return False

        if value not in self._sudoku.grid[row][column].pos_number:
            print("Wrong Number entered")
            self.invalidNumberInput.emit(row, column, "Wrong Number entered")
            return False

        try:
            self._sudoku.grid[row][column].number = value
        except ValueError:
            print("Value entered is not a number between 1 and 9")
            self.invalidNumberInput.emit(row, column, "Value entered is not a number between 1 and 9")
            return False

        # make changes in QML
        self.cellChanged.emit(row, column, value)
        return True


if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    frontend = SudokuFrontend()
    frontend.generate_new_sudoku()


    engine.rootContext().setContextProperty("sudokuFrontend", frontend)

    qml_file = Path(__file__).parent / "main.qml"
    engine.load(str(qml_file))


    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())