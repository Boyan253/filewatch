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


def test_snapshot_skips_noise_directories(tmp_path):
    junk = tmp_path / "__pycache__"
    junk.mkdir()
    (junk / "a.py").write_text("x", encoding="utf-8")
    assert filewatch.snapshot(str(tmp_path)) == {}

def test_diff_detects_added():
    added, _, _ = filewatch.diff({}, {"a": (1, 1)})
    assert added == ["a"]


def test_diff_detects_removed():
    _, removed, _ = filewatch.diff({"a": (1, 1)}, {})
    assert removed == ["a"]

def test_diff_detects_changed():
    _, _, changed = filewatch.diff({"a": (1, 1)}, {"a": (2, 1)})
    assert changed == ["a"]


def test_describe_summarises():
    text = filewatch.describe(["x/new.py"], [], ["x/old.py"])
    assert "+new.py" in text and "~old.py" in text
