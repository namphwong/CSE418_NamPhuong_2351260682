import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from index import build_index, DEFAULT_DOCS_DIR
from search import build_friendly_query, search_documents, run_advanced_cli, run_friendly_cli

class RegressionTests(unittest.TestCase):
    def test_failed_rebuild_preserves_index(self):
        with TemporaryDirectory() as temp:
            p=Path(temp)/"i"
            build_index(index_dir=p)
            before=search_documents("learning",p)
            for source in [Path(temp)/"missing", Path(temp)/"empty"]:
                if source.name=="empty": source.mkdir()
                with self.assertRaises(FileNotFoundError): build_index(source,p)
                self.assertEqual(search_documents("learning",p),before)
            source=Path(temp)/"bad";source.mkdir()
            (source/"a.txt").write_text("Title",encoding="utf-8")
            with self.assertRaises(ValueError): build_index(source,p)
            self.assertEqual(search_documents("learning",p),before)
            # Failure while publishing must restore the old directory.
            original=Path.rename
            def rename(path,target):
                if path.name=="new": raise OSError("simulated publish failure")
                return original(path,target)
            with patch.object(Path,"rename",rename):
                with self.assertRaises(OSError): build_index(index_dir=p)
            self.assertEqual(search_documents("learning",p),before)
            build_index(index_dir=p)
            self.assertEqual(search_documents("learning",p),before)
    def test_friendly_rejects_query_syntax(self):
        for value in ["learning OR software", "title:software", "(learning)", "learning^2"]:
            with self.assertRaises(ValueError): build_friendly_query(value,"","")
    def test_exact_query_semantics(self):
        with TemporaryDirectory() as temp:
            root=Path(temp)/"docs";root.mkdir();p=Path(temp)/"i"
            for name,text in {"a":"alpha beta gamma", "b":"alpha delta beta", "c":"beta alpha"}.items():
                (root/(name+".txt")).write_text(name+"\n"+text,encoding="utf-8")
            build_index(root,p)
            def hits(q): return {Path(str(r["path"])).stem for r in search_documents(q,p)}
            self.assertEqual(hits('"alpha beta"'),{"a"})
            self.assertEqual(hits('"alpha beta"~2'),{"a","b"})
            self.assertEqual(hits('alpha NOT delta'),{"a","c"})
            self.assertEqual(hits('gamma OR delta'),{"a","b"})
            self.assertEqual(hits('alpha AND gamma'),{"a"})
            self.assertEqual(hits('gam*'),{"a"})
            self.assertEqual(hits('gamm?'),{"a"})
            self.assertEqual(hits(build_friendly_query("alpha","gamma delta","")),{"a","b"})
    def test_eof_at_query_and_selection(self):
        with TemporaryDirectory() as temp:
            p=Path(temp)/"i";build_index(index_dir=p)
            for runner,answers in [(run_advanced_cli,[]),(run_advanced_cli,["learning"]),(run_friendly_cli,["learning","",""])]:
                iterator=iter(answers);output=[]
                def read(_):
                    try: return next(iterator)
                    except StopIteration: raise EOFError
                runner(p,input_fn=read,output_fn=output.append,auto_build=False)
                self.assertIn("Đã kết thúc",output[-1])

    def test_selection_reports_missing_and_invalid_utf8_files(self):
        from search import _choose_result
        with TemporaryDirectory() as temp:
            p=Path(temp)/"document.txt"
            for invalid in [False, True]:
                if invalid: p.write_bytes(bytes([255]))
                output=[]
                self.assertTrue(_choose_result([{"path":str(p)}],lambda _:"1",output.append))
                self.assertIn("Không thể đọc tài liệu",output[-1])
