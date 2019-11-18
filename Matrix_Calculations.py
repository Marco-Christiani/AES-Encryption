import numpy as np
from textwrap import wrap
from Key_Calculations import hexstr_to_int, int_to_hexstr

POLYCONSTANT = 0b100011011
ARR = np.array([[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]])
ARR_INV = np.array([[14, 11, 13, 9], [9, 14, 11, 13], [13, 9, 14, 11],
                    [11, 13, 9, 14]])


class Matrix:
    def __init__(self, data: str):
        self.matrix = np.empty([4, 4], dtype='U2')
        i = 0
        data = wrap(data, 2)
        for byte in data:
            self.matrix[i % 4][i // 4] = byte
            i += 1

    def shift_rows(self, inverse=False):
        i = 0
        for row in self.matrix:
            if inverse:
                self.matrix[i] = np.roll(row, i)
            else:
                self.matrix[i] = np.roll(row, -i)
            i += 1

    def mix_columns(self, inverse=False):
        MIX_ARR = ARR
        if inverse:
            MIX_ARR = ARR_INV
        matrix_as_num = np.zeros([4, 4])
        i = 0
        for row in self.matrix:
            matrix_as_num[i, :] = [hexstr_to_int(x) for x in row]
            i += 1

        # Multiply each column of matrix with mix columns matrix
        temp_mat = np.zeros([4, 4])
        for i in range(4):
            col = matrix_as_num[:, i]
            # For each column of mix matrix, multiply by element in current matrix column
            for j in range(4):
                elem = col[j]
                for k in range(4):
                    temp_mat[k, j] = mult(elem,
                                          MIX_ARR[k, j])  # ^ POLYCONSTANT


            print(temp_mat)
            # Add columns of temp_mat together
            result_vec = np.zeros(4)
            result_vec_str = np.empty(4, dtype='U2')  # column of final matrix
            for p in range(4):
                row = temp_mat[p, :]
                for elem in row:
                    result_vec[p] = int(elem) ^ int(result_vec[p])  # sum all elements in row
                temp = mod_p(result_vec[p])
                result_vec_str[p] = int_to_hexstr(temp)  # Convert to hex without 0x
            # print('Before mod:', result_vec)
            # print('After mod:', [mod_p(x) for x in result_vec])
            # self.matrix[i, :] = result_vec_str
            self.matrix[:, i] = result_vec_str

    def inv_mix_columns(self):
        matrix_as_num = np.zeros([4, 4])
        i = 0
        for row in self.matrix:
            matrix_as_num[i, :] = [hexstr_to_int(x) for x in row]
            i += 1
        # Multiply each column of matrix with mix columns matrix
        result = np.zeros([4, 4])
        for i in range(4):
            col = matrix_as_num[:, i]
            # Mix current col by multiplying by inverse mix array
            result[0, i] = mult(col[0], ARR_INV[0, 0]) ^ mult(col[0], ARR_INV[0, 1]) \
                           ^ mult(col[0], ARR_INV[0, 2]) ^ mult(col[0], ARR_INV[0, 3])
            result[1, i] = mult(col[1], ARR_INV[1, 0]) ^ mult(col[1], ARR_INV[1, 1]) \
                           ^ mult(col[1], ARR_INV[1, 2]) ^ mult(col[1], ARR_INV[1, 3])
            result[2, i] = mult(col[2], ARR_INV[2, 0]) ^ mult(col[2], ARR_INV[2, 1]) \
                           ^ mult(col[2], ARR_INV[2, 2]) ^ mult(col[2], ARR_INV[2, 3])
            result[3, i] = mult(col[3], ARR_INV[3, 0]) ^ mult(col[3], ARR_INV[3, 1]) \
                           ^ mult(col[3], ARR_INV[3, 2]) ^ mult(col[3], ARR_INV[3, 3])
            self.matrix[0, i] = int_to_hexstr(int(result[0, i]))
            self.matrix[1, i] = int_to_hexstr(int(result[1, i]))
            self.matrix[2, i] = int_to_hexstr(int(result[2, i]))
            self.matrix[3, i] = int_to_hexstr(int(result[3, i]))
            print(result)

    def flatten_cols(self):
        return ''.join(self.matrix.flatten())

    def flatten_rows(self):
        return ''.join(self.matrix.flatten(order='F'))

    def __str__(self):
        return np.array2string(self.matrix)


def mult(a, b):
    a = int(a)
    b = int(b)

    if b == 1:
        result = a
    elif b == 2:
        result = a << 1
    elif b == 3:
        result = (a << 1) ^ a
    elif b == 9:
        result = (a << 3) ^ a
    elif b == 11:
        # result = ((a << 2) ^ a) << 1
        result = mod_p(a << 3) ^ mod_p((a << 1) ^ a)  # a*8 + a*3
    elif b == 13:
        # result = (((a << 1) ^ a) << 2) ^ a
        result = mod_p(a << 3) ^ mod_p((a << 1) ^ a) ^ (a << 1)  # a*8 + a*3 +a*2
    elif b == 14:
        # result = ((((a << 1) ^ a) << 1) ^ a) << 1
        result = (a << 3) ^ ((a << 1) ^ a) ^ ((a << 1) ^ a)  # a*8 + a*3 +a*3
    else:
        return Exception
    # return mod_p(result)
    return result


def mod_p(number):
    bit_rep = bin(int(number))
    num_bits = len([c for c in bit_rep.split('0b')[1]])
    if num_bits > 8:
        modconstant = POLYCONSTANT << (num_bits - 9
                                       )  # Left align POLYCONSTANT with number
        return int(number) ^ modconstant
    return int(number)
