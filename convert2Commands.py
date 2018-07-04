

f = open('myCodes.commands.txt', 'r')
fout = open('myCodes.commandOrder.txt', 'w')
ftrash = open('trash.txt', 'w')

fout.write('mode, on, swingMoves, swingPosition, fan, xfan, temp, check\n')
lines = f.readlines()

for l in lines:
  mode = eval('0b'+ l[4:7][::-1])
  onOff = int(l[7])
  fan = eval('0b' + l[8:10][::-1])
  swingMoves = int(l[10])
  temp = eval('0b' + l[12:16][::-1])
  xfan = int(l[27])
  swingPosition = eval('0b' + l[41:45][::-1])
  check = eval('0b' + l[69:73][::-1])
  trash = l[0:4] + l[11:12] + l[16:27] + l[28:41] + l[45:69] + l[73:76]
  fout.write('%d, %d, %d, %d, %d, %d, %d, %d\n' % (mode, onOff, swingMoves, swingPosition, fan, xfan, temp, check))
  ftrash.write(trash)
  #ftrash.write('\n')

fout.close()
ftrash.close()


