import os
from PIL import Image


def group(lst, n):
	for i in range(0, len(lst), n):
		val = lst[i:i+n]
		if len(val) == n:
			yield tuple(val)

fileList = []			
for filename in os.listdir("."):    
    if filename.endswith('.bc'):
        fileList.append(filename)

for currentFile in fileList:
    x = 0
    numBytes = 0
    out = []
    with open(currentFile) as f:
        byte = f.read(1)
        while byte != "":
            x += 1
            # Do stuff with byte.
            if x == 22:
                sizeData = '{:02x}'.format(ord(byte))
                if sizeData == '32':
                    picSize = 512
                elif sizeData == '31':
                    picSize = 256
                else:
                    picSize = 128
                numBytes = picSize*picSize*2+48    
        
            if x > 49 and x < numBytes:
                d = '{:02x}'.format(ord(byte))
                out.append(int("0x%s%s" % (d[0],d[0]), 16))
                out.append(int("0x%s%s" % (d[1],d[1]), 16))
            byte = f.read(1)
			
    newimage = Image.new('RGBA', (picSize, picSize))  # type, size
    newimage.putdata(list(group(out, 4)))
    pngName = currentFile[:len(currentFile)-2] + "png"
    newimage.save(pngName)
