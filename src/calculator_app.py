"""
PyQt6 기반 계산기 GUI 애플리케이션
UI 렌더링 및 사용자 인터랙션을 담당하는 클래스
SOLID 원칙을 준수하여 설계됨
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QGridLayout, QPushButton, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.calculator_engine import CalculatorEngine


class CalculatorApp(QMainWindow):
    """
    계산기 GUI 애플리케이션 클래스
    
    책임:
    - UI 렌더링
    - 사용자 입력 처리
    - 이벤트 핸들링
    
    SOLID 원칙:
    - SRP: UI만 담당
    - DIP: CalculatorEngine에 의존 (구현이 아닌 인터페이스)
    """
    
    def __init__(self):
        """계산기 애플리케이션 초기화"""
        super().__init__()
        self.engine = CalculatorEngine()  # 의존성 주입
        self.setup_ui()
    
    def setup_ui(self):
        """UI 구성 요소 설정"""
        self.setWindowTitle("계산기")
        self.setFixedSize(300, 400)
        
        # 중앙 위젯 생성
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 디스플레이 (결과 표시 영역)
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFont(QFont("Arial", 20))
        self.display.setText("0")
        self.display.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                background-color: #f5f5f5;
            }
        """)
        main_layout.addWidget(self.display)
        
        # 버튼 그리드 레이아웃
        button_layout = QGridLayout()
        button_layout.setSpacing(5)
        
        # 버튼 정의 (행, 열, 행span, 열span, 텍스트, 스타일)
        buttons = [
            # 첫 번째 행: 7, 8, 9, ×
            (0, 0, 1, 1, "7", "number"),
            (0, 1, 1, 1, "8", "number"),
            (0, 2, 1, 1, "9", "number"),
            (0, 3, 1, 1, "×", "operator"),
            
            # 두 번째 행: 4, 5, 6, -
            (1, 0, 1, 1, "4", "number"),
            (1, 1, 1, 1, "5", "number"),
            (1, 2, 1, 1, "6", "number"),
            (1, 3, 1, 1, "-", "operator"),
            
            # 세 번째 행: 1, 2, 3, +
            (2, 0, 1, 1, "1", "number"),
            (2, 1, 1, 1, "2", "number"),
            (2, 2, 1, 1, "3", "number"),
            (2, 3, 1, 1, "+", "operator"),
            
            # 네 번째 행: +/-, 0, ., =
            (3, 0, 1, 1, "+/-", "special"),
            (3, 1, 1, 1, "0", "number"),
            (3, 2, 1, 1, ".", "number"),
            (3, 3, 1, 1, "=", "equals"),
        ]
        
        # 버튼 생성 및 배치
        for row, col, rowspan, colspan, text, button_type in buttons:
            button = self.create_button(text, button_type)
            button_layout.addWidget(button, row, col, rowspan, colspan)
            self.connect_button(button, text, button_type)
        
        # Clear 버튼 추가 (선택사항)
        clear_button = self.create_button("C", "special")
        button_layout.addWidget(clear_button, 4, 0, 1, 4)
        self.connect_button(clear_button, "C", "special")
        
        main_layout.addLayout(button_layout)
    
    def create_button(self, text: str, button_type: str) -> QPushButton:
        """
        버튼 생성 및 스타일 적용
        
        Args:
            text: 버튼 텍스트
            button_type: 버튼 타입 (number, operator, equals, special)
        
        Returns:
            생성된 QPushButton
        """
        button = QPushButton(text)
        button.setFont(QFont("Arial", 16))
        button.setMinimumHeight(60)
        
        # 버튼 타입별 스타일 적용
        if button_type == "number":
            button.setStyleSheet("""
                QPushButton {
                    background-color: #ffffff;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                }
                QPushButton:pressed {
                    background-color: #e0e0e0;
                }
            """)
        elif button_type == "operator":
            button.setStyleSheet("""
                QPushButton {
                    background-color: #f5f5f5;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #e8e8e8;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """)
        elif button_type == "equals":
            button.setStyleSheet("""
                QPushButton {
                    background-color: #4A90E2;
                    color: white;
                    border: 1px solid #357ABD;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #357ABD;
                }
                QPushButton:pressed {
                    background-color: #2E6DA4;
                }
            """)
        else:  # special
            button.setStyleSheet("""
                QPushButton {
                    background-color: #f9f9f9;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #e8e8e8;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """)
        
        return button
    
    def connect_button(self, button: QPushButton, text: str, button_type: str):
        """
        버튼 이벤트 연결
        
        Args:
            button: 연결할 버튼
            text: 버튼 텍스트
            button_type: 버튼 타입
        """
        if button_type == "number":
            button.clicked.connect(lambda: self.on_number_clicked(text))
        elif button_type == "operator":
            button.clicked.connect(lambda: self.on_operator_clicked(text))
        elif button_type == "equals":
            button.clicked.connect(self.on_equals_clicked)
        else:  # special
            if text == "C":
                button.clicked.connect(self.on_clear_clicked)
            elif text == "+/-":
                button.clicked.connect(self.on_toggle_sign_clicked)
    
    def on_number_clicked(self, number: str):
        """
        숫자 버튼 클릭 핸들러
        
        Args:
            number: 클릭된 숫자 문자열
        """
        try:
            display = self.engine.input_number(number)
            self.display.setText(display)
        except Exception as e:
            self.display.setText("Error")
            print(f"오류 발생: {e}")
    
    def on_operator_clicked(self, operator: str):
        """
        연산자 버튼 클릭 핸들러
        
        Args:
            operator: 클릭된 연산자 문자열
        """
        try:
            display = self.engine.input_operator(operator)
            self.display.setText(display)
        except (ValueError, ArithmeticError) as e:
            self.display.setText("Error")
            print(f"오류 발생: {e}")
    
    def on_equals_clicked(self):
        """등호 버튼 클릭 핸들러"""
        try:
            display = self.engine.calculate()
            self.display.setText(display)
        except ArithmeticError as e:
            self.display.setText("Error: 0으로 나눌 수 없습니다")
            print(f"오류 발생: {e}")
        except Exception as e:
            self.display.setText("Error")
            print(f"오류 발생: {e}")
    
    def on_clear_clicked(self):
        """Clear 버튼 클릭 핸들러"""
        display = self.engine.clear()
        self.display.setText(display)
    
    def on_toggle_sign_clicked(self):
        """+/- 버튼 클릭 핸들러"""
        display = self.engine.toggle_sign()
        self.display.setText(display)


def main():
    """애플리케이션 진입점"""
    app = QApplication(sys.argv)
    calculator = CalculatorApp()
    calculator.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

