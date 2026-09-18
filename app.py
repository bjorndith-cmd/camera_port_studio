#!/usr/bin/env python3
"""
Camera Port Studio - Web UI
MIUI / HyperOS Camera Magisk Module Generator
Maximum camera modes support
"""

import streamlit as st
from pathlib import Path
import tempfile
import zipfile
from datetime import datetime

from generator.module_builder import build_module

st.set_page_config(
    page_title="Camera Port Studio",
    page_icon="📷",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #ff2d55, #ff9500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header { color: #888; font-size: 1rem; margin-bottom: 1.5rem; }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #ff2d55, #ff6b00);
        color: white; font-weight: 600; border: none; border-radius: 8px;
    }
    .stDownloadButton>button {
        width: 100%; background: #00c853; color: white; font-weight: 600; border-radius: 8px;
    }
    .info-box {
        background: #1e1e2e; border-left: 4px solid #ff2d55;
        padding: 1rem; border-radius: 6px; margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">📷 Camera Port Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">MIUI / HyperOS Camera → Magisk Module · Maximum modes · Xiaomi 13 Ultra (ishtar) priority</div>', unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    st.header("📦 Module Info")
    module_id = st.text_input("Module ID", value="miuicamera_ishtar_max")
    module_name = st.text_input("Display Name", value="MIUI Camera Port (Max Modes)")
    version = st.text_input("Version", value="5.3.0-max")
    version_code = st.text_input("Version Code", value="530")
    author = st.text_input("Author", value="CameraPortStudio")
    description = st.text_area(
        "Description",
        value="Ported MIUI/HyperOS Camera with maximum modes enabled: dual aperture, Leica, 8K, RAW, Night, Portrait, Director, Film and more.",
        height=90,
    )

    st.divider()
    st.header("📱 Target Device")
    device_options = {
        "Xiaomi 13 Ultra (ishtar)": ("ishtar", "Xiaomi 13 Ultra"),
        "Xiaomi 14 Ultra (aurora)": ("aurora", "Xiaomi 14 Ultra"),
        "Xiaomi 15 Pro (xuanyuan)": ("xuanyuan", "Xiaomi 15 Pro"),
        "Xiaomi MIX Fold 4 (goku)": ("goku", "Xiaomi MIX Fold 4"),
        "Xiaomi 14 Pro (shennong)": ("shennong", "Xiaomi 14 Pro"),
        "Generic / Custom": ("generic", "Generic Xiaomi"),
    }
    selected_device = st.selectbox("Device", list(device_options.keys()))
    codename, device_name = device_options[selected_device]

    if selected_device == "Generic / Custom":
        codename = st.text_input("Codename", value="ishtar")
        device_name = st.text_input("Market Name", value="Xiaomi Device")

# ========== TABS ==========
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Source APK",
    "2. Camera Modes (Max)",
    "3. System Compatibility",
    "4. Build & Download"
])

# --- Tab 1 ---
with tab1:
    st.subheader("Исходный файл камеры")
    st.markdown("""
    Загрузите **MiuiCamera.apk** (рекомендуются сборки HyperOS 2.0 Global Leica 5.3.x).  
    Без APK модуль создаётся с плейсхолдером — можно положить APK вручную позже.
    """)
    uploaded_apk = st.file_uploader("Выберите MiuiCamera.apk", type=["apk"])

    if uploaded_apk:
        size_mb = uploaded_apk.size / 1024 / 1024
        st.success(f"Загружен: **{uploaded_apk.name}** ({size_mb:.1f} MB)")
        try:
            with zipfile.ZipFile(uploaded_apk) as z:
                names = z.namelist()
                has_manifest = any("AndroidManifest.xml" in n for n in names)
                has_dex = any(n.endswith(".dex") for n in names)
                if has_manifest and has_dex:
                    st.info("✅ Похоже на валидный APK (AndroidManifest + DEX найдены)")
                else:
                    st.warning("⚠️ Файл может быть повреждён или это не APK")
        except Exception as e:
            st.warning(f"Не удалось проверить APK: {e}")

# --- Tab 2: Maximum Modes ---
with tab2:
    st.subheader("Режимы и функции камеры")
    st.markdown("Включите столько режимов, сколько нужно. Они записываются в `device_features/*.xml`.")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("✅ Включить ВСЁ", use_container_width=True):
            for k in ["dual", "leica", "street", "raw", "portrait", "pro", "8k", "4k120", "hfr",
                      "dolby", "log", "director", "cinematic", "night", "moon", "astro", "macro",
                      "doc", "clone", "long_exp", "film"]:
                st.session_state[f"mode_{k}"] = True
            st.rerun()
    with col_b:
        if st.button("⭐ Рекомендуемый набор", use_container_width=True):
            rec = {
                "dual": True, "leica": True, "street": True, "raw": True, "portrait": True,
                "pro": True, "8k": True, "4k120": True, "hfr": True, "dolby": True, "log": True,
                "director": True, "cinematic": True, "night": True, "moon": True, "astro": False,
                "macro": True, "doc": True, "clone": False, "long_exp": True, "film": True,
            }
            for k, v in rec.items():
                st.session_state[f"mode_{k}"] = v
            st.rerun()
    with col_c:
        if st.button("❌ Выключить всё", use_container_width=True):
            for k in ["dual", "leica", "street", "raw", "portrait", "pro", "8k", "4k120", "hfr",
                      "dolby", "log", "director", "cinematic", "night", "moon", "astro", "macro",
                      "doc", "clone", "long_exp", "film"]:
                st.session_state[f"mode_{k}"] = False
            st.rerun()

    # Init defaults once
    if "modes_ready" not in st.session_state:
        rec = {
            "dual": True, "leica": True, "street": True, "raw": True, "portrait": True,
            "pro": True, "8k": True, "4k120": True, "hfr": True, "dolby": True, "log": True,
            "director": True, "cinematic": True, "night": True, "moon": True, "astro": False,
            "macro": True, "doc": True, "clone": False, "long_exp": True, "film": True,
        }
        for k, v in rec.items():
            if f"mode_{k}" not in st.session_state:
                st.session_state[f"mode_{k}"] = v
        st.session_state["modes_ready"] = True

    def mode_cb(key, label, help_text=""):
        return st.checkbox(label, value=st.session_state.get(f"mode_{key}", True),
                           key=f"cb_{key}", help=help_text)

    with st.expander("🔧 Аппаратные функции", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            support_dual = mode_cb("dual", "Диафрагма f/1.9 ↔ f/4.0", "Только ishtar / устройства с механической диафрагмой")
        with c2:
            support_leica = mode_cb("leica", "Leica Authentic / Vibrant / Watermark")
        with c3:
            support_street = mode_cb("street", "Уличный режим + Fastshot")

    with st.expander("📸 Фото, Pro и RAW", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            support_raw = mode_cb("raw", "Ultra RAW 14-bit / DNG")
            support_portrait = mode_cb("portrait", "Портрет + Bokeh + Master Portrait")
        with c2:
            support_pro = mode_cb("pro", "Pro: Focus Peaking / Zebra / Histogram")
            support_long_exp = mode_cb("long_exp", "Длинная выдержка + Light Painting")
        with c3:
            support_film = mode_cb("film", "Film Mode + Vintage фильтры")
            support_macro = mode_cb("macro", "Макро + Super Macro + Tele Macro")

    with st.expander("🎬 Видео", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            support_8k = mode_cb("8k", "8K 24fps на всех сенсорах")
            support_4k120 = mode_cb("4k120", "4K 120fps")
        with c2:
            support_hfr = mode_cb("hfr", "1080p 240fps (HFR)")
            support_dolby = mode_cb("dolby", "Dolby Vision HDR")
        with c3:
            support_log = mode_cb("log", "LOG-профиль")
            support_director = mode_cb("director", "Director Mode")
            support_cinematic = mode_cb("cinematic", "Cinematic Mode")

    with st.expander("🌙 Ночь, AI и специальные режимы", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            support_night = mode_cb("night", "Super Night / Extreme Night")
            support_moon = mode_cb("moon", "Режим Луны")
        with c2:
            support_astro = mode_cb("astro", "Астро-режим (экспериментально)")
            support_doc = mode_cb("doc", "Документы + ID Card")
        with c3:
            support_clone = mode_cb("clone", "Clone Mode (экспериментально)")

    st.markdown("""
    <div class="info-box">
    <b>Совет:</b> Большинство флагов работают на ishtar при правильном APK. 
    Некоторые (Astro, Clone) могут не появиться в UI, если сама сборка камеры их не поддерживает.
    Флаги только <i>разблокируют</i> режимы, которые уже есть в APK.
    </div>
    """, unsafe_allow_html=True)

# --- Tab 3 ---
with tab3:
    st.subheader("Совместимость и системные патчи")
    target_rom = st.radio(
        "Целевая прошивка",
        ["HyperOS Official", "Xiaomi.eu / Моды", "AOSP / Custom ROM"],
        horizontal=True,
    )
    rom_map = {
        "HyperOS Official": "HyperOS",
        "Xiaomi.eu / Моды": "Xiaomi.eu",
        "AOSP / Custom ROM": "AOSP",
    }
    target_rom_key = rom_map[target_rom]

    c1, c2 = st.columns(2)
    with c1:
        hyperos3 = st.checkbox("HyperOS 3.0 / Android 16 props", value=True)
        sdk_bypass = st.checkbox("Bypass SDK restriction (API 35/36)", value=True)
        enable_spoof = st.checkbox("Device Spoof Engine", value=False)
        if enable_spoof:
            spoof_options = ["ishtar", "aurora", "xuanyuan", "goku", "shennong", "No Spoofing"]
            spoof_device = st.selectbox("Spoof as", spoof_options, index=0)
            if spoof_device == "No Spoofing":
                enable_spoof = False
                spoof_device = codename
        else:
            spoof_device = codename
    with c2:
        thermal_fix = st.checkbox("Смягчение thermal throttling (для 8K)", value=True)
        aux_whitelist = st.checkbox("AUX cameras whitelist (AOSP fix)", value=True)
        disable_stock = st.checkbox("Отключить стоковую камеру (pm disable)", value=False)

    st.markdown("""
    <div class="info-box">
    <b>Чёрный экран / зависание кнопок:</b><br>
    • Поставьте Spoof на «No Spoofing» или точный codename вашего устройства<br>
    • Очистите данные приложения Камера<br>
    • Используйте APK, совместимый с вашим HAL
    </div>
    """, unsafe_allow_html=True)

# --- Tab 4 ---
with tab4:
    st.subheader("Сборка Magisk-модуля")

    mode_map = {
        "dual": "Dual Aperture", "leica": "Leica", "street": "Street/Fastshot",
        "raw": "RAW 14-bit", "portrait": "Portrait", "pro": "Pro tools",
        "8k": "8K", "4k120": "4K120", "hfr": "HFR 240", "dolby": "Dolby Vision",
        "log": "LOG", "director": "Director", "cinematic": "Cinematic",
        "night": "Night", "moon": "Moon", "astro": "Astro", "macro": "Macro",
        "doc": "Document", "clone": "Clone", "long_exp": "Long Exposure", "film": "Film"
    }
    enabled_modes = []
    for k, label in mode_map.items():
        val = st.session_state.get(f"cb_{k}", st.session_state.get(f"mode_{k}", False))
        if val:
            enabled_modes.append(label)

    st.write(f"**Включено режимов:** {len(enabled_modes)}")
    if enabled_modes:
        st.caption(", ".join(enabled_modes))

    if st.button("🚀 Собрать Magisk Module", type="primary"):
        with st.spinner("Генерация модуля с выбранным набором режимов..."):
            apk_path = None
            if uploaded_apk is not None:
                tmp_apk = Path(tempfile.gettempdir()) / uploaded_apk.name
                with open(tmp_apk, "wb") as f:
                    f.write(uploaded_apk.getbuffer())
                apk_path = str(tmp_apk)

            out_name = f"MiuiCamera_{codename}_{version}_{datetime.now().strftime('%Y%m%d_%H%M')}.zip"
            out_path = Path(tempfile.gettempdir()) / out_name

            def get_mode(key, default=True):
                return st.session_state.get(f"cb_{key}", st.session_state.get(f"mode_{key}", default))

            try:
                result = build_module(
                    apk_path=apk_path,
                    output_path=str(out_path),
                    module_id=module_id,
                    module_name=module_name,
                    version=version,
                    version_code=version_code,
                    author=author,
                    description=description,
                    codename=codename,
                    device_name=device_name,
                    target_rom=target_rom_key,
                    support_dual_aperture=get_mode("dual"),
                    support_leica=get_mode("leica"),
                    support_street=get_mode("street"),
                    support_8k=get_mode("8k"),
                    support_raw=get_mode("raw"),
                    support_portrait=get_mode("portrait"),
                    support_pro=get_mode("pro"),
                    support_4k120=get_mode("4k120"),
                    support_hfr=get_mode("hfr"),
                    support_dolby=get_mode("dolby"),
                    support_log=get_mode("log"),
                    support_director=get_mode("director"),
                    support_cinematic=get_mode("cinematic"),
                    support_night=get_mode("night"),
                    support_moon=get_mode("moon"),
                    support_astro=get_mode("astro"),
                    support_macro=get_mode("macro"),
                    support_doc=get_mode("doc"),
                    support_clone=get_mode("clone"),
                    support_long_exp=get_mode("long_exp"),
                    support_film=get_mode("film"),
                    enable_spoof=enable_spoof,
                    spoof_device=spoof_device,
                    disable_stock_camera=disable_stock,
                    thermal_fix=thermal_fix,
                    aux_whitelist=aux_whitelist,
                    sdk_bypass=sdk_bypass,
                    hyperos3=hyperos3,
                )

                st.success("✅ Модуль успешно собран!")
                st.markdown(f"**Файл:** `{out_name}`")

                with open(result, "rb") as f:
                    st.download_button(
                        label="⬇️ Скачать Magisk ZIP",
                        data=f,
                        file_name=out_name,
                        mime="application/zip",
                    )

                st.info("""
                **Установка:**
                1. Скопируйте ZIP на телефон  
                2. Magisk / KernelSU / APatch → Modules → Install from storage  
                3. Перезагрузка  
                4. При чёрном экране — очистите данные Камеры и попробуйте native spoof
                """)
            except Exception as e:
                st.error(f"Ошибка сборки: {e}")
                st.exception(e)

st.divider()
st.caption("Camera Port Studio · Локальный генератор · Не связан с Xiaomi · Используйте на свой риск")
