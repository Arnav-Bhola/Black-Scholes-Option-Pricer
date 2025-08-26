import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os
import numpy as np
from .heatmap import Heatmap
from .enums import OptionType

pastel_r2g = LinearSegmentedColormap.from_list(
    "pastel_red_green", ["#ff9f9f", "#ffeeac", "#9eff9e"]
)

class HeatmapGenerator():
    def __init__(self,  strike_price, time_to_exp, risk_free_rate, min_stock_price, max_stock_price, min_volatility, max_volatility):
        self.strike_price = strike_price
        self.time_to_exp = time_to_exp
        self.risk_free_rate = risk_free_rate
        self.min_stock_price = min_stock_price
        self.max_stock_price = max_stock_price
        self.min_volatility = min_volatility
        self.max_volatility = max_volatility
        self.call_heatmap = Heatmap(self.strike_price, self.time_to_exp, self.risk_free_rate, self.min_stock_price, self.max_stock_price, self.min_volatility, self.max_volatility, OptionType.CALL_OPTION)
        self.put_heatmap = Heatmap(self.strike_price, self.time_to_exp, self.risk_free_rate, self.min_stock_price, self.max_stock_price, self.min_volatility, self.max_volatility, OptionType.PUT_OPTION)
    
    def compute_heatmaps(self):
        [self.stock_prices, self.volatilities] = self.call_heatmap.generate_grid()
        self.put_heatmap.generate_grid()

        self.call_heatmap_values = self.call_heatmap.compute_matrix()
        self.put_heatmap_values = self.put_heatmap.compute_matrix()
    
    def graph_call_heatmap(self):
        sns.set_theme(style="white")
        fig, ax = plt.subplots(figsize=(8, 6))

        sns.heatmap(
            self.call_heatmap_values,
            ax=ax,
            xticklabels=[round(s, 2) for s in self.stock_prices],
            yticklabels=[round(v, 2) for v in self.volatilities],
            cmap=pastel_r2g,
            annot=True,
            fmt=".2f",
            cbar=True,
            linecolor='gray'
        )
        ax.set_title("CALL", fontsize=14)
        ax.set_xlabel("Stock Price")
        ax.set_ylabel("Volatility")
        ax.tick_params(axis='x', rotation=0)
        ax.tick_params(axis='y', rotation=0)
        ax.xaxis.tick_bottom()
        ax.yaxis.tick_left()

        plt.tight_layout()
        self.call_graph = fig
        plt.close(fig)

    def graph_put_heatmap(self):
        sns.set_theme(style="white")
        fig, ax = plt.subplots(figsize=(8, 6))

        sns.heatmap(
            self.put_heatmap_values,
            ax=ax,
            xticklabels=[round(s, 2) for s in self.stock_prices],
            yticklabels=[round(v, 2) for v in self.volatilities],
            cmap=pastel_r2g,
            annot=True,
            fmt=".2f",
            cbar=True,
            linecolor='gray'
        )
        ax.set_title("PUT", fontsize=14)
        ax.set_xlabel("Stock Price")
        ax.set_ylabel("Volatility")

        ax.tick_params(axis='x', rotation=0)
        ax.tick_params(axis='y', rotation=0)
        ax.xaxis.tick_bottom()
        ax.yaxis.tick_left()

        plt.tight_layout()
        self.put_graph = fig
        plt.close(fig)

    def graph_heatmaps(self):
        self.graph_call_heatmap()
        self.graph_put_heatmap()

    def save_heatmaps(self, save_dir="heatmaps"):
        os.makedirs(save_dir, exist_ok=True)
        
        call_path = os.path.join(save_dir, "call_heatmap.png")
        put_path = os.path.join(save_dir, "put_heatmap.png")
        
        if hasattr(self, "call_graph"):
            self.call_graph.savefig(call_path, dpi=300)
        if hasattr(self, "put_graph"):
            self.put_graph.savefig(put_path, dpi=300)


if __name__ == "__main__":
    heatmap_generator = HeatmapGenerator(70.00, 1.10, 0.10, 79.94, 119.92, 0.17, 0.38)
    heatmap_generator.compute_heatmaps()
    heatmap_generator.graph_heatmaps()
    heatmap_generator.save_heatmaps()
