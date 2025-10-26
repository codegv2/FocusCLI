import time, os, asyncio, aioconsole, json, playsound, colorama
from colorama import Fore, Back, Style
colorama.just_fix_windows_console()

base_dir = os.path.dirname(os.path.abspath(__file__))

json_path = os.path.join(base_dir, "focushistory.json")
with open(json_path) as json_file:
    json_data = json.load(json_file)

sound_path = os.path.join(base_dir, "sounds","bell_alarm.mp3")
with open(sound_path) as soundfile:
    soundfile = sound_path

def clearcli():
    os.system('cls' if os.name == 'nt' else 'clear')

clearcli()
while True:
    print(Fore.LIGHTBLACK_EX+"____________________________________________"+Fore.RESET)
    print(Style.BRIGHT+"## # \ FOCUS CLI / # ##"+Style.RESET_ALL)
    print()
    print(Fore.LIGHTGREEN_EX+"/focus:"+Fore.RESET,Fore.LIGHTYELLOW_EX+"set up your study session.")
    print(Fore.LIGHTGREEN_EX+"/focus_history:"+Fore.RESET,Fore.LIGHTYELLOW_EX+"check your focus history.")
    print(Fore.LIGHTGREEN_EX+"/clear_history:"+Fore.RESET,Fore.LIGHTYELLOW_EX+"clear your focus history.")
    print(Fore.LIGHTGREEN_EX+"/exit:"+Fore.RESET,Fore.LIGHTYELLOW_EX+"exit the program.")
    print(Fore.LIGHTBLACK_EX+"____________________________________________"+Fore.RESET)
    print()

    commandInput = input(Fore.GREEN)
    print(Fore.RESET)
    clearcli()

    if commandInput == "/focus":
        while True:
            backed = False
            while True:
                print(Fore.LIGHTYELLOW_EX+"Type in how much"+Fore.CYAN,"time",Fore.LIGHTYELLOW_EX+"you're going to study in minutes")
                print(Fore.LIGHTYELLOW_EX+"Like this",Fore.LIGHTBLACK_EX+"->",Fore.CYAN+"'<minutes>'.",Fore.GREEN+"Example: 25")
                print(Fore.GREEN+Style.BRIGHT+"#"+Style.RESET_ALL,Fore.LIGHTYELLOW_EX+"Type",Fore.LIGHTGREEN_EX+"'/back'",Fore.LIGHTYELLOW_EX+"to return to the menu.")
                print()

                focusTimeInput = input(Fore.GREEN)
                print(Fore.RESET)

                if focusTimeInput == "/back":
                    backed = True
                    break

                try:
                    if int(focusTimeInput) >= 1:
                        break
                except:
                    pass
                clearcli()
                print(Fore.RED+Style.BRIGHT+"# TIME ISN'T VALID. PLEASE TYPE IN THE TIME AGAIN. #"+Fore.RESET+Style.RESET_ALL)
                print()
            
            if backed == True:
                clearcli()
                break

            while True:
                print(Fore.LIGHTYELLOW_EX+"What are you going to study for?: ")
                print(Fore.LIGHTBLACK_EX+"(Max: 40 characters)")
                print(Fore.GREEN+Style.BRIGHT+"#"+Style.RESET_ALL,Fore.LIGHTYELLOW_EX+"Type",Fore.LIGHTGREEN_EX+"'/back'",Fore.LIGHTYELLOW_EX+"to return to the menu.")
                print()

                focusNameInput = input(Fore.GREEN)
                print(Fore.RESET)

                if focusNameInput == "/back":
                    backed = True
                    break

                if len(focusNameInput) > 0 and len(focusNameInput) < 40:
                    break
                else:
                    clearcli()
                    print(Fore.RED+Style.BRIGHT+"# NAME ISN'T VALID. PLEASE TYPE IN THE NAME AGAIN. #"+Fore.RESET+Style.RESET_ALL)
                    print()
                    pass

            if backed == True:
                clearcli()
                break
            
            def addZero(number):
                if len(str(number)) <= 1:
                    return f"0{number}"
                else:
                    return number

            focusDateStart = f"{addZero(time.localtime().tm_mday)}/{addZero(time.localtime().tm_mon)}/{addZero(time.localtime().tm_year)}"
            focusTimeStart = f"{addZero(time.localtime().tm_hour)}:{addZero(time.localtime().tm_min)}:{addZero(time.localtime().tm_sec)}"

            clearcli()

            # focusDateStart
            # focusTimeStart

            # focusNameInput
            # focusTimeInput

            focusTimeInput = int(focusTimeInput)
            secondsFTI = 00
            stop = False
            stopSound = False
            lastedXTime = 0

            async def timeRegression(min, sec):
                global stop, lastedXTime
                min -= 1
                sec = 59
                while True:
                    if stop == True:
                        break
                    elif min < 0:
                        clearcli()
                        print(Fore.LIGHTBLACK_EX+"________________________"+Fore.RESET)
                        print(Style.BRIGHT+Fore.GREEN+"#"+Style.RESET_ALL,Fore.LIGHTYELLOW_EX+"Session ended!",Style.BRIGHT+Fore.GREEN+"#"+Style.RESET_ALL+Fore.RESET)
                        print(Fore.LIGHTYELLOW_EX+"Press",Fore.LIGHTGREEN_EX+"'Enter'",Fore.LIGHTYELLOW_EX+"to exit.")
                        print(Fore.LIGHTBLACK_EX+"________________________"+Fore.RESET)
                        while True:
                            await asyncio.sleep(0.00001)
                            if stopSound == True:
                                break
                            playsound.playsound(soundfile)
                        return lastedXTime

                    printMin = str(min)
                    printSec = str(sec)

                    if len(printSec) <= 1:
                        printSec = f"0{sec}"
                    else:
                        pass

                    if len(printMin) <= 1:
                        printMin = f"0{min}"
                    else:
                        pass

                    print(Fore.LIGHTYELLOW_EX+"Time left:",Fore.CYAN+f"{printMin}",Fore.GREEN+"min,",Fore.CYAN+f"{str(printSec)}",Fore.GREEN+"secs",Fore.RESET, end="\r")
                    await asyncio.sleep(1)
                    sec -= 1
                    if sec < 0:
                        min -= 1
                        sec = 59
                        lastedXTime += 1

            async def enterToLeave():
                global stop, stopSound
                await aioconsole.ainput(Fore.BLACK)
                stop = True
                stopSound = True
                return stop, stopSound

            async def timer():
                await asyncio.gather(
                    timeRegression(focusTimeInput, secondsFTI),
                    enterToLeave(),
                    )

            print(Fore.LIGHTBLACK_EX+"_________________________________"+Fore.RESET)
            print(Fore.LIGHTYELLOW_EX+"Studying for:",Fore.CYAN+f"{focusNameInput}")
            print(Fore.LIGHTYELLOW_EX+"Press",Fore.LIGHTGREEN_EX+"'Enter'",Fore.LIGHTYELLOW_EX+"to end the session.")
            print(Fore.LIGHTBLACK_EX+"_________________________________"+Fore.RESET)
            print()
            asyncio.run(timer())
            clearcli()

            try:
                session = {
                    "name":focusNameInput,
                    "inputtime":focusTimeInput,
                    "date":focusDateStart,
                    "hourstart":focusTimeStart,
                    "lastedtime":lastedXTime,
                }

                json_data[len(dict(json_data).keys())+1] = session

                with open(json_path, "w") as json_file:
                    json.dump(json_data, json_file)
            except:
                print(Fore.RED+Style.BRIGHT+"# SOMETHING WENT WRONG. CHECK YOUR '.JSON' FILE. #"+Fore.RESET+Style.RESET_ALL)

            break

    elif commandInput == "/focus_history":
        try:
            with open(json_path) as json_file:
                json_data = json.load(json_file)
        except:
            print("error")

        page = 0
        while True:
            if json_data == {}:
                clearcli()
                print(Fore.LIGHTBLUE_EX+"# You don't have any focus history yet!"+Fore.RESET)
                break
            
            reversed_json_data = list(dict(json_data).keys())
            reversed_json_data.reverse()
            
            while True:
                p = []
                pageDict = {}
                arrayCount = 0
                pageCount = 0
                for k in reversed_json_data:
                    p.append(k)
                    arrayCount += 1
                    pageDict[f"{pageCount}"] = p
                    if arrayCount % 2 == 0:
                        p = []
                        pageCount += 1
                        pass
                break
            
            print(Style.BRIGHT+"# # SESSIONS # #"+Style.RESET_ALL)
            print(Fore.LIGHTBLACK_EX+"___________________"+Fore.RESET)
            for k in pageDict[f"{page}"]:
                name = json_data[k]["name"]
                date = json_data[k]["date"]
                hourstart = json_data[k]["hourstart"]
                lastedtime = json_data[k]["lastedtime"]

                print(Fore.RESET+Style.BRIGHT+"#",Fore.CYAN+"Session",f"{k}",Fore.MAGENTA+"-",Fore.CYAN+f"{name}"+Style.RESET_ALL)
                print(Style.BRIGHT+Fore.MAGENTA+"-"+Style.RESET_ALL,Fore.LIGHTYELLOW_EX+"The date was",Fore.GREEN+f"{date}")
                print(Style.BRIGHT+Fore.MAGENTA+"-"+Style.RESET_ALL,Fore.LIGHTYELLOW_EX+"Started at",Fore.GREEN+f"{hourstart}")
                if lastedtime == 1:
                    print(Style.BRIGHT+Fore.MAGENTA+"-"+Style.RESET_ALL,Fore.LIGHTYELLOW_EX+"The session lasted a minute")
                elif lastedtime < 1:
                    print(Style.BRIGHT+Fore.MAGENTA+"-"+Style.RESET_ALL,Fore.LIGHTYELLOW_EX+"The session lasted less than a minute.")
                else:
                    print(Style.BRIGHT+Fore.MAGENTA+"-"+Style.RESET_ALL,Fore.LIGHTYELLOW_EX+"The session lasted",f"{lastedtime}","minutes")
                print()
            
            print(Fore.RESET+Style.BRIGHT+"#",Fore.MAGENTA+"Page",f"{page+1}"+Fore.LIGHTBLACK_EX+"/"+Fore.MAGENTA+f"{len(list(pageDict.keys()))}"+Style.RESET_ALL)
            print(Fore.LIGHTBLACK_EX+"_________________________________"+Fore.RESET)
            print(Fore.LIGHTGREEN_EX+"/exit:"+Fore.RESET,Fore.LIGHTYELLOW_EX+"return to the menu.")
            print(Fore.LIGHTGREEN_EX+"/np:"+Fore.RESET,Fore.LIGHTYELLOW_EX+"next page.")
            print(Fore.LIGHTGREEN_EX+"/pp:"+Fore.RESET,Fore.LIGHTYELLOW_EX+"previous page.")
            print(Fore.LIGHTGREEN_EX+"/sp:"+Fore.RESET,Fore.LIGHTYELLOW_EX+"select the page.")
            print(Fore.LIGHTBLACK_EX+"_________________________________"+Fore.RESET)

            fhInput = input(Fore.GREEN)

            if fhInput == "/exit":
                print(Fore.RESET)
                clearcli()
                break
            elif fhInput == "/np":
                if page < len(list(pageDict.keys()))-1:
                    page += 1
            elif fhInput == "/pp":
                if page < len(list(pageDict.keys())) and page > 0:
                    page -= 1
            elif fhInput == "/sp":
                pageInput = input(Fore.MAGENTA)
                try:
                    if f"{int(pageInput)-1}" in pageDict:
                        page = int(pageInput)-1
                except:
                    pass
            print(Fore.RESET)
            clearcli()

    elif commandInput == "/exit":
        break
    elif commandInput == "/clear_history":
        with open(json_path, "w") as json_file:
            json.dump({}, json_file)
        print(Fore.LIGHTBLUE_EX+"# Focus history cleared."+Fore.RESET)
    else:
        pass
print(Fore.GREEN+"# FocusCLI exited successfully."+Fore.RESET)
