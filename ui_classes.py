from PyQt5 import QtWidgets, QtCore
from elements import *


# dialog for adding a character
class AddChar_Diag(QtWidgets.QDialog):
    resized = QtCore.pyqtSignal()
    def __init__(self, Parent=None):
        super().__init__()
        self.parent = Parent
        self.level = -1
        self.index = 0
        self.questions = self.parent.story.questions
        self.character = None
        self.FirstRun = True
        self.setGeometry(100,100,500,250)
        self.UiComponents()
        self.show()
        self.resized.connect(self.update)
        self.UiComponents()
        self.move_next()

    def UiComponents(self):
        self.question = QtWidgets.QLabel(self)
        self.next_button = QtWidgets.QPushButton(self)
        self.level_button = QtWidgets.QRadioButton(self)
        self.low_det = QtWidgets.QAction(self)
        self.low_det.setText("Low Detail")
        self.med_det = QtWidgets.QAction(self)
        self.med_det.setText("Medium Detail")
        self.high_det = QtWidgets.QAction(self)
        self.high_det.setText("High Detail")
        self.level_button.addAction(self.low_det)
        self.level_button.addAction(self.med_det)
        self.level_button.addAction(self.high_det)
        self.text = QtWidgets.QTextEdit(self)
        self.text.setHidden(True)
        self.next_button.clicked.connect(self.move_next)


        self.question.setGeometry(20, 20, 250, 25)
        self.text.setGeometry(10, 50, self.geometry().width() -20, self.geometry().height()-50)

    def update(self):
        geom = self.geometry()
        x = geom.width()
        y = geom.height()

        

    def run(self):
        if self.FirstRun:
            self.startup()

        self.move_next()

    def startup(self):
        
        return

    def ask_question(self, q):
        self.question.setText(q)

    def move_next(self):
        if self.FirstRun:
            if self.level == 0:
                # check which level the user wants to do
                return
            else:
                # get's the character's name
                return
            
            
        data = self.text.toPlainText()
        char_attr = Attribute()
        char_attr.set_e1(self.questions["Questions"][self.index]["QuestionString"])
        char_attr.set_e2(data)

        self.character

        return