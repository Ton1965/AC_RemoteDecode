import io
import binascii as ba

f = io.FileIO('32194283', 'rb')
data = f.readall()
res = ba.hexlify(data[108:])

fout = io.FileIO('result.txt', 'w')
fout.write(res)

fout.close()
