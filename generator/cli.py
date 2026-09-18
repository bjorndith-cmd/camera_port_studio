#!/usr/bin/env python3
"""
Camera Port Studio - CLI mode
Usage examples:

  python -m generator.cli --apk MiuiCamera.apk --device ishtar --all-modes
  python -m generator.cli --apk MiuiCamera.apk --device ishtar --no-8k --no-astro -o my_port.zip
"""

import argparse
from pathlib import Path
from .module_builder import build_module


def main():
    p = argparse.ArgumentParser(description="Camera Port Studio CLI - Magisk Module Generator")
    p.add_argument("--apk", type=str, default=None, help="Path to MiuiCamera.apk")
    p.add_argument("-o", "--output", type=str, default="MiuiCamera_Port.zip", help="Output ZIP path")
    p.add_argument("--device", type=str, default="ishtar", help="Codename (ishtar, aurora, ...)")
    p.add_argument("--name", type=str, default="Xiaomi 13 Ultra", help="Market name")
    p.add_argument("--module-id", type=str, default="miuicamera_port")
    p.add_argument("--module-name", type=str, default="MIUI Camera Port")
    p.add_argument("--version", type=str, default="5.3.0-max")
    p.add_argument("--author", type=str, default="CameraPortStudio")

    # Mode toggles (default True, use --no-xxx to disable)
    p.add_argument("--all-modes", action="store_true", help="Force enable all modes")
    p.add_argument("--no-dual", action="store_true")
    p.add_argument("--no-leica", action="store_true")
    p.add_argument("--no-street", action="store_true")
    p.add_argument("--no-8k", action="store_true")
    p.add_argument("--no-raw", action="store_true")
    p.add_argument("--no-portrait", action="store_true")
    p.add_argument("--no-pro", action="store_true")
    p.add_argument("--no-4k120", action="store_true")
    p.add_argument("--no-hfr", action="store_true")
    p.add_argument("--no-dolby", action="store_true")
    p.add_argument("--no-log", action="store_true")
    p.add_argument("--no-director", action="store_true")
    p.add_argument("--no-cinematic", action="store_true")
    p.add_argument("--no-night", action="store_true")
    p.add_argument("--no-moon", action="store_true")
    p.add_argument("--astro", action="store_true", help="Enable astro (off by default)")
    p.add_argument("--no-macro", action="store_true")
    p.add_argument("--no-doc", action="store_true")
    p.add_argument("--clone", action="store_true", help="Enable clone (off by default)")
    p.add_argument("--no-long-exp", action="store_true")
    p.add_argument("--no-film", action="store_true")

    # System
    p.add_argument("--spoof", type=str, default=None, help="Spoof device codename")
    p.add_argument("--no-hyperos3", action="store_true")
    p.add_argument("--no-sdk-bypass", action="store_true")
    p.add_argument("--no-thermal", action="store_true")
    p.add_argument("--no-aux", action="store_true")
    p.add_argument("--disable-stock", action="store_true")

    args = p.parse_args()

    def on(flag_no, default=True):
        if args.all_modes:
            return True
        return default and not flag_no

    config = dict(
        module_id=args.module_id,
        module_name=args.module_name,
        version=args.version,
        version_code="530",
        author=args.author,
        description="CLI generated MIUI/HyperOS Camera port with selected modes",
        codename=args.device,
        device_name=args.name,
        support_dual_aperture=on(args.no_dual),
        support_leica=on(args.no_leica),
        support_street=on(args.no_street),
        support_8k=on(args.no_8k),
        support_raw=on(args.no_raw),
        support_portrait=on(args.no_portrait),
        support_pro=on(args.no_pro),
        support_4k120=on(args.no_4k120),
        support_hfr=on(args.no_hfr),
        support_dolby=on(args.no_dolby),
        support_log=on(args.no_log),
        support_director=on(args.no_director),
        support_cinematic=on(args.no_cinematic),
        support_night=on(args.no_night),
        support_moon=on(args.no_moon),
        support_astro=args.astro or args.all_modes,
        support_macro=on(args.no_macro),
        support_doc=on(args.no_doc),
        support_clone=args.clone or args.all_modes,
        support_long_exp=on(args.no_long_exp),
        support_film=on(args.no_film),
        enable_spoof=bool(args.spoof),
        spoof_device=args.spoof or args.device,
        hyperos3=not args.no_hyperos3,
        sdk_bypass=not args.no_sdk_bypass,
        thermal_fix=not args.no_thermal,
        aux_whitelist=not args.no_aux,
        disable_stock_camera=args.disable_stock,
    )

    print(f"[*] Building module for {args.name} ({args.device})...")
    if args.apk:
        print(f"[*] Using APK: {args.apk}")
    else:
        print("[!] No APK provided — placeholder will be used")

    path = build_module(apk_path=args.apk, output_path=args.output, **config)
    print(f"[+] Done: {path}")


if __name__ == "__main__":
    main()
