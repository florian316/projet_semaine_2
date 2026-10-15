import json
 
with open("mesures_capteurs_reseau.json", encoding="utf-8") as f:
    data = json.load(f)
 
 #Capteur avec ses mesures brutes, ses mesures nettoyées et ses compteurs d'anomalies.
class Capteur:
    
    #Crée le capteur et nettoie ses mesures automatiquement.
    def __init__(self, nom, mesures_brut, borne_min, borne_max): 
        self.nom = nom
        self.mesures_brut = mesures_brut
        self.mesure_netoyees = []
        self.nb_manquant = 0
        self.nb_aberrant = 0
        self.nb_non_numerique = 0
        self.borne_min = borne_min
        self.borne_max = borne_max
        self.nettoyer()
     #Garde les valeurs valides et compte les manquantes, non numériques et aberrantes.
    def nettoyer(self):
        for valeur in self.mesures_brut:
            if valeur is None:
                self.nb_manquant += 1
                continue
            try:
                nombre = float(valeur)
            except (ValueError, TypeError):
                self.nb_non_numerique += 1
                continue
 
            if not (self.borne_min <= nombre <= self.borne_max):
                self.nb_aberrant += 1
                continue
 
            self.mesure_netoyees.append(nombre)

    #Renvoie le nombre de mesures valides.
    def nb_valeur_valide(self):  
        return len(self.mesure_netoyees)
    
    def moyenne(self):
        if len(self.mesure_netoyees) > 0:
            return sum(self.mesure_netoyees) / len(self.mesure_netoyees)
        else:
            return None
    
    def maximum(self):
        if len(self.mesure_netoyees) > 0:
            return max(self.mesure_netoyees)
        else:
            return None

    def minimum(self):
        if len(self.mesure_netoyees) > 0:
            return min(self.mesure_netoyees)
        else:
            return None
        
    #Renvoie le nombre total de valeurs rejetées.
    def nb_anomalies(self):  
        return self.nb_manquant + self.nb_aberrant + self.nb_non_numerique
 
 
t = Capteur("temperature_bureau", data["temperature_bureau"], -10, 50)
h = Capteur("humidite_serre", data["humidite_serre"], 0, 100)
p = Capteur("pression_capteur_ext", data["pression_capteur_ext"], 870, 1085)
l = Capteur("luminosite_atelier", data["luminosite_atelier"], 0, 20000)
 

dict_capteur = {
    "temperature_bureau": t,
    "humidite_serre": h,
    "pression_capteur_ext": p,
    "luminosite_atelier": l
}
 
liste_capteurs = list(dict_capteur.values())
 
 
#Trie les capteurs du plus grand au plus petit nombre d'anomalies.
def tri_insertion(liste):
    
    for i in range(1, len(liste)):
        element = liste[i]
        j = i - 1
        while j >= 0 and liste[j].nb_anomalies() < element.nb_anomalies():
            liste[j + 1] = liste[j]
            j = j - 1
        liste[j + 1] = element
    return liste

for capteur in dict_capteur.values():
    print(capteur.nom, "| valides :", capteur.nb_valeur_valide(),
          "| moyenne :", round(capteur.moyenne(), 2),
          "| min :", capteur.minimum(), "| max :", capteur.maximum(),
          "| anomalies :", capteur.nb_anomalies())

print()
print("Classement par nombre d'anomalies :")
for capteur in tri_insertion(liste_capteurs):
    print(capteur.nom, ":", capteur.nb_anomalies())

