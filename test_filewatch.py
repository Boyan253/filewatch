import filewatch


def test_snapshot_lists_files(tmp_path):
    (tmp_path / "a.py").write_text("x", encoding="utf-8")
    (tmp_path / "b.txt").write_text("y", encoding="utf-8")
    assert len(filewatch.snapshot(str(tmp_path))) == 2

def test_snapshot_filters_extensions(tmp_path):
    (tmp_path / "a.py").write_text("x", encoding="utf-8")
    (tmp_path / "b.txt").write_text("y", encoding="utf-8")
    state = filewatch.snapshot(str(tmp_path), [".py"])
    assert len(state) == 1
