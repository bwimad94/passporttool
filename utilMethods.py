class Utilities(object):
    # This method creates a back button for the GUI using tkinter
    def backButton(self,event, widget):
        event.destroy()
        widget.deiconify()
        widget.lift()

    def focus_next_textbox(self, e):
        e.widget.tk_focusNext().focus()
        return ("break")
