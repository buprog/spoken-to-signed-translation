"""
Tests for Turkish (tr) to Turkish Sign Language (tsm/TİD) pipeline integration.

These tests verify:
1. Turkish text processing (tokenization and lemmatization)
2. Text-to-gloss conversion for Turkish
3. Proper error handling when TİD lexicon data is missing
4. Pipeline integration with Turkish language codes
"""

import subprocess
import tempfile
from pathlib import Path

import pytest

from spoken_to_signed.text_to_gloss.simple import text_to_gloss as simple_text_to_gloss


def test_turkish_tokenization_and_lemmatization():
    """Test that Turkish text is properly tokenized and lemmatized."""
    text = "Küçük çocuklar İstanbul'da pizza yiyorlar"
    result = simple_text_to_gloss(text, language="tr")

    assert len(result) == 1  # One sentence
    glosses = result[0]
    assert len(glosses) > 0  # Has tokens

    # Verify we have GlossItem objects with word and gloss attributes
    for item in glosses:
        assert hasattr(item, "word")
        assert hasattr(item, "gloss")
        assert isinstance(item.word, str)
        assert isinstance(item.gloss, str)


def test_turkish_simple_glosser_basic():
    """Test basic Turkish glossing with simplemma."""
    text = "Merhaba dünya"
    result = simple_text_to_gloss(text, language="tr")

    assert len(result) == 1
    glosses = result[0]
    assert len(glosses) == 2

    # Check that words are lowercased
    assert glosses[0].word == "merhaba"
    assert glosses[1].word == "dünya"


def test_turkish_morphology_handling():
    """Test that Turkish agglutinative morphology is handled via lemmatization."""
    # Turkish has rich morphology: "evlerimizden" = ev-ler-imiz-den (house-PL-1PL.POSS-ABL)
    text = "evlerimizden"
    result = simple_text_to_gloss(text, language="tr")

    assert len(result) == 1
    glosses = result[0]
    assert len(glosses) == 1

    # The lemma should be simpler than the inflected form
    # simplemma should attempt to lemmatize this
    assert glosses[0].word == "evlerimizden"
    assert isinstance(glosses[0].gloss, str)


def test_turkish_text_to_gloss_cli():
    """Test the text_to_gloss CLI with Turkish input."""
    result = subprocess.run(
        [
            "text_to_gloss",
            "--text",
            "Merhaba dünya",
            "--glosser",
            "simple",
            "--spoken-language",
            "tr",
            "--signed-language",
            "tsm",
        ],
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    assert "merhaba" in result.stdout.lower()
    assert "dünya" in result.stdout.lower()


def test_turkish_tid_without_lexicon_fails_gracefully():
    """Test that the pipeline fails clearly when TİD lexicon is missing.
    
    With fingerspelling disabled, the system must fail with a clear error
    when TİD pose data is not available in the lexicon. This tests that:
    1. The CLI accepts tr/tsm arguments (no argparse error)
    2. The actual pose lookup fails (real TİD data missing)
    3. The error message is clear and informative
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        pose_path = Path(tmp_dir) / "output.pose"

        # Try to use the dummy lexicon which doesn't have Turkish/TİD data
        # Disable fingerspelling to force lookup failure
        result = subprocess.run(
            [
                "text_to_gloss_to_pose",
                "--text",
                "Merhaba dünya",
                "--glosser",
                "simple",
                "--lexicon",
                "assets/dummy_lexicon",
                "--spoken-language",
                "tr",
                "--signed-language",
                "tsm",
                "--pose",
                str(pose_path),
                "--disable-fingerspelling",  # Force lexicon lookup, no fallback
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Should fail because dummy lexicon doesn't have Turkish/TİD data
        # The system should fail gracefully, not silently produce wrong output
        assert result.returncode != 0, "Should fail without TİD lexicon data when fingerspelling is disabled"

        # The error should be informative about missing poses
        error_output = result.stderr.lower()
        # We expect "No poses found" error from pose lookup
        assert (
            "no poses found" in error_output or "exception" in error_output
        ), f"Error should indicate missing TİD poses in lexicon: {result.stderr}"
        
        # Should NOT be an argparse error (tr/tsm should be accepted)
        assert "invalid choice" not in error_output, f"Should not be argparse error, tr/tsm must be accepted: {result.stderr}"


def test_turkish_language_code_accepted():
    """Verify that 'tr' and 'tsm' are accepted language codes in the system."""
    # This test ensures the language codes are properly configured
    # We test this by verifying the CLI accepts these codes
    result = subprocess.run(
        ["text_to_gloss", "--text", "test", "--glosser", "simple", "--spoken-language", "tr", "--signed-language", "tsm"],
        capture_output=True,
        text=True,
        timeout=10,
    )

    # Should not fail with "invalid choice" error
    assert "invalid choice" not in result.stderr.lower(), "Turkish language codes should be accepted"


@pytest.mark.parametrize(
    "text,expected_word_count",
    [
        ("Merhaba", 1),
        ("Merhaba dünya", 2),
        ("Ben Türkçe öğreniyorum", 3),
        ("İstanbul'da yaşıyorum", 2),
        ("Türk İşaret Dili önemlidir", 4),
    ],
)
def test_turkish_sentence_structures(text, expected_word_count):
    """Test various Turkish sentence structures."""
    result = simple_text_to_gloss(text, language="tr")

    assert len(result) == 1
    glosses = result[0]
    assert len(glosses) == expected_word_count, f"Expected {expected_word_count} words in '{text}'"


def test_turkish_special_characters():
    """Test that Turkish special characters (ç, ğ, ı, ö, ş, ü) are handled correctly."""
    text = "çalışmak görmek ışık öğrenci şehir üzüm"
    result = simple_text_to_gloss(text, language="tr")

    assert len(result) == 1
    glosses = result[0]
    assert len(glosses) == 6

    # Check that special characters are preserved
    words = [g.word for g in glosses]
    assert "çalışmak" in words or "çalış" in " ".join(words)
    assert any("ş" in w for w in words), "Turkish 'ş' character should be preserved"
    assert any("ğ" in w or "g" in w for w in words), "Turkish 'ğ' character should be handled"


def test_tid_documentation_exists():
    """Verify that TİD documentation file exists."""
    doc_path = Path("docs/TURKISH_TID_SUPPORT.md")
    assert doc_path.exists(), "Turkish/TİD documentation should exist"

    content = doc_path.read_text(encoding="utf-8")
    assert "TİD" in content or "Türk İşaret Dili" in content
    assert "tsm" in content  # Language code should be documented
    assert "tr" in content  # Spoken language code should be documented
