from Main import *


def demo():
    basepath = 'testfiles/'
    ptext= read_file(basepath+'aes-plaintext11.txt')
    key = read_file(basepath+'aes-key11.txt')
    mode = BlockMode.ECB
    aes = AES(verbose=False, block_mode=mode)
    print(mode)
    print('Output:\n' + aes.encrypt(key, ptext))
    print()

    ptext= read_file(basepath+'aes-plaintext12.txt')
    key = read_file(basepath+'aes-key12.txt')
    mode = BlockMode.ECB
    aes = AES(verbose=False, block_mode=mode)
    print(mode)
    print('Output:\n' + aes.encrypt(key, ptext))
    print()

    ptext= read_file(basepath+'aes-plaintext13.txt')
    key = read_file(basepath+'aes-key13.txt')
    mode = BlockMode.ECB
    aes = AES(verbose=False, block_mode=mode)
    print(mode)
    print('Output:\n' + aes.encrypt(key, ptext))
    print()

    mode = BlockMode.CBC
    aes = AES(verbose=False, block_mode=mode)
    print(mode)
    print('Output:\n' + aes.encrypt(key, ptext))
    print()

    ctext = read_file(basepath+'aes-ciphertext10-cbc.txt')
    key = read_file(basepath+'aes-key10.txt')
    mode = BlockMode.CBC
    aes = AES(verbose=False, block_mode=mode)
    print(mode)
    ptext = aes.decrypt(key, ctext)
    print('Output:\n' + ptext)


if __name__ == '__main__':
    demo()