# -*- coding: utf-8 -*-
"""
Created on 06 ‎March ‎2018, ‏‎10:49:57 PM

@Author: Prashant Kumar


Sheet Location
--

Before Run

- *pip install google-api-python-client*
- *pip install tkinter*
- *pip install oauth2client*
"""

from __future__ import print_function
import tkinter
import httplib2
import os
import tkinter.messagebox

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient import discovery as apiclient

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class GoogleAPI:
    """
        Get the API intraface with google sheets
        
        Methods
        --------
        **__init__(string)** : Initilize with google sheet ID.
        
        **getSheet()** : returns all data contains in speradsheet.
        
        **insertRow(string, string, string)** : Insert a row in spreadsheet.
    """
    
    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = '' #Name of your application in API
    credential = []
    sheetId = []
    rangeName = []
    
    def __init__(self, sheet_id):
        self.APPLICATION_NAME = 'Python' #Name of your application in API
        self.sheetId = sheet_id 
        self.credential = self.get_credentials()
        self.rangeName = 'Sheet1!A2:E'



    def get_credentials(self):
        """
        Gets valid user credentials from storage.
    
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
    
        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-python-quickstart.json')
    
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
    
    def getSheet(self):
        """
        returns all data contains in speradsheet.
        """
        http = self.credential.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    
        result = service.spreadsheets().values().get(spreadsheetId=self.sheetId, range=self.rangeName).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            print('Data : ')
            for row in values:
                print(row)
        return values

    def insertRow(self, c1, c2, c3):
        """
            Insert a row in spreadsheet.
        """        
        service = apiclient.build('sheets', 'v4', credentials=self.credential)
        spreadsheet_id = self.sheetId
        range_ = self.rangeName
        value_input_option = 'RAW'
        insert_data_option = 'INSERT_ROWS'
        value_range_body = {
          "values": [
            [
              c1,
              c2,
              c3
            ]
          ]
        }
        
        request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
        request.execute()

def buttonClick():
    """onClickListner for submit button."""
    try:
        sheet = GoogleAPI('<your API key>')
        sheet.insertRow(name.get(), rollNo.get(), rate.get())
    except:  
        tkinter.messagebox.showerror("Error", "Not Save,, Check your Internet Connection.")
    tkinter.messagebox.showinfo("Info", "Saved to google sheet")



win = tkinter.Tk()


blue = tkinter.Frame(master=win, height=50, bg='royal blue')
blue.pack(fill=tkinter.BOTH, expand=1)

win.title("Google form Submision")
win.geometry("300x300+10+10")
win.resizable(0, 0)


l = tkinter.Label(blue, text="Google form Submision", font=("Helvetica", 16), bg="royal blue", fg="white")
l.pack()

lname = tkinter.Label(blue, text="Name", bg="royal blue")
lname.pack()

name = tkinter.StringVar()
name.set("")
name = tkinter.Entry(blue,textvariable=name)
name.pack()

lroll = tkinter.Label(blue, text="Roll No" , bg="royal blue")
lroll.pack()

roll = tkinter.StringVar()
roll.set("")
rollNo = tkinter.Entry(blue,textvariable=roll)
rollNo.pack()

lrate = tkinter.Label(blue, text="Rate Us", bg="royal blue")
lrate.pack()

rate = tkinter.StringVar()
rate.set("")
rate= tkinter.Entry(blue,textvariable=rate)
rate.pack()

submitBtn = tkinter.Button(blue, text="Submit", command=buttonClick,  bg="orange red")
submitBtn.pack()

close = tkinter.Button(blue, text='Quit', command=win.destroy,  bg="orange red")
close.pack()

win.mainloop()