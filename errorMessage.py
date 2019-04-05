import tkMessageBox

class Errors(object):
    def errorMessageStartup(self):
        tkMessageBox.showinfo("Check Inputs","Required Input Fields are Incomplete/Incorrect!")

    def errorMessagePassportNumber(self):
        tkMessageBox.showinfo("Passport Number Mismatch","Input Passport Number Mismatches Stored Data!")

    def notEnoughMatchesFound(self):
        tkMessageBox.showinfo("Face/Signature Mismatch", "Unable to Verify Holder!")

    def tagNotFound(self):
        tkMessageBox.showinfo("Tag Not Found!", "Unable to Verify Tag Information!")

    def dbAccessDenied(self):
        tkMessageBox.showinfo("Acess DENIED!", "Wrong Username or Password!")

    def incorrectImageSize(self):
        tkMessageBox.showinfo("Input Rejected!", "Image Should be of Size 413x531!")

    def issuanceError(self):
        tkMessageBox.showinfo("Process Halted!", "Issuance Proess Could NOT be COMPLETED!")

    def genericError(self,msg):
        tkMessageBox.showinfo("Error Notification!", msg)