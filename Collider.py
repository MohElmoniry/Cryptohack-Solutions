from pwn import *
import json
msg1 = open('message1.py', 'rb').read()
msg2 = open('message2.bin','rb').read()
r = remote("socket.cryptohack.org", 13389)

payload1 = {
	'document' : msg1.hex()
}

payload2 = {
	'document' : msg2.hex()
}
payload1 = json.dumps(payload1).encode()
payload2 = json.dumps(payload2).encode()

r.sendlineafter(b'store\n', payload1)
r.sendlineafter(b'\n', payload2)
print(r.recvline())
r.close()