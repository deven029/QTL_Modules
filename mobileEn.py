import random, string

def keyGenerator(size=10, chars=string.digits):
    return list(map(int,''.join(random.choice(chars) for _ in range(size))))

def cipherMobile(mobile_number,key):
    mobNo = list(map(int, (list(mobile_number))))

    for i in range(len(key)):
        mobNo[i] = (mapper[(key[i])] +mobNo[i] )% 10
    return ''.join(map(str, (mobNo)))

def deCipherMobile(cipherMno,key):
    cipherMno = list(map(int, (list(cipherMno))))
    mno = []
    for i in range (len(cipherMno)):
        mno.append((cipherMno[i] - mapper[key[i]])%10)
    return ''.join(map(str, (mno)))

mapper = list(map(int, (list('1234567890'))))
key = keyGenerator()
cipherMno = cipherMobile('8872383735',key)
mno = deCipherMobile(cipherMno,key)
print('key: ',key, 'CT: ',cipherMno,'mno: ',mno)