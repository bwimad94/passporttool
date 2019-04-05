import mysql.connector
import mysql.connector.constants
from generateKey import *
from calculateWatermark import *
from PIL import Image
import numpy as np
import os
from passwordGeneration import *
from AES import *
from AESpwd import *

class Complete_Issuance(generateKey,Calculate,generatePassword,AESCipher):

    def __init__(self,path,signPath,firstNm,secondNm,thirdNm,familyNm,passport):

        self.path=path#original image location
        self.firstNm=firstNm
        self.secondNm=secondNm
        self.thirdNm=thirdNm
        self.familyNm=familyNm
        self.passport=passport
        self.signPath=signPath
        self.filename=""
        self.signFileName=""
        self.AESpwdObj=AESPassword(self.passport)
        self.AESpwd=self.AESpwdObj.calPwd()
        self.aesDBEncryptObj=AESCipher(self.AESpwd)




    def embedWM(self):

        self.keyObj=generateKey()#Generate secret key for encryption
        self.key = self.keyObj.genKey()
        print self.key

        watermark = Calculate(self.key, self.firstNm, self.secondNm, self.thirdNm, self.familyNm, self.passport)
        self.row = watermark.calculateRow()
        self.column = watermark.calculateCol()
        self.sumAll = watermark.calculateSum()

        self.watermarkImg = Image.open(self.path)

        self.pixel = self.watermarkImg.load()#load image as pixel array

       #Get the sum of pixel values at location row,column
        self.pixelSum = sum(self.pixel[self.row, self.column])


        self.avg = (self.pixelSum / 3) + 1
        self.pixCount = self.sumAll / self.avg

        # this is the watermark
        self.value = self.sumAll % self.avg
        self.rColumn = self.column + self.pixCount + 1

        #Ensures rcolumn does not exceed the image dimensions
        if self.rColumn >= 531:
            self.rColumn = 530

        #Extract RGB values of input image to seperate arrays
        self.r, self.g, self.b = np.array(self.watermarkImg).T

        #Get the RGB values at location row,column
        self.rval = self.r[self.row, self.rColumn]
        self.gval = self.g[self.row, self.rColumn]
        self.bval = self.b[self.row, self.rColumn]
        self.name = ''

        #Find the maximum pixel value at location row,column
        self.Max = self.rval
        if self.gval > self.Max:
            self.Max = self.gval
        if self.bval > self.Max:
            self.Max = self.bval
            if self.gval > self.bval:
                self.Max = self.gval

        #Decides which channel contains the maximum value
        if self.Max == self.rval:
            self.name = 'R'
        elif self.Max == self.gval:
            self.name = 'G'
        else:
            self.name = 'B'

        #Replaces the maximum pixel at location row,column with the watermark
        self.maxPixel = max(self.pixel[self.row, self.rColumn])
        self.maxIndex = (self.pixel[self.row, self.rColumn]).index(max(self.pixel[self.row, self.rColumn]))
        self.pixelNewList = list(self.pixel[self.row, self.rColumn])
        self.pixelNewList[self.maxIndex] = self.value
        self.pixel[self.row, self.rColumn] = tuple(self.pixelNewList)

    def insertToTemplateDB(self):

        self.passportEncrypted = self.aesDBEncryptObj.encryptAES(self.passport)

        self.imgTemplateDir = 'C:/Users/BHAGYA/Dropbox/FYP_Application/ePassportv.2/Templates/facial/'  # default directory to store files
        self.template_suffix = 'png'
        self.fileNameImage = os.path.join(self.imgTemplateDir, self.passport + "." + self.template_suffix)

        self.signTemplateDir = 'C:/Users/BHAGYA/Dropbox/FYP_Application/ePassportv.2/Templates/signatures/'  # default directory to store files
        self.fileNameSign = os.path.join(self.signTemplateDir, self.passport + "." + self.template_suffix)


        self.connCL = mysql.connector.connect(user='bwimad', passwd='DdA2*H&tB', host='64.62.211.131',
                                              database="bwimad_fyp")
        self.curCL = self.connCL.cursor()
        #self.conn = mysql.connector.connect(user='root', passwd='root', host='localhost', database="fyp", port=3306)
        #self.cur = self.conn.cursor()
        self.add_entry = "INSERT INTO holder_templates VALUES ('%s', '%s', '%s')" % \
                          (self.passport, self.fileNameImage,self.fileNameSign)
        #self.cur.execute(self.add_entry)
        self.curCL.execute(self.add_entry)
        #self.conn.commit()
        self.connCL.commit()
        #self.cur.close()
        #self.conn.close()
        self.curCL.close()
        self.connCL.close()







        #This method inserts data into passport holder information database
    def insertToHolderDB(self,holderGender,holderDOB,holderPOB,holderProfession,holderNIC,holderType,holderNation,dateIssued,dateExpired):

        self.connCL = mysql.connector.connect(user='bwimad', passwd='DdA2*H&tB', host='64.62.211.131',database="bwimad_fyp",port=3306)
        self.curCL = self.connCL.cursor()
        #self.conn = mysql.connector.connect(user='root', passwd='root', host='localhost', database="fyp", port=3306)
        #self.cur = self.conn.cursor()

        self.add_holder = "INSERT INTO passport_holders VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s', '%s','%s','%s')" % \
                          (self.passport, self.firstNm, self.secondNm, self.thirdNm, self.familyNm,
                           holderGender, holderDOB, holderPOB, holderProfession, holderNIC,
                           holderType, holderNation, dateIssued,dateExpired,self.path,self.signPath)
        #self.cur.execute(self.add_holder)
        self.curCL.execute(self.add_holder)
        #self.conn.commit()
        self.connCL.commit()
        #self.cur.close()
        #self.conn.close()
        self.curCL.close()
        self.connCL.close()

    # This method inserts data into watermarking information database
    def insertToWMDB(self):
        #This method inserts data into local database and the cloud database seperately

        self.connCL = mysql.connector.connect(user='bwimad', passwd='DdA2*H&tB', host='64.62.211.131',database="bwimad_fyp",port=3306)
        self.curCL=self.connCL.cursor()
        #self.conn = mysql.connector.connect(user='root', passwd='root', host='localhost', database="fyp", port=3306)
        #self.cur = self.conn.cursor()
        self.add_watermark_values = "INSERT INTO watermarking_info  (pass_no,SCRT_KEY,ROW,COL,RCOLUMN,SUM,PIX_COUNT,WATERMARK,CHANNEL,ORIGINAL_VAL) VALUES  ('%s', %d, %d, %d,%d, %d, %d, %d, '%s',%d)" % \
                                    (self.passport, int(self.key), int(self.row), int(self.column),
                                     int(self.rColumn), int(self.sumAll), int(self.pixCount), int(self.value),
                                     self.name, int(self.maxPixel))


        #self.cur.execute(self.add_watermark_values )
        self.curCL.execute(self.add_watermark_values )
        #self.conn.commit()
        self.connCL.commit()
        #self.cur.close()
        #self.conn.close()
        self.curCL.close()
        self.connCL.close()

    #Saving images in png format

    def saveTagImg(self):
        self.Imagedir = 'C:/Users/BHAGYA/Dropbox/fyp/.idea/image_files/'
        self.image_suffix = 'png'
        self.filename = os.path.join(self.Imagedir, self.passport + "." + self.image_suffix)
        if self.filename:
            return self.watermarkImg.save(self.filename, lossless=True)
        else:
            pass

    def saveTagSign(self):
        self.Signdir = 'C:/Users/BHAGYA/Dropbox/fyp/.idea/image_files/'
        self.sign_suffix = 'png'
        self.watermarkSignImg = Image.open(self.signPath)
        self.signFileName = os.path.join(self.Signdir, self.passport+"_signature" + "." + self.sign_suffix)
        if self.signFileName:
            return self.watermarkSignImg.save(self.signFileName, lossless=True)
        else:
            pass

    def saveRFIDFile(self,holderGender,holderDOB,holderPOB,holderProfession,holderNIC,holderType,holderNation,dateIssued,dateExpired):

        #This methods saves encrypted user data in a text file which will be saved into an RFID tag

        self.connCL = mysql.connector.connect(user='bwimad', passwd='DdA2*H&tB', host='64.62.211.131',
                                              database="bwimad_fyp", port=3306)
        self.curCL = self.connCL.cursor()
        #self.conn = mysql.connector.connect(user='root', passwd='root', host='localhost', database="fyp", port=3306)
        #self.cur = self.conn.cursor()

        self.RFIDdir = 'C:/Users/BHAGYA/Dropbox/fyp/.idea/rfid_files/' #default directory to store files
        self.rfid_suffix = 'txt'
        if self.filename!="":

            #Encrypt information
            self.passwordObj=generatePassword()
            self.password = self.passwordObj.genPassword()
            self.AESObj = AESCipher(self.password)
            self.encryptedReference = self.AESObj.encryptAES(self.filename)
            self.encryptedSignRef = self.AESObj.encryptAES(self.signFileName)
            self.encryptedPass_num = self.AESObj.encryptAES(self.passport)
            self.encryptedFirst = self.AESObj.encryptAES(self.firstNm)
            self.encryptedSecond = self.AESObj.encryptAES(self.secondNm)
            self.encryptedThird = self.AESObj.encryptAES(self.thirdNm)
            self.encryptedLast = self.AESObj.encryptAES(self.familyNm)
            self.encryptedGen = self.AESObj.encryptAES(holderGender)
            self.encryptedDOB = self.AESObj.encryptAES(holderDOB)
            self.encryptedPOB = self.AESObj.encryptAES(holderPOB)
            self.encryptedProf = self.AESObj.encryptAES(holderProfession)
            self.encryptedNIC = self.AESObj.encryptAES(holderNIC)
            self.encryptedType = self.AESObj.encryptAES(holderType)
            self.encryptedNation = self.AESObj.encryptAES(holderNation)
            self.encryptedIssued = self.AESObj.encryptAES(dateIssued)
            self.encryptedExpired = self.AESObj.encryptAES(dateExpired)

            #Save information into a text file
            self.fileContent = open(os.path.join(self.RFIDdir, self.passport + "." + self.rfid_suffix),'w')  # can remove dir which will save files to same folder as the the exe file
            self.fileContent.write(self.encryptedReference + "\n")
            self.fileContent.write(self.encryptedSignRef + "\n")
            self.fileContent.write(self.encryptedPass_num + "\n")
            self.fileContent.write(self.encryptedFirst + "\n")
            self.fileContent.write(self.encryptedSecond + "\n")
            self.fileContent.write(self.encryptedThird + "\n")
            self.fileContent.write(self.encryptedLast + "\n")
            self.fileContent.write(self.encryptedGen + "\n")
            self.fileContent.write(self.encryptedDOB + "\n")
            self.fileContent.write(self.encryptedPOB + "\n")
            self.fileContent.write(self.encryptedProf + "\n")
            self.fileContent.write(self.encryptedNIC + "\n")
            self.fileContent.write(self.encryptedType + "\n")
            self.fileContent.write(self.encryptedNation + "\n")
            self.fileContent.write(self.encryptedIssued + "\n")
            self.fileContent.write(self.encryptedExpired + "\n")
            self.fileContent.close()

            #Updates databases
            #self.cur.execute("UPDATE watermarking_info SET imagePath = %s WHERE pass_no=%s",(self.filename, self.passport))
            #self.cur.execute("UPDATE watermarking_info SET password = %s WHERE pass_no=%s",(self.password, self.passport))
            #self.cur.execute("UPDATE watermarking_info SET signaturePath= %s WHERE pass_no=%s",(self.signFileName, self.passport))
            self.curCL.execute("UPDATE watermarking_info SET imagePath = %s WHERE pass_no=%s",
                             (self.filename, self.passport))
            self.curCL.execute("UPDATE watermarking_info SET password = %s WHERE pass_no=%s",
                             (self.password, self.passport))
            self.curCL.execute("UPDATE watermarking_info SET signaturePath= %s WHERE pass_no=%s",
                             (self.signFileName, self.passport))
            #self.conn.commit()
            self.connCL.commit()
            #self.cur.close()
            #self.conn.close()
            self.curCL.close()
            self.connCL.close()

