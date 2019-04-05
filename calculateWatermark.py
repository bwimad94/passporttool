import itertools

class Calculate(object):

    def __init__(self,secretKey,first,second,third,family,passport):
        self.first=first
        self.second=second
        self.third=third
        self.family=family
        self.passport=passport

        self.secretKey = secretKey

        self.secretList = list(self.secretKey)
        self.newListInt = []

        #converts the string list into an integer list
        for self.i in self.secretList:
            self.newListInt.append((int(self.i)))

        #creates a new list with reordered secretkey values
        self.newRoundRobin = self.newListInt[1:]
        self.newRoundRobin.append(self.newListInt[0])


        self.firstNm = first.upper()

        self.secondNm = second.upper()

        if self.secondNm == '*OPTIONAL':#If no second name reuse first name
            self.secondNm = self.firstNm

        self.lastNm = family.upper()

        self.thirdNm = third.upper()#If no third name reuse last name
        if self.thirdNm == '*OPTIONAL':
            self.thirdNm = self.lastNm

        self.passNum = passport.upper()

        #converts all string to lists
        self.listFirst = list(self.firstNm)
        self.listSecond = list(self.secondNm)
        self.listFamily = list(self.lastNm)
        self.listPass = list(self.passNum)
        self.listThird = list(self.thirdNm)

        self.passLetters = []

        #Extract all letters in the passport number to a seperate list
        for self.ch in self.listPass:
            if self.ch.isalpha():
                self.passLetters.append(self.ch)

        # Extract all numbers in the passport number to a seperate list
        self.passInt = [int(self.x) for self.x in self.listPass if self.x.isdigit()]

        #dictionary mapping each letter in the alphabet with the corresponding code value
        self.entries = {
            'A': 1,
            'B': 2,
            'C': 3,
            'D': 4,
            'E': 5,
            'F': 6,
            'G': 7,
            'H': 8,
            'I': 9,
            'J': 10,
            'K': 11,
            'L': 12,
            'M': 13,
            'N': 14,
            'O': 15,
            'P': 16,
            'Q': 17,
            'R': 18,
            'S': 19,
            'T': 20,
            'U': 21,
            'V': 22,
            'W': 23,
            'X': 24,
            'Y': 25,
            'Z': 26

        }

    #This method caluculates the row value for watermark algorithm

    def calculateRow(self):
        self.firstList = []
        self.firstListEncrypted = []

        #Assigns code values to the letters in the first name
        for self.ch in self.listFirst:
            for self.key, self.val in self.entries.items():

                if self.ch == self.key:
                    self.ch = self.val

                    self.firstList.append(self.ch)

        #Creates a key array with new key combination for the row calculation by adding consecutive key values in a round robin manner
        self.keyArray = [(int(self.x) + int(self.y)) for (self.x, self.y) in zip(self.newListInt, self.newRoundRobin)]

        #Obtains a list of numeric values by multiplying each the coded character in first name against the respective key in key array
        for self.keyVal, self.ch in zip(itertools.cycle(self.keyArray), self.firstList):
            self.newVal = int(self.keyVal) * self.ch
            self.firstListEncrypted.append(self.newVal)

        #Row value is equal to the summation of the list of numeric values
        self.row = sum(self.firstListEncrypted)

        #Ensures rowvalue does not exceed the pixel dimensions of the input image
        if self.row >= 413:
            self.row = 412


        return self.row


    def calculateCol(self):
        self.secondList = []


        self.secondListEncrypted = []

        #Encodes letters in the first name
        for self.ch in self.listSecond:
            for self.key, self.val in self.entries.items():

                if self.ch == self.key:
                    self.ch = self.val

                    self.secondList.append(self.ch)

        self.keySecondList = []

        # Creates a key array with new key combination for the row calculation by adding alternating key values in a round robin manner
        self.keySecondList.append(self.secretList[2])
        self.keySecondList.append(self.secretList[3])
        self.keySecondList.append(self.secretList[0])
        self.keySecondList.append(self.secretList[1])
        self.secondKeyArray = [(int(self.x) + int(self.y)) for (self.x, self.y) in zip(self.secretList, self.keySecondList)]

        # Obtains a list of numeric values by multiplying each the coded character in second name against the respective key in key array
        for self.keyVal, self.ch in zip(itertools.cycle(self.secondKeyArray), self.secondList):
            self.newValSecond = int(self.keyVal) * self.ch
            self.secondListEncrypted.append(self.newValSecond)

        self.column = sum(self.secondListEncrypted)

        #Ensures that the column value does not exceed inut image dimensions
        if self.column >= 531:
            self.column = 530


        return  self.column

    def calculateSum(self):

        self.thirdList=[]
        self.familyList=[]
        self.passList = []


        #Encoded family name
        for self.ch in self.listFamily:
            for self.key, self.val in self.entries.items():

                if self.ch == self.key:
                    self.ch = self.val

                    self.familyList.append(self.ch)

        # Obtains a list of numeric values by multiplying each the coded character in family name against the respective key in original key array
        self.familyArray = [(int(self.x) * int(self.y)) for (self.x, self.y) in zip(itertools.cycle(self.newListInt), self.familyList)]
        self.familyArrSum = sum(self.familyArray)

        #Encodes third name
        for self.ch in self.listThird:
            for self.key, self.val in self.entries.items():

                if self.ch == self.key:
                    self.ch = self.val

                    self.thirdList.append(self.ch)

        # Obtains a list of numeric values by multiplying each coded character in third name against the respective key in original key array
        self.thirdArray = [(int(self.x) * int(self.y)) for (self.x, self.y) in zip(itertools.cycle(self.newListInt), self.thirdList)]
        self.thirdArrSum = sum(self.thirdArray)

        #Encodes the letters in passport number
        for self.ch in self.passLetters:
            for self.key, self.val in self.entries.items():

                if self.ch == self.key:
                    self.ch = int(self.val)

                    self.passList.append(self.ch)

        #Append the encoded password letters to the integer array where the passport digits are stored
        self.passList.extend(self.passInt)

        self.passArrSum = sum(self.passList)

        self.sumAll = self.familyArrSum+ self.thirdArrSum + self.passArrSum

        return self.sumAll
