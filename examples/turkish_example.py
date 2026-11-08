#!/usr/bin/env python3
"""
Turkish (Türkçe) to Turkish Sign Language (TİD) Example
========================================================

This example demonstrates the Turkish language support in the spoken-to-signed pipeline.

IMPORTANT: This example shows text-to-gloss conversion only, which WORKS with Turkish.
The gloss-to-pose and pose-to-video steps require a real TİD lexicon, which is
not included in this repository.

Requirements:
    pip install spoken-to-signed

Usage:
    python examples/turkish_example.py
"""

from spoken_to_signed.text_to_gloss.simple import text_to_gloss


def print_separator():
    print("\n" + "=" * 70 + "\n")


def demo_turkish_glossing():
    """Demonstrate Turkish text to gloss conversion."""
    print("Türkçe Metin → Gloss Dönüşümü / Turkish Text → Gloss Conversion")
    print_separator()

    examples = [
        "Merhaba dünya",
        "Ben Türkçe öğreniyorum",
        "Küçük çocuklar İstanbul'da pizza yiyorlar",
        "Türk İşaret Dili önemli bir dildir",
        "Bugün hava çok güzel",
    ]

    for text in examples:
        print(f"Input (Türkçe): {text}")

        # Process with simple glosser
        result = text_to_gloss(text, language="tr")

        # Extract glosses
        glosses = result[0]  # First (and only) sentence
        gloss_output = " ".join(g.gloss.upper() for g in glosses)

        print(f"Gloss Output:   {gloss_output}")
        print()

    print_separator()


def explain_tid_limitations():
    """Explain what works and what requires TİD data."""
    print("TİD Destek Durumu / TİD Support Status")
    print_separator()

    print("✅ ÇALIŞIYOR / WORKING:")
    print("   - Türkçe metin işleme / Turkish text processing")
    print("   - Tokenizasyon / Tokenization")
    print("   - Lemmatizasyon / Lemmatization")
    print("   - Metin → Gloss dönüşümü / Text → Gloss conversion")
    print()

    print("⚠️  GERÇEKTİR TİD VERİSİ GEREKTİRİR / REQUIRES REAL TİD DATA:")
    print("   - Gloss → Pose dönüşümü / Gloss → Pose conversion")
    print("   - TİD işaret sözlüğü / TİD sign lexicon")
    print("   - Pose → Video oluşturma / Pose → Video generation")
    print()

    print("Bu repository gerçek TİD pose verisi içermemektedir.")
    print("This repository does not include real TİD pose data.")
    print()
    print("Daha fazla bilgi için: docs/TURKISH_TID_SUPPORT.md")
    print("For more information: docs/TURKISH_TID_SUPPORT.md")
    print_separator()


def show_cli_usage():
    """Show command-line usage examples."""
    print("Komut Satırı Kullanımı / Command Line Usage")
    print_separator()

    print("Text to Gloss (WORKS / ÇALIŞIR):")
    print()
    print("  text_to_gloss \\")
    print('    --text "Merhaba dünya" \\')
    print("    --glosser simple \\")
    print("    --spoken-language tr \\")
    print("    --signed-language tsm")
    print()
    print_separator()

    print("Text to Gloss to Pose (REQUIRES TİD LEXICON / TİD SÖZLÜĞÜ GEREKTİRİR):")
    print()
    print("  text_to_gloss_to_pose \\")
    print('    --text "Merhaba dünya" \\')
    print("    --glosser simple \\")
    print("    --lexicon /path/to/tid/lexicon \\  # TİD sözlüğü / TİD lexicon needed!")
    print("    --spoken-language tr \\")
    print("    --signed-language tsm \\")
    print("    --pose output.pose")
    print()
    print("Note: This will fail without a real TİD lexicon.")
    print("Not: Gerçek TİD sözlüğü olmadan başarısız olacaktır.")
    print_separator()


if __name__ == "__main__":
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║   Türkçe → Türk İşaret Dili (TİD) Örneği                        ║")
    print("║   Turkish → Turkish Sign Language (TİD) Example                  ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print()

    demo_turkish_glossing()
    explain_tid_limitations()
    show_cli_usage()

    print("\n✅ Örnek tamamlandı! / Example completed!\n")
