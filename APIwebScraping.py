from flask import Flask, request, jsonify
import json
import time
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def script(state, commodity, market):
    # URL of the website with the dropdown fields
    initial_url = "https://agmarknet.gov.in/SearchCmmMkt.aspx"
    
    try:
        # Use requests to get the initial page
        session = requests.Session()
        
        # Get the initial page to extract form data
        response = session.get(initial_url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract viewstate and other form fields
        viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
        viewstategenerator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
        eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']
        
        # Get commodity options
        commodity_dropdown = soup.find('select', {'id': 'ddlCommodity'})
        commodity_options = {option.text: option['value'] for option in commodity_dropdown.find_all('option')}
        
        # Get state options
        state_dropdown = soup.find('select', {'id': 'ddlState'})
        state_options = {option.text: option['value'] for option in state_dropdown.find_all('option')}
        
        # Get market options (will be populated after state selection)
        market_options = {}
        
        # Calculate the date 7 days ago from today
        today = datetime.now()
        desired_date = today - timedelta(days=7)
        date_str = desired_date.strftime('%d-%b-%Y')
        
        # First POST: Select commodity and state
        first_post_data = {
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstategenerator,
            '__EVENTVALIDATION': eventvalidation,
            'ddlCommodity': commodity_options.get(commodity, ''),
            'ddlState': state_options.get(state, ''),
            'txtDate': date_str,
            'btnGo': 'Go'
        }
        
        response = session.post(initial_url, data=first_post_data, timeout=30)
        response.raise_for_status()
        
        # Parse the response to get updated form fields and market options
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract updated form fields
        viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
        viewstategenerator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
        eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']
        
        # Get market options after state selection
        market_dropdown = soup.find('select', {'id': 'ddlMarket'})
        if market_dropdown:
            market_options = {option.text: option['value'] for option in market_dropdown.find_all('option')}
        
        # Second POST: Select market
        second_post_data = {
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstategenerator,
            '__EVENTVALIDATION': eventvalidation,
            'ddlCommodity': commodity_options.get(commodity, ''),
            'ddlState': state_options.get(state, ''),
            'ddlMarket': market_options.get(market, ''),
            'txtDate': date_str,
            'btnGo': 'Go'
        }
        
        response = session.post(initial_url, data=second_post_data, timeout=30)
        response.raise_for_status()
        
        # Parse the final response to extract data
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the data table
        table = soup.find('table', {'id': 'cphBody_GridPriceData'})
        if not table:
            return {"error": "Data table not found"}
        
        # Extract data from table
        data_list = []
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if cells:
                row_data = [cell.get_text(strip=True) for cell in cells]
                if row_data and len(row_data) > 1:  # Skip empty rows
                    data_list.append(row_data)
        
        # Process data (skip header rows)
        jsonList = []
        for i, row_data in enumerate(data_list[2:], 1):  # Start from index 2 to skip headers
            if len(row_data) >= 11:  # Ensure we have enough columns
                d = {}
                d["S.No"] = str(i)
                d["City"] = row_data[1] if len(row_data) > 1 else ""
                d["Commodity"] = row_data[3] if len(row_data) > 3 else ""
                d["Min Prize"] = row_data[6] if len(row_data) > 6 else ""
                d["Max Prize"] = row_data[7] if len(row_data) > 7 else ""
                d["Model Prize"] = row_data[8] if len(row_data) > 8 else ""
                d["Date"] = row_data[9] if len(row_data) > 9 else date_str
                jsonList.append(d)
        
        return jsonList
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to process data: {str(e)}"}

app = Flask(__name__)

@app.route('/', methods=['GET'])
def homePage():
    dataSet = {"Page": "Home Page navigate to request page", "Time Stamp": time.time()}
    return jsonify(dataSet)

@app.route('/request', methods=['GET'])
def requestPage():
    commodityQuery = request.args.get('commodity')
    stateQuery = request.args.get('state')
    marketQuery = request.args.get('market')

    if not commodityQuery or not stateQuery or not marketQuery:
        return jsonify({"error": "Missing query parameters"})

    try:
        json_data = json.dumps(script(stateQuery, commodityQuery, marketQuery), indent=4)
        return json_data
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)