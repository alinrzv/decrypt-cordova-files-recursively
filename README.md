# Decrypt Files encrypted using Cordova Crypt File Plugin
Python script to decrypt files encrypted using Cordova in Android app

## Where is Secret Key and IV?

1. Decompile APK using Dex2Jar and open JAR file in JD-Gui
2. Secrey Key and IV can be found hardcoded in `com.tkyaki.cordova/DecryptResource.class` file 
OR if you are using an online decompiler (ex: decompiler[.com]) you can look into path `/sources/com/tkyaji/cordova/DecryptResource.class`

## Usage

Standalone usage (it will decrypt html,css,js files):

```python decrypt-cordova-files.py "secret_key" "iv_value" "directory_path"```


## Credits to:
https://gist.github.com/swinton/8409454

http://stackoverflow.com/a/12525165/119849

http://blog.rz.my/2017/11/decrypting-cordova-crypt-file-plugin.html

https://ourcodeworld.com/articles/read/386/how-to-encrypt-protect-the-source-code-of-an-android-cordova-app
