import praw
import sys
import os
import re
import time
import random
from threading import Thread

# TODO: Add "good/bad bot" comment replies
#   Add at least 100 quotes/phrases in txt
#   Create logic to reply to "breach" and "hacker" respectively
#   Add ability to be called by user
#   Create bot class and refactor
#   Add stat counter


required = ["posts.log", "botComments.log", "hacker_phrase.txt"]


def instantiate():
    # create reddit instance
    print("Authenticating...")
    r = praw.Reddit('imin_bot')
    print("Success!!\n")
    return r


def vote():
    good_bot = []
    bad_bot = []
    votes = []
    for reply in r.inbox.unread():
        if re.search(r"\bgood bot\b", reply.body, re.IGNORECASE) and reply.was_comment:
            good_bot.append(reply.id)
            votes.append(reply)
            print(reply.author.name + " voted imin_bot as a GOOD BOT.")
            with open("goodBot.log", "w") as f:
                for reply_id in good_bot:
                    f.write(reply_id + "\n")
        elif re.search(r"\bbad bot\b", reply.body, re.IGNORECASE):
            bad_bot.append(reply.id)
            votes.append(reply)
            print(reply.author.name + " voted imin_bot as a BAD BOT.")
            with open("badBot.log", "w") as f:
                for reply_id in bad_bot:
                    f.write(reply_id + "\n")
        r.inbox.mark_read(votes)

def fileCheck():
    for file in required:
        if not os.path.isfile(file) and file != "hacker_phrase.txt":
            newFile = file.rsplit('.', 1)[0]
            globals()[newFile] = []
            print(newFile + " created.")
        elif not os.path.isfile(file) and file == "hacker_phrase.txt":
            sys.exit("File \"hacker_phrase.txt\" is missing. \nThis file is required for bot to function.\nExiting...")
        else:
            with open(file, "r") as f:
                newVar = file.rsplit('.', 1)[0]
                globals()[newVar] = f.read()
                globals()[newVar] = globals()[newVar].split("\n")
                globals()[newVar] = list(filter(None, globals()[newVar]))


def calling():
     new_mentions = []
     call_log = []
     unread = []
     for mention in r.inbox.stream():
        if mention.id in [r.inbox.unread(), r.inbox.mentions()]:
                new_mentions.append(mention)
                call_log.append(mention.id)
                with open("calls.log", "w") as f:
                    for mention_id in call_log:
                        f.write(mention_id + "\n")
                mention.reply(body=reply_quote + footer + tempphrase)
                print("Called by " + mention.author.name + ". -- I have replied.")
                r.inbox.mark_read(new_mentions)


def postReply():
    redditBot = r.redditor("imin_bot")
    autoMod = "AutoModerator"
    # subreddit = r.subreddit("masterhacker+cybersecurity+hacking+Hacking_Tutorials")
    # subreddit = r.subreddit("all")  ## THIS APPARENTLY RESULTED IN A SHADOWBAN
    subreddit = r.subreddit("bottest+test")

    for submission in subreddit.stream.submissions():
        if re.search(r"\bhacker\b | \bhackers\b", submission.title, re.IGNORECASE):
            if submission.id not in posts and submission.author not in [redditBot, autoMod]:
                botComment = submission.reply(body=reply_quote + footer + tempphrase)
                print("Bot replied to " + submission.id + " written by " + submission.author.name)
                posts.append(submission.id)
                with open("posts.log", "w") as f:
                    for post_id in posts:
                        f.write(post_id + "\n")
                botComments.append(botComment.id)
                with open("botComments.log", "w") as f:
                    for comment_id in botComments:
                        f.write(comment_id + "\n")
        # break


def main():
    # Define necessary variables -- TODO: Find a better way to do this
    global r
    global reply_quote
    global footer
    global tempphrase
    # Check for existence of logs and response list
    fileCheck()

    reply_quote = random.choice(hacker_phrase)
    footer = "\n\n*^(Beep Boop Wee Doo! I am a bot and this action was performed automatically.)*"
    tempphrase = "\n*^(I am currently under development and learning to not be annoying. My inbox will be temporarily " \
                 "monitored.)*"

    # Start an instance and call threaded functions
    r = instantiate()
    post.start()
    call.start()
    vote.start()

'''
    with open("posts.log", "r") as f:
        posts = f.read()
        posts = posts.split("\n")
        posts = list(filter(None, posts))

    with open("hacker_phrase.txt", "r") as f:
        hacker_phrase = f.read()
        hacker_phrase = hacker_phrase.split("\n")
        hacker_phrase = list(filter(None, hacker_phrase))
'''

if __name__ == "__main__":
    post = Thread(target=postReply)
    call = Thread(target=calling)
    vote = Thread(target=vote)
    main()
