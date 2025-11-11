from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import List


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "questions.json"


@dataclass
class Question:
    id: int
    category: str
    question: str
    options: List[str]
    correct_index: int
    explanation: str


def load_questions(path: Path = DATA_PATH) -> List[Question]:
    """
    Load questions from a JSON file and convert them into Question objects.
    """
    raw = json.loads(path.read_text(encoding="utf-8"))
    questions: List[Question] = []
    for row in raw:
        questions.append(
            Question(
                id=row["id"],
                category=row["category"],
                question=row["question"],
                options=row["options"],
                correct_index=row["correct_index"],
                explanation=row["explanation"],
            )
        )
    return questions


def ask_question(q: Question) -> bool:
    """
    Ask a single question in the terminal, return True if user answered correctly.
    """
    print("\n----------------------------------------")
    print(f"[{q.category}] Question #{q.id}")
    print(q.question)
    print()

    for i, opt in enumerate(q.options):
        print(f"  {i + 1}. {opt}")

    while True:
        user_input = input("\nYour answer (1–4, or 'q' to quit): ").strip()
        if user_input.lower() == "q":
            # special marker meaning "user aborted the quiz"
            raise KeyboardInterrupt
        if user_input in {"1", "2", "3", "4"}:
            choice = int(user_input) - 1
            break
        print("Please enter 1, 2, 3, 4 or 'q'.")

    is_correct = choice == q.correct_index
    if is_correct:
        print("✅ Correct!")
    else:
        correct_text = q.options[q.correct_index]
        print(f"❌ Not quite. Correct answer: {q.correct_index + 1}. {correct_text}")

    print(f"ℹ️  Explanation: {q.explanation}")
    return is_correct


def run_quiz(num_questions: int = 5) -> None:
    """
    Run a simple aerospace quiz in the terminal.
    """
    questions = load_questions()

    if num_questions > len(questions):
        num_questions = len(questions)

    selected = random.sample(questions, k=num_questions)

    print("🚀 Aerospace Knowledge Quiz")
    print("Answer the questions using 1–4, or press 'q' to quit.\n")

    correct = 0
    asked = 0

    try:
        for q in selected:
            if ask_question(q):
                correct += 1
            asked += 1
    except KeyboardInterrupt:
        print("\nQuiz aborted by user.")

    if asked > 0:
        score = correct / asked * 100
        print(f"\nYour score: {correct}/{asked} ({score:.1f}%)")
    else:
        print("\nNo questions answered.")


if __name__ == "__main__":
    run_quiz()
