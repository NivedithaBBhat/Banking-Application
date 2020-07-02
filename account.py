import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter.constants import DISABLED, NORMAL


class Account():
    def new_record(self):
        self.acc_new['state']=DISABLED
        self.populate_blank();
    def save_record(self):
        account_id=int(self.account_id.get())
        cust_name=self.cust_name.get()
        city=self.city.get()
        state=self.state.get()
        phone=self.phone.get()
        opening_balance=float(self.opening_balance.get())
        if(opening_balance<500):
            messagebox.showerror("Error","Minimum Balance Should be Rs 500")
        else:
            open_date=self.open_date.get()
        
            if self.acc_new['state']==DISABLED:
                sql="Insert into account_mast (account_id,cust_name,city,state,phone,opening_balance,open_date) values('%d','%s','%s','%s','%s','%f','%s')" %(account_id,cust_name,city,state,phone,opening_balance,open_date)
            else:
                sql="Update account_mast set cust_name='%s',city='%s',state='%s',phone='%s',opening_balance='%f',open_date='%s' where account_id='%d'" %(cust_name,city,state,phone,opening_balance,open_date,account_id)
            try:
                self.cursor.execute(sql)
                self.cn.commit()
                messagebox.showinfo("Saved","Details Saved Successfully")
                sql="Select * from account_mast"
                self.results=self.cursor.fetchall() 
            except:
                self.cn.rollback()     
            self.acc_new["state"]=NORMAL
        
    def delete_record(self):
        acc_id=int(self.acc_id.get())
        s=messagebox.askyesno("Warning", "Are you Sure to Delete?")
        if(s==True):
            sql="Delete From account_mast WHERE acc_id='%d'" %(acc_id)
            try:
                self.cursor.execute(sql)
                self.cn.commit()
                sql="Select * from account_mast"
                self.results=self.cursor.fetchall() 
                self.populate_blank()
                self.previous_record() 
            except:
                self.cn.rollback()
            
            
    def exit_form(self):
        s=messagebox.askyesno("Warning","Are you sure to Exit?")
        if(s==True):
            self.root.destroy()
        
    def first_record(self):
        if len(self.results)>0:
            self.current_record=0
            self.populate_record()
            
    def next_record(self):
        if len(self.results)>0:
            self.current_record+=1;
            if self.current_record>=len(self.results):
                self.current_record=0
            self.populate_record()
            
    def previous_record(self):
        if len(self.results)>0:
            self.current_record-=1
            if self.current_record<0:
                self.current_record=len(self.results)-1
            self.populate_record()
            
    def last_record(self):
        if len(self.results)>0:
            self.current_record=len(self.results)-1
            self.populate_record()
             
    def populate_record(self):
            row=self.results[self.current_record]
            self.account_id.delete(0,END)
            self.account_id.insert(0,row[0])
            self.cust_name.delete(0,END)
            self.cust_name.insert(0,row[1])
            self.city.delete(0,END)
            self.city.insert(0,row[2])
            self.state.delete(0,END)
            self.state.insert(0,row[3])
            self.phone.delete(0,END)
            self.phone.insert(0,row[4])
            self.opening_balance.delete(0,END)
            self.opening_balance.insert(0,row[5])
            self.open_date.delete(0,END)
            self.open_date.insert(0,row[6]) 
            
    def populate_blank(self):
        self.account_id.delete(0,END)
        self.cust_name.delete(0,END)
        self.city.delete(0,END) 
        self.state.delete(0,END) 
        self.phone.delete(0,END)
        self.opening_balance.delete(0,END) 
        self.open_date.delete(0,END) 
            
    
        
        
    def __init__(self):
        config = {'user':'NivedithaBhat', 'password':'123', 'host':'localhost', 'database':'bank'}
        self.cn = mysql.connector.connect(**config)
        print("Connected")
        self.cursor = self.cn.cursor()
            
        self.root = Tk()
        self.root.title("Banking Application")
        self.root.geometry("700x500")
        l1=Label(self.root,text="Account Details",fg="blue",bg="white",font="times 20 bold")
        l1.pack()
        

        
        account_id = Label(self.root, text="Account Id:", anchor=E)
        self.account_id = Entry(self.root)
        account_id.place(x=100, y=50)
        self.account_id.place(x=200, y=50)
                
        cust_name = Label(self.root, text="Customer Name:", anchor=E)
        self.cust_name = Entry(self.root)
        cust_name.place(x=100, y=80)
        self.cust_name.place(x=200, y=80)
                
        city = Label(self.root, text="City:", anchor=E)
        self.city = Entry(self.root)
        city.place(x=100, y=110)
        self.city.place(x=200, y=110)
                
        state = Label(self.root, text="State: ", anchor=E)
        self.state = Entry(self.root)
        state.place(x=100, y=140)
        self.state.place(x=200, y=140)
        
        phone=Label(self.root,text="Phone Number:",anchor=E)
        self.phone=Entry(self.root)
        phone.place(x=100,y=170)
        self.phone.place(x=200,y=170)
                
        opening_balance = Label(self.root, text="Opening Balance: ", anchor=E)
        self.opening_balance = Entry(self.root)
        opening_balance.place(x=100, y=200)
        self.opening_balance.place(x=200, y=200)
                
        open_date = Label(self.root, text="Opening Date (dd/mm/yyyy):", anchor=E)
        self.open_date = Entry(self.root)
        open_date.place(x=100, y=230)
        self.open_date.place(x=270, y=230)
                
                # Creating Buttons and placing it
        self.acc_new = Button(self.root, text="New",command=self.new_record)
        self.acc_new.place(x=120, y=300)
                
        acc_save = Button(self.root, text="Save",command=self.save_record)
        acc_save.place(x=170, y=300)
                
        acc_delete = Button(self.root, text="Delete",command=self.delete_record)
        acc_delete.place(x=220, y=300)
                
        acc_exit = Button(self.root, text="Exit",command=self.exit_form)
        acc_exit.place(x=280, y=300)
                
        acc_first = Button(self.root, text="First",command=self.first_record)
        acc_first.place(x=120, y=350)
                
        acc_next = Button(self.root, text="Next",command=self.next_record)
        acc_next.place(x=170, y=350)
                
        acc_previous = Button(self.root, text="Previous",command=self.previous_record)
        acc_previous.place(x=220, y=350)
               
        ac_last = Button(self.root, text="Last",command=self.last_record)
        ac_last.place(x=290, y=350)
        
        try:
            sql="SELECT * FROM account_mast"
            self.cursor.execute(sql)
            self.results=self.cursor.fetchall()
            self.current_record=0
        except:
            print("Error in fetching data")
            
        self.first_record() 
        self.root.mainloop()  

