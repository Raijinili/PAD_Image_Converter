import os
import glob
from PIL import Image


def group(lst, n):
    for i in range(0, len(lst), n):
        val = lst[i:i+n]
        if len(val) == n:
            yield tuple(val)



def make_image(f):
        
        # byte = f.read(1)
        header = f.read(48)
        
        sizeData = header[21]
        
        if sizeData == 0x32:
            picSize = 512
        elif sizeData == 0x31:
            picSize = 256
        else:
            picSize = 128
        
        numBytes = picSize*picSize*2
        
        # Should be small enough to fit in memory.
        image = f.read(numBytes)
        
    out = []
    for rg, ba in group(image, 2):
        r, g = divmod(byte, 16)
        b, a = divmod(byte, 16)
        
        #!TODO: Check order.
        out.append((r, g, b, a))
    
    newimage = Image.new('RGBA', (picSize, picSize))  # type, size
    newimage.putdata(out)
    
    return newimage

for currentFile in glob.iglob('./*.bc'):
    with open(currentFile, 'rb') as f:
        newimage = make_image(f)
    pngName = currentFile[:-2] + "png"
    newimage.save(pngName)
