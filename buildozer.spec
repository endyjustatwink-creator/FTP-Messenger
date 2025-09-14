[app]
title = FTP Messenger
package.name = ftpmessenger
package.domain = org.ftpmessenger
version = 0.1
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
orientation = portrait
requirements = python3,kivy==2.3.0,openssl,requests,plyer
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
android.api = 33
android.minapi = 21
android.ndk = 23b
p4a.branch = master

[buildozer]
log_level = 2
