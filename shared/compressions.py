#COMPRESS DECOMPRESS

import zlib

def compress_data(data):
    return zlib.compress(data)

def decompress_data(data):
    return zlib.decompress(data)
