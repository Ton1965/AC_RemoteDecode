import io
import binascii as ba

f = open('myCodes.txt', 'r')
data = f.readlines()

fout = open('myCodes.hex.txt', 'w')

for l in data:
  offset = 0

  if not '=' in l:
#    fout.write(l)
    continue
  idx = l.find('=') + 1
#  fout.write(l[:idx])
  s = l[idx:]
  s.strip()
  data = ba.a2b_base64(s)
  type = data[offset]
  repeat = data[offset + 1]
  length = data[offset + 2] + data[offset + 3] * 256
  
  record = ba.hexlify(data[offset + 4 : offset + 4 + length])
  for elem in record:
    fout.write('%c' % elem);
  fout.write('\n')


  offset = offset + 4 + length
  if offset >= len(data):
    print("Too long string!")
    continue

fout.close()

