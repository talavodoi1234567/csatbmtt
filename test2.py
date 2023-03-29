import chardet

bytes_data = b'\xa9\xe7\x1d\xd3'
str_data = bytes_data.decode('UTF-16')
print(bytes_data.decode('UTF-16').encode('UTF-16'), str_data)
