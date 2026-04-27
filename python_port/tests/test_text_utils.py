from libresprite_py.text_utils import replace_string, split_string, trim_string


def test_replace_string_basic() -> None:
    assert replace_string("a-b-c", "-", ":") == "a:b:c"


def test_replace_string_empty_needle_no_change() -> None:
    assert replace_string("abc", "", "x") == "abc"


def test_replace_string_non_overlapping_scan_matches_cpp_flow() -> None:
    assert replace_string("aaaa", "aa", "a") == "aa"


def test_split_string_keeps_empty_segments() -> None:
    assert split_string("a,,b,", ",") == ["a", "", "b", ""]


def test_split_string_multiple_separators() -> None:
    assert split_string("a:b,c", ":,") == ["a", "b", "c"]


def test_trim_string_regular_case() -> None:
    assert trim_string("  hello  ") == "hello"


def test_trim_string_single_non_space_char_matches_cpp_behavior() -> None:
    # C++ implementation returns empty string for 1-char trimmed content due to i<j condition.
    assert trim_string("x") == ""
