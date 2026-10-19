"""Read the shared student configuration independently of the working directory."""
import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "student_info.json"
FIELDS = ("full_name", "student_id", "group", "university", "course")


def load_student(path=CONFIG_PATH):
    """Return validated student details; report invalid or missing data clearly."""
    with Path(path).open(encoding="utf-8") as source:
        student = json.load(source)
    if not isinstance(student, dict):
        raise ValueError("Student configuration must be a JSON object")
    for field in FIELDS:
        if not isinstance(student.get(field), str) or not student[field].strip():
            raise ValueError(f"Student configuration requires a nonempty string: {field}")
    return {field: student[field] for field in FIELDS}
