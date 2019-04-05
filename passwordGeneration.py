import random,os,string
class generatePassword(object):
    def genPassword(self):
        length = 14
        chars = string.ascii_letters + string.digits + '!@#$%_&*-' #Password will include ASCII letters, numbers and special characters
        random.seed = (os.urandom(1024))  # Return a string of n random bytes suitable for cryptographic use.

        password = ''.join(random.choice(chars) for i in range(length))
        return password
