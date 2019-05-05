from PIL import Image

image = Image.open("test.jpg")
# L = list(image.getdata())
# N = 20
# for i in range(N):
# 		print("Origin",L[i])
# print("-"*20)
#print(list(image.getdata()))

def even_pixel_image(image):
	pixels = list(image.getdata()) #pixels的长度为图像像素点数量
	#print(len(pixels),pixels[299])
	even_pixels = [(r>>1<<1,g>>1<<1,b>>1<<1) for r,g,b in pixels]
	#print(image.size,image.mode,image)
	# for i in range(N):
	# 	print("Even image",even_pixels[i])
	# print("-"*20)

	even_image = Image.new(image.mode,image.size)
	even_image.putdata(even_pixels)	
	return even_image

def encrypt(image,data,encoding):
	offset = 1
	even_image = even_pixel_image(image)
	carrier_pixels = list(even_image.getdata())
	byte_str = compose_byte_str(data,encoding)
	bytes_to_encrypt = len(byte_str)/8  
	allowed = len(carrier_pixels)*2//8 #保证所有字节都能被加密,乘3表示每个像素点都可存储2bit数据
 
	if(bytes_to_encrypt > allowed):
		print("Too more bits to encrypt! ")
		print(allowed,"Bytes allowed,",bytes_to_encrypt,"Bytes given")

	for index,(r,g,b) in enumerate(carrier_pixels):
		if (index+offset)*2>bytes_to_encrypt*8:
			break
		carrier_pixels[index] = (r,g+int(byte_str[index*2+0]),b+int(byte_str[index*2+1]))
	# for i in range(N):
	# 	print("Add info",carrier_pixels[i])
	# print("-"*20)	
	#print(carrier_pixels)
	encryptedImage = Image.new(even_image.mode, even_image.size)  # 创建新图片以存放编码后的像素
	#carrier_pixels = [(1,2,3),(4,5,6),(7,8,9),(1,2,3),(1,2,3),(4,5,6),(7,8,9)]
	encryptedImage.putdata(carrier_pixels)  # 添加编码后的数据
	return encryptedImage
	

def compose_byte_str(contents,encoding):
	byte_str = ['']
	count = 0
	for b in bytearray(contents,encoding):
		bin_code = bin(b).replace("0b",'')#去掉二进制开头的0b
		byte_padding = '0'*(8-len(bin_code)) #不足8位的左侧补0对齐
		byte = byte_padding+bin_code #构造一个字节
		byte_str.append(byte) #形成一个字符串的二进制编码序列
		count+=1
	payload = bin(count*8).replace("0b",'')
	payload_padding = '0'*(32-len(payload))
	byte_str[0] = payload_padding+payload
	return "".join(byte_str)

def find_delimiter(binary_str):
	index     = 0
	delimiter = [0]
	while  index < len(binary_str):
		bytes_cnt  = binary_str[index:].index('0')
		length     = bytes_cnt*8 if bytes_cnt else 8
		index      = index+length
		delimiter.append(index)
	return delimiter

def get_data(binary_str,start,stop):
	data = binary_str[start:stop]
	bytes_cnt = len(data)//8
	#print(bytes_cnt,"\n")
	count = 0
	decode_char = []
	while count<bytes_cnt:
		if count==0:
			if bytes_cnt==1:
				extracted = data[8*count+1:8*(count+1)]
			else:
				extracted = data[8*count+bytes_cnt+1:8*(count+1)]	
		else:
			extracted = data[8*count+2:8*(count+1)]
		decode_char.append(extracted)
		count += 1
	return "".join(decode_char)
	#return chr(int("".join(decode_char),2))

def decodeImage(image):
	pixels = list(image.getdata())  # 获得像素列表
	print("-"*20)
	# for i in range(N):
	# 	print("Read enc",pixels[i])
	offset = 16
	payload = []
	for index,(r,g,b) in enumerate(pixels):
		if index+1>offset:
			break
		payload.append(str(int(g>>1<<1!=g)))
		payload.append(str(int(b>>1<<1!=b)))
	bits_to_exract = int(eval("0b"+"".join(payload)))
	print(bits_to_exract)

	decode_str = []
	for index,(r,g,b) in enumerate(pixels):
		if index<offset:
			continue
		if index+1>offset+bits_to_exract/2:
			break
		print(index)
		decode_str.append(str(int(g>>1<<1!=g)))
		decode_str.append(str(int(b>>1<<1!=b)))
	binary_str = "".join(decode_str)
	print("".join(decode_str))

	delimiter = find_delimiter(binary_str)	
	for i in range(len(delimiter)-1):
		start = delimiter[i]
		stop  = delimiter[i+1]
		print(start,stop)
		decode_char = get_data(binary_str,start,stop)
		print(decode_char)
		decode_str.append(chr(int(decode_char,2)))
	print("".join(decode_str))
	
	binary = ''.join([str(int(g>>1<<1!=g))+str(int(b>>1<<1!=b)) for (r,g,b) in pixels])  # 提取图片中所有最低有效位中的数据
	
	# #找到数据截止处的索引
	# locationDoubleNull = binary.find('0000000000000000')
	# endIndex = locationDoubleNull+(8-(locationDoubleNull % 8)) if locationDoubleNull%8 != 0 else locationDoubleNull
	# print(binary[0:endIndex])
	# data = binaryToString(binary[0:endIndex])
	# return data


# even_pixel_image(image)
# im = Image.open("even.png")
# Even = list(im.getdata())
# for i in range(N):
# 	print("Read even",Even[i])
#print(list(image.getdata()))

encrypt(image,"粮台出事了，风紧扯呼","utf-8").save('enc.png')
decodeImage(Image.open("enc.png"))


# bs = compose_byte_str("Hello生死狙击是",'utf-8') 
# print(bs)
# limit = len(bs)
#print(decodeImage(image))
