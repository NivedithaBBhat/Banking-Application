import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter.constants import DISABLED, NORMAL



class Transaction():
        def new_record(self):
            self.tran_new['state']=DISABLED
            self.populate_blank()

        def save_record(self):
            tran_id=int(self.tran_id.get())
            account_id=int(self.account_id.get())
            tran_type=self.tran_type.get()
            tran_type=tran_type.upper()
            tran_date=self.tran_date.get()
            amount=float(self.amount.get())
            
            
            self.cursor.execute("select * from account_mast where account_id='%d'"%(account_id))
            z=self.cursor.fetchone()  
           
            if(tran_type=="D"):
            
                s="update account_mast set opening_balance=opening_balance+%f where account_id='%d'"%(amount,account_id)
                self.cursor.execute(s)
                self.cn.commit()
                messagebox.showinfo("Deposit","Deposited Successfully")
            elif(tran_type=="W" and float(z[5])>(amount-500)):
               
                s="update account_mast set opening_balance=opening_balance-%f where account_id='%d'"%(amount,account_id)
                self.cursor.execute(s)
                self.cn.commit()
                messagebox.showinfo("Withdraw","Withdrawed Successfully")
            else:
                messagebox.showerror("Error","No Enough Money to Withdraw")     
            
                   
            
            if self.tran_new['state']==DISABLED:
                sql="Insert into account_tran (tran_id,account_id,tran_type,tran_date,amount) values('%d','%d','%s','%s','%f')" %(tran_id,account_id,tran_type,tran_date,amount)
             
            else:
                sql="Update account_tran set tran_type='%s',tran_date='%s',amount='%f' where tran_id='%d'" %(tran_type,tran_date,amount,tran_id)
            try:
                self.cursor.execute(sql)
                self.cn.commit()
                sql="Select * from account_tran"
                self.results=self.cursor.fetchall() 
            except:
                self.cn.rollback()     
            self.tran_new["state"]=NORMAL
             
        def delete(self):
            tran_id=int(self.tran_id.get())
            s=messagebox.askyesno("Warning", "Are you Sure to Delete?")
            if(s==True):
                sql="Delete From account_tran WHERE tran_id='%d'" %(tran_id)
                try:
                    self.cursor.execute(sql)
                    self.cn.commit()
                    sql="Select * from account_tran"
                    self.results=self.cursor.fetchall() 
                    self.populate_blank()
                    self.previous_record()  
                except:
                    self.cn.rollback()
        def exit_form(self):
            self.root.destroy()
                     
        def first_record(self):
            if len(self.results)>0:
                self.current_record=0
                self.populate_record()
                 
        def next_record(self):
            if len(self.results)>0:
                self.current_record+=1
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
            self.tran_id.delete(0,END)
            self.tran_id.insert(0,row[0])
            self.account_id.delete(0,END)
            self.account_id.insert(0,row[1])
            self.tran_type.delete(0,END)
            self.tran_type.insert(0,row[2])
            self.tran_date.delete(0,END)
            self.tran_date.insert(0,row[3])
            self.amount.delete(0,END)
            self.amount.insert(0,row[4])
                  
        def populate_blank(self):
            self.tran_id.delete(0,END)
            self.account_id.delete(0,END)
            self.tran_type.delete(0,END)
            self.tran_date.delete(0,END) 
            self.amount.delete(0,END) 

            
        def __init__(self):
            config = {'user':'NivedithaBhat', 'password':'123', 'host':'localhost', 'database':'bank'}
            self.cn = mysql.connector.connect(**config)
            print("Connected")
            self.cursor = self.cn.cursor()
            try:
                #creating table
                sql = """Create Table account_tran
                (tran_id     int        Primary Key,
                account_id   int   References account_mast, 
                tran_type    char(1),
                tran_date    varchar(10),
                amount       decimal(7,2))"""
                self.cursor.execute(sql)
                print("Table created")
                
            except Exception :
                print()
            
            

            
           
            self.root = Tk()
            self.root.title("Banking Application")
            self.root.geometry("700x500")
            l1=Label(self.root,text="Transaction Details",fg="blue",bg="white",font="times 20 bold")
            l1.pack()
             
            tran_id = Label(self.root, text="Transaction Id:", anchor=E)
            self.tran_id = Entry(self.root)
            tran_id.place(x=100, y=50)
            self.tran_id.place(x=200, y=50)
            
            account_id = Label(self.root, text="Account Id:", anchor=E)
            self.account_id = Entry(self.root)
            account_id.place(x=100, y=80)
            self.account_id.place(x=200, y=80)
            
            tran_type = Label(self.root, text="Transaction Type (D/W):", anchor=E)
            self.tran_type = Entry(self.root)
            tran_type.place(x=100, y=110)
            self.tran_type.place(x=250, y=110)
            
            tran_date = Label(self.root, text="Transaction Date:", anchor=E)
            self.tran_date = Entry(self.root)
            tran_date.place(x=100, y=140)
            self.tran_date.place(x=200, y=140)
            
            amount = Label(self.root, text="Amount:", anchor=E)
            self.amount = Entry(self.root)
            amount.place(x=100, y=170)
            self.amount.place(x=200, y=170)
            
            #creating buttons and placing it
            self.tran_new = Button(self.root, text="New",command=self.new_record)
            self.tran_new.place(x=120, y=300)
            
            tran_save = Button(self.root, text="Save",command=self.save_record)
            tran_save.place(x=170, y=300)
            
            tran_delete = Button(self.root, text="Delete",command=self.delete)
            tran_delete.place(x=220, y=300)
            
            tran_exit = Button(self.root, text="Exit",command=self.exit_form)
            tran_exit.place(x=280, y=300)
            
            tran_first = Button(self.root, text="First",command=self.first_record)
            tran_first.place(x=120, y=350)
            
            tran_next = Button(self.root, text="Next",command=self.next_record)
            tran_next.place(x=170, y=350)
            
            tran_previous = Button(self.root, text="Previous",command=self.previous_record)
            tran_previous.place(x=220, y=350)
            
            tran_last = Button(self.root, text="Last",command=self.last_record)
            tran_last.place(x=290, y=350)
        
            try:
                sql="SELECT * FROM account_tran"
                self.cursor.execute(sql)
                self.results=self.cursor.fetchall()
                self.current_record=0
            except:
                print("Error in fetching data")
            self.first_record() 
            self.root.mainloop()  


