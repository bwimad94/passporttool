from Tkinter import *
from Tkconstants import *
from uploadImg import *
from featureMatcher import *
from inputValidation import InputValidation
from Tkinter import Button
from verifyWatermark import *
import os
import mysql.connector
from AES import *
from errorMessage import *
from utilMethods import *
from matchSignature import *
from mysql.connector import errorcode

class Prompt(InputValidation,verifyWatermark,uploadImg,featureMatcher,AESCipher,Utilities,Errors,signatureMatcher):


    def backToMain(self):

        # This method refreshes the start-up screen for a new issuance

        try:
            self.watermarkTL_toplevel.destroy()
            root.deiconify()
            root.lift()
            self.canvas2.delete(self.passportImg)
            self.canvas2.delete(self.passportSign)
            self.ePass.delete(0,END)
            self.ePass.focus_set()
            self.db_tag_canvas.delete(self.db_img)
            self.db_tag_canvas.delete(self.db_sign)
            self.db_tag_canvas.delete(self.tag_img)
            self.db_tag_canvas.delete(self.tag_sign)
            self.featureMatching_canvas.delete(self.match_face)
            self.featureMatching_canvas.delete(self.match_sign)
            os.remove('C:\Users\BHAGYA\Dropbox\FYP_Application\ePassportv.3\Scanned_Images\holder.jpg')
            #os.remove('C:\Users\BHAGYA\Dropbox\FYP_Application\ePassportv.2\Scanned_Signatures\holder_Sign.png')
        except Exception as ex:
            template = "An exception of type {0} occurred. Details:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            self.errorObj.genericError(message)


    def create_verifyImg(self):

        #This method uploads the scanned image of the passport from a default location
       try:
           self.resized_width = 500
           self.resized_height = 300

           self.verifyPath = 'C:\Users\BHAGYA\Dropbox\FYP_Application\ePassportv.3\Scanned_Images\holder.jpg'

           if self.verifyPath:
               self.verifyImgObj = uploadImg(self.verifyPath)
               self.ttkverifyImg = self.verifyImgObj.uploadResized(self.resized_width, self.resized_height)
               #self.canvas2.delete(self.passportImg)
               self.passportImg=self.canvas2.create_image(125, 200, image=self.ttkverifyImg, anchor='nw')
               self.canvas2.grid()
               self.canvas2.image = self.ttkverifyImg

           else:
               self.errorObj.genericError("Image Path Does NOT Exist!")


       except Exception as ex:

           template = "An exception of type {0} occurred. Details:\n{1!r}"

           message = template.format(type(ex).__name__, ex.args)

           self.errorObj.genericError(message)

    def checkSignatures(self):
        #This method performs the signature similarity check

        try:


            img=Image.open(self.verifyPath)
            width, height = img.size  # Get dimensions

            #Crops the scanned image so that it frames the section with signature
            croppedImg = img.crop((width - 600, height - 625, width - 150, height - 475))
            croppedImg.save("cropped.png")

            img = cv2.imread("cropped.png",0)



            self.scannedSign = img
            self.storedSign= cv2.imread(self.db_getSignPath, 0)

            #Resizes the scanned and stored signs be of identical dimensions
            self.scannedSign = cv2.resize(self.scannedSign, (400, 250))
            self.storedSign = cv2.resize(self.storedSign, (400, 250))



            if self.scannedSign is None:
                self.errorObj.errorMessageStartup()
            if self.storedSign is None:
                self.errorObj.errorMessageStartup()

            self.kp_pair_obj=signatureMatcher(self.scannedSign, self.storedSign)

            self.kp_pair_sign = self.kp_pair_obj.match_images()

            if self.kp_pair_sign:
                self.drawImgSign = self.kp_pair_obj.draw_matches(self.kp_pair_sign)
                cv2.waitKey()
                self.signMatching_canvas.image = self.drawImgSign
                self.match_sign=self.signMatching_canvas.create_image(25, 50, image=self.drawImgSign, anchor='nw')
                self.signMatching_canvas.grid()

                self.scannedSignLabel = Label(self.signMatching_canvas, text="Scanned Signature")
                self.scannedSignLabel.grid()
                self.scannedSignLabel.config(bg="Black",fg="White", font=("Courier", 14))
                self.scannedSignLabel_window = self.signMatching_canvas.create_window(150, 325, anchor=NW,
                                                                                       window=self.scannedSignLabel)

                self.storedSignLabel = Label(self.signMatching_canvas, text="Stored Signature")
                self.storedSignLabel.grid()
                self.storedSignLabel.config(bg="Black", fg="White", font=("Courier", 14))
                self.storedSignLabel_window = self.signMatching_canvas.create_window(550, 325, anchor=NW,
                                                                                      window=self.storedSignLabel)

                #Two signatures must have at least 70 siilar key points between them to be considered similar
                if len(self.kp_pair_sign) < 70:
                    self.signMatchMsg.set("   SIGNATURE MISMATCH!   ")
                    self.signMatchMsgLabel = Label(self.signMatching_canvas, textvariable=self.signMatchMsg)
                    self.signMatchMsgLabel.grid()
                    self.signMatchMsgLabel.config(bg="RED", font=("Courier", 14))
                    self.signMatchMsgLabel_window = self.signMatching_canvas.create_window(200, 400, anchor=NW,
                                                                                              window=self.signMatchMsgLabel)



                else:
                    self.signMatchMsg.set("HOLDER SIGNATURE AUTHENTICATED!")
                    self.signMatchMsgLabel = Label(self.signMatching_canvas, textvariable=self.signMatchMsg)
                    self.signMatchMsgLabel.grid()
                    self.signMatchMsgLabel.config(bg="GREEN", font=("Courier", 14))
                    self.signMatchMsgLabel_window = self.signMatching_canvas.create_window(200, 400, anchor=NW,
                                                                                              window=self.signMatchMsgLabel)

        except Exception as ex:
            template = "An exception of type {0} occurred. Details:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            self.errorObj.genericError(message)


    def signSimilarityGUI(self):
        # GUI Configurations for signature similarity window
        try:
            self.featureMatching_toplevel.withdraw()
            self.signMatching_toplevel = Toplevel()
            self.signMatching_toplevel.attributes('-topmost', True)
            self.signMatching_toplevel.wm_title("Match Signature")
            self.signMatching_width = 850
            self.signMatching_height = 600
            self.signMatching_ws = self.signMatching_toplevel.winfo_screenwidth()
            self.signMatching_hs = self.signMatching_toplevel.winfo_screenheight()
            self.x = (self.signMatching_ws / 2) - (self.signMatching_width / 2)
            self.y = (self.signMatching_hs / 2) - (self.signMatching_height / 2)
            self.signMatching_toplevel.geometry(
                '%dx%d+%d+%d' % (self.signMatching_width, self.signMatching_height, self.x, self.y))
            self.signMatching_toplevel.config(background="#CCD1D1")
            self.signMatching_toplevel.option_add("*Font", "Courier 12 bold ")

            self.signMatching_toplevel.option_add("*Button.Font", "Courier 12 bold")
            self.signMatching_toplevel.option_add("*Button.Background", "#1F618D")
            self.signMatching_toplevel.option_add("*Button.Foreground", "#A9CCE3")

            self.signMatching_toplevel.option_add("*Label.Font", "Courier 11 bold")
            self.signMatching_toplevel.option_add("*Label.Background", "#1F618D")
            self.signMatching_toplevel.option_add("*Label.Foreground", "#A9CCE3")
            self.signMatching_toplevel.option_add("*Label.bd", 10)
            self.signMatching_toplevel.option_add("*Label.Relief", "ridge")

            self.signMatching_canvas = Canvas(self.signMatching_toplevel, width=850, height=700)
            self.signMatching_canvas.config(background="#CCD1D1")
            self.signMatching_canvas.grid(row=0, column=1, columnspan=3)

            self.signMatching_back_button = Button(self.signMatching_toplevel, text="<<<Back",
                                                   command=lambda: self.backObj.backButton(self.signMatching_toplevel,
                                                                                           self.featureMatching_toplevel))
            self.signMatching_back_button.grid()
            self.signMatching_back_button_windows = self.signMatching_canvas.create_window(25, 550, anchor=NW,
                                                                                           window=self.signMatching_back_button)

            self.finalProceed = Button(self.signMatching_toplevel, text="Complete Validation>>>",
                                       command=self.verifyWatermarkGUI)
            self.finalProceed.grid(row=8, column=3)
            self.finalProceed_window = self.signMatching_canvas.create_window(550, 550, anchor=NW,
                                                                              window=self.finalProceed)

            self.checkSignatures()

        except Exception as ex:
            template = "An exception of type {0} occurred. Details:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            self.errorObj.genericError(message)

    def checkSimilarity(self):
        #This method performs the facial image simialrity check

        try:
            #Obtains scanned image and the database image
            self.scannedImg=Image.open(self.verifyPath)
            self.storedImg=cv2.imread(self.db_getImgPath,0)

            #Crops the scanned image to obtain the area with facial photograph
            croppedImg = self.scannedImg.crop((25, 110, 423, 591))
            croppedImg.save("croppedImg.png")

            img = cv2.imread("croppedImg.png", 0)

            self.scannedImg = img

            #Resizes both the images so they are similar in size
            self.scannedImg= cv2.resize(self.scannedImg, (413, 531))
            self.storedImg = cv2.resize(self.storedImg, (413, 531))

            #self.scannedImg = cv2.resize(self.scannedImg, (350, 468))
            #self.storedImg = cv2.resize(self.storedImg, (350, 468))

            if self.scannedImg is None:
                self.errorObj.errorMessageStartup()
            if self.storedImg is None:
                self.errorObj.errorMessageStartup()

            #Calculates similarity
            self.kp_pair_objImg=featureMatcher(self.scannedImg,self.storedImg)

            self.template=self.kp_pair_objImg.matchTemplate()

            self.kp_pair=self.kp_pair_objImg.match_images()

            if self.kp_pair:
                self.drawImg=self.kp_pair_objImg.draw_matches(self.kp_pair)
                cv2.waitKey()
                self.featureMatching_canvas.image = self.drawImg
                self.match_face=self.featureMatching_canvas.create_image(75 , 25, image=self.drawImg, anchor='nw')
                self.featureMatching_canvas.grid()

                self.scannedFaceLabel = Label(self.featureMatching_canvas, text="Scanned Facial Photograph")
                self.scannedFaceLabel.grid()
                self.scannedFaceLabel.config(bg="Black", fg="White", font=("Courier", 14))
                self.scannedFaceLabel_window = self.featureMatching_canvas.create_window(150, 550, anchor=NW,
                                                                                         window=self.scannedFaceLabel)

                self.storedFaceLabel = Label(self.featureMatching_canvas, text="Stored Facial Photograph")
                self.storedFaceLabel.grid()
                self.storedFaceLabel.config(bg="Black", fg="White", font=("Courier", 14))
                self.storedFaceLabel_window = self.featureMatching_canvas.create_window(550, 550, anchor=NW,
                                                                                        window=self.storedFaceLabel)

                #Images must have at least 100 similar key points between them to considered similar
                if len(self.kp_pair)<100:
                    self.imageMatchMsg.set("   HOLDER IMAGE MISMATCH!   ")
                    self.faceMatchMsgLabel = Label(self.featureMatching_canvas, textvariable=self.imageMatchMsg)
                    self.faceMatchMsgLabel.grid()
                    self.faceMatchMsgLabel.config(bg="RED", font=("Courier", 14))
                    self.faceMatchMsgLabel_window = self.featureMatching_canvas.create_window(300, 600, anchor=NW,
                                                                                              window=self.faceMatchMsgLabel)



                else:
                    self.imageMatchMsg.set("  HOLDER FACE AUTEHNTICATED!  ")
                    self.faceMatchMsgLabel = Label(self.featureMatching_canvas, textvariable=self.imageMatchMsg)
                    self.faceMatchMsgLabel.grid()
                    self.faceMatchMsgLabel.config(bg="GREEN", font=("Courier", 14))
                    self.faceMatchMsgLabel_window = self.featureMatching_canvas.create_window(300, 600, anchor=NW,
                                                                                              window=self.faceMatchMsgLabel)

        except Exception as ex:
            template = "An exception of type {0} occurred. Details:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            self.errorObj.genericError(message)


    def facialSimilarityGUI(self):
        try:
            # GUI COnfigurations for facial similarity check window
            self.db_tag_toplevel.withdraw()
            self.featureMatching_toplevel = Toplevel()
            self.featureMatching_toplevel.attributes('-topmost',True)
            self.featureMatching_toplevel.wm_title("Match Features")
            self.db_tag_width = 1000
            self.db_tag_height = 700
            self.db_tag_ws = self.featureMatching_toplevel.winfo_screenwidth()
            self.db_tag_hs = self.featureMatching_toplevel.winfo_screenheight()
            self.x = (self.db_tag_ws / 2) - (self.db_tag_width / 2)
            self.y = (self.db_tag_hs / 2) - (self.db_tag_height / 2)
            self.featureMatching_toplevel.geometry('%dx%d+%d+%d' % (self.db_tag_width, self.db_tag_height, self.x, self.y))
            self.featureMatching_toplevel.config(background="#CCD1D1")
            self.featureMatching_toplevel.option_add("*Font", "Courier 12 bold ")

            self.featureMatching_toplevel.option_add("*Button.Font", "Courier 12 bold")
            self.featureMatching_toplevel.option_add("*Button.Background", "#1F618D")
            self.featureMatching_toplevel.option_add("*Button.Foreground", "#A9CCE3")

            self.featureMatching_toplevel.option_add("*Label.Font", "Courier 11 bold")
            self.featureMatching_toplevel.option_add("*Label.Background", "#1F618D")
            self.featureMatching_toplevel.option_add("*Label.Foreground", "#A9CCE3")
            self.featureMatching_toplevel.option_add("*Label.bd", 10)
            self.featureMatching_toplevel.option_add("*Label.Relief", "ridge")


            self.featureMatching_canvas = Canvas(self.featureMatching_toplevel, width=1500, height=700)
            self.featureMatching_canvas.config(background="#CCD1D1")
            self.featureMatching_canvas.grid(row=0, column=1, columnspan=3)




            self.featureMatching_back_button = Button(self.featureMatching_toplevel, text="<<<Back",
                                      command=lambda: self.backObj.backButton(self.featureMatching_toplevel, self.db_tag_toplevel))
            self.featureMatching_back_button.grid()
            self.featureMatching_back_button_windows = self.featureMatching_canvas.create_window(25, 650, anchor=NW, window=self.featureMatching_back_button)

            self.finalProceed = Button(self.featureMatching_toplevel, text="Validate Signature>>>", command=self.signSimilarityGUI)
            self.finalProceed.grid(row=8, column=3)
            self.finalProceed_window = self.featureMatching_canvas.create_window(750, 650, anchor=NW, window=self.finalProceed)

            self.checkSimilarity()

        except Exception as ex:
            template = "An exception of type {0} occurred. Details:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            self.errorObj.genericError(message)

    def verifyWatermarkGUI(self):

        try:
            # GUI COnfigurations for Complete Verification window

            self.signMatching_toplevel.withdraw()
            self.watermarkTL_toplevel = Toplevel()
            self.watermarkTL_toplevel.attributes("-topmost",True)
            self.watermarkTL_toplevel.wm_title("Verify Watermark")
            self.watermarkTL_width = 750
            self.watermarkTL_height = 700
            self.watermarkTL_ws = self.watermarkTL_toplevel.winfo_screenwidth()
            self.watermarkTL_hs = self.watermarkTL_toplevel.winfo_screenheight()
            self.x = (self.watermarkTL_ws / 2) - (self.watermarkTL_width / 2)
            self.y = (self.watermarkTL_hs / 2) - (self.watermarkTL_height / 2)
            self.watermarkTL_toplevel.geometry(
                '%dx%d+%d+%d' % (self.watermarkTL_width, self.watermarkTL_height, self.x, self.y))
            self.watermarkTL_toplevel.config(background="#CCD1D1")
            self.watermarkTL_toplevel.option_add("*Font", "Courier 12 bold ")

            self.watermarkTL_toplevel.option_add("*Button.Font", "Courier 12 bold")
            self.watermarkTL_toplevel.option_add("*Button.Background", "#1F618D")
            self.watermarkTL_toplevel.option_add("*Button.Foreground", "#A9CCE3")

            self.watermarkTL_toplevel.option_add("*Label.Font", "Courier 11 bold")
            self.watermarkTL_toplevel.option_add("*Label.Background", "#1F618D")
            self.watermarkTL_toplevel.option_add("*Label.Foreground", "#A9CCE3")
            self.watermarkTL_toplevel.option_add("*Label.bd", 10)
            self.watermarkTL_toplevel.option_add("*Label.Relief", "ridge")

            self.watermarkTL_canvas = Canvas(self.watermarkTL_toplevel, width=1500, height=700)
            self.watermarkTL_canvas.config(background="#CCD1D1")
            self.watermarkTL_canvas.grid(row=0, column=1, columnspan=3)

            self.watermarkTL_back_button = Button(self.watermarkTL_toplevel, text="<<<Back",command=lambda: self.backObj.backButton(self.watermarkTL_toplevel,self.signMatching_toplevel))
            self.watermarkTL_back_button.grid()
            self.watermarkTL_back_button_windows = self.watermarkTL_canvas.create_window(25, 650, anchor=NW,
                                                                                         window=self.watermarkTL_back_button)

            self.backToMainBttn= Button(self.watermarkTL_toplevel, text="Return to Main>>>", command=self.backToMain)
            self.backToMainBttn.grid(row=8, column=3)
            self.backToMainBttn_window = self.watermarkTL_canvas.create_window(500, 650, anchor=NW,
                                                                             window=self.backToMainBttn)
            self.finalScanImg = uploadImg(self.db_getImgPath)
            self.finalScanSign = uploadImg(self.db_getSignPath)
            self.ttkScanImg = self.finalScanImg.uploadResized(200, 250)
            self.ttkSignImg = self.finalScanSign.uploadResized(350, 100)

            self.successPath = uploadImg('check.png')
            self.failPath = uploadImg('fail2.png')
            self.success = self.successPath.uploadResized(100, 100)
            self.fail = self.failPath.uploadResized(100, 100)


            if len(self.kp_pair)>=100:


                self.facialProfileLbl = Label(self.watermarkTL_toplevel, text="Facial Profile Verification Successful")
                self.facialProfileLbl.grid()
                self.facialProfileLbl.config(font=('Courier', 16),bg="#2ECC71",fg="#0B5345  ")
                self.facialProfileLbl_window = self.watermarkTL_canvas.create_window(125, 25, anchor=NW,
                                                                                     window=self.facialProfileLbl)

                self.finalProfile= self.watermarkTL_canvas.create_image(265,75, image=self.ttkScanImg, anchor='nw')
                self.watermarkTL_canvas.grid()
                self.watermarkTL_canvas.image = self.ttkScanImg

                self.successProfile = self.watermarkTL_canvas.create_image(310, 172, image=self.success, anchor='nw')
                self.watermarkTL_canvas.grid()
                self.watermarkTL_canvas.image = self.success

            else:
                self.facialProfileLbl = Label(self.watermarkTL_toplevel, text="Facial Profile Verification Unsuccessful")
                self.facialProfileLbl.grid()
                self.facialProfileLbl.config(font=('Courier', 16), bg="red", fg="white")
                self.facialProfileLbl_window = self.watermarkTL_canvas.create_window(125, 25, anchor=NW,
                                                                                     window=self.facialProfileLbl)

                self.finalProfile = self.watermarkTL_canvas.create_image(265, 75, image=self.ttkScanImg, anchor='nw')
                self.watermarkTL_canvas.grid()
                self.watermarkTL_canvas.image = self.ttkScanImg

                self.failProfile = self.watermarkTL_canvas.create_image(310, 172, image=self.fail, anchor='nw')
                self.watermarkTL_canvas.grid()
                self.watermarkTL_canvas.image = self.fail

            if len(self.kp_pair_sign)>=70:

                self.signProfileLbl = Label(self.watermarkTL_toplevel, text="Signature Profile Verification Successful")
                self.signProfileLbl.grid()
                self.signProfileLbl.config(font=('Courier', 16), bg="#2ECC71", fg="#0B5345  ")
                self.signProfileLbl_window = self.watermarkTL_canvas.create_window(100, 350, anchor=NW,
                                                                                     window=self.signProfileLbl)

                self.finalSignature = self.watermarkTL_canvas.create_image(200, 400, image=self.ttkSignImg, anchor='nw')
                self.watermarkTL_canvas.grid()
                self.watermarkTL_canvas.image = self.ttkSignImg

                self.successSign = self.watermarkTL_canvas.create_image(325, 405, image=self.success, anchor='nw')
                self.watermarkTL_canvas.grid()
                self.watermarkTL_canvas.image = self.success

            else:
                self.signProfileLbl = Label(self.watermarkTL_toplevel, text="Signature Profile Verification Unsuccessful")
                self.signProfileLbl.grid()
                self.signProfileLbl.config(font=('Courier', 16), bg="red", fg="white")
                self.signProfileLbl_window = self.watermarkTL_canvas.create_window(100, 350, anchor=NW,
                                                                                   window=self.signProfileLbl)

                self.finalSignature = self.watermarkTL_canvas.create_image(200, 400, image=self.ttkSignImg, anchor='nw')
                self.watermarkTL_canvas.grid()
                self.watermarkTL_canvas.image = self.ttkSignImg

                self.failSign = self.watermarkTL_canvas.create_image(325, 405, image=self.fail, anchor='nw')
                self.watermarkTL_canvas.grid()
                self.watermarkTL_canvas.image = self.fail

            self.result=verifyWatermark(self.verify_Pass_No.get().upper())

            if self.result:

                self.verifyWatermarkLbl = Label(self.watermarkTL_toplevel, text="Watermark Verification Successful")
                self.verifyWatermarkLbl.grid()
                self.verifyWatermarkLbl.config(font=('Courier', 16), bg="#2ECC71", fg="#0B5345")
                self.verifyWatermarkLbl_window = self.watermarkTL_canvas.create_window(100, 550, anchor=NW,
                                                                                   window=self.verifyWatermarkLbl)

                self.successWM = self.watermarkTL_canvas.create_image(575, 515, image=self.success, anchor='nw')
                self.watermarkTL_canvas.grid()
                self.watermarkTL_canvas.image = self.success

            else:
                self.verifyWatermarkLbl = Label(self.watermarkTL_toplevel, text="Watermark Verification Unsuccessful")
                self.verifyWatermarkLbl.grid()
                self.verifyWatermarkLbl.config(font=('Courier', 16), bg="red", fg="white")
                self.verifyWatermarkLbl_window = self.watermarkTL_canvas.create_window(100, 550, anchor=NW,
                                                                                       window=self.verifyWatermarkLbl)

                self.failWM = self.watermarkTL_canvas.create_image(575, 515, image=self.fail, anchor='nw')
                self.watermarkTL_canvas.grid()
                self.watermarkTL_canvas.image = self.fail


        except Exception as ex:
            template = "An exception of type {0} occurred. Details:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            self.errorObj.genericError(message)



    def verifyDBInfo(self):

        try:
            """ conn = mysql.connector.connect(user='bwimad', passwd='#######', host='64.62.211.131',
                                                           database="bwimad_fyp")"""
            conn = mysql.connector.connect(user='root', passwd='root', host='localhost', database="fyp",
                                                port=3306)
        except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    self.errorObj.dbAccessDenied()
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    self.errorObj.genericError("Database DOES NOT Exist!")
                else:
                    self.errorObj.genericError(err)
        try:

            cur = conn.cursor()

            self.passportNumber = self.verify_Pass_No.get().upper()

            #Accesses central database and retrieves information using passport number as reference

            self.ref_pass_no= "SELECT pass_no FROM passport_holders WHERE pass_no='%s'" % \
                             (self.passportNumber)
            cur.execute(self.ref_pass_no)

            self.db_getPassNum = cur.fetchone()[0]

            self.ref_first= "SELECT first FROM passport_holders WHERE pass_no='%s'" % \
                                (self.passportNumber)
            cur.execute(self.ref_first)
            self.db_getFirst = cur.fetchone()[0]

            print self.db_getFirst

            self.ref_second="SELECT second FROM passport_holders WHERE pass_no='%s'" % \
                                (self.passportNumber)
            cur.execute(self.ref_second)
            self.db_getSecond = cur.fetchone()[0]
            if self.db_getSecond == '*OPTIONAL':
                self.db_getSecond = 'NONE'

            self.ref_third = "SELECT third FROM passport_holders WHERE pass_no='%s'" % \
                              (self.passportNumber)
            cur.execute(self.ref_third)
            self.db_getThird = cur.fetchone()[0]
            if self.db_getThird == '*OPTIONAL':
                self.db_getThird = 'NONE'

            self.ref_family = "SELECT last FROM passport_holders WHERE pass_no='%s'" % \
                             (self.passportNumber)
            cur.execute(self.ref_family)
            self.db_getLast = cur.fetchone()[0]

            self.ref_gender = "SELECT gender FROM passport_holders WHERE pass_no='%s'" % \
                             (self.passportNumber)
            cur.execute(self.ref_gender)
            self.db_getGen = cur.fetchone()[0]

            self.ref_DOB = "SELECT DOB FROM passport_holders WHERE pass_no='%s'" % \
                             (self.passportNumber)
            cur.execute(self.ref_DOB)
            self.db_getDOB = cur.fetchone()[0]

            self.ref_POB= "SELECT POB FROM passport_holders WHERE pass_no='%s'" % \
                             (self.passportNumber)
            cur.execute(self.ref_POB)
            self.db_getPOB = cur.fetchone()[0]

            self.ref_profession= "SELECT profession FROM passport_holders WHERE pass_no='%s'" % \
                             (self.passportNumber)
            cur.execute(self.ref_profession)
            self.db_getProf = cur.fetchone()[0]

            self.ref_NIC = "SELECT NIC FROM passport_holders WHERE pass_no='%s'" % \
                             (self.passportNumber)
            cur.execute(self.ref_NIC)
            self.db_getNIC = cur.fetchone()[0]

            self.ref_Type= "SELECT type FROM passport_holders WHERE pass_no='%s'" % \
                             (self.passportNumber)
            cur.execute(self.ref_Type)
            self.db_getType = cur.fetchone()[0]

            self.ref_Nation = "SELECT nation FROM passport_holders WHERE pass_no='%s'" % \
                             (self.passportNumber)
            cur.execute(self.ref_Nation)
            self.db_getNation = cur.fetchone()[0]

            self.ref_Issued = "SELECT issued FROM passport_holders WHERE pass_no='%s'" % \
                             (self.passportNumber)
            cur.execute(self.ref_Issued)
            self.db_getIssued = cur.fetchone()[0]

            self.ref_Expired= "SELECT expired FROM passport_holders WHERE pass_no='%s'" % \
                             (self.passportNumber)
            cur.execute(self.ref_Expired)
            self.db_getExpired = cur.fetchone()[0]

            self.ref_Image = "SELECT imagePath FROM passport_holders WHERE pass_no='%s'" % \
                               (self.passportNumber)
            cur.execute(self.ref_Image)
            self.db_getImgPath = cur.fetchone()[0]


            self.ref_Signature = "SELECT signaturePath FROM passport_holders WHERE pass_no='%s'" % \
                               (self.passportNumber)
            cur.execute(self.ref_Signature)
            self.db_getSignPath= cur.fetchone()[0]

            cur.close()
            conn.close()



        except Exception as ex:

            template = "An exception of type {0} occurred. Details:\n{1!r}"

            message = template.format(type(ex).__name__, ex.args)

            self.errorObj.genericError(message)

        try:
            #Inserts the database image and signature into the GUI
            self.Img_width = 132
            self.Img_height = 170
            self.Sign_width = 250
            self.Sign_height = 50

            self.imgObj=uploadImg(self.db_getImgPath)
            self.signObj=uploadImg(self.db_getSignPath)


            self.ttkdb_img=self.imgObj.uploadResized(self.Img_width,self.Img_height)

            self.ttkdb_sign = self.signObj.uploadResized(self.Sign_width, self.Sign_height )

            self.db_img=self.db_tag_canvas.create_image(25, 60, image=self.ttkdb_img, anchor='nw')
            self.db_tag_canvas.grid()
            self.db_tag_canvas.image = self.ttkdb_img

            self.db_sign=self.db_tag_canvas.create_image(400, 520, image=self.ttkdb_sign, anchor='nw')
            self.db_tag_canvas.grid()
            self.db_tag_canvas.image = self.ttkdb_sign



        except Exception as ex:

            template = "An exception of type {0} occurred. Details:\n{1!r}"

            message = template.format(type(ex).__name__, ex.args)

            self.errorObj.genericError(message)


        try:
            #Inserts database information into the GUI
            self.dbLabel=Label(self.db_tag_canvas,text=self.db_getPassNum)
            self.dbLabel.grid()
            self.dbLabel.config(font=("Courier", 16), bg="#4A235A", fg="white")
            self.dbLabel_windows = self.db_tag_canvas.create_window(300, 20, anchor=NW, window=self.dbLabel)

            self.dbFirst.delete(0, END)
            self.dbFirst.insert(INSERT, self.db_getFirst)
            self.dbFirst.config(state="disabled")

            self.dbsecondEntry.delete(0, END)
            self.dbsecondEntry.insert(INSERT, self.db_getSecond)
            self.dbsecondEntry.config(state="disabled")

            self.dbeThird.delete(0, END)
            self.dbeThird.insert(INSERT, self.db_getThird)
            self.dbeThird.config(state="disabled")

            self.dbeFamily.delete(0, END)
            self.dbeFamily.insert(INSERT, self.db_getLast)
            self.dbeFamily.config(state="disabled")

            self.dbgenderDropdown.delete(0, END)
            self.dbgenderDropdown.insert(INSERT, self.db_getGen)
            self.dbgenderDropdown.config(state="disabled")

            self.dbdobEntry.delete(0, END)
            self.dbdobEntry.insert(INSERT, self.db_getDOB)
            self.dbdobEntry.config(state="disabled")

            self.dbpobEntry.delete(0, END)
            self.dbpobEntry.insert(INSERT, self.db_getPOB)
            self.dbpobEntry.config(state="disabled")

            self.dbprofessionEntry.delete(0, END)
            self.dbprofessionEntry.insert(INSERT, self.db_getProf)
            self.dbprofessionEntry.config(state="disabled")

            self.dbnicEntry.delete(0, END)
            self.dbnicEntry.insert(INSERT, self.db_getNIC)
            self.dbnicEntry.config(state="disabled")

            self.dbtypeEntry.delete(0, END)
            self.dbtypeEntry.insert(INSERT, self.db_getType)
            self.dbtypeEntry.config(state="disabled")

            self.dbstatusEntry.delete(0, END)
            self.dbstatusEntry.insert(INSERT, self.db_getNation)
            self.dbstatusEntry.config(state="disabled")

            self.dbissuedEntry.delete(0, END)
            self.dbissuedEntry.insert(INSERT, self.db_getIssued)
            self.dbissuedEntry.config(state="disabled")

            self.dbexpiredEntry.delete(0, END)
            self.dbexpiredEntry.insert(INSERT, self.db_getExpired)
            self.dbexpiredEntry.config(state="disabled")


        except Exception as ex:

            template = "An exception of type {0} occurred. Details:\n{1!r}"

            message = template.format(type(ex).__name__, ex.args)

            self.errorObj.genericError(message)

    def verifyTag_Info(self):

            #Directory containing RFID files
            self.RFIDdir = 'C:/Users/BHAGYA/Dropbox/fyp/.idea/rfid_files/'
            self.rfid_suffix = 'txt'

            #conn = mysql.connector
            try:
                conn = mysql.connector.connect(user='bwimad', passwd='########', host='64.62.211.131',
                                               database="bwimad_fyp")
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    self.errorObj.dbAccessDenied()
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    self.errorObj.genericError("Database DOES NOT Exist!")
                else:
                    self.errorObj.genericError(err)
            try:

                cur = conn.cursor()

                self.passportNumber = self.verify_Pass_No.get().upper()

                #Acquires the password from the database that was used for AES encryption of RFID data
                self.get_password = "SELECT password FROM watermarking_info WHERE pass_no='%s'" % \
                                    (self.passportNumber)
                cur.execute(self.get_password)
                self.tag_password = cur.fetchone()[0]

                cur.close()
                conn.close()

                #Open file that is saved using the passport number
                self.fileOpen = open(os.path.join(self.RFIDdir, self.passportNumber + "." + self.rfid_suffix), 'r')

                if self.fileOpen:
                    #Decrypts each line in the opened file
                    self.aesDECObj = AESCipher(self.tag_password)

                    self.readImgPath = self.fileOpen.readline()
                    self.decryptedImgPath = self.aesDECObj.decryptAES(self.readImgPath)

                    self.readSignPath = self.fileOpen.readline()
                    self.decryptedSignPath = self.aesDECObj.decryptAES(self.readSignPath)

                    self.readPassport = self.fileOpen.readline()
                    self.decryptedPassport = self.aesDECObj.decryptAES(self.readPassport)

                    self.readFirst = self.fileOpen.readline()
                    self.decryptedFirst = self.aesDECObj.decryptAES(self.readFirst)

                    self.readSecond = self.fileOpen.readline()
                    self.decryptedSecond = self.aesDECObj.decryptAES(self.readSecond)

                    if self.decryptedSecond == '*OPTIONAL':
                        self.decryptedSecond = 'NONE'

                    self.readThird = self.fileOpen.readline()
                    self.decryptedThird = self.aesDECObj.decryptAES(self.readThird)
                    if self.decryptedThird == '*OPTIONAL':
                        self.decryptedThird = 'NONE'

                    self.readLast = self.fileOpen.readline()
                    self.decryptedLast = self.aesDECObj.decryptAES(self.readLast)

                    self.readGen = self.fileOpen.readline()
                    self.decryptedGen = self.aesDECObj.decryptAES(self.readGen)

                    self.readDOB = self.fileOpen.readline()
                    self.decryptedDOB = self.aesDECObj.decryptAES(self.readDOB)

                    self.readPOB = self.fileOpen.readline()
                    self.decryptedPOB = self.aesDECObj.decryptAES(self.readPOB)

                    self.readProf = self.fileOpen.readline()
                    self.decryptedProf = self.aesDECObj.decryptAES(self.readProf)

                    self.readNIC = self.fileOpen.readline()
                    self.decryptedNIC = self.aesDECObj.decryptAES(self.readNIC)

                    self.readType = self.fileOpen.readline()
                    self.decryptedType = self.aesDECObj.decryptAES(self.readType)

                    self.readNation = self.fileOpen.readline()
                    self.decryptedNation = self.aesDECObj.decryptAES(self.readNation)

                    self.readIssued = self.fileOpen.readline()
                    self.decryptedIssued = self.aesDECObj.decryptAES(self.readIssued)

                    self.readExpired = self.fileOpen.readline()
                    self.decryptedExpired = self.aesDECObj.decryptAES(self.readExpired)

                else:
                    self.errorObj.tagNotFound()

            except Exception as ex:
                    template = "An exception of type {0} occurred. Details:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    self.errorObj.genericError(message)




            try:
               #Inserting tag image onto GUI
                self.tagImg_width = 132
                self.tagImg_height = 170
                self.tagSign_width = 250
                self.tagSign_height = 50

                self.tagImgObj = uploadImg(self.decryptedImgPath)
                self.tagSignObj = uploadImg(self.decryptedSignPath)

                self.ttktag_img = self.tagImgObj.uploadResized(self.tagImg_width, self.tagImg_height)

                self.ttktag_sign = self.signObj.uploadResized(self.tagSign_width, self.tagSign_height)

                self.tag_img=self.db_tag_canvas.create_image(800, 60, image=self.ttktag_img, anchor='nw')
                self.db_tag_canvas.grid()
                self.db_tag_canvas.image = self.ttkdb_img

                self.tag_sign=self.db_tag_canvas.create_image(1175, 520, image=self.ttktag_sign, anchor='nw')
                self.db_tag_canvas.grid()
                self.db_tag_canvas.image = self.ttkdb_sign



            except Exception as ex:

                template = "An exception of type {0} occurred. Details:\n{1!r}"

                message = template.format(type(ex).__name__, ex.args)

                self.errorObj.genericError(message)



            try:
                self.tag_passport= Label(self.db_tag_toplevel, text=self.decryptedPassport)
                self.tag_passport.grid()
                self.tag_passport.config(font=("Courier", 16), bg="#154360", fg="white")
                self.tag_passport_windows = self.db_tag_canvas.create_window(1010, 20, anchor=NW, window=self.tag_passport)

                #Inserting Information into the GUI
                self.tagFirst.delete(0, END)
                self.tagFirst.insert(INSERT, self.decryptedFirst)
                self.tagFirst.config(state="disabled")

                self.tagsecondEntry.delete(0, END)
                self.tagsecondEntry.insert(INSERT, self.decryptedSecond)
                self.tagsecondEntry.config(state="disabled")

                self.tageThird.delete(0, END)
                self.tageThird.insert(INSERT, self.decryptedThird)
                self.tageThird.config(state="disabled")

                self.tageFamily.delete(0, END)
                self.tageFamily.insert(INSERT, self.decryptedLast)
                self.tageFamily.config(state="disabled")

                self.taggenderDropdown.delete(0, END)
                self.taggenderDropdown.insert(INSERT, self.decryptedGen)
                self.taggenderDropdown.config(state="disabled")

                self.tagdobEntry.delete(0, END)
                self.tagdobEntry.insert(INSERT, self.decryptedDOB)
                self.tagdobEntry.config(state="disabled")

                self.tagpobEntry.delete(0, END)
                self.tagpobEntry.insert(INSERT, self.decryptedPOB)
                self.tagpobEntry.config(state="disabled")

                self.tagprofessionEntry.delete(0, END)
                self.tagprofessionEntry.insert(INSERT, self.decryptedProf)
                self.tagprofessionEntry.config(state="disabled")

                self.tagnicEntry.delete(0, END)
                self.tagnicEntry.insert(INSERT, self.decryptedNIC)
                self.tagnicEntry.config(state="disabled")

                self.tagtypeEntry.delete(0, END)
                self.tagtypeEntry.insert(INSERT, self.decryptedType)
                self.tagtypeEntry.config(state="disabled")

                self.tagstatusEntry.delete(0, END)
                self.tagstatusEntry.insert(INSERT, self.decryptedNation)
                self.tagstatusEntry.config(state="disabled")

                self.tagissuedEntry.delete(0, END)
                self.tagissuedEntry.insert(INSERT, self.decryptedIssued)
                self.tagissuedEntry.config(state="disabled")

                self.tagexpiredEntry.delete(0, END)
                self.tagexpiredEntry.insert(INSERT, self.decryptedExpired)
                self.tagexpiredEntry.config(state="disabled")




            except Exception as ex:

                template = "An exception of type {0} occurred. Details:\n{1!r}"

                message = template.format(type(ex).__name__, ex.args)

                self.errorObj.genericError(message)



    def showDB_TAG(self):

        #GUI configurations for Database and RFID tag comparison window

        try:
            self.validateInputs = InputValidation()

            if self.verify_Pass_No.get()!= "":

                self.passNum_validated=self.validateInputs.validatePassport(self.verify_Pass_No.get().upper())
                if self.verifyPath != ""  and self.passNum_validated:
                    # GUI COnfigurations
                    root.withdraw()
                    self.db_tag_toplevel = Toplevel()
                    self.db_tag_toplevel.wm_title("Database and Tag Information")
                    self.db_tag_toplevel.attributes('-topmost',True)
                    self.db_tag_width = 1500
                    self.db_tag_height = 700
                    self.db_tag_ws = self.db_tag_toplevel.winfo_screenwidth()
                    self.db_tag_hs = self.db_tag_toplevel.winfo_screenheight()
                    self.x = (self.db_tag_ws / 2) - (self.db_tag_width / 2)
                    self.y = (self.db_tag_hs / 2) - (self.db_tag_height / 2)
                    self.db_tag_toplevel.geometry('%dx%d+%d+%d' % (self.db_tag_width, self.db_tag_height, self.x, self.y))
                    self.db_tag_toplevel.config(background="#CCD1D1")
                    self.db_tag_toplevel.option_add("*Font", "Courier 12 bold ")

                    self.db_tag_toplevel.option_add("*Button.Font", "Courier 12 bold")
                    self.db_tag_toplevel.option_add("*Button.Background", "#1F618D")
                    self.db_tag_toplevel.option_add("*Button.Foreground", "#A9CCE3")

                    self.db_tag_toplevel.option_add("*Label.Font", "Courier 11 bold")
                    self.db_tag_toplevel.option_add("*Label.Background", "#1F618D")
                    self.db_tag_toplevel.option_add("*Label.Foreground", "#A9CCE3")
                    self.db_tag_toplevel.option_add("*Label.bd", 10)
                    self.db_tag_toplevel.option_add("*Label.Relief", "ridge")

                    self.db_tag_canvas = Canvas(self.db_tag_toplevel, width=1500, height=700)
                    self.db_tag_canvas.config(background="#CCD1D1")
                    self.db_tag_canvas.grid(row=0, column=1, columnspan=3)

                    self.db_label = Label(self.db_tag_toplevel, text="Database Information")
                    self.db_label.grid()
                    self.db_label.config(font=("Courier", 16), bg="#4A235A", fg="white")
                    self.db_label_windows = self.db_tag_canvas.create_window(25, 20, anchor=NW, window=self.db_label)

                    self.tag_label = Label(self.db_tag_toplevel, text="Tag Information")
                    self.tag_label.grid()
                    self.tag_label.config(font=("Courier", 16), bg="#154360", fg="white")
                    self.tag_label_windows = self.db_tag_canvas.create_window(800, 20, anchor=NW, window=self.tag_label)

                    self.back_button = Button(self.db_tag_toplevel, text="<<<Back",
                                              command=lambda: self.backObj.backButton(self.db_tag_toplevel, root))
                    self.back_button.grid()
                    self.back_button_windows = self.db_tag_canvas.create_window(25, 650, anchor=NW, window=self.back_button)

                    self.validate_button = Button(self.db_tag_toplevel, text="Validate Facial Photograph>>>",
                                                  command=self.facialSimilarityGUI)
                    self.validate_button.grid()
                    self.validate_button_windows = self.db_tag_canvas.create_window(1150, 650, anchor=NW,
                                                                                    window=self.validate_button)

                    self.dbfirstLabel = Label(self.db_tag_toplevel, text="First Name :")
                    self.dbfirstLabel.grid(row=2, column=0)
                    self.dbfirstLabel.config(bg="#4A235A", fg="white")
                    self.dbfirstLabel_window = self.db_tag_canvas.create_window(25, 250, anchor=NW,
                                                                                window=self.dbfirstLabel)

                    self.dbFirst = Entry(self.db_tag_toplevel)
                    self.dbFirst.grid(row=2, column=4)
                    self.dbFirst_window = self.db_tag_canvas.create_window(140, 250, anchor=NW, window=self.dbFirst)

                    self.dbsecondLabel = Label(self.db_tag_toplevel, text="Second Name:")
                    self.dbsecondLabel.grid(row=3, column=0)
                    self.dbsecondLabel.config(bg="#4A235A", fg="white")
                    self.dblabel_window = self.db_tag_canvas.create_window(25, 300, anchor=NW, window=self.dbsecondLabel)
                    self.dbsecondEntry = Entry(self.db_tag_toplevel, fg="#922B21")
                    self.dbsecondEntry.grid(row=3, column=1)
                    self.dbsecondEntry_window = self.db_tag_canvas.create_window(140, 300, anchor=NW,
                                                                                 window=self.dbsecondEntry)

                    self.dbthirdLabel = Label(self.db_tag_toplevel, text="Third Name :")
                    self.dbthirdLabel.grid(row=4, column=0)
                    self.dbthirdLabel.config(bg="#4A235A", fg="white")
                    self.dbthirdLabel_window = self.db_tag_canvas.create_window(25, 350, anchor=NW,
                                                                                window=self.dbthirdLabel)
                    self.dbeThird = Entry(self.db_tag_toplevel, fg="#922B21")
                    self.dbeThird.grid(row=4, column=1)
                    self.dbeThird_window = self.db_tag_canvas.create_window(140, 350, anchor=NW, window=self.dbeThird)

                    self.dbfamilyLabel = Label(self.db_tag_toplevel, text="Last Name  :")
                    self.dbfamilyLabel.grid(row=5, column=0)
                    self.dbfamilyLabel.config(bg="#4A235A", fg="white")
                    self.dbfamilyLabel_window = self.db_tag_canvas.create_window(25, 400, anchor=NW,
                                                                                 window=self.dbfamilyLabel)
                    self.dbeFamily = Entry(self.db_tag_toplevel)
                    self.dbeFamily.grid(row=5, column=1)
                    self.dbeFamily_window = self.db_tag_canvas.create_window(140, 400, anchor=NW, window=self.dbeFamily)

                    self.dbgenderLabel = Label(self.db_tag_toplevel, text="Gender\t   :")
                    self.dbgenderLabel.grid(row=7, column=0)
                    self.dbgenderLabel.config(bg="#4A235A", fg="white")
                    self.dbgenderLabel_window = self.db_tag_canvas.create_window(25, 450, anchor=NW,
                                                                                 window=self.dbgenderLabel)
                    self.dbgenderDropdown = Entry(self.db_tag_toplevel)
                    self.dbgenderDropdown.grid(row=7, column=1)
                    self.dbgenderDropdown_window = self.db_tag_canvas.create_window(140, 450, anchor=NW,
                                                                                    window=self.dbgenderDropdown)

                    self.dbdobLabel = Label(self.db_tag_toplevel, text="DOB\t   :")
                    self.dbdobLabel.grid(row=8, column=0)
                    self.dbdobLabel.config(bg="#4A235A", fg="white")
                    self.dbdobLabel_window = self.db_tag_canvas.create_window(25, 500, anchor=NW, window=self.dbdobLabel)
                    self.dbdobEntry = Entry(self.db_tag_toplevel)
                    self.dbdobEntry.grid(row=8, column=1)
                    self.dbdobEntry_window = self.db_tag_canvas.create_window(140, 500, anchor=NW, window=self.dbdobEntry)

                    self.dbpobLabel = Label(self.db_tag_toplevel, text="POB\t   :")
                    self.dbpobLabel.grid()
                    self.dbpobLabel.config(bg="#4A235A", fg="white")
                    self.dbpobLabel_window = self.db_tag_canvas.create_window(25, 550, anchor=NW, window=self.dbpobLabel)
                    self.dbpobEntry = Entry(self.db_tag_toplevel)
                    self.dbpobEntry.grid()
                    self.dbpobEntry_window = self.db_tag_canvas.create_window(140, 550, anchor=NW, window=self.dbpobEntry)

                    self.dbprofessionLabel = Label(self.db_tag_toplevel, text="Profession :")
                    self.dbprofessionLabel.grid()
                    self.dbprofessionLabel.config(bg="#4A235A", fg="white")
                    self.dbprofessionLabel_window = self.db_tag_canvas.create_window(25, 600, anchor=NW,
                                                                                     window=self.dbprofessionLabel)
                    self.dbprofessionEntry = Entry(self.db_tag_toplevel)
                    self.dbprofessionEntry.grid()
                    self.dbprofessionEntry_window = self.db_tag_canvas.create_window(140, 600, anchor=NW,
                                                                                     window=self.dbprofessionEntry)

                    self.dbnicLabel = Label(self.db_tag_toplevel, text="NIC Number :")
                    self.dbnicLabel.grid()
                    self.dbnicLabel.config(bg="#4A235A", fg="white")
                    self.dbnicLabel_window = self.db_tag_canvas.create_window(365, 250, anchor=NW, window=self.dbnicLabel)
                    self.dbnicEntry = Entry(self.db_tag_toplevel)
                    self.dbnicEntry.grid()
                    self.dbnicEntry_window = self.db_tag_canvas.create_window(480, 250, anchor=NW, window=self.dbnicEntry)

                    self.dbtypeLabel = Label(self.db_tag_toplevel, text="Type\t   :")
                    self.dbtypeLabel.grid()
                    self.dbtypeLabel.config(bg="#4A235A", fg="white")
                    self.dbtypeLabel_window = self.db_tag_canvas.create_window(365, 300, anchor=NW, window=self.dbtypeLabel)
                    self.dbtypeEntry = Entry(self.db_tag_toplevel)
                    self.dbtypeEntry.grid()
                    self.dbtypeEntry_window = self.db_tag_canvas.create_window(480, 300, anchor=NW, window=self.dbtypeEntry)

                    self.dbstatusLabel = Label(self.db_tag_toplevel, text="Nationality:")
                    self.dbstatusLabel.grid()
                    self.dbstatusLabel.config(bg="#4A235A", fg="white")
                    self.dbstatusLabel_window = self.db_tag_canvas.create_window(365, 350, anchor=NW,
                                                                                 window=self.dbstatusLabel)
                    self.dbstatusEntry = Entry(self.db_tag_toplevel)
                    self.dbstatusEntry.grid()
                    self.dbstatusEntry_window = self.db_tag_canvas.create_window(480, 350, anchor=NW,
                                                                                 window=self.dbstatusEntry)

                    self.dbissuedLabel = Label(self.db_tag_toplevel, text="Issued On  :")
                    self.dbissuedLabel.grid()
                    self.dbissuedLabel.config(bg="#4A235A", fg="white")
                    self.dbissuedLabel_window = self.db_tag_canvas.create_window(365, 400, anchor=NW,
                                                                                 window=self.dbissuedLabel)
                    self.dbissuedEntry = Entry(self.db_tag_toplevel)
                    self.dbissuedEntry.grid()
                    self.dbissuedEntry_window = self.db_tag_canvas.create_window(480, 400, anchor=NW,
                                                                                 window=self.dbissuedEntry)

                    self.dbexpiredLabel = Label(self.db_tag_toplevel, text="Expires On :")
                    self.dbexpiredLabel.grid()
                    self.dbexpiredLabel.config(bg="#4A235A", fg="white")
                    self.dbexpiredLabel_window = self.db_tag_canvas.create_window(365, 450, anchor=NW,
                                                                                  window=self.dbexpiredLabel)
                    self.dbexpiredEntry = Entry(self.db_tag_toplevel)
                    self.dbexpiredEntry.grid()
                    self.dbexpiredEntry_window = self.db_tag_canvas.create_window(480, 450, anchor=NW,
                                                                                  window=self.dbexpiredEntry)

                    self.tagfirstLabel = Label(self.db_tag_toplevel, text="First Name :")
                    self.tagfirstLabel.grid(row=2, column=0)
                    self.tagfirstLabel.config(bg="#154360", fg="white")
                    self.tagfirstLabel_window = self.db_tag_canvas.create_window(800, 250, anchor=NW,
                                                                                 window=self.tagfirstLabel)

                    self.tagFirst = Entry(self.db_tag_toplevel)
                    self.tagFirst.grid(row=2, column=4)
                    self.tagFirst_window = self.db_tag_canvas.create_window(915, 250, anchor=NW, window=self.tagFirst)

                    self.tagsecondLabel = Label(self.db_tag_toplevel, text="Second Name:")
                    self.tagsecondLabel.grid(row=3, column=0)
                    self.tagsecondLabel.config(bg="#154360", fg="white")
                    self.taglabel_window = self.db_tag_canvas.create_window(800, 300, anchor=NW, window=self.tagsecondLabel)
                    self.tagsecondEntry = Entry(self.db_tag_toplevel, fg="#922B21")
                    self.tagsecondEntry.grid(row=3, column=1)
                    self.tagsecondEntry_window = self.db_tag_canvas.create_window(915, 300, anchor=NW,
                                                                                  window=self.tagsecondEntry)

                    self.tagthirdLabel = Label(self.db_tag_toplevel, text="Third Name :")
                    self.tagthirdLabel.grid(row=4, column=0)
                    self.tagthirdLabel.config(bg="#154360", fg="white")
                    self.tagthirdLabel_window = self.db_tag_canvas.create_window(800, 350, anchor=NW,
                                                                                 window=self.tagthirdLabel)
                    self.tageThird = Entry(self.db_tag_toplevel, fg="#922B21")
                    self.tageThird.grid(row=4, column=1)
                    self.tageThird_window = self.db_tag_canvas.create_window(915, 350, anchor=NW, window=self.tageThird)

                    self.tagfamilyLabel = Label(self.db_tag_toplevel, text="Last Name  :")
                    self.tagfamilyLabel.grid(row=5, column=0)
                    self.tagfamilyLabel.config(bg="#154360", fg="white")
                    self.tagfamilyLabel_window = self.db_tag_canvas.create_window(800, 400, anchor=NW,
                                                                                  window=self.tagfamilyLabel)
                    self.tageFamily = Entry(self.db_tag_toplevel)
                    self.tageFamily.grid(row=5, column=1)
                    self.tageFamily_window = self.db_tag_canvas.create_window(915, 400, anchor=NW, window=self.tageFamily)

                    self.taggenderLabel = Label(self.db_tag_toplevel, text="Gender\t   :")
                    self.taggenderLabel.grid(row=7, column=0)
                    self.taggenderLabel.config(bg="#154360", fg="white")
                    self.taggenderLabel_window = self.db_tag_canvas.create_window(800, 450, anchor=NW,
                                                                                  window=self.taggenderLabel)
                    self.taggenderDropdown = Entry(self.db_tag_toplevel)
                    self.taggenderDropdown.grid(row=7, column=1)
                    self.taggenderDropdown_window = self.db_tag_canvas.create_window(915, 450, anchor=NW,
                                                                                     window=self.taggenderDropdown)

                    self.tagdobLabel = Label(self.db_tag_toplevel, text="DOB\t   :")
                    self.tagdobLabel.grid(row=8, column=0)
                    self.tagdobLabel.config(bg="#154360", fg="white")
                    self.tagdobLabel_window = self.db_tag_canvas.create_window(800, 500, anchor=NW, window=self.tagdobLabel)
                    self.tagdobEntry = Entry(self.db_tag_toplevel)
                    self.tagdobEntry.grid(row=8, column=1)
                    self.tagdobEntry_window = self.db_tag_canvas.create_window(915, 500, anchor=NW, window=self.tagdobEntry)

                    self.tagpobLabel = Label(self.db_tag_toplevel, text="POB\t   :")
                    self.tagpobLabel.grid()
                    self.tagpobLabel.config(bg="#154360", fg="white")
                    self.tagpobLabel_window = self.db_tag_canvas.create_window(800, 550, anchor=NW, window=self.tagpobLabel)
                    self.tagpobEntry = Entry(self.db_tag_toplevel)
                    self.tagpobEntry.grid()
                    self.tagpobEntry_window = self.db_tag_canvas.create_window(915, 550, anchor=NW, window=self.tagpobEntry)

                    self.tagprofessionLabel = Label(self.db_tag_toplevel, text="Profession :")
                    self.tagprofessionLabel.grid()
                    self.tagprofessionLabel.config(bg="#154360", fg="white")
                    self.tagprofessionLabel_window = self.db_tag_canvas.create_window(800, 600, anchor=NW,
                                                                                      window=self.tagprofessionLabel)
                    self.tagprofessionEntry = Entry(self.db_tag_toplevel)
                    self.tagprofessionEntry.grid()
                    self.tagprofessionEntry_window = self.db_tag_canvas.create_window(915, 600, anchor=NW,
                                                                                      window=self.tagprofessionEntry)

                    self.tagnicLabel = Label(self.db_tag_toplevel, text="NIC Number :")
                    self.tagnicLabel.grid()
                    self.tagnicLabel.config(bg="#154360", fg="white")
                    self.tagnicLabel_window = self.db_tag_canvas.create_window(1140, 250, anchor=NW,
                                                                               window=self.tagnicLabel)
                    self.tagnicEntry = Entry(self.db_tag_toplevel)
                    self.tagnicEntry.grid()
                    self.tagnicEntry_window = self.db_tag_canvas.create_window(1255, 250, anchor=NW,
                                                                               window=self.tagnicEntry)

                    self.tagtypeLabel = Label(self.db_tag_toplevel, text="Type\t   :")
                    self.tagtypeLabel.grid()
                    self.tagtypeLabel.config(bg="#154360", fg="white")
                    self.tagtypeLabel_window = self.db_tag_canvas.create_window(1140, 300, anchor=NW,
                                                                                window=self.tagtypeLabel)
                    self.tagtypeEntry = Entry(self.db_tag_toplevel)
                    self.tagtypeEntry.grid()
                    self.tagtypeEntry_window = self.db_tag_canvas.create_window(1255, 300, anchor=NW,
                                                                                window=self.tagtypeEntry)

                    self.tagstatusLabel = Label(self.db_tag_toplevel, text="Nationality:")
                    self.tagstatusLabel.grid()
                    self.tagstatusLabel.config(bg="#154360", fg="white")
                    self.tagstatusLabel_window = self.db_tag_canvas.create_window(1140, 350, anchor=NW,
                                                                                  window=self.tagstatusLabel)
                    self.tagstatusEntry = Entry(self.db_tag_toplevel)
                    self.tagstatusEntry.grid()
                    self.tagstatusEntry_window = self.db_tag_canvas.create_window(1255, 350, anchor=NW,
                                                                                  window=self.tagstatusEntry)

                    self.tagissuedLabel = Label(self.db_tag_toplevel, text="Issued On  :")
                    self.tagissuedLabel.grid()
                    self.tagissuedLabel.config(bg="#154360", fg="white")
                    self.tagissuedLabel_window = self.db_tag_canvas.create_window(1140, 400, anchor=NW,
                                                                                  window=self.tagissuedLabel)
                    self.tagissuedEntry = Entry(self.db_tag_toplevel)
                    self.tagissuedEntry.grid()
                    self.tagissuedEntry_window = self.db_tag_canvas.create_window(1255, 400, anchor=NW,
                                                                                  window=self.tagissuedEntry)

                    self.tagexpiredLabel = Label(self.db_tag_toplevel, text="Expires On :")
                    self.tagexpiredLabel.grid()
                    self.tagexpiredLabel.config(bg="#154360", fg="white")
                    self.tagexpiredLabel_window = self.db_tag_canvas.create_window(1140, 450, anchor=NW,
                                                                                   window=self.tagexpiredLabel)
                    self.tagexpiredEntry = Entry(self.db_tag_toplevel)
                    self.tagexpiredEntry.grid()
                    self.tagexpiredEntry_window = self.db_tag_canvas.create_window(1255, 450, anchor=NW,
                                                                                   window=self.tagexpiredEntry)

                    self.verifyDBInfo()
                    self.verifyTag_Info()

        except Exception as ex:
            template = "An exception of type {0} occurred. Details:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            self.errorObj.genericError(message)






    def __init__(self, root):
        #GUI configurations for start-up window
        try:
            root.config(background="#CCD1D1")
            root.option_add("*Font", "Courier 12 bold ")

            root.option_add("*Button.Font", "Courier 12 bold")
            root.option_add("*Button.Background", "#1F618D")
            root.option_add("*Button.Foreground", "#A9CCE3")

            root.option_add("*Label.Font", "Courier 11 bold")
            root.option_add("*Label.Background", "#1F618D")
            root.option_add("*Label.Foreground", "#A9CCE3")
            root.option_add("*Label.bd",10)
            root.option_add("*Label.Relief", "ridge")
            root.attributes('-topmost', True)


            root.wm_title("Passport Authentication")
            w = 720
            h = 700
            ws = root.winfo_screenwidth()
            hs = root.winfo_screenheight()
            x = (ws / 2) - (w / 2)
            y = (hs / 2) - (h / 2)

            root.geometry('%dx%d+%d+%d' % (w, h, x, y))  # give dimensions
            root.config(background="#FFFFFF")
            root.resizable(0, 0)

            self.passportImg = Image.new('RGB', (200, 250))
            self.passportSign = Image.new('RGB', (350, 100))
            self.profileimage= Image.new('RGB', (413, 531))
            self.verifyImg = Image.new('RGB', (413, 531))
            self.tagImg = Image.new('RGB', (413, 531))
            self.sign_image_path=""
            self.db_getImgPath=""
            self.db_getSignPath=""
            self.verifyPath=""
            self.db_link=""
            self.backObj=Utilities()
            self.errorObj=Errors()
            self.imageMatchMsg = StringVar()
            self.signMatchMsg=StringVar()

            """self.profileimage = Image.new('RGB', (132,170))
            self.verifyImg = Image.new('RGB', (132,170))
            self.tagImg = Image.new('RGB', (132,170))"""

            self.frame = Frame(root)
            self.frame.grid()



            self.canvas2 = Canvas(width=720, height=700)
            self.canvas2.config(background="#CCD1D1")
            self.canvas2.grid(row=0, column=1, columnspan=3)

            self.mainLabel = Label(root, text="------Enter Holder Information------")
            self.mainLabel.grid()
            self.mainLabel.config(font=("Courier", 16))
            self.mainLabel_windows = self.canvas2.create_window(120, 20, anchor=NW, window=self.mainLabel)

            self.b2 = Button(text="Scan Passport", command=self.create_verifyImg)
            self.b2.grid(row=1, column=1)
            self.b2_window = self.canvas2.create_window(250, 550, anchor=NW, window=self.b2)




            self.verify_Pass_No = StringVar()
            self.pass_numberLbl = Label(root, text="Passport Number :",width=20,height=2)
            self.pass_numberLbl.grid(row=0,column=0,ipadx=5,ipady=5)
            self.pass_numberLbl.configure()
            self.pass_number_window = self.canvas2.create_window(130, 95, anchor=NW, window=self.pass_numberLbl)
            self.ePass = Entry(root, textvariable=self.verify_Pass_No,width=20,bd=5)#set focus on this
            self.ePass.grid(row=2, column=1,ipadx=3)
            self.ePass.focus_set()
            self.ePass.configure(highlightbackground="#1F618D",highlightcolor="#1F618D",highlightthickness=2)
            self.ePass_window = self.canvas2.create_window(350, 100, anchor=NW, window=self.ePass)


            self.printPass = Button(root, text="Proceed>>>", command=self.showDB_TAG)
            self.printPass.grid(row=8, column=3)
            self.printPass_window = self.canvas2.create_window(550, 610, anchor=NW, window=self.printPass)



            mainloop()

        except Exception as ex:
            template = "An exception of type {0} occurred. Details:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            self.errorObj.genericError(message)


if __name__ == '__main__':
    root = Tk()
    prompt = Prompt(root)
