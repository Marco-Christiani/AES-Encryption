from enum import Enum
from textwrap import wrap


class BlockMode(Enum):
    ECB = 1
    CBC = 2


class ByteMode(Enum):
    b16 = 16
    b24 = 24
    b32 = 32


class BlockStream:
    def __init__(self, textstream, block_mode: BlockMode, byte_mode: ByteMode):
        self.textstream = textstream
        self.byte_mode = byte_mode.value
        self.blockstream = []
        self.curr_block = 0
        if block_mode is BlockMode.ECB:
            self.parse_ecb_blocks()
        elif block_mode is BlockMode.CBC:
            self.parse_cbc_blocks()

    def parse_ecb_blocks(self):
        bytes = wrap(self.textstream, 2)
        full_blocks = [bytes[i:i+self.byte_mode] for i in range(0, len(bytes), self.byte_mode)]
        self.blockstream = full_blocks

        partial_block_size = len(bytes) % self.byte_mode
        partial_block_start = len(bytes) - partial_block_size
        if partial_block_size > 0:
            partial_block = bytes[partial_block_start:len(bytes)+partial_block_size]
            padded_block = []
            # Pad final last block with 0's
            for i in range(self.byte_mode-partial_block_size):
                padded_block.append(0)
            padded_block += partial_block
            self.blockstream = full_blocks+padded_block

    def parse_cbc_blocks(self):
        return NotImplemented

    def get_next_block(self):
        block = self.blockstream[self.curr_block]
        self.curr_block += 1
        return ''.join(block)

    def get_block_num(self):
        return self.curr_block

    def is_empty(self):
        return len(self.blockstream) == self.curr_block


