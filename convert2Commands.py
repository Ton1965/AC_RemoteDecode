

f = open('commands.txt', 'r')
fout = open('commandOrder.txt', 'w')
ftrash = open('trash.txt', 'w')

lines = f.readlines()

for l in lines:
  mode = eval('0b'+ l[4:7][::-1])
  onOff = int(l[7])
  fan = eval('0b' + l[8:10][::-1])
  temp = eval('0b' + l[12:16][::-1])
  strange = eval('0b' + l[69:73][::-1])
  trash = l[0:4] + l[10:12] + l[16:69] + l[73:76]
  fout.write('%d, %d, %d, %d, %d\n' % (mode, onOff, fan, temp, strange))
  ftrash.write(trash)
  ftrash.write('\n')

fout.close()
ftrash.close()


