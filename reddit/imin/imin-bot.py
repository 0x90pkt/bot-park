#!/usr/local/bin/python3

import praw
import os
import re
import time
import random


if not os.path.isfile("posts.log"):
    posts = []
else:
    with open("posts.log", "r") as f:
        posts = f.read()
        posts = posts.split("\n")
        posts = list(filter(None, posts))

with open("hacker_phrase.txt", "r") as f:
    hacker_phrase = f.read()
    hacker_phrase = hacker_phrase.split("\n")
    hacker_phrase = list(filter(None, hacker_phrase))


def instantiate():
    # create reddit instance
    print("Authenticating...")
    r = praw.Reddit('imin_bot')
    print("Success!!\n")
    return r


def main():
    r = instantiate()
    redditBot = r.redditor("imin_bot")
    autoMod = "AutoModerator"
    #subreddit = r.subreddit("masterhacker+cybersecurity+hacking+Hacking_Tutorials")
    subreddit = r.subreddit("all") ## This is only here for mass testing -- Remove when comleted.
    footer = "\n\n*^(Beep Boop Wee Doo! I am a bot and this action was performed automatically.)*"
    tempphrase = "\n*^(I am currently under development and learning to not be annoying. My inbox will be temporarily " \
                 "monitored.)*"

    for submission in subreddit.stream.submissions():
        if re.search(r"\bhacker\b | \bhackers\b", submission.title, re.IGNORECASE):
            if submission.id not in posts and submission.author not in [redditBot, autoMod]:
                reply_quote = random.choice(hacker_phrase)
                submission.reply(body=reply_quote + footer + tempphrase)
                print("Bot replied to " + submission.id + " written by " + submission.author.name)
                posts.append(submission.id)
                with open("posts.log", "w") as f:
                    for post_id in posts:
                        f.write(post_id + "\n")
        # break


if __name__ == "__main__":
    main()
