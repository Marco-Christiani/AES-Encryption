from textwrap import wrap


class BlockStream:
    def __init__(self, textstream, decrypt: bool = False):
        self.textstream = textstream
        self.blockstream = []
        self.curr_block = 0
        self.blocksize = 16  # 16 bytes
        self.parse_blocks(decrypt)

    def parse_blocks(self, decrypt=False):
        bytes = wrap(self.textstream, 2)
        full_blocks = [
            bytes[i:i + self.blocksize]
            for i in range(0, len(bytes), self.blocksize)
        ]
        self.blockstream = full_blocks
        # ---------------------- Padding ----------------------------
        partial_block_size = len(bytes) % self.blocksize
        partial_block_start = len(bytes) - partial_block_size
        if partial_block_size > 0:
            partial_block = bytes[partial_block_start:len(bytes) +
                                  partial_block_size]
            padded_block = []
            # Pad final last block with 0's
            for i in range(self.blocksize - partial_block_size):
                padded_block.append(0)
            padded_block += partial_block
            self.blockstream = full_blocks + padded_block
        # -----------------------------------------------------------
        if decrypt:
            self.blockstream = list(reversed(self.blockstream))

    def get_next_block(self):
        block = self.blockstream[self.curr_block]
        self.curr_block += 1
        return ''.join(block)

    def get_prev_block(self):
        block = self.blockstream[self.curr_block-1]
        return ''.join(block)

    def get_block_num(self):
        return self.curr_block

    def is_empty(self):
        return len(self.blockstream) == self.curr_block
