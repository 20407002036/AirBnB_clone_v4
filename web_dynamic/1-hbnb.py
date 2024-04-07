from flask import Flask, render_template
import uuid

from models import storage
from models.amenity import Amenity
from models.place import Place
from models.state import State
from models.user import User

app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()

@app.route('/1-hbnb', strict_slashes=False)
def hbnb():
    """ HBNB is alive! """
    states = storage.all(State)  # Retrieve all states
    states_dict = {}  # Initialize an empty dictionary to hold states and cities
    for state in states.values():
        cities = state.cities  # Get the cities associated with the state
        states_dict[state] = cities  # Add state and its cities to the dictionary

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)
    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)
    users = dict([user.id, "{} {}".format(user.first_name, user.last_name)]
                 for user in storage.all('User').values())

    ctxt = {
        'states': states_dict,  # Pass the dictionary instead of a list
        'amenities': amenities,
        'places': places,
        'users': users,
        'cache_id': str(uuid.uuid4())
    }
    return render_template('1-hbnb.html', **ctxt)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
