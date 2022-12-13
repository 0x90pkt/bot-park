from multiprocessing import Process
from bot import *

# TODO: Add graceful shutdown

if __name__ == "__main__":
    # check for required files
    bot.fileCheck()
    # start instance and setup for running on separate threads
    r = bot.instantiate()
    print("Bot is running...")
    post = Process(target=bot.postReply, args=(bot, r))
    call = Process(target=bot.calling, args=(bot, r))
    vote = Process(target=bot.vote, args=(bot, r))
    print("Processes have been created! \nInitiating processes...\n")
    post.start()
    call.start()
    vote.start()
    time.sleep(0.5)
    print("\n")
