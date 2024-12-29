import sys
import pygame
from PyQt5.QtWidgets import (
    QApplication, QLabel,
    QPushButton, QLineEdit, QWidget, QMessageBox)
from PyQt5.QtGui import QIcon, QFont, QIntValidator

def get_screen_size():
    pygame.init()
    display_info = pygame.display.Info()
    return display_info.current_w, display_info.current_h

SCREEN_WIDTH, SCREEN_HEIGHT = get_screen_size()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.labels = []
        self.frames = []
        self.pfs_labels = []
        self.started = False
        self.setWindowTitle("Advanced OS Project")
        self.setGeometry(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setWindowIcon(QIcon("OS.jpg"))
        self.setStyleSheet("background-color: #f0f8ff;")
        label = QLabel("Advanced OS Project", self)
        label.setFont(QFont("Helvetica", 40))
        label.setStyleSheet("text-decoration: underline;"
                            "font-weight: bold;")
        label_size = label.sizeHint()
        label.setGeometry(0, 0, label_size.width(), label_size.height())
        label.move(SCREEN_WIDTH // 2 - label_size.width() // 2, 0)
        label2 = QLabel("Choose the page replacement algorithm to try", self)
        label2.setFont(QFont("Helvetica", 25))
        label2.setStyleSheet("text-decoration: underline;"
                            "font-weight: bold;")
        label_size2 = label2.sizeHint()
        label2.setGeometry(0, 0, label_size2.width(), label_size2.height())
        label2.move(SCREEN_WIDTH // 2 - label_size2.width() // 2, 100)
        self.button_style = """
            QPushButton {
                background-color: #87cefa;
                color: #2c3e50;
                font-family: Helvetica;
                font-size: 14pt;
                font-weight: bold;
                border: 2px solid #4682b4;
                border-radius: 8px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #4682b4;
                color: white;
            }
        """
        self.addButtons()
        self.addTextBox()

    def addTextBox(self):
        only_int = QIntValidator()
        label = QLabel("Number of Frames: ", self)
        label.setFont(QFont("Helvetica", 20))
        self.line_frame = QLineEdit(self)
        self.line_frame.setFont(QFont("Helvetica", 20))
        self.line_frame.move(800, 300)
        self.line_frame.setValidator(only_int)
        label_size = label.sizeHint()
        label.move(800 - label_size.width(), 300)
        label2 = QLabel("Reference String: ", self)
        label2.setFont(QFont("Helvetica", 20))
        label_size2 = label2.sizeHint()
        self.ref_string = QLineEdit(self)
        self.ref_string.setFont(QFont("Helvetica", 20))
        self.ref_string.setGeometry(800, 350, 700, label_size2.height())
        label2.move(800 - label_size2.width(), 350)
    
    def addButtons(self):
        self.optimal = QPushButton("Optimal", self)
        self.fifo = QPushButton("FIFO", self)
        self.lru = QPushButton("LRU", self)
        self.exit = QPushButton("Exit", self)
        self.next = QPushButton("Next", self)
        self.back = QPushButton("Back", self)
        self.optimal.setStyleSheet(self.button_style)
        self.fifo.setStyleSheet(self.button_style)
        self.lru.setStyleSheet(self.button_style)
        self.exit.setStyleSheet(self.button_style)
        self.next.setStyleSheet(self.button_style)
        self.back.setStyleSheet(self.button_style)
        self.optimal.clicked.connect(self.optimal_page_replacement)
        self.fifo.clicked.connect(self.fifo_page_replacement)
        self.lru.clicked.connect(self.lru_page_replacement)
        self.exit.clicked.connect(self.exit_action)
        self.next.clicked.connect(self.nextButton)
        self.back.clicked.connect(self.backButton)
        x = 600
        self.optimal.move(x, 200)
        self.fifo.move(x + 200, 200)
        self.lru.move(x + 400, 200)
        self.exit.move(x + 600, 200)
        self.next.move(1300, 900)
        self.back.move(500, 900)
    
    def check_string(self, string: str, type: str):
        length_of_string = len(string)
        if length_of_string == 0:
            QMessageBox.warning(self, "Warning", f"Missing values in {type}")
            return False
        cnt_space = 0
        for i in range(length_of_string):
            if string[i] != ' ' and not string[i].isnumeric():
                QMessageBox.warning(self, "Warning", f"{string[i]} is not correct in {type}")
                return False
            elif string[i] == ' ':
                cnt_space += 1
                if cnt_space > 1:
                    QMessageBox.warning(self, "Warning", f"Too spaces in index {i} in {type}")
                    return False
            elif string[i].isnumeric():
                cnt_space = 0
            else:
                QMessageBox.warning(self, "Warning", f"Something went wrong in {i + 1} in {type}")
                return False
        return True
    
    def nextButton(self):
        if not self.started:
            QMessageBox.warning(self, "Warning", "You haven't chosen an algorithm yet")
            return
        if self.curr_block >= len(self.all_blocks):
            QMessageBox.warning(self, "Warning", "It's completed")
            return
        self.y_frames = 600
        self.x_frames += 80
        if self.pfs[self.curr_block] == "Yes":
            for i in range(len(self.all_blocks[self.curr_block])):
                frame = QLabel(f"{self.all_blocks[self.curr_block][i]}", self)
                frame.setFont(QFont("Helvetica", 30))
                frame.move(self.x_frames, self.y_frames)
                frame.setStyleSheet("""
                    QLabel {
                        background-color: lightblue;
                        border: 1px solid gray;
                    }
                """)
                frame.show()
                self.frames.append(frame)
                self.y_frames += frame.sizeHint().height()
        
        label_pf = QLabel(f"{self.pfs[self.curr_block]}", self)
        label_pf.setFont(QFont("Helvetica", 30))
        label_pf.move(self.x_pfs, self.y_pfs)
        label_pf.show()
        self.x_pfs += 80
        self.pfs_labels.append(label_pf)
        self.curr_block += 1
    
    def backButton(self):
        if not self.started:
            QMessageBox.warning(self, "Warning", "You haven't chosen an algorithm yet")
            return
        if self.curr_block < 2:
            QMessageBox.warning(self, "Warning", "Too far back")
            return
        if self.pfs[self.curr_block - 1] == "Yes":
            for i in range(len(self.frames) - int(self.line_frame.text()), len(self.frames)):
                self.frames[i].deleteLater()
                self.frames[i] = None
            for _ in range(3):
                self.frames.pop()
        self.pfs_labels[self.curr_block].deleteLater()
        self.pfs_labels[self.curr_block] = None
        self.pfs_labels.pop()
        self.x_frames -= 80
        self.x_pfs -= 80
        self.curr_block -= 1
    
    def start(self):
        self.started = True
        self.x_string = 150
        self.y_string = 500
        self.x_frames = 150
        self.y_frames = 600
        self.x_pfs = 150
        self.y_pfs = 400
        self.curr_block = 0
        if self.labels:
            for label in self.labels:
                label.deleteLater()
                label = None
            self.labels = []

        if self.pfs_labels:
            for label in self.pfs_labels:
                label.deleteLater()
                label = None
            self.pfs_labels = []

        if self.frames:
            for frame in self.frames:
                frame.deleteLater()
                frame = None
            self.frames = []

        for i in range(len(self.all_nums)):
            label = QLabel(f"{self.all_nums[i]}", self)
            label.setFont(QFont("Helvetica", 15))
            label.move(self.x_string, self.y_string)
            label.show()
            self.labels.append(label)
            self.x_string += 80

        for i in range(len(self.all_blocks[self.curr_block])):
            frame = QLabel(f"{self.all_blocks[self.curr_block][i]}", self)
            frame.setFont(QFont("Helvetica", 30))
            frame.move(self.x_frames, self.y_frames)
            frame.setStyleSheet("""
                QLabel {
                    background-color: lightblue;
                    border: 1px solid gray;
                }
            """)
            frame.show()
            self.frames.append(frame)
            self.y_frames += frame.sizeHint().height()
        
        page_fault_label = QLabel(f"Page Fault = {self.page_fault}", self)
        page_fault_label.setFont(QFont("Helvetica", 40))
        page_fault_label.move(100, 900)
        page_fault_label.show()
        self.pfs_labels.append(page_fault_label)
        
        pf = QLabel(f"{self.pfs[self.curr_block]}", self)
        pf.setFont(QFont("Helvetica", 30))
        pf.move(self.x_pfs, self.y_pfs)
        pf.show()
        self.pfs_labels.append(pf)
        self.x_pfs += 80
        
        self.curr_block += 1
    
    def optimal_page_replacement(self):
        if not self.check_string(self.line_frame.text(), "Number of Frames") or not self.check_string(self.ref_string.text(), "Reference String"):
            return
        self.all_blocks = []
        frames2 = []
        frames = int(self.line_frame.text())
        if frames > 5 or frames <= 0:
            QMessageBox.warning(self, "Warning", f"{frames} is too big (Max 5)")
            return
        f, page_fault, pf = [], 0, 'No'
        self.pfs = []
        s = self.ref_string.text()
        s = list(map(int, s.strip().split()))
        if len(s) > 20:
            QMessageBox.warning(self, "Warning", "Too many numbers in reference string (Max: 20)")
            return
        self.all_nums = s.copy()
        print(len(self.all_nums))
        occurance = [None for _ in range(frames)]
        for i in range(len(s)):
            if s[i] not in f:
                if len(f) < frames:
                    f.append(s[i])
                else:
                    for x in range(len(f)):
                        if f[x] not in s[i + 1:]:
                            f[x] = s[i]
                            break
                        else:
                            occurance[x] = s[i + 1:].index(f[x])
                    else:
                        f[occurance.index(max(occurance))] = s[i]
                page_fault += 1
                pf = 'Yes'
            else:
                pf = 'No'
            for x in f:
                frames2.append(x)
            for _ in range(frames - len(f)):
                frames2.append(' ')
            self.all_blocks.append(frames2)
            self.pfs.append(pf)
            frames2 = []
        self.page_fault = page_fault
        self.start()

    def fifo_page_replacement(self):
        if not self.check_string(self.line_frame.text(), "Number of Frames") or not self.check_string(self.ref_string.text(), "Reference String"):
            return
        self.all_blocks = []
        frames2 = []
        frames = int(self.line_frame.text())
        if frames > 5 or frames <= 0:
            QMessageBox.warning(self, "Warning", f"{frames} is too big")
            return
        f, page_fault, top, pf = [], 0, 0, 'No'
        self.pfs = []
        s = self.ref_string.text()
        s = list(map(int, s.strip().split()))
        if len(s) > 20:
            QMessageBox.warning(self, "Warning", "Too many numbers in reference string (Max: 20)")
            return
        self.all_nums = s.copy()
        for i in s:
            if i not in f:
                if len(f) < frames:
                    f.append(i)
                else:
                    f[top] = i
                    top = (top + 1) % frames
                page_fault += 1
                pf = 'Yes'
            else:
                pf = 'No'
            for x in f:
                frames2.append(x)
            for _ in range(frames - len(f)):
                frames2.append(' ')
            self.all_blocks.append(frames2)
            self.pfs.append(pf)
            frames2 = []
        self.page_fault = page_fault
        self.start()

    def lru_page_replacement(self):
        if not self.check_string(self.line_frame.text(), "Number of Frames") or not self.check_string(self.ref_string.text(), "Reference String"):
            return
        self.all_blocks = []
        frames2 = []
        frames = int(self.line_frame.text())
        if frames > 5 or frames <= 0:
            QMessageBox.warning(self, "Warning", f"{frames} is too big")
            return
        f, st, page_fault, pf = [], [], 0, 'No'
        self.pfs = []
        s = self.ref_string.text()
        s = list(map(int, s.strip().split()))
        if len(s) > 20:
            QMessageBox.warning(self, "Warning", "Too many numbers in reference string (Max: 20)")
            return
        self.all_nums = s.copy()
        for i in s:
            if i not in f:
                if len(f) < frames:
                    f.append(i)
                    st.append(len(f) - 1)
                else:
                    ind = st.pop(0)
                    f[ind] = i
                    st.append(ind)
                pf = 'Yes'
                page_fault += 1
            else:
                st.append(st.pop(st.index(f.index(i))))
                pf = 'No'
            for x in f:
                frames2.append(x)
            for _ in range(frames - len(f)):
                frames2.append(' ')
            self.all_blocks.append(frames2)
            self.pfs.append(pf)
            frames2 = []
        self.page_fault = page_fault
        self.start()
    
    def exit_action(self):
        reply = QMessageBox.question(self, "Exit", "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())