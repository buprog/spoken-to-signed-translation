# Turkish (Türkçe) ve Türk İşaret Dili (TİD) Desteği / Turkish and Turkish Sign Language Support

## English

### Overview

This document describes the Turkish language infrastructure added to the spoken-to-signed-translation pipeline for Turkish Sign Language (Türk İşaret Dili - TİD).

**Language Codes:**
- Spoken Language: `tr` (Turkish / Türkçe)
- Signed Language: `tsm` (Turkish Sign Language / Türk İşaret Dili)

### Current Implementation Status

#### ✅ Working Now (Text Processing Only)

1. **Turkish Text Processing**: Turkish language support via `simplemma` library for tokenization and lemmatization
2. **Pipeline Integration**: Turkish (`tr`) is accepted as a spoken language in CLI and code
3. **Sign Language Configuration**: Turkish Sign Language (`tsm`) is configured in the language system
4. **Text-to-Gloss Pipeline**: Turkish text can be processed through the `simple` glosser (lemmatization only, not TİD grammar)
5. **Testing Infrastructure**: Turkish-specific test cases for text processing (13 tests)
6. **Error Handling**: Clear errors when TİD lexicon data is missing

#### ⚠️ Requires Real TİD Data (Not Yet Available)

The following components **require authentic Turkish Sign Language lexicon data** to function:

1. **TİD Lexicon**: No pose database exists for Turkish signs in this repository
   - Real TİD pose recordings are needed
   - Signs must be captured from native TİD signers
   - Linguistic validation by TİD experts is required

2. **Gloss-to-Pose Conversion**: Cannot convert glosses to TİD poses without lexicon
   - The system will fail gracefully with a clear error message
   - Fingerspelling fallback requires Turkish fingerspelling alphabet poses

3. **Advanced Glossers**: The `rules`, `nmt`, and `spacylemma` glossers may need TİD-specific linguistic rules

### How to Use

#### Text-to-Gloss (Works Now)

```bash
text_to_gloss \
  --text "Merhaba dünya" \
  --glosser "simple" \
  --spoken-language "tr" \
  --signed-language "tsm"
```

This will output Turkish lemmas as glosses.

#### Text-to-Gloss-to-Pose (Requires TİD Lexicon)

```bash
# This will FAIL without a real TİD lexicon
text_to_gloss_to_pose \
  --text "Merhaba dünya" \
  --glosser "simple" \
  --lexicon "path/to/tid/lexicon" \
  --spoken-language "tr" \
  --signed-language "tsm" \
  --pose "output.pose"
```

**Expected Error**: The system will report that TİD pose data is not available in the lexicon.

### Creating a TİD Lexicon

To add real TİD support, you need:

1. **Pose Files**: Record TİD signs in pose format (`.pose` files)
   - Use pose-format library: https://github.com/sign-language-processing/pose-format
   - Record from native TİD signers
   - Ensure proper licensing and consent

2. **Index CSV**: Create an `index.csv` file with the structure:
   ```csv
   path,spoken_language,signed_language,start,end,segment_start,segment_end,words,glosses,priority
   tsm/merhaba.pose,tr,tsm,0,0,500,1500,merhaba,MERHABA,0
   tsm/dünya.pose,tr,tsm,0,0,600,1800,dünya,DÜNYA,0
   ```

3. **Directory Structure**:
   ```
   tid_lexicon/
   ├── index.csv
   └── tsm/
       ├── merhaba.pose
       ├── dünya.pose
       └── ...
   ```

### Linguistic Considerations

1. **Turkish Morphology**: Turkish is an agglutinative language with rich morphology
   - The `simple` glosser uses lemmatization to handle this
   - More sophisticated glossers may be needed for better TİD grammar

2. **TİD Grammar**: Turkish Sign Language has its own grammatical structure
   - Word order may differ from spoken Turkish
   - Classifier constructions and spatial grammar need specialized handling
   - Future work: implement TİD-specific grammatical rules

3. **Regional Variation**: TİD may have regional dialects
   - Lexicon should document regional variants if included

### Testing

Run Turkish-specific tests:

```bash
pytest tests/test_turkish_tid.py -v
```

These tests verify:
- Turkish text tokenization and lemmatization
- Pipeline integration
- Error handling when TİD data is missing

### Resources and References

**TİD Resources:**
- [Turkish Sign Language Research](https://www.bogazici.edu.tr/tr-TR/Index)
- [İşaret Dili](https://isaret.org.tr/)
- [ELAN Corpus of TİD](https://github.com/sign-language-processing/signbank-plus) - if available

**Technical Resources:**
- [Pose Format Library](https://github.com/sign-language-processing/pose-format)
- [Sign Language Datasets](https://github.com/sign-language-processing/datasets)

### Contributing TİD Data

If you have access to TİD data:

1. Ensure proper licensing and permissions
2. Follow the lexicon format described above
3. Include metadata about signers and regional variants
4. Validate glosses with TİD experts
5. Submit via pull request with documentation

### License Considerations

**Important**: Any TİD lexicon data added must:
- Have explicit permission from signers
- Include proper attribution
- Comply with data protection regulations
- Respect intellectual property rights

Do not add pose data without proper authorization.

---

## Türkçe

### Genel Bakış

Bu belge, Türk İşaret Dili (TİD) için konuşulan dilden işaret diline çeviri hattına eklenen Türkçe dil altyapısını açıklamaktadır.

**Dil Kodları:**
- Konuşulan Dil: `tr` (Türkçe)
- İşaret Dili: `tsm` (Türk İşaret Dili)

### Mevcut Uygulama Durumu

#### ✅ Şu An Çalışan (Sadece Metin İşleme)

1. **Türkçe Metin İşleme**: `simplemma` kütüphanesi ile Türkçe dil desteği (tokenizasyon ve lemmatizasyon)
2. **Hattı Entegrasyonu**: Türkçe (`tr`) CLI ve kodda konuşulan dil olarak kabul ediliyor
3. **İşaret Dili Yapılandırması**: Türk İşaret Dili (`tsm`) dil sisteminde yapılandırıldı
4. **Metin-Gloss Hattı**: Türkçe metin `simple` glosser ile işlenebilir (sadece lemmatizasyon, TİD grameri değil)
5. **Test Altyapısı**: Türkçe'ye özel metin işleme test senaryoları (13 test)
6. **Hata Yönetimi**: TİD sözlük verisi eksik olduğunda net hatalar

#### ⚠️ Gerçek TİD Verisi Gerektirir (Henüz Mevcut Değil)

Aşağıdaki bileşenler **gerçek Türk İşaret Dili sözlük verisi** gerektirir:

1. **TİD Sözlüğü**: Bu depoda Türkçe işaretler için pose veritabanı mevcut değil
   - Gerçek TİD pose kayıtları gerekli
   - İşaretler anadili TİD olan işaret dilcilerden kaydedilmeli
   - TİD uzmanları tarafından dilbilimsel doğrulama gerekli

2. **Gloss-Pose Dönüşümü**: Sözlük olmadan gloss'ları TİD pose'larına dönüştüremez
   - Sistem net bir hata mesajı ile düzgün şekilde başarısız olacak
   - Parmak alfabesi geri dönüşü için Türkçe parmak alfabesi pose'ları gerekli

3. **Gelişmiş Glosser'lar**: `rules`, `nmt`, ve `spacylemma` glosser'lar TİD'ye özel dilbilimsel kurallar gerektirebilir

### Nasıl Kullanılır

#### Metin-Gloss (Şimdi Çalışıyor)

```bash
text_to_gloss \
  --text "Merhaba dünya" \
  --glosser "simple" \
  --spoken-language "tr" \
  --signed-language "tsm"
```

Bu, Türkçe lemmaları gloss olarak çıktı verecektir.

#### Metin-Gloss-Pose (TİD Sözlüğü Gerektirir)

```bash
# Gerçek TİD sözlüğü olmadan BAŞARISIZ olacak
text_to_gloss_to_pose \
  --text "Merhaba dünya" \
  --glosser "simple" \
  --lexicon "yol/tid/sözlüğü" \
  --spoken-language "tr" \
  --signed-language "tsm" \
  --pose "cikti.pose"
```

**Beklenen Hata**: Sistem, TİD pose verisinin sözlükte bulunmadığını bildirecek.

### TİD Sözlüğü Oluşturma

Gerçek TİD desteği eklemek için gerekenler:

1. **Pose Dosyaları**: TİD işaretlerini pose formatında (`.pose` dosyaları) kaydedin
   - pose-format kütüphanesini kullanın: https://github.com/sign-language-processing/pose-format
   - Anadili TİD olan işaret dilcilerden kayıt yapın
   - Uygun lisans ve izin alın

2. **Index CSV**: Aşağıdaki yapıda bir `index.csv` dosyası oluşturun:
   ```csv
   path,spoken_language,signed_language,start,end,segment_start,segment_end,words,glosses,priority
   tsm/merhaba.pose,tr,tsm,0,0,500,1500,merhaba,MERHABA,0
   tsm/dünya.pose,tr,tsm,0,0,600,1800,dünya,DÜNYA,0
   ```

3. **Dizin Yapısı**:
   ```
   tid_lexicon/
   ├── index.csv
   └── tsm/
       ├── merhaba.pose
       ├── dünya.pose
       └── ...
   ```

### Dilbilimsel Değerlendirmeler

1. **Türkçe Morfoloji**: Türkçe, zengin morfolojiye sahip sondan eklemeli bir dildir
   - `simple` glosser bunu ele almak için lemmatizasyon kullanır
   - Daha iyi TİD grameri için daha sofistike glosser'lar gerekebilir

2. **TİD Grameri**: Türk İşaret Dili'nin kendi gramer yapısı vardır
   - Sözcük dizilişi konuşulan Türkçe'den farklı olabilir
   - Sınıflandırıcı yapıları ve uzamsal gramer özel işleme gerektirir
   - Gelecek çalışma: TİD'ye özel gramer kuralları uygulama

3. **Bölgesel Çeşitlilik**: TİD bölgesel lehçelere sahip olabilir
   - Sözlük, dahil edilirse bölgesel varyantları belgelemelidir

### Test Etme

Türkçe'ye özel testleri çalıştırın:

```bash
pytest tests/test_turkish_tid.py -v
```

Bu testler şunları doğrular:
- Türkçe metin tokenizasyonu ve lemmatizasyonu
- Hattı entegrasyonu
- TİD verisi eksik olduğunda hata yönetimi

### Kaynaklar ve Referanslar

**TİD Kaynakları:**
- [Türk İşaret Dili Araştırmaları](https://www.bogazici.edu.tr/tr-TR/Index)
- [İşaret Dili](https://isaret.org.tr/)
- [TİD ELAN Derlemi](https://github.com/sign-language-processing/signbank-plus) - varsa

**Teknik Kaynaklar:**
- [Pose Format Kütüphanesi](https://github.com/sign-language-processing/pose-format)
- [İşaret Dili Veri Setleri](https://github.com/sign-language-processing/datasets)

### TİD Verisi Katkıda Bulunma

Eğer TİD verisine erişiminiz varsa:

1. Uygun lisans ve izinlerin olduğundan emin olun
2. Yukarıda açıklanan sözlük formatını izleyin
3. İşaret dilciler ve bölgesel varyantlar hakkında metadata ekleyin
4. Gloss'ları TİD uzmanları ile doğrulayın
5. Dokümantasyon ile birlikte pull request gönderin

### Lisans Değerlendirmeleri

**Önemli**: Eklenen herhangi bir TİD sözlük verisi:
- İşaret dilcilerden açık izin içermeli
- Uygun atıf içermeli
- Veri koruma düzenlemelerine uymalı
- Fikri mülkiyet haklarına saygı göstermeli

Uygun yetki olmadan pose verisi eklemeyin.
