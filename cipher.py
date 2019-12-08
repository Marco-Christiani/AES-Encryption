import click
import matplotlib.pyplot as plt
from Main import *
from PIL import Image


@click.command()
@click.option('-k', '--key', help='Key of length 16, 24, or 32 bytes.')
@click.option('-t', '--text', help='Text to encrypt (block padding is currently not supported).')
@click.option('-b', '--block-mode', default=1, help='1 for ECB, 2 for CBC')
@click.option('-tf', '--text-file', type=click.Path(exists=True), help='Input text file.')
@click.option('-kf', '--key-file', type=click.Path(exists=True), help='Input key file.')
@click.option('--verbose', type=bool, default=False)
@click.option('--debug', type=bool, default=False)
@click.option('--decrypt', type=bool, default=False)
def cipher(verbose, debug, block_mode, text=None, key=None, text_file=None, key_file=None, decrypt=False):
    if debug:
        verbose = False
    block_mode = BlockMode(block_mode)
    aes = AES(debug, verbose, block_mode)

    prompt = 'Encrypt'
    output_prompt = 'Ciphertext'
    if decrypt:
        prompt = 'Decrypt'
        output_prompt = 'Plaintext'

    if text_file:
        # txt_path = BASE_PATH+text_file
        # key_path = BASE_PATH+key_file

        # log(f'\n{"-"*20}{prompt}ing {fname_txt}{"-"*20}')
        aes.log(f'{prompt}ing {text_file}'.center(60, '-'))
        txt = read_file(text_file)
    elif text:
        txt = text
    else:
        return Exception()

    if text_file:
        key = read_file(key_file)
    elif not text:
        return Exception()

    aes.log('Configuration'.center(60, '-'))
    aes.log(f'DEBUG set to {debug}')
    aes.log(f'VERBOSE set to {verbose}')
    aes.log(f'Block mode set to {block_mode}')
    aes.log(f'Seed: {key}')
    aes.log('-'*60)
    aes.log(f'{prompt}ing data...', color=Fore.CYAN)

    if decrypt:
        output = aes.decrypt(key, txt)
    else:
        output = aes.encrypt(key, txt)

    aes.log(f'{prompt}ion complete.', color=Fore.CYAN)
    aes.log(f'\n{output_prompt}:')
    aes.log(output)


if __name__ == '__main__':
    init(autoreset=True)
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
    # img_bytes = wrap(ctext, 2)
    # img_bytes = [hexstr_to_int(b) for b in img_bytes]
    # img_length = len(img_bytes)
    # height = 12
    # width = 8
    # bytearr = np.array(img_bytes).astype(int)
    # bytearr = bytearr.reshape( (width, height) )
    #
    # im = Image.fromarray(bytearr, mode='L')
    # plt.gray()
    # plt.imshow(im)
    # plt.show()
