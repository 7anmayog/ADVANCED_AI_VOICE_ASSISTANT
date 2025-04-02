from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QStackedWidget, 
                            QWidget, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QFrame, QLabel, QSizePolicy)
from PyQt5.QtGui import (QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, 
                        QPixmap, QTextBlockFormat, QLinearGradient, QBrush, QPalette)
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtGui import QTextOption
from dotenv import dotenv_values
import sys
import os

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + ","
        else:
            new_query += "."

    return new_query.capitalize()

def SetMicrophoneStatus(Command):
    with open(rf'{TempDirPath}\Mic.data', "w", encoding='utf-8') as file:
        file.write(Command)

def GetMicrophoneStatus():
    with open(rf'{TempDirPath}\Mic.data', "r", encoding='utf-8') as file:
        return file.read()

def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}\Status1.data', "w", encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    with open(rf'{TempDirPath}\Status1.data', "r", encoding='utf-8') as file:
        return file.read()

def GraphicsDirectoryPath(Filename):
    return rf'{GraphicsDirPath}\{Filename}'

def TempDirectoryPath(Filename):
    return rf'{TempDirPath}\{Filename}'

def ShowTextToScreen(Text):
    with open(TempDirectoryPath("Responses.data"), "w", encoding='utf-8') as file:
        file.write(Text)

class ChatSection(QWidget):
    def __init__(self):
        super().__init__()
        
        # Solid background (no transparency)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(15, 25, 45))
        self.setPalette(palette)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Solid chat text edit
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #0f1a2f;
                border: 2px solid #3a4a6a;
                border-radius: 8px;
                color: #e0e0ff;
                font-size: 14px;
                padding: 12px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(30, 40, 70, 0.5);
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #5a6a9a;
                min-height: 20px;
                border-radius: 4px;
            }
        """)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        self.chat_text_edit.setLineWrapMode(QTextEdit.WidgetWidth)
        self.chat_text_edit.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        layout.addWidget(self.chat_text_edit)


        # Animated GIF label
        self.gif_label = QLabel()
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
        movie.setScaledSize(QSize(300, 200))
        self.gif_label.setMovie(movie)
        movie.start()

        # Status label with animation
        self.label = QLabel("Ready")
        self.label.setStyleSheet("""
            QLabel {
                color: #a0b0ff;
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
                background-color: rgba(20, 40, 80, 0.7);
                border-radius: 4px;
            }
        """)
        self.label.setAlignment(Qt.AlignRight)

        # Add widgets with proper spacing
        layout.addWidget(self.label)
        layout.addWidget(self.gif_label)
        layout.setStretch(0, 1)

        # Message animation setup
        self.message_animation = QPropertyAnimation(self.chat_text_edit.viewport(), b"pos")
        self.message_animation.setDuration(300)
        self.message_animation.setEasingCurve(QEasingCurve.OutQuad)

        # Timer for updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)

    def loadMessages(self):
        global old_chat_message
        try:
            with open(TempDirectoryPath('Responses.data'), "r", encoding='utf-8') as file:
                messages = file.read()

                if messages and str(old_chat_message) != str(messages):
                    self.animateMessageAppearance()
                    self.addMessage(message=messages, color='#e0e0ff')
                    old_chat_message = messages
        except Exception as e:
            print(f"Error loading messages: {e}")

    def animateMessageAppearance(self):
        self.message_animation.setStartValue(QPoint(0, 20))
        self.message_animation.setEndValue(QPoint(0, 0))
        self.message_animation.start()

    def SpeechRecogText(self):
        try:
            with open(TempDirectoryPath('Status1.data'), "r", encoding='utf-8') as file:
                status = file.read()
                self.label.setText(status)
        except Exception as e:
            print(f"Error reading status: {e}")

    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        format = QTextCharFormat()
        format.setForeground(QColor(color))
        
        block_format = QTextBlockFormat()
        block_format.setTopMargin(10)
        block_format.setLeftMargin(10)
        
        cursor.setBlockFormat(block_format)
        cursor.setCharFormat(format)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)
        self.chat_text_edit.ensureCursorVisible()

class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Gradient background
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(10, 20, 40))
        gradient.setColorAt(1, QColor(0, 5, 15))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Animated GIF
        gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
        movie.setScaledSize(QSize(min(600, screen_width//2), min(400, screen_height//2)))
        gif_label.setMovie(movie)
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()

        # ====== MICROPHONE BUTTON FIX ======
        # Mic button with hover effect
        self.mic_icon = QPixmap(GraphicsDirectoryPath('Mic_on.png'))
        self.muted_icon = QPixmap(GraphicsDirectoryPath('Mic_off.png'))
        
        self.icon_label = QLabel()
        self.icon_label.setPixmap(self.mic_icon.scaled(
            80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("""
            QLabel {
                background-color: rgba(30, 50, 90, 0.7);
                border-radius: 40px;
                padding: 10px;
            }
            QLabel:hover {
                background-color: rgba(50, 70, 110, 0.9);
            }
        """)
        
        # Connect click handler
        self.icon_label.mousePressEvent = self.toggle_mic
        self.mic_muted = False
        # ====== END MICROPHONE BUTTON FIX ======

        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #a0b0ff;
                font-size: 16px;
                font-weight: bold;
                padding: 8px 15px;
                background-color: rgba(20, 40, 80, 0.7);
                border-radius: 12px;
            }
        """)
        self.status_label.setAlignment(Qt.AlignCenter)

        # Add widgets to layout
        layout.addStretch(1)
        layout.addWidget(gif_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.icon_label)
        layout.addStretch(1)

        # Timer for status updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)

    # ====== ADD THIS NEW METHOD ======
    def toggle_mic(self, event):
        self.mic_muted = not self.mic_muted
        if self.mic_muted:
            self.icon_label.setPixmap(self.muted_icon.scaled(
                80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
            SetMicrophoneStatus("False")
        else:
            self.icon_label.setPixmap(self.mic_icon.scaled(
                80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
            SetMicrophoneStatus("True")

    def SpeechRecogText(self):
        try:
            with open(TempDirectoryPath('Status1.data'), "r", encoding='utf-8') as file:
                self.status_label.setText(file.read())
        except Exception as e:
            print(f"Error reading status: {e}")

class MessageScreen(QWidget):  # MOVED BEFORE MainWindow
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Gradient background
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(10, 20, 40))
        gradient.setColorAt(1, QColor(0, 5, 15))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        # Layout setup
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Add chat section
        self.chat_section = ChatSection()
        layout.addWidget(self.chat_section)

class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.setFixedHeight(50)
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a3a;
                border-bottom: 1px solid #3a3a6a;
            }
            QPushButton {
                background-color: transparent;
                color: #e0e0ff;
                border: none;
                padding: 8px 15px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
            }
            QLabel {
                color: #e0e0ff;
                font-size: 16px;
                font-weight: bold;
                padding-left: 15px;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(5)

        # Title label
        title_label = QLabel(f" {Assistantname} AI ")
        title_label.setStyleSheet("font-size: 18px;")

        # Navigation buttons
        home_button = QPushButton("Home")
        home_button.setIcon(QIcon(GraphicsDirectoryPath("Home.png")))
        home_button.clicked.connect(lambda: self.switchScreen(0))
        
        chat_button = QPushButton("Chat")
        chat_button.setIcon(QIcon(GraphicsDirectoryPath("Chats.png")))
        chat_button.clicked.connect(lambda: self.switchScreen(1))

        # Window control buttons
        minimize_button = QPushButton()
        minimize_button.setIcon(QIcon(GraphicsDirectoryPath('Minimize2.png')))
        minimize_button.clicked.connect(self.minimizeWindow)
        
        self.maximize_button = QPushButton()
        self.maximize_button.setIcon(QIcon(GraphicsDirectoryPath('Maximize.png')))
        self.maximize_button.clicked.connect(self.maximizeWindow)
        
        close_button = QPushButton()
        close_button.setIcon(QIcon(GraphicsDirectoryPath('Close.png')))
        close_button.clicked.connect(self.closeWindow)
        close_button.setStyleSheet("""
            QPushButton:hover {
                background-color: #ff5555;
            }
        """)

        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(chat_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)

        # Draggable window setup
        self.draggable = True
        self.offset = None

    def switchScreen(self, index):
        # Animate screen transition
        animation = QPropertyAnimation(self.stacked_widget, b"pos")
        animation.setDuration(300)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        if index > self.stacked_widget.currentIndex():
            animation.setStartValue(QPoint(-50, 0))
        else:
            animation.setStartValue(QPoint(50, 0))
            
        animation.setEndValue(QPoint(0, 0))
        animation.start()
        self.stacked_widget.setCurrentIndex(index)

    def minimizeWindow(self):
        self.parent().showMinimized()

    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(QIcon(GraphicsDirectoryPath('Maximize.png')))
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(QIcon(GraphicsDirectoryPath('Minimize.png')))

    def closeWindow(self):
        self.parent().close()

    def mousePressEvent(self, event):
        if self.draggable and event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and self.offset is not None and event.buttons() == Qt.LeftButton:
            self.parent().move(event.globalPos() - self.offset)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Window shadow effect
        self.shadow = QFrame(self)
        self.shadow.setStyleSheet("""
            background: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(30, 50, 100, 150),
                stop:1 rgba(10, 20, 50, 150));
            border-radius: 10px;
        """)
        self.shadow.setGeometry(10, 10, self.width()-20, self.height()-20)
        
        # Main container
        self.container = QWidget()
        self.container.setStyleSheet("""
            background-color: #0a0a1a;
            border-radius: 10px;
            border: 1px solid #3a4a7a;
        """)
        
        # Window animation
        self.opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_animation.setDuration(500)
        self.opacity_animation.setStartValue(0)
        self.opacity_animation.setEndValue(1)
        self.opacity_animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        # Setup UI
        self.initUI()
        self.opacity_animation.start()

    def initUI(self):
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        
        self.setGeometry(100, 100, int(screen_width//2), int(screen_height//1.5))
        
        # Stacked widget for screens
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(InitialScreen())
        self.stacked_widget.addWidget(MessageScreen())
        
        # Custom title bar
        self.top_bar = CustomTopBar(self, self.stacked_widget)
        self.setMenuWidget(self.top_bar)
        
        # Main layout
        main_layout = QVBoxLayout(self.container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.stacked_widget)
        
        self.setCentralWidget(self.container)
        
        # Resize handler
        self.resize_timer = QTimer()
        self.resize_timer.timeout.connect(self.updateShadow)
        self.resize_timer.start(100)

    def updateShadow(self):
        self.shadow.setGeometry(10, 10, self.width()-20, self.height()-20)

    def resizeEvent(self, event):
        self.updateShadow()
        super().resizeEvent(event)

def GraphicalUserInterface():
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Dark palette
    palette = app.palette()
    palette.setColor(QPalette.Window, QColor(10, 20, 40))
    palette.setColor(QPalette.WindowText, QColor(220, 220, 255))
    palette.setColor(QPalette.Base, QColor(15, 25, 45))
    palette.setColor(QPalette.AlternateBase, QColor(20, 30, 50))
    palette.setColor(QPalette.ToolTipBase, QColor(200, 200, 255))
    palette.setColor(QPalette.ToolTipText, QColor(20, 20, 40))
    palette.setColor(QPalette.Text, QColor(220, 220, 255))
    palette.setColor(QPalette.Button, QColor(30, 40, 70))
    palette.setColor(QPalette.ButtonText, QColor(220, 220, 255))
    palette.setColor(QPalette.Highlight, QColor(80, 100, 160))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUserInterface()

    
