from Main import *
import matplotlib.pyplot as plt
from PIL import Image


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

    ctext= read_file(basepath+'aes-ciphertext10-cbc.txt')
    key = read_file(basepath+'aes-key10.txt')
    mode = BlockMode.CBC
    aes = AES(verbose=False, block_mode=mode)
    print(mode)
    ptext = aes.decrypt(key, ctext)
    print('Output:\n' + ptext)

    # Convert to image
    img_bytes = wrap(ptext, 2)
    img_bytes = [hexstr_to_int(b) for b in img_bytes]
    height = 12
    width = 8
    bytearr = np.array(img_bytes).astype(int)
    bytearr = bytearr.reshape( (height, width) )

    im = Image.fromarray(bytearr, mode='L')
    plt.gray()
    plt.imshow(im)
    plt.show()


if __name__ == '__main__':
    demo()