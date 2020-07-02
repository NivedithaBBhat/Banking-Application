from account import Account
from transaction import Transaction
from tkinter import *
from tkinter import messagebox

class BankApp(Account,Transaction):
    
    def account(self):
        s1=Account()
    def transaction(self):
        s2=Transaction()
    def exit(self):
        s=messagebox.askyesno("Warning","Are you sure to Exit??")
        if(s==True):
            self.root.destroy()    
    def __init__(self):
        self.root=Tk()
        self.root.title("Banking Application")
        self.root.geometry("1000x600")
        l1=Label( self.root,text="Banking Application",fg="blue",bg="white",font="times 20 bold")
        l1.place(x=350,y=0)
        messagebox.showinfo("Welcome","Welcome to the Banking mode")
        b1=Button(self.root,text="Account Details",fg="Green",bg="white",font="times 20 bold",command=self.account)
        b1.place(x=100,y=100)
        b2=Button(self.root,text="Transaction details",fg="purple",bg="white",font="times 20 bold",command=self.transaction)
        b2.place(x=600,y=100)
        l2=Label(self.root,text="Thank you for using this Application!!",fg="Black",bg="white",font="times 20 bold")
        l2.place(x=300,y=350)
        b3=Button(self.root,text="Exit",fg="Black",bg="Yellow",font="times 20 bold",command=self.exit)
        b3.place(x=450,y=250)
        self.root.mainloop()
        
s=BankApp()
        
        
        
        
        
    


