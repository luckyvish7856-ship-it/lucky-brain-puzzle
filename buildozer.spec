[app]
title = LUCKY BRAIN PUZZLE PRO
package.name = luckybrainpuzzle
package.domain = org.lucky
source.dir = .
source.main = main.py
version = 1.0.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
source.include_exts = py,json,png,jpg,kv
android.archs = arm64-v8a, armeabi-v7a
android.minapi = 23

[buildozer]
log_level = 2
warn_on_root = 1
