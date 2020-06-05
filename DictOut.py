Dict = {'W1':{'iz00240':{'lastlogon':'heute','Ldap':'Z1','PSW':'HalloW1'},'izx0240':{'lastlogon':'HEUTE','Ldap':'Z1','PSW':'HALLOW1'}}, \
        'W2':{'iz00240':{'lastlogon':'gestern','Ldap':'Z2','PSW':'HalloW2'},'izx0240':{'lastlogon':'GESTERN','Ldap':'Z2','PSW':'HALLOW2'}}, \
        'SW1':{'iz00240':{'lastlogon':'morgen','Ldap':'Z3','PSW':'HalloSw1'},'izx0240':{'lastlogon':'MORGEN','Ldap':'Z3','PSW':'HALLOSW1'}}}
PruefListe = ('lastlogon', 'Ldap', 'PSW','Quatsch','GrosserQuatsch')


keys = Dict.keys()
for hmcK, hmcV in Dict.items():
        users = hmcV.keys()

d = open("E:\\myData\\Programmieren\\Python\\XMLParsing\\ergebnis.txt","w",encoding="utf-8")
for user in users:
    d.write("UiD: "+user+"\n")
    d.write("          ")
    for PL in PruefListe:
        d.write("{:10}  ".format(PL[:9]))     #PL[:9] = nur die ersten 10 Zeichen des String werden angezeigt
    d.write("\n")
    for suf in keys:
        attribListe = ""
        d.write("HMC{:3}".format(suf)+"     ")
        for attrib in PruefListe:
            try:
                d.write(" {:8}  ".format(Dict[suf][user][attrib]))
            except (KeyError):
                d.write(" {:8}  ".format("   ---"))
        d.write("\n")
    d.write("\n")
d.close()
