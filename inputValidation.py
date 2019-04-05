from datetime import *

class InputValidation(object):

    def validateFirst(self,first):
        self.count = 0
        self.first=str(first)

        if first:
        #checks whether the input contains any numbers, if it does a counter is incremented
            for self.char in first:
                if self.char.isdigit():
                    self.count += 1

            if self.count > 0:

                return "First Name Cannot Contain Numbers!"
        else:
            return "First Name Cannot Be Empty!"

    def validateSecond(self,second):
        self.count = 0
        self.second=str(second)
        #Since second name is optional no error is generated when the field is empty
        # checks whether the input contains any numbers, if it does a counter is incremented
        for self.char in second:
            if self.char.isdigit():
                self.count += 1
        if self.count > 0:

            return "Second Name Cannot Contain Numbers!"

    def validateThird(self, third):
        self.count = 0
        self.third = str(third)

        for self.char in third:
            if self.char.isdigit():
                self.count += 1
        if self.count > 0:
            return "Third Name Cannot Contain Numbers!"


    def validateFamily(self, family):
        self.count = 0
        self.family = str(family)

        if family:

            for self.char in family:
                if self.char.isdigit():
                    self.count += 1
            if self.count > 0:

                return "Family Name Cannot Contain Numbers!"
        else:
            return "Family Name Cannot Be Empty!"


    def validatePassport(self,passportNum):

        # Checks whether the passport number is empty
        # Checks whether the first character is one of N/M/D
        # Checks whether the length of passport number is 7
        # Checks whether all characters except the first character are numbers
        # If the first two characters are OL then the length should be 8 and all characters except OL should be numbers

        if passportNum!="":

            if (passportNum[0]=='N' or passportNum[0]=='M' or passportNum[0]=='D') and len(passportNum)== 8 and passportNum[1:].isdigit():
                return True

            elif passportNum[0]=='O' and passportNum[1] =='L' and len(passportNum) ==9 and passportNum[2:].isdigit():
                return True

            else:
                return False
        else:
            return False


    def validateDate(self,date_text):

        #Ensures that any date inserted is in DD-MM-YYYY format
        if not date_text == "" :
            if not date_text == 'DD/MM/YYYY':
                try:
                    datetime.strptime(date_text, '%d/%m/%Y')
                except ValueError:
                    return "Incorrect data format, should be DD/MM/YYYY"
            else:
                return "Date Field has to be Specified!"
        else:
            return "Date Field Cannot be Empty!"



    def validateNIC(self,nic):
        #Ensures the NIC Number conforms to the valid format
        #Correct format returns boolean false

        self.nic=str(nic)

        try:
            if nic:
                if nic.isdigit() and len(nic)==12:
                    return False
                elif nic[9]=="V" and nic[0:9].isdigit() and len(nic)==10:
                    return False
                else:
                    return "NIC Incorrect Format!"
            else:
                return "NIC Cannot be EMPTY!"
        except IndexError:
            return "NIC Incorrect Format!"

    def validateText(self,input):

        #Ensures that input is specific and does not contain numbers

        noSpace=input.replace(" ","")#removes any spaces
        if input and input !="CITY/TOWN":
            if noSpace.isalpha():
                return False
            else:
                return "Entered Data Cannot Contain Numbers!"
        else:
            return "Enter Specififc Data!"





