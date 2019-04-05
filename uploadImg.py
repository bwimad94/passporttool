from PIL import ImageTk, Image


class uploadImg(object):

    def __init__(self,path):#the method required the path of the image file
        self.path=path



#This method upload an image in its original size

    def getOriginal(self):

        try:
            Img= Image.open(self.path)

            ttkImg = ImageTk.PhotoImage(Img)#converts image to tkinter image object

            return ttkImg

        except Exception:
            pass

#This method uploads a resized image
    def uploadResized(self,width,height):#this me

        try:
            Img = Image.open(self.path)
            resized = Img.resize((width, height), Image.ANTIALIAS)
            ttkImg = ImageTk.PhotoImage(resized)#converts image to tkinter image object
            return ttkImg

        except Exception:
            print Exception
            pass




#This method upload a resized image with reduced opacity
    def uploadTRansparent(self,opacity,width,height):
        try:
            Img = Image.open(self.path)
            Img.putalpha(opacity)
            resized = Img.resize((width, height), Image.ANTIALIAS)
            ttkImg = ImageTk.PhotoImage(resized)#converts image to tkinter image object
            return ttkImg

        except Exception:
            print Exception
            pass
