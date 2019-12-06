from Main import *
VERBOSE = False
BASE_PATH = './testfiles/'


def read_file(path):
    print(f'Loading file {path}... ', end='')
    f = open(path)
    contents = f.readlines()
    contents = ''.join(contents)
    f.close()
    if contents is not None:
        print('File loaded!')
    else:
        print('Read failed.')
        print('Process terminated.')
        exit()
    return contents


def run_encrypt(fname_txt, fname_key, block_mode, _decrypt=False):
    prompt = 'Encrypt'
    output_prompt = 'Ciphertext'
    if _decrypt:
        prompt = 'Decrypt'
        output_prompt = 'Plaintext'

    txt_path = BASE_PATH+fname_txt
    key_path = BASE_PATH+fname_key

    print(f'\n{"-"*20}{prompt}ing {fname_txt}{"-"*20}')

    key = read_file(key_path)
    txt = read_file(txt_path)

    print('txt: ', wrap(txt,2))

    print('VERBOSE set to', VERBOSE)
    print('Block mode set to', block_mode)
    print('Seed:', key)
    print(f'{prompt}ing data...')

    if _decrypt:
        output = decrypt(key, txt, block_mode, VERBOSE)
    else:
        output = encrypt(key, txt, block_mode, VERBOSE)

    print(f'{prompt}ion complete.')
    print(f'\n{output_prompt}:')
    print(output)


if __name__ == '__main__':
    ptext_filename = 'aes-plaintext11.txt'
    # key_filename = 'aes-key11.txt'
    # mode = BlockMode.ECB
    # run_encrypt(ptext_filename, key_filename, mode)
    #
    # ptext_filename = 'aes-plaintext12.txt'
    # key_filename = 'aes-key12.txt'
    # mode = BlockMode.ECB
    # run_encrypt(ptext_filename, key_filename, mode)
    #
    # ptext_filename = 'aes-plaintext13.txt'
    # key_filename = 'aes-key13.txt'
    # mode = BlockMode.ECB
    # run_encrypt(ptext_filename, key_filename, mode)
    #
    # ptext_filename = 'aes-plaintext13.txt'
    # key_filename = 'aes-key13.txt'
    # mode = BlockMode.CBC
    # run_encrypt(ptext_filename, key_filename, mode)

    ctext_filename = 'aes-ciphertext10-cbc.txt'
    key_filename = 'aes-key10.txt'
    mode = BlockMode.CBC

    print(len(wrap(read_file(BASE_PATH+ ctext_filename), 2)))
    print(len(wrap(read_file(BASE_PATH+ key_filename), 2)))

    run_encrypt(ctext_filename, key_filename, mode, _decrypt=True)
