#!/usr/bin/env python3
"""
Camera Port Studio - Magisk Module Builder
Generates Magisk modules for MIUI/HyperOS Camera ports.
Supports maximum camera modes and multiple devices.
"""

import os
import shutil
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any


TEMPLATES_DIR = Path(__file__).parent / "templates"


class ModuleBuilder:
    def __init__(self):
        self.config: Dict[str, Any] = {}

    def set_config(self, **kwargs):
        self.config.update(kwargs)

    def _render(self, template_name: str, **extra) -> str:
        path = TEMPLATES_DIR / template_name
        text = path.read_text(encoding="utf-8")
        data = {**self.config, **extra}
        for key, value in data.items():
            placeholder = "{{" + key + "}}"
            text = text.replace(placeholder, str(value))
        return text

    def _bool_str(self, val: bool) -> str:
        return "true" if val else "false"

    def _get_bool(self, key: str, default: bool = True) -> bool:
        return bool(self.config.get(key, default))

    def build(self, apk_path: Optional[str] = None, output_path: str = "MiuiCamera_Port.zip") -> str:
        """Build the Magisk module ZIP. Returns path to the created ZIP."""
        cfg = self.config

        # Module metadata
        module_id = cfg.get("module_id", "miuicamera_port")
        module_name = cfg.get("module_name", "MIUI Camera Port")
        version = cfg.get("version", "1.0.0")
        version_code = cfg.get("version_code", "100")
        author = cfg.get("author", "CameraPortStudio")
        description = cfg.get("description", "Ported MIUI/HyperOS Camera with maximum modes")
        codename = cfg.get("codename", "ishtar")
        device_name = cfg.get("device_name", "Xiaomi 13 Ultra")
        target_rom = cfg.get("target_rom", "HyperOS")

        # Feature flags (maximum by default)
        support_dual = self._get_bool("support_dual_aperture", True)
        support_leica = self._get_bool("support_leica", True)
        support_street = self._get_bool("support_street", True)
        support_8k = self._get_bool("support_8k", True)
        support_raw = self._get_bool("support_raw", True)
        support_portrait = self._get_bool("support_portrait", True)
        support_pro = self._get_bool("support_pro", True)
        support_4k120 = self._get_bool("support_4k120", True)
        support_hfr = self._get_bool("support_hfr", True)
        support_dolby = self._get_bool("support_dolby", True)
        support_log = self._get_bool("support_log", True)
        support_director = self._get_bool("support_director", True)
        support_cinematic = self._get_bool("support_cinematic", True)
        support_night = self._get_bool("support_night", True)
        support_moon = self._get_bool("support_moon", True)
        support_astro = self._get_bool("support_astro", False)
        support_macro = self._get_bool("support_macro", True)
        support_doc = self._get_bool("support_doc", True)
        support_clone = self._get_bool("support_clone", False)
        support_long_exp = self._get_bool("support_long_exp", True)
        support_film = self._get_bool("support_film", True)

        # System options
        enable_spoof = self._get_bool("enable_spoof", False)
        spoof_device = cfg.get("spoof_device", codename)
        disable_stock = self._get_bool("disable_stock_camera", False)
        thermal_fix = self._get_bool("thermal_fix", True)
        aux_whitelist = self._get_bool("aux_whitelist", True)
        sdk_bypass = self._get_bool("sdk_bypass", True)
        hyperos3 = self._get_bool("hyperos3", True)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "module"
            root.mkdir()

            # --- module.prop ---
            prop = self._render(
                "module.prop",
                MODULE_ID=module_id,
                MODULE_NAME=module_name,
                VERSION=version,
                VERSION_CODE=version_code,
                AUTHOR=author,
                DESCRIPTION=description,
            )
            (root / "module.prop").write_text(prop, encoding="utf-8")

            # --- META-INF ---
            meta = root / "META-INF" / "com" / "google" / "android"
            meta.mkdir(parents=True)
            update_binary = '''#!/sbin/sh
# Magisk Module Installer
MODPATH=${0%/*}
SKIPUNZIP=1
. $MODPATH/customize.sh
'''
            (meta / "update-binary").write_text(update_binary, encoding="utf-8")
            (meta / "updater-script").write_text("#MAGISK\n", encoding="utf-8")

            # --- system structure ---
            priv_app = root / "system" / "priv-app" / "MiuiCamera"
            priv_app.mkdir(parents=True)

            if apk_path and Path(apk_path).is_file():
                shutil.copy2(apk_path, priv_app / "MiuiCamera.apk")
            else:
                (priv_app / "PLACE_APK_HERE.txt").write_text(
                    "Place your MiuiCamera.apk here and rebuild the module.\n"
                    "Recommended: HyperOS 2.0 / 5.3.x Leica builds for ishtar.\n",
                    encoding="utf-8",
                )

            # device_features
            feat_dir = root / "system" / "etc" / "device_features"
            feat_dir.mkdir(parents=True)

            render_kwargs = dict(
                SUPPORT_DUAL_APERTURE=self._bool_str(support_dual),
                SUPPORT_LEICA=self._bool_str(support_leica),
                SUPPORT_STREET=self._bool_str(support_street),
                SUPPORT_8K=self._bool_str(support_8k),
                SUPPORT_RAW=self._bool_str(support_raw),
                SUPPORT_PORTRAIT=self._bool_str(support_portrait),
                SUPPORT_PRO=self._bool_str(support_pro),
                SUPPORT_4K120=self._bool_str(support_4k120),
                SUPPORT_HFR=self._bool_str(support_hfr),
                SUPPORT_DOLBY=self._bool_str(support_dolby),
                SUPPORT_LOG=self._bool_str(support_log),
                SUPPORT_DIRECTOR=self._bool_str(support_director),
                SUPPORT_CINEMATIC=self._bool_str(support_cinematic),
                SUPPORT_NIGHT=self._bool_str(support_night),
                SUPPORT_MOON=self._bool_str(support_moon),
                SUPPORT_ASTRO=self._bool_str(support_astro),
                SUPPORT_MACRO=self._bool_str(support_macro),
                SUPPORT_DOC=self._bool_str(support_doc),
                SUPPORT_CLONE=self._bool_str(support_clone),
                SUPPORT_LONG_EXP=self._bool_str(support_long_exp),
                SUPPORT_FILM=self._bool_str(support_film),
            )

            if codename == "ishtar" and (TEMPLATES_DIR / "ishtar.xml").exists():
                xml = self._render("ishtar.xml", **render_kwargs)
                (feat_dir / "ishtar.xml").write_text(xml, encoding="utf-8")
            else:
                # Generic rich template for other devices
                generic = f'''<?xml version="1.0" encoding="utf-8"?>
<!-- Generated by Camera Port Studio for {device_name} ({codename}) -->
<features>
    <bool name="is_xiaomi">true</bool>
    <string name="device_name">{codename}</string>
    <string name="market_name">{device_name}</string>
    <bool name="support_quad_camera">true</bool>
    <bool name="is_support_ultra_wide">true</bool>
    <bool name="support_dual_aperture">{self._bool_str(support_dual)}</bool>
    <bool name="support_leica_authentic">{self._bool_str(support_leica)}</bool>
    <bool name="support_leica_vibrant">{self._bool_str(support_leica)}</bool>
    <bool name="support_leica_filter">{self._bool_str(support_leica)}</bool>
    <bool name="support_leica_watermark">{self._bool_str(support_leica)}</bool>
    <bool name="support_street_mode">{self._bool_str(support_street)}</bool>
    <bool name="support_fastshot">{self._bool_str(support_street)}</bool>
    <bool name="support_8k_video">{self._bool_str(support_8k)}</bool>
    <bool name="support_8k_24fps">{self._bool_str(support_8k)}</bool>
    <bool name="support_super_raw">{self._bool_str(support_raw)}</bool>
    <bool name="support_14bit_raw">{self._bool_str(support_raw)}</bool>
    <bool name="support_portrait_mode">{self._bool_str(support_portrait)}</bool>
    <bool name="support_bokeh">{self._bool_str(support_portrait)}</bool>
    <bool name="support_pro_mode">true</bool>
    <bool name="support_focus_peaking">{self._bool_str(support_pro)}</bool>
    <bool name="support_dolby_vision">{self._bool_str(support_dolby)}</bool>
    <bool name="support_log_video">{self._bool_str(support_log)}</bool>
    <bool name="support_director_mode">{self._bool_str(support_director)}</bool>
    <bool name="support_cinematic_mode">{self._bool_str(support_cinematic)}</bool>
    <bool name="camera_supported_super_night">{self._bool_str(support_night)}</bool>
    <bool name="support_moon_mode">{self._bool_str(support_moon)}</bool>
    <bool name="support_macro_mode">{self._bool_str(support_macro)}</bool>
    <bool name="support_document_mode">{self._bool_str(support_doc)}</bool>
    <bool name="support_clone_mode">{self._bool_str(support_clone)}</bool>
    <bool name="support_long_exposure">{self._bool_str(support_long_exp)}</bool>
    <bool name="support_film_mode">{self._bool_str(support_film)}</bool>
    <bool name="support_panorama">true</bool>
    <bool name="support_ai_scene">true</bool>
    <bool name="support_heif">true</bool>
    <bool name="support_live_photo">true</bool>
</features>
'''
                (feat_dir / f"{codename}.xml").write_text(generic, encoding="utf-8")

            # permissions
            perm_dir = root / "system" / "etc" / "permissions"
            perm_dir.mkdir(parents=True)
            shutil.copy2(
                TEMPLATES_DIR / "privapp-permissions-miuicamera.xml",
                perm_dir / "privapp-permissions-miuicamera.xml",
            )

            # --- scripts ---
            disable_block = ""
            if disable_stock:
                disable_block = '''
# Disable stock camera package
pm disable-user --user 0 com.android.camera 2>/dev/null || true
'''
            customize = self._render(
                "customize.sh",
                DEVICE_NAME=device_name,
                CODENAME=codename,
                DISABLE_STOCK_CAMERA=disable_block,
            )
            (root / "customize.sh").write_text(customize, encoding="utf-8")

            # post-fs-data.sh
            resetprop_block = ""
            if enable_spoof:
                resetprop_block = f'''
resetprop ro.product.device {spoof_device}
resetprop ro.product.model "{device_name}"
resetprop ro.product.name {spoof_device}
'''
            if hyperos3:
                resetprop_block += '''
resetprop ro.mi.os.version.code 3
resetprop ro.mi.os.version.name "OS3.0"
resetprop ro.miui.ui.version.code 816
'''
            if sdk_bypass:
                resetprop_block += '''
# Help bypass some SDK checks
resetprop ro.build.version.sdk 34
'''

            library_fix = '''
# Attempt to make camera libs available (best-effort)
for lib in libcamera_metadata.so libcamera_client.so; do
  if [ -f /system/lib64/$lib ]; then
    mkdir -p $MODDIR/system/lib64
    cp -f /system/lib64/$lib $MODDIR/system/lib64/ 2>/dev/null || true
  fi
done
'''

            selinux_block = '''
if command -v magiskpolicy >/dev/null 2>&1; then
  magiskpolicy --live "allow hal_camera_default * * *" 2>/dev/null || true
fi
'''

            postfs = self._render(
                "post-fs-data.sh",
                DEVICE_NAME=device_name,
                CODENAME=codename,
                RESETPROP_BLOCK=resetprop_block,
                LIBRARY_FIX_BLOCK=library_fix,
                SELINUX_BLOCK=selinux_block,
            )
            (root / "post-fs-data.sh").write_text(postfs, encoding="utf-8")

            # service.sh
            thermal_block = ""
            if thermal_fix:
                thermal_block = '''
# Soft thermal (best-effort)
resetprop persist.vendor.thermal.config 0 2>/dev/null || true
'''

            aux_block = ""
            if aux_whitelist:
                aux_block = '''
# AUX camera whitelist for AOSP / custom ROMs
resetprop vendor.camera.aux.packagelist com.android.camera,org.codeaurora.snapcam,com.google.android.GoogleCamera 2>/dev/null || true
resetprop persist.vendor.camera.privapp.list com.android.camera 2>/dev/null || true
'''

            service = self._render(
                "service.sh",
                CODENAME=codename,
                THERMAL_BLOCK=thermal_block,
                AUX_WHITELIST_BLOCK=aux_block,
            )
            (root / "service.sh").write_text(service, encoding="utf-8")

            # sepolicy.rule
            shutil.copy2(TEMPLATES_DIR / "sepolicy.rule", root / "sepolicy.rule")

            # --- Create ZIP ---
            out = Path(output_path)
            if out.exists():
                out.unlink()

            with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
                for file_path in root.rglob("*"):
                    if file_path.is_file():
                        arcname = file_path.relative_to(root)
                        zf.write(file_path, arcname)

            return str(out.resolve())


def build_module(
    apk_path: Optional[str] = None,
    output_path: str = "MiuiCamera_Port.zip",
    **config,
) -> str:
    builder = ModuleBuilder()
    builder.set_config(**config)
    return builder.build(apk_path=apk_path, output_path=output_path)
