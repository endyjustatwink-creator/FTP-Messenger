name: Build Android APK

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Install dependencies
      run: |
        sudo apt update
        sudo apt install -y zlib1g-dev openjdk-17-jdk
        pip install buildozer
    - name: Build APK
      run: buildozer android debug
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: FTP-Messenger-APK
        path: bin/*.apk
