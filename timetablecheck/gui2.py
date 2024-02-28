import easygui
import main

def gui (msg, title, default):
    result = easygui.enterbox(title, msg, default=default)
    print(result)
    return result

if __name__ == "__main__":
    default = main.readstate("adv.txt")
    result = gui("Timetable check", "Please input your order. To put in a variable, enclose it in curly brackets ({}) (e.g. {a[0]}) Key: a[0] = description, a[1] = room, a[2] = period, a[3] = teacher, a[4] = isinclass, a[5] = time left, a[6] = email, a[7] = next period desc, a[8] = next period room.", default)