[app]
title = FTP Messenger
package.name = ftpmessenger
package.domain = org.ftpmessenger
version = 0.1
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
orientation = portrait
requirements = python3,kivy,openssl,requests,plyer
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 31
android.minapi = 21
android.ndk = 23b
android.sdk = 33
p4a.branch = master

[buildozer]
log_level = 2
