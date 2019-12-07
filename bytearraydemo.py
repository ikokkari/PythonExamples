# Strings contain unicode characters somehow internally stored. They
# can be extracted to a byte array with given Unicode encoding. This
# byte array can be processed with byte array operations such as
# checksums and compressions, not caring where these bytes came from.

s = "This will be turned into an array of bytes."

print(f"Length of s is {len(s)}.")
s2 = s.encode('utf-8')
print(f"Length of s2 bytes is {len(s2)}.")
s3 = s2.decode('utf-8')
print(f"Decoding bytes gives the string <{s3}>.")

import zlib
from hashlib import sha256

print(f"Adler checksum of string s: {zlib.adler32(s2)}")
print(f"CRC32 checksum of string s: {zlib.crc32(s2)}")

with open('warandpeace.txt', encoding="utf-8") as wap:
    s = " ".join(list(wap))   # this will be a really long string
print(f"'War and Peace' contains {len(s)} characters.") 

sb = s.encode('utf-8')
print(f"Encoded as byte array using utf-8, this gives {len(sb)} bytes.")

hsh = sha256()
hsh.update(sb)
print(f"SHA 256 checksum is: <{hsh.hexdigest()}>")

sbc = zlib.compress(sb)
print(f"Compressed, it has only {len(sbc)} bytes.")

sd = zlib.decompress(sbc)
assert sd == sb

sbd = sb.decode('utf-8')
print(f"Decompressed 'War and Peace' again has {len(sbd)} characters.")
assert s == sbd
