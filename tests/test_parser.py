import re

import pytest

from mdclense.parser import MarkdownParser


@pytest.fixture
def parser():
    """Fixture to create parser instance for tests"""
    return MarkdownParser()


def test_headers(parser):
    """Test header parsing"""
    # ATX headers
    assert parser.parse("# Header 1") == "Header 1"
    assert parser.parse("### Deep Header") == "Deep Header"

    # Setext headers
    assert parser.parse("Header 1\n========") == "Header 1"
    assert parser.parse("Header 2\n--------") == "Header 2"


def test_emphasis(parser):
    """Test emphasis parsing"""
    # Bold
    assert parser.parse("This is **bold** text") == "This is bold text"
    assert parser.parse("This is __bold__ text") == "This is bold text"

    # Italic
    assert parser.parse("This is *italic* text") == "This is italic text"
    assert parser.parse("This is _italic_ text") == "This is italic text"

    # Bold and italic
    assert (
        parser.parse("This is ***bold and italic*** text")
        == "This is bold and italic text"
    )


def test_links_and_images(parser):
    """Test links and images parsing"""
    # Links
    assert parser.parse("[Link text](http://example.com)") == "Link text"

    # Images
    assert parser.parse("![Alt text](image.jpg)") == "Alt text"

    # Reference links
    assert parser.parse("[Link][ref]\n[ref]: http://example.com") == "Link"


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("- Item 1\n- Item 2", "Item 1\nItem 2"),  # Unordered list
        ("1. First\n2. Second", "First\nSecond"),  # Ordered list
        ("- [ ] Todo\n- [x] Done", "Todo\nDone"),  # Task list
    ],
)
def test_lists(parser, input_text, expected):
    """Test lists parsing with parameterized inputs"""
    assert parser.parse(input_text) == expected


def test_code_blocks(parser):
    """Test code block parsing"""
    # Code blocks
    assert parser.parse("```python\nprint('hello')\n```") == "[CODE BLOCK]"

    # Inline code
    assert parser.parse("Use the `print()` function") == "Use the print() function"


# @pytest.mark.parametrize(
#     "quote_text",
#     [
#         "> Simple quote",
#         "> Multi-line\n> quote\n> text",
#         "> Nested\n>> quote",
#     ],
# )
# def test_blockquotes(parser, quote_text):
#     """Test blockquote parsing with different formats"""
#     result = parser.parse(quote_text)
#     assert ">" not in result
#     assert result.strip() == quote_text.replace(">", "").strip()


@pytest.mark.parametrize(
    "rule",
    [
        "---",
        "***",
        "___",
        "- - -",
        "* * *",
    ],
)
def test_horizontal_rules(parser, rule):
    """Test horizontal rule parsing with different formats"""
    assert parser.parse(f"{rule}\nText") == "Text"


def test_tables(parser):
    """Test table parsing"""
    table = """
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |
    """.strip()
    assert parser.parse(table) == ""


def test_strikethrough(parser):
    """Test strikethrough parsing"""
    assert parser.parse("~~struck through~~") == "struck through"
    assert parser.parse("This is ~~struck~~ through") == "This is struck through"


@pytest.mark.parametrize(
    "html,expected",
    [
        ("<strong>Bold</strong>", "Bold"),
        ("<em>Italic</em>", "Italic"),
        ('<a href="url">Link</a>', "Link"),
    ],
)
def test_html(parser, html, expected):
    """Test HTML tag parsing with different tags"""
    assert parser.parse(html) == expected


def test_footnotes(parser):
    """Test footnote parsing"""
    text = """Here's a note[^1] and another[^2]

[^1]: First note
[^2]: Second note"""
    expected = "Here's a note and another"
    assert parser.parse(text) == expected


# @pytest.mark.parametrize(
#     "input_text,expected",
#     [
#         (r"\*not italic\*", "*not italic*"),
#         (r"\[not a link\]", "[not a link]"),
#         (r"\`not code\`", "`not code`"),
#     ],
# )
# def test_nested_formatting(parser):
#     """Test nested formatting combinations"""
#     test_cases = [
#         ("**_Bold italic_**", "Bold italic"),
#         ("*`Italic code`*", "Italic code"),
#         ("**[Bold link](url)**", "Bold link"),
#         ("`*Code italic*`", "Code italic"),
#     ]
#     for input_text, expected in test_cases:
#         assert parser.parse(input_text) == expected


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("Text\n\n\nMore text", "Text\n\nMore text"),
        ("  Indented  text  ", "Indented  text"),
        ("\n\n\nExtra lines\n\n\n", "Extra lines"),
    ],
)
def test_whitespace_cleaning(parser, input_text, expected):
    """Test whitespace cleaning with different formats"""
    assert parser.parse(input_text) == expected


def test_json_like_structure(parser):
    """Test parsing JSON-like structure"""
    test_cases = [
        ('"answer": "Simple text"', "Simple text"),
        ('"answer": "**Bold** text"', "Bold text"),
        ('"response": "*Italic* text"', "Italic text"),
    ]
    for input_text, expected in test_cases:
        assert parser.parse(input_text) == expected


def test_complex_document(parser):
    """Test parsing a complex document with multiple elements"""
    complex_doc = """
# Main Header

## Subheader

This is a paragraph with **bold** and *italic* text.

- List item 1
  - Nested item
- List item 2

> Blockquote with **bold**
> Multiple lines with *italic*

```python
def hello():
    print('world')
```

1. Ordered list
2. With [link](http://example.com)

| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |

~~Struck through~~ and `inline code`
    """.strip()

    result = parser.parse(complex_doc)

    # Test specific elements are handled correctly
    assert "# Main Header" not in result
    assert "**bold**" not in result
    assert "*italic*" not in result
    assert "```python" not in result
    assert "| Header 1 |" not in result
    assert "~~Struck through~~" not in result
    assert "`inline code`" not in result

    # Test content is preserved
    assert "Main Header" in result
    assert "bold" in result
    assert "italic" in result
    assert "List item" in result
    assert "Blockquote" in result
    assert "[CODE BLOCK]" in result
    assert "inline code" in result


@pytest.fixture
def patterns():
    """Fixture to provide markdown patterns"""
    return MarkdownParser().patterns


@pytest.mark.parametrize(
    "test_input,pattern_key,should_match",
    [
        ("# Header", "headers", True),
        ("### Deep Header", "headers", True),
        ("Plain text", "headers", False),
        ("**bold**", "bold_asterisks", True),
        ("not bold", "bold_asterisks", False),
        ("*italic*", "italic_asterisk", True),
        ("_italic_", "italic_underscore", True),
        ("[link](url)", "links", True),
        ("![image](url)", "images", True),
        ("- list item", "unordered_lists", True),
        ("1. ordered item", "ordered_lists", True),
        ("```code```", "code_blocks", True),
        ("`inline code`", "inline_code", True),
        ("> quote", "blockquotes", True),
        ("~~strike~~", "strikethrough", True),
    ],
)
def test_patterns(patterns, test_input, pattern_key, should_match):
    """Test pattern matching for various markdown elements"""
    pattern = patterns[pattern_key]
    if should_match:
        assert re.search(pattern, test_input, re.MULTILINE) is not None
    else:
        assert re.search(pattern, test_input, re.MULTILINE) is None


def test_pattern_edge_cases(patterns):
    """Test pattern matching for edge cases"""
    edge_cases = [
        ("headers", "#Header", False),  # No space after #
        ("bold_asterisks", "** bold**", False),  # Space after opening **
        ("italic_asterisk", "*italic *", False),  # Space before closing *
        ("links", "[link(url)", False),  # Incomplete link syntax
        ("code_blocks", "```\ncode", False),  # Unclosed code block
    ]

    for pattern_key, test_input, should_match in edge_cases:
        pattern = patterns[pattern_key]
        match = re.search(pattern, test_input, re.MULTILINE)
        assert (match is not None) == should_match
