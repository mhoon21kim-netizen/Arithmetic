"""
PyQt6 기반 계산기 GUI 애플리케이션
UI 렌더링 및 사용자 인터랙션을 담당하는 클래스
SOLID 원칙을 준수하여 설계됨
"""
import sys
import os
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

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
        """
        UI 구성 요소 설정
        
        README.md 4.2 구현 단계에 따른 구현:
        1. 기본 윈도우 생성
        2. 디스플레이 영역
        3. 버튼 그리드 생성
        4. 이벤트 연결
        5. 스타일링
        
        레이아웃:
        ┌─────────────────────┐
        │      Display        │  ← QLineEdit (읽기 전용)
        ├─────────────────────┤
        │  7  │  8  │  9  │ × │
        │  4  │  5  │  6  │ - │
        │  1  │  2  │  3  │ + │
        │ +/- │  0  │  .  │ = │
        └─────────────────────┘
        """
        # ============================================
        # 1. 기본 윈도우 생성
        # ============================================
        # QMainWindow 상속 (이미 상속됨)
        # 윈도우 크기 및 제목 설정
        self.setWindowTitle("계산기")
        self.setFixedSize(300, 400)
        
        # 중앙 위젯 생성
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # ============================================
        # 2. 디스플레이 영역
        # ============================================
        # QLineEdit 또는 QLabel 사용 (QLineEdit 선택)
        # 읽기 전용, 우측 정렬
        self.display = QLineEdit()
        self.display.setReadOnly(True)  # 읽기 전용
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)  # 우측 정렬
        self.display.setFont(QFont("Arial", 20))  # 폰트 설정
        self.display.setText("0")
        # 스타일링 (5단계에서 상세히 처리)
        self.display.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                background-color: #f5f5f5;
            }
        """)
        main_layout.addWidget(self.display)
        
        # ============================================
        # 3. 버튼 그리드 생성
        # ============================================
        # QGridLayout 사용
        button_layout = QGridLayout()
        button_layout.setSpacing(5)  # 레이아웃 간격 조정 (5단계)
        
        # 버튼 정의 (행, 열, 행span, 열span, 텍스트, 스타일)
        # - 숫자 버튼 (0-9)
        # - 연산자 버튼 (+, -, ×, ÷, =)
        # - 특수 버튼 (+/-, Clear)
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
            (3, 0, 1, 1, "+/-", "special"),  # 특수 버튼
            (3, 1, 1, 1, "0", "number"),     # 숫자 버튼
            (3, 2, 1, 1, ".", "number"),     # 숫자 버튼 (소수점)
            (3, 3, 1, 1, "=", "equals"),    # 연산자 버튼
        ]
        
        # 버튼 생성 및 배치
        for row, col, rowspan, colspan, text, button_type in buttons:
            button = self.create_button(text, button_type)  # 스타일링 적용 (5단계)
            button_layout.addWidget(button, row, col, rowspan, colspan)
            # 이벤트 연결은 4단계에서 처리
            self.connect_button(button, text, button_type)
        
        # Clear 버튼 추가 (특수 버튼)
        clear_button = self.create_button("C", "special")
        button_layout.addWidget(clear_button, 4, 0, 1, 4)
        self.connect_button(clear_button, "C", "special")
        
        main_layout.addLayout(button_layout)
    
    def create_button(self, text: str, button_type: str) -> QPushButton:
        """
        버튼 생성 및 스타일 적용
        
        README.md 4.2 구현 단계 - 5. 스타일링:
        - 버튼 크기 및 색상
        - 폰트 설정
        - 레이아웃 간격 조정
        
        Args:
            text: 버튼 텍스트
            button_type: 버튼 타입 (number, operator, equals, special)
        
        Returns:
            생성된 QPushButton
        """
        button = QPushButton(text)
        # 폰트 설정
        button.setFont(QFont("Arial", 16))
        # 버튼 크기 설정
        button.setMinimumHeight(60)
        
        # 버튼 타입별 스타일 적용 (색상)
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
        
        README.md 4.2 구현 단계 - 4. 이벤트 연결:
        - 버튼 클릭 → CalculatorEngine 메서드 호출
        - 결과 → 디스플레이 업데이트
        
        README.md 4.3 이벤트 처리 흐름:
        사용자 클릭 → on_number_clicked() / on_operator_clicked() → 
        CalculatorEngine.input_number() / input_operator() → 
        CalculatorEngine.calculate() (연산자 클릭 시) → 디스플레이 업데이트
        
        Args:
            button: 연결할 버튼
            text: 버튼 텍스트
            button_type: 버튼 타입
        """
        # 사용자 클릭 이벤트를 핸들러 메서드에 연결
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
        
        README.md 4.3 이벤트 처리 흐름:
        사용자 클릭
            ↓
        on_number_clicked() (현재 메서드)
            ↓
        CalculatorEngine.input_number()
            ↓
        디스플레이 업데이트
        
        Args:
            number: 클릭된 숫자 문자열
        """
        try:
            # 1단계: 사용자 클릭 → on_number_clicked() 호출됨 (이미 실행 중)
            # 2단계: CalculatorEngine.input_number() 메서드 호출
            display = self.engine.input_number(number)
            # 3단계: 디스플레이 업데이트
            self.display.setText(display)
        except Exception as e:
            self.display.setText("Error")
            print(f"오류 발생: {e}")
    
    def on_operator_clicked(self, operator: str):
        """
        연산자 버튼 클릭 핸들러
        
        README.md 4.3 이벤트 처리 흐름:
        사용자 클릭
            ↓
        on_operator_clicked() (현재 메서드)
            ↓
        CalculatorEngine.input_operator()
            ↓
        CalculatorEngine.calculate() (연산자 클릭 시, 연속 연산인 경우)
            ↓
        디스플레이 업데이트
        
        Args:
            operator: 클릭된 연산자 문자열
        """
        try:
            # 1단계: 사용자 클릭 → on_operator_clicked() 호출됨 (이미 실행 중)
            # 2단계: CalculatorEngine.input_operator() 메서드 호출
            #        (내부에서 연속 연산인 경우 calculate() 자동 호출)
            display = self.engine.input_operator(operator)
            # 3단계: 디스플레이 업데이트
            self.display.setText(display)
        except (ValueError, ArithmeticError) as e:
            self.display.setText("Error")
            print(f"오류 발생: {e}")
    
    def on_equals_clicked(self):
        """
        등호 버튼 클릭 핸들러
        
        README.md 4.3 이벤트 처리 흐름:
        사용자 클릭 (= 버튼)
            ↓
        on_equals_clicked() (현재 메서드)
            ↓
        CalculatorEngine.calculate()
            ↓
        디스플레이 업데이트
        """
        try:
            # 1단계: 사용자 클릭 → on_equals_clicked() 호출됨 (이미 실행 중)
            # 2단계: CalculatorEngine.calculate() 메서드 호출
            display = self.engine.calculate()
            # 3단계: 디스플레이 업데이트
            self.display.setText(display)
        except ArithmeticError as e:
            self.display.setText("Error: 0으로 나눌 수 없습니다")
            print(f"오류 발생: {e}")
        except Exception as e:
            self.display.setText("Error")
            print(f"오류 발생: {e}")
    
    def on_clear_clicked(self):
        """
        Clear 버튼 클릭 핸들러
        
        README.md 4.2 구현 단계 - 4. 이벤트 연결:
        버튼 클릭 → CalculatorEngine.clear() 메서드 호출
        결과 → 디스플레이 업데이트
        """
        # CalculatorEngine 메서드 호출
        display = self.engine.clear()
        # 결과 → 디스플레이 업데이트
        self.display.setText(display)
    
    def on_toggle_sign_clicked(self):
        """
        +/- 버튼 클릭 핸들러
        
        README.md 4.2 구현 단계 - 4. 이벤트 연결:
        버튼 클릭 → CalculatorEngine.toggle_sign() 메서드 호출
        결과 → 디스플레이 업데이트
        """
        # CalculatorEngine 메서드 호출
        display = self.engine.toggle_sign()
        # 결과 → 디스플레이 업데이트
        self.display.setText(display)


def main():
    """애플리케이션 진입점"""
    app = QApplication(sys.argv)
    calculator = CalculatorApp()
    calculator.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

