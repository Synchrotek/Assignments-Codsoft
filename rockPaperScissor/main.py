import sys
import random
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class RockPaperScissorsGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rock-Paper-Scissors Game")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.heading_label = QLabel("Game", self)
        self.heading_label.setFont(QFont("Arial", 20))
        self.heading_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.heading_label)

        self.horizontal_line = QLabel("<hr>", self)
        self.layout.addWidget(self.horizontal_line)

        self.choose_label = QLabel("Choose your option:", self)
        self.choose_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.choose_label)

        self.rock_button = QPushButton("Rock", self)
        self.rock_button.setFont(QFont("Arial", 12))
        self.rock_button.clicked.connect(lambda: self.play("Rock"))
        self.layout.addWidget(self.rock_button)

        self.paper_button = QPushButton("Paper", self)
        self.paper_button.setFont(QFont("Arial", 12))
        self.paper_button.clicked.connect(lambda: self.play("Paper"))
        self.layout.addWidget(self.paper_button)

        self.scissors_button = QPushButton("Scissors", self)
        self.scissors_button.setFont(QFont("Arial", 12))
        self.scissors_button.clicked.connect(lambda: self.play("Scissors"))
        self.layout.addWidget(self.scissors_button)

        self.computer_label = QLabel("Computer chose:", self)
        self.computer_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.computer_label)

        self.computer_choice_text = QLineEdit(self)
        self.computer_choice_text.setReadOnly(True)
        self.computer_choice_text.setFont(QFont("Arial", 12))
        self.computer_choice_text.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.computer_choice_text)

        self.result_label = QLabel("Score: 0/0", self)
        self.result_label.setFont(QFont("Arial", 14))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.result_label)

        self.horizontal_line = QLabel("<hr>", self)
        self.layout.addWidget(self.horizontal_line)

        self.score_label = QLabel("", self)
        self.score_label.setFont(QFont("Arial", 16))
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.score_label)

        self.user_wins = 0
        self.total_plays = 0

    def play(self, user_choice):
        choices = ["Rock", "Paper", "Scissors"]
        computer_choice = random.choice(choices)
        self.computer_choice_text.setText(computer_choice)

        if user_choice == computer_choice:
            result = "It's a tie!"
        elif (
            (user_choice == "Rock" and computer_choice == "Scissors")
            or (user_choice == "Paper" and computer_choice == "Rock")
            or (user_choice == "Scissors" and computer_choice == "Paper")
        ):
            result = "You Win!"
            self.user_wins += 1
        else:
            result = "You Lose!"

        self.result_label.setText(result)
        if user_choice != computer_choice:
            self.total_plays += 1
        self.score_label.setText(f"Score: {self.user_wins}/{self.total_plays}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RockPaperScissorsGame()
    window.show()
    sys.exit(app.exec_())
