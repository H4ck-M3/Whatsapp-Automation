import os
import time
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


launch_interactive()

