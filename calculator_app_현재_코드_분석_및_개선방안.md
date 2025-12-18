# calculator_app.py 현재 코드 분석 및 개선 방안 (업데이트)

## 현재 상태 요약

### ✅ 이미 개선된 사항 (우선순위 1 완료)
- ✅ Dead Code 제거: `import os` 제거 완료
- ✅ 상수 정의: `ButtonType` Enum, `ButtonConfig` 클래스 생성 완료
- ✅ 메서드 분해: `setup_ui()` 메서드를 3개 메서드로 분리 완료
- ✅ 에러 대화상자: QMessageBox를 사용한 에러 처리 추가 완료

---

## 1단계: 코드 스멜 분석 (현재 상태)

### 1.1 발견된 코드 스멜

#### 1. Duplicate Code (중복 코드) ⚠️
- **위치**: 
  - 이벤트 핸들러 메서드들 (`on_number_clicked`, `on_operator_clicked`, `on_equals_clicked`)
  - 스타일시트 생성 로직 (`create_button()` 메서드 내부)
- **문제점**:
  - 이벤트 핸들러들이 동일한 패턴 반복 (try-except, display 업데이트, 에러 처리)
  - 스타일시트가 거의 동일한 구조 반복 (4개의 if-elif 분기)
- **영향**: DRY 원칙 위반, 유지보수 비용 증가

#### 2. Long Method (긴 메서드) ⚠️
- **위치**: `create_button()` 메서드 (약 80줄)
- **문제점**: 
  - 스타일시트 생성 로직이 메서드 내부에 하드코딩
  - 4개의 if-elif 분기로 버튼 타입별 스타일 처리
- **영향**: 가독성 저하, 유지보수 어려움

#### 3. Feature Envy (기능 질투) ⚠️
- **위치**: `create_button()` 메서드
- **문제점**:
  - 스타일시트 로직이 UI 클래스에 혼재
  - 스타일 관리가 CalculatorApp 클래스의 책임이 아님
- **영향**: 응집도 저하, SRP 위반

#### 4. Long Parameter List (긴 매개변수 리스트) ⚠️
- **위치**: 버튼 정의 튜플 `(row, col, rowspan, colspan, text, button_type)`
- **문제점**: 6개의 매개변수로 가독성 저하
- **영향**: 가독성 저하, 실수 가능성 증가

#### 5. Primitive Obsession (원시 타입 집착) ⚠️
- **위치**: 버튼 정의를 튜플로 처리
- **문제점**: 
  - 버튼 정의를 튜플로 표현하여 의미 파악 어려움
  - 데이터 클래스나 NamedTuple 사용 권장
- **영향**: 가독성 저하, 타입 안정성 부족

#### 6. 중복된 에러 처리 로직 ⚠️
- **위치**: 
  - `on_operator_clicked()`와 `on_equals_clicked()`에서 동일한 에러 처리
  - `self.display.setText("0")` 반복
  - `self.engine.clear()` 반복
- **문제점**: 에러 처리 로직이 여러 곳에 중복
- **영향**: DRY 원칙 위반

---

## 2단계: 정적 분석

### 2.1 순환 복잡도 (Cyclomatic Complexity)

#### 높은 복잡도 메서드
1. **`create_button()`**: 복잡도 4
   - 4개의 if-elif 분기 (버튼 타입별 스타일)

2. **`connect_button()`**: 복잡도 5
   - 4개의 if-elif 분기 + 중첩된 if (SPECIAL 타입 처리)

3. **`_setup_button_grid()`**: 복잡도 3
   - 버튼 생성 루프 + 특수 버튼 처리

### 2.2 결합도 (Coupling)

#### 높은 결합도
- **PyQt6 위젯에 강하게 결합**: `QPushButton`, `QLineEdit`, `QGridLayout`, `QMessageBox` 등
- **CalculatorEngine에 의존**: 하지만 인터페이스가 아닌 구체 클래스에 의존
- **스타일시트 하드코딩**: 스타일 변경 시 코드 수정 필요

### 2.3 응집도 (Cohesion)

#### 낮은 응집도
- **스타일 관리가 UI 클래스에 혼재**: `create_button()`에서 스타일시트 생성
- **에러 처리 로직 분산**: 각 핸들러에 에러 처리 로직이 분산

### 2.4 코드 메트릭

| 메트릭 | 값 | 평가 |
|--------|-----|------|
| 파일 크기 | 482줄 | 보통 |
| 클래스 수 | 3 (ButtonType, ButtonConfig, CalculatorApp) | 적절 |
| 메서드 수 | 12 | 적절 |
| 평균 메서드 길이 | ~40줄 | 적절 |
| 최대 메서드 길이 | 80줄 | 다소 김 |
| 순환 복잡도 | 4-5 | 보통 |

---

## 3단계: SOLID 원칙 분석

### 3.1 SRP (Single Responsibility Principle) - 단일 책임 원칙

#### 위반 사항
1. **`CalculatorApp` 클래스가 여전히 여러 책임**
   - UI 렌더링 ✅
   - 이벤트 핸들링 ✅
   - 스타일 관리 ⚠️ (Feature Envy)
   - 에러 처리 ⚠️ (중복)

2. **`create_button()` 메서드가 너무 많은 일을 수행**
   - 버튼 생성
   - 스타일시트 생성
   - 스타일 적용

#### 개선 방안
- 스타일 관리를 별도 클래스로 분리 (`ButtonStyleManager`)
- 에러 처리를 공통 메서드로 추출

### 3.2 OCP (Open/Closed Principle) - 개방/폐쇄 원칙

#### 위반 사항
1. **새로운 버튼 타입 추가 시 `create_button()` 수정 필요**
   - if-elif 체인으로 버튼 타입 처리
   - 새로운 타입 추가 시 코드 수정 필요

2. **스타일 변경 시 코드 수정 필요**
   - 스타일시트가 메서드 내부에 하드코딩

#### 개선 방안
- Strategy 패턴으로 버튼 스타일 관리
- Factory 패턴으로 버튼 생성
- 딕셔너리 기반 스타일 매핑

### 3.3 LSP (Liskov Substitution Principle) - 리스코프 치환 원칙

#### 준수 상태
- ✅ 현재 상속 관계가 없어 해당 없음

### 3.4 ISP (Interface Segregation Principle) - 인터페이스 분리 원칙

#### 준수 상태
- ✅ 현재 인터페이스가 없어 해당 없음

### 3.5 DIP (Dependency Inversion Principle) - 의존성 역전 원칙

#### 위반 사항
1. **구체 클래스에 직접 의존**
   - `CalculatorEngine` 구체 클래스에 직접 의존
   - 인터페이스나 추상 클래스 부재

2. **PyQt6 위젯에 직접 의존**
   - `QPushButton`, `QLineEdit` 등 구체 위젯에 직접 의존

#### 개선 방안
- `CalculatorEngine`에 대한 인터페이스 정의 (`ICalculatorEngine`)
- 위젯 팩토리 패턴 적용 (선택사항)

---

## 4단계: 개선 방안 (단계별)

### 4.1 단계 1: 스타일 관리 분리 (우선순위 2)

**목표**: 스타일시트 로직을 별도 클래스로 분리

**구현 내용**:
```python
class ButtonStyleManager:
    """버튼 스타일 관리 클래스"""
    
    @staticmethod
    def get_style(button_type: ButtonType) -> str:
        """버튼 타입에 따른 스타일 반환"""
        styles = {
            ButtonType.NUMBER: ButtonStyleManager._number_style(),
            ButtonType.OPERATOR: ButtonStyleManager._operator_style(),
            ButtonType.EQUALS: ButtonStyleManager._equals_style(),
            ButtonType.SPECIAL: ButtonStyleManager._special_style(),
        }
        return styles.get(button_type, "")
    
    @staticmethod
    def _number_style() -> str:
        return f"""
            QPushButton {{
                background-color: {ButtonConfig.COLOR_NUMBER_BG};
                border: 1px solid {ButtonConfig.COLOR_DISPLAY_BORDER};
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {ButtonConfig.COLOR_NUMBER_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {ButtonConfig.COLOR_NUMBER_PRESSED};
            }}
        """
    # ... 기타 스타일 메서드
```

**효과**:
- Feature Envy 해결
- 스타일 관리 중앙화
- OCP 준수 (새 스타일 추가 용이)
- `create_button()` 메서드 단순화

### 4.2 단계 2: 버튼 팩토리 패턴 적용 (우선순위 2)

**목표**: 버튼 생성 로직 분리, OCP 준수

**구현 내용**:
```python
class ButtonFactory:
    """버튼 생성 팩토리"""
    
    @staticmethod
    def create_button(text: str, button_type: ButtonType) -> QPushButton:
        """버튼 생성 및 스타일 적용"""
        button = QPushButton(text)
        button.setFont(QFont(ButtonConfig.FONT_FAMILY, ButtonConfig.FONT_SIZE_BUTTON))
        button.setMinimumHeight(ButtonConfig.BUTTON_HEIGHT)
        button.setStyleSheet(ButtonStyleManager.get_style(button_type))
        return button
```

**효과**:
- 버튼 생성 로직 분리
- SRP 준수
- 재사용성 향상
- `CalculatorApp` 클래스 단순화

### 4.3 단계 3: 이벤트 핸들러 통합 (우선순위 2)

**목표**: 중복 코드 제거, 공통 패턴 추출

**구현 내용**:
```python
class CalculatorApp(QMainWindow):
    def _handle_calculation(self, action: Callable[[], str], error_title: str = "계산 오류"):
        """공통 계산 핸들러"""
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
        """계산기 상태 초기화"""
        self.display.setText("0")
        self.engine.clear()
    
    def on_number_clicked(self, number: str):
        """숫자 버튼 클릭 핸들러"""
        self._handle_calculation(
            lambda: self.engine.input_number(number),
            "입력 오류"
        )
    
    def on_operator_clicked(self, operator: str):
        """연산자 버튼 클릭 핸들러"""
        self._handle_calculation(
            lambda: self.engine.input_operator(operator),
            "연산자 오류"
        )
    
    def on_equals_clicked(self):
        """등호 버튼 클릭 핸들러"""
        self._handle_calculation(
            lambda: self.engine.calculate(),
            "계산 오류"
        )
```

**효과**:
- Duplicate Code 제거
- 에러 처리 중앙화
- 유지보수성 향상
- 코드 라인 수 감소

### 4.4 단계 4: 버튼 설정 데이터 구조화 (우선순위 3)

**목표**: 버튼 정의를 데이터 구조로 분리

**구현 내용**:
```python
from dataclasses import dataclass

@dataclass
class ButtonDefinition:
    """버튼 정의 데이터 클래스"""
    row: int
    col: int
    rowspan: int
    colspan: int
    text: str
    button_type: ButtonType

class ButtonLayoutConfig:
    """버튼 레이아웃 설정"""
    
    @staticmethod
    def get_button_definitions() -> list[ButtonDefinition]:
        """버튼 정의 리스트 반환"""
        return [
            ButtonDefinition(0, 0, 1, 1, "7", ButtonType.NUMBER),
            ButtonDefinition(0, 1, 1, 1, "8", ButtonType.NUMBER),
            # ...
        ]
    
    @staticmethod
    def get_special_buttons() -> list[tuple[ButtonDefinition, int, int]]:
        """특수 버튼 정의 (C, =)"""
        return [
            (ButtonDefinition(4, 0, 1, 2, ButtonConfig.BUTTON_CLEAR, ButtonType.SPECIAL), 4, 0),
            (ButtonDefinition(4, 2, 1, 2, ButtonConfig.BUTTON_EQUALS, ButtonType.EQUALS), 4, 2),
        ]
```

**효과**:
- Long Parameter List 해결
- 데이터와 로직 분리
- 가독성 향상
- 타입 안정성 향상

### 4.5 단계 5: 인터페이스 정의 (우선순위 3)

**목표**: 의존성 역전 원칙 준수

**구현 내용**:
```python
from abc import ABC, abstractmethod

class ICalculatorEngine(ABC):
    """계산기 엔진 인터페이스"""
    
    @abstractmethod
    def input_number(self, number: str) -> str:
        pass
    
    @abstractmethod
    def input_operator(self, operator: str) -> str:
        pass
    
    @abstractmethod
    def calculate(self) -> str:
        pass
    
    @abstractmethod
    def clear(self) -> str:
        pass
    
    @abstractmethod
    def toggle_sign(self) -> str:
        pass

class CalculatorApp(QMainWindow):
    def __init__(self, engine: ICalculatorEngine = None):
        super().__init__()
        self.engine = engine or CalculatorEngine()  # 의존성 주입
        self.setup_ui()
```

**효과**:
- DIP 준수
- 테스트 용이성 향상 (Mock 객체 사용 가능)
- 결합도 감소

---

## 5단계: 개선 우선순위

### 우선순위 1 (즉시 개선) ✅ 완료
1. ✅ Dead Code 제거
2. ✅ 상수 정의
3. ✅ 메서드 분해

### 우선순위 2 (단기 개선)
4. ⏳ **스타일 관리 분리**: `ButtonStyleManager` 클래스 생성
5. ⏳ **버튼 팩토리**: `ButtonFactory` 클래스 생성
6. ⏳ **이벤트 핸들러 통합**: 공통 핸들러 메서드 생성

### 우선순위 3 (중기 개선)
7. ⏳ **데이터 구조화**: `ButtonDefinition` 데이터 클래스
8. ⏳ **인터페이스 정의**: `ICalculatorEngine` 인터페이스

---

## 6단계: 개선 효과 예상

### 코드 품질 지표 개선

| 지표 | 현재 | 우선순위 2 후 | 우선순위 3 후 |
|------|------|---------------|---------------|
| 최대 메서드 길이 | 80줄 | ~30줄 | ~25줄 |
| 순환 복잡도 | 4-5 | 2-3 | 2 |
| 중복 코드 | 보통 | 낮음 | 매우 낮음 |
| Magic String | 0 | 0 | 0 |
| 결합도 | 높음 | 중간 | 낮음 |

### SOLID 원칙 준수도

| 원칙 | 현재 | 우선순위 2 후 | 우선순위 3 후 |
|------|------|---------------|---------------|
| SRP | ⚠️ 부분 위반 | ✅ 준수 | ✅ 준수 |
| OCP | ⚠️ 위반 | ✅ 준수 | ✅ 준수 |
| LSP | ✅ 해당 없음 | ✅ 해당 없음 | ✅ 해당 없음 |
| ISP | ✅ 해당 없음 | ✅ 해당 없음 | ✅ 해당 없음 |
| DIP | ⚠️ 위반 | ⚠️ 부분 위반 | ✅ 준수 |

---

## 7단계: 구현 체크리스트

### 우선순위 2 구현 체크리스트

- [ ] **4.1 단계**: 스타일 관리 분리
  - [ ] `ButtonStyleManager` 클래스 생성
  - [ ] 스타일시트 메서드 분리
  - [ ] `create_button()` 메서드 리팩토링

- [ ] **4.2 단계**: 버튼 팩토리 패턴
  - [ ] `ButtonFactory` 클래스 생성
  - [ ] 버튼 생성 로직 이동
  - [ ] `CalculatorApp`에서 팩토리 사용

- [ ] **4.3 단계**: 이벤트 핸들러 통합
  - [ ] `_handle_calculation()` 메서드 생성
  - [ ] `_reset_calculator()` 메서드 생성
  - [ ] 이벤트 핸들러 리팩토링

### 우선순위 3 구현 체크리스트

- [ ] **4.4 단계**: 데이터 구조화
  - [ ] `ButtonDefinition` 데이터 클래스 생성
  - [ ] `ButtonLayoutConfig` 클래스 생성
  - [ ] 버튼 정의 리팩토링

- [ ] **4.5 단계**: 인터페이스 정의
  - [ ] `ICalculatorEngine` 인터페이스 생성
  - [ ] 의존성 주입 개선
  - [ ] 테스트 코드 작성

---

## 결론

현재 코드는 우선순위 1 단계를 완료하여 상당히 개선되었습니다. 
하지만 여전히 다음과 같은 개선 여지가 있습니다:

**주요 개선 포인트**:
1. 스타일 관리 분리 (Feature Envy 해결)
2. 버튼 팩토리 패턴 (OCP 준수)
3. 이벤트 핸들러 통합 (Duplicate Code 제거)
4. 데이터 구조화 (가독성 향상)
5. 인터페이스 정의 (DIP 준수)

이러한 개선을 통해 더 깔끔하고 유지보수하기 쉬운 코드가 됩니다.

