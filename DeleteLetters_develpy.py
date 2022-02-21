from logging import shutdown
from imapclient import IMAPClient
import ssl,time
from threading import Thread
import os


start_time = time.time()
   # открываем файл,убираем пустые строки
with open('del_emails_from.txt', "r+", encoding='utf-8') as f:
    lines = f.readlines()
    f.seek(0)
    f.writelines(line for line in lines if line.strip())
    f.truncate()

   # делаем подсчет строк на выход
with open('del_emails_from.txt',"r") as f:
    line_count2 = 0
    for line in f:
        line_count2 += 1
   ####################################################################################

def main():
   emptyfiletest2 = os.stat('Good.txt')
   if emptyfiletest2.st_size != 0:
      work_with_imap()
      
   else:
      print("File 'Good.txt' is empty")
                            
def size_file():
   emptyfiletest2 = os.stat('Good.txt')
   if emptyfiletest2.st_size != 0:
      with open("Good.txt", "r+", encoding='utf-8') as f: #чистка пустых строк
          lines = f.readlines()
          f.seek(0)
          f.writelines(line for line in lines if line.strip())
          f.truncate()
   else:
      print("File 'Good.txt' is empty")
   return emptyfiletest2                  

def readline_write():
   file_size = size_file()
   if file_size.st_size != 0:
      with open('Good.txt',"r") as f:    
            good_list = f.read().splitlines()
            if '|' in good_list[-1]: #чистка если закинули Good с AIOC
                  good_list[-1] = (good_list[-1]).replace('|',' ')
                  good_list[-1] = (good_list[-1])[:-4]
                  email = good_list[-1].split(':')[0]
                  email = email.replace(' ','')
                  password = good_list[-1].split(':')[1]
                  password = password.replace(' ','')
            else: # Если просто чистый email:pass
               email = good_list[-1].split(':')[0]
               email = email.replace(' ','')
               password = good_list[-1].split(':')[1]
               password = password.replace(' ','')
               domain = email.split("@")[1]
         
            with open('Good.txt',"w+") as f:
               for i in range(len(good_list)-1):
                  f.writelines(good_list[i])
                  f.writelines("\n")
            time.sleep(0.1)
   while file_size.st_size != 0:                 
      return email,password,domain                                            
                                    
def work_with_imap():
   emptyfiletest2 = os.stat('Good.txt')
   if emptyfiletest2.st_size != 0:
      email_imap,password_imap,domain_imap = readline_write()
   with open('del_emails_from.txt',"r") as f:
         good_list_senders = f.read().splitlines()
   with open('imap.list',"r") as fa:
               imaplines = fa.readlines()  
   lines_imap = len(imaplines)     
   d = 0
   Login = False
   while Login == False:
      for d in range(lines_imap):
         if d == lines_imap-1:
            Login = True
         try:
            if domain_imap in imaplines[d]:
               f = imaplines[d].split("|")
               del f[0]
               del f[-1]
               if f[0] == domain_imap:
                  if len(f) == 3:  
                     imap = f[1]   
                     port = f[2]
                     if port != "143":
                        try:                                               
                              with IMAPClient(imap,port=port) as server:
                                 responce_server = server.login(email_imap, password_imap)                     
                                 if "Logged in" in responce_server.decode('utf-8'):
                                    print("\n"+"Connecting...")
                                    server.select_folder("INBOX", readonly=False)
                                    t = 0
                                    for t in range(line_count2): 
                                       print("\nУдаляю письма... ")
                                       print("Отправитель: ", f"{good_list_senders[t]} ")
                                       list_mails = server.search(criteria = 'FROM ' f"{good_list_senders[t]}")
                                       messages_flagged = server.add_flags(messages = list_mails,flags=br'\Deleted',silent=False)
                                       server.delete_messages(messages=messages_flagged,silent=True)
                                       shutdown()                 
                                       print("Почта: ",email_imap)
                                       print("Уебали все письма, OK!")                              
                                    return True
                                    
                                 else: continue
                        except: print("Retrying...")
                        continue
                     else:
                        try:
                           ssl_context = ssl.create_default_context()
                           ssl_context.check_hostname = False
                           ssl_context.verify_mode = ssl.CERT_NONE
                           try:                          
                              with IMAPClient(imap,port=port,ssl_context=ssl_context) as server:
                                 responce_server = server.login(email_imap, password_imap)
                                 if "Logged in" in responce_server.decode('utf-8'):
                                    print("\n"+"Connecting...")
                                    t = 0
                                    for t in range(line_count2): 
                                       print("\nУдаляю письма... ")
                                       print("Отправитель: ", f"{good_list_senders[t]} ")
                                       list_mails = server.search(criteria = 'FROM ' f"{good_list_senders[t]}")
                                       messages_flagged = server.add_flags(messages = list_mails,flags=br'\Deleted',silent=False)
                                       server.delete_messages(messages=messages_flagged,silent=True)
                                       shutdown()                 
                                       print("Почта: ",email_imap)
                                       print("Уебали все письма, OK!")                              
                                    return True
                                 else: continue
                           except:
                              with IMAPClient(imap,port=port,ssl=False) as server:
                                 responce_server = server.login(email_imap, password_imap)                               
                                 server.select_folder("INBOX", readonly=False)                                 
                                 if "Logged in" or "login successful" in responce_server.decode('utf-8'):
                                    print("\n"+"Connecting...")
                                    t = 0
                                    for t in range(line_count2): 
                                       print("\nУдаляю письма... ")
                                       print("Отправитель: ", f"{good_list_senders[t]} ")
                                       list_mails = server.search(criteria = 'FROM ' f"{good_list_senders[t]}")
                                       messages_flagged = server.add_flags(messages = list_mails,flags=br'\Deleted',silent=False)
                                       server.delete_messages(messages=messages_flagged,silent=True)
                                       shutdown()                 
                                       print("Почта: ",email_imap)
                                       print("Уебали все письма, OK!")
                                    return True
                                 else: continue
                        except:
                           print("Retrying...")
                           continue                     
                  else:                        
                     if len(f) == 4:
                        imap = f[1]   
                        port = f[2]
                        if f[3] == "true":
                           try:
                           
                              with IMAPClient(imap,port=port) as server:
                                 responce_server = server.login(email_imap, password_imap)                           
   
                                 if "Logged in" in responce_server.decode('utf-8'):
                                    print("\n"+"Connecting...")
                                    server.select_folder("INBOX", readonly=False)
                                    t = 0
                                    for t in range(line_count2): 
                                       print("\nУдаляю письма... ")
                                       print("Отправитель: ", f"{good_list_senders[t]} ")
                                       list_mails = server.search(criteria = 'FROM ' f"{good_list_senders[t]}")
                                       messages_flagged = server.add_flags(messages = list_mails,flags=br'\Deleted',silent=False)
                                       server.delete_messages(messages=messages_flagged,silent=True)
                                       shutdown()                 
                                       print("Почта: ",email_imap)
                                       print("Уебали все письма, OK!")
                                    return True
                           except:
                              print("Retrying...")
                              continue
                        else:
                           try:
                              ssl_context = ssl.create_default_context()
                              ssl_context.check_hostname = False
                              ssl_context.verify_mode = ssl.CERT_NONE
   
                              try:                          
                                 with IMAPClient(imap,port=port,ssl_context=ssl_context) as server:
                                    responce_server = server.login(email_imap, password_imap)
                                    if "Logged in" in responce_server.decode('utf-8'):
                                       print("\n"+"Connecting...")
                                       server.select_folder("INBOX", readonly=False)
                                       t = 0
                                       for t in range(line_count2): 
                                          print("\nУдаляю письма... ")
                                          print("Отправитель: ", f"{good_list_senders[t]} ")
                                          list_mails = server.search(criteria = 'FROM ' f"{good_list_senders[t]}")
                                          messages_flagged = server.add_flags(messages = list_mails,flags=br'\Deleted',silent=False)
                                          server.delete_messages(messages=messages_flagged,silent=True)
                                          shutdown()                 
                                          print("Почта: ",email_imap)
                                          print("Уебали все письма, OK!")
                                       return True
                                    else:continue
                              except:
                                 with IMAPClient(imap,port=port,ssl=False) as server:
                                    responce_server = server.login(email_imap, password_imap)   
                                    if "Logged in" in responce_server.decode('utf-8'):
                                       server.select_folder("INBOX", readonly=False)
                                       t = 0
                                       for t in range(line_count2): 
                                          print("\nУдаляю письма... ")
                                          print("Отправитель: ", f"{good_list_senders[t]} ")
                                          list_mails = server.search(criteria = 'FROM ' f"{good_list_senders[t]}")
                                          messages_flagged = server.add_flags(messages = list_mails,flags=br'\Deleted',silent=False)
                                          server.delete_messages(messages=messages_flagged,silent=True)
                                          shutdown()                 
                                          print("Почта: ",email_imap)
                                          print("Уебали все письма, OK!")
                                       return True
                                    else: continue
                           except:
                              print("Retrying...")
                              continue            
         except: pass             
   else: 
      pass

while size_file().st_size != 0:
   i = 1     
   for i in range(300):
         i = Thread(target=work_with_imap)
         i.start()
         time.sleep(0.1)
   time.sleep(0.1)
else: 
   print("--- %s seconds ---" % (time.time() - start_time))

input("\n**ver 1.2*******Developed by********** PRESS ENTER FOR RESTART ***********@develpy*******")