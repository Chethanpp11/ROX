# import multiprocessing
# from engine.features import *
# # from engine.command import user_greetings

# # To run Jarvis
# def startJarvis():
#         # Code for process 1
#         print("Process 1 is running.")
#         from main import start
#         start()

# # To run hotword
# def listenHotword():
#         # Code for process 2
#         print("Process 2 is running.")
#         from engine.features import hotword
#         hotword()

# # Start both processes
# if __name__ == '__main__':
#         p1 = multiprocessing.Process(target=startJarvis)
#         p2 = multiprocessing.Process(target=listenHotword)
#         playAssistantSound()
#         p1.start()
#         p2.start()
#         p1.join()
#         if p2.is_alive():
#                 p2.terminate()
#                 p2.join()

#         print("system stop")

import multiprocessing
import time  # Importing time module for delays
from engine.features import *
# from engine.command import user_greetings

# To run Jarvis
def startJarvis():
    # Code for process 1
    print("Process 1 is starting...")
    time.sleep(1)  # Delay for smoother startup
    from main import start
    start()

# To run hotword
def listenHotword():
    # Code for process 2
    print("Process 2 is starting...")
    time.sleep(1)  # Delay to allow process 1 to initialize
    from engine.features import hotword
    hotword()

# Start both processes
if __name__ == '__main__':
        print("Initializing processes...")
        time.sleep(0.5)  # Slight delay before starting processes

        p1 = multiprocessing.Process(target=startJarvis)
        p2 = multiprocessing.Process(target=listenHotword)

        
        time.sleep(0.5)  # Delay after playing sound

        p1.start()
        print("Process 1 started.")
        time.sleep(0.5)  # Allow some time before starting process 2
        
        p2.start()
        print("Process 2 started.")
        playAssistantSound()  # Play assistant sound before starting processes
        p1.join()
        print("Process 1 finished.")
        
        if p2.is_alive():
                print("Terminating process 2...")
                time.sleep(0.5)  # Graceful wait before termination
                p2.terminate()
                p2.join()
                print("Process 2 terminated.")

        print("System stop.")
