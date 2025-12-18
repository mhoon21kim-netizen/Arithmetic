"""
계산기 엔진 모듈
비즈니스 로직과 상태 관리를 담당하는 클래스
SOLID 원칙을 준수하여 설계됨
"""
from typing import Optional, Dict, Callable
from src.arithmetic import Arithmetic


class CalculatorEngine:
    """
    계산기 엔진 클래스
    
    책임:
    - 계산기 상태 관리 (현재 값, 대기 중인 연산자 등)
    - 숫자 및 연산자 입력 처리
    - 계산 수행
    
    SOLID 원칙:
    - SRP: 계산 상태 관리만 담당
    - DIP: Arithmetic 클래스에 의존 (추상화)
    """
    
    # 연산자 매핑 딕셔너리 (Magic String 제거, OCP 준수)
    OPERATION_MAP: Dict[str, Callable[[float, float], float]] = {
        '+': Arithmetic.add,
        '-': Arithmetic.subtract,
        '*': Arithmetic.multiply,
        '×': Arithmetic.multiply,
        '/': Arithmetic.divide,
        '÷': Arithmetic.quotient,
    }
    
    def __init__(self):
        """계산기 엔진 초기화"""
        self.current_value: float = 0.0
        self.pending_operation: Optional[str] = None
        self.pending_value: Optional[float] = None
        self.display: str = "0"
        self.waiting_for_operand: bool = True
    
    def input_number(self, number: str) -> str:
        """
        숫자 입력 처리
        
        Args:
            number: 입력된 숫자 문자열 (0-9, '.')
        
        Returns:
            업데이트된 디스플레이 문자열
        """
        if self.waiting_for_operand:
            self.display = number
            self.waiting_for_operand = False
        else:
            if number == '.':
                if '.' not in self.display:
                    self.display += number
            else:
                if self.display == "0":
                    self.display = number
                else:
                    self.display += number
        
        return self.display
    
    def input_operator(self, operator: str) -> str:
        """
        연산자 입력 처리
        
        Args:
            operator: 연산자 문자열 (+, -, *, ×, /, ÷)
        
        Returns:
            업데이트된 디스플레이 문자열
        """
        if operator not in self.OPERATION_MAP:
            raise ValueError(f"지원하지 않는 연산자입니다: {operator}")
        
        input_value = float(self.display)
        
        if self.pending_operation is None:
            # 첫 번째 연산자 입력
            self.current_value = input_value
        else:
            # 연속 연산 수행 (이전 연산자로 계산)
            if not self.waiting_for_operand:
                # 새로운 숫자가 입력된 경우에만 계산
                try:
                    self.current_value = self._calculate(
                        self.pending_operation,
                        self.current_value,
                        input_value
                    )
                    self.display = self._format_result(self.current_value)
                except ArithmeticError as e:
                    self.clear()
                    raise e
        
        self.pending_operation = operator
        self.pending_value = self.current_value
        self.waiting_for_operand = True
        
        return self.display
    
    def calculate(self) -> str:
        """
        계산 수행 (= 버튼 클릭 시)
        
        Returns:
            계산 결과 디스플레이 문자열
        
        Raises:
            ArithmeticError: 0으로 나누기 등의 수학적 오류
        """
        if self.pending_operation is None:
            return self.display
        
        input_value = float(self.display)
        
        try:
            result = self._calculate(
                self.pending_operation,
                self.current_value,
                input_value
            )
            self.display = self._format_result(result)
            self.current_value = result
            self.pending_operation = None
            self.pending_value = None
            self.waiting_for_operand = True
        except ArithmeticError as e:
            self.clear()
            raise e
        
        return self.display
    
    def _calculate(self, operator: str, a: float, b: float) -> float:
        """
        실제 계산 수행 (내부 메서드)
        
        Args:
            operator: 연산자
            a: 첫 번째 피연산자
            b: 두 번째 피연산자
        
        Returns:
            계산 결과
        
        Raises:
            ArithmeticError: 0으로 나누기 등의 수학적 오류
        """
        operation_func = self.OPERATION_MAP.get(operator)
        if operation_func is None:
            raise ValueError(f"지원하지 않는 연산자입니다: {operator}")
        
        # 정수 연산인 경우 정수로 변환
        if operator in ['/', '//']:
            return operation_func(int(a), int(b))
        else:
            return operation_func(a, b)
    
    def _format_result(self, value: float) -> str:
        """
        결과 포맷팅 (불필요한 소수점 제거)
        
        Args:
            value: 포맷팅할 값
        
        Returns:
            포맷팅된 문자열
        """
        if value == int(value):
            return str(int(value))
        return str(value)
    
    def clear(self) -> str:
        """
        계산기 초기화
        
        Returns:
            초기화된 디스플레이 문자열 ("0")
        """
        self.current_value = 0.0
        self.pending_operation = None
        self.pending_value = None
        self.display = "0"
        self.waiting_for_operand = True
        return self.display
    
    def clear_entry(self) -> str:
        """
        현재 입력만 초기화 (CE 기능)
        
        Returns:
            초기화된 디스플레이 문자열 ("0")
        """
        self.display = "0"
        self.waiting_for_operand = True
        return self.display
    
    def toggle_sign(self) -> str:
        """
        부호 변경 (+/- 버튼)
        
        Returns:
            부호가 변경된 디스플레이 문자열
        """
        if self.display != "0":
            if self.display.startswith('-'):
                self.display = self.display[1:]
            else:
                self.display = '-' + self.display
        return self.display

