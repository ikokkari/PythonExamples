# Strings a sequences of unicode characters, and the encoding
# used internally to store a string object does not show on the
# outside. The contents of each string can be extracted into a
# byte array in desired Unicode encoding. This byte array can
# be processed further with operations such as checksums and
# compressions, without a care where these bytes originally
# came from and what they were considered to represent there.

import zlib
from hashlib import sha256

s = "This will be turned into an array of bytes \U0001F603, man!"

print(f"Length of s is {len(s)} characters.")
sb = s.encode('utf-8')
print(f"Length of sb is {len(sb)} bytes.")
s = sb.decode('utf-8')
print(f"Decoding sb gives back the string:\n{repr(s)}.")

print(f"Adler checksum of string is {zlib.adler32(sb)}.")
print(f"CRC32 checksum of string is {zlib.crc32(sb)}.")

with open('warandpeace.txt', encoding="utf-8") as wap:
    s = " ".join(list(wap))   # This will be one long string.

print(f"'War and Peace' contains {len(s)} characters.")

sb = s.encode('utf-8')
print(f"Encoded as byte array using utf-8, this gives {len(sb)} bytes.")

chk = sha256()  # Cryptographic checksum, a bit slower to compute.
chk.update(sb)
print(f"Its SHA-256 checksum is:\n{chk.hexdigest()}")

# Natural language contains so much redundancy and uses so few of
# the available charactes and words that it compresses massively.
sbc = zlib.compress(sb)
print(f"Compressed, it needs only {len(sbc)} bytes.")

sd = zlib.decompress(sbc)
assert sd == sb     # Decompression brings back the original data.

sbd = sb.decode('utf-8')
print(f"Decompressed 'War and Peace' has {len(sbd)} characters.")
assert s == sbd     # The original data produces an equal string.
