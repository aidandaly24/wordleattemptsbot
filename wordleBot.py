import tweepy
import configparser
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import os
from time import sleep


# Credentials
apiKey = API_KEY
apiKeySecret = API_KEY_SECRET
accessToken = ACCESS_TOKEN
accessTokenSecret = ACCESS_TOKEN_SECRET


# Authentification
auth = tweepy.OAuthHandler(apiKey, apiKeySecret)
auth.set_access_token(accessToken, accessTokenSecret)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# Gets date and finds Wordle #
currentTime = datetime.datetime.now()
day247 = datetime.date(2022, 2, 21)
dayToday = datetime.date(currentTime.year, currentTime.month, currentTime.day)
delta = (dayToday - day247).days
wordleNum = str(247 + delta)


# Seaerch Tweets
keyWord = 'Wordle ' + wordleNum + '-filter:retweets'
limit = 17000
tweets = tweepy.Cursor(api.search_tweets, q=keyWord,
                       count=100, tweet_mode='extended').items(limit)

tweetList = []

for tweet in tweets:
    tweetList.append(tweet.full_text)


# Finds Data
data = [0, 0, 0, 0, 0, 0, 0]
print(data)
print(sum(data))

for i in range(len(tweetList)):
    tweetCurr = tweetList[i]

    try:
        wordleIndex = tweetCurr.index('/6')
        triesIndex = wordleIndex-1
        tries = tweetCurr[triesIndex]
        if tries == '1':
            data[0] += 1
        elif tries == '2':
            data[1] += 1
        elif tries == '3':
            data[2] += 1
        elif tries == '4':
            data[3] += 1
        elif tries == '5':
            data[4] += 1
        elif tries == '6':
            data[5] += 1
        else:
            data[6] += 1
    except ValueError:
        print("Variable x is not defined")
        continue
    except:
        print("Something else went wrong")

# Finds Data Size
dataSize = sum(data)

# Finds Percentages
percentages = []

for i in range(len(data)):
    percent = (data[i]/sum(data)*100)
    percentages.append(round(percent, 1))

# Adds Data and Percentages to file
hour = (currentTime.hour)
time = "12PM"
f = open("/Users/aidandaly/Desktop/PersonalCode/TwitterBot/data.txt", "a")
dataString = f"\n{wordleNum} Data {time}: "
f.write(dataString)
for i in range(len(data)):
    f.write(str(data[i]) + " ")
percentagesString = f"\n{wordleNum} Percentages {time}: "
f.write(percentagesString)
for i in range(len(percentages)):
    f.write(str(percentages[i]) + " ")

# Finds Average
sumForAverage = 0
for i in range(len(data)-1):
    sumForAverage += (i+1)*data[i]

average = sumForAverage/(sum(data)-data[6])
average = round(average, 1)

# Emoji Data Visualization
greenBox = '\U0001F7E9'
yellowBox = '\U0001F7E8'
blackBox = "\U00002B1B"

emojiAttempt = []
maxPercent = max(percentages)
for i in range(len(percentages)):
    emojis = ''
    ratio = percentages[i]/maxPercent
    ratioCheck = 1/5
    bigger = ratio/ratioCheck
    numGreen = int(bigger)
    emojis += greenBox*numGreen
    if bigger-numGreen >= 0.5 or numGreen == 0:
        emojis += yellowBox
    while len(emojis) < 5:
        emojis += blackBox
    emojiAttempt.append(emojis)


# Plot Data Visualisation
matplotlib.style.use('fivethirtyeight')
sns.set_style("dark")
plotdata = pd.DataFrame(
    {"Percentages": percentages},
    index=["1", "2", "3", "4", "5", "6", "X"])
plotdata.plot(kind="bar")
plt.xticks(horizontalalignment="center")
plt.title("Wordle Number Attempt Percentages")
plt.xlabel("Attempt Number")
plt.ylabel("Percent")
plt.savefig(
    '/Users/aidandaly/Desktop/PersonalCode/TwitterBot/StatsPics/wordle' + wordleNum + '.jpg')


# Creates and sends out tweet
path = os.getcwd()
tweetSend = f"Wordle {wordleNum} X Stats ({time})\n\n{emojiAttempt[0]}Attempt 1: {percentages[0]}%\n{emojiAttempt[1]}Attempt 2: {percentages[1]}%\n{emojiAttempt[2]}Attempt 3: {percentages[2]}%\n{emojiAttempt[3]}Attempt 4: {percentages[3]}%\n{emojiAttempt[4]}Attempt 5: {percentages[4]}%\n{emojiAttempt[5]}Attempt 6: {percentages[5]}%\n{emojiAttempt[6]}Failed X: {percentages[6]}%\nAverage attempts: {average}\nData Size: {dataSize} Tweets"
imagePath = 'wordle' + wordleNum + '.jpg'
print(tweetSend)
mediaImage = api.media_upload(
    filename='/Users/aidandaly/Desktop/PersonalCode/TwitterBot/StatsPics/wordle' + wordleNum + '.jpg')
mediaImages = [mediaImage.media_id_string]
api.update_status(status=tweetSend, media_ids=mediaImages)
