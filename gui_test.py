from tkinter import *

# names to grab of website
comic_names = ["calvinandhobbes","garfield","bc","pearlsbeforeswine",
    "peanuts","nonsequitur","wizardofid","pickles","foxtrot",
    "forbetterorforworse","getfuzzy","luann","doonesbury","andycapp",
    "frank-and-ernest"]
# names to display
comic_options = ["Calvin and Hobbes","Garfield","B.C.","Pearls Before Swine",
    "Peanuts","Non Sequitur","Wizard of Id","Pickles","FoxTrot",
    "For Better or For Worse","Get Fuzzy","Luann","Doonesbury","Andy Capp",
    "Frank and Ernest"]

def get_comics(comic_selections, load_btn):
    import requests
    import datetime
    import time
    from PIL import Image
    import os.path

    # comics to gather
    comics = []
    for i in (range(len(comic_names))):
        if(comic_selections[i]):
            comics.append(comic_names[i])

    # current date
    date_info = datetime.datetime.now()
    date = str(date_info.year) + "/" + str(date_info.month) + "/" + str(date_info.day)
    # check if its a new day
    with open("date.txt", 'r') as file:
        old_date = file.read()
        if str(date_info.date()) in old_date:
            new_day = False
        else:
            new_day = True

    # download comics if not already downloaded
    for iter in range(len(comics)):
        comic = comics[iter]

        # check if already download
        if os.path.isfile("Saved Comics/" + comic + ".jpg") and not new_day:
            continue

        # get image url from gocomics.com
        url = "https://www.gocomics.com/" + comic + "/" + date
        # check for internet connection
        internet = True
        try:
            r = requests.get(url, stream=True)
            if iter == 0:
                print("Downloading Comics. This should take about 5 seconds.")
            error_text.config(text ="")
            root.update_idletasks()
        except:
            internet = False
            error_text.config(text ='No internet connection')
            root.update_idletasks()
            break

        for i in range(len(r.text)):
            if r.text[i:(i+9)] == "assets.am":
                image_url = "https://" + r.text[i:(i+55)]
                break

        # download image using link from gocomics.com
        r = requests.get(image_url, stream=True)
        with open("Saved Comics/" + comic + ".jpg", "wb") as f:
            for data in r:
                f.write(data)

    # write last update date
    if new_day and (date_info.hour > 5) and len(comics) > 0 and internet :
        with open("date.txt", 'w') as file:
            file.write(str(date_info.date()))

    # display comics
    for iter in range(len(comics)):
        try:
            im = Image.open("Saved Comics/" + comics[iter] + ".jpg")
            im.show()
        except:
            Exception

    # change button text
    load_btn.config(text = "Load Comics!", relief = RAISED)


# initialte tkinter
root = Tk()
root.geometry("500x680")


# display header
header = Label(root, text ='Pick Your Comics!', font = "50")
header.pack()

# get old selections
with open("selections.txt", "r") as file:
    old_selections = [int(x) for x in file.read()]

# display checkboxes
comic_button_vars = []
comic_buttons = []
for i in range(len(comic_options)):
    comic_button_vars.append(IntVar())
    comic_buttons.append(Checkbutton(root, text = comic_options[i],
                                    variable = comic_button_vars[i],
                                    onvalue = 1,
                                    offvalue = 0,
                                    height = 2,
                                    width = 20))
    # load old selections
    if(old_selections[i]):
        comic_buttons[i].select()

    comic_buttons[i].pack()


# display load button
load_btn = Button(root, text = 'Load Comics!' ,bd = '5')

def load_comic_func():
    load_btn.config(text = "Loading!", relief = SUNKEN)
    root.update_idletasks()

    # set comic selections
    comic_selections = []
    for i in range(len(comic_options)):
        if(comic_button_vars[i].get()):
            comic_selections.append(True)
        else:
            comic_selections.append(False)
    # save old selections
    with open("selections.txt", "w") as file:
        for i in range(len(comic_selections)):
            file.write(str(int(comic_selections[i])))

    # remove loading text
    get_comics(comic_selections, load_btn)

load_btn.config(command = load_comic_func)
load_btn.pack()

error_text = Label(root, text ="", font = "50")
error_text.pack()

# loop through display
mainloop()



# Checkbutton1 = IntVar()
# Checkbutton2 = IntVar()
# Checkbutton3 = IntVar()

# Checkbutton1 = IntVar()
# Button1 = Checkbutton(root, text = "Calvin and Hobbes",
#                       variable = Checkbutton1,
#                       onvalue = 1,
#                       offvalue = 0,
#                       height = 2,
#                       width = 40)
# Button1.select()
#
# Checkbutton2 = IntVar()
# Button2 = Checkbutton(root, text = "Garfield",
#                       variable = Checkbutton2,
#                       onvalue = 1,
#                       offvalue = 0,
#                       height = 2,
#                       width = 10)
#
# Checkbutton3 = IntVar()
# Button3 = Checkbutton(root, text = "Peanuts",
#                       variable = Checkbutton3,
#                       onvalue = 1,
#                       offvalue = 0,
#                       height = 2,
#                       width = 10)
#
# Button1.pack()
# Button2.pack()
# Button3.pack()
#
