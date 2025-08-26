import os
import yfinance as yf
import pandas as pd

class DataLoader():
    def __init__(self, ticker, cache_dir="data"):
        self.ticker = ticker
        self.cache_dir = cache_dir
        self.data = None

        os.makedirs(self.cache_dir, exist_ok=True)
        self.file_path = os.path.join(self.cache_dir, f"{self.ticker}_data.csv")

    def fetch_data(self, period='max'):
        ticker_obj = yf.Ticker(self.ticker)
        unfiltered_data = ticker_obj.history(period=period)
        filtered_data = unfiltered_data[['Close']]
        filtered_data.sort_index(inplace=True)
        self.data = filtered_data
        return filtered_data

    def get_data(self):
        if self.data is not None:
            return self.data
        else:
            raise ValueError("Data not fetched yet. Call fetch_data() first.")
    
    def save_to_csv(self):
        if self.data is None:
            raise ValueError("No data to save. Fetch or load data first.")
        self.data.to_csv(self.file_path)
        print(f"Data saved to {self.file_path}")

    def load_from_csv(self) -> pd.DataFrame:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"No cached file found at {self.file_path}")
        self.data = pd.read_csv(self.file_path, index_col='Date', parse_dates=True)
        self.data.sort_index(inplace=True)  # Ensure chronological order
        return self.data


if __name__ == "__main__":
    data_loader = DataLoader(ticker='AAPL')
    df = data_loader.fetch_data()
    data_loader.save_to_csv()
    df2 = data_loader.load_from_csv()
    print(df2.tail())