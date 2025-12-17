# GREEN 단계 최소 단위 구현 시나리오

## 목표
TDD의 GREEN 단계 원칙에 따라 최소한의 코드로 모든 테스트를 통과시키기

## 현재 상태
- ✅ RED 단계 완료: 테스트 케이스 10개 작성 완료
- ❌ 구현 코드 없음: `src/arithmetic.py` 파일 미존재
- ❌ 모든 테스트 실패: `ModuleNotFoundError: No module named 'src.arithmetic'`

## 구현 전략
**최소 단위 구현 원칙**: 각 단계마다 최소한의 코드만 작성하여 해당 테스트만 통과시키기

---

## 단계별 구현 시나리오

### Phase 1: 기본 구조 생성 (1단계)

**목표**: 모듈을 찾을 수 있도록 기본 구조만 생성

1. **파일 생성**
   - `src/arithmetic.py` 파일 생성
   - `Arithmetic` 클래스 선언만 추가 (메서드 없음)

2. **예상 결과**
   - `ModuleNotFoundError` 해결
   - 모든 테스트에서 `AttributeError: type object 'Arithmetic' has no attribute 'add'` 발생

3. **검증**
   ```bash
   pytest tests/test_arithmetic.py -v
   ```

---

### Phase 2: 우선순위 1 - `add()` 메서드 구현 (2단계)

**목표**: 덧셈 관련 테스트 3개 통과

#### 2-1. 최소 구현: 첫 번째 테스트 통과
1. **구현**
   - `add()` 정적 메서드 추가
   - 최소 구현: `return a + b` (양수 테스트 통과)

2. **테스트 실행**
   ```bash
   pytest tests/test_arithmetic.py::TestArithmetic::test_addition_positive_numbers -v
   ```

3. **예상 결과**
   - ✅ TC-001 통과
   - ❌ TC-002, TC-003도 통과 (덧셈은 기본 연산이므로)

#### 2-2. 검증: 모든 덧셈 테스트 통과 확인
1. **전체 덧셈 테스트 실행**
   ```bash
   pytest tests/test_arithmetic.py::TestArithmetic::test_addition_positive_numbers -v
   pytest tests/test_arithmetic.py::TestArithmetic::test_addition_with_zero -v
   pytest tests/test_arithmetic.py::TestArithmetic::test_addition_negative_numbers -v
   ```

2. **예상 결과**
   - ✅ TC-001, TC-002, TC-003 모두 통과
   - 덧셈은 기본 연산이므로 추가 로직 불필요

---

### Phase 3: 우선순위 2 - `subtract()` 메서드 구현 (3단계)

**목표**: 뺄셈 테스트 1개 통과

1. **구현**
   - `subtract()` 정적 메서드 추가
   - 최소 구현: `return a - b`

2. **테스트 실행**
   ```bash
   pytest tests/test_arithmetic.py::TestArithmetic::test_subtraction -v
   ```

3. **예상 결과**
   - ✅ TC-004 통과

---

### Phase 4: 우선순위 3 - `multiply()` 메서드 구현 (4단계)

**목표**: 곱셈 테스트 2개 통과

1. **구현**
   - `multiply()` 정적 메서드 추가
   - 최소 구현: `return a * b`

2. **테스트 실행**
   ```bash
   pytest tests/test_arithmetic.py::TestArithmetic::test_multiplication_negative_numbers -v
   pytest tests/test_arithmetic.py::TestArithmetic::test_multiplication_with_zero -v
   ```

3. **예상 결과**
   - ✅ TC-005, TC-006 모두 통과
   - 곱셈은 기본 연산이므로 추가 로직 불필요

---

### Phase 5: 우선순위 4 - `divide()` 메서드 구현 (5단계)

**목표**: 정수 나눗셈 테스트 3개 통과 (TC-007, TC-009, TC-010)

#### 5-1. 최소 구현: 정수 나눗셈 기본 로직
1. **구현**
   - `divide()` 정적 메서드 추가
   - 최소 구현: `return a // b` (정수 나눗셈 연산자 사용)

2. **테스트 실행**
   ```bash
   pytest tests/test_arithmetic.py::TestArithmetic::test_division_integer -v
   pytest tests/test_arithmetic.py::TestArithmetic::test_division_negative -v
   ```

3. **예상 결과**
   - ✅ TC-007 통과 (5 // 2 = 2)
   - ✅ TC-009 통과 (-10 // 2 = -5)
   - ❌ TC-010 실패 (0 // 0는 ZeroDivisionError 발생, ArithmeticError 필요)

#### 5-2. 예외 처리 추가: 0으로 나누기
1. **구현 수정**
   - `divide()` 메서드에 예외 처리 추가
   - `if b == 0: raise ArithmeticError()` 추가

2. **테스트 실행**
   ```bash
   pytest tests/test_arithmetic.py::TestArithmetic::test_division_by_zero -v
   ```

3. **예상 결과**
   - ✅ TC-010 통과 (ArithmeticError 발생)

#### 5-3. 전체 divide 테스트 확인
1. **전체 divide 테스트 실행**
   ```bash
   pytest tests/test_arithmetic.py::TestArithmetic::test_division_integer -v
   pytest tests/test_arithmetic.py::TestArithmetic::test_division_negative -v
   pytest tests/test_arithmetic.py::TestArithmetic::test_division_by_zero -v
   ```

2. **예상 결과**
   - ✅ TC-007, TC-009, TC-010 모두 통과

---

### Phase 6: 우선순위 5 - `quotient()` 메서드 구현 (6단계)

**목표**: 소수점 나눗셈 테스트 1개 통과

1. **구현**
   - `quotient()` 정적 메서드 추가
   - 최소 구현: `return a / b` (일반 나눗셈 연산자 사용)

2. **테스트 실행**
   ```bash
   pytest tests/test_arithmetic.py::TestArithmetic::test_division_quotient -v
   ```

3. **예상 결과**
   - ✅ TC-008 통과 (5 / 2 = 2.5)

---

### Phase 7: 최종 검증 (7단계)

**목표**: 모든 테스트 통과 확인

1. **전체 테스트 실행**
   ```bash
   pytest tests/test_arithmetic.py -v
   ```

2. **예상 결과**
   - ✅ 모든 테스트 통과 (10개)
   - ✅ 테스트 커버리지 100%

3. **README.md 체크리스트 업데이트**
   - 각 단계 완료 시 체크박스 체크

---

## 구현 코드 예상 구조

```python
# src/arithmetic.py

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
```

---

## 구현 순서 요약

| 단계 | 작업 | 테스트 ID | 예상 시간 |
|------|------|----------|----------|
| 1 | 기본 구조 생성 | - | 1분 |
| 2 | `add()` 메서드 | TC-001, TC-002, TC-003 | 2분 |
| 3 | `subtract()` 메서드 | TC-004 | 1분 |
| 4 | `multiply()` 메서드 | TC-005, TC-006 | 1분 |
| 5 | `divide()` 메서드 | TC-007, TC-009, TC-010 | 3분 |
| 6 | `quotient()` 메서드 | TC-008 | 1분 |
| 7 | 최종 검증 | 전체 (10개) | 1분 |

**총 예상 시간**: 약 10분

---

## 검증 기준

### 각 단계별 검증
- ✅ 해당 단계의 테스트가 통과하는가?
- ✅ 이전 단계의 테스트가 여전히 통과하는가? (회귀 테스트)
- ✅ 코드가 최소한으로 구현되었는가?

### 최종 검증
- ✅ 모든 테스트 케이스 통과 (10개)
- ✅ 테스트 커버리지 100%
- ✅ README.md 체크리스트 완료

---

## 주의사항

1. **최소 단위 원칙**: 각 단계에서 최소한의 코드만 작성
2. **점진적 구현**: 한 번에 하나의 기능만 구현
3. **테스트 우선**: 각 구현 후 즉시 테스트 실행
4. **회귀 방지**: 새 기능 추가 시 기존 테스트도 함께 실행

---

**시나리오 작성일**: 2025-12-16  
**승인 대기 중**: 사용자 승인 후 구현 진행

