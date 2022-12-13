## THIS MAY NOT WORK, THE KID IS SCREAMING AT ME!!!

import praw
import sys
import os
import re
import time
import random

# TODO: Add "good/bad bot" comment replies
#   Add at least 100 quotes/phrases in txt
#   Create logic to reply to "breach" and "hacker" respectively
#   Add stat counter

required = ["posts.log", "botComments.log", "hacker_phrase.txt"]


class bot:

    def __init__(self):
        with open("hacker_phrase.txt", "r") as f:
            hacker_phrase = f.read()
            hacker_phrase = hacker_phrase.split("\n")
            hacker_phrase = list(filter(None, hacker_phrase))
        self.phrase = hacker_phrase
        self.quote = random.choice(hacker_phrase)
        self.footer = "\n\n*^(Beep Boop Wee Doo! I am a bot and this action was performed automatically.)*"
        self.tempphrase = "\n*^(I am currently under development and learning to not be annoying. My inbox will be temporarily " \
                     "monitored.)*"
        with open("posts.log", "r") as f:
            posts = f.read()
            posts = posts.split("\n")
            posts = list(filter(None, posts))
        self.posts = posts
        with open("botComments.log", "r") as f:
            botComments = f.read()
            botComments = botComments.split("\n")
            botComments = list(filter(None, botComments))
        self.botComments = botComments

    @staticmethod
    def instantiate():
        # create reddit instance
        print("\nAuthenticating...")
        r = praw.Reddit('imin_bot')
        print("Success!!\n")
        return r

    def vote(self, r):
        bot.__init__(self)
        good_bot = []
        bad_bot = []
        votes = []
        print("Vote monitoring has started...")
        while True:
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

    @staticmethod
    def fileCheck():
        print("Verifying all required files are present.")
        for file in required:
            if not os.path.isfile(file) and file != "hacker_phrase.txt":
                newFile = file.rsplit('.', 1)[0]
                globals()[newFile] = []
                print(newFile + " created.")
            elif not os.path.isfile(file) and file == "hacker_phrase.txt":
                sys.exit("File \"hacker_phrase.txt\" is missing. \nThis file is required for bot to function."
                         "\nExiting...")
            else:
                with open(file, "r") as f:
                    newVar = file.rsplit('.', 1)[0]
                    globals()[newVar] = f.read()
                    globals()[newVar] = globals()[newVar].split("\n")
                    globals()[newVar] = list(filter(None, globals()[newVar]))
                print(newVar, "file is here.")

    def calling(self, r):
        bot.__init__(self)
        new_mentions = []
        call_log = []
        unread = []
        print("Inbox monitoring has started...")
        while True:
            for mention in r.inbox.mentions():
                if mention.new:
                    new_mentions.append(mention)
                    call_log.append(mention.id)
                    with open("calls.log", "w") as f:
                        for mention_id in call_log:
                            f.write(mention_id + "\n")
                    mention.reply(body=self.quote + self.footer + self.tempphrase)
                    print("Called by " + mention.author.name + ". -- I have replied.")
                    r.inbox.mark_read(new_mentions)

    def postReply(self, r):
        bot.__init__(self)
        redditBot = r.redditor("imin_bot")
        autoMod = "AutoModerator"
        # subreddit = r.subreddit("masterhacker+cybersecurity+hacking+Hacking_Tutorials")
        # subreddit = r.subreddit("all")  ## THIS APPARENTLY RESULTED IN A SHADOWBAN
        subreddit = r.subreddit("bottest+test")
        print("Post monitoring has started...")
        while True:
            for submission in subreddit.stream.submissions():
                if re.search(r"\bhacker\b | \bhackers\b", submission.title, re.IGNORECASE):
                    if submission.id not in self.posts and submission.author not in [redditBot, autoMod]:
                        # botComment = submission.reply(body=reply_quote + footer + tempphrase)
                        botComment = submission.reply(body=self.quote + self.footer + self.tempphrase)
                        print("Bot replied to " + submission.id + " written by " + submission.author.name)
                        self.posts.append(submission.id)
                        with open("posts.log", "w") as f:
                            for post_id in self.posts:
                                f.write(post_id + "\n")
                        self.botComments.append(botComment.id)
                        with open("botComments.log", "w") as f:
                            for comment_id in self.botComments:
                                f.write(comment_id + "\n")
                # break
