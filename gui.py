import os
import time
from datetime import datetime
from Config.selenium_config import get_browser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


browser = get_browser()
browser.get("https://web.whatsapp.com/")

time.sleep(45)

srch_input_class = "_13NKt copyable-text selectable-text"
srch_input_class = srch_input_class.split(" ")
srch_input_class = ".".join(srch_input_class)
srch_input_elt = browser.find_element(By.CLASS_NAME, srch_input_class)
srch_input_elt.send_keys("", Keys.RETURN)

time.sleep(2)

msg_input_class = "fd365im1 to2l77zo bbv8nyr4 mwp4sxku gfz4du6o ag5g9lrv"
msg_input_class = msg_input_class.split(" ")
msg_input_class = ".".join(msg_input_class)
msg_input_elt = browser.find_element(By.CLASS_NAME, msg_input_class)
msg_input_elt.send_keys("", Keys.RETURN)


def send_message(chat, message):
    srch_input_elt.clear()
    srch_input_elt.send_keys(chat, Keys.RETURN)
    msg_input_elt = browser.find_element(By.CLASS_NAME, msg_input_class)
    for character in message:
        msg_input_elt.send_keys(character)
    msg_input_elt.send_keys("", Keys.RETURN)


def cmd(command):
    command = command + " > " + os.path.join("Assets", "command_results.txt")
    output = ""
    os.system(command)
    
    with open(os.path.join("Assets", "command_results.txt"), "r+") as results:
        output = results.read()
    
    return output


# Interactive console
def launch_interactive():
    stop = 0
    mode = "message"
    chat = "Dev Test"
    while stop == 0:
        print("Current mode : Commande") if mode == "command" else print("Current mode : Message")
        print("Current chat: " + chat)
        
        ask = input("Saisir la commande > ") if mode == "command" else input("Saisir le message : ")
        if (ask == "quit"):
            browser.close()
            break
        elif (len(ask) >= 8 and ask[0:8] == "set mode"):
            ask = ask[9:]
            mode = ask
        elif (len(ask) >= 8 and ask[0:8] == "set chat"):
            ask = ask[9:]
            chat = ask
        else:
            if (mode == "command"):
                output = str(cmd(ask))
                send_message(chat, output)
            elif (mode == "message"):
                send_message(chat, ask)
            else:
                send_message(chat, ask)


def get_next_hop(patterns) -> list:
    hour = datetime.utcnow().hour
    min = datetime.utcnow().minute
    hour = "0"+str(hour) if hour < 10 else str(hour)
    min = "0"+str(min) if min < 10 else str(min)
    minute_set = []
    to_return = list()
 
    keys = patterns.keys()
    # print("Current time : " + str(hour) + ":" + str(min))
    for key in keys:
        if (str(key) == str(hour)):
            minute_set = patterns[key]
            # print("The minute set is : " + str(minute_set))
            for minute in minute_set:
                if (minute == str(min)):
                    to_return.append(key)
                    to_return.append(minute)
                    return to_return
                elif (int(min) < int(minute)):
                    to_return.append(key)
                    to_return.append(minute)
                    return to_return
                else:
                    if (hour == "23"):
                        to_return.append("00")
                        to_return.append("00")
                        return to_return
        else:
            if (int(key) > int(hour)):
                to_return.append(key)
                to_return.append(patterns[str(key)][0])
                return to_return
            else:
                continue
        

        

def launch_automated():
    patterns = {}
    message_sent = 0
    for i in range(0, 24, 1):
        if (i<10):
            patterns["0"+str(i)] = []
        else:
            patterns[str(i)] = []

    # Add direct and reverse patterns
    keys = patterns.keys()
    for key in keys:
        if (key != "00" and key != "11" and key != "22"):
            patterns[key].append(key)
        if (int(key) not in [16, 17, 18, 19]):
            patterns[key].append(key[::-1])
    
    # Populating "00"
    for i in range(1, 6, 1):
        patterns["00"].append(str(i)+str(i))

    # Sorting
    for key in keys:
        patterns[key].sort()

    
    while 1:
        print("Listening...")
        hour = datetime.utcnow().hour
        min = datetime.utcnow().minute
        hour = "0"+str(hour) if hour < 10 else str(hour)
        min = "0"+str(min) if min < 10 else str(min)
        tmp = get_next_hop(patterns)
        print("Current time : " + str(hour) + ":" + str(min))
        print("The next hop is : "+ str(tmp[0]) + ":" + str(tmp[1]))
        if (str(tmp[0]) == str(hour) and str(tmp[1]) == str(min) and message_sent == 0):
            print("Sending message...")
            message = str(tmp[0]) + ":" + str(tmp[1])
            send_message("Marshall", message)
            print("message sent !")
            message_sent = 1
        print("____________________")
        time.sleep(1)


launch_automated()