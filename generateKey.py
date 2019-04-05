from random import choice

#This class generates a random key for watermark creation
class generateKey(object):
    def genKey(self):
        # Opens the text file containing a list of keys and acquire the keys into an array
        text_file=open('keys.txt','r')
        secret_list=text_file.read().split(',')
        text_file.close()

        #Choose a random four digit key from the list of possible keys
        secret_list=map(int,secret_list)
        secretKey = str(choice(secret_list))
        return secretKey


