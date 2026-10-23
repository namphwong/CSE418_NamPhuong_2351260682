import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from src.bai03_chi_muc_nguoc import build_index, search_documents, run_cli
from src.data import Document
from src.safe_index import rebuild_index
from src.whoosh_common import document_schema

class RegressionTests(unittest.TestCase):
    def test_failed_rebuild_preserves_results_and_releases_lock(self):
        with TemporaryDirectory() as temp:
            path = Path(temp)/"index"
            build_index(path)
            before = search_documents("học máy", path)
            def broken():
                yield dict(doc_id="1", title="A", content="valid")
                raise ValueError("bad data")
            with self.assertRaises(ValueError):
                rebuild_index(path, document_schema(), broken())
            self.assertEqual(search_documents("học máy", path), before)
            build_index(path)
            self.assertEqual(search_documents("học máy", path), before)
    def test_duplicate_ids_rejected(self):
        with TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                build_index(Path(temp)/"i", (Document(1,"A","a"),Document(1,"B","b")))
    def test_eof_and_actual_count(self):
        with TemporaryDirectory() as temp:
            output=[]
            def eof(_): raise EOFError
            run_cli(Path(temp)/"i",documents=(Document(1,"A","python"),),input_fn=eof,output_fn=output.append)
            self.assertIn("1 tài liệu", output[0])
            self.assertIn("Đã kết thúc",output[-1])
