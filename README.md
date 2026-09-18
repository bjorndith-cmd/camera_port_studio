# 📷 Camera Port Studio

**Локальный генератор Magisk-модулей** для портирования MIUI / HyperOS Camera.  
Поддержка **максимального количества режимов** камеры перед сборкой.

Вдохновлён проектами *Magisk Module Modifier* и *MIUI & HyperOS Camera Porting Studio for Xiaomi 13 Ultra*.

---

## Возможности

### Режимы камеры (включаются галочками перед сборкой)
- Dual Aperture f/1.9 ↔ f/4.0 (ishtar)
- Leica Authentic / Vibrant / Watermark / Mono
- Street Mode + Fastshot
- Ultra RAW 14-bit / DNG
- Portrait + Bokeh + Master Portrait Lens
- Pro: Focus Peaking, Zebra, Histogram
- 8K 24fps на всех сенсорах
- 4K 120fps, 1080p 240fps
- Dolby Vision + LOG
- Director Mode + Cinematic Mode
- Super Night / Extreme Night
- Moon Mode, Astro (эксп.), Macro / Super Macro
- Document / ID Card, Clone (эксп.)
- Long Exposure + Light Painting
- Film Mode + Vintage фильтры

Кнопки **«Включить ВСЁ»** / **«Рекомендуемый набор»** / **«Выключить всё»**.

### Система
- Генерация полной структуры Magisk-модуля
- `device_features/{codename}.xml` с максимальным набором флагов (~100)
- Device Spoof Engine
- HyperOS 3.0 / Android 16 props + SDK bypass
- Thermal soft profile, AUX whitelist, SELinux rules
- Поддержка ishtar, aurora, xuanyuan, goku, shennong и generic

### Интерфейсы
- **Веб-UI** (Streamlit) — основной
- **CLI** — для автоматизации
- Готовые `.bat` для Windows + инструкция по сборке EXE

---

## Быстрый старт (Windows)

1. Распакуйте архив
2. Дважды кликните **`run.bat`**
3. Откроется браузер → загрузите APK → включите нужные режимы → «Собрать»

---

## CLI

```bash
# Активировать venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/macOS

# Максимум режимов
python -m generator.cli --apk MiuiCamera.apk --device ishtar --all-modes -o port_max.zip

# Выборочно
python -m generator.cli --apk MiuiCamera.apk --device ishtar --no-astro --no-clone -o port.zip

# Без APK (плейсхолдер)
python -m generator.cli --device ishtar --all-modes
```

---

## Сборка EXE

Запустите `build_exe.bat` (требует Python + pip).  
Или вручную:

```bash
pip install -r requirements.txt pyinstaller
pyinstaller --noconfirm --onefile --console --name CameraPortStudio --add-data "generator;generator" --collect-all streamlit app.py
```

---

## Онлайн

Можно бесплатно задеплоить на Streamlit Community Cloud или Hugging Face Spaces (тип Streamlit).

---

## Важно

- Это **не** binary-патчер APK. Инструмент упаковывает ваш APK + генерирует XML и скрипты, которые *разблокируют* режимы, уже присутствующие в сборке камеры.
- Некоторые флаги (Astro, Clone) могут не отобразиться в UI, если конкретная версия APK их не содержит.
- При чёрном экране: native spoof / очистка данных Камеры / правильный APK под ваш HAL.

---

## Структура

```
camera_port_studio/
├── app.py                  # Streamlit UI
├── run.bat / build_exe.bat
├── requirements.txt
├── README.md
└── generator/
    ├── module_builder.py
    ├── cli.py
    └── templates/
        ├── ishtar.xml      # Максимум флагов
        ├── module.prop
        ├── customize.sh
        ├── post-fs-data.sh
        ├── service.sh
        ├── sepolicy.rule
        └── privapp-permissions-miuicamera.xml
```

MIT · Не связан с Xiaomi / Leica · Используйте на свой риск.
