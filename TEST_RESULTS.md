# Türk İşaret Dili (TİD) - Ham Test Sonuçları

## Test Ortamı
- **OS:** Linux (Ubuntu)
- **Python:** 3.12.3
- **Tarih:** 8 Kasım 2026
- **Branch:** cursor/add-turkish-tid-infrastructure-8e63

## Test 1: Paket Kurulumu
```bash
cd /workspace
pip install -e .
```
**Sonuç:** ✅ Başarılı
```
Successfully installed spoken-to-signed
```

## Test 2: Tüm Türkçe Testleri
```bash
export PATH="$HOME/.local/bin:$PATH"
pytest tests/test_turkish_tid.py -v
```
**Sonuç:** ✅ 13/13 Geçti
```
tests/test_turkish_tid.py::test_turkish_tokenization_and_lemmatization PASSED [  7%]
tests/test_turkish_tid.py::test_turkish_simple_glosser_basic PASSED      [ 15%]
tests/test_turkish_tid.py::test_turkish_morphology_handling PASSED       [ 23%]
tests/test_turkish_tid.py::test_turkish_text_to_gloss_cli PASSED         [ 30%]
tests/test_turkish_tid.py::test_turkish_tid_without_lexicon_fails_gracefully PASSED [ 38%]
tests/test_turkish_tid.py::test_turkish_language_code_accepted PASSED    [ 46%]
tests/test_turkish_tid.py::test_turkish_sentence_structures[Merhaba-1] PASSED [ 53%]
tests/test_turkish_tid.py::test_turkish_sentence_structures[Merhaba dünya-2] PASSED [ 61%]
tests/test_turkish_tid.py::test_turkish_sentence_structures[Ben Türkçe öğreniyorum-3] PASSED [ 69%]
tests/test_turkish_tid.py::test_turkish_sentence_structures[İstanbul'da yaşıyorum-2] PASSED [ 76%]
tests/test_turkish_tid.py::test_turkish_sentence_structures[Türk İşaret Dili önemlidir-4] PASSED [ 84%]
tests/test_turkish_tid.py::test_turkish_special_characters PASSED        [ 92%]
tests/test_turkish_tid.py::test_tid_documentation_exists PASSED          [100%]

============================== 13 passed in 5.35s ==============================
```

## Test 3: Mevcut (Regresyon) Testler
```bash
pytest tests/test_e2e.py -v
```
**Sonuç:** ✅ 5/5 Geçti (Hiçbir şey bozmadık)
```
tests/test_e2e.py::test_text_to_gloss_to_pose PASSED                     [ 20%]
tests/test_e2e.py::test_fingerspelling_produces_pose PASSED              [ 40%]
tests/test_e2e.py::test_no_fingerspelling_fails_for_unknown_word PASSED  [ 60%]
tests/test_e2e.py::test_coverage_info_prints_summary PASSED              [ 80%]
tests/test_e2e.py::test_coverage_stats_saves_json PASSED                 [100%]

============================== 5 passed in 8.52s ==============================
```

## Test 4: CLI Text-to-Gloss (Türkçe)
```bash
text_to_gloss \
  --text "Merhaba dünya" \
  --glosser simple \
  --spoken-language tr \
  --signed-language tsm
```
**Exit Code:** 0 ✅
**Çıktı:**
```
Text to gloss
Input text: Merhaba dünya
Output gloss: [[GlossItem(word='merhaba', gloss='merhaba'), GlossItem(word='dünya', gloss='dünya')]]
```

## Test 5: CLI Text-to-Gloss (Türkçe Lemmatizasyon)
```bash
text_to_gloss \
  --text "Ben Türkçe öğreniyorum" \
  --glosser simple \
  --spoken-language tr \
  --signed-language tsm
```
**Exit Code:** 0 ✅
**Çıktı:**
```
Text to gloss
Input text: Ben Türkçe öğreniyorum
Output gloss: [[GlossItem(word='ben', gloss='ben'), GlossItem(word='türkçe', gloss='türkçe'), GlossItem(word='öğreniyorum', gloss='öğren')]]
```

**Not:** "öğreniyorum" → "öğren" (lemmatizasyon çalışıyor)

## Test 6: CLI Argparse Kabul (tr/tsm)
```bash
text_to_gloss_to_pose --help 2>&1 | grep -A2 "spoken-language"
```
**Sonuç:** ✅ tr ve tsm kabul ediliyor
```
--spoken-language {de,fr,it,en,tr}
--signed-language {sgg,gsg,bfi,ase,tsm}
```

## Test 7: TİD Sözlüğü Eksikliği Hatası (Fingerspelling Kapalı)
```bash
text_to_gloss_to_pose \
  --text "merhaba" \
  --glosser simple \
  --lexicon assets/dummy_lexicon \
  --spoken-language tr \
  --signed-language tsm \
  --pose /tmp/test.pose \
  --disable-fingerspelling
echo "EXIT_CODE: $?"
```
**Exit Code:** 1 ✅ (Beklenen hata)
**Stderr:**
```
Traceback (most recent call last):
  File "/home/ubuntu/.local/bin/text_to_gloss_to_pose", line 8, in <module>
    sys.exit(text_to_gloss_to_pose())
  File "/workspace/spoken_to_signed/bin.py", line 203, in text_to_gloss_to_pose
    result, coverage = _gloss_to_pose(
  File "/workspace/spoken_to_signed/bin.py", line 41, in _gloss_to_pose
    results.append(gloss_to_pose(gloss, pose_lookup, spoken_language, signed_language))
  File "/workspace/spoken_to_signed/gloss_to_pose/__init__.py", line 18, in gloss_to_pose
    results = pose_lookup.lookup_sequence(glosses, spoken_language, signed_language, source)
  File "/workspace/spoken_to_signed/gloss_to_pose/lookup/lookup.py", line 207, in lookup_sequence
    raise Exception(f"No poses found for {gloss_sequence}")
Exception: No poses found for merhaba/merhaba
EXIT_CODE: 1
```

**Analiz:** ✅ Gerçek TİD sözlük eksikliği hatası (argparse hatası DEĞİL)

## Test 8: TİD Sözlüğü Eksikliği (Fingerspelling AÇIK - Default Davranış)
```bash
text_to_gloss_to_pose \
  --text "merhaba" \
  --glosser simple \
  --lexicon assets/dummy_lexicon \
  --spoken-language tr \
  --signed-language tsm \
  --pose /tmp/merhaba.pose
echo "EXIT_CODE: $?"
```
**Exit Code:** 0 ✅ (Fingerspelling fallback çalıştı)
**Stdout:**
```
Processing 1 of 7 ...
Processing 2 of 7 ...
Processing 3 of 7 ...
Processing 4 of 7 ...
Processing 5 of 7 ...
Processing 6 of 7 ...
Processing 7 of 7 ...
Text to gloss to pose
Input text: merhaba
Output pose: /tmp/merhaba.pose
EXIT_CODE: 0
```

**Analiz:** ✅ Fingerspelling fallback kullanıldı (7 harf = m-e-r-h-a-b-a)
**Not:** Bu Türkçe parmak alfabesi değil, İngilizce/evrensel parmak alfabesi. Gerçek TİD parmak alfabesi gerekli.

## Test 9: Örnek Program
```bash
python3 examples/turkish_example.py | head -40
```
**Exit Code:** 0 ✅
**Çıktı:**
```
╔═══════════════════════════════════════════════════════════════════╗
║   Türkçe → Türk İşaret Dili (TİD) Örneği                        ║
║   Turkish → Turkish Sign Language (TİD) Example                  ║
╚═══════════════════════════════════════════════════════════════════╝

Türkçe Metin → Gloss Dönüşümü / Turkish Text → Gloss Conversion
======================================================================

Input (Türkçe): Merhaba dünya
Gloss Output:   MERHABA DÜNYA

Input (Türkçe): Ben Türkçe öğreniyorum
Gloss Output:   BEN TÜRKÇE ÖĞREN

Input (Türkçe): Küçük çocuklar İstanbul'da pizza yiyorlar
Gloss Output:   KÜÇÜK ÇOCUK İSTANBUL PIZZA YE

Input (Türkçe): Türk İşaret Dili önemli bir dildir
Gloss Output:   TÜRK İŞARET DIL ÖNEM BIR DIL

Input (Türkçe): Bugün hava çok güzel
Gloss Output:   BUGÜN HAVA ÇOK GÜZEL
```

## Özet

| Test | Komut | Exit | Durum |
|------|-------|------|-------|
| Kurulum | `pip install -e .` | 0 | ✅ Başarılı |
| Türkçe Testler | `pytest tests/test_turkish_tid.py -v` | 0 | ✅ 13/13 |
| Regresyon | `pytest tests/test_e2e.py -v` | 0 | ✅ 5/5 |
| Text-to-Gloss | `text_to_gloss --tr --tsm` | 0 | ✅ Çalışıyor |
| Lemmatizasyon | "öğreniyorum" → "öğren" | 0 | ✅ Çalışıyor |
| Argparse tr/tsm | `--help` kontrolü | 0 | ✅ Kabul ediyor |
| TİD Eksikliği (FP off) | `--disable-fingerspelling` | 1 | ✅ Doğru hata |
| Fingerspelling Fallback | Default davranış | 0 | ✅ Çalışıyor* |
| Örnek Program | `python3 examples/turkish_example.py` | 0 | ✅ Çalışıyor |

**Notlar:**
- (*) Fingerspelling fallback İngilizce/evrensel parmak alfabesi kullanıyor (TİD alfabesi değil)
- TİD sözlüğü eksikliği gerçek lookup hatasıyla bildiriliyor (argparse hatası değil)
- tr/tsm dil kodları tüm CLI komutlarında kabul ediliyor
- Mevcut diller (de, fr, it, en) etkilenmedi

## Kritik Düzeltme

**Önceki Sorun:** `text_to_gloss_to_pose` argparse erken hatasıyla tr/tsm'i reddediyordu
**Düzeltme:** Lexicon varsa bile base dilleri (tr/tsm dahil) argparse'a ekledik
**Sonuç:** Gerçek TİD sözlük eksikliği hatası lookup seviyesinde yakalanıyor (doğru davranış)

## Sınırlamalar (Açıkça Belirtildi)

1. ✅ **Text-to-Gloss ÇALIŞIYOR:** Türkçe metin işleme ve lemmatizasyon
2. ⚠️ **Gloss-to-Pose:** Gerçek TİD sözlüğü gerekiyor (dahil değil)
3. ⚠️ **Fingerspelling:** TİD parmak alfabesi yok, evrensel/İngilizce kullanılıyor
4. ⚠️ **TİD Gramer:** TİD'ye özel gramer kuralları yok (sadece lemmatizasyon)

**Sistem sahte TİD çevirisi üretmiyor, sınırlamalar net belirtiliyor.**
