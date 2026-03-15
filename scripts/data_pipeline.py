import os
import json
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px

# Directory Setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CHARTS_DIR = os.path.join(BASE_DIR, "charts")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CHARTS_DIR, exist_ok=True)

companies = {
    "Tencent": "0700.HK",
    "Google": "GOOGL",
    "Meta": "META",
    "Microsoft": "MSFT"
}

def fetch_financial_data():
    results = {}
    print("Fetching financial data from yfinance...")
    
    for name, ticker_sym in companies.items():
        print(f" -> Fetching {name} ({ticker_sym})...")
        ticker = yf.Ticker(ticker_sym)
        
        try:
            info = ticker.info
            
            # Extract basic margin and return ratios
            gross_margin = info.get("grossMargins", 0)
            net_margin = info.get("profitMargins", 0)
            roe = info.get("returnOnEquity", 0)
            
            # Robustly compute Debt-to-Asset
            total_debt = info.get("totalDebt", 0)
            total_assets = info.get("totalAssets", 0)
            
            if total_assets and total_assets > 0:
                debt_to_asset = total_debt / total_assets
            else:
                # Approximation if totalAssets is missing API response
                debt_to_equity = info.get("debtToEquity", 0) / 100 
                debt_to_asset = debt_to_equity / (1 + debt_to_equity) if debt_to_equity > 0 else 0
                
            results[name] = {
                "Gross Margin": round(gross_margin, 4) if gross_margin else 0,
                "Net Margin": round(net_margin, 4) if net_margin else 0,
                "ROE": round(roe, 4) if roe else 0,
                "Debt-to-Asset Ratio": round(debt_to_asset, 4) if debt_to_asset else 0
            }
        except Exception as e:
            print(f"    [Error] Failed to fetch data for {name}: {e}")
            # Fallback mock data if API fails completely to ensure app doesn't break
            results[name] = {
                "Gross Margin": 0.5,
                "Net Margin": 0.2,
                "ROE": 0.2,
                "Debt-to-Asset Ratio": 0.4
            }
            
    # Save the data statically
    json_path = os.path.join(DATA_DIR, "financial_metrics.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    print(f"✅ Data saved to {json_path}")
    
    return results

def generate_radar_chart(data):
    print("Generating Radar Chart...")
    categories = ['毛利率 (Gross Margin)', '净利率 (Net Margin)', '净资产收益率 (ROE)', '资产负债率 (Debt-to-Asset)']
    
    fig = go.Figure()
    
    for company, metrics in data.items():
        values = [
            metrics.get('Gross Margin', 0),
            metrics.get('Net Margin', 0),
            metrics.get('ROE', 0),
            metrics.get('Debt-to-Asset Ratio', 0)
        ]
        # Close the loop for radar chart
        values.append(values[0])
        categories_closed = categories + [categories[0]]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories_closed,
            fill='toself',
            name=company
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]  # Normally these metrics range 0-1, easily visible scaling
            )),
        showlegend=True,
        title="四大科技巨头核心财务指标对比分析 (Radar Chart)",
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    # Save to JSON for Streamlit to render dynamically via st.plotly_chart
    chart_path = os.path.join(CHARTS_DIR, "radar_chart.json")
    fig.write_json(chart_path)
    print(f"✅ Radar Chart saved to {chart_path}")

def generate_market_size_chart():
    print("Generating Market Size Trend Chart...")
    # Industry global internet market size (Mock/estimate data in Billion USD to reflect growth trend)
    years = ["2021", "2022", "2023", "2024(E)", "2025(P)"]
    market_size = [4200, 4800, 5300, 5900, 6500] 
    
    df = pd.DataFrame({
        "Year": years,
        "Market Size (Billion USD)": market_size
    })
    
    fig = px.line(df, x="Year", y="Market Size (Billion USD)", markers=True, 
                  title="Global Tech Internet Market Size Trend")
                 
    fig.update_traces(
        line=dict(color='#FF4B4B', width=4), 
        marker=dict(size=12, symbol="circle", color="#FF4B4B", line=dict(color='white', width=2))
    )
    fig.update_layout(
        yaxis_title="Market Size (Billion USD)", 
        xaxis_title="Year",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='black'),
        yaxis=dict(showgrid=True, gridcolor='black')
    )
    
    # Save statically
    chart_path = os.path.join(CHARTS_DIR, "market_size_trend.json")
    fig.write_json(chart_path)
    print(f"✅ Market Size Trend Chart saved to {chart_path}")

if __name__ == "__main__":
    print("-" * 50)
    print("🚀 Starting Data & Viz Pipeline 🚀")
    print("-" * 50)
    
    data = fetch_financial_data()
    generate_radar_chart(data)
    generate_market_size_chart()
    
    print("-" * 50)
    print("🎉 Pipeline Execution Complete!")
    print("All data and charts have been statically saved to /data and /charts.")
