import sys, Tkinter as TK
root = TK.Tk()
tv = TK.StringVar()
frm = TK.Frame(root, bg="red",
               width=500, height=500, padx=10, pady=10).pack()
TK.Label(frm, textvariable=tv).pack()
TK.Entry(frm, textvariable=tv).pack()
tv.set("Welcome!")
TK.Button(frm, text="Exit", command=root.quit).pack()
TK.mainloop()
print tv.get()


