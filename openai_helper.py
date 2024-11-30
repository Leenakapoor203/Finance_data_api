import openai
import json
import pandas as pd
import os
from dotenv import load_dotenv
import yfinance as yf

load_dotenv()
api_key=os.getenv("openai_key")

openai.api_key = api_key

def extract_financial_data(text):
    prompt = get_prompt_financial() + text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user","content": prompt}]
    )
    content = response.choices[0]['message']['content']

    try:
        data = json.loads(content)
        return pd.DataFrame(data.items(), columns=["Measure", "Value"])

    except (json.JSONDecodeError, IndexError):
        pass

    return pd.DataFrame({
        "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
        "Value": ["", "", "", "", ""]
    })



def get_prompt_financial():
    return '''Please retrieve company name, revenue, net income and earnings per share (a.k.a. EPS)
    from the following news article. If you can't find the information from this article 
    then return "Not found". Do not make things up.    
    Then retrieve a stock symbol corresponding to that company. For this you can use
    your general knowledge (it doesn't have to be from this article). Always return your
    response as a valid JSON string. The format of that string should be this, 
    {
        "Company Name": "Walmart",
        "Stock Symbol": "WMT",
        "Revenue": "12.34 million",
        "Net Income": "34.78 million",
        "EPS": "2.1 $"
    }
    News Article:
    ============

    '''

if __name__ == '__main__':
    text = '''
    Tesla's Earning news in text format: Tesla's earning this quarter blew all the estimates. 
    They reported 4.5 billion $ profit against a revenue of 30 billion $. 
    Their earnings per share was 2.3 $
    '''
    df = extract_financial_data(text)

    print(df.to_string())



def fetch_company_financial_data(company_name):
    try:
        # Use yfinance to search and fetch the company's data
        ticker = yf.Ticker(company_name)
        info = ticker.info

        # Extract relevant information
        data = {
            "Company Name": info.get("shortName", "Not found"),
            "Stock Symbol": info.get("symbol", "Not found"),
            "Revenue": f"{info.get('totalRevenue', 'Not found'):,}" if info.get('totalRevenue') else "Not found",
            "Net Income": f"{info.get('netIncomeToCommon', 'Not found'):,}" if info.get('netIncomeToCommon') else "Not found",
            "EPS": f"{info.get('trailingEps', 'Not found')}" if info.get('trailingEps') else "Not found",
        }

        return pd.DataFrame(data.items(), columns=["Measure", "Value"])

    except Exception as e:
        print(f"Error fetching data for {company_name}: {e}")
        return pd.DataFrame({
            "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
            "Value": ["Not found", "Not found", "Not found", "Not found", "Not found"]
        })
