import re


class MarkdownParser:
    """
    A comprehensive markdown parser that converts markdown text to plain text.
    Handles all common markdown syntax elements.
    """

    def __init__(self):
        # Common markdown patterns
        self.patterns = {
            "headers": r"^#{1,6}\s+",  # Headers with #
            "alternate_h1": r"^=+\s*$",  # Alternate H1 style
            "alternate_h2": r"^-+\s*$",  # Alternate H2 style
            "bold_asterisks": r"\*\*(?!\s)(.+?)(?<!\s)\*\*",  # Bold with **
            "bold_underscores": r"__(?!\s)(.+?)(?<!\s)__",  # Bold with __
            "italic_asterisk": r"\*(?!\s)([^*]+?)(?<!\s)\*",  # Italic with *
            "italic_underscore": r"_(?!\s)([^_]+?)(?<!\s)_",  # Italic with _
            "bold_italic": r"\*\*\*(?!\s)(.+?)(?<!\s)\*\*\*",  # Bold and italic
            "code_blocks": r"```[\s\S]*?```",  # Code blocks
            "inline_code": r"`([^`]+)`",  # Inline code
            "links": r"\[([^\]]+)\]\(([^)]+)\)",  # Links [text](url)
            "images": r"!\[([^\]]*)\]\(([^)]+)\)",  # Images ![alt](url)
            "reference_links": r"\[([^\]]+)\]\[([^\]]*)\]",  # Reference links
            "reference_defs": r"^\[([^\]]+)\]:\s*([^\s]+)(?:\s+\"([^\"]+)\")?\s*$",  # Reference definitions
            "blockquotes": r"^\s*>\s+",  # Blockquotes
            "unordered_lists": r"^\s*[-*+]\s+",  # Unordered lists
            "ordered_lists": r"^\s*\d+\.\s+",  # Ordered lists
            "horizontal_rules": r"^(?:\*{3,}|-{3,}|_{3,})\s*$",  # Horizontal rules
            "strikethrough": r"~~(.+?)~~",  # Strikethrough
            "html_tags": r"<[^>]+>",  # HTML tags
            "footnotes": r"\[\^([^\]]+)\](?!:)",  # Footnotes
            "footnote_defs": r"^\[\^([^\]]+)\]:\s*(.+)$",  # Footnote definitions
            "task_lists": r"^\s*[-*+]\s+\[([ xX])\]\s*(.+)$",  # Task lists
            "tables": r"\|.*\|",  # Tables
            "escape_chars": r"\\([\\`*{}[\]()#+\-.!_>])",  # Escaped characters
        }

    def remove_code_blocks(self, text):
        """Remove code blocks and replace with placeholder text"""
        return re.sub(
            self.patterns["code_blocks"],
            "[CODE BLOCK]",
            text,
            flags=re.MULTILINE | re.DOTALL,
        )

    def remove_inline_code(self, text):
        """Convert inline code to plain text"""
        return re.sub(self.patterns["inline_code"], r"\1", text)

    def remove_headers(self, text):
        """Remove all header styles"""
        # Remove # style headers
        text = re.sub(self.patterns["headers"], "", text, flags=re.MULTILINE)

        # Handle alternate style headers (===== and ------)
        lines = text.split("\n")
        processed_lines = []
        skip_next = False

        for i, line in enumerate(lines):
            if skip_next:
                skip_next = False
                continue

            if i < len(lines) - 1:
                next_line = lines[i + 1]
                if re.match(self.patterns["alternate_h1"], next_line):
                    processed_lines.append(line)
                    skip_next = True
                elif re.match(self.patterns["alternate_h2"], next_line):
                    processed_lines.append(line)
                    skip_next = True
                else:
                    processed_lines.append(line)
            else:
                processed_lines.append(line)

        return "\n".join(processed_lines)

    def remove_emphasis(self, text):
        """Remove all emphasis (bold, italic, bold-italic)"""
        text = re.sub(self.patterns["bold_italic"], r"\1", text)
        text = re.sub(self.patterns["bold_asterisks"], r"\1", text)
        text = re.sub(self.patterns["bold_underscores"], r"\1", text)
        text = re.sub(self.patterns["italic_asterisk"], r"\1", text)
        text = re.sub(self.patterns["italic_underscore"], r"\1", text)
        return text

    def remove_reference_links(self, text):
        """Remove reference-style links, preserving text content"""
        # First remove reference definitions and store link text
        text = re.sub(r"^\[([^\]]+)\]:\s*[^\n]*$", "", text, flags=re.MULTILINE)
        # Then handle reference link usage, keeping only the link text
        text = re.sub(r"\[([^\]]+)\]\[[^\]]*\]", r"\1", text)
        return text.strip()

    def remove_links_and_images(self, text):
        """Remove markdown links and images, preserving text content"""
        text = re.sub(
            self.patterns["images"], r"\1", text
        )  # Replace images with alt text
        text = re.sub(self.patterns["links"], r"\1", text)  # Replace links with text
        return text

    def remove_task_lists(self, text):
        """Convert task lists to plain text, removing checkbox markers"""
        return re.sub(
            r"^\s*[-*+]\s+\[([ xX])\]\s*(.+)$", r"\2", text, flags=re.MULTILINE
        )

    def remove_lists(self, text):
        """Convert markdown lists to plain text"""
        text = re.sub(
            self.patterns["unordered_lists"] + "(.+)", r"\1", text, flags=re.MULTILINE
        )
        text = re.sub(
            self.patterns["ordered_lists"] + "(.+)", r"\1", text, flags=re.MULTILINE
        )
        return text

    def remove_blockquotes(self, text):
        """Remove blockquote markers and preserve content with proper spacing"""
        lines = text.split("\n")
        result = []
        for line in lines:
            # Count number of '>' characters to preserve proper spacing
            gt_count = len(re.findall(r">", line))
            # Replace blockquote markers with appropriate number of spaces
            line = re.sub(r"^\s*(?:>\s*)+", " " * (gt_count + 1), line)
            result.append(line)
        return "\n".join(result)

    def remove_horizontal_rules(self, text):
        """Remove horizontal rules"""
        lines = []
        for line in text.split("\n"):
            if not re.match(r"^\s*[-*_](\s*[-*_])*\s*$", line):
                lines.append(line)
        return "\n".join(lines)

    def remove_tables(self, text):
        """Remove markdown tables"""
        lines = text.split("\n")
        return "\n".join(
            line for line in lines if not re.match(self.patterns["tables"], line)
        )

    def remove_html(self, text):
        """Remove HTML tags"""
        return re.sub(self.patterns["html_tags"], "", text)

    def remove_strikethrough(self, text):
        """Remove strikethrough formatting"""
        return re.sub(self.patterns["strikethrough"], r"\1", text)

    def remove_footnotes(self, text):
        """Remove footnotes and their definitions"""
        # Remove footnote references
        text = re.sub(self.patterns["footnotes"], "", text)
        # Remove footnote definitions
        text = re.sub(self.patterns["footnote_defs"], "", text, flags=re.MULTILINE)
        return text.strip()

    def unescape_characters(self, text):
        """Remove escape characters while preserving the actual characters"""

        def replace_escape(match):
            """Helper function to handle escaped characters"""
            char = match.group(1)
            # These are the special markdown characters we want to preserve without the escape
            if char in r"`*_{}[]()#+-.!\\":
                return char
            return "\\" + char

        # Run the replacement multiple times to handle nested escapes
        for _ in range(2):  # Two passes should handle most cases
            text = re.sub(r"\\([\\`*_{}\[\]()#+\-.!])", replace_escape, text)

        return text

    def clean_whitespace(self, text):
        """Clean up excessive whitespace"""
        # Replace multiple newlines with double newlines
        text = re.sub(r"\n{3,}", "\n\n", text)
        # Remove trailing/leading whitespace from lines
        text = "\n".join(line.strip() for line in text.split("\n"))
        # Remove trailing/leading whitespace from whole text
        return text.strip()

    def parse(self, markdown_text):
        """
        Convert markdown text to plain text by removing all markdown formatting

        Args:
            markdown_text (str): The markdown text to be converted

        Returns:
            str: Plain text without markdown formatting
        """
        # Handle JSON-like structure if present
        if markdown_text.startswith('"') and ":" in markdown_text:
            try:
                content = markdown_text.split(":", 1)[1].strip().strip('"')
                content = content.replace("\\n", "\n").replace('\\"', '"')
            except:
                content = markdown_text
        else:
            content = markdown_text

        # Apply transformations in the correct order
        text = content
        transformations = [
            self.remove_code_blocks,
            self.remove_inline_code,
            self.remove_headers,
            self.remove_emphasis,
            self.remove_reference_links,
            self.remove_links_and_images,
            self.remove_task_lists,
            self.remove_lists,
            self.unescape_characters,  # Move unescaping before blockquotes
            self.remove_blockquotes,
            self.remove_horizontal_rules,
            self.remove_tables,
            self.remove_html,
            self.remove_strikethrough,
            self.remove_footnotes,
            self.clean_whitespace,
        ]

        for transform in transformations:
            text = transform(text)

        return text
