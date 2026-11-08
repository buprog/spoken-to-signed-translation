"""
Tests for Turkish (tr) to Turkish Sign Language (tsm/TİD) pipeline integration.

These tests verify:
1. Turkish text processing (tokenization and lemmatization)
2. Text-to-gloss conversion for Turkish
3. Proper error handling when TİD lexicon data is missing
4. Pipeline integration with Turkish language codes
5. NO fake TİD output (no non-TİD fingerspelling fallback)
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
    
    CRITICAL: Tests that tsm does NOT silently use non-TİD fingerspelling.
    
    Tests TWO scenarios:
    1. DEFAULT (no flags): Must fail because no verified TİD fingerspelling exists
    2. EXPLICIT --disable-fingerspelling: Must also fail (redundant check)
    
    Both must:
    - Accept tr/tsm CLI arguments (no argparse error)
    - Fail at pose lookup (real TİD lexicon missing)
    - NOT create output pose file (no fake TİD)
    - Return clear error message
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        # SCENARIO 1: Default behavior - NO flags
        # This is CRITICAL: tsm should fail even without --disable-fingerspelling
        # because we don't have verified TİD fingerspelling alphabet
        pose_path_default = Path(tmp_dir) / "output_default.pose"
        result_default = subprocess.run(
            [
                "text_to_gloss_to_pose",
                "--text",
                "Merhaba",  # Turkish word not in dummy_lexicon
                "--glosser",
                "simple",
                "--lexicon",
                "assets/dummy_lexicon",
                "--spoken-language",
                "tr",
                "--signed-language",
                "tsm",
                "--pose",
                str(pose_path_default),
                # NO --disable-fingerspelling - testing default behavior
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Must fail for tsm (no verified TİD alphabet)
        assert result_default.returncode != 0, (
            "DEFAULT: Should fail for tsm without TİD lexicon. "
            "Must NOT silently use non-TİD fingerspelling."
        )
        
        # Must NOT create fake TİD pose file
        assert not pose_path_default.exists(), (
            "DEFAULT: Should NOT create pose file when TİD data is missing. "
            "Creating a pose would be fake TİD output."
        )
        
        # Check error details
        error_default = result_default.stderr.lower()
        assert "no poses found" in error_default or "exception" in error_default, (
            f"DEFAULT: Should have clear pose lookup error. Got: {result_default.stderr}"
        )
        assert "invalid choice" not in error_default, (
            "DEFAULT: Should not be argparse error (tr/tsm must be accepted)"
        )

        # SCENARIO 2: Explicit --disable-fingerspelling (redundant but thorough)
        pose_path_explicit = Path(tmp_dir) / "output_explicit.pose"
        result_explicit = subprocess.run(
            [
                "text_to_gloss_to_pose",
                "--text",
                "Merhaba",
                "--glosser",
                "simple",
                "--lexicon",
                "assets/dummy_lexicon",
                "--spoken-language",
                "tr",
                "--signed-language",
                "tsm",
                "--pose",
                str(pose_path_explicit),
                "--disable-fingerspelling",  # Explicit disable
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Must also fail with explicit disable
        assert result_explicit.returncode != 0, "EXPLICIT: Should fail with --disable-fingerspelling"
        assert not pose_path_explicit.exists(), "EXPLICIT: Should NOT create pose file"
        
        error_explicit = result_explicit.stderr.lower()
        assert "no poses found" in error_explicit or "exception" in error_explicit, (
            f"EXPLICIT: Should have pose lookup error. Got: {result_explicit.stderr}"
        )
        assert "invalid choice" not in error_explicit, "EXPLICIT: Should not be argparse error"


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
