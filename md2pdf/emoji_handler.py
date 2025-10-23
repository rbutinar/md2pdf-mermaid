#!/usr/bin/env python3
"""
Emoji handling utilities for PDF conversion
Provides multiple strategies for rendering emoji in PDFs
"""

import re
import tempfile
import os
from typing import Optional, Tuple, List


def detect_emoji(text: str) -> List[Tuple[str, int, int]]:
    """
    Detect all emoji characters in text and return their positions.

    Args:
        text: Input text to scan for emoji

    Returns:
        List of (emoji_char, start_pos, end_pos) tuples
    """
    if not text:
        return []

    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U00002600-\U000026FF"  # misc symbols
        "\U00002700-\U000027BF"  # dingbats
        "\U0001F018-\U0001F270"  # various symbols
        "\U0000231A-\U0000231B"  # watches
        "\U000023E9-\U000023FA"  # av symbols
        "\U000025AA-\U000025FE"  # geometric shapes
        "\U00002B05-\U00002B07"  # arrows
        "\U00002934-\U00002935"  # arrows
        "\U00003030"              # wavy dash
        "\U0000303D"              # part alternation mark
        "\U00003297"              # circled ideograph
        "\U00003299"              # circled ideograph
        "\U0001F170-\U0001F251"  # enclosed alphanumerics
        "]+",
        flags=re.UNICODE
    )

    results = []
    for match in emoji_pattern.finditer(text):
        results.append((match.group(), match.start(), match.end()))

    return results


def is_simple_symbol(char: str) -> bool:
    """
    Check if a character is a simple symbol that should be preserved.

    These are characters that look like emoji but are actually standard
    Unicode symbols that most fonts support.

    Args:
        char: Single character to check

    Returns:
        True if it's a simple symbol that should not be treated as emoji
    """
    codepoint = ord(char)

    # Simple arrows (commonly supported)
    simple_arrows = [
        0x2190, 0x2191, 0x2192, 0x2193,  # ← ↑ → ↓
        0x2194, 0x2195,                   # ↔ ↕
        0x21D0, 0x21D1, 0x21D2, 0x21D3,  # ⇐ ⇑ ⇒ ⇓
        0x21D4, 0x21D5,                   # ⇔ ⇕
        0x2934, 0x2935,                   # ⤴ ⤵
        0x2B05, 0x2B06, 0x2B07,          # ⬅ ⬆ ⬇
    ]

    # Math and technical symbols
    technical_symbols = [
        0x00D7,  # ×
        0x00F7,  # ÷
        0x2212,  # −
        0x2260,  # ≠
        0x2264,  # ≤
        0x2265,  # ≥
        0x221E,  # ∞
    ]

    # Checkmarks, X marks, and boxes (basic forms used in markdown)
    basic_checks = [
        0x2713,  # ✓ checkmark
        0x2714,  # ✔ heavy checkmark
        0x2717,  # ✗ ballot X
        0x2718,  # ✘ heavy ballot X
        0x2610,  # ☐ ballot box
        0x2611,  # ☑ ballot box with check
        0x2612,  # ☒ ballot box with X
    ]

    # Stars and basic geometric shapes
    basic_shapes = [
        0x2605,  # ★ black star
        0x2606,  # ☆ white star
        0x25A0,  # ■ black square
        0x25A1,  # □ white square
        0x25B2,  # ▲ black up-pointing triangle
        0x25B3,  # △ white up-pointing triangle
        0x25BC,  # ▼ black down-pointing triangle
        0x25BD,  # ▽ white down-pointing triangle
        0x25C6,  # ◆ black diamond
        0x25C7,  # ◇ white diamond
    ]

    # Note: ✅ (0x2705) is NOT included here because it's typically rendered
    # as a colorful emoji. We want to convert it to an image for color support.

    return codepoint in simple_arrows + technical_symbols + basic_checks + basic_shapes


def try_pilmoji_conversion(text: str) -> Optional[Tuple[str, List[str]]]:
    """
    Try to convert emoji to inline images using Pilmoji.

    This function attempts to:
    1. Detect emoji in text
    2. Generate PNG images for each emoji using Pilmoji
    3. Return modified text with image placeholders and list of image paths

    Args:
        text: Text containing emoji

    Returns:
        Tuple of (modified_text, [image_paths]) if successful, None if Pilmoji unavailable
        Image paths are temporary files that should be cleaned up by caller
    """
    try:
        from pilmoji import Pilmoji
        from PIL import Image, ImageFont, ImageDraw
    except ImportError:
        return None

    emoji_list = detect_emoji(text)
    if not emoji_list:
        return text, []

    # Create temporary directory for emoji images
    temp_dir = tempfile.mkdtemp(prefix='md2pdf_emoji_')
    image_paths = []
    modified_text = text
    offset = 0  # Track position changes due to replacements

    # Font size for emoji rendering (needs to be large for good quality)
    emoji_size = 72  # 72pt for good quality

    for emoji_char, start, end in emoji_list:
        # Skip simple symbols that don't need image conversion
        if len(emoji_char) == 1 and is_simple_symbol(emoji_char):
            continue

        try:
            # Create a small image for the emoji
            img = Image.new('RGBA', (emoji_size, emoji_size), (255, 255, 255, 0))

            # Use Pilmoji to render the emoji
            with Pilmoji(img) as pilmoji:
                # Draw emoji at position (0, 0)
                pilmoji.text((0, 0), emoji_char, fill=(0, 0, 0, 255),
                           font=ImageFont.truetype("arial.ttf", emoji_size) if os.name == 'nt'
                           else ImageFont.load_default())

            # Save to temporary file
            img_path = os.path.join(temp_dir, f'emoji_{len(image_paths)}.png')
            img.save(img_path, 'PNG')
            image_paths.append(img_path)

            # Create placeholder for ReportLab
            # We'll use a special marker that converter.py can recognize
            placeholder = f'<img src="{img_path}" width="12" height="12" valign="middle"/>'

            # Replace emoji with placeholder
            adj_start = start + offset
            adj_end = end + offset
            modified_text = modified_text[:adj_start] + placeholder + modified_text[adj_end:]
            offset += len(placeholder) - (end - start)

        except Exception as e:
            # If rendering fails, leave the emoji as-is
            print(f"Warning: Failed to render emoji {emoji_char}: {e}")
            continue

    return modified_text, image_paths


def remove_unsupported_emoji(text: str, keep_simple_symbols: bool = True) -> str:
    """
    Remove emoji that cannot be rendered, optionally keeping simple symbols.

    This is a fallback when no other emoji rendering method is available.

    Args:
        text: Input text
        keep_simple_symbols: If True, keep simple Unicode symbols (arrows, checkmarks)

    Returns:
        Text with unsupported emoji removed
    """
    if not text:
        return text

    result = []
    for char in text:
        codepoint = ord(char)

        # Keep simple symbols if requested
        if keep_simple_symbols and is_simple_symbol(char):
            result.append(char)
            continue

        # Check if character is an emoji (simplified heuristic)
        is_emoji = (
            (codepoint >= 0x1F300 and codepoint <= 0x1F9FF) or  # Misc symbols and pictographs
            (codepoint >= 0x2600 and codepoint <= 0x26FF) or    # Misc symbols
            (codepoint >= 0x2700 and codepoint <= 0x27BF) or    # Dingbats
            (codepoint >= 0x1F600 and codepoint <= 0x1F64F) or  # Emoticons
            (codepoint >= 0x1F680 and codepoint <= 0x1F6FF) or  # Transport and map symbols
            (codepoint >= 0x2300 and codepoint <= 0x23FF) or    # Miscellaneous Technical
            (codepoint >= 0xFE00 and codepoint <= 0xFE0F)       # Variation selectors
        )

        if not is_emoji:
            result.append(char)

    return ''.join(result)


class EmojiHandler:
    """
    High-level emoji handler that tries multiple strategies.

    Strategies (in order of preference):
    1. Pilmoji: Convert emoji to colored PNG images
    2. Symbola font: Render emoji in black & white using Unicode font
    3. Removal: Remove unsupported emoji as fallback
    """

    def __init__(self, strategy: str = 'auto'):
        """
        Initialize emoji handler.

        Args:
            strategy: 'auto', 'pilmoji', 'font', or 'remove'
        """
        self.strategy = strategy
        self.temp_files = []

    def process_text(self, text: str) -> str:
        """
        Process text according to selected strategy.

        Args:
            text: Input text with potential emoji

        Returns:
            Processed text
        """
        if self.strategy == 'auto':
            # Try strategies in order of preference
            result = try_pilmoji_conversion(text)
            if result:
                modified_text, temp_files = result
                self.temp_files.extend(temp_files)
                return modified_text

            # Fallback to removal with simple symbols preserved
            return remove_unsupported_emoji(text, keep_simple_symbols=True)

        elif self.strategy == 'pilmoji':
            result = try_pilmoji_conversion(text)
            if result:
                modified_text, temp_files = result
                self.temp_files.extend(temp_files)
                return modified_text
            else:
                raise RuntimeError("Pilmoji is not installed. Install with: pip install pilmoji")

        elif self.strategy == 'font':
            # For font strategy, we keep all emoji and rely on font support
            # This is handled in converter.py by using appropriate fonts
            return text

        elif self.strategy == 'remove':
            return remove_unsupported_emoji(text, keep_simple_symbols=True)

        elif self.strategy == 'keep' or self.strategy == 'font':
            # Keep all emoji and symbols - requires Unicode font support in PDF
            # This is handled by the font configuration in converter.py
            return text

        else:
            raise ValueError(f"Unknown emoji strategy: {self.strategy}")

    def cleanup(self):
        """Clean up temporary files created during emoji conversion."""
        for file_path in self.temp_files:
            try:
                os.unlink(file_path)
            except:
                pass

        # Also try to remove temp directories
        temp_dirs = set(os.path.dirname(f) for f in self.temp_files)
        for temp_dir in temp_dirs:
            try:
                os.rmdir(temp_dir)
            except:
                pass

        self.temp_files.clear()
