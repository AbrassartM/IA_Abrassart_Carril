import csv

def BDD(cat, serie) :
    """
    function BDD
        Retourne les noms de fichiers issus de la BDD
        selon leur catégorie et leur série

        in:
        cat : (string) nom de leur catégorie
        serie : (int) numéro de la série - écrire 0 si
        on ne veut pas de série particulière

        out:
        BDD_utile : (np.array(string)) noms pertinents issus de la BDD
    """
    fname = "BDD_Signaux_reels.csv"
    file = open(fname, "r")
 
    reader = csv.reader(file)
    BDD_utile = []
    
    if serie == 0 :
        for row in reader :
            for i in range(0,14) :
                if cat in row[i] :
                    BDD_utile.append(row[i-1])
    else :
        for row in reader :
            if cat in row[2*serie-1] :
                BDD_utile.append(row[2*serie-2])
    file.close()
    return BDD_utile


def BDD_inv(nom) :
    """
    function BDD_inv
        Retourne la série d'où est issu le nom ddu signal
        donné en entrée

        in:
        nom : (string) nom du signal recherché
    """
    fname = "BDD_Signaux_reels.csv"
    file = open(fname, "r")
 
    reader = csv.reader(file)
    
    for row in reader :
        for i in row :
            if nom in i :
                print("Serie", row.index(nom)//2+1)
            
    file.close()
    

def BDD_type(typ) :
    """
    function BDD_type
        Retourne les noms de fichiers issus de la BDD
        qui contiennent le signal d'un même véhicule - samu, gend
        pol, americaine, pomp, amb

        in:
        typ : (string) nom du véhicule abrégé

        out:
        BDD_type : (np.array(string)) noms pertinents issus de la BDD
    """
    # On peut choisir une liste ou juste les noms
    # Tous les types : 'pol' , 'pomp' , 'amb' , 'samu' , 'americaine'
    fname = "BDD_Signaux_reels.csv"
    file = open(fname, "r")
 
    reader = csv.reader(file)
    BDD_type = []
    
    for row in reader :
        for i in row :
            if typ in i :
                BDD_type.append(i)
                
    file.close()
    return BDD_type
    