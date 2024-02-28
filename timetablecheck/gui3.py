import easygui
import main
import update

def gui (msg, title, default):
    result = easygui.enterbox(msg, title, default=default)
    print(result)
    return result

if __name__ == "__main__":
    default = main.readstate("details.txt")
    if default == "":
        a = gui("Please enter your cookie node. To get it, go to the SEQTA website, hit option+command+i and navigate to Network, refresh your page and look for the 'timetable' section. Click it and scroll down until you find JSESSIONID: and a node. Copy the node (without the 'JSESSIONID:') and paste the number in here:", "New user detected!", default)
    else:
        a = gui("Please enter your cookie node. To get it, go to the SEQTA website, hit option+command+i and navigate to Network, refresh your page and look for the 'timetable' section. Click it and scroll down until you find JSESSIONID: and a node. Copy the node (without the 'JSESSIONID:') and paste the number in here:", "Change cookie node", default)
    if a != None:
        main.writestate(a, "details.txt")
    else:
        exit()
    a = update.updater()
    if a.content == b"{\"status\":\"401\"}":
        main.rumps.alert("Oops!", "There was a problem with fetching the timetable. Try to re-input your cookie node in 'Change Cookie Node', or if you don't have school today, use advanced update and select another date.")
    else:
        main.rumps.alert("Working!", "Your cookie worked. You should be able to use timetablecheck now.")
