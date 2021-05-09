import sys
import mido
import music21

filepath=sys.argv[1]
m=music21.midi.translate.midiFilePathToStream(filepath)
k=m.analyze("key")
print("此midi文件的调性：",k)
ismajor=(k.type=='major')
print("移到平行{}调".format({True:"大",False:'小'}[not ismajor]))
tonemid=k.getTonic().midi

mid=mido.MidiFile(filepath)
deltadict={}

if(ismajor):
    moveset={4,9,11}
    deltadict={(i+tonemid)%12:-1 for i in moveset}
    pass
else:
    moveset={3,8,10}
    deltadict={(i+tonemid)%12:1 for i in moveset}
    pass
for tr in mid.tracks:
    for msg in tr:
        if hasattr(msg,"note"):
            #print(msg.note,deltadict.get(msg.note%12,0))
            #print(msg)
            msg.note+=deltadict.get(msg.note%12,0)
            #print(msg)
            #input()
#for msg in mid:
#    if hasattr(msg,"note"):
#        print(msg.note)
#        input()
mid.save(filepath[:-4]+{True:"-大",False:'-小'}[not ismajor]+"调.mid")

#import ipdb
#ipdb.set_trace()