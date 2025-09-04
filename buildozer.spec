[app]

# (str) Title of your application
title = Video Downloader

# (str) Package name
package.name = videodownloader

# (str) Package domain (unique identifier)
package.domain = org.exemplo

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (comma separated)
source.include_exts = py

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy,yt-dlp,brotli,pycryptodomex,certifi

# (str) Entry point of the application
main.py = video_downloader_app.py

# (str) Application orientation (portrait, landscape or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0


#
# Android specific
#
[android]

# (int) Android API to use
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# ⚠️ Importante: usar o SDK instalado no workflow
sdk.dir = /home/runner/android-sdk

# (bool) Use --private data storage (True) or not (False)
android.private_storage = True

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE


#
# Buildozer itself
#
[buildozer]

log_level = 2
warn_on_root = 1
