import hashlib
password = "Alex Ford"
hashObj = hashlib.md5()
hashObj.update(password.encode('utf-16'))
print(hashObj.hexdigest())
