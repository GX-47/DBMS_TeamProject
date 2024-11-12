from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Abhi301103#@localhost/ams'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app) # Add this import at the top
CORS(app)  # Add this line after creating the Flask app

# Database Models
class Flight(db.Model):
    Flight_ID = db.Column(db.Integer, primary_key=True)
    Capacity = db.Column(db.Integer)
    Model = db.Column(db.String(100))
    Source = db.Column(db.String(100))
    Destination = db.Column(db.String(100))
    Ticket_Cost = db.Column(db.Float)
    Status = db.Column(db.String(50))
    Arrival = db.Column(db.String(100))
    Departure = db.Column(db.String(100))

class Passenger(db.Model):
    Passenger_ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Age = db.Column(db.Integer)
    Gender = db.Column(db.String(50))

class Crew(db.Model):
    Crew_ID = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(100))
    Salary = db.Column(db.Float)
    Years_of_service = db.Column(db.Integer)
    
class Captain(db.Model):
    Captain_ID = db.Column(db.Integer, primary_key = True)
    Crew_ID = db.Column(db.Integer)
    
class Booking(db.Model):
    Booking_ID = db.Column(db.Integer, primary_key = True)
    Passenger_ID = db.Column(db.Integer)
    Flight_ID = db.Column(db.Integer)
    Seat_No = db.Column(db.Integer)
    Seat_Type = db.Column(db.String(100))
    
class Food(db.Model):
    Item_name = db.Column(db.Integer, primary_key = True)
    Cost = db.Column(db.Float)
    Stock = db.Column(db.Integer)
    
class Buys(db.Model):
    Passenger_ID = db.Column(db.Integer, primary_key = True)
    Item_name = db.Column(db.String(50))
    
class Serves(db.Model):
    Crew_ID = db.Column(db.Integer, primary_key = True)
    Item_name = db.Column(db.String(50))
    
class Luggage(db.Model):
    Passenger_ID = db.Column(db.Integer)
    Flight_ID = db.Column(db.Integer)
    Luggage_ID = db.Column(db.Integer, primary_key = True)
    Type = db.Column(db.String(50))


# Marshmallow Schemas
class FlightSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Flight

flight_schema = FlightSchema()
flights_schema = FlightSchema(many=True)

class PassengersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Passenger

passenger_schema = PassengersSchema()
passengers_schema = PassengersSchema(many=True)

class CrewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Crew

crew_schema = CrewSchema()
crews_schema = CrewSchema(many=True)

class CaptainSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Captain

captain_schema = CaptainSchema()
captains_schema = CaptainSchema(many=True)

class BookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Booking

booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)

class FoodSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Food

food_schema = FoodSchema()
foods_schema = FoodSchema(many=True)

class BuysSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Buys

buys_schema = BuysSchema()
buyss_schema = BuysSchema(many=True)

class ServesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Serves

serves_schema = ServesSchema()
servess_schema = ServesSchema(many=True)

class LuggageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Luggage

luggage_schema = LuggageSchema()
luggages_schema = LuggageSchema(many=True)

# API Routes
@app.route('/flights', methods=['POST'])
def add_flight():
    data = request.get_json()
    new_flight = Flight(
        Capacity=data['Capacity'],
        Model=data['Model'],
        Source=data['Source'],
        Destination=data['Destination'],
        Ticket_Cost=data['Ticket_Cost'],
        Status=data['Status'],
        Arrival=data['Arrival'],
        Departure=data['Departure']
    )
    db.session.add(new_flight)
    db.session.commit()
    return flight_schema.jsonify(new_flight)

@app.route('/passengers', methods=['POST'])
def add_passenger():
    data = request.get_json()
    new_passenger = Passenger(
        Passenger_ID=data['Passenger_ID'],
        Name=data['Name'],
        Age=data['Age'],
        Gender=data['Gender']
    )
    db.session.add(new_passenger)
    db.session.commit()
    return passenger_schema.jsonify(new_passenger)

@app.route('/crew', methods=['POST'])
def add_crew():
    data = request.get_json()
    new_crew = Crew(
        Crew_ID=data['Crew_ID'],
        Name=data['Name'],
        Salary=data['Salary'],
        Years_of_service=data['Years_of_service']
    )
    db.session.add(new_crew)
    db.session.commit()
    return crew_schema.jsonify(new_crew)

@app.route('/captain', methods=['POST'])
def add_captain():
    data = request.get_json()
    new_captain = Captain(
        Captain_ID = data['Captain_ID'],
        Crew_ID=data['Crew_ID']
    )
    db.session.add(new_captain)
    db.session.commit()
    return captain_schema.jsonify(new_captain)

@app.route('/bookings', methods=['POST'])
def add_booking():
    data = request.get_json()
    new_booking = Booking(
        Booking_ID = data['Booking_ID'],
        Passenger_ID=data['Passenger_ID'],
        Flight_ID = data['Flight_ID'],
        Seat_No = data['Seat_No'],
        Seat_Type = data['Seat_Type']
    )
    db.session.add(new_booking)
    db.session.commit()
    return booking_schema.jsonify(new_booking)

@app.route('/food', methods=['POST'])
def add_food():
    data = request.get_json()
    new_food = Food(
        Item_name = data['Item_name'],
        Cost=data['Cost'],
        Stock = data['Stock']
    )
    db.session.add(new_food)
    db.session.commit()
    return food_schema.jsonify(new_food)

@app.route('/buys', methods=['POST'])
def add_buys():
    data = request.get_json()
    new_buys = Buys(
        Passenger_ID = data['Passenger_ID'],
        Item_name=data['Item_name']
    )
    db.session.add(new_buys)
    db.session.commit()
    return buys_schema.jsonify(new_buys)

@app.route('/luggage', methods=['POST'])
def add_luggage():
    data = request.get_json()
    new_luggage = Luggage(
        Passenger_ID = data['Passenger_ID'],
        Flight_ID = data['Flight_ID'],
        Luggage_ID = data['Luggage_ID'],
        Type = data['Type']
    )
    db.session.add(new_luggage)
    db.session.commit()
    return luggage_schema.jsonify(new_luggage)


@app.route('/flights', methods=['GET'])
def get_flights():
    flights = Flight.query.all()
    return flights_schema.jsonify(flights)

@app.route('/passengers', methods=['GET'])
def get_passengers():
    passengers = Passenger.query.all()
    return passengers_schema.jsonify(passengers)

@app.route('/crew', methods=['GET'])
def get_crews():
    crew = Crew.query.all()
    return crews_schema.jsonify(crew)

@app.route('/captain', methods=['GET'])
def get_captains():
    captains = Captain.query.all()
    return captains_schema.jsonify(captains)

@app.route('/bookings', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    return bookings_schema.jsonify(bookings)

@app.route('/food', methods=['GET'])
def get_foods():
    foods = Food.query.all()
    return foods_schema.jsonify(foods)

@app.route('/buys', methods=['GET'])
def get_buys():
    buyss = Buys.query.all()
    return buyss_schema.jsonify(buyss)

@app.route('/luggage', methods=['GET'])
def get_luggages():
    luggages = Luggage.query.all()
    return luggages_schema.jsonify(luggages)

#Function
@app.route('/api/total_flights', methods=['GET'])
def get_total_flights():
    result = db.session.execute("SELECT total_flights();")
    total_flights = result.fetchone()[0]
    return jsonify({"total_flights": total_flights})

#Procedure
@app.route('/api/update_food_stock', methods=['POST'])
def update_food_stock():
    data = request.get_json()
    item_name = data['item_name']
    new_stock = data['new_stock']

    db.session.execute("CALL update_food_stock(:item_name, :new_stock)", 
                       {"item_name": item_name, "new_stock": new_stock})
    db.session.commit()
    return jsonify({"message": f"Stock updated for {item_name}"})

#Trigger
@app.route('/api/flight_logs', methods=['GET'])
def get_flight_logs():
    logs = db.session.execute("SELECT * FROM FlightLogs ORDER BY log_time DESC").fetchall()
    log_list = [{"log_id": log[0], "message": log[1], "log_time": log[2].strftime("%Y-%m-%d %H:%M:%S")} for log in logs]
    return jsonify(log_list)


if __name__ == '__main__':
    # Create the tables in the database
    with app.app_context():
        db.create_all()

    # Run the Flask app
    app.run(debug=True)
