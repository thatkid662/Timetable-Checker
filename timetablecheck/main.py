import rumps
import update
import subprocess
import pyperclip
import search
import webbrowser
import os
import re
from datetime import datetime, time
from AppKit import NSBundle
bundle = NSBundle.mainBundle()
info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
info['LSUIElement'] = '1'

cwd = os.path.expandvars("/Users/$USER/Documents/timetablecheck")

def get_details():
    b = search.getcurrentperiod()
    json = periodjson(b[0], b[1])
    njson = periodjson(b[0]+1, b[1])
    teacher = getvalue(json, 'staff')
    email = getvalue(json, "staffEmail")
    isinclass = getvalue(json, "label")
    desc = getvalue(json, 'description')
    ndesc = getvalue(njson, 'description')
    room = getvalue(json, 'room')
    nroom = getvalue(njson, 'room')
    end = getvalue(json, 'until')
    start = getvalue(json, 'from')
    try:
        hours, minutes, seconds = [int(s) for s in end.split(':')]
    except ValueError:
        timebetween = "No school"
    else:
        now = datetime.now()
        dateend = datetime.combine(datetime.now().date(), time(hours, minutes, seconds))
        timebetween = dateend - now
        timebetween = str(timebetween)[:-7]
        if timebetween[0] == "-":
            timebetween = "Break"
    return [desc, room, b, teacher, isinclass, timebetween, email, ndesc, nroom]

def periodjson(p, t):
    a = getvalue(search.loadjson(), 'items')
    if a == [] or t == 0:
        return -1
    formatted_time = t[p-1].strftime("%I:%M %p")
    if formatted_time[0] == "0":
        formatted_time = formatted_time[1:]
    tsyntax = f'Period {p}. {formatted_time}'
    tsyntax = tsyntax[:-3]
    json = search.search(search.loadjson(), "period", tsyntax)
    return json

@rumps.clicked("More...", "Email teacher")
def emailteacher(_):
    a = get_details()
    if a != -1:
        path2 = "compose-email.scpt"
        pyperclip.copy(a[6])
        subprocess.Popen(["osascript", path2], stdout=subprocess.DEVNULL)
    else:
        rumps.alert("Oops!", "You can't do that, your not in school silly.", None, None, None, "resources/image.svg")

@rumps.clicked("More...", "Customize Advanced...")
def customize(_):
    b = get_details()
    while True:
        result = subprocess.run(["/usr/local/bin/python3", "gui2.py"], cwd=cwd, capture_output=True, text=True)
        stdout = result.stdout[:-1]
        if stdout == 'None' or stdout == "":
            break
        else:
            writestate(stdout, "adv.txt")
            break
    
@rumps.clicked("More...", "Customize Advanced...", "Reset customization")
def resetc(_):
    writestate("{(a[0] + ', ' + a[1]) if a[0] != 0 else ''}{(', ' + a[4]) if a[4] != '' else ''}, {a[5] if str(a[5])[0] != '-' else 'Break'}", "adv.txt")

@rumps.clicked('Textbooks', 'Campion')
def opencampion(self):
    webbrowser.open('https://ststephens-duncraig.campion.education/my-books')

@rumps.clicked('Textbooks', 'Cambridge')
def opencampion(self):
    webbrowser.open('https://www.cambridge.org/go/resources')

@rumps.clicked('Textbooks', 'Oxford oBook')
def opencampion(self):
    webbrowser.open('https://hub.oxforddigital.com.au/library.html')

@rumps.clicked('Update Now...')
def u(self):
    response = update.updater()
    if len(response.content) < 100:
        rumps.alert("Unsuccessfully updated", "Unsuccessfully updated. Please check your cookie node.", icon_path="resources/download.svg")
    else:
        rumps.alert("Successfully updated",f"Successfully updated timetable. It took {round(response.elapsed.total_seconds(),2)} seconds and the file size was {round(len(response.content) / 1000,1)} kB.","Cool!",None,None,'resources/download.svg')

@rumps.clicked('Update Now...', 'Advanced...')
def advancedupdate(_):
    b = 0
    while True:
        result = subprocess.run(["/usr/local/bin/python3", "gui.py"], cwd=cwd,capture_output=True, text=True)
        a = result.stdout[2:-3]
        try:
            start, end = a.split("', '")
        except ValueError:
            break
        else:
            response = update.updater(start, end)
            if (response != -1 and response.content != 0):
                rumps.alert("Successfully updated",f"Successfully updated timetable. It took {round(response.elapsed.total_seconds(),2)} seconds and the file size was {round(len(response.content) / 1000,1)} kB.)","Cool!",None,None,'resources/download.svg')
                break
            else:
                rumps.alert('Invalid input.')

@rumps.clicked("More...", "Open Timetable")
def opentimetable(_):
    if datetime.now().isocalendar().week % 2 == 0:
        subprocess.run(["open", "-a", "Preview", "resources/b.png"], cwd=cwd)
    else: 
        subprocess.run(["open", "-a", "Preview", "resources/a.png"], cwd=cwd)

def writestate(state, file="state.txt"):
    with open (file, "w") as f:
        f.write(str(state))

def readstate(file="state.txt"):
    with open (file, "r") as f:
        return f.read()

def getvalue(json, key, default=''):
    value = search.search_(json, key)
    value = value.get(key, default)
    return value

class MyMenuApp(rumps.App):
    def __init__(self):  # Note the double underscores for the constructor
        super(MyMenuApp, self).__init__("")
        
        if readstate("cookie.txt") == "":
            subprocess.run(["/usr/local/bin/python3", "gui3.py"], cwd=cwd)

        self.icon = "resources/logo.png"
        self.menu = [
            [rumps.MenuItem('Update Now...', None, key='h', icon='resources/download.svg'), [
                "Advanced...",
            ]],
            "Enable Display", 
            ["More...", [
            ]]
        ]

        @rumps.clicked('Enable Display')
        def toggle(sender):
            sender.state = not sender.state
            writestate(sender.state)
            display(f'{sender.state}')
        
        @rumps.timer(300)
        def updatetimer(_):
            update.updater()

        @rumps.timer(1)
        def timer(_):
            display(f'{readstate()}')
            a = datetime.now().time()
            a = a.strftime("%H:%M:%S")
            if a == "15:20:00":
                exit()

        @rumps.clicked('More...', "Change Cookie Node")
        def changeid(_):
            subprocess.run(["/usr/local/bin/python3", "gui3.py"], cwd=cwd)

        @rumps.clicked("More...", "Check Attendance")
        def checkattendance(_):
            a = get_details()
            rumps.alert("Attendance", f"Your attendance is currently '{a[4]}'.", icon_path="resources/image.svg")

        @rumps.clicked("More...", "Toggle Advanced")
        def more(sender):
            sender.state = not sender.state
            if sender.state == 1: 
                writestate(2)
                display("2")
            else: 
                writestate(0)
                display("0")

        @rumps.clicked("More...", "Debug")
        def debug(_):
            a = get_details()
            rumps.alert("Debug Menu", a)
        
        def periodjson(p, t):
            a = getvalue(search.loadjson(), 'items')
            if a == [] or t == 0:
                return -1
            formatted_time = t[p-1].strftime("%I:%M %p")
            if formatted_time[0] == "0":
                formatted_time = formatted_time[1:]
            tsyntax = f'Period {p}. {formatted_time}'
            tsyntax = tsyntax[:-3]
            json = search.search(search.loadjson(), "period", tsyntax)
            return json

        def display(sender, self=self):
            if sender == '0':
                self.icon = 'resources/logo.png'
                self.title = ''
            elif sender == '2':
                a = get_details()
                self.icon = None
                if a != -1:
                    adv = readstate("adv.txt")
                    b = re.findall(r"{([^}]*)}", adv)
                    for content in b:
                        e = eval(content, {"a": a})
                        adv = adv.replace("{" + str(content) + "}", str(e))
                    self.title = adv
                else:
                    self.title = "No period."
            else:
                a = get_details()
                if a == -1:
                    period = 'No period'
                else:
                    period = f'(P{a[2]})'
                if period == 'No period':
                    self.title = period
                    self.icon = None
                else:
                    self.title = f'{a[0]}, {a[1]}'
                    self.icon = None

if __name__ == "__main__":  # Ensure this block is present
    writestate(0)
    app = MyMenuApp()  # Create an instance of the app
    app.run()  # Call run() on the instance