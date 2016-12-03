from PIL import Image
from midiutil.MidiFile import MIDIFile

def rgbtohsl(r,g,b):
    r1 = r/255
    g1 = g/255
    b1 = b/255

    cmax = max(r1,g1,b1)
    cmin = min(r1,g1,b1)
    
    d = cmax - cmin

    l = (cmax + cmin)/2

    if d == 0:
        h = 0
        s = 0
    else:
        if cmax == r1:
            h = 60 * (((g1-b1)/d)%6)
        elif cmax == g1:
            h = 60 * (((b1-r1)/d)+2)
        elif cmax == b1:
            h = 60 * (((r1-g1)/2)+4)
        s = d/(1-abs(2*l - 1))
    return (h,s,l)

def makenote(h,s,l):
    pitch = int((h * 127) // 360)
    vol = int((s + l)/2 * 127)
    return(pitch, vol)

def notevollst(lst):
    """
    parameter lst must be list of (h,s,l) tuples
    returns tuple([notelist], [vollist])
    """
    notelst = []
    vollst = []
    for item in lst:
        x = makenote(item[0],item[1],item[2])
        notelst.append(x[0])
        vollst.append(x[1])
    return(notelst, vollst)

def makemidifile(notelst, vollst, name):
    track = 0
    channel = 0
    time = 0
    duration = 1
    tempo = 360
    mymidi = MIDIFile(1, adjust_origin=False)
    mymidi.addTempo(track, time, tempo)
    for i in range(len(notelst)):
        print(i / len(notelst))
        mymidi.addNote(track, channel, notelst[i], time, duration, vollst[i])
        time += 1
    with open(name, "wb") as output_file:
        mymidi.writeFile(output_file)
        
def getimagedata(filepath):
    im = Image.open(filepath)
    pix = im.load()
    rgblst = []
    ydivs = int(im.size[1]/30)
    #print("ydivs: ", ydivs)
    xdivs = int(im.size[0]/30)
    #print("xdivs: ", xdivs)
    for y in range(im.size[1]):
        #print(y%ydivs)
        if y%ydivs == 0:
            #print("Line")
            for x in range(im.size[0]):
                #print(x%xdivs)
                if x%xdivs == 0:
                    rgblst.append(pix[x,y])
    return(rgblst)

def rgblsttohsllst(lst):
    """
    parameter lst must be (r,g,b) tuples
    return list of (h, s, l) tuples
    """
    hsl = []
    for item in lst:
        hsl.append(rgbtohsl(item[0],item[1],item[2]))
    return hsl


    
a = getimagedata('cat.jpg')
print("got")
a = rgblsttohsllst(a)
print("converted to hsl")
b = notevollst(a)
print("converted to notes/vol")
makemidifile(b[0],b[1],'cat.mid')
    
