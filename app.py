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
            "error": "No API key. Either enter one above or ask the Space owner to configure GOOGLE_MAPS_API_KEY",
            "name": "", "original": "", "weighted": "", "num_reviews": "", "explanation": ""
        }
    
    if not restaurant_name or restaurant_name.strip() == "":
        return {
            "error": "Please enter a restaurant name",
            "name": "", "original": "", "weighted": "", "num_reviews": "", "explanation": ""
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
            return {
                "error": "API key invalid or Places API not enabled",
                "name": "", "original": "", "weighted": "", "num_reviews": "", "explanation": ""
            }
        
        if search_data['status'] != 'OK' or not search_data.get('candidates'):
            return {
                "error": f"'{restaurant_name}' not found. Try being more specific (include city)",
                "name": "", "original": "", "weighted": "", "num_reviews": "", "explanation": ""
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
                "error": f"API Error: {details_data.get('status', 'Unknown')}",
                "name": "", "original": "", "weighted": "", "num_reviews": "", "explanation": ""
            }
        
        place = details_data['result']
        name = place.get('name', 'Unknown')
        original_rating = place.get('rating')
        num_ratings = place.get('user_ratings_total')
        
        if original_rating is None or num_ratings is None:
            return {
                "error": f"No rating data available for {name}",
                "name": name, "original": "", "weighted": "", "num_reviews": "", "explanation": ""
            }
        
        weighted_rating = compute_rating(r_value, w_value, original_rating, num_ratings)
        
        explanation = f"""
**Calculation:**

`({r_value} × {w_value} + {original_rating} × {num_ratings}) / ({w_value} + {num_ratings}) = {weighted_rating:.2f}★`

This assumes {w_value} prior ratings of {r_value}★ exist before considering the {num_ratings:,} actual reviews.

With few reviews, the score pulls toward {r_value}★ (your prior belief). With many reviews, actual ratings dominate the score. This prevents misleading ratings from small sample sizes.
"""        
        return {
            "error": "",
            "name": name,
            "original": f"{original_rating}★",
            "weighted": f"{weighted_rating:.2f}★",
            "num_reviews": f"{num_ratings:,} reviews",
            "explanation": explanation
        }
        
    except Exception as e:
        return {
            "error": f"Error: {str(e)}",
            "name": "", "original": "", "weighted": "", "num_reviews": "", "explanation": ""
        }

def process_restaurant(restaurant_name, r_value, w_value, user_api_key):
    result = get_restaurant_rating(restaurant_name, r_value, w_value, user_api_key)
    
    if result["error"]:
        return result["error"], "", "", "", "", result["explanation"] if result["explanation"] else ""
    
    return "", result["name"], result["original"], result["weighted"], result["num_reviews"], result["explanation"]

with gr.Blocks(title="Bayesian Restaurant Ratings", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🍽️ Bayescore
    
    Recalculates restaurant ratings using a Bayesian approach.
    
    We treat each restaurant as if it started with **W** prior ratings of **R** stars, then factor in actual reviews.
    This prevents edge cases like "1 perfect review = 5★" or brand new places being unfairly judged.
    """)
    
    with gr.Accordion("API Key", open=not GOOGLE_MAPS_API_KEY):
        if GOOGLE_MAPS_API_KEY:
            gr.Markdown("API key found")
        else:
            gr.Markdown("""
            No API key in environment. You can:
            1. Enter your key below
            2. Fork this Space and add `GOOGLE_MAPS_API_KEY` in Settings → Secrets
            
            [Get an API key →](https://console.cloud.google.com) (enable Places API)
            """)
        
        api_key_input = gr.Textbox(
            label="Google Maps API Key (optional)",
            placeholder="Paste API key here",
            type="password",
            value="",
            info="Never stored"
        )
    
    with gr.Row():
        with gr.Column(scale=2):
            restaurant_input = gr.Textbox(
                label="Restaurant Name",
                placeholder="e.g., 'Joe's Pizza Brooklyn' or 'Noma Copenhagen'",
                lines=1
            )
            
            with gr.Row():
                r_slider = gr.Slider(
                    minimum=1,
                    maximum=5,
                    value=2.5,
                    step=0.1,
                    label="R - Prior Rating",
                    info="Your default belief about an unrated place"
                )
                
                w_slider = gr.Slider(
                    minimum=0,
                    maximum=50,
                    value=5,
                    step=1,
                    label="W - Prior Weight",
                    info="How many prior ratings worth of confidence"
                )
            
            submit_btn = gr.Button("Calculate Rating", variant="primary", size="lg")
    
    error_output = gr.Markdown(visible=True)
    
    with gr.Row():
        name_output = gr.Textbox(label="Restaurant", interactive=False)
    
    with gr.Row():
        with gr.Column():
            original_output = gr.Textbox(label="Google Rating", interactive=False)
        with gr.Column():
            weighted_output = gr.Textbox(label="Bayesian Rating", interactive=False)
        with gr.Column():
            reviews_output = gr.Textbox(label="Review Count", interactive=False)
    
    explanation_output = gr.Markdown()
    
    gr.Markdown("""
    ---
    ### Parameter Guide:
    
    **R (Prior Rating):** What score would you assume for a place with zero reviews?
    - Don't use the minimum (1★) - places with terrible reviews should score worse than no-review places
    - Try the median of all established places in your area (often 3-4★)
    - Lower = more skeptical, Higher = more optimistic
    
    **W (Prior Weight):** How strongly should this prior influence the final score?
    - Higher W = prior dominates (useful when reviews are noisy/spammy)
    - Lower W = actual reviews dominate faster (useful when reviews are reliable)
    - Rule of thumb: W should be between C/20 and C/5, where C = typical review count
    - W=0 ignores prior entirely, W=∞ ignores actual reviews
    
    ### Examples:
    - **Conservative** (R=3.5, W=20): Heavily weights your prior, slow to trust extreme ratings
    - **Balanced** (R=2.5, W=5): Moderate influence, adjusts reasonably with reviews
    - **Trusting** (R=3, W=2): Mostly trusts actual ratings, minimal adjustment
    """)
    
    submit_btn.click(
        fn=process_restaurant,
        inputs=[restaurant_input, r_slider, w_slider, api_key_input],
        outputs=[error_output, name_output, original_output, weighted_output, reviews_output, explanation_output]
    )
    
    restaurant_input.submit(
        fn=process_restaurant,
        inputs=[restaurant_input, r_slider, w_slider, api_key_input],
        outputs=[error_output, name_output, original_output, weighted_output, reviews_output, explanation_output]
    )

if __name__ == "__main__":
    demo.launch()