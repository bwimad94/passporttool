import mysql.connector
from calculateWatermark import *
from PIL import Image
import numpy as np
from errorMessage import *
from mysql.connector import errorcode
class verifyWatermark(Calculate):

    def __init__(self,passNumber):
        self.passNumber=passNumber

        self.errorObj=Errors()

    def verifyWatermark(self):


        conn=mysql.connector

        try:
            """ conn = mysql.connector.connect(user='bwimad', passwd='DdA2*H&tB', host='64.62.211.131',
                                                           database="bwimad_fyp")"""
            conn = mysql.connector.connect(user='root', passwd='root', host='localhost', database="fyp",
                                                port=3306)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print "Access Denied to Database"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exists")
            else:
                print(err)

        try:

            cur = conn.cursor()

            get_first = "SELECT first FROM passport_holders WHERE pass_no='%s'" % \
                        (self.passNumber)
            get_second = "SELECT second FROM passport_holders WHERE pass_no='%s'" % \
                         (self.passNumber)
            get_third = "SELECT third FROM passport_holders WHERE pass_no='%s'" % \
                        (self.passNumber)
            get_family = "SELECT last FROM passport_holders WHERE pass_no='%s'" % \
                         (self.passNumber)
            get_key = "SELECT SCRT_KEY FROM watermarking_info WHERE pass_no='%s'" % \
                      (self.passNumber)
            get_row = "SELECT ROW FROM watermarking_info WHERE pass_no='%s'" % \
                      (self.passNumber)
            get_col = "SELECT COL FROM watermarking_info WHERE pass_no='%s'" % \
                      (self.passNumber)
            get_sum = "SELECT SUM FROM watermarking_info WHERE pass_no='%s'" % \
                      (self.passNumber)
            get_channel = "SELECT CHANNEL FROM watermarking_info WHERE pass_no='%s'" % \
                          (self.passNumber)
            get_original = "SELECT ORIGINAL_VAL FROM watermarking_info WHERE pass_no='%s'" % \
                           (self.passNumber)
            get_PIX_COUNT = "SELECT PIX_COUNT FROM watermarking_info WHERE pass_no='%s'" % \
                            (self.passNumber)
            get_rcolumn = "SELECT RCOLUMN FROM watermarking_info WHERE pass_no='%s'" % \
                          (self.passNumber)
            get_watermark = "SELECT WATERMARK FROM watermarking_info WHERE pass_no='%s'" % \
                            (self.passNumber)
            get_tagImg= "SELECT imagePath FROM watermarking_info WHERE pass_no='%s'" % \
                            (self.passNumber)
            get_verifyImg= "SELECT imagePath FROM passport_holders WHERE pass_no='%s'" % \
                            (self.passNumber)
            print get_tagImg

            cur.execute(get_first)
            frstNm = cur.fetchone()[0]
            cur.execute(get_second)
            scndNm = cur.fetchone()[0]
            if scndNm == '*optional':
                scndNm = frstNm
            cur.execute(get_third)
            thrdNm = cur.fetchone()[0]
            cur.execute(get_family)
            fmlyNm = cur.fetchone()[0]
            if thrdNm == '*optional':
                thrdNm = fmlyNm
            cur.execute(get_key)
            key = cur.fetchone()[0]
            cur.execute(get_row)
            db_row = cur.fetchone()[0]
            cur.execute(get_col)
            db_col = cur.fetchone()[0]
            cur.execute(get_sum)
            db_sum = cur.fetchone()[0]
            cur.execute(get_channel)
            db_channel = cur.fetchone()[0]
            cur.execute(get_original)
            db_original = cur.fetchone()[0]
            cur.execute(get_PIX_COUNT)
            db_pixCount = cur.fetchone()[0]
            cur.execute(get_rcolumn)
            db_rcolumn = cur.fetchone()[0]
            cur.execute(get_watermark)
            db_watermark = cur.fetchone()[0]
            cur.execute(get_tagImg)
            db_tagImg=cur.fetchone()[0]
            cur.execute(get_verifyImg)
            verifyImg=cur.fetchone()[0]

            cur.close()
            conn.close()


            count = 0
            pixSum = 0
            verifyWM = Calculate(str(key), frstNm, scndNm, thrdNm, fmlyNm, self.passNumber)
            recalRow = verifyWM.calculateRow() #
            recalColumn = verifyWM.calculateCol()
            recalSumAll = verifyWM.calculateSum()



            tagWatermark = 0
            tagR, tagG, tagB = np.array(Image.open(db_tagImg)).T

            tagImg=Image.open(db_tagImg)
            verifyPixels = tagImg.load()

            if recalColumn != db_rcolumn:
                pixSum = sum(verifyPixels[recalRow, recalColumn])

            if db_channel == 'R':

                if recalColumn == db_rcolumn: # check if column and rcolumn are the same.if same retrieve original value
                    pix = list(verifyPixels[recalRow, recalColumn])
                    pix[0] = db_original
                    pixSum = sum(pix)

            elif db_channel == 'G':

                if recalColumn == db_rcolumn:
                    pix = list(verifyPixels[recalRow, recalColumn])
                    pix[1] = db_original
                    pixSum = sum(pix)

            elif db_channel == 'B':

                if recalColumn == db_rcolumn:
                    pix = list(verifyPixels[recalRow, recalColumn])
                    pix[2] = db_original
                    pixSum = sum(pix)

            recalAvg = (pixSum / 3) + 1

            recalPixCount = recalSumAll / recalAvg

            recalWatermark = recalSumAll % recalAvg

            recalRColumn=  recalColumn + recalPixCount + 1


            #Obtains the tag watermark
            if db_channel == 'R':
                tagWatermark = tagR[recalRow, recalRColumn]


            elif db_channel == 'G':

                tagWatermark = tagG[recalRow, recalRColumn]


            elif db_channel == 'B':
                tagWatermark = tagB[recalRow, recalRColumn]




            if db_row == recalRow:
                count += 1
            if db_col == recalColumn:
                count += 1
            if db_sum == recalSumAll:
                count += 1


            if count == 3:
                if recalPixCount == db_pixCount and recalWatermark == db_watermark == tagWatermark:
                    return True

                else:
                    return False


            else:
                return False

        except Exception:
            pass
