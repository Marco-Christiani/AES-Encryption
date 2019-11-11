from Key_Calculations import *
from Matrix_Calculations import *
from BlockStream import *
from prettytable import PrettyTable


def encrypt(seed, plaintext, verbose=False):
    result = PrettyTable(field_names=None)
    table = PrettyTable()
    key_sch = KeySchedule(seed)
    byte_mode = key_sch.get_byte_mode()
    block_stream = BlockStream(plaintext, BlockMode.ECB, byte_mode)
    ctext_result = ''

    while not block_stream.is_empty():
        # Get next plaintext block
        ctext = block_stream.get_next_block()
        table.field_names = ['Round', 'Operation',
                             'Byte String']  # Create Table for new block
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

            # if rounds == 8:
            if key_sch.is_final_round():
                final_key = key_sch.get_next_key()
                ctext = mat.flatten_rows()
                ctext = add_round_key(final_key, ctext)  # Add final round key
                table.add_row(['', f'Add Round Key', ctext])
                break
            mat.mix_columns()  # Mix Columns
            table.add_row(['', 'Mix Columns', mat.flatten_cols()])
            ctext = mat.flatten_cols()

            table.add_row(['', '', ''])
        if verbose:
            result.add_row([f'Block {block_stream.get_block_num()} Ciphertext:', ctext])
            result.header = False
            result.vrules = 0
            print(table)
        ctext_result += ''.join(ctext)
        key_sch.reset_roundkey_count()

    print(result)
    print('Encrypted Message:', ctext_result)
    return ctext_result