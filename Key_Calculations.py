import numpy as np
from textwrap import wrap

DEBUG = False
POLYCONSTANT = 0b100011011
SBOX = [
    '63', '7C', '77', '7B', 'F2', '6B', '6F', 'C5', '30', '01', '67', '2B',
    'FE', 'D7', 'AB', '76', 'CA', '82', 'C9', '7D', 'FA', '59', '47', 'F0',
    'AD', 'D4', 'A2', 'AF', '9C', 'A4', '72', 'C0', 'B7', 'FD', '93', '26',
    '36', '3F', 'F7', 'CC', '34', 'A5', 'E5', 'F1', '71', 'D8', '31', '15',
    '04', 'C7', '23', 'C3', '18', '96', '05', '9A', '07', '12', '80', 'E2',
    'EB', '27', 'B2', '75', '09', '83', '2C', '1A', '1B', '6E', '5A', 'A0',
    '52', '3B', 'D6', 'B3', '29', 'E3', '2F', '84', '53', 'D1', '00', 'ED',
    '20', 'FC', 'B1', '5B', '6A', 'CB', 'BE', '39', '4A', '4C', '58', 'CF',
    'D0', 'EF', 'AA', 'FB', '43', '4D', '33', '85', '45', 'F9', '02', '7F',
    '50', '3C', '9F', 'A8', '51', 'A3', '40', '8F', '92', '9D', '38', 'F5',
    'BC', 'B6', 'DA', '21', '10', 'FF', 'F3', 'D2', 'CD', '0C', '13', 'EC',
    '5F', '97', '44', '17', 'C4', 'A7', '7E', '3D', '64', '5D', '19', '73',
    '60', '81', '4F', 'DC', '22', '2A', '90', '88', '46', 'EE', 'B8', '14',
    'DE', '5E', '0B', 'DB', 'E0', '32', '3A', '0A', '49', '06', '24', '5C',
    'C2', 'D3', 'AC', '62', '91', '95', 'E4', '79', 'E7', 'C8', '37', '6D',
    '8D', 'D5', '4E', 'A9', '6C', '56', 'F4', 'EA', '65', '7A', 'AE', '08',
    'BA', '78', '25', '2E', '1C', 'A6', 'B4', 'C6', 'E8', 'DD', '74', '1F',
    '4B', 'BD', '8B', '8A', '70', '3E', 'B5', '66', '48', '03', 'F6', '0E',
    '61', '35', '57', 'B9', '86', 'C1', '1D', '9E', 'E1', 'F8', '98', '11',
    '69', 'D9', '8E', '94', '9B', '1E', '87', 'E9', 'CE', '55', '28', 'DF',
    '8C', 'A1', '89', '0D', 'BF', 'E6', '42', '68', '41', '99', '2D', '0F',
    'B0', '54', 'BB', '16'
]


class KeySchedule:
    """
    Creates an AES key schedule by expanding an initial key (seed) and stores the expanded result as a list of subkeys.
    """
    def __init__(self, seed, decrypt=False):
        """
        Sets up a KeySchedule with user options.

        :param seed: key to be expanded
        :param decrypt: if true, reverses key schedule order
        """
        self.key = []  # byte array as strings i.e. ['0a', '2f', ...]
        self.key_schedule = []  # expanded key broken into round keys
        self.curr_round = 0
        self.decrypt = decrypt
        seed = wrap(seed, 2)
        seedlen = len(seed)
        if seedlen == 16:
            self.rounds = 10
            self.key_expansion_128(seed)

        elif seedlen == 24:
            self.rounds = 12
            self.key_expansion_192(seed)

        elif seedlen == 32:
            self.rounds = 14
            self.key_expansion_256(seed)
        else:
            raise Exception('Key length must be 16, 24, or 32 bytes.')

    def key_expansion_128(self, seed):
        """
        Expands 16 byte key to 128 byte keyschedule, according to AES specification.

        :param seed: array of hex digits [A2, 5D, E4...]
        """
        key = seed
        count = 0
        key_len = len(key)
        while len(key) < 176:
            for i in range(4):
                temp1 = key[key_len - 4:key_len]  # last 4 bytes
                if i == 0:
                    temp1 = key_expansion_core(temp1, count)
                    count += 1
                temp2 = key[key_len - 16:key_len]  # temp2 (last 16 bytes)
                temp2 = temp2[0:4]  # first 4 of last 16 bytes
                result = []
                for j in range(4):
                    result.append(get_XOR(temp1[j], temp2[j]))
                key += result
                key_len = len(key)
                if key_len >= 176:
                    break

        self.key_schedule = [key[i:i + 16] for i in range(0, len(key), 16)]
        self.key_schedule = [''.join(key) for key in self.key_schedule]
        self.key = key
        if self.decrypt:
            self.key_schedule = list(reversed(self.key_schedule))
            self.key = ''.join(self.key_schedule)
        if DEBUG:
            print('Using 128 byte expansion...')
            print(f'Key is {"".join(key)}')
            print(f'Length is {len(key)} bytes')
            print(f'Key schedule is {self.key_schedule}')
            print(f'{len(self.key_schedule)} subkeys')

    def key_expansion_192(self, seed):
        """
        Expands 24 byte key to 192 byte keyschedule, according to AES specification.

        :param seed: array of hex digits [A2, 5D, E4...]
        """
        key = seed
        count = 0
        key_len = len(key)
        while len(key) < 208:
            for i in range(6):
                temp1 = key[key_len - 4:key_len]  # last 4 bytes
                if i == 0:
                    temp1 = key_expansion_core(temp1, count)
                    count += 1
                temp2 = key[key_len - 24:key_len]  # temp2 (last 24 bytes)
                temp2 = temp2[0:4]  # first 4 of last 24 bytes
                result = []
                for j in range(4):
                    result.append(get_XOR(temp1[j], temp2[j]))
                key += result
                key_len = len(key)
                if key_len >= 208:
                    break

        self.key_schedule = [key[i:i + 16] for i in range(0, len(key), 16)]
        self.key_schedule = [''.join(key) for key in self.key_schedule]
        self.key = key
        if self.decrypt:
            self.key_schedule = list(reversed(self.key_schedule))
            self.key = ''.join(self.key_schedule)
        if DEBUG:
            print('Using 192 byte expansion...')
            print(f'Key is {"".join(key)}')
            print(f'Length is {len(key)} bytes')
            print(f'Key schedule is {self.key_schedule}')
            print(f'{len(self.key_schedule)} subkeys')

    def key_expansion_256(self, seed):
        """
        Expands 32 byte key to 256 byte keyschedule, according to AES specification.

        :param seed: array of hex digits [A2, 5D, E4...]
        """
        key = seed
        count = 0
        key_len = len(key)
        while len(key) < 240:
            for i in range(8):
                temp1 = key[key_len - 4:key_len]  # last 4 bytes
                if i == 0:
                    temp1 = key_expansion_core(temp1, count)
                    count += 1
                if i == 4:
                    temp1 = [SBOX[hexstr_to_int(x)] for x in temp1]
                temp2 = key[key_len - 32:key_len]  # temp2 (last 32 bytes)
                temp2 = temp2[0:4]  # first 4 of last 32 bytes
                result = []
                for j in range(4):
                    result.append(get_XOR(temp1[j], temp2[j]))
                key += result
                key_len = len(key)
                if key_len >= 240:
                    break

        self.key_schedule = [key[i:i + 16] for i in range(0, len(key), 16)]
        self.key_schedule = [''.join(key) for key in self.key_schedule]
        self.key = key
        if self.decrypt:
            self.key_schedule = list(reversed(self.key_schedule))
            self.key = ''.join(self.key_schedule)
        if DEBUG:
            print('Using 256 byte expansion...')
            print(f'Key is {"".join(key)}')
            print(f'Length is {len(key)} bytes')
            print(f'Key schedule is {self.key_schedule}')
            print(f'{len(self.key_schedule)} subkeys')

    def is_final_round(self):
        return self.rounds == self.curr_round

    def get_next_key(self):
        """
        Gets next key in key schedule from 0 to num_keys

        :return: next key
        """
        result = self.key_schedule[self.curr_round]
        self.curr_round += 1
        return result

    def get_keyschedule(self):
        return self.key_schedule

    def get_num_rounds(self):
        return self.rounds

    def reset_roundkey_count(self):
        self.curr_round = 0


def key_expansion_core(key: list, i: int) -> str:
    """
    Key Expansion Core according to AES specification.

    :param key: array of hex digits as strings ie [A2, 5D, ..]
    :param i: number of times this function has been called
    """
    key = np.roll(key, -1)  # rotate_left
    key = sub_bytes(key)
    key = wrap(key, 2)

    rcon = 2**i  # calculate x^i
    if i == 8:
        rcon = rcon ^ POLYCONSTANT
    if i == 9:
        rcon = rcon ^ (POLYCONSTANT << 1)

    xor = rcon ^ hexstr_to_int(key[0])  # XOR rcon with the first byte of key
    xor = xor % POLYCONSTANT

    key[0] = hex(xor).split('0x')[1]  # convert ints in key to hex strings
    key[0] = int_to_hexstr(xor)

    return key


def get_XOR(x: str, y: str) -> str:
    """
    Performs an XOR between two bytes as hex strings

    :param x: hex digits as string ie 'A2'
    :param y: x XOR y as string
    :return:
    """
    result = hexstr_to_int(x) ^ hexstr_to_int(y)
    result = int_to_hexstr(result)
    return result


def add_round_key(key: str, text: str) -> str:
    """
    Performs an XOR between each byte of key and text

    :param key: string of bytes
    :param text: string of bytes
    :return: key XOR text
    """
    result = ''
    kbytes = wrap(key, 2)
    tbytes = wrap(text, 2)
    for kbyte, tbyte in zip(kbytes, tbytes):
        result += get_XOR(kbyte, tbyte)
    return result


def hexstr_to_int(hexstr):
    return int('0x' + hexstr, 0)


def int_to_hexstr(number):
    """
    Convert to hex without '0x'
    :param number: number to convert
    :return: hex representation as 2 character string
    """
    result = hex(number).split('0x')[1]  # Convert to string without '0x'
    # Pad with zeros if necessary
    result = '0' * (2 - len(result)) + result
    return result


def sub_bytes(bytes, inverse=False):
    """
    Substitute bytes according to SBOX constant

    :param bytes: string or array of bytes
    :return: string representation of substituted bytes
    """
    if type(bytes) is str:
        bytes = wrap(bytes, 2)

    if inverse:
        result = [SBOX.index(b.upper()) for b in bytes]
        result = [int_to_hexstr(h) for h in result]
    else:
        result = [SBOX[hexstr_to_int(b)] for b in bytes]

    return ''.join(result)
