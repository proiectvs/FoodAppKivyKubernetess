from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import socket
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/dev"
mongo = PyMongo(app)
db = mongo.db



@app.route("/")
def index():
    hostname = socket.gethostname()
    return jsonify(message="Welcome to Tasks app! I am running inside {} pod!".format(hostname))

    
###############################################
@app.route("/login")
def login():
    data = request.get_json(force=True)
    email=data["nume"]
    
    userlogat=db.user.find_one({"email": f"{email}"})
    if  userlogat:
        if userlogat["parola"]==data["parola"]:
            return("gasit")
        else:
            return("1")
    else:
        return("1")
    



@app.route("/comenzi")
def afiseaza_comenzi():
    comenzi = db.comanda.find()
    data = []
    for comanda in comenzi:
        item = {
            "id": str(comanda["_id"]),
            "produse_comanda": comanda["produse_comanda"],
            "status_comanda": comanda["status_comanda"],
            "pret_comanda": comanda["pret_comanda"],
            "id_user":comanda["id_user"]
        }
        data.append(item)
    return jsonify(
        data=data
    )
    
@app.route("/comanda", methods=["POST"])
def create_comenzi():
    print(1)
    data = request.get_json(force=True)
    db.comanda.insert_one({"produse_comanda": data["produse_comanda"],
            "status_comanda": data["status_comanda"],
            "pret_comanda": data["pret_comanda"],
            "id_user":data["id_user"]
                           
    
    })
    return jsonify(
        message="comanda salvata cu succes!"
    )
    
@app.route("/users")
def afiseaza_useri():
    users = db.user.find()
    data = []
    for user in users:
        item = {
            "id": str(user["_id"]),
            "nume": user["nume"],
            "prenume": user["prenume"],
            "parola": user["parola"],
            "email":user["email"],
            "adresa":user["adresa"]
        }
        data.append(item)
    return jsonify(
        data=data
    )    

    
@app.route("/register", methods=["POST"])
def register():
    print(1)
    data = request.get_json(force=True)
    db.user.insert_one({"nume": data["nume"],
            "prenume": data["prenume"],
            "parola": data["parola"],
            "email":data["email"],
            "adresa":data["adresa"]
                           
    
    })
    return jsonify(
        message="comanda salvata cu succes!"
    )
    
    
    
@app.route("/comenzi/delete", methods=["POST"])
def sterge_comenzi():
    db.comanda.remove()
    return jsonify(
        message="comenzi sterse "
    )    
    
@app.route("/users/delete", methods=["POST"])
def sterge_users():
    db.user.remove()
    return jsonify(
        message="Utilizatori stersi"
    )    
#################################################    
    
    
 
    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)