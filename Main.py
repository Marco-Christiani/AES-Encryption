from Key_Calculations import *
from Matrix_Calculations import *
from BlockStream import *
from prettytable import PrettyTable
from enum import Enum


class BlockMode(Enum):
    ECB = 1
    CBC = 2


def encrypt(seed,
            plaintext,
            block_mode: BlockMode = BlockMode.ECB,
            verbose=False):
    result = PrettyTable(field_names=None)

    key_sch = KeySchedule(seed)
    block_stream = BlockStream(plaintext.lower())
    ctext_result = []

    while not block_stream.is_empty():
        # Get next plaintext block
        temp = block_stream.get_next_block()
        if (block_mode is BlockMode.CBC) \
                and (block_stream.get_block_num() != 1):
            temp = add_round_key(
                temp, ctext)  # XOR w/ previous ciphered block (reuse method)
        ctext = temp

        # Create Table for new block
        table = PrettyTable()
        table.field_names = ['Round', 'Operation', 'Byte String']
        table.align['Operation'] = 'l'
        table.add_row(['', 'Current Block', ctext])

        # Encrypt block -------------------------------------------------------
        for round_num in range(key_sch.get_num_rounds()):
            roundkey = key_sch.get_next_key()

            ctext = add_round_key(roundkey, ctext)  # Add round key
            table.add_row([round_num, f'Add Round Key', ctext])

            ctext = sub_bytes(ctext)  # Sub bytes
            table.add_row(['', 'Sub Bytes', ctext])

            mat = Matrix(ctext)  # Convert to 4x4 byte matrix
            mat.shift_rows()  # Shift rows
            table.add_row(['', 'Shift Rows', mat.flatten_rows()])

            if key_sch.is_final_round():
                final_key = key_sch.get_next_key()
                ctext = mat.flatten_rows()
                ctext = add_round_key(final_key, ctext)  # Add final round key
                table.add_row(['', f'Add Round Key', ctext])
                break
            mat.mix_columns()  # Mix Columns
            table.add_row(['', 'Mix Columns', mat.flatten_rows()])
            ctext = mat.flatten_rows()

            table.add_row(['', '', ''])
        if verbose:
            result.add_row(
                [f'Block {block_stream.get_block_num()} Ciphertext:', ctext])
            result.header = False
            result.vrules = 0
            print(table)
        ctext_result.append(''.join(ctext))
        key_sch.reset_roundkey_count()
        # End Encrypt Block ----------------------------------------------------
    ctext_result = ''.join(ctext_result)
    if verbose:
        print(result)
        print('Encrypted Message:', ctext_result)
    return ctext_result


def decrypt(seed,
            ciphertext,
            block_mode: BlockMode = BlockMode.ECB,
            verbose=False):
    result = PrettyTable(field_names=None)
    table = PrettyTable()

    key_sch = KeySchedule(seed, decrypt=True)
    # key_sch = KeySchedule(seed)
    # block_stream = BlockStream(ciphertext.lower(), decrypt=True)
    block_stream = BlockStream(ciphertext.lower())
    ptext_result = []

    while not block_stream.is_empty():
        # Get next ciphertext block
        temp = block_stream.get_next_block()
        if (block_mode is BlockMode.CBC) \
                and (block_stream.get_block_num() != 1):
            temp = add_round_key(
                temp, ptext)  # XOR w/ previous decrypted block (reuse method)
        ptext = temp

        # Create Table for new block
        table.field_names = ['Round', 'Operation', 'Byte String']
        table.align['Operation'] = 'l'
        table.add_row(['', 'Current Block', ptext])

        # Decrypt block -------------------------------------------------------
        for round_num in range(key_sch.get_num_rounds()):
            roundkey = key_sch.get_next_key()
            ptext = add_round_key(roundkey, ptext)  # Add  round key
            table.add_row([round_num, f'Add Round Key', ptext])

            mat = Matrix(ptext)  # Convert to 4x4 byte matrix

            if round_num > 0:
                mat.mix_columns(inverse=True)  # Mix Columns
                table.add_row(['', 'Inv Mix Columns', mat.flatten_rows()])
                ptext = mat.flatten_cols()

            mat.shift_rows(inverse=True)  # Inverse shift rows
            ptext = mat.flatten_rows()
            table.add_row(['', 'Inv Shift Rows', ptext])

            ptext = sub_bytes(ptext, inverse=True)  # Inverse sub bytes
            table.add_row(['', 'Inv Sub Bytes', ptext])

            table.add_row(['', '', ''])
            if key_sch.is_final_round():
                final_key = key_sch.get_next_key()
                ptext = add_round_key(ptext, final_key)  # Add final round key
                table.add_row(['', f'Add Round Key', ptext])
                break

        if verbose:
            result.add_row(
                [f'Block {block_stream.get_block_num()} Plaintext:', ptext])
            result.header = False
            result.vrules = 0
            print(table)
        ptext_result.append(''.join(ptext))
        key_sch.reset_roundkey_count()
        # End Decrypt Block ----------------------------------------------------
    ctext_result = ''.join(ptext_result)
    if verbose:
        print(result)
        print('Decrypted Message:', ptext_result)
    return ctext_result
