import requests
import main
from datetime import datetime

def updater(f=None, t=None):
    website = main.readstate("website.txt")
    cookie = main.readstate("cookie.txt")
    cookies = {
    'JSESSIONID': cookie,
    }
    if f != None and t != None:
        json_data = {
            'from': f'{f}',
            'until': f'{t}',
            'student': 5000,
        }
    else:
        now = datetime.now().date()
        now = now.strftime("%Y-%m-%d")
        json_data = {
            'from': f'{now}',
            'until': f'{now}',
            'student': 5000,
        }
    try:
        response = requests.post((website + '/seqta/student/load/timetable?'), cookies=cookies, headers=None, json=json_data)
    # Check for successful response
    except:
        print('An exception occured, probably invalid input')
        return -1

    if response.status_code == 200:
    # Open the file in binary write mode
            with open(f"times.json", "wb") as f:
                # Write the response content to the file
                f.write(response.content)
    else:
        print(f"Error downloading file: {response.status_code}")
    return response

if __name__ == "__main__":
    updater()
