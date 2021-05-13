import smtplib
import time
server = smtplib.SMTP('smtp.gmail.com',587)
server.ehlo()
server.starttls()
server.ehlo()
server.login("gastonkitambala@gmail.com", "kitambalas1998")
msg = ("hello" + time.ctime())
print(msg)
server.sendmail("gastonkitambala@gmail.com", "gastonkitambala@yahoo.com",msg)
print("Messsage sent")
server.quit()
