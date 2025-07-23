from flask import Flask, render_template, request
import requests
import json
import os

app = Flask(__name__)

# 🌍 Load continent-based country data
def load_country_data():
    with open("static/countries.json", "r", encoding="utf-8") as file:
        return json.load(file)

# 🏅 Load national sport data
def load_national_sports():
    with open("static/national_sport.json", "r", encoding="utf-8") as file:
        return json.load(file)

country_data = load_country_data()
national_sports = load_national_sports()

def fetch_country_info(query):
    # Determine if it's a code or a name
    if len(query.strip()) in [2, 3]:
        url = f"https://restcountries.com/v3.1/alpha/{query}"
    else:
        url = f"https://restcountries.com/v3.1/name/{query}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if not data or (isinstance(data, dict) and data.get("status") == 404):
            return None

        country = data[0]
        code = country.get('cca2', '').upper()
        sport = national_sports.get(code, 'N/A')

        return {
            'name': country.get('name', {}).get('common', 'N/A'),
            'capital': country.get('capital', ['N/A'])[0],
            'region': country.get('region', 'N/A'),
            'population': country.get('population', 'N/A'),
            'currency': ', '.join(country.get('currencies', {}).keys()),
            'languages': ', '.join(country.get('languages', {}).values()),
            'flag': country.get('flags', {}).get('png', ''),
            'coatOfArms': country.get('coatOfArms', {}).get('png', ''),
            'mapLink': country.get('maps', {}).get('googleMaps', ''),
            'latlng': country.get('latlng', [0, 0]),
            'national_sport': sport
        }

    except Exception:
        return None

@app.route('/')
def index():
    return render_template('index.html', country_data=country_data)

@app.route('/country', methods=['POST'])
def get_country():
    user_input = request.form['country'].strip()
    country_info = fetch_country_info(user_input)

    if not country_info:
        error_msg = f'❌ Could not find country info for “{user_input}”. Please enter a valid country name or code.'
        return render_template('index.html', error=error_msg, country_data=country_data)

    return render_template('index.html', country=country_info, country_data=country_data)

@app.route('/country/<code>')
def country_by_code(code):
    country_info = fetch_country_info(code)

    if not country_info:
        error_msg = f'❌ Could not find country info for “{code}”. Please enter a valid country name or code.'
        return render_template('index.html', error=error_msg, country_data=country_data)

    return render_template('index.html', country=country_info, country_data=country_data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))  # Azure uses PORT env variable
    app.run(host='0.0.0.0', port=port, debug=True)
