import argparse
import pyDes
import intelhex
import struct
import hashlib
import time
from hashlib import sha256




class FirmwarePacker:
    def __init__(self, version, key = '', iv = '', block_size = 512):
        self.ih = intelhex.IntelHex()
        self.ih.padding = 0xFF
        self.key = key
        self.iv = iv
        self.version = version
        self.block_size = block_size
        self.blocks = {}
        self.version_binary_str = self.parse_version(self.version)
        self.packed_buffer = None
        self.packed_hash = None

    def load_from_file(self, file):
        self.ih.loadhex(file)
        min_addr = self.ih.minaddr()
        max_addr = self.ih.maxaddr()

        current_addr = min_addr

        while current_addr < max_addr:
            page_start = current_addr
            page_end = current_addr + self.block_size
            current_addr = page_end
            #page = self.ih[page_start:page_end]
            #page_binary_str = page.tobinstr()
            page = self.ih.tobinstr(start=page_start, size=512)
            page_binary_str = page
            offset = page_start - 0x10000
            self.blocks[offset] = page_binary_str

    def write_to_file(self, file):
        f = open(file, 'wb')
        buffer = self.pack()
        f.write(buffer)

    def calculate_checksum(self, content, length = 8):
        sha256 = hashlib.sha256()
        sha256.update(content)
        checksum = sha256.digest()[:length]
        return checksum

    def encrypt(self, content):
        encryptor = pyDes.triple_des(self.key, mode=pyDes.CBC, IV=self.iv)
        encrypted_content = encryptor.encrypt(content)
        return encrypted_content

    def parse_version(self, version):
        version_numbers = list(map(lambda x : int(x), version.strip().split(".")))
        if len(version_numbers) != 4:
            return None

        major = version_numbers[0]
        minor = version_numbers[1]
        release = version_numbers[2]
        build = version_numbers[3]

        version_str = '%d%d%d%05X' % (major, minor, release, build)
        version_binary_str = bytearray.fromhex(version_str)
        return version_binary_str

    def pack(self):
        buffer = bytearray()
        for address in self.blocks:
            content = self.blocks[address]
            block_buffer = self.pack_block(address, content)
            buffer += block_buffer
        sh = hashlib.sha256()
        sh.update(buffer)
        self.packed_hash = sh.hexdigest()
        print("Pack hash: " + self.packed_hash)
        header = self.pack_header()
        self.packed_buffer = header + buffer
        return self.packed_buffer

    def pack_header(self):
        header = self.version_binary_str
        sha256 = hashlib.sha256()
        sha256.update(self.version_binary_str)
        checksum = sha256.digest()[:4]

        header = header + checksum
        header = header + b'\x00' * (32 - len(header))

        packhash =  bytearray.fromhex(self.packed_hash)
        header = header + packhash
        
        # signature part
        header = header + b'\x00' * 64
        return header

    def pack_block(self, address, content):
        #address = address & 0xFFFF
        buffer = struct.pack('>LL%ds' % len(content), address, 0, content)

        encrypted_buffer = self.encrypt(buffer)
        # print("%08X" % address, buffer.hex(' '), "\n---\n", encrypted_buffer.hex(' '))
        encrypted_buffer_with_checksum = encrypted_buffer + self.calculate_checksum(encrypted_buffer)
        return encrypted_buffer_with_checksum

def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Input hex file, like mason_app.hex", type=str, default="mason_app.hex", required=False)
    parser.add_argument("-i", "--iv", help="3DES CBC initial vection", type=str, default="DE59B68A", required=False)
    parser.add_argument("-k", "--key", help="3DES key, length must be 16 or 24 byte", type=str, default="C6E6B09E45227FCD80BF497C", required=False)
    parser.add_argument("-t", "--target-version", help="Target version, format is X.X.X.XXXXX, 1.0.0.000000", default="1.0.0.000000", required=False)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_argument()
    firmware_packer = FirmwarePacker(args.target_version, args.key, args.iv)
    print('Loading file from %s ...' % args.file)
    firmware_packer.load_from_file(args.file)
    current = int(time.time());
    output = f"./artifacts/unsigned_firmware_{current}.bin"
    print('Packing and write to file %s ...' % output)
    firmware_packer.write_to_file(output)
    print('Done.')
    exit(0)