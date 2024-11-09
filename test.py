import time
run = True
while run:
    try:
        print("hi")
        time.sleep(1)
    except KeyboardInterrupt:
        print("stop")
        run = False
