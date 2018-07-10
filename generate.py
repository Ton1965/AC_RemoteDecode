import binascii as ba

def setByte(string, location, newByte):
  if len(newByte) != 1:
    print("Bad arguments to setByte!\n")
    return ''

  return string[:location] + newByte + string[location + 1:]

def setBytes(string, location, newBytes):
  if len(newBytes) != location[1] - location[0]:
    print("Bad arguments to setBytes!\n")
    return ''

  return string[:location[0]] + newBytes + string[location[1]:]

durations = {'B' : '00012794', 'C' : '12000290', 'D' : '12000d05', '0' : '1212', '1' : '1236'}

def convert2Durations(string):
  currentByte = ''
  converted = ''
  for b in string:
    if b in durations:
      converted = converted + durations[b]
    else:
      print("Bad symbol %d in generated line!" % b)
    
  return converted

def process(command):
  command = convert2Durations(command)
  hexCommand = ba.unhexlify(command)
  #prepend command type (always 38), repeat count and data length
  length = len(hexCommand)
  header = bytes([38, 0, length % 256, length // 256])
  length1 = ((length // 8) + 1) * 8
  padLength = length1 - length
  pad = bytearray(b'\0') * padLength
  hexCommand = header + hexCommand + pad
  command = str(ba.b2a_base64(hexCommand, newline = False))

  return command[2:len(command) - 1]


commandTemplate = 'B10010010010100000000011100001010010C10000000010001000000000000001111D'

on_off = {'on' : 1, 'off' : 0}
on_off_byte = 4

mode = {'heat' : 4, 'cool' : 1}
mode_byte = [1, 4]

fan = {'low' : 1, 'medium' : 2, 'high' : 3, 'auto' : 0}
fan_byte = [5, 7]

temp_low = 16
temp_high = 30
temp_byte = [9, 13]

checksum_byte = [65, 69]

fout = open("tosot.ini", "w")

command = commandTemplate
command = setByte(command, on_off_byte, str(on_off['off']))
modestring = "{0:03b}".format(mode['cool'])[::-1]
command = setBytes(command, mode_byte, modestring)
fanstring = "{0:02b}".format(0)[::-1]
command = setBytes(command, fan_byte, fanstring)
tempstring = "{0:04b}".format(10)[::-1]
command = setBytes(command, temp_byte, tempstring)
checksum = (1 + 8 * 0 + 10 + 12) % 16
checksumstring = "{0:04b}".format(checksum)[::-1]
command = setBytes(command, checksum_byte, checksumstring)
command = process(command)

fout.write('[off]\noff_command = ' + command + '\n')

fout.write('[idle]\nidle_commnad = ' + command + '\n')

for m in mode:
  fout.write("\n[" + m + "]\n")
  for f in fan:
    fout.write('\n')
    fprefix = f + "_"
    for temp in range(16, 31):
      label = fprefix + str(temp)
      fout.write(label + " = ")
      command = commandTemplate
      modestring = "{0:03b}".format(mode[m])[::-1]
      command = setBytes(command, mode_byte, modestring)
      command = setByte(command, on_off_byte, str(on_off['on']))
      fanstring = "{0:02b}".format(fan[f])[::-1]
      command = setBytes(command, fan_byte, fanstring)
      tempstring = "{0:04b}".format(temp - 16)[::-1]
      command = setBytes(command, temp_byte, tempstring)
      checksum = (mode[m] + 8 * on_off['on'] + (temp - 16) + 12) % 16
      checksumstring = "{0:04b}".format(checksum)[::-1]
      command = setBytes(command, checksum_byte, checksumstring)
      command = process(command)
      fout.write(command + '\n')


fout.close()
