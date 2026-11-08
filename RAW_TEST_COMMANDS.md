# Ham Test Komutları - tsm Fingerspelling Düzeltmesi

## Sorun: Sahte TİD Çıktısı

tsm (TİD) için İngilizce/evrensel parmak alfabesi kullanarak "başarılı" pose oluşturuluyordu.
Bu SAHTE TİD çıktısı - gerçek TİD parmak alfabesi doğrulanmadan kullanılamaz.

## Düzeltme

tsm için fingerspelling backup devre dışı bırakıldı. Artık TİD sözlüğü yoksa NET HATA veriyor.

---

## Test 1: tsm VARSAYILAN (flag yok) - Artık BAŞARISIZ

```bash
$ cd /workspace
$ export PATH="$HOME/.local/bin:$PATH"
$ rm -f /tmp/test_tsm_new.pose

$ text_to_gloss_to_pose \
  --text "xyz" \
  --glosser simple \
  --lexicon assets/dummy_lexicon \
  --spoken-language tr \
  --signed-language tsm \
  --pose /tmp/test_tsm_new.pose

Traceback (most recent call last):
  File "/home/ubuntu/.local/bin/text_to_gloss_to_pose", line 8, in <module>
    sys.exit(text_to_gloss_to_pose())
  File "/workspace/spoken_to_signed/bin.py", line 212, in text_to_gloss_to_pose
    result, coverage = _gloss_to_pose(
  File "/workspace/spoken_to_signed/bin.py", line 50, in _gloss_to_pose
    results.append(gloss_to_pose(gloss, pose_lookup, spoken_language, signed_language))
  File "/workspace/spoken_to_signed/gloss_to_pose/__init__.py", line 18, in gloss_to_pose
    results = pose_lookup.lookup_sequence(glosses, spoken_language, signed_language, source)
  File "/workspace/spoken_to_signed/gloss_to_pose/lookup/lookup.py", line 207, in lookup_sequence
    raise Exception(f"No poses found for {gloss_sequence}")
Exception: No poses found for xyz/xyz

$ echo "EXIT: $?"
EXIT: 1

$ ls -lh /tmp/test_tsm_new.pose
ls: cannot access '/tmp/test_tsm_new.pose': No such file or directory
```

**Sonuç:**
- ✅ EXIT 1 (hata)
- ✅ Pose dosyası oluşmadı
- ✅ Net hata mesajı: "No poses found"
- ✅ Sahte TİD çıktısı YOK

---

## Test 2: tsm --disable-fingerspelling - BAŞARISIZ (beklenen)

```bash
$ rm -f /tmp/test_tsm_disabled.pose

$ text_to_gloss_to_pose \
  --text "xyz" \
  --glosser simple \
  --lexicon assets/dummy_lexicon \
  --spoken-language tr \
  --signed-language tsm \
  --pose /tmp/test_tsm_disabled.pose \
  --disable-fingerspelling

Traceback (most recent call last):
  File "/home/ubuntu/.local/bin/text_to_gloss_to_pose", line 8, in <module>
    sys.exit(text_to_gloss_to_pose())
  File "/workspace/spoken_to_signed/bin.py", line 212, in text_to_gloss_to_pose
    result, coverage = _gloss_to_pose(
  File "/workspace/spoken_to_signed/bin.py", line 50, in _gloss_to_pose
    results.append(gloss_to_pose(gloss, pose_lookup, spoken_language, signed_language))
  File "/workspace/spoken_to_signed/gloss_to_pose/__init__.py", line 18, in gloss_to_pose
    results = pose_lookup.lookup_sequence(glosses, spoken_language, signed_language, source)
  File "/workspace/spoken_to_signed/gloss_to_pose/lookup/lookup.py", line 207, in lookup_sequence
    raise Exception(f"No poses found for {gloss_sequence}")
Exception: No poses found for xyz/xyz

$ echo "EXIT: $?"
EXIT: 1

$ ls -lh /tmp/test_tsm_disabled.pose
ls: cannot access '/tmp/test_tsm_disabled.pose': No such file or directory
```

**Sonuç:**
- ✅ EXIT 1 (hata)
- ✅ Pose dosyası oluşmadı
- ✅ Net hata mesajı
- ✅ Sahte TİD çıktısı YOK

---

## Test 3: de->sgg VARSAYILAN - BAŞARILI (fingerspelling çalışıyor)

```bash
$ rm -f /tmp/test_de_new.pose

$ text_to_gloss_to_pose \
  --text "xyz" \
  --glosser simple \
  --lexicon assets/dummy_lexicon \
  --spoken-language de \
  --signed-language sgg \
  --pose /tmp/test_de_new.pose

Trimming poses...
Smooth concatenating poses...
Scaling pose...
Text to gloss to pose
Output pose: /tmp/test_de_new.pose

$ echo "EXIT: $?"
EXIT: 0

$ ls -lh /tmp/test_de_new.pose
-rw-r--r-- 1 ubuntu ubuntu 70K Nov  8 19:57 /tmp/test_de_new.pose
```

**Sonuç:**
- ✅ EXIT 0 (başarılı)
- ✅ Pose dosyası oluştu
- ✅ Fingerspelling fallback çalıştı (xyz için)
- ✅ Mevcut diller etkilenmedi

---

## Test 4: Python API Test - tsm Fingerspelling Kapalı

```python
$ python3 << 'EOF'
from spoken_to_signed.gloss_to_pose.lookup.fingerspelling_lookup import FingerspellingPoseLookup

f = FingerspellingPoseLookup()

# tr->tsm var mı?
print("tr->tsm exists:", 'tr' in f.words_index and 'tsm' in f.words_index.get('tr', {}))

# Ama bin.py'de devre dışı
print("\nbin.py'de tsm için fingerspelling backup=None (devre dışı)")
EOF

tr->tsm exists: True

bin.py'de tsm için fingerspelling backup=None (devre dışı)
```

**Açıklama:**
- tr->tsm fingerspelling verileri package'da var (indirilen veriler)
- AMA bin.py'de tsm için fingerspelling backup None yapıldı
- Sebep: Veri kaynağı/doğruluğu belirsiz (gerçek TİD alfabesi mi değil mi bilinmiyor)
- Sonuç: Sahte TİD çıktısı üretilmiyor

---

## Test 5: Tüm Testler

```bash
$ pytest tests/test_turkish_tid.py tests/test_e2e.py -v

============================= test session starts ==============================
tests/test_turkish_tid.py::test_turkish_tokenization_and_lemmatization PASSED [  5%]
tests/test_turkish_tid.py::test_turkish_simple_glosser_basic PASSED      [ 11%]
tests/test_turkish_tid.py::test_turkish_morphology_handling PASSED       [ 16%]
tests/test_turkish_tid.py::test_turkish_text_to_gloss_cli PASSED         [ 22%]
tests/test_turkish_tid.py::test_turkish_tid_without_lexicon_fails_gracefully PASSED [ 27%]
tests/test_turkish_tid.py::test_turkish_language_code_accepted PASSED    [ 33%]
tests/test_turkish_tid.py::test_turkish_sentence_structures[Merhaba-1] PASSED [ 38%]
tests/test_turkish_tid.py::test_turkish_sentence_structures[Merhaba dünya-2] PASSED [ 44%]
tests/test_turkish_tid.py::test_turkish_sentence_structures[Ben Türkçe öğreniyorum-3] PASSED [ 50%]
tests/test_turkish_tid.py::test_turkish_sentence_structures[İstanbul'da yaşıyorum-2] PASSED [ 55%]
tests/test_turkish_tid.py::test_turkish_sentence_structures[Türk İşaret Dili önemlidir-4] PASSED [ 61%]
tests/test_turkish_tid.py::test_turkish_special_characters PASSED        [ 66%]
tests/test_turkish_tid.py::test_tid_documentation_exists PASSED          [ 72%]
tests/test_e2e.py::test_text_to_gloss_to_pose PASSED                     [ 77%]
tests/test_e2e.py::test_fingerspelling_produces_pose PASSED              [ 83%]
tests/test_e2e.py::test_no_fingerspelling_fails_for_unknown_word PASSED  [ 88%]
tests/test_e2e.py::test_coverage_info_prints_summary PASSED              [ 94%]
tests/test_e2e.py::test_coverage_stats_saves_json PASSED                 [100%]

============================== 18 passed in 12.59s ==============================
```

**Sonuç:**
- ✅ 13/13 Türkçe testleri geçti
- ✅ 5/5 Regresyon testleri geçti (mevcut diller etkilenmedi)
- ✅ Toplam 18/18 başarılı

---

## Özet

| Test | Komut | Exit | Pose Oluştu? | Durum |
|------|-------|------|--------------|-------|
| tsm varsayılan | `--tr --tsm` (flag yok) | 1 | ❌ | ✅ Doğru (sahte TİD yok) |
| tsm --disable | `--tr --tsm --disable-fingerspelling` | 1 | ❌ | ✅ Doğru |
| de->sgg varsayılan | `--de --sgg` | 0 | ✅ | ✅ Doğru (fingerspelling çalışıyor) |
| Tüm testler | `pytest` | - | - | ✅ 18/18 geçti |

**Kritik Düzeltme:**
- tsm için fingerspelling backup artık None
- TİD yoksa İngilizce alfabesiyle sahte çıktı üretmiyor
- Açık ve net hata veriyor: "No poses found"
- Pose dosyası oluşmuyor
- Mevcut dillerin fingerspelling davranışı korundu

**Dürüstlük:**
- ✅ Sahte TİD çıktısı YOK
- ✅ Başka dil silent fallback YOK
- ✅ TİD verisi yoksa NET HATA
- ✅ Pose/video çıktısı oluşmuyor
