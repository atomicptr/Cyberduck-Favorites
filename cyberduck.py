import sys
import os
import getpass
import xml.etree.ElementTree as ET
import Alfred

handler = Alfred.Handler(sys.argv)

f = open("cyberduck_settings_folder.txt", "r")
settings_folder = f.read()

# remove the \n
settings_folder = settings_folder[:-1]
f.close()

settings_folder = settings_folder.replace("${username}", getpass.getuser())

settings_folder = os.path.join(settings_folder, "Bookmarks")

bookmark_info = []

for files in os.listdir(settings_folder):
	if files.endswith(".duck"):
		keys = []
		values = []

		file_path = os.path.join(settings_folder, files)

		tree = ET.parse(file_path)

		root = tree.getroot()[0]

		for child in root:
			if child.tag == "key":
				keys.append(child.text)
			elif child.tag == "string":
				values.append(child.text)

		bookmark_info.append({"keys": keys, "values": values, "file_path": file_path})

for info in bookmark_info:
	nickname = ""
	username = ""
	port = ""
	protocol = ""
	hostname = ""
	file_path = info["file_path"]

	i = 0

	for key in info["keys"]:
		if key == "Nickname":
			nickname = info["values"][i]
		elif key == "Username":
			username = info["values"][i]
		elif key == "Port":
			port = info["values"][i]
		elif key == "Protocol":
			protocol = info["values"][i]
		elif key == "Hostname":
			hostname = info["values"][i]

		i += 1

	if handler.query.lower() in nickname.lower():
		handler.add_new_item(title=nickname, subtitle="%s %s@%s:%s" % (protocol.upper(), username, hostname, port), icon="bookmark_icon.png", arg=file_path)

handler.push()
