import numpy as np
from textwrap import wrap
from Key_Calculations import hexstr_to_int, int_to_hexstr

POLYCONSTANT = 0b100011011
ARR = np.array([[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]])
ARR_INV = np.array([[14, 11, 13,  9], [9, 14, 11, 13], [13,  9, 14, 11], [11, 13,  9, 14]])

class Matrix:
    def __init__(self, data: str):
        self.matrix = np.empty([4, 4], dtype='U2')
        i = 0
        data = wrap(data, 2)
        for byte in data:
            self.matrix[i % 4][i // 4] = byte
            i += 1

    def shift_rows(self):
        i = 0
        for row in self.matrix:
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

            # Add columns of temp_mat together
            result_vec = np.zeros(4)
            result_vec_str = np.empty(4, dtype='U2')  # column of final matrix
            for p in range(4):
                row = temp_mat[p, :]
                for elem in row:
                    result_vec[p] = int(elem) ^ int(
                        result_vec[p]
                    )  # ^ POLYCONSTANT  # sum all elements in row
                temp = mod_p(result_vec[p])
                result_vec_str[p] = int_to_hexstr(
                    temp)  # Convert to hex without 0x
            self.matrix[i, :] = result_vec_str

    def flatten_cols(self):
        return ''.join(self.matrix.flatten())

    def flatten_rows(self):
        return ''.join(self.matrix.flatten(order='F'))

    def __str__(self):
        return ''.join(self.matrix.flatten(order='F'))


def mult(a, b):
    a = int(a)
    b = int(b)
    if b == 1:
        return a
    if b == 2:
        return a << 1
    if b == 3:
        return (a << 1) ^ a
    else:
        raise Exception


def mod_p(number):
    bit_rep = bin(int(number))
    num_bits = len([c for c in bit_rep.split('0b')[1]])
    if num_bits > 8:
        modconstant = POLYCONSTANT << (num_bits - 9
                                       )  # Left align POLYCONSTANT with number
        return int(number) ^ modconstant
    return int(number)
