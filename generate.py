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

Leaders = {'L1' : '000127', 'L2' : '94', 'L3' : '000290', 'U' : '000d05'}
digits = {'0' : '12', '1' : '36'}

def convert2Durations(string):
  currentByte = ''
  converted = ''
  for b in string:
    currentByte = currentByte + b
    if currentByte in digits:
      converted = converted + '12' + digits[currentByte]
    elif currentByte in Leaders:
      converted = converted + Leaders[currentByte]
    elif currentByte == 'L':
      continue
    currentByte = ''
    
  return converted

def process(command):
  command = convert2Durations(command)
  hexCommand = ba.unhexlify(command)
  #prepend command type (always 38), repeat count and data length
  length = len(hexCommand)
  header = bytes([38, 0, length % 256, length // 256])
  hexCommand = header + hexCommand
  command = str(ba.b2a_base64(hexCommand, newline = False))

  return command[1:]


commandTemplate = 'L1L210010010010100000000011100001010010L310000000010001000000000000001111U'

on_off = {'on' : 1, 'off' : 0}
on_off_byte = 7

mode = {'heat' : 4, 'cool' : 1}
mode_byte = [4, 7]

fan = {'low' : 1, 'medium' : 2, 'high' : 3, 'auto' : 0}
fan_byte = [8, 10]

temp_low = 16
temp_high = 30
temp_byte = [12, 16]

checksum_byte = [69, 73]

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
