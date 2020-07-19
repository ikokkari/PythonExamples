# Strings contain unicode characters somehow internally stored. They
# can be extracted to a byte array with given Unicode encoding. This
# byte array can be processed with byte array operations such as
# checksums and compressions, not caring where these bytes came from.

import zlib
from hashlib import sha256

s = "This will be turned into an array of bytes \U0001F603."

print(f"Length of s is {len(s)}.")
sb = s.encode('utf-8')
print(f"Length of bytes is {len(sb)}.")
s = sb.decode('utf-8')
print(f"Decoding bytes gives the string {repr(s)}.")

print(f"Adler checksum of string s: {zlib.adler32(sb)}")
print(f"CRC32 checksum of string s: {zlib.crc32(sb)}")

with open('warandpeace.txt', encoding="utf-8") as wap:
    s = " ".join(list(wap))   # this will be a really long string
print(f"'War and Peace' contains {len(s)} characters.")

sb = s.encode('utf-8')
print(f"Encoded as byte array using utf-8, this gives {len(sb)} bytes.")

chk = sha256()  # Cryptographic checksum, a bit slower to compute
chk.update(sb)
print(f"SHA 256 checksum is: <{chk.hexdigest()}>")

sbc = zlib.compress(sb)
print(f"Compressed, it has only {len(sbc)} bytes.")

sd = zlib.decompress(sbc)
assert sd == sb     # Decompression restores the original data.

sbd = sb.decode('utf-8')
print(f"Decompressed 'War and Peace' again has {len(sbd)} characters.")
assert s == sbd
