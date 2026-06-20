import json
import unittest

from log16.epistemic_gate import (
    NEEDS_FILE_FIELD,
    UNSUPPORTED_MODE,
    evaluate_question,
    render_markdown,
)


class TestEpistemicGate(unittest.TestCase):
    def test_file_inventory_question_needs_file_field(self):
        decision = evaluate_question("Как произвести инвентаризацию файлового поля проекта?")
        self.assertEqual(decision.status, NEEDS_FILE_FIELD)
        self.assertFalse(decision.answer_available)
        self.assertIn("file-field-map-v01.md", decision.needed_file_field)
        self.assertIn("archivarius", decision.route)

    def test_empty_question_is_unsupported(self):
        decision = evaluate_question("")
        self.assertEqual(decision.status, UNSUPPORTED_MODE)
        self.assertFalse(decision.answer_available)

    def test_markdown_explains_unknown_state(self):
        q = "Как произвести инвентаризацию файлового поля проекта?"
        decision = evaluate_question(q)
        md = render_markdown(decision, q)
        self.assertIn("Я не могу дать проверяемый ответ", md)
        self.assertIn("NEEDS_FILE_FIELD", md)
        self.assertIn("Что нужно внести в файловое поле", md)

    def test_json_serializable(self):
        decision = evaluate_question("Как произвести инвентаризацию файлового поля проекта?")
        payload = json.dumps(decision.to_dict(), ensure_ascii=False)
        self.assertIn("NEEDS_FILE_FIELD", payload)


if __name__ == "__main__":
    unittest.main()
