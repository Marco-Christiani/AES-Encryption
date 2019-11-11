from unittest import TestCase
from Main import *

VERBOSE = True


class TestMain(TestCase):
    def setUp(self) -> None:
        self.seed = '12476278dbc36bd9dc2cf5716a43b4bb'
        self.plaintext = 'A01478BE92570366F1D13C098726DAC53722ddf33b549fb4d84da20855ed45bc'
        self.ciphertext = '196a288618c68aac46b475c66783929aacb12039b1fc7223e7f438e7ba354e19'

    def test_encrypt(self):
        ciphertext = encrypt(self.seed, self.plaintext, verbose=VERBOSE)
        self.assertEqual(self.ciphertext, ciphertext)

    def test_decrypt(self):
        plaintext = decrypt(self.seed, self.ciphertext, verbose=VERBOSE)
        self.assertEqual(self.plaintext, plaintext)
