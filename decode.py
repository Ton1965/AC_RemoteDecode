import binascii as ba

fin = open('tosot.hex', 'r')
commands = fin.readlines()

fout = open('tosot.commands.txt', 'w')
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
      buffer += 'A'
    else:
      if duration >= 0x85 and duration <= 0x9c:
        buffer += 'B'
      else:
        if duration >= 0x0280 and duration <= 0x29a:
          buffer += 'C'
        else:
          if duration >= 0x0e and duration <= 0x1d:
            buffer += '0'
          else:
            if duration >= 0x30 and duration <= 0x3a:
              buffer += '1'
            else:
              if duration >= 0xd00 and duration <= 0xd0a:
                buffer += 'D'
              else:
                buffer += 'U'
    if buffer == 'AB' or buffer == '0C' or buffer == '0D' or buffer == '01' or buffer == '00':
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
