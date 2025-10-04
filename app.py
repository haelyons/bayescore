import gradio as gr
import requests
import os

GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')

def compute_rating(r, w, g_mean, g_len):
    return ((r * w) + (g_mean * g_len)) / (w + g_len)

def get_restaurant_rating(restaurant_name, r_value, w_value, user_api_key):
    api_key = user_api_key.strip() if user_api_key and user_api_key.strip() else GOOGLE_MAPS_API_KEY
    
    if not api_key:
        return {
            "error": "❌ No API key provided",
            "api_status": "Missing API key",
            "name": "", "original": "", "weighted": "", "num_reviews": ""
        }
    
    if not restaurant_name or restaurant_name.strip() == "":
        return {
            "error": "Please enter a restaurant name",
            "api_status": "Ready",
            "name": "", "original": "", "weighted": "", "num_reviews": ""
        }
    
    try:
        search_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
        search_params = {
            'input': restaurant_name,
            'inputtype': 'textquery',
            'fields': 'place_id',
            'key': api_key
        }
        search_response = requests.get(search_url, params=search_params)
        search_data = search_response.json()
        
        if search_data['status'] == 'REQUEST_DENIED':
            error_msg = search_data.get('error_message', 'API request denied')
            return {
                "error": f"❌ **API Error**: {error_msg}",
                "api_status": f"Status: REQUEST_DENIED | Check API key and Places API enablement",
                "name": "", "original": "", "weighted": "", "num_reviews": ""
            }
        
        if search_data['status'] == 'INVALID_REQUEST':
            return {
                "error": f"❌ **Invalid Request**",
                "api_status": f"Status: INVALID_REQUEST | Check API parameters",
                "name": "", "original": "", "weighted": "", "num_reviews": ""
            }
        
        if search_data['status'] == 'OVER_QUERY_LIMIT':
            return {
                "error": f"❌ **Quota Exceeded**",
                "api_status": f"Status: OVER_QUERY_LIMIT | API quota exceeded for this key",
                "name": "", "original": "", "weighted": "", "num_reviews": ""
            }
        
        if search_data['status'] != 'OK' or not search_data.get('candidates'):
            return {
                "error": f"'{restaurant_name}' not found",
                "api_status": f"Status: {search_data['status']} | ZERO_RESULTS",
                "name": "", "original": "", "weighted": "", "num_reviews": ""
            }
        
        place_id = search_data['candidates'][0]['place_id']
        
        details_url = 'https://maps.googleapis.com/maps/api/place/details/json'
        details_params = {
            'place_id': place_id,
            'fields': 'name,rating,user_ratings_total',
            'key': api_key
        }
        details_response = requests.get(details_url, params=details_params)
        details_data = details_response.json()
        
        if details_data['status'] != 'OK':
            return {
                "error": f"❌ **Details API Error**",
                "api_status": f"Status: {details_data['status']} | {details_data.get('error_message', 'Unknown error')}",
                "name": "", "original": "", "weighted": "", "num_reviews": ""
            }
        
        place = details_data['result']
        name = place.get('name', 'Unknown')
        original_rating = place.get('rating')
        num_ratings = place.get('user_ratings_total')
        
        if original_rating is None or num_ratings is None:
            return {
                "error": f"No ratings available for {name}",
                "api_status": "Status: OK | No rating data",
                "name": name, "original": "", "weighted": "", "num_reviews": ""
            }
        
        weighted_rating = compute_rating(r_value, w_value, original_rating, num_ratings)
        
        return {
            "error": "",
            "api_status": "✓ Status: OK",
            "name": name,
            "original": f"{original_rating}",
            "weighted": f"{weighted_rating:.2f}",
            "num_reviews": f"{num_ratings:,}"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"❌ **Network Error**: {str(e)}",
            "api_status": "Connection failed",
            "name": "", "original": "", "weighted": "", "num_reviews": ""
        }
    except Exception as e:
        return {
            "error": f"❌ **Error**: {str(e)}",
            "api_status": "Exception occurred",
            "name": "", "original": "", "weighted": "", "num_reviews": ""
        }

def process_restaurant(restaurant_name, r_value, w_value, user_api_key):
    result = get_restaurant_rating(restaurant_name, r_value, w_value, user_api_key)
    
    if result["error"]:
        return result["api_status"], result["error"], "", "", ""
    
    return (
        result["api_status"],
        "",
        result["name"],
        f"{result['original']}★ ({result['num_reviews']} reviews)",
        f"{result['weighted']}★"
    )

with gr.Blocks(title="Bayescore") as demo:
    gr.Markdown("# 🍽️ Bayescore")
    gr.Markdown("Bayesian restaurant ratings that account for sample size")
    
    with gr.Accordion("API Key", open=not GOOGLE_MAPS_API_KEY):
        api_key_input = gr.Textbox(
            label="Google Maps API Key",
            placeholder="Enter API key or set GOOGLE_MAPS_API_KEY env var",
            type="password"
        )
    
    api_status = gr.Markdown(
        "✓ API key configured" if GOOGLE_MAPS_API_KEY else "⚠️ No API key"
    )
    
    restaurant_input = gr.Textbox(
        label="Restaurant Name",
        placeholder="e.g., 'Joe's Pizza Brooklyn'",
        elem_id="restaurant-search"
    )
    
    # Add Google Places Autocomplete to the textbox
    if GOOGLE_MAPS_API_KEY:
        gr.HTML(f"""
        <script src="https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_API_KEY}&libraries=places"></script>
        <script>
        function initAutocomplete() {{
            const input = document.querySelector('#restaurant-search input');
            if (!input) {{
                setTimeout(initAutocomplete, 100);
                return;
            }}
            const autocomplete = new google.maps.places.Autocomplete(input, {{
                types: ['establishment'],
                fields: ['name']
            }});
        }}
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', initAutocomplete);
        }} else {{
            initAutocomplete();
        }}
        </script>
        """)
    
    error_output = gr.Markdown()
    
    with gr.Row():
        r_slider = gr.Slider(
            minimum=1, maximum=5, value=2.5, step=0.1,
            label="Prior Rating (R)",
            info="Expected rating with no reviews"
        )
        w_slider = gr.Slider(
            minimum=0, maximum=50, value=5, step=1,
            label="Prior Weight (W)",
            info="Strength of prior belief"
        )
    
    with gr.Row():
        restaurant_name = gr.Textbox(label="Restaurant", interactive=False)
        google_rating = gr.Textbox(label="Google Rating", interactive=False)
        bayesian_rating = gr.Textbox(label="Bayesian Rating", interactive=False)
    
    restaurant_input.submit(
        fn=process_restaurant,
        inputs=[restaurant_input, r_slider, w_slider, api_key_input],
        outputs=[api_status, error_output, restaurant_name, google_rating, bayesian_rating]
    )
    
    r_slider.change(
        fn=process_restaurant,
        inputs=[restaurant_input, r_slider, w_slider, api_key_input],
        outputs=[api_status, error_output, restaurant_name, google_rating, bayesian_rating]
    )
    
    w_slider.change(
        fn=process_restaurant,
        inputs=[restaurant_input, r_slider, w_slider, api_key_input],
        outputs=[api_status, error_output, restaurant_name, google_rating, bayesian_rating]
    )

if __name__ == "__main__":
    demo.launch()