from Crypto.PublicKey import RSA

f = open('keypair.pem','r')
key = RSA.importKey(f.read())

print(key.d)
