from pwn import xor 
import requests 

ciphertext = "9608427a24c18a23003fbe62e6f60f171b8bb41ae480d97ff5476b008e8d04a452311e437f911c333a6343d4a489b3d182"
ciphertext = bytes.fromhex(ciphertext)

iv = ciphertext[:16]
payload = ciphertext[16:]

# flag = "crypto{0fb_15_5ymm37r1c4l_!!!11!}"
flag = ""
plaintext = flag.ljust(len(payload), "=")
target = payload

def encrypt(plaintext, iv): 
    r = requests.get("http://aes.cryptohack.org/symmetry/encrypt/" + plaintext.encode().hex() + "/" + iv.hex())
    return r.text.split(":")[1][1:-3]

for i in range(33):
    print(plaintext)
    for j in range(33, 127): 
        temp = plaintext 
        temp = temp[:i] + chr(j) + temp[i + 1:] 
        temp_c = bytes.fromhex(encrypt(temp, iv))
        print(temp)
        if target[:(i + 1)] == temp_c[:(i + 1)]:
            plaintext = temp 
            break 

print(plaintext)