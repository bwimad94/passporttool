from Tkinter import *
from inputValidation import *
from tkFileDialog import askopenfilename
from uploadImg import *
from errorMessage import *
from completeIssuance import *
from utilMethods import *


class Prompt(InputValidation,uploadImg,Complete_Issuance,Utilities,Errors):

    #This method refreshes the start-up screen for a new issuance
    def backToMain(self):
        try:

            self.watermarkTL_toplevel.destroy()

            root.deiconify()
            root.lift()
            self.canvas.delete(self.passportImg)
            self.canvas.delete(self.passportSign)
            if not self.firstErrorMsg:
                self.firstLabelValidate.destroy()
            if not self.secondErrorMsg:
                self.secondLabelValidate.destroy()
            if not self.thirdErrorMsg:
                self.thirdLabelValidate.destroy()
            if not self.familyErrorMsg:
                self.familyLabelValidate.destroy()
            if self.passportValidation:
                self.passportLabelValidate.destroy()
            if not self.dobValidate:
                self.dobLabelValidate.destroy()
            if not self.validatePOB:
                self.POBLabelValidate.destroy()

            if not self.validateProf:
                self.ProfLabelValidate.destroy()

            if not self.validateNIC:
                self.NICLabelValidate.destroy()

            if not self.validateNation:
                self.NationLabelValidate.destroy()

            if not self.expireValidate:
                self.expireLabelValidate.destroy()

            if not self.issueValidate:
                self.issuedLabelValidate.destroy()

            self.eFirst.delete(0,END)
            self.eFirst.focus_set()
            self.secondEntry.delete(0,END)
            self.secondEntry.insert(INSERT,'*OPTIONAL')
            self.eThird.delete(0,END)
            self.eThird.insert(INSERT,'*OPTIONAL')
            self.eFamily.delete(0,END)
            self.ePassport.delete(0,END)
            self.dobEntry.delete(0,END)
            self.dobEntry.insert(INSERT,'DD/MM/YYYY')
            self.pobEntry.delete(0,END)
            self.pobEntry.insert(INSERT,'CITY/TOWN')
            self.professionEntry.delete(0,END)
            self.professionEntry.insert(INSERT,'UNEMPLOYED')
            self.nicEntry.delete(0,END)
            self.issuedEntry.delete(0,END)
            self.issuedEntry.insert(INSERT,'DD/MM/YYYY')
            self.expiredEntry.delete(0,END)
            self.expiredEntry.insert(INSERT,'DD/MM/YYYY')
            #self.watermarkTL_canvas.delete(self.passportImg)
            #self.watermarkTL_canvas.delete(self.passportSign)
        except Exception as ex:
            template = "An exception of type {0} occurred. Details:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            self.errorObj.genericError(message)



    def verifyInputs(self):

        #Performs input validation for the inserted inputs

        try:
            self.errorCount = 0

            self.passport = self.ePassport.get().upper()
            self.firstNm = self.eFirst.get().upper()
            self.secondNm = self.secondEntry.get().upper()
            self.thirdNm = self.eThird.get().upper()
            self.familyNm = self.eFamily.get().upper()
            self.holderProfession = self.professionEntry.get().upper()
            self.holderNIC = self.nicEntry.get().upper()
            self.holderDOB = self.dobEntry.get()
            self.holderPOB = self.pobEntry.get().upper()
            self.dateIssued = self.issuedEntry.get()
            self.dateExpired = self.expiredEntry.get()
            self.holderNation = self.statusEntry.get().upper()
            self.validateInputs = InputValidation()
            self.holderGender = self.gender.get()
            self.holderType = self.type.get()

            self.firstErrorMsg = self.validateInputs.validateFirst(self.firstNm)
            self.secondErrorMsg = self.validateInputs.validateSecond(self.secondNm)
            self.thirdErrorMsg = self.validateInputs.validateThird(self.thirdNm)
            self.familyErrorMsg = self.validateInputs.validateFamily(self.familyNm)
            self.passportValidation = self.validateInputs.validatePassport(self.passport)

            self.dobValidate = self.validateInputs.validateDate(self.holderDOB)
            self.issueValidate = self.validateInputs.validateDate(self.dateIssued)
            self.expireValidate = self.validateInputs.validateDate(self.dateExpired)
            self.validatePOB = self.validateInputs.validateText(self.holderPOB)
            self.validateNation = self.validateInputs.validateText(self.holderNation)
            self.validateProf = self.validateInputs.validateText(self.holderProfession)
            self.validateNIC = self.validateInputs.validateNIC(self.holderNIC)

            if self.firstErrorMsg:
                self.errorCount += 1
                self.firstLabelValidate = Label(root, text=self.firstErrorMsg)
                self.firstLabelValidate.grid()
                self.firstLabelValidate.config(bg="#922B21")
                self.firstLabelValidate_window = self.canvas.create_window(550, 100, anchor=NW,
                                                                           window=self.firstLabelValidate)


            if self.secondErrorMsg:
                self.errorCount += 1
                self.secondLabelValidate = Label(root, text=self.secondErrorMsg)
                self.secondLabelValidate.grid()
                self.secondLabelValidate.config(bg="#922B21")
                self.secondLabelValidate_window = self.canvas.create_window(550, 165, anchor=NW,
                                                                            window=self.secondLabelValidate)



            if self.thirdErrorMsg:
                self.errorCount += 1
                self.thirdLabelValidate = Label(root, text=self.thirdErrorMsg)
                self.thirdLabelValidate.grid()
                self.thirdLabelValidate.config(bg="#922B21")
                self.thirdLabelValidate_window = self.canvas.create_window(550, 235, anchor=NW,
                                                                           window=self.thirdLabelValidate)



            if self.familyErrorMsg:
                self.errorCount += 1
                self.familyLabelValidate = Label(root, text=self.familyErrorMsg)
                self.familyLabelValidate.config(bg="#922B21")
                self.familyLabelValidate_window = self.canvas.create_window(550, 295, anchor=NW,
                                                                            window=self.familyLabelValidate)



            if not self.passportValidation:
                self.errorCount += 1
                self.passportLabelValidate = Label(root, text="Passport Number Format is Incorrect!")
                self.passportLabelValidate.config(bg="#922B21")
                self.passportLabelValidate_window = self.canvas.create_window(550, 360, anchor=NW,
                                                                              window=self.passportLabelValidate)

            if self.dobValidate:
                self.errorCount += 1
                self.dobLabelValidate = Label(root, text=self.dobValidate)
                self.dobLabelValidate.config(bg="#922B21")
                self.dobLabelValidate_window = self.canvas.create_window(550, 490, anchor=NW,
                                                                         window=self.dobLabelValidate)

            if self.validatePOB:
                self.errorCount += 1
                self.POBLabelValidate = Label(root, text=self.validatePOB)
                self.POBLabelValidate.config(bg="#922B21")
                self.POBLabelValidate_window = self.canvas.create_window(1050, 100, anchor=NW,
                                                                         window=self.POBLabelValidate)

            if self.validateProf:
                self.errorCount += 1
                self.ProfLabelValidate = Label(root, text=self.validateProf)
                self.ProfLabelValidate.config(bg="#922B21")
                self.ProfLabelValidate_window = self.canvas.create_window(1050, 165, anchor=NW,
                                                                          window=self.ProfLabelValidate)


            if self.validateNIC:
                self.errorCount += 1
                self.NICLabelValidate = Label(root, text=self.validateNIC)
                self.NICLabelValidate.config(bg="#922B21")
                self.NICLabelValidate_window = self.canvas.create_window(1050, 230, anchor=NW,
                                                                         window=self.NICLabelValidate)


            if self.validateNation:
                self.errorCount += 1
                self.NationLabelValidate = Label(root, text=self.validateNation)
                self.NationLabelValidate.config(bg="#922B21")
                self.NationLabelValidate_window = self.canvas.create_window(1050, 360, anchor=NW,
                                                                            window=self.NationLabelValidate)

            if self.issueValidate:
                self.errorCount += 1
                self.issuedLabelValidate = Label(root, text=self.issueValidate)
                self.issuedLabelValidate.config(bg="#922B21")
                self.issuedLabelValidate_window = self.canvas.create_window(1050, 425, anchor=NW,
                                                                            window=self.issuedLabelValidate)


            if self.expireValidate:
                self.errorCount += 1
                self.expireLabelValidate = Label(root, text=self.expireValidate)
                self.expireLabelValidate.config(bg="#922B21")
                self.expireLabelValidate_window = self.canvas.create_window(1050,490, anchor=NW,
                                                                            window=self.expireLabelValidate)

            if not self.verifyPath:
                self.imageError=Label(root,text='No Image Detected!')
                self.imageError.config(bg="#922B21")
                self.imageError_window = self.canvas.create_window(100, 100, anchor=NW,
                                                                            window=self.imageError)
            else:
                pass

            if not self.sign_image_path:
                self.signError = Label(root, text='No Signature Detected!')
                self.signError.config(bg="#922B21")
                self.signError_window = self.canvas.create_window(100, 500, anchor=NW,
                                                                   window=self.signError)
            else:
                pass

            if self.errorCount==0 and self.verifyPath != "" and self.sign_image_path != "":
                self.embedWatermarkGUI()
            else:
                self.errorObj.errorMessageStartup()

        except Exception as ex:
            template = "An exception of type {0} occurred. Details:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            self.errorObj.genericError(message)

    def embedWatermarkGUI(self):
        #GUI configurations for issuance complete window
        try:
            root.withdraw()
            self.watermarkTL_toplevel = Toplevel()
            #self.watermarkTL_toplevel.attributes("-topmost", True)
            self.watermarkTL_toplevel.wm_title("Embed Watermark")
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
            self.watermarkTL_toplevel.option_add("*Label.Relief", "flat")

            self.watermarkTL_canvas = Canvas(self.watermarkTL_toplevel, width=1500, height=700)
            self.watermarkTL_canvas.config(background="#CCD1D1")
            self.watermarkTL_canvas.grid(row=0, column=1, columnspan=3)

            self.holderInfoLbl=Label(self.watermarkTL_toplevel,text='Passport Information')
            self.holderInfoLbl.grid()
            self.holderInfoLbl.config(font=("Courier", 16), bg="#4A235A", fg="white",relief='ridge')
            self.holderInfoLbl_window=self.watermarkTL_canvas.create_window(250,25,anchor=NW,window=self.holderInfoLbl)

            if self.familyNm and self.familyNm and self.secondNm!='*OPTIONAL' and self.thirdNm!='*OPTIONAL':

                self.holderFNm=Label(self.watermarkTL_toplevel,text="Full Name: "+self.firstNm+" "+self.secondNm+" "+self.thirdNm+" "+self.familyNm)
                self.holderFNm.grid()
                self.holderFNm.config(bg='#CCD1D1',fg='black')
                self.holderFNm_window=self.watermarkTL_canvas.create_window(200,75,anchor=NW,window=self.holderFNm)

            elif self.familyNm and self.familyNm and self.secondNm!='*OPTIONAL' and self.thirdNm =='*OPTIONAL':

                self.holderFNm=Label(self.watermarkTL_toplevel,text="Full Name: "+self.firstNm+" "+self.secondNm+" "+self.familyNm)
                self.holderFNm.grid()
                self.holderFNm.config(bg='#CCD1D1', fg='black')
                self.holderFNm_window=self.watermarkTL_canvas.create_window(200,75,anchor=NW,window=self.holderFNm)

            elif self.familyNm and self.familyNm and self.secondNm =='*OPTIONAL' and self.thirdNm =='*OPTIONAL':

                self.holderFNm=Label(self.watermarkTL_toplevel,text="Full Name: "+self.firstNm+" "+self.familyNm)
                self.holderFNm.grid()
                self.holderFNm.config(bg='#CCD1D1', fg='black')
                self.holderFNm_window=self.watermarkTL_canvas.create_window(200,75,anchor=NW,window=self.holderFNm)

            self.holderPNum=Label(self.watermarkTL_toplevel,text="Passport No. "+self.passport)
            self.holderPNum.grid()
            self.holderPNum.config(bg='#CCD1D1', fg='black')
            self.holderPNum_widnow=self.watermarkTL_canvas.create_window(200,125,anchor=NW,window=self.holderPNum)

            self.holderGen= Label(self.watermarkTL_toplevel, text="Gender: "+self.holderGender)
            self.holderGen.grid()
            self.holderGen.config(bg='#CCD1D1', fg='black')
            self.holderGen_widnow = self.watermarkTL_canvas.create_window(200, 175, anchor=NW, window=self.holderGen)

            self.holderDOBLbl = Label(self.watermarkTL_toplevel, text="DOB: "+self.holderDOB)
            self.holderDOBLbl.grid()
            self.holderDOBLbl.config(bg='#CCD1D1', fg='black')
            self.holderDOBLbl_widnow = self.watermarkTL_canvas.create_window(200, 225, anchor=NW, window=self.holderDOBLbl)

            self.holderPOBLbl = Label(self.watermarkTL_toplevel, text="POB: "+self.holderPOB)
            self.holderPOBLbl.grid()
            self.holderPOBLbl.config(bg='#CCD1D1', fg='black')
            self.holderPOBLbl_widnow = self.watermarkTL_canvas.create_window(375, 225, anchor=NW, window=self.holderPOBLbl)

            self.holderProfLbl = Label(self.watermarkTL_toplevel, text="Profession: "+self.holderProfession)
            self.holderProfLbl.grid()
            self.holderProfLbl.config(bg='#CCD1D1', fg='black')
            self.holderProfLbl_widnow = self.watermarkTL_canvas.create_window(200, 275, anchor=NW, window=self.holderProfLbl)

            self.holderNICLbl = Label(self.watermarkTL_toplevel, text="NIC: "+self.holderNIC)
            self.holderNICLbl.grid()
            self.holderNICLbl.config(bg='#CCD1D1', fg='black')
            self.holderNICLbl_widnow = self.watermarkTL_canvas.create_window(200, 325, anchor=NW, window=self.holderNICLbl)

            self.holderTypeLbl = Label(self.watermarkTL_toplevel, text="Type: "+self.holderType)
            self.holderTypeLbl.grid()
            self.holderTypeLbl.config(bg='#CCD1D1', fg='black')
            self.holderTypeLbl_widnow = self.watermarkTL_canvas.create_window(200, 375, anchor=NW, window=self.holderTypeLbl)

            self.holderNtnLbl = Label(self.watermarkTL_toplevel, text="Nationality: "+self.holderNation)
            self.holderNtnLbl.grid()
            self.holderNtnLbl.config(bg='#CCD1D1', fg='black')
            self.holderNtnLbl_widnow = self.watermarkTL_canvas.create_window(375, 375, anchor=NW, window=self.holderNtnLbl)





            self.passIssuedLbl = Label(self.watermarkTL_toplevel, text="Issued: "+self.dateIssued)
            self.passIssuedLbl.grid()
            self.passIssuedLbl.config(bg='#CCD1D1', fg='black')
            self.passIssuedLbl_widnow = self.watermarkTL_canvas.create_window(200, 425, anchor=NW, window=self.passIssuedLbl)

            self.passExpLbl = Label(self.watermarkTL_toplevel, text="Expires: "+self.dateExpired)
            self.passExpLbl.grid()
            self.passExpLbl.config(bg='#CCD1D1', fg='black')
            self.passExpLbl_widnow = self.watermarkTL_canvas.create_window(400, 425, anchor=NW, window=self.passExpLbl)

            self.imgLbl= uploadImg(self.verifyPath)
            self.ttkverifyImgLbl = self.imgLbl.uploadResized(132,170)
            self.verifyImgLbl= self.watermarkTL_canvas.create_image(50, 75, image=self.ttkverifyImgLbl, anchor='nw')
            self.watermarkTL_canvas.grid()
            self.watermarkTL_canvas.image = self.ttkverifyImgLbl

            self.signLbl = uploadImg(self.sign_image_path)
            self.ttkverifySignLbl = self.signLbl.uploadTRansparent(200,300, 50)
            self.verifySignLbl = self.watermarkTL_canvas.create_image(200, 455, image=self.ttkverifySignLbl, anchor='nw')
            self.watermarkTL_canvas.grid()
            self.watermarkTL_canvas.image = self.ttkverifySignLbl



            self.back_button = Button(self.watermarkTL_toplevel, text="<<<Back",
                                      command=lambda: self.backObj.backButton(self.watermarkTL_toplevel, root))
            self.back_button.grid()
            self.back_button_windows = self.watermarkTL_canvas.create_window(25, 650, anchor=NW, window=self.back_button)

            self.complete_button = Button(self.watermarkTL_toplevel, text="Complete Issuance",
                                      command=self.embedWatermark)
            self.complete_button.grid()
            #self.complete_button.config(bg='black',fg='white')
            self.complete_button_windows = self.watermarkTL_canvas.create_window(250, 525, anchor=NW, window=self.complete_button)

            self.new_button = Button(self.watermarkTL_toplevel, text="New Issuance",
                                          command=self.backToMain)
            self.new_button.grid()

            self.new_button_windows = self.watermarkTL_canvas.create_window(600, 650, anchor=NW,
                                                                                 window=self.new_button)
        except Exception as ex:
            template = "An exception of type {0} occurred. Details:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            self.errorObj.genericError(message)
    """def progress(self):
        self.pb = ttk.Progressbar(self.watermarkTL_toplevel, orient="horizontal", length=200, mode="determinate")
        self.pb.grid()
        self.pb_windows = self.watermarkTL_canvas.create_window(100, 525, anchor=NW,
                                                                window=self.pb)
        self.pb.start(50)
        self.watermarkTL_toplevel.after(20000, self.pb.stop)

    def initUI(self):
        self.popup = popup = Toplevel()
        self.popup.attributes('-topmost', True)
        self.popup.wm_title("Match Features")
        self.db_tag_width = 400
        self.db_tag_height = 200
        self.db_tag_ws = self.popup.winfo_screenwidth()
        self.db_tag_hs = self.popup.winfo_screenheight()
        self.x = (self.db_tag_ws / 2) - (self.db_tag_width / 2)
        self.y = (self.db_tag_hs / 2) - (self.db_tag_height / 2)
        self.popup.geometry('%dx%d+%d+%d' % (self.db_tag_width, self.db_tag_height, self.x, self.y))
        Label(popup, text="Please wait until the file is created").grid(
            row=0, column=0)
        self.progressbar = progressbar = ttk.Progressbar(popup,
                                                         orient=HORIZONTAL, length=200, mode='indeterminate')
        progressbar.grid()
        progressbar.start()
        self.checkfile()

    def checkfile(self):
        self.RFIDdir = 'C:/Users/BHAGYA/Dropbox/fyp/.idea/rfid_files/'  # default directory to store files
        self.rfid_suffix = 'txt'
        RFIDpath = os.path.join(self.RFIDdir, self.passport + "." + self.rfid_suffix)
        if os.path.exists(RFIDpath):
            print 'found it'
            self.progressbar.stop()
            self.popup.destroy()
        else:
            print 'not created yet'
            self.popup.after(100, self.checkfile)  # Call this method after 100 ms.

    def completeAll(self):
        self.initUI()

        time.sleep(2)

        self.embedWatermark()"""


    def embedWatermark(self):

        #Completes the issunace process


            try:

                self.watermarkObj=Complete_Issuance(self.verifyPath,self.sign_image_path,self.firstNm,self.secondNm,self.thirdNm,self.familyNm,self.passport)


            except Exception as ex:

                template = "An exception of type {0} occurred. Details:\n{1!r}"

                message = template.format(type(ex).__name__, ex.args)

                self.errorObj.genericError(message)

            try:

                self.watermarkObj.embedWM()
                self.complete_msg = Label(self.watermarkTL_toplevel,
                                          text="Watermarking Completed!")
                self.complete_msg.grid()
                self.complete_msg.config(bg='green', fg='black')
                self.complete_msg_windows = self.watermarkTL_canvas.create_window(250, 575, anchor=NW,
                                                                                  window=self.complete_msg)
            except Exception as ex:
                template = "An exception of type {0} occurred. Details:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                self.errorObj.genericError(message)
                self.complete_msg = Label(self.watermarkTL_toplevel,
                                          text="Watermarking COULD NOT be Completed!")
                self.complete_msg.grid()
                self.complete_msg.config(bg='red', fg='white')
                self.complete_msg_windows = self.watermarkTL_canvas.create_window(250, 575, anchor=NW,
                                                                                  window=self.complete_msg)

            """try:
                self.watermarkObj.insertToTemplateDB()

            except EXCEPTION:

                pass"""

            try:
                self.watermarkObj.insertToHolderDB(self.holderGender,self.holderDOB,self.holderPOB,self.holderProfession,self.holderNIC,self.holderType,self.holderNation,self.dateIssued,self.dateExpired)
                self.watermarkObj.insertToWMDB()
                self.completeHolderDB_msg = Label(self.watermarkTL_toplevel,
                                          text="Central Server Successfully Updated!")
                self.completeHolderDB_msg.grid()
                self.completeHolderDB_msg.config(bg='green', fg='black')
                self.completeHolderDB_msg_windows = self.watermarkTL_canvas.create_window(200, 615, anchor=NW,
                                                                                  window=self.completeHolderDB_msg)
            except Exception as ex:
                template = "An exception of type {0} occurred. Details:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                self.errorObj.genericError(message)
                self.completeHolderDB_msg = Label(self.watermarkTL_toplevel,
                                                  text="Central Server COULD NOT be Updated!")
                self.completeHolderDB_msg.grid()
                self.completeHolderDB_msg.config(bg='red', fg='white')
                self.completeHolderDB_msg_windows = self.watermarkTL_canvas.create_window(200, 615, anchor=NW,
                                                                                          window=self.completeHolderDB_msg)
            try:
                self.watermarkObj.saveTagImg()
                self.watermarkObj.saveTagSign()
                self.watermarkObj.saveRFIDFile(self.holderGender,self.holderDOB,self.holderPOB,self.holderProfession,self.holderNIC,self.holderType,self.holderNation,self.dateIssued,self.dateExpired)

                self.complete_msg= Label(self.watermarkTL_toplevel, text="RFID File Successfully Created!")
                self.complete_msg.grid()
                self.complete_msg.config(bg='green',fg='black')
                self.complete_msg_windows = self.watermarkTL_canvas.create_window(225, 650, anchor=NW,
                                                                                     window=self.complete_msg)
            except Exception as ex:
                template = "An exception of type {0} occurred. Details:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                self.errorObj.genericError(message)
                self.completeRFID_msg = Label(self.watermarkTL_toplevel, text="RFID File Creation Unsuccessful!")
                self.completeRFID_msg.grid()
                self.completeRFID_msg.config(bg='green', fg='black')
                self.completeRFID_msg_windows = self.watermarkTL_canvas.create_window(225, 650, anchor=NW,
                                                                                  window=self.completeRFID_msg)





    def create_image(self):
        # Creates the holder facial photograph

        try:

            self.verifyPath = askopenfilename(filetypes=(("PNG Files", "*.png"), ("All Files", ".*")))#acquires file path

            if self.verifyPath:
                self.imageError.destroy()
                self.verifyImgObj = uploadImg(self.verifyPath)
                self.originalImg=self.verifyImgObj.getOriginal()
                if self.originalImg.height()==531 and self.originalImg.width()==413:#ensures the image is within required dimensions
                    self.ttkverifyImg = self.verifyImgObj.uploadResized(300,350)
                    self.passportImg = self.canvas.create_image(50, 25, image=self.ttkverifyImg, anchor='nw')
                    self.canvas.grid()
                    self.canvas.image = self.ttkverifyImg
                else:
                    self.errorObj.incorrectImageSize()
            else:
                self.errorObj.genericError('Image Path Does Not Exist!')


        except Exception as ex:

            template = "An exception of type {0} occurred. Details:\n{1!r}"

            message = template.format(type(ex).__name__, ex.args)

            self.errorObj.genericError(message)


    def create_Signature(self):
        # Creates holder signature photograph

        try:
            self.sign_image_path = askopenfilename(filetypes=(("PNG Files", "*.png"), ("All Files", ".*")))

            if self.sign_image_path:
                self.signError.destroy()
                self.signImgObj = uploadImg(self.sign_image_path)
                self.signImg = self.signImgObj.uploadResized(350, 100)
                self.canvas.image = self.signImg
                self.passportSign = self.canvas.create_image(50, 500, image=self.signImg, anchor='nw')
                self.canvas.grid(side=LEFT, padx=2, pady=2)
            else:
                self.errorObj.genericError('Signature Path Does Not Exist!')

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
            root.option_add("*Label.bd", 10)
            root.option_add("*Label.Relief", "ridge")
            root.attributes('-topmost', True)

            root.wm_title("Passport Issuance")
            w = 1500
            h = 700
            ws = root.winfo_screenwidth()
            hs = root.winfo_screenheight()
            x = (ws / 2) - (w / 2)
            y = (hs / 2) - (h / 2)

            root.geometry('%dx%d+%d+%d' % (w, h, x, y))  # give dimensions
            root.config(background="#FFFFFF")
            root.resizable(0, 0)

            self.imageError=Label(root,text='')
            self.signError=Label(root,text='')
            self.firstLabelValidate=Label(root,text='')
            self.secondLabelValidate = Label(root, text='')
            self.thirdLabelValidate = Label(root, text='')
            self.familyLabelValidate = Label(root, text='')
            self.NationLabelValidate = Label(root, text='')
            self.passportLabelValidate = Label(root, text='')
            self.typeLabelValidate = Label(root, text='')
            self.POBLabelValidate = Label(root, text='')
            self.NICLabelValidate = Label(root, text='')
            self.dobLabelValidate = Label(root, text='')
            self.ProfLabelValidate = Label(root, text='')
            self.issuedLabelValidate = Label(root, text='')
            self.expireLabelValidate = Label(root, text='')

            self.profileimage= Image.new('RGB', (413, 531))
            self.verifyImg = Image.new('RGB', (413, 531))
            self.tagImg = Image.new('RGB', (413, 531))
            self.createPath=""
            self.verifyPath=""
            self.sign_image_path=""
            self.db_link=""
            self.verifyTxt = StringVar()
            self.backObj=Utilities()
            self.errorObj=Errors()

            """self.profileimage = Image.new('RGB', (132,170))
            self.verifyImg = Image.new('RGB', (132,170))
            self.tagImg = Image.new('RGB', (132,170))"""

            self.frame = Frame(root)
            self.frame.grid()

            self.canvas = Canvas(width=1500, height=700)
            self.canvas.grid(row=0, column=1, columnspan=3)

            self.canvas.config(background="#CCD1D1")


            self.b = Button(text="Upload Photo", command=self.create_image)
            self.b.grid(row=1, column=1)
            self.b_window = self.canvas.create_window(125, 400, anchor=NW, window=self.b)
            self.button_opt = {'padx': 5, 'pady': 5}
            self.signatureUpload = Button(text='Upload Signature', command=self.create_Signature)
            self.signatureUpload .grid_configure(**self.button_opt)
            self.signatureUpload .grid(row=10, column=2)
            self.signatureUpload_window = self.canvas.create_window(100, 630, anchor=NW, window=self.signatureUpload )




            """sep = Separator(root, orient=HORIZONTAL)
            sep.grid(sticky=EW, row=2)"""

            self.first = StringVar()

            self.passport = StringVar()

            self.second = StringVar(value='*OPTIONAL')

            self.mid = StringVar(value='*OPTIONAL')

            self.last = StringVar()

            self.type=StringVar()
            self.type.set("PB")

            self.gender=StringVar()
            self.gender.set("M")

            self.dob=StringVar(value="DD/MM/YYYY")

            self.pob=StringVar(value="CITY/TOWN")

            self.profession=StringVar(value="UNEMPLOYED")

            self.nic=StringVar()

            self.nationality=StringVar(value="SRI LANKAN")

            self.issued = StringVar(value="DD/MM/YYYY")

            self.expired = StringVar(value="DD/MM/YYYY")

            self.noError=StringVar()
            self.noError.set('')



            self.root_subject=Label(root,text="Enter Holder Information")
            self.root_subject.grid(row=2, column=0)
            self.root_subject.config(font=("Courier", 16), bg="#4A235A", fg="white")
            self.root_subject_window = self.canvas.create_window(750, 25, anchor=NW, window=self.root_subject)

            self.firstLabel = Label(root, text="First Name :")
            self.firstLabel.grid(row=2, column=0)
            self.label_window = self.canvas.create_window(500, 75, anchor=NW, window=self.firstLabel)




            self.eFirst = Entry(root, textvariable=self.first)
            self.eFirst.grid(row=2, column=4)
            self.eFirst.bind("<Return>", self.focus_next_textbox)
            self.eFirst.focus_set()
            self.eFirst_window = self.canvas.create_window(625, 75, anchor=NW, window=self.eFirst)


            self.secondLabel = Label(root, text="Second Name:")
            self.secondLabel.grid(row=3, column=0)
            self.label_window = self.canvas.create_window(500, 140, anchor=NW, window=self.secondLabel)
            self.secondEntry = Entry(root, textvariable=self.mid,fg="#922B21")
            self.secondEntry.grid(row=3, column=1)
            self.secondEntry.bind("<Return>", self.focus_next_textbox)
            self.secondEntry_window = self.canvas.create_window(625, 140, anchor=NW, window=self.secondEntry)

            self.label2 = Label(root, text="Third Name :")
            self.label2.grid(row=4, column=0)
            self.label2_window = self.canvas.create_window(500, 205, anchor=NW, window=self.label2)
            self.eThird = Entry(root, textvariable=self.second,fg="#922B21")
            self.eThird.grid(row=4, column=1)
            self.eThird.bind("<Return>", self.focus_next_textbox)
            self.eThird_window = self.canvas.create_window(625, 205, anchor=NW, window=self.eThird)

            self.label3 = Label(root, text="Last Name  :")
            self.label3.grid(row=5, column=0)
            self.label3_window = self.canvas.create_window(500, 270, anchor=NW, window=self.label3)
            self.eFamily = Entry(root, textvariable=self.last)
            self.eFamily.grid(row=5, column=1)
            self.eFamily.bind("<Return>", self.focus_next_textbox)
            self.eFamily_window = self.canvas.create_window(625, 270, anchor=NW, window=self.eFamily)

            self.label4 = Label(root, text="Passport No.")
            self.label4.grid(row=6, column=0)
            self.label4_window = self.canvas.create_window(500, 335, anchor=NW, window=self.label4)
            self.ePassport = Entry(root, textvariable=self.passport)
            self.ePassport.grid(row=6, column=1)
            self.ePassport_window = self.canvas.create_window(625, 335, anchor=NW, window=self.ePassport)

            self.genderLabel=Label(root,text="Gender\t   :")
            self.genderLabel.grid(row=7,column=0)
            self.genderLabel_window=self.canvas.create_window(500,400,anchor=NW,window=self.genderLabel)
            self.genderDropdown = OptionMenu(root, self.gender, "M", "F")
            self.genderDropdown.grid(row=7,column=1)
            self.genderDropdown_window=self.canvas.create_window(625,400,anchor=NW,window=self.genderDropdown)

            self.dobLabel=Label(root,text="DOB\t   :")
            self.dobLabel.grid(row=8,column=0)
            self.dobLabel_window=self.canvas.create_window(500,465,anchor=NW,window=self.dobLabel)
            self.dobEntry=Entry(root,textvariable=self.dob)
            self.dobEntry.grid(row=8,column=1)
            self.dobEntry_window=self.canvas.create_window(625,465,anchor=NW,window=self.dobEntry)

            self.pobLabel = Label(root, text="POB\t   :")
            self.pobLabel.grid()
            self.pobLabel_window = self.canvas.create_window(1000, 75, anchor=NW, window=self.pobLabel)
            self.pobEntry = Entry(root, textvariable=self.pob)
            self.pobEntry.grid()
            self.pobEntry.bind("<Return>", self.focus_next_textbox)
            self.pobEntry_window = self.canvas.create_window(1125, 75, anchor=NW, window=self.pobEntry)

            self.professionLabel = Label(root, text="Profession :")
            self.professionLabel.grid()
            self.professionLabel_window = self.canvas.create_window(1000, 140, anchor=NW, window=self.professionLabel)
            self.professionEntry = Entry(root, textvariable=self.profession)
            self.professionEntry.grid()
            self.professionEntry.bind("<Return>", self.focus_next_textbox)
            self.professionEntry_window = self.canvas.create_window(1125, 140, anchor=NW, window=self.professionEntry)

            self.nicLabel = Label(root, text="NIC Number :")
            self.nicLabel.grid()
            self.nicLabel_window = self.canvas.create_window(1000, 205, anchor=NW, window=self.nicLabel)
            self.nicEntry = Entry(root, textvariable=self.nic)
            self.nicEntry.grid()
            self.nicEntry.bind("<Return>", self.focus_next_textbox)
            self.nicEntry_window = self.canvas.create_window(1125, 205, anchor=NW, window=self.nicEntry)

            self.typeLabel = Label(root, text="Type \t   :")
            self.typeLabel.grid()
            self.typeLabel_window = self.canvas.create_window(1000, 270, anchor=NW, window=self.typeLabel)
            self.typeEntry = OptionMenu(root, self.type,"PA","PB","PC","PD")
            self.typeEntry.grid()
            self.typeEntry.bind("<Return>", self.focus_next_textbox)
            self.typeEntry_window = self.canvas.create_window(1125, 270, anchor=NW, window=self.typeEntry)

            self.statusLabel = Label(root, text="Nationality:")
            self.statusLabel.grid()
            self.statusLabel_window = self.canvas.create_window(1000, 335, anchor=NW, window=self.statusLabel)
            self.statusEntry = Entry(root, textvariable=self.nationality)
            self.statusEntry.grid()
            self.statusEntry.bind("<Return>", self.focus_next_textbox)
            self.statusEntry_window = self.canvas.create_window(1125, 335, anchor=NW, window=self.statusEntry)

            self.issuedLabel = Label(root, text="Issued On  :")
            self.issuedLabel.grid()
            self.issuedLabel_window = self.canvas.create_window(1000, 400, anchor=NW, window=self.issuedLabel)
            self.issuedEntry = Entry(root, textvariable=self.issued)
            self.issuedEntry.grid()
            self.issuedEntry.bind("<Return>", self.focus_next_textbox)
            self.issuedEntry_window = self.canvas.create_window(1125, 400, anchor=NW, window=self.issuedEntry)



            self.expiredLabel = Label(root, text="Expires On :")
            self.expiredLabel.grid()
            self.expiredLabel_window = self.canvas.create_window(1000, 465, anchor=NW, window=self.expiredLabel)
            self.expiredEntry = Entry(root, textvariable=self.expired)
            self.expiredEntry.grid()
            self.expiredEntry.bind("<Return>", self.focus_next_textbox)
            self.expiredEntry_window = self.canvas.create_window(1125, 465, anchor=NW, window=self.expiredEntry)

            self.a = Button(root, text="Proceed>>>", command=self.verifyInputs)
            self.a.grid(row=8, column=3)
            self.a_window = self.canvas.create_window(1300, 620, anchor=NW, window=self.a)

            mainloop()

        except Exception as ex:
            template = "An exception of type {0} occurred. Details:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            self.errorObj.genericError(message)



root = Tk()
prompt = Prompt(root)

