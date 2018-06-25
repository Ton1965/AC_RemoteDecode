import io
import binascii as ba

f = io.FileIO('32194283', 'rb')
data = f.readall()

fout = open('result.txt', 'w')

offset = 108
for i in range(501):
  type = data[offset]
  repeat = data[offset + 1]
  length = data[offset + 2] + data[offset + 3] * 256
  
  record = ba.hexlify(data[offset + 4 : offset + 4 + length])
  for elem in record:
    fout.write('%c' % elem);

  fout.write('\n')
  offset += 960

fout.close()
