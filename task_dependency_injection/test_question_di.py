"""
Итоговый код с использованием интерфейсов и Dependency Injection.
Преимущество: легко добавлять новые типы вопросов и стратегии оценивания
без изменения TestGrader.
"""

from typing import Protocol, Dict, List


class Question(Protocol):
    """Интерфейс для тестового вопроса."""
    @property
    def question_id(self) -> str: ...
    @property
    def text(self) -> str: ...
    def check_answer(self, student_answer: str) -> bool: ...


class GradingStrategy(Protocol):
    """Интерфейс для стратегии оценивания теста."""
    def calculate_score(self, questions: List[Question], answers: Dict[str, str]) -> float: ...


class MultipleChoiceQuestion:
    """Вопрос с множественным выбором."""
    def __init__(self, question_id: str, text: str, correct_answer: str):
        self._question_id = question_id
        self._text = text
        self.correct_answer = correct_answer
    @property
    def question_id(self) -> str:
        return self._question_id
    @property
    def text(self) -> str:
        return self._text
    def check_answer(self, student_answer: str) -> bool:
        return student_answer.lower().strip() == self.correct_answer.lower().strip()


class TrueFalseQuestion:
    """Вопрос типа "Верно/Неверно"."""
    def __init__(self, question_id: str, text: str, correct_answer: bool):
        self._question_id = question_id
        self._text = text
        self.correct_answer = correct_answer
    @property
    def question_id(self) -> str:
        return self._question_id
    @property
    def text(self) -> str:
        return self._text
    def check_answer(self, student_answer: str) -> bool:
        answer_bool = student_answer.lower().strip() in ["true", "верно", "да", "1"]
        return answer_bool == self.correct_answer


class OpenQuestion:
    """Открытый вопрос (требует текстового ответа)."""
    def __init__(self, question_id: str, text: str, keywords: List[str]):
        self._question_id = question_id
        self._text = text
        self.keywords = keywords
    @property
    def question_id(self) -> str:
        return self._question_id
    @property
    def text(self) -> str:
        return self._text
    def check_answer(self, student_answer: str) -> bool:
        answer_lower = student_answer.lower()
        return any(keyword.lower() in answer_lower for keyword in self.keywords)


class StrictGradingStrategy:
    """Строгая стратегия: все или ничего."""
    def calculate_score(self, questions: List[Question], answers: Dict[str, str]) -> float:
        if not questions:
            return 0.0
        correct = sum(1 for q in questions if q.check_answer(answers.get(q.question_id, "")))
        return (correct / len(questions)) * 100


class PartialCreditGradingStrategy:
    """Стратегия с частичными баллами."""
    def calculate_score(self, questions: List[Question], answers: Dict[str, str]) -> float:
        if not questions:
            return 0.0
        total_score = 0.0
        for question in questions:
            answer = answers.get(question.question_id, "")
            if answer:
                total_score += 1.0 if question.check_answer(answer) else 0.3
        return (total_score / len(questions)) * 100


class TestGrader:
    """Система проверки тестовых вопросов с использованием Dependency Injection."""
    def __init__(self, grading_strategy: GradingStrategy):
        self.grading_strategy = grading_strategy
        self.questions: List[Question] = []
        self.student_answers: Dict[str, str] = {}
    def add_question(self, question: Question):
        self.questions.append(question)
    def submit_answer(self, question_id: str, answer: str):
        self.student_answers[question_id] = answer
    def grade_test(self) -> float:
        return self.grading_strategy.calculate_score(self.questions, self.student_answers)

if __name__ == "__main__":
    print("=" * 60)
    print("Итоговый код С Dependency Injection")
    print("=" * 60)
    print("\n1. Строгая стратегия оценивания:")
    grader1 = TestGrader(StrictGradingStrategy())
    grader1.add_question(MultipleChoiceQuestion("q1", "Столица России?", "Москва"))
    grader1.add_question(TrueFalseQuestion("q2", "Python - язык программирования", True))
    grader1.add_question(OpenQuestion("q3", "Что такое ООП?", ["объект", "класс"]))
    grader1.submit_answer("q1", "Москва")
    grader1.submit_answer("q2", "верно")
    grader1.submit_answer("q3", "ООП - это программирование с использованием объектов и классов")
    print(f"Результат: {grader1.grade_test():.1f}%")
    print("\n2. Стратегия с частичными баллами:")
    grader2 = TestGrader(PartialCreditGradingStrategy())
    grader2.add_question(MultipleChoiceQuestion("q1", "Столица России?", "Москва"))
    grader2.add_question(TrueFalseQuestion("q2", "Python - язык программирования", True))
    grader2.submit_answer("q1", "Санкт-Петербург")
    grader2.submit_answer("q2", "верно")
    print(f"Результат: {grader2.grade_test():.1f}% (с частичными баллами)")
    print("\n" + "=" * 60)

