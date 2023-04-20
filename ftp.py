from ftplib import FTP


with open('FTPTarget.txt', 'r') as st:
   target = st.readline()
   st.close()


ftp = FTP(target)
ftp.login()
print("DIRECTORY CONTENTS: ")
ftp.retrlines('LIST')