import random
word=random.choice(list(open('EnglishWords.txt','r'))).strip()
letters=set(word)
limbs=10
while letters and limbs:
    print(" ".join("_"if x in letters else x for x in word),limbs)
    try:letters.remove(input()[0])
    except:limbs-=1
print(word)
