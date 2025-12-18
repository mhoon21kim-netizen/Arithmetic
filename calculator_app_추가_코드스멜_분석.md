# calculator_app.py 추가 코드 스멜 분석

## 발견된 추가 코드 스멜

### 1. Inconsistent Error Handling (일관성 없는 에러 처리)

**위치**: `on_clear_clicked()`, `on_toggle_sign_clicked()` 메서드

**문제점**:
- 다른 이벤트 핸들러들(`on_number_clicked`, `on_operator_clicked`, `on_equals_clicked`)은 `_handle_calculation()`을 사용하여 일관된 에러 처리를 함
- 하지만 `on_clear_clicked()`와 `on_toggle_sign_clicked()`는 직접 구현되어 에러 처리가 없음
- 에러 발생 시 예외가 처리되지 않아 애플리케이션이 크래시할 수 있음

**현재 코드**:
```python
def on_clear_clicked(self):
    display = self.engine.clear()  # 에러 처리 없음
    self.display.setText(display)

def on_toggle_sign_clicked(self):
    display = self.engine.toggle_sign()  # 에러 처리 없음
    self.display.setText(display)
```

**영향**: 
- DRY 원칙 위반
- 일관성 없는 에러 처리
- 잠재적 버그

**우선순위**: 높음 (즉시 개선 필요)

---

### 2. Type Inconsistency (타입 불일치)

**위치**: `ButtonLayoutConfig.get_special_buttons()`

**문제점**:
- 반환 타입이 `list[tuple[ButtonDefinition, int, int]]`로 정의되어 있음
- 하지만 `ButtonDefinition`에 이미 `row`, `col` 정보가 포함되어 있음
- 실제 사용 시 불필요한 언패킹이 필요함

**현재 코드**:
```python
def get_special_buttons() -> list[tuple[ButtonDefinition, int, int]]:
    return [
        (ButtonDefinition(4, 0, 1, 2, ...), 4, 0),  # row, col 중복
        (ButtonDefinition(4, 2, 1, 2, ...), 4, 2),  # row, col 중복
    ]

# 사용 시
for btn_def, row, col in special_buttons:  # 불필요한 언패킹
    button_layout.addWidget(button, row, col, btn_def.rowspan, btn_def.colspan)
```

**영향**:
- 데이터 중복
- 타입 불일치
- 가독성 저하

**우선순위**: 중간 (개선 권장)

---

### 3. Magic String (매직 문자열)

**위치**: 버튼 정의에서 소수점 `"."` 하드코딩

**문제점**:
- 소수점 버튼 텍스트가 하드코딩되어 있음
- 다른 버튼 텍스트는 `ButtonConfig`에 상수로 정의되어 있지만 소수점은 없음

**현재 코드**:
```python
ButtonDefinition(3, 2, 1, 1, ".", ButtonType.NUMBER),  # Magic String
```

**영향**:
- 일관성 부족
- 유지보수성 저하

**우선순위**: 낮음 (개선 권장)

---

### 4. Complex Conditionals (복잡한 조건문)

**위치**: `connect_button()` 메서드

**문제점**:
- 여러 if-elif 분기와 중첩된 if문으로 복잡함
- 전략 패턴이나 딕셔너리 매핑으로 개선 가능

**현재 코드**:
```python
def connect_button(self, button: QPushButton, text: str, button_type: ButtonType):
    if button_type == ButtonType.NUMBER:
        button.clicked.connect(lambda: self.on_number_clicked(text))
    elif button_type == ButtonType.OPERATOR:
        button.clicked.connect(lambda: self.on_operator_clicked(text))
    elif button_type == ButtonType.EQUALS:
        button.clicked.connect(self.on_equals_clicked)
    else:  # ButtonType.SPECIAL
        if text == ButtonConfig.BUTTON_CLEAR:
            button.clicked.connect(self.on_clear_clicked)
        elif text == ButtonConfig.BUTTON_TOGGLE_SIGN:
            button.clicked.connect(self.on_toggle_sign_clicked)
```

**영향**:
- 순환 복잡도 증가
- 확장성 저하
- OCP 위반 (새 버튼 타입 추가 시 수정 필요)

**우선순위**: 중간 (개선 권장)

---

### 5. Feature Envy (기능 질투)

**위치**: `_setup_button_grid()` 메서드

**문제점**:
- `get_special_buttons()`의 반환값을 언패킹하는 로직이 복잡함
- 일반 버튼과 특수 버튼을 다르게 처리하는 로직이 분리되어 있음

**현재 코드**:
```python
# 일반 버튼
for btn_def in button_definitions:
    button = ButtonFactory.create_button(btn_def.text, btn_def.button_type)
    button_layout.addWidget(button, btn_def.row, btn_def.col, ...)
    self.connect_button(button, btn_def.text, btn_def.button_type)

# 특수 버튼 (다른 처리 방식)
special_buttons = ButtonLayoutConfig.get_special_buttons()
for btn_def, row, col in special_buttons:  # 다른 언패킹 방식
    button = ButtonFactory.create_button(btn_def.text, btn_def.button_type)
    button_layout.addWidget(button, row, col, btn_def.rowspan, btn_def.colspan)
    self.connect_button(button, btn_def.text, btn_def.button_type)
```

**영향**:
- 코드 중복
- 일관성 부족

**우선순위**: 중간 (개선 권장)

---

## 개선 방안

### 우선순위 1: 일관된 에러 처리

**목표**: 모든 이벤트 핸들러가 `_handle_calculation()`을 사용하도록 통일

**구현**:
```python
def on_clear_clicked(self):
    """Clear 버튼 클릭 핸들러"""
    self._handle_calculation(
        lambda: self.engine.clear(),
        "초기화 오류"
    )

def on_toggle_sign_clicked(self):
    """+/- 버튼 클릭 핸들러"""
    self._handle_calculation(
        lambda: self.engine.toggle_sign(),
        "부호 변경 오류"
    )
```

**효과**:
- 일관된 에러 처리
- DRY 원칙 준수
- 버그 예방

---

### 우선순위 2: 타입 일관성 개선

**목표**: `get_special_buttons()` 반환 타입을 `list[ButtonDefinition]`로 통일

**구현**:
```python
@staticmethod
def get_special_buttons() -> list[ButtonDefinition]:
    """특수 버튼 정의 (C, =)"""
    return [
        ButtonDefinition(4, 0, 1, 2, ButtonConfig.BUTTON_CLEAR, ButtonType.SPECIAL),
        ButtonDefinition(4, 2, 1, 2, ButtonConfig.BUTTON_EQUALS, ButtonType.EQUALS),
    ]

# 사용 시
for btn_def in ButtonLayoutConfig.get_button_definitions() + ButtonLayoutConfig.get_special_buttons():
    button = ButtonFactory.create_button(btn_def.text, btn_def.button_type)
    button_layout.addWidget(button, btn_def.row, btn_def.col, btn_def.rowspan, btn_def.colspan)
    self.connect_button(button, btn_def.text, btn_def.button_type)
```

**효과**:
- 타입 일관성
- 코드 단순화
- 중복 제거

---

### 우선순위 3: Magic String 제거

**목표**: 소수점 버튼 텍스트를 상수로 정의

**구현**:
```python
class ButtonConfig:
    # ... 기존 상수들
    BUTTON_DECIMAL = "."  # 소수점 버튼

# 사용
ButtonDefinition(3, 2, 1, 1, ButtonConfig.BUTTON_DECIMAL, ButtonType.NUMBER),
```

**효과**:
- 일관성 향상
- 유지보수성 향상

---

### 우선순위 4: 조건문 단순화 (전략 패턴)

**목표**: `connect_button()` 메서드의 복잡한 조건문을 딕셔너리 매핑으로 개선

**구현**:
```python
def connect_button(self, button: QPushButton, text: str, button_type: ButtonType):
    """버튼 이벤트 연결"""
    # 버튼 타입별 핸들러 매핑
    handler_map = {
        ButtonType.NUMBER: lambda: self.on_number_clicked(text),
        ButtonType.OPERATOR: lambda: self.on_operator_clicked(text),
        ButtonType.EQUALS: self.on_equals_clicked,
    }
    
    # 특수 버튼 핸들러 매핑
    special_handler_map = {
        ButtonConfig.BUTTON_CLEAR: self.on_clear_clicked,
        ButtonConfig.BUTTON_TOGGLE_SIGN: self.on_toggle_sign_clicked,
    }
    
    # 핸들러 연결
    if button_type in handler_map:
        button.clicked.connect(handler_map[button_type])
    elif button_type == ButtonType.SPECIAL and text in special_handler_map:
        button.clicked.connect(special_handler_map[text])
```

**효과**:
- 순환 복잡도 감소
- 확장성 향상
- OCP 준수

---

## 개선 우선순위 요약

| 우선순위 | 코드 스멜 | 영향도 | 개선 난이도 |
|---------|----------|--------|------------|
| 1 | Inconsistent Error Handling | 높음 | 낮음 |
| 2 | Type Inconsistency | 중간 | 낮음 |
| 3 | Magic String | 낮음 | 매우 낮음 |
| 4 | Complex Conditionals | 중간 | 중간 |

---

## 결론

현재 코드는 대부분의 주요 리팩토링이 완료되었지만, 몇 가지 추가 개선 사항이 있습니다:

1. **즉시 개선 필요**: 에러 처리 일관성
2. **개선 권장**: 타입 일관성, 조건문 단순화
3. **선택적 개선**: Magic String 제거

이러한 개선을 통해 코드 품질을 더욱 향상시킬 수 있습니다.

