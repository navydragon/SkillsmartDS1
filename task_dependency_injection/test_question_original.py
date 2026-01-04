"""
Исходный код без использования Dependency Injection.
Проблема: класс TestGrader жестко привязан к конкретному типу вопросов
и способу проверки. При добавлении новых типов вопросов или стратегий
оценивания придется изменять код TestGrader.
"""


class MultipleChoiceQuestion:
    """Вопрос с множественным выбором."""
    
    def __init__(self, question_id: str, text: str, correct_answer: str):
        self.question_id = question_id
        self.text = text
        self.correct_answer = correct_answer
    
    def check_answer(self, student_answer: str) -> bool:
        """Проверка ответа студента."""
        return student_answer.lower().strip() == self.correct_answer.lower().strip()


class TestGrader:
    """
    Система проверки тестовых вопросов.
    
    ПРОБЛЕМА: жестко привязан к MultipleChoiceQuestion.
    Чтобы добавить другие типы вопросов (открытые, верно/неверно) 
    или изменить стратегию оценивания, нужно изменять этот класс.
    """
    
    def __init__(self):
        self.questions = []
        self.student_answers = {}
    
    def add_question(self, question: MultipleChoiceQuestion):
        """Добавить вопрос в тест."""
        self.questions.append(question)
    
    def submit_answer(self, question_id: str, answer: str):
        """Сохранить ответ студента."""
        self.student_answers[question_id] = answer
    
    def grade_test(self) -> float:
        """
        Проверить тест и вернуть оценку.
        
        ПРОБЛЕМА: логика проверки захардкожена для MultipleChoiceQuestion.
        """
        if not self.questions:
            return 0.0
        
        correct = 0
        for question in self.questions:
            student_answer = self.student_answers.get(question.question_id, "")
            # Жесткая привязка к методу check_answer класса MultipleChoiceQuestion
            if question.check_answer(student_answer):
                correct += 1
        
        return (correct / len(self.questions)) * 100


# Пример использования
if __name__ == "__main__":
    print("=" * 60)
    print("Исходный код БЕЗ Dependency Injection")
    print("=" * 60)
    
    grader = TestGrader()
    
    # Добавление вопросов
    q1 = MultipleChoiceQuestion("q1", "Столица России?", "Москва")
    q2 = MultipleChoiceQuestion("q2", "2 + 2 = ?", "4")
    grader.add_question(q1)
    grader.add_question(q2)
    
    # Ответы студента
    grader.submit_answer("q1", "Москва")
    grader.submit_answer("q2", "4")
    
    # Проверка
    score = grader.grade_test()
    print(f"\nРезультат теста: {score:.1f}%")
    
