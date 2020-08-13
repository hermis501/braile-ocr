from textblob import TextBlob
from textblob import Word

f=open ("E:/braille/braille.txt","a+")
with open ("MUSOC.txt","r") as fp:
    content=fp.read()
blob=TextBlob(content)
p=(blob.correct())
open("E:/braille/braille_corrected.txt","w+")
f.write(str(p))
f.close()

