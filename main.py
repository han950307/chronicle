'''
Created on Aug 5, 2016

@author: han95
'''
from urllib2 import Request, urlopen, URLError
from urllib import quote_plus
import json
import Tkinter
import tkFont

root = Tkinter.Tk();
msg = ""
user = None
dukecardEntry = None
equipEntry = None
equipCheckoutEvent = None
eventEntry = None
event = None

""" FONTS """
titleFont = tkFont.Font(family="Helvetica", size=30)
errorFont = tkFont.Font(family="Helvetica", size=12, weight="bold")
dirFont = tkFont.Font(family="Helvetica", size=20)

""" DEFAULT FUNCTIONS """
def resetFrame():
  global root
  for widget in root.winfo_children():
    widget.destroy()
  textvar = Tkinter.StringVar()
  label = Tkinter.Label(root, textvariable=textvar, font=titleFont)
  textvar.set("The Chronicle Photo Equipment Checkout Station")
  label.pack()

def expandScreen():
  global root
  w, h = root.winfo_screenwidth(), root.winfo_screenheight()
  root.overrideredirect(1)
  root.geometry("%dx%d+0+0" % (w, h))
  root.focus_set()  # <-- move focus to this widget
  root.bind("<Control-R>", lambda e: e.widget.quit())  

""" API CALLS """
def getUInfo(dukecardID):
  requestURL = str('http://chronphoto-niblet.rhcloud.com/_api/getuser.php?dukecardID=') + str(dukecardID)
  request = Request(requestURL)
  try:
    response = urlopen(request)
  except URLError, e:
    print 'Error:', e
  jsonstr = response.read()
  data = json.loads(jsonstr)
  return data;

def parseJSON(jsonstr):
  data = json.loads(jsonstr)
  return data;

def getEquipInfo(equipID):
  requestURL = str('http://chronphoto-niblet.rhcloud.com/_api/getequipinfo.php?equipID=') + str(equipID)
  request = Request(requestURL)
  try:
    response = urlopen(request)
  except URLError, e:
    print 'Error:', e
  jsonstr = response.read()
  return jsonstr

def checkoutEquip(equipID):
  # API for checkout equipement.
  global user
  global event
  requestURL = str('http://chronphoto-niblet.rhcloud.com/_api/checkoutequip.php?equipID=') + \
               str(equipID) + str('&dukecardID=') + str(user['dukecardID']) + str('&eventDesc=') + str(quote_plus(event))
  request = Request(requestURL)
  try:
    response = urlopen(request)
  except URLError, e:
    print 'Error:', e
  jsonstr = response.read()
  return jsonstr

def checkinEquip(equipID):
  global user
  global event
  requestURL = str('http://chronphoto-niblet.rhcloud.com/_api/checkinequip.php?equipID=') + \
               str(equipID) + str('&dukecardID=') + str(user['dukecardID']) + str('&eventDesc=') + str(quote_plus(event))
  request = Request(requestURL)
  try:
    response = urlopen(request)
  except URLError, e:
    print 'Error:', e
  jsonstr = response.read()
  return jsonstr

""" PROGRAM STARTS HERE """
def loadLoginGUI(*args):
  global root
  global msg
  global user
  global dukecardEntry
  user = None
  
  resetFrame()
  expandScreen()

  root.bind("<Return>", mainGUILogic)
  parent = Tkinter.Frame(root)

  # Initialize Widgets
  directionTxt = Tkinter.StringVar()
  directionLabel = Tkinter.Label(parent, textvariable=directionTxt, font=dirFont)
  directionTxt.set("Scan your DukeCard to begin.")
  errorTxt = Tkinter.StringVar()
  errorLabel = Tkinter.Label(parent, textvariable=errorTxt, font=errorFont, fg="red")
  errorTxt.set(msg)
  dukecardEntry = Tkinter.Entry(parent)
  submitButton = Tkinter.Button(parent, text="Submit", command=mainGUILogic)
  
  # Format Widgets
  
  # Grid/Pack Widgets
  
  directionLabel.pack()
  dukecardEntry.pack()
  submitButton.pack()
  errorLabel.pack()
  
  parent.pack(expand=1)
  
  # Set cursor to entry
  dukecardEntry.focus()
  
  # Reset msg
  msg = ""

# process

def mainGUILogic(*args):
  global dukecardEntry
  global msg
  global user
  dukecardIDin = dukecardEntry.get()
  if (len(dukecardIDin) > 9):
    dukecardID = dukecardIDin[0:9]
  else:
    dukecardID = dukecardIDin
  user = getUInfo(dukecardID)
  if (user['dukecardID'] == '-1'):
    msg = "Photographer {} not found in database. Please register or contact photo editor.".format(dukecardID);
    loadLoginGUI()
    return
  loadMainGUI()

def loadMainGUI(*args):
  global reasonEntry
  global root
  global msg
  global user
  global eventEntry
  
  resetFrame()
  root.bind("<Return>", loadMainGUI)
  parent = Tkinter.Frame(root)
  
  # Initialize Widgets
  directionTxt = Tkinter.StringVar()
  directionLabel = Tkinter.Label(parent, textvariable=directionTxt, font=dirFont)
  directionTxt.set("""Welcome {}!
  
  Please choose an option.
  """.format(user['firstname']))
  errorTxt = Tkinter.StringVar()
  errorLabel = Tkinter.Label(parent, textvariable=errorTxt, font=errorFont, fg="red")
  errorTxt.set(msg)
  cibutton = Tkinter.Button(parent, text="RETURN EQUIPMENT", command=loadCheckinGUI)
  cobutton = Tkinter.Button(parent, text="CHECKOUT EQUIPMENT", command=loadPreCheckoutGUI)
  
  # Format Widgets
  
  # Grid/Pack Widgets
  
  directionLabel.pack()
  cobutton.pack()
  cibutton.pack()
  errorLabel.pack()
  
  parent.pack(expand=1)
  
  # Reset error message
  msg = ""

""" CHECKOUT LOGIC"""
def loadPreCheckoutGUI(*args):
  global reasonEntry
  global root
  global msg
  global user
  global eventEntry
  
  resetFrame()
  root.bind("<Return>", loadCheckoutLogic)
  parent = Tkinter.Frame(root)
  
  # Initialize Widgets
  directionTxt = Tkinter.StringVar()
  directionLabel = Tkinter.Label(parent, textvariable=directionTxt, font=dirFont)
  directionTxt.set("""CHECK OUT EQUIPMENT (Step 1/2)
  
  Please type in the name of your event. 
  """)
  errorTxt = Tkinter.StringVar()
  errorLabel = Tkinter.Label(parent, textvariable=errorTxt,font=errorFont,  fg="red")
  errorTxt.set(msg)
  eventEntry = Tkinter.Entry(parent)
  cibutton = Tkinter.Button(parent, text="SUBMIT", command=loadCheckoutGUI)
  
  directionLabel.pack()
  eventEntry.pack()
  cibutton.pack()
  errorLabel.pack()
  eventEntry.focus()
  
  parent.pack(expand=1)
  
  # Reset error message
  msg = ""
  

def loadCheckoutLogic(*args):
  global eventEntry
  global msg
  global event
  event = eventEntry.get()
  if (event == "" or event == None):
    msg = "Please type in the event for which you're checking out equipment."
    loadPreCheckoutGUI()
    return
  
  # logic to check whether the entry is a registered equipment.
  isEquip = True
  try:
    int(event)
  except ValueError:
    isEquip = False
  if (isEquip):
    equipID = event
    response = getEquipInfo(equipID)
    equip = parseJSON(response)
    if (equip['equipID'] == '-1'):
      msg = "Please type in the name of your event"
      loadPreCheckoutGUI()
      return
    else:
      msg = "Please input the name of your event before trying to check out any equipment."
      loadPreCheckoutGUI()
    return
  
  loadCheckoutGUI()

def loadCheckoutGUI():
  global msg
  global equipEntry
  
  resetFrame()
  root.bind("<Return>", checkoutSubmit)
  parent = Tkinter.Frame()
  
  # Initialize Widgets
  directionTxt = Tkinter.StringVar()
  directionLabel = Tkinter.Label(parent, textvariable=directionTxt, font=dirFont)
  directionTxt.set("""CHECK OUT EQUIPMENT (Step 2/2)
  
  Scan the barcode of all equipment you'd like to checkout.
  Click DONE when finished.
  """)
  errTxt = Tkinter.StringVar()
  errLabel = Tkinter.Label(parent, textvariable=errTxt, font=errorFont, fg="red")
  errTxt.set(msg)
  equipEntry = Tkinter.Entry(parent)
  submit = Tkinter.Button(parent, text="Checkout", command=checkoutSubmit)
  done = Tkinter.Button(parent, text="DONE", command=loadLoginGUI)
  
  # Format Widgets
  
  
  # Grid/Pack Widgets
  directionLabel.pack()
  equipEntry.pack()
  submit.pack()
  done.pack()
  errLabel.pack()
  parent.pack(expand=1)
  
  # Set Cursor to Entry
  equipEntry.focus()
  
  # Reset error msg
  msg = ""
  
def checkoutSubmit(*args):
  # almost done
  global msg
  global equipEntry
  global user
  equipID = equipEntry.get()
  
  response = getEquipInfo(equipID)
  equip = parseJSON(response)
  if (equip['equipID'] == '-1'):
    msg = "Equipment {} not found in database. Please contact the photo editor".format(equipID);
    loadCheckoutGUI()
    return
  isSuccess = parseJSON(checkoutEquip(equipID))
  if (isSuccess['success'] == '1'):
    msg = "{} checked out to {} {}.".format(equip['description'], user['firstname'], user['lastname'])
  else:
    msg = "There was an error {}. Please contact the photo editor.".format(isSuccess['error'])
  loadCheckoutGUI()
  
""" CHECKIN LOGIC """
def loadCheckinGUI():
  global msg
  global equipEntry
  
  resetFrame()
  root.bind("<Return>", checkinSubmit)
  parent = Tkinter.Frame()
  
  # Initialize Widgets
  directionTxt = Tkinter.StringVar()
  directionLabel = Tkinter.Label(parent, textvariable=directionTxt, font=dirFont)
  directionTxt.set("""RETURN EQUIPMENT
  
  Scan the barcode of all equipment you are returning.
  Click DONE when finished.
  """)
  errTxt = Tkinter.StringVar()
  errLabel = Tkinter.Label(parent, textvariable=errTxt, font=errorFont,  fg="red")
  errTxt.set(msg)
  equipEntry = Tkinter.Entry(parent)
  submit = Tkinter.Button(parent, text="Submit", command=checkinSubmit)
  done = Tkinter.Button(parent, text="DONE", command=loadLoginGUI)
  
  # Format Widgets
  
  
  # Grid/Pack Widgets
  directionLabel.pack()
  equipEntry.pack()
  submit.pack()
  done.pack()
  errLabel.pack()
  parent.pack(expand=1)
  
  # Set Cursor to Entry
  equipEntry.focus()
  
  # Reset error msg
  msg = ""
  
def checkinSubmit(*args):
  # almost done
  global msg
  global equipEntry
  equipID = equipEntry.get()
  response = getEquipInfo(equipID)
  equip = parseJSON(response)
  if (equip['equipID'] == '-1'):
    msg = "Equipment {} not found in database. Please contact the photo editor".format(equipID);
    loadCheckinGUI()
    return
  isSuccess = parseJSON(checkinEquip(equipID))
  if (isSuccess['success'] == '1'):
    msg = "{} returned.".format(equip['description'])
  else:
    msg = "There was an error {}. Please contact the photo editor.".format(isSuccess['error'])
  loadCheckinGUI()
  
""" START PROGRAM """
def startProgram():
  global root  
  root.bind("<Return>", loadLoginGUI)
  
  # Initialize Widgets
  directionTxt = Tkinter.StringVar()
  directionLabel = Tkinter.Label(root, textvariable=directionTxt)
  directionTxt.set("Press enter to begin the program.")
  
  # Grid/Pack Widgets
  directionLabel.pack()
  
  root.mainloop()

startProgram()
