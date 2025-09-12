if __name__ == '__main__':
    import time
    from threading import Thread
    from src.draw_formation import END_EVENT, main as drawer_main, get_offsets

    def f():
        t = 0
        while True and not END_EVENT.is_set():
            time.sleep(0.5)
            if t >= 30 and not END_EVENT.is_set():
                print("Main thread ending work")
                END_EVENT.set()
            print(f"[{t}] meow | offsets = {get_offsets()}")
            t += 0.5

    th_f = Thread(target=f)
    th_f.start()

    drawer_main()