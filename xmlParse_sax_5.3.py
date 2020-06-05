import xml.sax, os, sys, datetime

class SampleHandler_User(xml.sax.handler.ContentHandler):
	def __init__(self):
		self.pruefListe = {"pwAuthenticationyype", "ldapserver", "passwordrule", "disabled", \
							"lastlogon", "sessiontimeout", "verifytimeout", "idletimeout", \
							"pwrequiredfordisruptiveact"}
		self.wert = ""
		self.user = ""
		self.dict = {}
		self.auditSektor = False
		self.userSektor = False
		self.rolesSektor = False
		self.itemSektor = False
		self.collectData = False
		
	def startDocument(self):
		pass
		
	def endDocument(self):
		print("EndeDocument")
		
	def startElement(self, name, attrs):

			if self.auditSektor and name == "name":
					self.userSektor = True
					self.user = ""
			if self.auditSektor and (name in self.pruefListe):
					self.collectData = True
			if self.auditSektor and name == "roles":
					self.rolesSektor = True
			if self.rolesSektor and name == "item":
					self.itemSektor = True
		
	#--- Abfragen auf Attribut 'Users' und setzen Begin des Auswertebereichs ---
			attrsListe = attrs.getNames()
			i=0
			for attribut in attrsListe:
				if attrs.getValue(attribut) == "Users":
					self.auditSektor = True
				i += 1

		
		
	def endElement(self, name):
		if name == "auditdata":
			self.auditSektor = False
		if self.auditSektor and name == "name":
			self.userSektor = False
			self.user = self.wert  #UserID zwischenspeichern
			self.wert = ""
		if self.auditSektor and (name in self.pruefListe):
			#----- Umkehr der Logik ob ein User disabled oder Aktiv ist
			if name == "disabled":
				if self.wert == "false":
					self.wert = "nein"
				else:
					self.wert = "disabled"
			#----- Verbesserte Ausgabe von pwrequiredfordisruptiveact		
			if name == "pwrequiredfordisruptiveact":
				if self.wert == "false":
					self.wert = "no"
				else:
					self.wert = "yes"		
			self.collectData = False
			self.dict[name] = self.wert
			UserAttrib[name] = self.wert		#User Attribut speichern
			UiD[self.user] = UserAttrib			#User Attribute eine UserID zuordnen
			self.wert = ""   #Variable muss zurückgesetzt werden!! klappt noch nicht
			
		if self.itemSektor and name == "item":
			#print("Roles                      -",self.wert)
			self.itemSektor = False
			self.wert = ""
		if self.rolesSektor and name == "roles":
			self.rolesSektor = False

		if self.auditSektor and name == "user":
			UiD[self.user]=self.dict
			self.dict={}

		
		
	def characters(self, content ):
		if self.userSektor or self.collectData or self.itemSektor:
			self.wert += content.strip()


class SampleHandler_PSWProfil(xml.sax.handler.ContentHandler):
	def __init__(self):
		self.pruefListe = {"rulename", "expirationcount", "minimumlength","maximumlength", \
							"consecutivecharacters", "historycount", "casesensitive", \
							"alphabetic", "numeric", "special"}
		self.wert = ""
		self.rule = ""
		self.dict = {}
		self.auditSektor = False
		self.ruleSektor = False
		self.collectData = False
		self.characterRule = False
		
	def startDocument(self):
		pass
		
	def endDocument(self):
		print("EndeDocument")
		
	def startElement(self, name, attrs):
		if self.auditSektor and name == "rule":
				self.ruleSektor = True
				self.rule = ""
				self.dict = {}
		if self.auditSektor and (name in self.pruefListe):
				self.collectData = True
		if self.auditSektor and name == "characterrule":
				self.characterRule = True
	#--- Abfragen auf Attribut 'Users' und setzen Begin des Auswertebereichs ---
		attrsListe = attrs.getNames()
		i=0
		for attribut in attrsListe:
			if attrs.getValue(attribut) == "Password rules":
				self.auditSektor = True
			i += 1
		
		
	def endElement(self, name):
		if name == "auditdata":
			self.auditSektor = False
		if self.auditSektor and name == "rule":
			self.userSektor = False
			self.wert = ""
		if self.characterRule and name == "characterrule":
			self.characterRule = False
		if self.auditSektor and (name in self.pruefListe) and not self.characterRule:				
			if name == "rulename":
				self.rule = self.wert
			else:	
				self.dict[name] = self.wert
			self.collectData = False
			self.characterRule = False
			#----- Ausgabe Daten			
			self.wert = ""
		if self.auditSektor and name == "rule":
			PSWProf[self.rule] = self.dict
		#pass
		
		
	def characters(self, content ):
		if self.ruleSektor and self.collectData:
			self.wert += content.strip()



def Auswertung_User(dateiname):
	print("***********************************************************")
	print(dateiname)
	print("***********************************************************")
	handler = SampleHandler_User()
	print("handler: ",handler)
	parser = xml.sax.make_parser()
	parser.setContentHandler(handler)
	parser.parse(dateiname)

def Auswertung_PSWProfil(dateiname):
	print("***********************************************************")
	print(dateiname)
	print("***********************************************************")
	print("lK 1")
	handler = SampleHandler_PSWProfil()
	print("lK 2")
	parser = xml.sax.make_parser()
	print("lK 3")
	parser.setContentHandler(handler)
	print("lK 4")
	parser.parse(dateiname)

PruefListe = ["pwAuthenticationyype", "ldapserver", "passwordrule", "disabled", \
				   "lastlogon", "sessiontimeout", "verifytimeout", "idletimeout", \
				   "pwrequiredfordisruptiveact"]

UserAttrib = {}		#einzelne Attribute mit Werten
PSWProf ={}
AuditListe = {}
PSWProfilListe = {}

auditPath = ['E:\\myData\\Programmieren\\Python\\auditlog']
Suffix = []
d = open("E:\\myData\\Programmieren\\Python\\XMLParsing\\ergebnis.txt","w",encoding="utf-8")
d.write("Eingelesene Dateien\n")

for d2z in range(0,len(auditPath)):
	os.chdir(auditPath[d2z])
	FilesInDir = os.listdir()  #Einlesen Dateinamen aus dem aktiven Verzeichnis

for Dataset in FilesInDir:
	d.write(Dataset+"\n")

for D in FilesInDir:
	F = D.partition(".")      #Filename aufspalten in "xxxx",".","yyy.xml"
	F = F[2].partition(".")   #2tes Element aufspalten in "yyy",".","xml"
	G = F[0]
	Suffix.append(G[3:])      #SysSuffix ab Stelle 3

i=0
for i in range(0,len(FilesInDir)):
	UiD = {}
	PSWProf = {}
	datei = auditPath[0] + "\\" + FilesInDir[i]
	Auswertung_User(datei)
	AuditListe[Suffix[i]] = UiD
	Auswertung_PSWProfil(datei)
	PSWProfilListe[Suffix[i]] = PSWProf
	print(PSWProf)

print(PSWProfilListe)
'''
print("AL: ",AuditListe)  #Hier steht das komplette Dic drin
print("Suffix: ",Suffix)
print("UiD: ",UiD)
'''
'''
#Auswertung_PSWProfil(datei)
'''
Dict = AuditListe
keys = Dict.keys()
for hmcK, hmcV in Dict.items():
        users = hmcV.keys()

d = open("E:\\myData\\Programmieren\\Python\\XMLParsing\\ergebnis.txt","w",encoding="utf-8")
for user in users:
    d.write("UiD: "+user+"\n")
    d.write("          ")
    for PL in PruefListe:
        d.write("{:26}-".format(PL[:26]))     #PL[:9] = nur die ersten 10 Zeichen des String werden angezeigt
    d.write("\n")
    for suf in keys:
        attribListe = ""
        d.write("HMC{:3}".format(suf)+"    ")
        for attrib in PruefListe:
            try:
                d.write("{:26}-".format(Dict[suf][user][attrib]))
            except (KeyError):
                d.write("{:26}-".format("---"))
        d.write("\n")
    d.write("\n")

#PSW Profil
pswkeys = PSWProfilListe.keys()
for pswK, pswV in PSWProfilListe.items():
        pswprofs = pswV.keys()
for pswprof in pswprofs:
    d.write("UiD: "+pswprof+"\n")
    d.write("          ")
    for PL in PruefListe:
        d.write("{:26}-".format(PL[:26]))     #PL[:9] = nur die ersten 10 Zeichen des String werden angezeigt
    d.write("\n")
    for suf in pswkeys:
        attribListe = ""
        d.write("HMC{:3}".format(suf)+"    ")
        for attrib in PruefListe:
            try:
                d.write("{:26}-".format(Dict[suf][pswprof][attrib]))
            except (KeyError):
                d.write("{:26}-".format("---"))
        d.write("\n")
    d.write("\n")

d.close()


