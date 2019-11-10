from Key_Calculations import *
from Matrix_Calculations import *
from BlockStream import *
from textwrap import wrap
from prettytable import PrettyTable


def encrypt(seed, plaintext):
    table = PrettyTable()
    table.field_names = ['Round', 'Operation', 'Byte String']
    table.align['Operation'] = 'l'

    key_sch = KeySchedule(seed)

    rounds = -1
    block_stream = BlockStream(plaintext, BlockMode.ECB, ByteMode.b16)
    ctext = block_stream.get_next_block()
    table.add_row(['', 'Current Block', ''.join(ctext)])

    # Encrypt block -------------------------------------------------------

    for roundkey in key_sch.get_keyschedule():
        ctext = add_round_key(roundkey, ctext)  # Add round key
        table.add_row([rounds, f'Add Round Key', ''.join(ctext)])
        ctext = sub_bytes(ctext)  # Sub bytes
        table.add_row(['', 'Sub Bytes', ''.join(ctext)])

        mat = Matrix(''.join(ctext))  # Convert to 4x4 byte matrix
        mat.shift_rows()  # Shift rows
        table.add_row(['', 'Shift Rows', ''.join(mat.flatten_rows())])

        if rounds == 8:
            table.add_row(['', '', ''])
            final_key = key_sch.get_keyschedule()[-1]
            ctext = mat.flatten_rows()
            ctext = add_round_key(final_key, ctext)  # Add final round key
            table.add_row([rounds+1, f'Add Round Key', ''.join(ctext)])
            break
        mat.mix_columns()  # Mix Columns
        table.add_row(['', 'Mix Columns', ''.join(mat.flatten_cols())])
        ctext = mat.flatten_cols()

        table.add_row(['', '', ''])
        rounds += 1
    print(table)

# encrypt('12476278dbc36bd9dc2cf5716a43b4bb', 'this is the text to encrypt')
encrypt('12476278dbc36bd9dc2cf5716a43b4bb', 'A01478BE92570366F1D13C098726DAC5')




