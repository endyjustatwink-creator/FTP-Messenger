[app]

# Название приложения
title = FTP Messenger

# Имя пакета (должно быть уникальным)
package.name = ftpmessenger

# Домен пакета (обычно наоборот)
package.domain = org.ftpmessenger

# Версия приложения
version = 1.0

# Требуемые модули Python
requirements = python3, kivy, openssl, libffi

# Иконка приложения (положите в папку)
# icon.filename = %(source.dir)s/data/icon.png

# Исходный код главного файла
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Разрешения Android
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# API уровня Android
android.api = 29
android.minapi = 21
android.ndk = 23b

# Архитектура
android.arch = armeabi-v7a

# Ориентация экрана
orientation = portrait

# Полноэкранный режим
fullscreen = 0

[buildozer]

# Уровень логирования
log_level = 2
