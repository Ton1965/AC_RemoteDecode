import binascii as ba

fin = open('myCodes.hex.txt', 'r')
commands = fin.readlines()

fout = open('myCodes.commands.txt', 'w')
for l in commands:
  l = l[:len(l) - 1]
  current = 0
  buffer = ''
  while True:
    duration = int('0x' + l[current : current + 2], base = 16)
    current += 2
    if duration == 0:
      duration = int('0x' + l[current : current + 4], base = 16)
      current += 4
    if duration >= 0x0120 and duration <= 0x0130:
      buffer = 'L1'
    else:
      if duration >= 0x85 and duration <= 0x9c:
        buffer = 'L2'
      else:
        if duration >= 0x0280 and duration <= 0x29a:
          buffer = 'L3'
        else:
          if duration >= 0x0e and duration <= 0x1d:
            buffer = buffer + '0'
          else:
            if duration >= 0x30 and duration <= 0x3a:
              buffer = buffer + '1'
            else:
              buffer = 'U'
    if buffer == 'L1' or buffer == 'L2' or buffer == 'L3' or buffer == 'U':
      fout.write(buffer)
      buffer = ''
    if buffer == '00' or buffer == '01':
      fout.write(buffer[1])
      buffer = ''
    if len(buffer) > 2:
      print('Unexpected file format!')
      fout.write(buffer)
      buffer = ''
    
    if current >= len(l):
      fout.write(buffer)
      fout.write('\n')
      break
	
fout.close()
