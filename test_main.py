from unittest import TestCase
from Main import *

VERBOSE = False
DEBUG = False


class TestMain(TestCase):
    def setUp(self) -> None:
        self.ptext = 'A01478BE92570366F1D13C098726DAC53722ddf33b549fb4d84da20855ed45bcA01478BE92570366F1D13C098726DAC' \
                     '53722ddf33b549fb4d84da20855ed45bc'
        self.seed128 = '12476278dbc36bd9dc2cf5716a43b4bb'
        self.seed192 = '9d1e29e03b24b556c16744b9fd5ba204b24b9d1e29e056c1'
        self.seed256 = '18dbc36b277d9d627862dbc36bd9dc2cf5716a43b4bb12c2474cf5716a43b4bb'
        self.aes = AES(debug=DEBUG, verbose=VERBOSE)

    def test_128_ecb(self):
        ctext = '196a288618c68aac46b475c66783929aacb12039b1fc7223e7f438e7ba354e19196a288618c68aac46b475c66783929aacb1' \
                '2039b1fc7223e7f438e7ba354e19'
        self.aes.set_blockmode(BlockMode.ECB)
        result = self.aes.encrypt(self.seed128, self.ptext)
        self.assertEqual(ctext, result)

        ptext = self.aes.decrypt(self.seed128, result)
        self.assertEqual(self.ptext.lower(), ptext.lower())


    def test_128_cbc(self):
        ctext = '196a288618c68aac46b475c66783929a62317e77aed691f908680fc692d1ebec2cbccb9460b6a07bb932f18f65aab89dcf29' \
                '662dd67d683af8904b2e242a2c0c'
        self.aes.set_blockmode(BlockMode.CBC)
        result = self.aes.encrypt(self.seed128, self.ptext)
        self.assertEqual(ctext, result)

        result = self.aes.decrypt(self.seed128, ctext)
        self.assertEqual(self.ptext.lower(), result.lower())


    def test_192_ecb(self):
        ctext = 'b549204a81419dbef1e439ffb20269cf2fdddc147fa2bc2c243776858ccd1e48b549204a81419dbef1e439ffb20269cf2fdd' \
                'dc147fa2bc2c243776858ccd1e48'
        self.aes.set_blockmode(BlockMode.ECB)
        result = self.aes.encrypt(self.seed192, self.ptext)
        self.assertEqual(ctext, result)

        ptext = self.aes.decrypt(self.seed192, result)
        self.assertEqual(self.ptext.lower(), ptext.lower())


    def test_192_cbc(self):
        ctext = 'b549204a81419dbef1e439ffb20269cf3d5bd54dc704374e1ac6a752342450351c7f7d702b3f840bd7bebd2d691019b720c6' \
                'a19be88415123ce03bac7a0ae660'
        self.aes.set_blockmode(BlockMode.CBC)
        result = self.aes.encrypt(self.seed192, self.ptext)
        self.assertEqual(ctext, result)

        ptext = self.aes.decrypt(self.seed192, result)
        self.assertEqual(self.ptext.lower(), ptext.lower())

    def test_256_ecb(self):
        ctext = 'b421b6541081ad44f56ec3fe3eaa7f651c7854304c08047dceb442d5fb4e5a17b421b6541081ad44f56ec3fe3eaa7f651c78' \
                '54304c08047dceb442d5fb4e5a17'
        self.aes.set_blockmode(BlockMode.ECB)
        result = self.aes.encrypt(self.seed256, self.ptext)
        self.assertEqual(ctext, result)

        ptext = self.aes.decrypt(self.seed256, result)
        self.assertEqual(self.ptext.lower(), ptext.lower())

    def test_256_cbc(self):
        ctext = 'b421b6541081ad44f56ec3fe3eaa7f652721a7c9815abd92c8c70467b75fdafeffbd3cad5f5fecdff6665d3ed8af596cbfbc' \
                '555d19136c79035cbd0ba6a98570'
        self.aes.set_blockmode(BlockMode.CBC)
        e_result = self.aes.encrypt(self.seed256, self.ptext)
        self.assertEqual(ctext, e_result)

        d_result = self.aes.decrypt(self.seed256, e_result)
        self.assertEqual(self.ptext.lower(), d_result)

    def test_case_8(self):
        ptext = '0862760c67a0cdc3ede779b9eca00837d5f054da8afb588bce1033373dd9154868ffe11c4338a28a914a834c43d781addad9' \
                'ac8a40a3aa9a8ff4a9ca71b87627ad840e86dfc33b28d06d6eca440d345986885afc85207c8acf6b0b797ea8a4fc4979eaac' \
                'b43f8081a907856765b6151d065a1d96e0121ff46107240b1d89199a'
        seed = 'a5495495d0b61741fa674a77fd7ac231e8d10b6819db40e1'
        ctext_ecb = '1c47ecadaef89648085cdb40949f5fc947774da8a3ee4f881f5164dfb04541de3b8be0b2aa155b15f71f0a9ccec1f716' \
                    '7c8e5866968c22fa19c658da98f4f73bb9f136a63e7b7085cd86e8ccbe15cb7e48ba3f7491c67ac65744e4264bd659c4' \
                    '1aedf3a1f5deb9f07557d69ea7df74c31b61731443cf0b89df41b454720195e8'
        ctext_cbc = '1c47ecadaef89648085cdb40949f5fc9011eadff1d9dbefea1ca6c82c93640040614d2a84e512c4a213ec5b6c7d29834' \
                    'c0762a0daa22298e3cb062828f155f8b7d4678f4bac3e3688ee420b486fbaa1cda87ac811c62e4ad1613222c6ada8ddc' \
                    '861a6f10faaecc3f14cd8271dd66ddb220ac0fda50f47050cac22bd829df6d0d'
        self.aes.set_blockmode(BlockMode.ECB)
        result = self.aes.encrypt(seed, ptext)
        self.assertEqual(ctext_ecb, result)

        self.aes.set_blockmode(BlockMode.CBC)
        result = self.aes.encrypt(seed, ptext)
        self.assertEqual(ctext_cbc, result)

    def test_diff(self):
        """
        pt = 'f921ade849c8aac7b2036636443aed99'
        bits = [bin(hexstr_to_int(b)) for b in pt]
        bits = ''.join(bits)
        bits = ''.join(bits.split('0b'))

        xor = add_round_key('838958fb8c24640f8f23d161f9666329', 'a1823eb7b6d0de74f5f943f0aee6d11e') # XOR
        bits = [bin(hexstr_to_int(b)) for b in xor]
        bits = ''.join(bits)
        bits.count('1') # 61
        """
        p = 'a1b2c3d4e5f6778888776f5e4d3c2b1a'
        c = '4c77e6ea58d64755b8deb26c042c6e5f'
        for byte in wrap(p, 2):


            if byte in wrap(c,2):
                print(byte)


