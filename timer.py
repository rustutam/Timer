import os
import sys
from time import gmtime
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import *


class Widget(QWidget):
    def __init__(self, window: QWidget, x_val: int,
                 y_val: int, width: int, height: int):
        super().__init__(window)
        self.setGeometry(x_val, y_val, width, height)


class Button(QPushButton):
    def __init__(self, window: QWidget, button_text: str, sheet_text: str,
                 x_val: int, y_val: int, width: int, height: int):
        super().__init__(button_text, window)
        self.setGeometry(x_val, y_val, width, height)
        self.setStyleSheet(sheet_text)


class Label(QLabel):
    def __init__(self, window: QWidget, label_text: str, sheet: str,
                 x_val: int, y_val: int, width: int, height: int):
        super().__init__(label_text, window)
        self.setGeometry(x_val, y_val, width, height)
        self.setStyleSheet(sheet)


class ComboBox(QComboBox):
    def __init__(self, window: QWidget, item: list, sheet_text: str,
                 x_val: int, y_val: int, width: int, height: int):
        super().__init__(window)
        self.addItems(item)
        self.setGeometry(x_val, y_val, width, height)
        self.setStyleSheet(sheet_text)


class SpinBox(QSpinBox):
    def __init__(self, window: QWidget, sheet: str, x_val: int,
                 y_val: int, width: int, height: int, buttons: bool):
        super().__init__(window)
        self.setGeometry(x_val, y_val, width, height)
        self.setStyleSheet(sheet)
        if not buttons:
            self.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.setAlignment(Qt.AlignCenter)


class TimerWindow(QMainWindow):

    def __init__(self, *__args):
        super().__init__(*__args)
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.execution)
        self.time = 0
        self.playlist = QMediaPlaylist(self)
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        self.media_player = QMediaPlayer(self)
        self.media_player.setPlaylist(self.playlist)
        self.set_first_signal()
        self.music = "Приора"
        self.setWindowTitle('Timer by rustut')
        self.setMaximumSize(600, 400)
        self.setMinimumSize(600, 400)
        self.setStyleSheet("background-color: rgb(67, 40, 24);")
        self.build_user_interface()
        self.show()

    def build_user_interface(self):
        button_stylesheet = """
                QPushButton {
                    font: bold;
                    font-size: 15pt;
                    border-radius: 9px;
                    color: rgb(67, 40, 24);
                    background-color: rgb(255, 230, 167);
                }
                QPushButton:hover {
                    font: bold;
                    font-size: 15pt;
                    border-radius: 9px;
                    color: rgb(67, 40, 24);
                    background-color: rgb(187, 148, 87);
                }
                QPushButton:pressed {
                    font: bold;
                    font-size: 15pt;
                    border-radius: 9px;
                    color: rgb(67, 40, 24);
                    background-color: rgb(175, 138, 81);
                }
                """
        spinbox_stylesheet = """
                            font-size: 40pt;
                            border-radius: 15px;
                            color: rgb(67, 40, 24);
                            background-color: rgb(255, 230, 167);
                        """
        label_stylesheet = """
            font: bold;
            font-size: 14pt;
            color: rgb(255, 230, 167);
        """
        combobox_stylesheet = """
            background-color: rgb(255, 230, 167);
            color: rgb(67, 40, 24);
        """

        self.spinbox_group = Widget(self, 100, 30, 400, 160)

        hours_label = Label(self.spinbox_group,
                            "HOURS",
                            label_stylesheet, 0, 0, 120, 31)
        minutes_label = Label(self.spinbox_group,
                              "MINUTES",
                              label_stylesheet, 140, 0, 120, 31)
        seconds_label = Label(self.spinbox_group,
                              "SECONDS",
                              label_stylesheet, 280, 0, 120, 31)

        self.hours_spinbox = SpinBox(self.spinbox_group, spinbox_stylesheet,
                                     0, 40, 120, 120, False)
        self.hours_spinbox.setMaximum(23)

        self.minutes_spinbox = SpinBox(self.spinbox_group, spinbox_stylesheet,
                                       140, 40, 120, 120, False)
        self.minutes_spinbox.setMaximum(59)
        self.seconds_spinbox = SpinBox(self.spinbox_group, spinbox_stylesheet,
                                       280, 40, 120, 120, False)
        self.seconds_spinbox.setMaximum(59)

        timer_control_group = Widget(self, 150, 210, 421, 61)
        self.start_pause_resume_button = Button(
            timer_control_group, "Start", button_stylesheet, 0, 0, 130, 60)
        self.reset_button = Button(
            timer_control_group, "Reset", button_stylesheet, 170, 0, 130, 60)
        self.start_pause_resume_button.clicked.connect(self.push_start)
        self.reset_button.clicked.connect(self.push_reset)

        self.set_time_group = Widget(self, 40, 300, 200, 80)

        ten_min_button = Button(self.set_time_group, "10 min",
                                button_stylesheet, 0, 0, 90, 30)
        thirty_min_button = Button(self.set_time_group, "30 min",
                                   button_stylesheet, 0, 45, 90, 30)
        one_hour_button = Button(self.set_time_group, "1 hour",
                                 button_stylesheet, 95, 0, 90, 30)
        five_hour_button = Button(self.set_time_group, "5 hour",
                                  button_stylesheet, 95, 45, 90, 30)
        ten_min_button.clicked.connect(self.set_ten_minutes)
        thirty_min_button.clicked.connect(self.set_thirty_minutes)
        one_hour_button.clicked.connect(self.set_one_hour)
        five_hour_button.clicked.connect(self.set_five_hour)

        self.music_group = Widget(self, 450, 330, 140, 70)
        hours_label = Label(self.music_group,
                            "MUSIC",
                            label_stylesheet, 0, 0, 120, 31)
        self.music_combobox = ComboBox(self.music_group, ["Приора", "Кавказ",
                                                          "Семёрка", "Кино"],
                                       combobox_stylesheet, 0, 40, 140, 25)
        self.music_combobox.currentTextChanged.connect(self.set_music)

    def set_music(self):
        self.music = self.music_combobox.currentText()
        if self.music == "Приора":
            self.set_first_signal()
        elif self.music == "Кавказ":
            self.set_second_signal()
        elif self.music == "Семёрка":
            self.set_third_signal()
        elif self.music == "Кино":
            self.set_fourth_signal()

    def push_start(self):
        hours = self.hours_spinbox.value()
        minutes = self.minutes_spinbox.value()
        seconds = self.seconds_spinbox.value()
        self.time = 3600 * hours + 60 * minutes + seconds
        self.media_player.stop()
        self.timer.start()
        self.disable_widgets()
        self.start_pause_resume_button.setText("Pause")
        self.start_pause_resume_button.clicked.connect(self.push_pause)

    def push_pause(self):
        self.timer.stop()
        self.start_pause_resume_button.setText("Resume")
        self.start_pause_resume_button.clicked.connect(self.push_resume)

    def push_resume(self):
        self.timer.start()
        self.start_pause_resume_button.setText("Pause")
        self.start_pause_resume_button.clicked.connect(self.push_pause)

    def push_reset(self):
        self.timer.stop()
        self.time = 0
        self.hours_spinbox.setValue(0)
        self.minutes_spinbox.setValue(0)
        self.seconds_spinbox.setValue(0)
        self.start_pause_resume_button.setText("Start")
        self.start_pause_resume_button.clicked.connect(self.push_start)
        self.enable_widgets()
        self.media_player.stop()

    def execution(self):
        if self.time <= 0:
            self.timer.stop()
            self.start_pause_resume_button.setText("Start")
            self.start_pause_resume_button.clicked.connect(self.push_start)
            self.enable_widgets()
            self.media_player.play()
        else:
            self.time -= 1
            hours = gmtime(self.time).tm_hour
            minutes = gmtime(self.time).tm_min
            seconds = gmtime(self.time).tm_sec
            self.hours_spinbox.setValue(hours)
            self.minutes_spinbox.setValue(minutes)
            self.seconds_spinbox.setValue(seconds)

    def enable_widgets(self):
        self.set_time_group.setEnabled(True)
        self.spinbox_group.setEnabled(True)
        self.music_group.setEnabled(True)

    def disable_widgets(self):
        self.set_time_group.setEnabled(False)
        self.spinbox_group.setEnabled(False)
        self.music_group.setEnabled(False)

    def set_ten_minutes(self):
        self.hours_spinbox.setValue(0)
        self.minutes_spinbox.setValue(10)
        self.seconds_spinbox.setValue(0)

    def set_thirty_minutes(self):
        self.hours_spinbox.setValue(0)
        self.minutes_spinbox.setValue(30)
        self.seconds_spinbox.setValue(0)

    def set_one_hour(self):
        self.hours_spinbox.setValue(1)
        self.minutes_spinbox.setValue(0)
        self.seconds_spinbox.setValue(0)

    def set_five_hour(self):
        self.hours_spinbox.setValue(5)
        self.minutes_spinbox.setValue(0)
        self.seconds_spinbox.setValue(0)

    def set_first_signal(self):
        self.add_media_to_playlist("music/priora.mp3")

    def set_second_signal(self):
        self.add_media_to_playlist("music/kavkaz.mp3")

    def set_third_signal(self):
        self.add_media_to_playlist("music/semerka.mp3")

    def set_fourth_signal(self):
        self.add_media_to_playlist("music/kino.mp3")

    def add_media_to_playlist(self, filename: str):
        self.playlist.clear()
        audio_path = os.path.join(os.getcwd(), filename)
        url = QUrl.fromLocalFile(audio_path)
        self.playlist.addMedia(QMediaContent(url))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimerWindow()
    sys.exit(app.exec())
