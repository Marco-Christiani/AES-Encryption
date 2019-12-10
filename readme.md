# AES-Encryption
1. [ Installation ](#install)
2. [ Command Line Tool ](#cmdline)
3. [ Run Tests ](#tests)
4. [ Run Demo ](#demo)

<a name="install"></a>
## Installation
```
unzip AES-Encryption.zip
cd AES-Encryption
pipenv install # This might take a moment
```
If pipenv or pip is not installed, install with ```chmod +x; sudo ./install.sh``` or:
```
sudo apt update
sudo apt install python3-pip -y
sudo pip3 install pipenv
```
*This application was built with Python 3.7*

Now that the virtual environment has been setup, dependencies are installed and all that is left is to activate the environment.

```pipenv shell``` will drop you into the virtual environment and all occurences of the ```python``` command in the remainder of this document assumes the ```pipenv shell``` command has been run. The virtual environment can be exited with ```exit```.

**Note that if you successfully activated the virtual environment ```(AES-Encryption)``` will appear beside the bash prompt**

*Alternatively, you can remain outside the virtual environment and the ```python``` command can be replaced with ```pipenv run```*

<a name="cmdline"></a>
## Command Line Tool
To read from text and key from files:
```
python cipher.py -tf <path/to/textfile> -kf <path/to/keyfile>
```

To pass literal strings:
```
python cipher.py -t <text> -k <key>
```
File and string input can be mixed:
```
python cipher.py -t <text> -kf <path/to/keyfile>
```
Decrypt with the ```--decrypt``` flag
```
python cipher.py -t <text> -k <key> --decrypt
```
Usage:
```
Usage: cipher.py [OPTIONS]

Options:
  -k, --key TEXT            Key of length 16, 24, or 32 bytes.
  -t, --text TEXT           Text to encrypt (block padding is currently not
                            supported).
  -b, --block-mode INTEGER  1 for ECB, 2 for CBC
  -tf, --text-file PATH     Input text file.
  -kf, --key-file PATH      Input key file.
  --verbose BOOLEAN
  --debug BOOLEAN
  --decrypt BOOLEAN
  --help                    Show this message and exit.
```
<a name="tests"></a>
## Run Tests
There are 8 test cases, output asserted against output from AES Web App. Each test encrypts a plaintext string, asserts its validity, decrypts the result, and asserts against the original plaintext. The final test case was provided on the site.
1. test_128_ecb
2. test_128_cbc
3. test_192_ecb
4. test_192_cbc
5. test_256_ecb
6. test_256_cbc
7. test_case_8

These tests can be run with ```python -m unittest discover```

<a name="demo"></a>
## Run Demo
```demo.py```:
- Encrypts aes-plaintext11.txt with aes-key11.txt in ECB mode
- Encrypts aes-plaintext12.txt with aes-key12.txt in ECB mode
- Encrypts aes-plaintext13.txt with aes-key13.txt in ECB mode
- Encrypts aes-plaintext13.txt with aes-key13.txt in CBC mode
- Decrypts aes-ciphertext10-cbc.txtt with aes-key10.txt in CBC mode
