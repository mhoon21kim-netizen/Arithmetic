"""
계산기 엔진 테스트 케이스
CalculatorEngine 클래스의 비즈니스 로직을 검증
"""
import pytest
from src.calculator_engine import CalculatorEngine


class TestCalculatorEngine:
    """계산기 엔진 테스트 클래스"""
    
    def setup_method(self):
        """각 테스트 전에 실행되는 설정 메서드"""
        self.engine = CalculatorEngine()
    
    def test_initial_state(self):
        """초기 상태 테스트"""
        assert self.engine.display == "0"
        assert self.engine.current_value == 0.0
        assert self.engine.pending_operation is None
        assert self.engine.waiting_for_operand is True
    
    def test_input_number(self):
        """숫자 입력 테스트"""
        result = self.engine.input_number("5")
        assert result == "5"
        assert self.engine.waiting_for_operand is False
    
    def test_input_multiple_numbers(self):
        """여러 숫자 입력 테스트"""
        self.engine.input_number("1")
        self.engine.input_number("2")
        self.engine.input_number("3")
        assert self.engine.display == "123"
    
    def test_input_decimal_point(self):
        """소수점 입력 테스트"""
        self.engine.input_number("5")
        self.engine.input_number(".")
        self.engine.input_number("2")
        assert self.engine.display == "5.2"
    
    def test_input_operator_addition(self):
        """덧셈 연산자 입력 테스트"""
        self.engine.input_number("5")
        result = self.engine.input_operator("+")
        assert result == "5"
        assert self.engine.pending_operation == "+"
        assert self.engine.current_value == 5.0
    
    def test_calculate_addition(self):
        """덧셈 계산 테스트"""
        self.engine.input_number("5")
        self.engine.input_operator("+")
        self.engine.input_number("3")
        result = self.engine.calculate()
        assert result == "8"
    
    def test_calculate_subtraction(self):
        """뺄셈 계산 테스트"""
        self.engine.input_number("10")
        self.engine.input_operator("-")
        self.engine.input_number("3")
        result = self.engine.calculate()
        assert result == "7"
    
    def test_calculate_multiplication(self):
        """곱셈 계산 테스트"""
        self.engine.input_number("5")
        self.engine.input_operator("×")
        self.engine.input_number("3")
        result = self.engine.calculate()
        assert result == "15"
    
    def test_calculate_division(self):
        """나눗셈 계산 테스트"""
        self.engine.input_number("10")
        self.engine.input_operator("/")
        self.engine.input_number("2")
        result = self.engine.calculate()
        assert result == "5"
    
    def test_calculate_division_by_zero(self):
        """0으로 나누기 예외 처리 테스트"""
        self.engine.input_number("10")
        self.engine.input_operator("/")
        self.engine.input_number("0")
        with pytest.raises(ArithmeticError):
            self.engine.calculate()
    
    def test_clear(self):
        """초기화 테스트"""
        self.engine.input_number("123")
        self.engine.input_operator("+")
        result = self.engine.clear()
        assert result == "0"
        assert self.engine.current_value == 0.0
        assert self.engine.pending_operation is None
    
    def test_toggle_sign_positive_to_negative(self):
        """부호 변경 테스트: 양수 → 음수"""
        self.engine.input_number("5")
        result = self.engine.toggle_sign()
        assert result == "-5"
    
    def test_toggle_sign_negative_to_positive(self):
        """부호 변경 테스트: 음수 → 양수"""
        self.engine.input_number("5")
        self.engine.toggle_sign()
        result = self.engine.toggle_sign()
        assert result == "5"
    
    def test_continuous_operations(self):
        """연속 연산 테스트"""
        # 5 + 3 - 2 = 6
        self.engine.input_number("5")
        self.engine.input_operator("+")
        self.engine.input_number("3")
        self.engine.input_operator("-")
        self.engine.input_number("2")
        result = self.engine.calculate()
        assert result == "6"
    
    def test_invalid_operator(self):
        """잘못된 연산자 입력 테스트"""
        self.engine.input_number("5")
        with pytest.raises(ValueError, match="지원하지 않는 연산자"):
            self.engine.input_operator("$")
    
    def test_format_result_integer(self):
        """정수 결과 포맷팅 테스트"""
        self.engine.input_number("5")
        self.engine.input_operator("+")
        self.engine.input_number("3")
        result = self.engine.calculate()
        # 정수는 소수점 없이 표시
        assert result == "8"
        assert "." not in result
    
    def test_format_result_decimal(self):
        """소수점 결과 포맷팅 테스트"""
        self.engine.input_number("5")
        self.engine.input_operator("÷")
        self.engine.input_number("2")
        result = self.engine.calculate()
        assert result == "2.5"

