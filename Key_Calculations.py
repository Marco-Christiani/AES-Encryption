import numpy as np

DEBUG = False
POLYCONSTANT = 0b100011011
SBOX = ['63', '7C', '77', '7B', 'F2', '6B', '6F', 'C5', '30', '01', '67', '2B', 'FE', 'D7', 'AB', '76', 'CA', '82',
        'C9', '7D', 'FA', '59', '47', 'F0', 'AD', 'D4', 'A2', 'AF', '9C', 'A4', '72', 'C0', 'B7', 'FD', '93', '26',
        '36', '3F', 'F7', 'CC', '34', 'A5', 'E5', 'F1', '71', 'D8', '31', '15', '04', 'C7', '23', 'C3', '18', '96',
        '05', '9A', '07', '12', '80', 'E2', 'EB', '27', 'B2', '75', '09', '83', '2C', '1A', '1B', '6E', '5A', 'A0',
        '52', '3B', 'D6', 'B3', '29', 'E3', '2F', '84', '53', 'D1', '00', 'ED', '20', 'FC', 'B1', '5B', '6A', 'CB',
        'BE', '39', '4A', '4C', '58', 'CF', 'D0', 'EF', 'AA', 'FB', '43', '4D', '33', '85', '45', 'F9', '02', '7F',
        '50', '3C', '9F', 'A8', '51', 'A3', '40', '8F', '92', '9D', '38', 'F5', 'BC', 'B6', 'DA', '21', '10', 'FF',
        'F3', 'D2', 'CD', '0C', '13', 'EC', '5F', '97', '44', '17', 'C4', 'A7', '7E', '3D', '64', '5D', '19', '73',
        '60', '81', '4F', 'DC', '22', '2A', '90', '88', '46', 'EE', 'B8', '14', 'DE', '5E', '0B', 'DB', 'E0', '32',
        '3A', '0A', '49', '06', '24', '5C', 'C2', 'D3', 'AC', '62', '91', '95', 'E4', '79', 'E7', 'C8', '37', '6D',
        '8D', 'D5', '4E', 'A9', '6C', '56', 'F4', 'EA', '65', '7A', 'AE', '08', 'BA', '78', '25', '2E', '1C', 'A6',
        'B4', 'C6', 'E8', 'DD', '74', '1F', '4B', 'BD', '8B', '8A', '70', '3E', 'B5', '66', '48', '03', 'F6', '0E',
        '61', '35', '57', 'B9', '86', 'C1', '1D', '9E', 'E1', 'F8', '98', '11', '69', 'D9', '8E', '94', '9B', '1E',
        '87', 'E9', 'CE', '55', '28', 'DF', '8C', 'A1', '89', '0D', 'BF', 'E6', '42', '68', '41', '99', '2D', '0F',
        'B0', '54', 'BB', '16']


class KeySchedule:

    def __init__(self, seed):
        self.key = []  # byte array as strings i.e. ['0a', '2f', ...]
        self.key_schedule = []  # expanded key broken into round keys
        seed = [seed[i:i + 2] for i in range(0, len(seed), 2)]  # break into array of pairs
        seedlen = len(seed)
        if seedlen == 16:
            self.key_expansion_128(seed)
        elif seedlen == 24:
            self.key_expansion_192(seed)
        elif seedlen == 32:
            self.key_expansion_256(seed)
        else:
            raise Exception('Key length must be 16, 24, or 32 bytes.')

    # seed: array of hex digits [A2, 5D, E4...]
    def key_expansion_128(self, seed):
        key = seed
        count = 0
        while len(key) < 176:
            for i in range(4):
                key_len = len(key)
                temp1 = key[key_len-4 : key_len] # last 4 bytes
                if i == 0:
                    temp1 = key_expansion_core(temp1, count)
                    count += 1
                temp2 = key[key_len-16 : key_len] # temp2 (last 16 bytes)
                temp2 = temp2[0:4] # first 4 of last 16 bytes
                result = []
                for j in range(4):
                    result.append(get_XOR(temp1[j], temp2[j]))
                key += result
                if DEBUG:
                    print('Completed round:', count)
                    print('Result:', result)
                    print('-'*40)
        self.key_schedule = [key[i:i + 16] for i in range(0, len(key), 16)]
        self.key = key

    # 192 byte expansion
    # seed: array of 1's and 0's as strings
    def key_expansion_192(self, seed):
        return None

    # 256 byte expansion is a special case
    def key_expansion_256(self, seed):
        return None

    def get_keyschedule(self):
        return self.key_schedule


# key: array of hex digits as strings ie [A2, 5D, ..]
def key_expansion_core(key, i):
    key = np.roll(key, -1) # rotate_left
    # key = [SBOX[ hexstr_to_int(c) ] for c in key] # s_box
    key = sub_bytes(key)

    rcon = 2**i # calculate x^i
    if i == 8:
        rcon = rcon ^ POLYCONSTANT
    if i == 9:
        rcon = rcon ^ (POLYCONSTANT << 1)

    xor = rcon^hexstr_to_int(key[0])  # XOR rcon with the first byte of key
    xor = xor%POLYCONSTANT

    key[0] = hex(xor).split('0x')[1]  # convert ints in key to hex strings
    key[0] = int_to_hexstr(xor)

    return key

# x: hex digits as string ie 'A2'
# y: hex digits as string ie 'A2'
# return: x XOR y as string
def get_XOR(x, y):
    result = hexstr_to_int(x) ^ hexstr_to_int(y)
    result = int_to_hexstr(result)
    # if len(result) == 1:
    #     result = '0'+result  # pad with 0
    return result


# key and text are arrays of bytes
# len(key) == len(text)
def add_round_key(key, text):
    result = []
    # kbytes = wrap(key, 2)
    # tbytes = wrap(text, 2)
    for kbyte, tbyte in zip(key, text):
        result.append(get_XOR(kbyte, tbyte))
    return result


def hexstr_to_int(hexstr):
    return int('0x'+hexstr, 0)


def int_to_hexstr(number):
    result = hex(number).split('0x')[1]  # Convert to string without '0x'
    # Pad with zeros if necessary
    result = '0'*(2-len(result))+result
    return result


def sub_bytes(bytes):
    return [SBOX[hexstr_to_int(b)] for b in bytes]


def test_keyschedule(seed):
    key_sch = KeySchedule(seed)
    # for i in range(1, 12):
    #     print(key_sch.get_round_key(i))
    for roundkey in key_sch.key_schedule:
        print(''.join(roundkey))


# test_keyschedule('12476278dbc36bd9dc2cf5716a43b4bb')



