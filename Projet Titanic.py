import csv
import os 

os.chdir(os.path.dirname(os.path.abspath(__file__)))


liste_p = []
with open('DM-titanic.csv', mode='r', encoding='utf-8') as f:
    lecteur = csv.DictReader(f)
    for ligne in lecteur:
        liste_p.append(dict(ligne))


nb_total = len(liste_p)

p54 = next(p for p in liste_p if p['PassengerId'] == '54')

nb_victimes = len([p for p in liste_p if p['Survived'] == '0']
                  
nb_e = len([p for p in liste_p if p['Age'] != '' and float(p['Age']) < 18])

p_marechal = 'Oui' if any("Marechal, Mr. Pierre" in p['Name'] for p in liste_p) else 'Non'

moy_c1 = sum([float(p['Age']) for p in liste_p if p['Pclass'] == '1' and p['Age'] != '']) / len([p for p in liste_p if p['Pclass'] == '1' and p['Age'] != ''])
                                                                                                 
h_p = [p for p in liste_p if p['Sex'] == 'male']
f_p = [p for p in liste_p if p['Sex'] == 'female']

stats_g = [
    {'label': 'Hommes', 'total': len(h_p), 'survivant': len([p for p in h_p if p['Survived'] == '1'])},
    {'label': 'Femmes', 'total': len(f_p), 'survivant': len([p for p in f_p if p['Survived'] == '1'])}
]

# Survie par Classes
stats_c = []

for n in ['1', '2', '3']:
    grp = [p for p in liste_p if p['Pclass'] == n]
    stats_c.append({'label': f'C{n}', 'total': len(grp), 'survivant': len([p for p in grp if p['Survived'] == '1'])})


# Survie par Ports
ports_map = {'C': 'Cherbourg', 'Q': 'Queenstown', 'S': 'Southampton'}
stats_p = []

for k, v in ports_map.items():
    grp = [p for p in liste_p if p['Embarked'] == k]
    stats_p.append({'label': v, 'total': len(grp), 'survivant': len([p for p in grp if p['Survived'] == '1'])})

nb_surv_cherbourg = len([p for p in liste_p if p['Embarked'] == 'C' and p['Survived'] == '1'])

#Survie par Age

stats_a = []

for cat, (min_a, max_a) in enumerate([(0,15), (15,30), (30,45), (45,60), (60,100)]):
    grp = [p for p in liste_p if p['Age'] != '' and min_a <= float(p['Age']) < max_a]
    stats_a.append({'label': f'{min_a}-{max_a}', 'total': len(grp), 'survivant': len([p for p in grp if p['Survived'] == '1'])})


nb_survivants = len([p for p in liste_p if p["Survived"]=='1']) 

# la taille de la famille 
for p in liste_p:
    p['FamilySize'] = int(p['SibSp']) + int(p['Parch']) + 1

# Trouver la plus grande famille
max_fam = max([p['FamilySize'] for p in liste_p])
Plus_grande_famille = next(p for p in liste_p if p['FamilySize'] == max_fam)


#  Seul vs En Famille
seuls = [p for p in liste_p if p['FamilySize'] == 1]
en_famille = [p for p in liste_p if p['FamilySize'] > 1]

stats_famille = [
    {'label': 'Voyage seul', 'total': len(seuls), 'survivant': len([p for p in seuls if p['Survived'] == '1'])},
    {'label': 'En famille', 'total': len(en_famille), 'survivant': len([p for p in en_famille if p['Survived'] == '1'])}
]


# Prix du billet le plus cher
prix_max = max([float(p['Fare']) for p in liste_p if p['Fare'] != ''])
passager_riche = next(p for p in liste_p if float(p['Fare']) == prix_max)

#Prix du billet le moins cher
prix_min = min([float(p['Fare']) for p in liste_p if p['Fare'] != ''])
passager_pauvre = next(p for p in liste_p if float(p['Fare']) == prix_min)

# Moyenne des tarifs par classe
moyennes_prix = []
for n in ['1', '2', '3']:
    tarifs = [float(p['Fare']) for p in liste_p if p['Pclass'] == n and p['Fare'] != '']
    moy = sum(tarifs) / len(tarifs) if tarifs else 0
    moyennes_prix.append({'label': f'Classe {n}', 'moyenne': round(moy, 2)})



#  On trie les passagers par prix 
p_tries = sorted([p for p in liste_p if p['Fare'] != ''], key=lambda x: float(x['Fare']))
total_p = len(p_tries)
taille_tranche = total_p // 20  # 5% du total

# On calcule la moyenne du prix et le taux de survie pour chaque tranche de 5%
stats_5pourcent = []
for i in range(20):
    debut = i * taille_tranche
    
    fin = (i + 1) * taille_tranche if i < 19 else total_p
    
    tranche = p_tries[debut:fin]
    
    moy_prix = sum([float(p['Fare']) for p in tranche]) / len(tranche)
    survivants = len([p for p in tranche if p['Survived'] == '1'])
    taux = (survivants / len(tranche)) * 100
    stats_5pourcent.append({'prix': round(moy_prix, 1), 'taux': round(taux, 1)})

# Analyse croisée : taux de survie par classe, sexe et tranche d'âge
classes = ['1', '2', '3']
ages = [('Enfant', 0, 18), ('Adulte', 18, 100)]

stats_hommes = []
stats_femmes = []

for c in classes:
    for a_nom, a_min, a_max in ages:
        # Filtrage pour les hommes
        grp_h = [p for p in liste_p if p['Sex'] == 'male' and p['Pclass'] == c and (p['Age'] != '' and a_min <= float(p['Age']) < a_max)]
        if grp_h:
            t_h = (len([p for p in grp_h if p['Survived'] == '1']) / len(grp_h)) * 100
            stats_hommes.append({'classe': f'Classe {c}', 'age': a_nom, 'total': len(grp_h), 'taux': round(t_h, 1)})
        
        # Filtrage pour les femmes
        grp_f = [p for p in liste_p if p['Sex'] == 'female' and p['Pclass'] == c and (p['Age'] != '' and a_min <= float(p['Age']) < a_max)]
        if grp_f:
            t_f = (len([p for p in grp_f if p['Survived'] == '1']) / len(grp_f)) * 100
            stats_femmes.append({'classe': f'Classe {c}', 'age': a_nom, 'total': len(grp_f), 'taux': round(t_f, 1)})

# Génération du rapport HTML
css = """:root {
    --bg: #0f172a;
    --card-bg: #1e293b;
    --txt: #f8fafc;
    --accent: #38bdf8;
    --win: #4ade80;
    --loss: #f87171;
}

body {
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--txt);
    margin: 0;
    padding: 40px;
}

.box {
    max-width: 1000px;
    margin: auto;
    background: var(--card-bg);
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
}

h1 { 
    font-size: 28px; 
    color: var(--accent); 
    text-align: center;
    margin-bottom: 24px; 
    border-bottom: 2px solid var(--accent); 
    padding-bottom: 10px; 
}


.screenshot-cards {
    display: flex;
    gap: 20px;
    margin-bottom: 30px;
}

.s-card {
    flex: 1;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    font-weight: bold;
}

.s-card span { display: block; font-size: 14px; margin-bottom: 5px; opacity: 0.9; }
.s-card div { font-size: 28px; }

.c-gray { background: #64748b; }
.c-green { background: #22c55e; }
.c-red { background: #ef4444; }


.dm-details {
    background: #0f172a;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 25px;
    border: 1px solid #334155;
}

table { width: 100%; border-collapse: collapse; margin-top: 15px; border-radius: 8px; overflow: hidden; }
th { background: #334155; text-align: left; padding: 12px; color: #94a3b8; font-size: 13px; }
td { padding: 12px; border-bottom: 1px solid #334155; font-size: 14px; }
.win { color: var(--win); font-weight: bold; }
.loss { color: var(--loss); font-weight: bold; }

.graph-container {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    height: 300px;
    background: #0f172a;
    padding: 40px 20px 60px 20px;
    border-radius: 12px;
    margin-top: 20px;
    border: 1px solid #334155;
}

.bar-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
    height: 100%;
    position: relative;
}

.bar {
    width: 70%;
    background: var(--accent);
    border-radius: 4px 4px 0 0;
    transition: height 0.3s ease;
    position: relative;
}

.bar:hover { background: var(--win); }

.bar-value {
    position: absolute;
    top: -25px;
    font-size: 10px;
    color: var(--txt);
    width: 100%;
    text-align: center;
}

.bar-label {
    position: absolute;
    bottom: -45px;
    font-size: 9px;
    color: #94a3b8;
    transform: rotate(-45deg);
    white-space: nowrap;
}

.tables-row {
    display: flex;
    gap: 30px;
    margin-top: 20px;
}

.table-container {
    flex: 1;
    min-width: 300px;
}

.table-container h4 {
    text-align: center;
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 10px;
}

.h-title { background: rgba(56, 189, 248, 0.2); color: #38bdf8; }
.f-title { background: rgba(244, 114, 182, 0.2); color: #f472b6; }
"""
with open("titanic.css", "w", encoding="utf-8") as f_css:
    f_css.write(css)

html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="titanic.css">
</head>
<body>
    <div class="box">
        <h1>Rapport d'Analyse : Titanic</h1>
        
        <div class="screenshot-cards">
            <div class="s-card c-gray"><span>Passagers</span><div>{nb_total}</div></div>
            <div class="s-card c-green"><span>Survivants</span><div>{nb_survivants}</div></div>
            <div class="s-card c-red"><span>Victimes</span><div>{nb_victimes}</div></div>
        </div>
        
        <div class="dm-details">
        <h3>Réponses au DM</h3>
            <p><b>1. Nombre de passagers :</b> {nb_total}</p>
            <p><b>2. Vérification Passager 54 :</b> {p54['Name']}, {p54['Age']} ans, Classe {p54['Pclass']}, Port {p54['Embarked']}, Survie: {'Oui' if p54['Survived']=='1' else 'Non'}</p>
            <p><b>3. Nombre de victimes :</b> {nb_victimes}</p>
            <p><b>4. Nombre d'enfants mineurs :</b> {nb_e}</p>
            <p><b>5. Présence de Pierre Marechal :</b> {p_marechal}</p>
            <p><b>6. Moyenne d'âge en 1ère classe :</b> {moy_c1:.1f} ans</p>
            <p><b>9. Survivants embarqués à Cherbourg :</b> {nb_surv_cherbourg}</p>
            <p><b>Plus grande famille :</b> {max_fam} personnes (Famille de {Plus_grande_famille['Name']})</p>
            <p><b>Passagers voyageant seuls :</b> {len(seuls)}</p>
            <p><b>Prix du billet le plus cher :</b> {prix_max:.2f} (£)</p>
            <p><b>Passager le plus riche :</b> {passager_riche['Name']}</p>
            <p><b>Prix du billet le moins cher :</b> {prix_min:.2f} (£)</p>
            <p><b>Passager le plus pauvre :</b> {passager_pauvre['Name']}</p>
        </div>

        <h3>Genres</h3>
        <table>
            <tr><th>Genre</th><th>Total</th><th>Survivants</th><th>Taux</th></tr>
            {"".join([f"<tr><td>{d['label']}</td><td>{d['total']}</td><td>{d['survivant']}</td><td class='{'win' if (d['survivant']/d['total']) > 0.45 else 'loss'}'>{round(d['survivant']/d['total']*100, 1)}%</td></tr>" for d in stats_g])}
        </table>

        <h3>Classes</h3>
        <table>
            <tr><th>Classe</th><th>Total</th><th>Survivants</th><th>Taux</th></tr>
            {"".join([f"<tr><td>{d['label']}</td><td>{d['total']}</td><td>{d['survivant']}</td><td class='{'win' if (d['survivant']/d['total']) > 0.45 else 'loss'}'>{round(d['survivant']/d['total']*100, 1)}%</td></tr>" for d in stats_c])}
        </table>

        <h3>Ports</h3>
        <table>
            <tr><th>Port</th><th>Total</th><th>Survivants</th><th>Taux</th></tr>
            {"".join([f"<tr><td>{d['label']}</td><td>{d['total']}</td><td>{d['survivant']}</td><td class='{'win' if (d['survivant']/d['total']) > 0.45 else 'loss'}'>{round(d['survivant']/d['total']*100, 1)}%</td></tr>" for d in stats_p])}
        </table>

        <h3>Âge</h3>
        <table>
            <tr><th>Tranche d'âge</th><th>Total</th><th>Survivants</th><th>Taux</th></tr>
            {"".join([f"<tr><td>{d['label']}</td><td>{d['total']}</td><td>{d['survivant']}</td><td class='{'win' if (d['survivant']/d['total']) > 0.45 else 'loss'}'>{round(d['survivant']/d['total']*100, 1)}%</td></tr>" for d in stats_a])}
        </table>

        <h3>Taux de survie selon la situation familiale</h3>
        <table>
            <tr><th>Situation</th><th>Total</th><th>Survivants</th><th>Taux</th></tr>
            {"".join([f"<tr><td>{d['label']}</td><td>{d['total']}</td><td>{d['survivant']}</td><td class='{'win' if (d['survivant']/d['total']) > 0.45 else 'loss'}'>{round(d['survivant']/d['total']*100, 1)}%</td></tr>" for d in stats_famille])}
        </table>

        <h3>Moyenne des tarifs par classe</h3>
        <table>
            <tr><th>Classe</th><th>Moyenne du tarif (£)</th></tr>
            {"".join([f"<tr><td>{d['label']}</td><td>{d['moyenne']}</td></tr>" for d in moyennes_prix])}
        </table>
    </div>

    <h3>Analyse du Taux de Survie par Tranche de Prix (5%)</h3>
        <p style="font-size: 12px; color: #94a3b8;">L'abscisse indique le prix moyen du billet (£), la hauteur indique le % de survie.</p>
        
        <div class="graph-container">
            {"".join([f'''
            <div class="bar-wrapper">
                <div class="bar-value">{d['taux']}%</div>
                <div class="bar" style="height: {d['taux']}%"></div>
                <div class="bar-label">{d['prix']}£</div>
            </div>
            ''' for d in stats_5pourcent])}
        </div>

        <h3>Matrices de Survie Comparées</h3>
        <div class="tables-row">
            
            <div class="table-container">
                <h4 class="h-title"> Hommes</h4>
                <table>
                    <tr><th>Classe</th><th>Âge</th><th>Total</th><th>Survie</th></tr>
                    {"".join([f"<tr><td>{d['classe']}</td><td>{d['age']}</td><td>{d['total']}</td><td class='{'win' if d['taux'] > 50 else 'loss'}'>{d['taux']}%</td></tr>" for d in stats_hommes])}
                </table>
            </div>

            <div class="table-container">
                <h4 class="f-title">Femmes</h4>
                <table>
                    <tr><th>Classe</th><th>Âge</th><th>Total</th><th>Survie</th></tr>
                    {"".join([f"<tr><td>{d['classe']}</td><td>{d['age']}</td><td>{d['total']}</td><td class='{'win' if d['taux'] > 50 else 'loss'}'>{d['taux']}%</td></tr>" for d in stats_femmes])}
                </table>
            </div>

        </div>
</body>
</html>
"""

with open("titanic.html", "w", encoding="utf-8") as f_html:
    f_html.write(html)

print("Fichiers générés : titanic.html, titanic.css")
print("Ouvrez le fichier titanic.html dans un navigateur pour voir le rapport d'analyse.")
