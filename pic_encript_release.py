"""
将一幅图片所有像素点的RGB值变成偶数，则最低位必为0，然后把
需要加密的信息转换为二进制编码，并将一串二进制编码加载到图片
像素点的G通道和B通道上，解码时先从G通道和B通道上获取二进制
编码，然后根据二进制编码解码出信息。
"""
from PIL import Image
image = Image.open("test.jpg")

def even_pixel_image(image):
	'''使所有像素点中的RGB值变为偶数'''
	pixels = list(image.getdata()) #pixels的长度为图像像素点数量
	even_pixels = [(r>>1<<1,g>>1<<1,b>>1<<1) for r,g,b in pixels]
	even_image = Image.new(image.mode,image.size)
	even_image.putdata(even_pixels)	
	return even_image

def encrypt(image,data,encoding='utf-8'):
	'''用于向图像中写入信息'''
	offset = 1
	#将偶数像素点读入并转化为列表以供加载信息
	even_image = even_pixel_image(image)
	carrier_pixels = list(even_image.getdata())

	byte_str = compose_byte_str(data,encoding)
	bytes_to_encrypt = len(byte_str)/8  
	allowed = len(carrier_pixels)*2//8 #保证所有字节都能被加密,乘2表示每个像素点都可存储2bit数据
 
	if(bytes_to_encrypt > allowed):
		print("Too more bits to encrypt! ")
		print(allowed,"Bytes allowed,",bytes_to_encrypt,"Bytes given")

	for index,(r,g,b) in enumerate(carrier_pixels):
		if (index+offset)*2>bytes_to_encrypt*8:
			break
		carrier_pixels[index] = (r,g+int(byte_str[index*2+0]),b+int(byte_str[index*2+1]))
	encryptedImage = Image.new(even_image.mode, even_image.size)  # 创建新图片以存放编码后的像素
	encryptedImage.putdata(carrier_pixels)  # 添加编码后的数据
	return encryptedImage
	

def compose_byte_str(contents,encoding):
	'''将明文字符串换为二进制编码串，并在串头加入长度信息'''
	count = 0
	byte_str = [''] #存储二进制编码串，预留位置0保存编码串长度值(二进制)
	for b in bytearray(contents,encoding):
		bin_code = bin(b).replace("0b",'')   #去掉二进制开头的0b
		byte_padding = '0'*(8-len(bin_code)) #不足8位的左侧补0对齐
		byte = byte_padding+bin_code         #构造一个字节
		byte_str.append(byte) #形成一个字符串的二进制编码序列
		count+=1
	#二进制编码串的长度的二进制值使用32bit保存，即int型
	payload = bin(count*8).replace("0b",'')
	payload_padding = '0'*(32-len(payload))
	byte_str[0] = payload_padding+payload
	return "".join(byte_str)


def find_delimiter(binary_str):
	'''解密时，确定各字符对应的utf8二进制编码在编码串的起止位置'''
	index     = 0
	delimiter = [0]
	while  index < len(binary_str):
		bytes_cnt  = binary_str[index:].index('0')
		#utf8使用可变长度编码，因此需界定每个字符在编码串中的起止位置
		length     = bytes_cnt*8 if bytes_cnt else 8
		index      = index+length
		delimiter.append(index)
	return delimiter

def get_data(binary_str,start,stop):
	'''根据各字符对应的utf8二进制编码在编码串的起止位置，提取其编码'''
	data = binary_str[start:stop]
	bytes_cnt = len(data)//8
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

def decodeImage(image):
	pixels = list(image.getdata())  # 获得像素列表
	offset = 16 #前16个像素点保存了32位字符串二进制编码串长度
	
	#获取字符串二进制编码串长度值
	payload = []
	for index,(r,g,b) in enumerate(pixels):
		if index+1>offset:
			break
		payload.append(str(int(g>>1<<1!=g)))
		payload.append(str(int(b>>1<<1!=b)))
	bits_to_exract = int(eval("0b"+"".join(payload))) #二进制转十进制
	print(bits_to_exract,"bits extracted from",bits_to_exract*2,"pixles.\n","-"*20)
	
	#获取字符串的utf8二进制编码串
	binary_str = []
	for index,(r,g,b) in enumerate(pixels):
		if index<offset:
			continue #跳过长度信息
		if index+1>offset+bits_to_exract/2:
			break #设置停止条件，避免因访问所有像素点造成的开销过大
		binary_str.append(str(int(g>>1<<1!=g)))
		binary_str.append(str(int(b>>1<<1!=b)))
	binary_str = "".join(binary_str)
    
	decode_str = []
	delimiter = find_delimiter(binary_str)	
	for i in range(len(delimiter)-1):
		start = delimiter[i]
		stop  = delimiter[i+1]
		decode_char = get_data(binary_str,start,stop)
		#解码utf8二进制编码
		decode_str.append(chr(int(decode_char,2)))
	print("".join(decode_str))

encrypt(image,"Hello，你好！").save('enc.png')
decodeImage(Image.open("enc.png"))
