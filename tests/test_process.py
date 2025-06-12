from search.process import extract_text, extract_regex, process_directory


def test_extract_text(tmp_path):
    file = tmp_path / "sample.txt"
    file.write_text("hello")
    assert extract_text(str(file)) == "hello"


def test_extract_regex_email():
    text = "Contact: a@test.com"
    assert extract_regex(text)["email"] == ["a@test.com"]


def test_process_directory_skips_openai(tmp_path, monkeypatch):
    sample = tmp_path / "file.txt"
    sample.write_text("email me at a@test.com")

    called = False

    def fake_classify_text(_text: str):
        nonlocal called
        called = True
        return ""

    monkeypatch.setattr("search.process.classify_text", fake_classify_text)
    result = process_directory(str(tmp_path))
    assert not called
    assert result[str(sample)]["regex"]["email"] == ["a@test.com"]
    assert result[str(sample)]["gpt"] == ""

