from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#create Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel.db"

db = SQLAlchemy(app)

class Destination(db.Model): # creating table for DB
    id = db.Column(db.Integer, primary_key=True) # unique id for each row
    destination = db.Column(db.String(50), nullable=False)
    Country = db.Column(db.String(50), nullable=False)
    Rating = db.Column(db.Float, nullable=False)
    
    # converting data into JSON format or similar to Dict
    def to_dict(self):
        return {
            "id": self.id,
            "destination": self.destination,
            "country": self.Country,
            "rating": self.Rating
        }

with app.app_context():
    db.create_all()


# https://www.worldtour.io/
#create Routes
@app.route("/")
def home(): 
    return jsonify({"message": "Welcome to the Travel API"})

# https://www.worldtour.io/destinations
@app.route("/destinations", methods=["GET"])
def get_destinatons():
    destinations = Destination.query.all() # fetch every row in db
    
    return jsonify([destination.to_dict()] for destination in destinations)

# https://www.worldtour.io/destinations/2
@app.route("/destinations/<int:destination_id>", methods=["GET"])
def get_destinaton(destination_id):
    requested_dest = Destination.query.get(destination_id)
    if requested_dest:
        return jsonify(requested_dest.to_dict())
    else:
        return jsonify({"error":"Destination Not Found!"}), 404


# POST Request
@app.route("/destinations", methods=["POST"])
def add_destination():
    data = request.get_json() # takes incoming json body and parse the info 

    #new object
    new_destination = Destination(destination=data["destination"],
                                  Country=data["country"],
                                  Rating=data["rating"])
    
    # inserting to db by tapping into current db session
    db.session.add(new_destination)
    db.session.commit() # always commit when done adding
    
    return jsonify(new_destination.to_dict()), 201

# PUT -> Udpate
@app.route("/destinations/<int:destination_id>", methods=["PUT"])
def update_destination(destination_id):
    data = request.get_json()
    
    destination = Destination.query.get(destination_id)
    if destination:
        # tapping into property destination of the class
        destination.destination = data.get("destination", destination.destination)
        destination.Country = data.get("country", destination.Country)
        destination.Rating = data.get("rating", destination.Rating)
        
        db.session.commit()
        
        return jsonify(destination.to_dict())
    
    else:
        return jsonify({"error":"destination Not Found!"}), 404


# DELETE
@app.route("/destinations/<int:destination_id>", methods=["DELETE"])
def delete_destination(destination_id):
    data = Destination.query.get(destination_id)
    
    if data:
        db.session.delete(data)
        db.session.commit()
        
        return jsonify({"message":"destination was deleted!"})
    
    else:
        return jsonify({"error":"destination Not Found!"}), 404
    



if __name__ == "__main__":
    app.run(debug=True) #to keep this running