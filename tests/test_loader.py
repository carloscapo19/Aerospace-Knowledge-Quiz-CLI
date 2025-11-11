from pathlib import Path

from src.quiz import load_questions, DATA_PATH


def test_load_questions_basic():
    questions = load_questions(DATA_PATH)
    assert len(questions) > 0
    q0 = questions[0]
    assert q0.question
    assert len(q0.options) >= 2
    assert 0 <= q0.correct_index < len(q0.options)
