import tweepy
import configparser
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import os


# Credentials
apiKey = 'M98TaliIufzswaRsqfzoVlv35'
apiKeySecret = 'IpwkM1hXRf2SMV0xAwAVCsPYbDRVNR3PwS5oAjUixyNMzoF70L'
accessToken = '1495844653525987330-cGvFkLVC61uxSJgFgeSQQAXDlpJ0VU'
accessTokenSecret = 'wM55VSRUGNjSfsZhyprfB0uZR1VHKlVSnwlp5TjHwWc5D'


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
limit = 10000

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
    except:
        print("Something else went wrong")

# Finds Percentages
percentages = []

for i in range(len(data)):
    percent = (data[i]/sum(data)*100)
    percentages.append(round(percent, 2))

# Finds Average
sumForAverage = 0
for i in range(len(data)-2):
    sumForAverage += (i+1)*data[i]

average = sumForAverage/(sum(data)-data[6])
average = round(average,  2)

# Emoji Data Visualization
greenBox = '\U0001F7E9'
yellowBox = '\U0001F7E8'
blackBox = "\U00002B1B"

emojiAttempt = []
maxPercent = max(percentages)
for i in range(len(percentages)):
    emojis = ''
    ratio = percentages[i]/maxPercent
    ratioCheck = 1/6
    bigger = ratio/ratioCheck
    numGreen = int(bigger)
    emojis += greenBox*numGreen
    if bigger-numGreen >= 0.5 or numGreen == 0:
        emojis += yellowBox
    while len(emojis) < 6:
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
plt.savefig('wordle' + wordleNum + '.jpg')


# Creates and sends out tweet
path = os.getcwd()
tweetSend = f"Wordle {wordleNum} Statistics\n\nAttempt 1: {emojiAttempt[0]}{percentages[0]}%\nAttempt 2: {emojiAttempt[1]}{percentages[1]}%\nAttempt 3: {emojiAttempt[2]}{percentages[2]}%\nAttempt 4: {emojiAttempt[3]}{percentages[3]}%\nAttempt 5: {emojiAttempt[4]}{percentages[4]}%\nAttempt 6: {emojiAttempt[5]}{percentages[5]}%\nFailed X: {emojiAttempt[6]}{percentages[6]}%\nThe average attempts for success was {average}.\n"
imagePath = 'wordle' + wordleNum + '.jpg'
print(tweetSend)
mediaImage = api.media_upload(
    filename='wordle' + wordleNum + '.jpg')
mediaImages = [mediaImage.media_id_string]
api.update_status(status=tweetSend, media_ids=mediaImages)
