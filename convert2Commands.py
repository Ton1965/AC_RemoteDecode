

f = open('tosot.commands.txt', 'r')
fout = open('tosot.commandOrder.txt', 'w')
ftrash = open('trash.txt', 'w')

fout.write('mode, on, swingMoves, swingPosition, fan, xfan, temp, check\n')
lines = f.readlines()

for l in lines:
  mode = eval('0b'+ l[1:4][::-1])
  onOff = int(l[4])
  fan = eval('0b' + l[5:7][::-1])
  swingMoves = int(l[7])
  temp = eval('0b' + l[9:13][::-1])
  xfan = int(l[24])
  swingPosition = eval('0b' + l[37:41][::-1])
  check = eval('0b' + l[65:69][::-1])
  trash = l[0:1] + l[8:9] + l[13:24] + l[25:37] + l[41:64] + l[69:70]
  fout.write('%d, %d, %d, %d, %d, %d, %d, %d\n' % (mode, onOff, swingMoves, swingPosition, fan, xfan, temp, check))
  ftrash.write(trash)
  ftrash.write('\n')

fout.close()
ftrash.close()


