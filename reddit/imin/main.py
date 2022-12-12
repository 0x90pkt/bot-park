import praw
import sys
import os
import re
import time
import random
from threading import Thread
from bot import *


def main():

    # call threaded functions
    post.start()
    call.start()
    vote.start()


if __name__ == "__main__":
    # check for required files
    bot.fileCheck()
    # start instance and setup for running on separate threads
    r = bot.instantiate()
    print("Bot is running...")
    bot = bot()
    post = Thread(bot.postReply(r))
    call = Thread(bot.calling(r))
    vote = Thread(bot.vote(r))
    main()
