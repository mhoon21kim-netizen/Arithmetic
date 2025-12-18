"""
PyQt6 기반 계산기 GUI 애플리케이션
UI 렌더링 및 사용자 인터랙션을 담당하는 클래스
SOLID 원칙을 준수하여 설계됨
"""
import sys
from enum import Enum
from dataclasses import dataclass
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QGridLayout, QPushButton, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import Callable
from abc import ABC, abstractmethod
from src.calculator_engine import CalculatorEngine


# ============================================
# 상수 및 Enum 정의 (우선순위 1 - 단계 2)
# ============================================

class ButtonType(Enum):
    """버튼 타입 Enum"""
    NUMBER = "number"
    OPERATOR = "operator"
    EQUALS = "equals"
    SPECIAL = "special"


class ButtonConfig:
    """버튼 설정 상수 클래스"""
    # 폰트 설정
    FONT_FAMILY = "Arial"
    FONT_SIZE_DISPLAY = 20
    FONT_SIZE_BUTTON = 16
    
    # 버튼 크기 설정
    BUTTON_HEIGHT = 60
    
    # 레이아웃 설정
    LAYOUT_SPACING = 5
    
    # 윈도우 설정
    WINDOW_TITLE = "계산기"
    WINDOW_WIDTH = 300
    WINDOW_HEIGHT = 400
    
    # 색상 상수
    COLOR_NUMBER_BG = "#ffffff"
    COLOR_NUMBER_HOVER = "#f0f0f0"
    COLOR_NUMBER_PRESSED = "#e0e0e0"
    
    COLOR_OPERATOR_BG = "#f5f5f5"
    COLOR_OPERATOR_HOVER = "#e8e8e8"
    COLOR_OPERATOR_PRESSED = "#d0d0d0"
    
    COLOR_EQUALS_BG = "#4A90E2"
    COLOR_EQUALS_HOVER = "#357ABD"
    COLOR_EQUALS_PRESSED = "#2E6DA4"
    COLOR_EQUALS_TEXT = "white"
    
    COLOR_SPECIAL_BG = "#f9f9f9"
    COLOR_SPECIAL_HOVER = "#e8e8e8"
    COLOR_SPECIAL_PRESSED = "#d0d0d0"
    
    # 디스플레이 스타일
    COLOR_DISPLAY_BG = "#f5f5f5"
    COLOR_DISPLAY_BORDER = "#ccc"
    
    # 스타일시트 상수 (추가 개선: Magic Numbers 제거)
    BORDER_RADIUS = "5px"
    BORDER_WIDTH_BUTTON = "1px"
    BORDER_WIDTH_DISPLAY = "2px"
    DISPLAY_PADDING = "10px"
    
    # 버튼 텍스트 상수
    BUTTON_CLEAR = "C"
    BUTTON_TOGGLE_SIGN = "+/-"
    BUTTON_EQUALS = "="
    BUTTON_DECIMAL = "."  # 우선순위 3 개선: 소수점 버튼 상수화
    
    # 디스플레이 초기값
    DISPLAY_INITIAL_VALUE = "0"


# ============================================
# 데이터 구조화 (우선순위 3 - 단계 1)
# ============================================

@dataclass
class ButtonDefinition:
    """
    버튼 정의 데이터 클래스
    
    Long Parameter List 해결을 위한 데이터 구조화
    """
    row: int
    col: int
    rowspan: int
    colspan: int
    text: str
    button_type: ButtonType


class ButtonLayoutConfig:
    """
    버튼 레이아웃 설정 클래스
    
    책임:
    - 버튼 레이아웃 정의 관리
    - 데이터와 로직 분리
    
    SOLID 원칙:
    - SRP: 레이아웃 설정만 담당
    """
    
    @staticmethod
    def get_button_definitions() -> list[ButtonDefinition]:
        """
        버튼 정의 리스트 반환
        
        Returns:
            버튼 정의 리스트
        """
        return [
            # 첫 번째 행: 7, 8, 9, ×
            ButtonDefinition(0, 0, 1, 1, "7", ButtonType.NUMBER),
            ButtonDefinition(0, 1, 1, 1, "8", ButtonType.NUMBER),
            ButtonDefinition(0, 2, 1, 1, "9", ButtonType.NUMBER),
            ButtonDefinition(0, 3, 1, 1, "×", ButtonType.OPERATOR),
            
            # 두 번째 행: 4, 5, 6, -
            ButtonDefinition(1, 0, 1, 1, "4", ButtonType.NUMBER),
            ButtonDefinition(1, 1, 1, 1, "5", ButtonType.NUMBER),
            ButtonDefinition(1, 2, 1, 1, "6", ButtonType.NUMBER),
            ButtonDefinition(1, 3, 1, 1, "-", ButtonType.OPERATOR),
            
            # 세 번째 행: 1, 2, 3, +
            ButtonDefinition(2, 0, 1, 1, "1", ButtonType.NUMBER),
            ButtonDefinition(2, 1, 1, 1, "2", ButtonType.NUMBER),
            ButtonDefinition(2, 2, 1, 1, "3", ButtonType.NUMBER),
            ButtonDefinition(2, 3, 1, 1, "+", ButtonType.OPERATOR),
            
            # 네 번째 행: +/-, 0, ., /
            ButtonDefinition(3, 0, 1, 1, ButtonConfig.BUTTON_TOGGLE_SIGN, ButtonType.SPECIAL),
            ButtonDefinition(3, 1, 1, 1, "0", ButtonType.NUMBER),
            ButtonDefinition(3, 2, 1, 1, ButtonConfig.BUTTON_DECIMAL, ButtonType.NUMBER),  # 우선순위 3 개선: Magic String 제거
            ButtonDefinition(3, 3, 1, 1, "/", ButtonType.OPERATOR),
        ]
    
    @staticmethod
    def get_special_buttons() -> list[ButtonDefinition]:
        """
        특수 버튼 정의 (C, =)
        
        우선순위 2 개선: 타입 일관성을 위해 list[ButtonDefinition]로 통일
        row, col 정보는 ButtonDefinition에 이미 포함되어 있음
        
        Returns:
            ButtonDefinition 리스트
        """
        return [
            ButtonDefinition(4, 0, 1, 2, ButtonConfig.BUTTON_CLEAR, ButtonType.SPECIAL),
            ButtonDefinition(4, 2, 1, 2, ButtonConfig.BUTTON_EQUALS, ButtonType.EQUALS),
        ]


# ============================================
# 인터페이스 정의 (우선순위 3 - 단계 2)
# ============================================

class ICalculatorEngine(ABC):
    """
    계산기 엔진 인터페이스
    
    의존성 역전 원칙(DIP) 준수를 위한 인터페이스 정의
    
    SOLID 원칙:
    - DIP: 추상화에 의존하도록 설계
    """
    
    @abstractmethod
    def input_number(self, number: str) -> str:
        """
        숫자 입력 처리
        
        Args:
            number: 입력된 숫자 문자열
        
        Returns:
            업데이트된 디스플레이 문자열
        """
        pass
    
    @abstractmethod
    def input_operator(self, operator: str) -> str:
        """
        연산자 입력 처리
        
        Args:
            operator: 연산자 문자열
        
        Returns:
            업데이트된 디스플레이 문자열
        """
        pass
    
    @abstractmethod
    def calculate(self) -> str:
        """
        계산 수행
        
        Returns:
            계산 결과 디스플레이 문자열
        """
        pass
    
    @abstractmethod
    def clear(self) -> str:
        """
        계산기 초기화
        
        Returns:
            초기화된 디스플레이 문자열
        """
        pass
    
    @abstractmethod
    def toggle_sign(self) -> str:
        """
        부호 변경
        
        Returns:
            부호가 변경된 디스플레이 문자열
        """
        pass


# ============================================
# 스타일 관리 클래스 (우선순위 2 - 단계 1)
# ============================================

class ButtonStyleManager:
    """
    버튼 스타일 관리 클래스
    
    책임:
    - 버튼 타입별 스타일시트 생성
    - 스타일 관리 중앙화
    
    SOLID 원칙:
    - SRP: 스타일 관리만 담당
    - OCP: 딕셔너리 기반으로 새 스타일 추가 용이
    
    추가 개선: 템플릿 메서드 패턴 적용으로 중복 코드 제거
    """
    
    @staticmethod
    def get_style(button_type: ButtonType) -> str:
        """
        버튼 타입에 따른 스타일 반환
        
        Args:
            button_type: 버튼 타입 (ButtonType Enum)
        
        Returns:
            스타일시트 문자열
        """
        styles = {
            ButtonType.NUMBER: ButtonStyleManager._number_style(),
            ButtonType.OPERATOR: ButtonStyleManager._operator_style(),
            ButtonType.EQUALS: ButtonStyleManager._equals_style(),
            ButtonType.SPECIAL: ButtonStyleManager._special_style(),
        }
        return styles.get(button_type, "")
    
    @staticmethod
    def _create_style(
        bg_color: str,
        hover_color: str,
        pressed_color: str,
        border_color: str = None,
        text_color: str = None
    ) -> str:
        """
        스타일시트 템플릿 메서드 (추가 개선: 템플릿 메서드 패턴)
        
        중복된 스타일시트 코드를 제거하고 공통 템플릿을 사용
        
        Args:
            bg_color: 배경색
            hover_color: 호버 시 배경색
            pressed_color: 클릭 시 배경색
            border_color: 테두리 색상 (기본값: COLOR_DISPLAY_BORDER)
            text_color: 텍스트 색상 (기본값: None, 기본 텍스트 색상 사용)
        
        Returns:
            스타일시트 문자열
        """
        border = border_color or ButtonConfig.COLOR_DISPLAY_BORDER
        color_style = f"color: {text_color};" if text_color else ""
        
        return f"""
            QPushButton {{
                background-color: {bg_color};
                border: {ButtonConfig.BORDER_WIDTH_BUTTON} solid {border};
                border-radius: {ButtonConfig.BORDER_RADIUS};
                {color_style}
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
            }}
        """
    
    @staticmethod
    def _number_style() -> str:
        """숫자 버튼 스타일"""
        return ButtonStyleManager._create_style(
            ButtonConfig.COLOR_NUMBER_BG,
            ButtonConfig.COLOR_NUMBER_HOVER,
            ButtonConfig.COLOR_NUMBER_PRESSED
        )
    
    @staticmethod
    def _operator_style() -> str:
        """연산자 버튼 스타일"""
        return ButtonStyleManager._create_style(
            ButtonConfig.COLOR_OPERATOR_BG,
            ButtonConfig.COLOR_OPERATOR_HOVER,
            ButtonConfig.COLOR_OPERATOR_PRESSED
        )
    
    @staticmethod
    def _equals_style() -> str:
        """등호 버튼 스타일"""
        return ButtonStyleManager._create_style(
            ButtonConfig.COLOR_EQUALS_BG,
            ButtonConfig.COLOR_EQUALS_HOVER,
            ButtonConfig.COLOR_EQUALS_PRESSED,
            border_color=ButtonConfig.COLOR_EQUALS_HOVER,
            text_color=ButtonConfig.COLOR_EQUALS_TEXT
        )
    
    @staticmethod
    def _special_style() -> str:
        """특수 버튼 스타일"""
        return ButtonStyleManager._create_style(
            ButtonConfig.COLOR_SPECIAL_BG,
            ButtonConfig.COLOR_SPECIAL_HOVER,
            ButtonConfig.COLOR_SPECIAL_PRESSED
        )


# ============================================
# 버튼 팩토리 클래스 (우선순위 2 - 단계 2)
# ============================================

class ButtonFactory:
    """
    버튼 생성 팩토리 클래스
    
    책임:
    - 버튼 생성 및 스타일 적용
    - 버튼 생성 로직 중앙화
    
    SOLID 원칙:
    - SRP: 버튼 생성만 담당
    - OCP: 새 버튼 타입 추가 시 확장 가능
    """
    
    @staticmethod
    def create_button(text: str, button_type: ButtonType) -> QPushButton:
        """
        버튼 생성 및 스타일 적용
        
        Args:
            text: 버튼 텍스트
            button_type: 버튼 타입 (ButtonType Enum)
        
        Returns:
            생성된 QPushButton
        """
        button = QPushButton(text)
        # 폰트 설정
        button.setFont(QFont(ButtonConfig.FONT_FAMILY, ButtonConfig.FONT_SIZE_BUTTON))
        # 버튼 크기 설정
        button.setMinimumHeight(ButtonConfig.BUTTON_HEIGHT)
        # 스타일 적용
        button.setStyleSheet(ButtonStyleManager.get_style(button_type))
        return button


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
    
    def __init__(self, engine: ICalculatorEngine = None):
        """
        계산기 애플리케이션 초기화
        
        Args:
            engine: 계산기 엔진 (의존성 주입, 기본값: CalculatorEngine)
        """
        super().__init__()
        # 의존성 역전 원칙(DIP) 준수: 인터페이스에 의존
        self.engine = engine or CalculatorEngine()
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
        │ +/- │  0  │  .  │ / │
        │     C    │    =     │
        └─────────────────────┘
        """
        self._setup_window()
        self._setup_display()
        self._setup_button_grid()
    
    def _setup_window(self):
        """
        기본 윈도우 생성 (우선순위 1 - 단계 3: 메서드 분해)
        
        QMainWindow 상속 (이미 상속됨)
        윈도우 크기 및 제목 설정
        """
        self.setWindowTitle(ButtonConfig.WINDOW_TITLE)
        self.setFixedSize(ButtonConfig.WINDOW_WIDTH, ButtonConfig.WINDOW_HEIGHT)
        
        # 중앙 위젯 생성
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        self.main_layout = QVBoxLayout()
        central_widget.setLayout(self.main_layout)
    
    def _setup_display(self):
        """
        디스플레이 영역 설정 (우선순위 1 - 단계 3: 메서드 분해)
        
        QLineEdit 또는 QLabel 사용 (QLineEdit 선택)
        읽기 전용, 우측 정렬
        """
        self.display = QLineEdit()
        self.display.setReadOnly(True)  # 읽기 전용
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)  # 우측 정렬
        self.display.setFont(QFont(ButtonConfig.FONT_FAMILY, ButtonConfig.FONT_SIZE_DISPLAY))
        self.display.setText(ButtonConfig.DISPLAY_INITIAL_VALUE)
        
        # 스타일링 (추가 개선: Magic Numbers 제거)
        self.display.setStyleSheet(f"""
            QLineEdit {{
                border: {ButtonConfig.BORDER_WIDTH_DISPLAY} solid {ButtonConfig.COLOR_DISPLAY_BORDER};
                border-radius: {ButtonConfig.BORDER_RADIUS};
                padding: {ButtonConfig.DISPLAY_PADDING};
                background-color: {ButtonConfig.COLOR_DISPLAY_BG};
            }}
        """)
        self.main_layout.addWidget(self.display)
    
    def _setup_button_grid(self):
        """
        버튼 그리드 생성 (우선순위 1 - 단계 3: 메서드 분해)
        
        QGridLayout 사용
        - 숫자 버튼 (0-9)
        - 연산자 버튼 (+, -, ×, /, =)
        - 특수 버튼 (+/-, Clear)
        
        우선순위 2 개선: 일반 버튼과 특수 버튼을 동일한 방식으로 처리하여 코드 중복 제거
        """
        # QGridLayout 사용
        button_layout = QGridLayout()
        button_layout.setSpacing(ButtonConfig.LAYOUT_SPACING)
        
        # 모든 버튼 정의 가져오기 (일반 버튼 + 특수 버튼)
        all_button_definitions = (
            ButtonLayoutConfig.get_button_definitions() + 
            ButtonLayoutConfig.get_special_buttons()
        )
        
        # 버튼 생성 및 배치 (ButtonFactory 사용)
        # 우선순위 2 개선: 일반 버튼과 특수 버튼을 동일한 방식으로 처리
        for btn_def in all_button_definitions:
            button = ButtonFactory.create_button(btn_def.text, btn_def.button_type)
            button_layout.addWidget(button, btn_def.row, btn_def.col, btn_def.rowspan, btn_def.colspan)
            self.connect_button(button, btn_def.text, btn_def.button_type)
        
        self.main_layout.addLayout(button_layout)
    
    def connect_button(self, button: QPushButton, text: str, button_type: ButtonType):
        """
        버튼 이벤트 연결
        
        README.md 4.2 구현 단계 - 4. 이벤트 연결:
        - 버튼 클릭 → CalculatorEngine 메서드 호출
        - 결과 → 디스플레이 업데이트
        
        README.md 4.3 이벤트 처리 흐름:
        사용자 클릭 → on_number_clicked() / on_operator_clicked() → 
        CalculatorEngine.input_number() / input_operator() → 
        CalculatorEngine.calculate() (연산자 클릭 시) → 디스플레이 업데이트
        
        우선순위 4 개선: 딕셔너리 매핑을 사용하여 조건문 단순화
        - 순환 복잡도 감소
        - OCP 준수 (새 버튼 타입 추가 시 확장 용이)
        
        Args:
            button: 연결할 버튼
            text: 버튼 텍스트
            button_type: 버튼 타입 (ButtonType Enum)
        """
        # 우선순위 4 개선: 버튼 타입별 핸들러 매핑 (딕셔너리 전략 패턴)
        handler_map = {
            ButtonType.NUMBER: lambda: self.on_number_clicked(text),
            ButtonType.OPERATOR: lambda: self.on_operator_clicked(text),
            ButtonType.EQUALS: self.on_equals_clicked,
        }
        
        # 특수 버튼 텍스트별 핸들러 매핑
        special_handler_map = {
            ButtonConfig.BUTTON_CLEAR: self.on_clear_clicked,
            ButtonConfig.BUTTON_TOGGLE_SIGN: self.on_toggle_sign_clicked,
        }
        
        # 핸들러 연결
        if button_type in handler_map:
            # 일반 버튼 타입 (NUMBER, OPERATOR, EQUALS)
            button.clicked.connect(handler_map[button_type])
        elif button_type == ButtonType.SPECIAL and text in special_handler_map:
            # 특수 버튼 타입 (C, +/-)
            button.clicked.connect(special_handler_map[text])
    
    # ============================================
    # 이벤트 핸들러 통합 (우선순위 2 - 단계 3)
    # ============================================
    
    def _handle_calculation(self, action: Callable[[], str], error_title: str = "계산 오류"):
        """
        공통 계산 핸들러 (우선순위 2 - 단계 3: 이벤트 핸들러 통합)
        
        중복된 에러 처리 로직을 통합하여 DRY 원칙 준수
        
        Args:
            action: 실행할 계산 액션 (Callable)
            error_title: 에러 대화상자 제목
        """
        try:
            display = action()
            self.display.setText(display)
        except ArithmeticError as e:
            self._show_error_dialog(error_title, "0으로 나눌 수 없습니다.")
            self._reset_calculator()
        except ValueError as e:
            self._show_error_dialog("연산자 오류", f"지원하지 않는 연산자입니다:\n{str(e)}")
            self._reset_calculator()
        except Exception as e:
            self._show_error_dialog(error_title, f"오류가 발생했습니다:\n{str(e)}")
            self._reset_calculator()
    
    def _reset_calculator(self):
        """
        계산기 상태 초기화 (우선순위 2 - 단계 3: 중복 코드 제거)
        
        에러 발생 시 계산기 상태를 초기화하는 공통 로직
        """
        self.display.setText(ButtonConfig.DISPLAY_INITIAL_VALUE)
        self.engine.clear()
    
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
        self._handle_calculation(
            lambda: self.engine.input_number(number),
            "입력 오류"
        )
    
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
        self._handle_calculation(
            lambda: self.engine.input_operator(operator),
            "연산자 오류"
        )
    
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
        self._handle_calculation(
            lambda: self.engine.calculate(),
            "계산 오류"
        )
    
    def on_clear_clicked(self):
        """
        Clear 버튼 클릭 핸들러
        
        README.md 4.2 구현 단계 - 4. 이벤트 연결:
        버튼 클릭 → CalculatorEngine.clear() 메서드 호출
        결과 → 디스플레이 업데이트
        
        우선순위 1 개선: 일관된 에러 처리를 위해 _handle_calculation() 사용
        """
        self._handle_calculation(
            lambda: self.engine.clear(),
            "초기화 오류"
        )
    
    def on_toggle_sign_clicked(self):
        """
        +/- 버튼 클릭 핸들러
        
        README.md 4.2 구현 단계 - 4. 이벤트 연결:
        버튼 클릭 → CalculatorEngine.toggle_sign() 메서드 호출
        결과 → 디스플레이 업데이트
        
        우선순위 1 개선: 일관된 에러 처리를 위해 _handle_calculation() 사용
        """
        self._handle_calculation(
            lambda: self.engine.toggle_sign(),
            "부호 변경 오류"
        )
    
    def _show_error_dialog(self, title: str, message: str):
        """
        에러 대화상자 표시
        
        Args:
            title: 대화상자 제목
            message: 에러 메시지
        """
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()


def main():
    """애플리케이션 진입점"""
    app = QApplication(sys.argv)
    calculator = CalculatorApp()
    calculator.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

