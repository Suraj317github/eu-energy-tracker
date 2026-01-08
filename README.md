# 🏆 EU Renewable Energy Tracker

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://eu-energy-tracker.streamlit.app/)

A Streamlit dashboard that tracks and visualizes the adoption of renewable energy across European countries. This application fetches official data directly from **Eurostat** to generate real-time leaderboards and trend analysis.

🔗 **[Click here to view the Live App](https://eu-energy-tracker.streamlit.app/)**

## 📊 Features

* **Top 10 Leaderboard:** Instantly identifies which European nations are leading in Green Energy.
* **Sector Analysis:** Filter data by specific sectors:
    * ⚡ Electricity
    * 🚗 Transport
    * 🔥 Heating & Cooling
* **Trend Visualization:** Interactive line charts showing the growth of the top performers over the last 15 years.
* **Smart Filtering:** Automatically excludes aggregate data (like "EU27" averages) to focus on individual country performance.
* **Raw Data Explorer:** Full access to the underlying dataset for deep-dive analysis.

## 🛠️ Built With

* **Python 3.9+**
* **Streamlit:** For the web interface and interactivity.
* **Eurostat Library:** For fetching official EU datasets programmatically.
* **Plotly:** For interactive, hoverable charts.
* **Pandas:** For data manipulation and cleaning.

## 📂 Data Source

* **Source:** [Eurostat Database](https://ec.europa.eu/eurostat/data/database)
* **Dataset Code:** `nrg_ind_ren` (Share of energy from renewable sources)
* **Unit:** Percentage (%)
* **Update Frequency:** Annual

## 🚀 How to Run Locally

If you want to run this dashboard on your own machine:

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Suraj317github/eu-energy-tracker.git
    cd eu-energy-tracker
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the app**
    ```bash
    streamlit run app.py
    ```

## 📜 License

This project is open-source and available under the MIT License.
