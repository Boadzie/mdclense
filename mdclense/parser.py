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
            "bold_asterisks": r"\*\*(.+?)\*\*",  # Bold with **
            "bold_underscores": r"__(.+?)__",  # Bold with __
            "italic_asterisk": r"\*([^*]+?)\*",  # Italic with *
            "italic_underscore": r"_([^_]+?)_",  # Italic with _
            "bold_italic": r"\*\*\*(.+?)\*\*\*",  # Bold and italic
            "code_blocks": r"```[\s\S]*?```",  # Code blocks
            "inline_code": r"`([^`]+)`",  # Inline code
            "links": r"\[([^\]]+)\]\(([^)]+)\)",  # Links [text](url)
            "images": r"!\[([^\]]*)\]\(([^)]+)\)",  # Images ![alt](url)
            "reference_links": r"\[([^\]]+)\]\[([^\]]*)\]",  # Reference links
            "blockquotes": r"^\s*>\s+",  # Blockquotes
            "unordered_lists": r"^\s*[-*+]\s+",  # Unordered lists
            "ordered_lists": r"^\s*\d+\.\s+",  # Ordered lists
            "horizontal_rules": r"^(?:\*{3,}|-{3,}|_{3,})\s*$",  # Horizontal rules
            "strikethrough": r"~~(.+?)~~",  # Strikethrough
            "html_tags": r"<[^>]+>",  # HTML tags
            "footnotes": r"\[\^([^\]]+)\]",  # Footnotes
            "task_lists": r"^\s*- \[([ xX])\]",  # Task lists
            "tables": r"\|.*\|",  # Tables
            "escape_chars": r"\\([\\`*{}[\]()#+\-.!_>])",  # Escaped characters
        }

    def remove_code_blocks(self, text):
        """Remove code blocks and replace with placeholder text"""
        return re.sub(self.patterns["code_blocks"], "[CODE BLOCK]", text)

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

    def remove_links_and_images(self, text):
        """Remove markdown links and images, preserving text content"""
        text = re.sub(
            self.patterns["images"], r"\1", text
        )  # Replace images with alt text
        text = re.sub(self.patterns["links"], r"\1", text)  # Replace links with text
        text = re.sub(
            self.patterns["reference_links"], r"\1", text
        )  # Replace reference links
        return text

    def remove_lists(self, text):
        """Convert markdown lists to plain text"""
        text = re.sub(self.patterns["unordered_lists"], "", text, flags=re.MULTILINE)
        text = re.sub(self.patterns["ordered_lists"], "", text, flags=re.MULTILINE)
        text = re.sub(self.patterns["task_lists"], "", text, flags=re.MULTILINE)
        return text

    def remove_blockquotes(self, text):
        """Remove blockquote markers"""
        return re.sub(self.patterns["blockquotes"], "", text, flags=re.MULTILINE)

    def remove_horizontal_rules(self, text):
        """Remove horizontal rules"""
        return re.sub(self.patterns["horizontal_rules"], "", text, flags=re.MULTILINE)

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
        """Remove footnotes"""
        return re.sub(self.patterns["footnotes"], "", text)

    def unescape_characters(self, text):
        """Remove escape characters while preserving the actual characters"""
        return re.sub(self.patterns["escape_chars"], r"\1", text)

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
                # Extract content from JSON-like structure
                content = markdown_text.split(":", 1)[1].strip().strip('"')
                # Remove escape characters from JSON string
                content = content.replace("\\n", "\n").replace('\\"', '"')
            except:
                content = markdown_text
        else:
            content = markdown_text

        # Apply all transformations
        text = content
        text = self.remove_code_blocks(text)
        text = self.remove_inline_code(text)
        text = self.remove_headers(text)
        text = self.remove_emphasis(text)
        text = self.remove_links_and_images(text)
        text = self.remove_lists(text)
        text = self.remove_blockquotes(text)
        text = self.remove_horizontal_rules(text)
        text = self.remove_tables(text)
        text = self.remove_html(text)
        text = self.remove_strikethrough(text)
        text = self.remove_footnotes(text)
        text = self.unescape_characters(text)
        text = self.clean_whitespace(text)

        return text
