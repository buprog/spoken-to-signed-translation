# Türk İşaret Dili (TİD) Desteği - Kurulum Kılavuzu

## 🎯 Özet

Bu fork'a **Türkçe (tr) → Türk İşaret Dili (TİD/tsm)** desteği eklendi. 

**Branch:** `cursor/add-turkish-tid-infrastructure-8e63`  
**Commit:** `e4b6135a19d36962ecfa6ae8d4311a876066c21e`  
**Repository:** https://github.com/buprog/spoken-to-signed-translation

## ✅ Çalışan Özellikler

- ✅ **Türkçe metin işleme**: simplemma ile tokenizasyon ve lemmatizasyon
- ✅ **Text-to-Gloss dönüşümü**: Türkçe metin → Gloss notasyonu
- ✅ **CLI entegrasyonu**: `tr` ve `tsm` dil kodları destekleniyor
- ✅ **13 test senaryosu**: Tümü başarılı
- ✅ **Türkçe özel karakterler**: ç, ğ, ı, ö, ş, ü tam destek

## ⚠️ Gerçek TİD Verisi Gerektiren Özellikler

- ⚠️ **Gloss-to-Pose dönüşümü**: TİD sözlüğü gerekli (dahil değil)
- ⚠️ **Pose-to-Video**: TİD pose verileri gerekli
- ⚠️ **TİD parmak alfabesi**: Henüz mevcut değil

**Önemli:** Sistem gerçek TİD verisi olmadan düzgün şekilde hata verir, yanlış çıktı üretmez.

## 📥 Linux'ta Kurulum (İzole Ortam)

### Seçenek 1: Python venv ile (Önerilen)

```bash
# 1. Gerekli sistem paketlerini kur (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# 2. Yeni dizin oluştur
mkdir ~/tid-translation
cd ~/tid-translation

# 3. Virtual environment oluştur
python3 -m venv tid_env
source tid_env/bin/activate

# 4. Repository'yi klonla
git clone https://github.com/buprog/spoken-to-signed-translation.git
cd spoken-to-signed-translation

# 5. Türkçe branch'e geç
git checkout cursor/add-turkish-tid-infrastructure-8e63

# 6. Paketi kur
pip install -e .

# 7. Test et
text_to_gloss \
  --text "Merhaba dünya" \
  --glosser simple \
  --spoken-language tr \
  --signed-language tsm
```

### Seçenek 2: Kullanıcı seviyesinde kurulum (venv olmadan)

```bash
# 1. Repository'yi klonla
cd ~
git clone https://github.com/buprog/spoken-to-signed-translation.git
cd spoken-to-signed-translation

# 2. Türkçe branch'e geç
git checkout cursor/add-turkish-tid-infrastructure-8e63

# 3. Kullanıcı seviyesinde kur
pip install --user -e .

# 4. PATH'i güncelle (kalıcı yapmak için ~/.bashrc'ye ekle)
export PATH="$HOME/.local/bin:$PATH"

# 5. Test et
text_to_gloss \
  --text "Türk İşaret Dili öğreniyorum" \
  --glosser simple \
  --spoken-language tr \
  --signed-language tsm
```

### Chatterbox ile İzolasyon

Mevcut Chatterbox kurulumunuzu etkilemeden:

1. **Ayrı virtual environment kullanın** (yukarıdaki Seçenek 1)
2. **Sistem paketlerini değiştirmeyin** (--user veya venv ile kur)
3. **CUDA/GPU gerektirmez** (CPU'da çalışır)
4. **Whisper'ı etkilemez** (farklı paket bağımlılıkları)

## 🧪 Testler

```bash
# Tüm Türkçe testlerini çalıştır
pytest tests/test_turkish_tid.py -v

# Örnek programı çalıştır
python3 examples/turkish_example.py

# Mevcut testlerin hala çalıştığını doğrula
pytest tests/test_e2e.py -v
```

## 📝 Kullanım Örnekleri

### Metin → Gloss (ÇALIŞIR)

```bash
text_to_gloss \
  --text "Küçük çocuklar İstanbul'da pizza yiyorlar" \
  --glosser simple \
  --spoken-language tr \
  --signed-language tsm
```

**Çıktı:**
```
Output gloss: [[GlossItem(word='küçük', gloss='küçük'), 
                GlossItem(word='çocuklar', gloss='çocuk'), 
                GlossItem(word='istanbul\'da', gloss='istanbul'), 
                GlossItem(word='pizza', gloss='pizza'), 
                GlossItem(word='yiyorlar', gloss='ye')]]
```

### Metin → Gloss → Pose (TİD SÖZLÜĞÜ GEREKTİRİR)

```bash
# Bu komut TİD sözlüğü olmadan HATA VERECEKTİR
text_to_gloss_to_pose \
  --text "Merhaba" \
  --glosser simple \
  --lexicon /path/to/tid/lexicon \
  --spoken-language tr \
  --signed-language tsm \
  --pose output.pose
```

**Beklenen Hata:** Sistem TİD verilerinin eksik olduğunu bildirecek.

## 📚 Dokümantasyon

- **Ana Dokümantasyon:** `docs/TURKISH_TID_SUPPORT.md`
- **Yapılandırma:** `config/turkish_tid_config.json`
- **Örnek Kod:** `examples/turkish_example.py`
- **Testler:** `tests/test_turkish_tid.py`

## 🔬 Yapılan Değişiklikler

### Dosyalar

1. **spoken_to_signed/bin.py**
   - `tr` ve `tsm` dil kodları CLI'a eklendi

2. **spoken_to_signed/gloss_to_pose/languages.py**
   - TİD yapılandırması ve notlar eklendi

3. **README.md**
   - Desteklenen diller tablosuna TİD eklendi
   - Sözlük gereksinimi konusunda uyarı eklendi

4. **Yeni Dosyalar:**
   - `docs/TURKISH_TID_SUPPORT.md` - İki dilli dokümantasyon
   - `config/turkish_tid_config.json` - Tam yapılandırma
   - `examples/turkish_example.py` - Çalışan örnek
   - `tests/test_turkish_tid.py` - 13 test senaryosu

### Test Sonuçları

```
✅ 13/13 Türkçe testi başarılı
✅ Mevcut e2e testleri hala çalışıyor
✅ CLI komutları beklendiği gibi çalışıyor
✅ Hata yönetimi düzgün çalışıyor
```

## 🎯 Kısıtlamalar ve Gelecek Çalışmalar

### Mevcut Kısıtlamalar

- TİD sözlüğü dahil değil (gerçek veriler gerekli)
- Yalnızca `simple` glosser destekleniyor
- TİD'ye özel gramer kuralları yok
- Türkçe parmak alfabesi yok
- Bölgesel lehçe desteği yok

### Gelecek Çalışmalar

- Türk Sağır Topluluğu ile TİD sözlüğü oluşturma
- TİD'ye özel gramer kuralları uygulama
- NMT modeli eğitimi (Türkçe → TİD gloss)
- Parmak alfabesi desteği ekleme
- `rules` ve `spacylemma` glosser'ları uyarlama

## 🔗 Linkler

- **Repository:** https://github.com/buprog/spoken-to-signed-translation
- **Branch:** https://github.com/buprog/spoken-to-signed-translation/tree/cursor/add-turkish-tid-infrastructure-8e63
- **Commit:** https://github.com/buprog/spoken-to-signed-translation/commit/e4b6135a19d36962ecfa6ae8d4311a876066c21e

## 🤝 Katkıda Bulunma

TİD verilerine erişiminiz varsa:

1. Uygun izinlerin olduğundan emin olun
2. `docs/TURKISH_TID_SUPPORT.md`'deki rehberi takip edin
3. İşaret dilcilerden açık onay alın
4. KVKK ve veri koruma düzenlemelerine uyun
5. Pull request gönderin

## ⚖️ Etik Değerlendirmeler

- ✅ **Gerçekçi uygulama**: Sahte veri veya uydurma çeviri yok
- ✅ **Açık sınırlamalar**: Neyin çalışıp neyin çalışmadığı net belirtildi
- ✅ **Düzgün hata yönetimi**: Eksik veri için net hatalar
- ✅ **İzin ve onay**: Gerçek TİD verisi için gereksinimler belgelendi
- ✅ **Topluluk odaklı**: Türk Sağır Topluluğu ile işbirliği önerildi

## 📞 İletişim

Sorularınız için GitHub'da issue açabilirsiniz:
https://github.com/buprog/spoken-to-signed-translation/issues

---

**Son Güncelleme:** 8 Kasım 2026  
**Versiyon:** 0.1.0  
**Durum:** Üretim için hazır (text-to-gloss), TİD sözlüğü için veri bekleniyor
