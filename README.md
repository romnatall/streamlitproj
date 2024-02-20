
# Stock and Tip Analysis App

This is a simple Python web application built using Streamlit for analyzing stock prices, tips, and playing a game of Rock-Paper-Scissors. The app utilizes various libraries, including yfinance for stock data, plotly for visualizations, and a custom machine learning model for the game.

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/romnatall/streamlitproj.git
   ```

2. Change into the project directory:

   ```bash
   cd streamlitproj
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit app using the following command:

```bash
streamlit run site.py 
```

This will launch a local web server, and you can access the app in your web browser at `http://localhost:8506` or else. The app has three main tabs:

### Stock Prices

- Displays closing prices and volume of Apple stock.
- Uses yfinance library for fetching stock data.
- Visualizes data using Plotly charts.

### Tips Analysis

- Reads tip data from a CSV file (`datasets/tips.csv`).
- Groups data by time and displays bar charts.
- Calculates the percentage difference in tips relative to the total bill.

### Rock-Paper-Scissors Game

- Implements a simple Rock-Paper-Scissors game.
- Utilizes a custom machine learning model for predicting computer choices.
- Keeps track of wins, losses, draws, and win rate.
- Displays images for user and computer choices.



## Credits

- [Streamlit](https://streamlit.io/) - The main web application framework.
- [yfinance](https://pypi.org/project/yfinance/) - Used for fetching stock data.
- [Plotly](https://plotly.com/) - Library for creating interactive visualizations.
- [Pandas](https://pandas.pydata.org/) - Data manipulation and analysis.
- [Pillow (PIL)](https://pillow.readthedocs.io/en/stable/) - Image processing library.

