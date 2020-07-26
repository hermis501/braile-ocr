from textblob import TextBlob
from textblob import Word

f=open ("E:\braille\MUSOC.txt","a+")
with open ("MUSOC.txt","r") as fp:
    content=fp.read()
blob=TextBlob(content)
p=(blob.correct())
open("E:\braille\MUSOC.txt","w+")
f.write(str(p))
f.close()

