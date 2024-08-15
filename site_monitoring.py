#to create a network monitoring tool to see if whether sites are up or down

import requests


websites_list = ["https://api.github.com", "https://api.github.com/invalid"]

def check_status():
    for url in websites_list:
        response = requests.get(url)
        if response.status_code == 200:
            print(url + " is up")
        elif response.status_code == 404:   #means requested page could not be found in the server . 
            print(url + " is down")



print("current websites link are these")
for url in websites_list:
    print(url)


extra = input("Do you want to add anything (y/n)")
if(extra=="n"):
    check_status()
    
if(extra=="y"):
    url_extra = input("Enter the url")
    websites_list.append(url_extra)
    check_status()



