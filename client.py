import socket
import threading
import time

KEY = 7934 # ключ для шифрования данных

shutdown = False
join = False



# принимаем данные от другого пользователя 
def receving (name, sock):
	while not shutdown:
		try:
			while True:
				data, addr = sock.recvfrom(1024)
				#print(data.decode("utf-8"))

				# Begin
				decrypt = ""; k = False
				for i in data.decode("utf-8"):
					if i == ":":
						k = True
						decrypt += i
					elif k == False or i == " ":
						decrypt += i
					else:
						decrypt += chr(ord(i)^KEY)
				print(decrypt)
				# End

				time.sleep(0.2)
		except:
			pass


HOST = socket.gethostbyname("")
PORT = 0

server = (HOST, 9090)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

s.setblocking(0) # Блокировку с recv поможет снять функция setblocking(0). 
# Тогда в случае отсутствия данных функция не будет ждать, а выкинет исключение socket.error,
# которое можно будет поймать в блоке try-except

# ввод имени пользователя чата
nickname = input("Your name: ")


r = threading.Thread(target = receving, args = ("RecvThread", s))
r.start()

while shutdown == False:
	if join == False:
		s.sendto(("--"+nickname + " ==> join chat ").encode("utf-8"),server)
		join = True
	else:
		try:
			message = input()

			# шифрование сообщений
			crypt_m = ""
			for i in message:
				crypt_m += chr(ord(i)^KEY)
			message = crypt_m
			# -------------

			if message != "":
				s.sendto(("--"+nickname + " : " + message).encode("utf-8"), server)
			
			time.sleep(0.2)
		except:
			s.sendto(("--"+nickname + " <== left chat ").encode("utf-8"), server)
			shutdown = True

r.join()
s.close()