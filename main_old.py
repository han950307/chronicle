from urllib2 import Request, urlopen, URLError
import json
import Tkinter

root = Tkinter.Tk()

def resetFrame():
  for widget in root.winfo_children():
    widget.destroy()
  textvar = Tkinter.StringVar()
  label = Tkinter.Label(root, textvariable=textvar)
  textvar.set("Chronicle Equipment Checkout Station")
  label.pack()

def getUInfo(dukecardID):
  requestURL = str('http://chronphoto-niblet.rhcloud.com/_api/getuser.php?dukecardID=')+str(dukecardID)
  request = Request(requestURL)
  try:
    response = urlopen(request)
  except URLError, e:
    print 'Error:', e
  jsonstr = response.read()
  data = json.loads(jsonstr)
  return data;

# Write code to put checkout info into database.
def checkout(equipID):
  print equipID

# When equipment is scanned this loads.
def checkoutEquip(*args):
  global entry
  equipID = entry.get()
  checkout(equipID)
  loadCheckoutEquipGUI()

# When checkout is clicked then ID is scanned, this loads.
def loadCheckoutEquipGUI():
  global entry
  global user
  global msg
  resetFrame()
  root.bind("<Return>", checkoutEquip)
  textvar = Tkinter.StringVar()
  textvar2 = Tkinter.StringVar()
  label = Tkinter.Label(root, textvariable=textvar)
  label2 = Tkinter.Label(root, textvariable=textvar2)
  textvar.set("Please scan all equipment, and click DONE when finished scanning.")
  textvar2.set("Welcome, {}!".format(user['firstname']))
  entry = Tkinter.Entry(root)
  button = Tkinter.Button(root, text="Submit", command=checkoutEquip)
  label2.pack()
  label.pack()
  entry.pack()
  button.pack()
  entry.focus()
  doneButton = Tkinter.Button(root, text="DONE", command=loadMainGUI)
  doneButton.pack()

# When ID is scanned, this logic happens.
def onCheckoutSubmit(*args):
  inputid = entry.get()
  dukecardID = inputid[:9]
  global user
  global msg
  user = getUInfo(dukecardID)
  if (user['dukecardID'] == '-1'):
    msg = "{} not found in database. Please register or contact photo editor.".format(dukecardID);
    loadCheckoutGUI()
  else:
    loadCheckoutEquipGUI()

# When checkout button is clicked, this loads.
def loadCheckoutGUI():
  global entry
  global msg
  resetFrame()
  textvar = Tkinter.StringVar()
  root.bind("<Return>", onCheckoutSubmit)
  label = Tkinter.Label(root, textvariable=textvar)
  textvar.set(msg)
  msg = ""
  label.pack()
  entry = Tkinter.Entry(root)
  button = Tkinter.Button(root, text="Submit", command=onCheckoutSubmit)
  entry.pack()
  button.pack()
  entry.focus()

def loadCheckinGUI():
  print "hello"

# Start here
def loadMainGUI():
  global msg
  msg = ""
  resetFrame()
  #w, h = root.winfo_screenwidth(), root.winfo_screenheight()
  #root.overrideredirect(1)
  #root.geometry("%dx%d+0+0" % (w, h))
  #root.focus_set()  # <-- move focus to this widget
  #root.bind("<Escape>", lambda e: e.widget.quit())
  
  
  cobutton = Tkinter.Button(root, text="Check Out", command = loadCheckoutGUI)
  cibutton = Tkinter.Button(root, text="Check In", command = loadCheckinGUI)
  
  cobutton.pack()
  cibutton.pack()
  
def startHere():
  global msg
  msg = ""
  resetFrame()
  root.bind("<Return>", loadCheckoutGUI)
  submit = Tkinter.Button(root, text="Submit", command = loadCheckoutGUI)
  entry.pack()
  
  textvar = Tkinter.StringVar()
  label = Tkinter.Label(root, textvariable=textvar)
  textvar.set("Scan your DukeCard to begin.")
  
  textvar2 = Tkinter.StringVar()
  label = Tkinter.Label(root, textvariable=textvar2)
  textvar2.set(msg)
  
  label.pack()
  submit.pack()
  
  root.mainloop()

loadMainGUI()