# This is for SWN Directory lookup
# If you've found this, it belongs to Yeran. Please don't hack him
import gspread

from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# Retrieve JSON key, authorize with Google Authority Server, then retrieve spreadsheet data
creds = ServiceAccountCredentials.from_json_keyfile_name('SWN_Info.json', scope)
# creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\Yeran\Desktop\Spreadsheet\SWN_Info.json', scope)
client = gspread.authorize(creds)
Planetary_Directory2 = client.open('Planetary Directory - SWN:RE')
Planetary_Directory = client.open('Planetary Directory - SWN:RE').worksheet("Planetary Directory")
SWNDirectory = Planetary_Directory.get_all_records()

# worksheet_list = client.open('Planetary Directory - SWN:RE').worksheets()
# This retrieves a list of worksheets. Does it request and initialize all worksheets though?

# worksheet_list[0].title
# This retrieves the title of a worksheet. This can be used to get a list of titles, and compare the input to the title of a gile

inputholder = 0


# keeping a list of the keys
directory_keylist = []
for key in SWNDirectory[0].keys():
	directory_keylist.append(key)


# Fix up sector hex locations
for entry in SWNDirectory:
	if len(str(entry["Hex"])) < 2:
		entry["Hex"] = "000" + str(entry["Hex"])
	else:
		entry["Hex"] = "0" + str(entry["Hex"])

# Find directory entry from string
def DirectoryEntryFinder(inputstring):
	returnlist = []
	returnstring = ""
	incrementer = 0
	for dictentry in SWNDirectory:
		for n in directory_keylist:
			if inputstring == str(dictentry[str(n)]):
				returnlist.append(DirectoryEntryRetriever(dictentry,1) + " - " + DirectoryEntryRetriever(dictentry,5))
				savedstring = DirectoryStringConcatenator(dictentry)
	if len(returnlist) > 1:
		while incrementer < len(returnlist):
			if returnstring == "":
				returnstring = "Which " + inputstring + "?\n" + returnlist[incrementer]
			else:
				returnstring = returnstring + "\n" + returnlist[incrementer]
			incrementer = incrementer + 1
		return returnstring
	elif len(returnlist) == 1:
		return savedstring
		return returnstring
	else:
		return "Done"

# Make an omega string once the directory entry is found
def DirectoryStringConcatenator(planetdict):
	n = 1
	LongString = ""
	for n in range (1, 18):
		LongString = LongString + str(DirectoryEntryRetriever(planetdict, n)) + "\n"
	return LongString

# Return the Planet info for the key # being returned
def DirectoryEntryRetriever(PlanetDict, n):
	return directory_keylist[n] + ": " + str(PlanetDict[str(directory_keylist[n])])

def InfoReturner(info_list, info_keylist):
	return_string = ""
	for dictitem in info_list:
		return_string = return_string + dictitem[info_keylist[0]] + "\n"
	print(return_string)

def TableEntryDetails(input,info_list,info_keylist):
	incrementer = 0
	return_string = ""
	for dictitem in info_list:
		if input == dictitem[info_keylist[0]]:
			while incrementer < len(info_keylist):
				return_string = return_string + info_keylist[incrementer] + ": " + str(dictitem[info_keylist[incrementer]]) + "\n"
				incrementer = incrementer + 1
			return return_string

def KeyListInitializer (dict):
	keylist = []
	for key in dict[0].keys():
		keylist.append(key)
		return keylist

currentSheet = Planetary_Directory2.worksheet("Planetary Details")
currentRecords = currentSheet.get_all_records()

KeyListInitializer(currentRecords)

# Get input. Keep getting input until "Done"

for index in Planetary_Directory2:
	print(index.title)

while inputholder < 1:
	Input = input("\n>>>What do you want to look up?\n\n")
	if Input == "Done":
		break
	else:
		currentSheet = Planetary_Directory2.worksheet(Input)
		if currentSheet.title == "Planetary Directory":
			Input = input("What Planet?")
			print(DirectoryEntryFinder(Input))
		else:
			