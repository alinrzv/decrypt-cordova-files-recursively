'''
Credits to:
https://gist.github.com/swinton/8409454
http://stackoverflow.com/a/12525165/119849
http://blog.rz.my/2017/11/decrypting-cordova-crypt-file-plugin.html
https://ourcodeworld.com/articles/read/386/how-to-encrypt-protect-the-source-code-of-an-android-cordova-app

Standalone usage:
python decrypt-cordova-files.py "secret_key" "iv_value" "directory_path"
'''

import sys
import base64
import os
import errno
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-s[-1]]

class AESCipher:
    def __init__(self, key):
        self.key = key.encode('utf-8')

    def encrypt(self, raw):
        raw = pad(raw).encode('utf-8')
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')

    def decrypt(self, enc):
        try:
            enc = base64.b64decode(enc)
            iv = enc[:AES.block_size]
            enc = enc[AES.block_size:]
            if len(iv) != 16:
                raise ValueError(f"Incorrect IV length: {len(iv)}")
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(enc))
            return decrypted.decode('utf-8')
        except (ValueError, KeyError, base64.binascii.Error) as e:
            print(f"Decryption error: {e}")
            return None

def is_base64_encoded(data):
    try:
        if len(data) % 4 == 0:
            base64.b64decode(data)
            return True
        return False
    except Exception:
        return False

def decrypt_file(input_file, cipher):
    with open(input_file, 'r', encoding='utf-8') as myfile:
        data = myfile.read().replace('\n', '')

    if not is_base64_encoded(data):
        print(f"File is not encoded: {input_file}")
        return

    decrypted = cipher.decrypt(data)
    
    if decrypted:
        output_dir = os.path.join("decrypted", os.path.dirname(input_file))
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        output_file = os.path.join("decrypted", input_file)
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(decrypted)
    else:
        print(f"Failed to decrypt file: {input_file}")

def process_directory(directory, cipher):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.css', '.html', '.js')):
                file_path = os.path.join(root, file)
                decrypt_file(file_path, cipher)

if len(sys.argv) != 4:
    print('Usage: python decrypt-cordova-files.py "secret_key" "iv_value" "directory"')
    sys.exit(1)

cipher = AESCipher(sys.argv[1])
directory = sys.argv[3]
process_directory(directory, cipher)
