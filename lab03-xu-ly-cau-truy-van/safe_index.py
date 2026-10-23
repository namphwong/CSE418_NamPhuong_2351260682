"""Build a replacement Whoosh index before publishing it (single writer)."""
from pathlib import Path
import tempfile
from whoosh.index import create_in


def rebuild_index(target, schema, documents):
    target = Path(target).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    # All disposable paths are generated children of this private directory.
    with tempfile.TemporaryDirectory(prefix=".rebuild-", dir=target.parent) as root:
        staging = Path(root) / "new"
        backup = Path(root) / "old"
        staging.mkdir()
        index = create_in(str(staging), schema)
        writer = None
        try:
            writer = index.writer()
            for document in documents:
                writer.add_document(**document)
            writer.commit()
            writer = None
        finally:
            if writer is not None:
                writer.cancel()
            index.close()
        if target.exists():
            target.rename(backup)
        try:
            staging.rename(target)
        except BaseException:
            if backup.exists():
                backup.rename(target)
            raise
    return target
