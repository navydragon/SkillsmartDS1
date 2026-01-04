# Защита кода от изменений требований: Dependency Injection

## Описание

Демонстрация использования **интерфейсов** и **Dependency Injection (DI)** для создания гибкого и легко изменяемого кода в контексте образовательной платформы LMS (Learning Management System) - система проверки тестовых вопросов.

## Проблема исходного кода

В файле `test_question_original.py` представлен код **без использования DI**:

- Класс `TestGrader` жестко привязан к конкретному типу вопросов `MultipleChoiceQuestion`
- Логика проверки захардкожена в методе `grade_test()`
- При необходимости добавить новые типы вопросов (открытые, верно/неверно) или изменить стратегию оценивания требуется изменять код `TestGrader`
- Сложно тестировать (невозможно легко подставить mock-объект)
- Нарушается принцип **Open/Closed** (открыт для расширения, закрыт для изменения)

## Решение с Dependency Injection

В файле `test_question_di.py` представлен **улучшенный код с DI**:

### Ключевые компоненты:

1. **Интерфейс `Question`** (Protocol)
   - Определяет контракт для всех типов вопросов
   - Свойства: `question_id`, `text`
   - Метод: `check_answer(student_answer: str) -> bool`

2. **Интерфейс `GradingStrategy`** (Protocol)
   - Определяет контракт для стратегий оценивания
   - Метод: `calculate_score(questions, answers) -> float`

3. **Реализации типов вопросов:**
   - `MultipleChoiceQuestion` - вопросы с множественным выбором
   - `TrueFalseQuestion` - вопросы типа "Верно/Неверно"
   - `OpenQuestion` - открытые вопросы с ключевыми словами

4. **Реализации стратегий оценивания:**
   - `StrictGradingStrategy` - строгая стратегия (все или ничего)
   - `PartialCreditGradingStrategy` - стратегия с частичными баллами

5. **Сервис с DI:**
   - `TestGrader` принимает стратегию оценивания через конструктор
   - Работает с любыми типами вопросов через интерфейс `Question`
   - Не зависит от конкретных реализаций
   - Легко расширяется без изменения кода



## Примеры использования

### Строгая стратегия оценивания:
```python
strict_strategy = StrictGradingStrategy()
grader = TestGrader(strict_strategy)

grader.add_question(MultipleChoiceQuestion("q1", "Столица России?", "Москва"))
grader.add_question(TrueFalseQuestion("q2", "Python - язык программирования", True))
grader.submit_answer("q1", "Москва")
grader.submit_answer("q2", "верно")

score = grader.grade_test()
```

### Стратегия с частичными баллами:
```python
partial_strategy = PartialCreditGradingStrategy()
grader = TestGrader(partial_strategy)
# ... добавление вопросов и ответов ...
score = grader.grade_test()
```

## Запуск примеров

```bash
# Исходный код (без DI)
python test_question_original.py

# Итоговый код (с DI)
python test_question_di.py
```



