# from googleapiclient.http import MediaIoBaseDownload
# import io

# def download_file(service, file_id, file_path):
#     request = service.files().get_media(fileId=file_id)
#     fh = io.FileIO(file_path, 'wb')
#     downloader = MediaIoBaseDownload(fh, request)
#     done = False
#     while done is False:
#         status, done = downloader.next_chunk()
#         print("Download %d%%." % int(status.progress() * 100))

# # Example usage
# download_file(service, 'your_file_id_here', 'destination_file_path_here')
# Python program to explain os.makedirs() method 

# importing os module 
import os 

# os.makedirs() method will raise 
# an OSError if the directory 
# to be created already exists 
# But It can be suppressed by 
# setting the value of a parameter 
# exist_ok as True 

# Directory 
directory = "documents"

# Parent Directory path 
parent_dir = "C:/Users/promact.DESKTOP-RHBFB7T/Desktop/Intelligent_Document_Finder"

# Path 
path = os.path.join(parent_dir, directory) 

# Create the directory 
# 'Nikhil' 
try: 
	os.makedirs(path, exist_ok = True) 
	print("Directory '%s' created successfully" % directory) 
except OSError as error: 
	print("Directory '%s' can not be created" % directory) 

# By setting exist_ok as True 
# error caused due already 
# existing directory can be suppressed 
# but other OSError may be raised 
# due to other error like 
# invalid path name 
