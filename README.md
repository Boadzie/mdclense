# `mdclense`

> A lightweight, efficient Python library for converting Markdown to plain text. `mdclense` strips away all Markdown formatting while preserving the original content, making it perfect for text analysis, content extraction, and data processing pipelines.

## Features

- Comprehensive Markdown support
- Preserves content while removing formatting
- Handles complex nested structures
- Clean whitespace management
- JSON-like structure support
- Zero dependencies beyond Python standard library

## Supported Markdown Elements

- Headers (ATX and Setext style)
- Emphasis (bold, italic, bold-italic)
- Links and images
- Lists (ordered, unordered, and task lists)
- Code blocks and inline code
- Blockquotes
- Tables
- Horizontal rules
- HTML tags
- Strikethrough
- Footnotes
- Escaped characters

## Installation

```bash
pip install mdclense
```

## Quick Start

```python
from mdclense.parser import MarkdownParser


# Create a parser instance
parser = MarkdownParser()

# Convert markdown to plain text
markdown_text = """
# Hello World

This is a **bold** and *italic* text with a [link](http://example.com).

- List item 1
- List item 2
"""

plain_text = parser.parse(markdown_text)
print(plain_text)
```

Output:

```
Hello World

This is a bold and italic text with a link.

List item 1
List item 2
```

## Advanced Usage

### Handling JSON-like Structures

```python
# Parse markdown content from JSON-like structure
json_text = '"answer": "This is **bold** text with a [link](url)"'
plain_text = parser.parse(json_text)
print(plain_text)  # Output: This is bold text with a link
```

### Working with Code Blocks

````python
markdown_text = '''
Here's some code:

```python
def hello():
    print("world")
````

'''

plain_text = parser.parse(markdown_text)
print(plain_text) # Code blocks are replaced with [CODE BLOCK] placeholder

````

## API Reference

### MarkdownParser Class

```python
class MarkdownParser:
    def parse(markdown_text: str) -> str:
        """
        Convert markdown text to plain text by removing all markdown formatting.

        Args:
            markdown_text (str): The markdown text to be converted

        Returns:
            str: Plain text without markdown formatting
        """
````

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Testing

```bash
# Install development dependencies
pip install pytest

# Run tests
pytest tests/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the need for a simple, dependency-free Markdown to plain text converter
- Thanks to all contributors who have helped shape this project
