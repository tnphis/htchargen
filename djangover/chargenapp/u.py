import random, string

def randomword(length):
   return u''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))
