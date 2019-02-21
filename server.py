import socket
import time


HOST = socket.gethostbyname("") # socket.gethostname() # ав
PORT = 9090 # определяем порт

chat_members = [] # список для подключенных клиентов

# работа сервера
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # определяем UDP и IP сокеты
s.bind((HOST, PORT)) # связываем хост с портом

stop_server = False # переменная для прекращения работы сервера
print("... Server Started ...") # сообщение о готовности работы




while not stop_server:

	try:
		message, client = s.recvfrom(1024) # наименование пользователя и его сообщение

		if client not in chat_members: 
			chat_members.append(client) # добаляем пользователя в список, при его отсутствии в нем

		time_members = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()) # для отображения времени на сервере

		print("["+client[0]+"]=["+str(client[1])+"]=["+time_members+"]/",end="")
		print(message.decode("utf-8"))



		# выполняем проверку для блокирования отправки своего сообщения самому клиенту
		for member in chat_members:
			if client != member:
				s.sendto(message, member)


	except:
		print("\n...Server Stopped...")
		stop_server = True

s.close() # закрываем хост с портом

