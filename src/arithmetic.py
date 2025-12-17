class Arithmetic:
    """사칙연산 클래스"""
    
    @staticmethod
    def add(a, b):
        """덧셈 연산"""
        return a + b
    
    @staticmethod
    def subtract(a, b):
        """뺄셈 연산"""
        return a - b
    
    @staticmethod
    def multiply(a, b):
        """곱셈 연산"""
        return a * b
    
    @staticmethod
    def divide(a, b):
        """정수 나눗셈 연산"""
        if b == 0:
            raise ArithmeticError("Division by zero")
        return a // b
    
    @staticmethod
    def quotient(a, b):
        """소수점 나눗셈 연산"""
        return a / b


if __name__ == "__main__":
    """간단한 사칙연산 콘솔 프로그램"""
    
    # 입력 화면
    print("입력화면")
    try:
        num1 = int(input("첫번째 정수값 >>"))
        operator = input("연산자>>")
        num2 = int(input("두번째 정수값>>"))
    except ValueError:
        print("올바른 정수를 입력해주세요.")
        exit(1)
    
    # 결과 뷰 화면
    print()
    print("결과 뷰 화면")
    print("=" * 30)
    
    # 연산자에 따른 계산 수행
    try:
        if operator == "+":
            result = Arithmetic.add(num1, num2)
            print(f"{num1} + {num2}을 계산합니다.")
            print("=" * 30)
            print(f"{num1}+{num2}={result}입니다.")
        elif operator == "-":
            result = Arithmetic.subtract(num1, num2)
            print(f"{num1} - {num2}을 계산합니다.")
            print("=" * 30)
            print(f"{num1}-{num2}={result}입니다.")
        elif operator == "*":
            result = Arithmetic.multiply(num1, num2)
            print(f"{num1} * {num2}을 계산합니다.")
            print("=" * 30)
            print(f"{num1}*{num2}={result}입니다.")
        elif operator == "/":
            result = Arithmetic.divide(num1, num2)
            print(f"{num1} / {num2}을 계산합니다.")
            print("=" * 30)
            print(f"{num1}/{num2}={result}입니다.")
        elif operator == "//":
            result = Arithmetic.divide(num1, num2)
            print(f"{num1} // {num2}을 계산합니다.")
            print("=" * 30)
            print(f"{num1}//{num2}={result}입니다.")
        elif operator == "÷" or operator == "÷":
            result = Arithmetic.quotient(num1, num2)
            print(f"{num1} ÷ {num2}을 계산합니다.")
            print("=" * 30)
            print(f"{num1}÷{num2}={result}입니다.")
        else:
            print(f"지원하지 않는 연산자입니다: {operator}")
            print("지원하는 연산자: +, -, *, /, //, ÷")
            exit(1)
    except ArithmeticError as e:
        print(f"오류가 발생했습니다: {e}")
        exit(1)

