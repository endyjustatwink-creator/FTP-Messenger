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
        
    - name: Check files
      run: |
        ls -la
        echo "Files in repository:"
        find . -type f -name "*.py" -o -name "*.spec"
        
    - name: Build APK
      run: |
        buildozer -v android debug
