import binascii as ba

fin = open('result.txt', 'r')
commands = fin.readlines()

fout = open('commands.txt', 'w')
for l in commands:
  current = 0
  buffer = ''
  while True:
    duration = l[current : current + 2]
    current += 2
    if duration == '00':
      duration = l[current : current + 4]
      current += 4
    if duration == '0127':
      buffer = 'L1'
    else:
      if duration == '94':
        buffer = 'L2'
      else:
        if duration == '0290':
          buffer = 'L3'
        else:
          if duration == '12':
            buffer = buffer + '0'
          else:
            if duration == '36':
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
