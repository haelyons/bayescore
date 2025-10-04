from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')

def compute_rating(r, w, g_mean, g_len):
    return ((r * w) + (g_mean * g_len)) / (w + g_len)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_rating', methods=['POST'])
def calculate_rating():
    restaurant_name = request.json.get('restaurant_name')
    
    if not GOOGLE_MAPS_API_KEY:
        return jsonify({'error': 'Google Maps API key is not set'}), 500
    
    if not restaurant_name:
        return jsonify({'error': 'Restaurant name is required'}), 400
    
    # First, search for the place
    search_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields=place_id&key={}'.format(restaurant_name, GOOGLE_MAPS_API_KEY)
    search_response = requests.get(search_url)
    search_data = search_response.json()
    
    if search_data['status'] != 'OK' or not search_data.get('candidates'):
        return jsonify({'error': 'Restaurant not found'}), 404
    
    place_id = search_data['candidates'][0]['place_id']
    
    # Now get the details for this place
    details_url = 'https://maps.googleapis.com/maps/api/place/details/json?place_id={}&fields=name,rating,user_ratings_total&key={}'.format(place_id, GOOGLE_MAPS_API_KEY)
    details_response = requests.get(details_url)
    details_data = details_response.json()
    
    if details_data['status'] == 'OK':
        place = details_data['result']
        name = place.get('name', 'Unknown')
        original_rating = place.get('rating')
        num_ratings = place.get('user_ratings_total')
        
        if original_rating is None or num_ratings is None:
            return jsonify({'error': 'Rating information not available'}), 404
        
        # Calculate new rating
        r = 2  # Default rating
        w = 3  # Weight
        recalculated_rating = compute_rating(r, w, original_rating, num_ratings)
        
        return jsonify({
            'name': name,
            'original_rating': original_rating,
            'recalculated_rating': round(recalculated_rating, 2)
        })
    else:
        return jsonify({'error': 'API Error: {}'.format(details_data.get('status', 'Unknown error'))}), 500

if __name__ == '__main__':
    if not GOOGLE_MAPS_API_KEY:
        print("WARNING: GOOGLE_MAPS_API_KEY environment variable is not set!")
    app.run(debug=True)