
# Python 3 code to demonstrate the 
# working of MD5 (byte - byte)
 
import hashlib
 

input_str = "yzbqklnj"
done = False
n = 1
mask = 0xfffff000000000000000000000000000
while not done:
	n += 1
	hash_str = input_str + str(n)
	result = hashlib.md5(hash_str.encode())
	firstfive = result.hexdigest()[0:5]
	if firstfive == "00000":
		done = True
		print("Part 1:  md5 hash of ", hash_str, " is ", result.hexdigest(), " n = ", n)

done = False
while not done:
	n += 1
	hash_str = input_str + str(n)
	result = hashlib.md5(hash_str.encode())
	firstfive = result.hexdigest()[0:6]
	if firstfive == "000000":
		done = True
		print("Part 2:  md5 hash of ", hash_str, " is ", result.hexdigest(), " n = ", n)
