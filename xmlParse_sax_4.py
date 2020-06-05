import xml.sax



class SampleHandler_User(xml.sax.handler.ContentHandler):
	def __init__(self):
		self.pruefListe = {"pwAuthenticationyype", "ldapserver", "passwordrule", "disabled", \
							"lastlogon", "sessiontimeout", "verifytimeout", "idletimeout", \
							"pwrequiredfordisruptiveact"}
		self.wert = ""
		self.user = ""
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
			self.user = ""
			#print("-----------------------------------------------------------")
		if self.auditSektor and name == "name":
			self.userSektor = False
			print("UserID:                    -",self.wert)
			self.user = self.wert
			print("user: ",user)
			self.wert = ""
		if self.auditSektor and (name in self.pruefListe):
			#----- Umkehr der Logik ob ein User disabled oder Aktiv ist
			if name == "disabled":
				if self.wert == "false":
					self.wert = "aktiv"
				else:
					self.wert = "disabled"
			#----- Verbesserte Ausgabe von pwrequiredfordisruptiveact		
			if name == "pwrequiredfordisruptiveact":
				if self.wert == "false":
					self.wert = "no"
				else:
					self.wert = "yes"		
					
			#----- Ausgabe Daten
			self.collectData = False
			#print("user-2- ",user)
			#print("-name- ",name)
			#print("-self.wert- ",self.wert)
			#print("-UserAttrib- ",UserAttrib)
			#print("-UiD- ",UiD)
			UserAttrib[name] = self.wert
			UiD[self.user] = UserAttrib[name]
			#print("----------------",UiD[self.user])
			print("{:26} - {}".format(name, self.wert))#," --- ",UserAttrib)
#			print("{:26} - {}".format(name,self.wert))
			self.wert = ""

			
		if self.itemSektor and name == "item":
			print("Roles                      -",self.wert)
			self.itemSektor = False
			self.wert = ""
		if self.rolesSektor and name == "roles":
			self.rolesSektor = False

		if self.auditSektor and name == "user":
			print("-----------------------------------------------------------")
		#pass
		
		
	def characters(self, content ):
		if self.userSektor or self.collectData or self.itemSektor:
			self.wert += content.strip()

class SampleHandler_PSWProfil(xml.sax.handler.ContentHandler):
	def __init__(self):
		self.pruefListe = {"rulename", "expirationcount", "minimumlength","maximumlength", \
							"consecutivecharacters", "historycount", "casesensitive", \
							"alphabetic", "numeric", "special"}
		self.wert = ""
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
			#----- Ausgabe Daten
			self.collectData = False
			self.characterRule = False
			print("{:26} - {}".format(name,self.wert))
			self.wert = ""

		if self.auditSektor and name == "rule":
			print("-----------------------------------------------------------")
		#pass
		
		
	def characters(self, content ):
		if self.ruleSektor and self.collectData:
			self.wert += content.strip()



def Auswertung_User(dateiname):
	print("***********************************************************")
	print(dateiname)
	print("***********************************************************")
	handler = SampleHandler_User()
	parser = xml.sax.make_parser()
	parser.setContentHandler(handler)
	parser.parse(dateiname)

def Auswertung_PSWProfil(dateiname):
	print("***********************************************************")
	print(dateiname)
	print("***********************************************************")
	handler = SampleHandler_PSWProfil()
	parser = xml.sax.make_parser()
	parser.setContentHandler(handler)
	parser.parse(dateiname)
#D:\Programmieren\AuditLogs-alleCECs\auditlogs
datei = "D:\\Programmieren\\AuditLogs-alleCECs\\auditlogs\\Audit89.HMCW1.xml"
datei2 = "D:\\Programmieren\\AuditLogs-alleCECs\\auditlogs\\Audit82.HMCW2.xml"
#datei2 = "F:\\FTP-Data\\Python\\code\\CodeInWork\\Data\\Audit82.HMCW2.xml"
#datei = "F:\\FTP-Data\\Python\\code\\CodeInWork\\Data\\Audit89.HMCW1_short.xml"	
#datei = "F:\\FTP-Data\\Python\\code\\CodeInWork\\Data\\Audit209.HMCW1.short.xml"
UserListe = {'ACSADMIN', 'ADVANCED', 'ENSADMIN', 'ENSOPERATOR', 'HCMNOT', \
			  'OPERATOR', 'SERVICE', 'SYSPROG', \
			  'UserTemplate_OC-MF', 'UserTemplate_Sysprog', 'UserTemplate_Admin'}
UserAttrib = {}
UiD = {}
Users = {}
HMCs = {}
user = ""

Auswertung_User(datei)
HMCs['W1'] = UiD

UiD = {}
Auswertung_User(datei2)
HMCs['W2'] = UiD
print("--------------------------------------")
print("--------------------------------------")
#print(HMCs)

print(UiD)
Dict = UiD
keys = Dict.keys()
print("DK: ",keys)
for hmcK, hmcV in Dict.items():
        users = hmcV.keys()
        print("user: ",users)
        print("hmcK: ",hmcK)
        print("hmcV: ", hmcV)
d = open("D:\\Programmieren\\AuditLogs-alleCECs\\auditlogs\\ergebnis.txt","w",encoding="utf-8")
for user in users:
        print("UiD: ",user)
        d.write("UiD: "+user+"\n")
        for suf in keys:
                attribListe = ""
                print("HMC"+suf)
                d.write("HMC"+suf+"\n")
                for attrib in PruefListe:
                        print("{:10}: {:8}".format(attrib,Dict[suf][user][attrib]))
                        d.write("{:10}: {:8}  ".format(attrib,Dict[suf][user][attrib]))
                d.write("\n")
d.close()
'''
check = 'lastlogon'
for usrLst in UserListe:
	for hmcK, hmcV in HMCs.items():
		HMC = HMCs[hmcK]
		for usrK, usrV in HMC.items():
			USR = HMC[usrK]
			#print("usrK--",usrK)
#			print(check + " - " + usrK + " -- " + USR[check])
			#for usrk in HMC[usrK]:
			#print("usrK: ",usrK)
			#print("usrV-LL: ",HMC[usrK][check])
			#if usrK in HMC[usrK]:
			#if usrK in UserListe:
		#		print("hmcK: ",hmcK)
		#		print("usrK: ",usrK)
		#		print("usrK-LL: ",check)
		#		print("usrV-LL: ",HMC[usrK][check])
				#print(" {} {} {} {}".format(hmcK, usrK, usrK['lastlogon'], usrV['lastlogon']))
			#print("usrV = ",usrV)
			#print("usrK = ",usrK)
	pass

#for hmcK, hmcV in HMCs.items():
#	USR = HMCs[hmcK]
	#print("usr - ",hmcK)
	#for usrK, usrV in USR.items():
	#	print(hmcK,"usr--",usrK)
	#	Attribute = USR[usrK]
	#	for key, value in Attribute.items():
	#		#print(key + "---" + value)
	#		pass


#for hmc in HMCs:
	#print("HMCNOT - ",hmc," ",HMCs[hmc]["HMCNOT"])
#	for k, v in HMCs[hmc]["HMCNOT"].items():
#		print(" {:26} = {}".format(k,v))


#Auswertung_PSWProfil(datei)
'''


