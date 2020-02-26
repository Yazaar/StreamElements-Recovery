from bs4 import BeautifulSoup
import re, json, requests

filename = 'parseme.txt'

def leaderboardData(userid):
    r = requests.get(f'https://api.streamelements.com/kappa/v2/points/{userid}/alltime?limit=0').json()
    r = requests.get(f'https://api.streamelements.com/kappa/v2/points/{userid}/alltime?limit={r["_total"]}').json()
    alltime = {}
    for user in r['users']:
        alltime[user['username']] = user['points']
    return alltime

def csvParser(usernames, watchtimes, points):
    csvWatchtime = ''
    csvPoints = ''
    csvBoth = ''
    for user in usernames:
        if user in watchtimes and user in points:
            csvBoth += f'{user},,{points[user]["current"]},{points[user]["max"]},{watchtimes[user]}\n'
        elif user in watchtimes:
            if perMinute == None:
                currentPts = 'CURRENT_POINTS'
                maxPts = 'MAX_POINTS'
            else:
                currentPts = int(watchtimes[user] * perMinute)
                maxPts = currentPts
            csvWatchtime += f'{user},,{currentPts},{maxPts},{watchtimes[user]}\n'
        else:
            if perMinute == None:
                wtime = 'WATCHTIME'
            else:
                wtime = int(points[user]["max"] / perMinute)
            csvPoints += f'{user},,{points[user]["current"]},{points[user]["max"]},{wtime}\n'
    return (csvWatchtime, csvBoth, csvPoints)

def handleWatchtime(user, duration):
    total_time = 0
    for i in range(int(len(duration)/2)):
        time_number = int(duration[i*2])
        time_type = duration[i*2+1].lower()
        if time_type[-1] == 's':
            time_type = time_type[:-1]
        for j in convertData:
            if j == time_type:
                total_time += time_number * convertData[j]
                break
    return (user, total_time)

with open('convert.json', 'r') as f:
    convertData = json.load(f)

with open('points-per-minute.txt', 'r') as f:
    try:
        perMinute = int(f.read())
    except Exception:
        print('points-watchtime ratio not found (unable to calculate data-losses)')
        perMinute = None

with open(filename, encoding='utf8') as f:
    data = f.read()

with open('SE_userid.txt', encoding='utf8') as f:
    SE_userid = f.read()

alltime = leaderboardData(SE_userid)
watchtimeData = {}
pointsData = {}
usernameData = set()

soup = BeautifulSoup(data, features="lxml")
html = soup.findAll('div', {'class': 'message'})

for subhtml in html:
    sender = subhtml.find('span', {'class': 'message-author__display-name'}).text
    if sender.lower() != 'streamelements':
        continue
    msg = subhtml.text.split(f'{sender}:', 1)[1].strip().rstrip()

    msg = re.sub(r'[\s\n]+', ' ', msg)
    
    re_data = re.match(r'([^ ]+) has spent (.+?) watching', msg)
    if re_data != None:
        user = re_data.group(1).lower()
        duration = re_data.group(2).split(' ')
        currentUser = handleWatchtime(user, duration)
        usernameData.add(currentUser[0])
        if not currentUser[0] in watchtimeData:
            watchtimeData[currentUser[0]] = currentUser[1]
            continue
        if watchtimeData[user] < currentUser[1]:
            watchtimeData[user] = currentUser[1]
            continue
    re_data = re.match(r'@[^,]+, ([^ ]+) has (\d+) [^ ]+ and is rank', msg)
    if re_data == None:
        re_data = re.match(r'([^ ]+) [^ ]+ \d+ [^ ]+ in roulette and now has (\d+)', msg)
    if re_data != None:
        user = re_data.group(1).lower()
        usernameData.add(user)
        points = int(re_data.group(2))
        if not user in pointsData:
            pointsData[user] = {}
            if user in alltime and alltime[user] > points:
                pointsData[user]['max'] = alltime[user]
            else:
                pointsData[user]['max'] = points
            pointsData[user]['current'] = points
            continue
        pointsData[user]['current'] = points
        if pointsData[user]['max'] < points:
            pointsData[user]['max'] = points
            continue

with open('data-watchtime.json', 'w') as f:
    json.dump(watchtimeData, f)

with open('data-points.json', 'w') as f:
    json.dump(pointsData, f)

csvData = csvParser(usernameData, watchtimeData, pointsData)

with open('result-only-watchtime.csv', 'w') as f:
    f.write(csvData[0])

with open('result-complete.csv', 'w') as f:
    f.write(csvData[1])

with open('result-only-points.csv', 'w') as f:
    f.write(csvData[2])