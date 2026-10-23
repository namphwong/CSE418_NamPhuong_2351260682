from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from index import build_index
from search import (
    build_friendly_query,
    format_results,
    run_friendly_cli,
    search_documents,
    split_terms,
)


PROJECT_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_DIR / "CS-Docs"


class SearchTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = TemporaryDirectory()
        self.index_dir = Path(self.temporary.name) / "index"
        build_index(DOCS_DIR, self.index_dir)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_split_terms_preserves_phrase_and_proximity(self) -> None:
        self.assertEqual(
            split_terms('machine "learning model" "whoosh library"~5'),
            ["machine", '"learning model"', '"whoosh library"~5'],
        )

    def test_build_friendly_query_matches_assignment_example(self) -> None:
        query = build_friendly_query(
            "learning data",
            "text image",
            "programming software",
        )
        self.assertEqual(
            query,
            "learning data (text OR image) NOT programming NOT software",
        )

    def test_build_friendly_query_rejects_empty_positive_part(self) -> None:
        with self.assertRaises(ValueError):
            build_friendly_query("", "", "software")

    def test_split_terms_rejects_unclosed_phrase(self) -> None:
        with self.assertRaises(ValueError):
            split_terms('"machine learning')

    def test_and_query_returns_documents_containing_both_terms(self) -> None:
        results = search_documents("learning AND data", self.index_dir)
        titles = {str(result["title"]) for result in results}
        self.assertIn("ML.txt - Machine Learning", titles)
        self.assertIn("DM.txt - Data Mining", titles)

    def test_or_query_returns_documents_containing_either_term(self) -> None:
        results = search_documents("artificial OR operating", self.index_dir)
        titles = {str(result["title"]) for result in results}
        self.assertIn("AI.txt - Artificial Intelligence", titles)
        self.assertIn("OS.txt - Operating System", titles)

    def test_not_query_excludes_forbidden_term(self) -> None:
        results = search_documents("software NOT engineering", self.index_dir)
        titles = {str(result["title"]) for result in results}
        self.assertIn("OS.txt - Operating System", titles)
        self.assertNotIn("SE.txt - Software Engineering", titles)

    def test_phrase_query(self) -> None:
        results = search_documents('"machine learning"', self.index_dir)
        titles = {str(result["title"]) for result in results}
        self.assertIn("ML.txt - Machine Learning", titles)
        self.assertIn("DM.txt - Data Mining", titles)

    def test_proximity_query(self) -> None:
        results = search_documents('"data mining"~5', self.index_dir)
        self.assertIn("DM.txt - Data Mining", {str(r["title"]) for r in results})

    def test_wildcard_query(self) -> None:
        results = search_documents("learn*", self.index_dir)
        self.assertTrue(results)

    def test_empty_or_unknown_query_returns_no_results(self) -> None:
        self.assertEqual(search_documents("", self.index_dir), [])
        self.assertEqual(search_documents("termthatdoesnotexist", self.index_dir), [])

    def test_format_results_numbers_from_one_and_contains_scores(self) -> None:
        lines = format_results(
            [
                {"title": "A", "score": 2.0},
                {"title": "B", "score": 1.0},
            ]
        )
        self.assertEqual(lines[0], "Số kết quả: 2")
        self.assertTrue(lines[1].startswith("1. A"))
        self.assertIn("2.0000", lines[1])
        self.assertTrue(lines[2].startswith("2. B"))

    def test_friendly_cli_builds_query_displays_content_and_exits(self) -> None:
        answers = iter(["learning", "machine data", "software", "1", "q"])
        output: list[str] = []
        run_friendly_cli(
            self.index_dir,
            input_fn=lambda _: next(answers),
            output_fn=output.append,
            auto_build=False,
        )

        joined = "\n".join(output)
        self.assertIn(
            "Câu truy vấn được tạo: learning (machine OR data) NOT software",
            joined,
        )
        self.assertIn("Nội dung tài liệu", joined)
        self.assertIn("Đã kết thúc chương trình.", joined)

    def test_friendly_cli_rejects_invalid_result_number(self) -> None:
        answers = iter(["learning", "", "", "999", "q"])
        output: list[str] = []
        run_friendly_cli(
            self.index_dir,
            input_fn=lambda _: next(answers),
            output_fn=output.append,
            auto_build=False,
        )

        self.assertTrue(any("phải nằm trong khoảng" in line for line in output))


if __name__ == "__main__":
    unittest.main()
