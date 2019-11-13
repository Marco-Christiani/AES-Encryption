from unittest import TestCase
from Main import *

VERBOSE = True


class TestMain(TestCase):

    def test_encrypt_128(self):
        seed = '12476278dbc36bd9dc2cf5716a43b4bb'
        ptext = 'A01478BE92570366F1D13C098726DAC53722ddf33b549fb4d84da20855ed45bc'
        ctext = '196a288618c68aac46b475c66783929aacb12039b1fc7223e7f438e7ba354e19'
        result = encrypt(seed, ptext, verbose=VERBOSE)
        self.assertEqual(ctext, result)

    def test_decrypt_128(self):
        seed = '12476278dbc36bd9dc2cf5716a43b4bb'
        ctext = '196a288618c68aac46b475c66783929aacb12039b1fc7223e7f438e7ba354e19'
        ptext = 'A01478BE92570366F1D13C098726DAC53722ddf33b549fb4d84da20855ed45bc'

        result = decrypt(seed, ctext, verbose=VERBOSE)
        self.assertEqual(ptext, result)

    def test_encrypt_192(self):
        seed = '9d1e29e03b24b556c16744b9fd5ba204b24b9d1e29e056c1'

        ptext = 'A01433b54978BE925703666F1D13C098726DAC56F1D13C098726DAC53722ddf33b549fb4A01478BE9257033722ddffb4'
        ctext = '566b9baab48dec6d53a34306bf54643d764776da4b6ac073d09a57ba55ee1b0d8a06f09a0dea5542e336fdd88de64a0d'
        result = encrypt(seed, ptext, verbose=VERBOSE)
        self.assertEqual(ctext, result)

    # def test_padding(self):
    #     # ctext = 'b549204a81419dbef1e439ffb20269cf2fdddc147fa2bc2c243776858ccd1e48'
    #     # ptext = 'A01478BE92570366F1D13C098726DAC53722ddf33b549fb4d84da20855ed45bc'