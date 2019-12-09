from Key_Calculations import *
from Matrix_Calculations import *
from BlockStream import *
from prettytable import PrettyTable
from enum import Enum
from colorama import Fore, Style
import click


class BlockMode(Enum):
    ECB = 1
    CBC = 2


class AES():
    def __init__(self, debug=False, verbose=False, block_mode: BlockMode = BlockMode.ECB):
        self.debug = debug
        self.verbose = verbose
        self.block_mode = block_mode

    def encrypt(self, seed, plaintext):
        result = PrettyTable(field_names=None)

        key_sch = KeySchedule(seed)
        block_stream = BlockStream(plaintext.lower())
        ctext_result = []

        while not block_stream.is_empty():
            # Get next plaintext block
            temp = block_stream.get_next_block()
            if (self.block_mode is BlockMode.CBC) \
                    and (block_stream.get_block_num() != 1):
                temp = add_round_key(
                    temp, ctext)  # XOR w/ previous ciphered block (reuse method)
            ctext = temp

            # Create Table for new block
            table = PrettyTable()
            table.field_names = ['Round', 'Operation', 'Byte String']
            table.align['Operation'] = 'l'
            table.add_row(['', 'Current Block', ctext])
            self.log(f'\nCurrent Block {ctext}', debug=True)

            # Encrypt block --------------------------------------------------------------------------------------------
            for round_num in range(key_sch.get_num_rounds()):
                roundkey = key_sch.get_next_key()

                ctext = add_round_key(roundkey, ctext)  # Add round key
                table.add_row([round_num, f'Add Round Key', ctext])
                self.log(f'{round_num} Add Round Key {ctext}', debug=True)

                ctext = sub_bytes(ctext)  # Sub bytes
                table.add_row(['', 'Sub Bytes', ctext])
                self.log(f'Sub Bytes {ctext}', debug=True)

                mat = Matrix(ctext)  # Convert to 4x4 byte matrix
                mat.shift_rows()  # Shift rows
                table.add_row(['', 'Shift Rows', mat.flatten_rows()])
                self.log(f'Shift Rows {mat.flatten_rows()}', debug=True)

                if key_sch.is_final_round():
                    final_key = key_sch.get_next_key()
                    ctext = mat.flatten_rows()
                    ctext = add_round_key(final_key, ctext)  # Add final round key
                    table.add_row(['', f'Add Round Key', ctext])
                    break
                mat.mix_columns()  # Mix Columns
                table.add_row(['', 'Mix Columns', mat.flatten_rows()])
                self.log(f'Mix Columns {mat.flatten_rows()}', debug=True)
                ctext = mat.flatten_rows()

                table.add_row(['', '', ''])
            if self.verbose:
                result.add_row(
                    [f'Block {block_stream.get_block_num()} Ciphertext:', ctext])
                # self.log(f'Block {block_stream.get_block_num()} Ciphertext: {ctext}', debug=True)
                result.header = False
                result.vrules = 0
                self.log(table)
            ctext_result.append(''.join(ctext))
            key_sch.reset_roundkey_count()
            # End Encrypt Block ----------------------------------------------------------------------------------------
        if self.verbose:
            print(result)
            print('Encrypted Message:', ctext_result)
        ctext_result = ''.join(ctext_result)
        return ctext_result

    def decrypt(self, seed, ciphertext):
        result = PrettyTable(field_names=None)
        table = PrettyTable()

        key_sch = KeySchedule(seed, decrypt=True)

        block_stream = BlockStream(ciphertext.lower())
        ptext_result = []

        while not block_stream.is_empty():
            prev_block = block_stream.get_prev_block()  # Save previous ciphertext block for CBC mode
            ptext = block_stream.get_next_block()  # Get next ciphertext block

            # Create Table for new block
            table.field_names = ['Round', 'Operation', 'Byte String']
            table.align['Operation'] = 'l'
            table.add_row(['', 'Current Block', ptext])
            self.log(f'\nCurrent Block {ptext}', debug=True)

            # Decrypt block --------------------------------------------------------------------------------------------
            for round_num in range(key_sch.get_num_rounds()):
                roundkey = key_sch.get_next_key()
                ptext = add_round_key(roundkey, ptext)  # Add  round key
                table.add_row([round_num, f'Add Round Key', ptext])
                self.log(f'{round_num} Add Round Key {ptext}', debug=True)

                mat = Matrix(ptext)  # Convert to 4x4 byte matrix

                if round_num > 0:
                    mat.mix_columns(inverse=True)  # Mix Columns
                    table.add_row(['', 'Inv Mix Columns', mat.flatten_rows()])
                    self.log(f'Inv Mix Columns {mat.flatten_rows()}', debug=True)
                    ptext = mat.flatten_cols()

                mat.shift_rows(inverse=True)  # Inverse shift rows
                ptext = mat.flatten_rows()
                table.add_row(['', 'Inv Shift Rows', ptext])
                self.log(f'Inv Shift Rows {ptext}', debug=True)

                ptext = sub_bytes(ptext, inverse=True)  # Inverse sub bytes
                table.add_row(['', 'Inv Sub Bytes', ptext])
                self.log(f'Inv Sub Bytes {ptext}', debug=True)

                table.add_row(['', '', ''])
                if key_sch.is_final_round():
                    final_key = key_sch.get_next_key()
                    ptext = add_round_key(ptext, final_key)  # Add final round key
                    table.add_row(['', 'Add Round Key', ptext])
                    self.log(f'Add Round Key {ptext}', debug=True)
                    break

            if (self.block_mode is BlockMode.CBC) \
                    and (block_stream.get_block_num() != 1):
                ptext = add_round_key(
                    ptext, prev_block)  # XOR w/ previous ciphertext block (reuse method)

            self.log(f'Block {block_stream.get_block_num()} Plaintext: {ptext}', debug=True)

            if self.verbose:
                result.add_row(
                    [f'Block {block_stream.get_block_num()} Plaintext:', ptext])
                result.header = False
                result.vrules = 0
                print(table)
            ptext_result.append(''.join(ptext))
            key_sch.reset_roundkey_count()
            # End Decrypt Block ----------------------------------------------------------------------------------------
        if self.verbose:
            print(result)
        ctext_result = ''.join(ptext_result)
        return ctext_result

    def set_blockmode(self, block_mode: BlockMode):
        self.block_mode = block_mode
    #                                                /------------------\
    # -----------------------------------------------| Helper Functions |-----------------------------------------------
    #                                                \------------------/
    def log(self, msg, debug=False, **kwargs):
        color = kwargs.get('color', '')
        if type(msg) is str:
            msg = color+msg
        if debug:  # if it is debugging output
            if self.debug:  # if class-wide debugging output is enabled
                click.echo(msg)
            else:
                return
        else:
            click.echo(msg)

def read_file(path):
    click.echo(f'Loading file {Fore.GREEN + path + Style.RESET_ALL}... ', nl=False, color=True)
    f = open(path)
    contents = f.readlines()
    contents = ''.join(contents)
    f.close()
    if contents is not None:
        click.echo('File loaded!')
    else:
        click.echo(Fore.RED + 'Read failed.' + Style.RESET_ALL)
        click.echo('Process terminated.')
        exit()
    return contents


if __name__ == '__main__':
    init(autoreset=True)
