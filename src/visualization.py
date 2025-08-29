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
    def __init__(self,  strike_price, time_to_exp, risk_free_rate, min_stock_price, max_stock_price, min_volatility, max_volatility, base_call_price=0, base_put_price=0):
        self.strike_price = strike_price
        self.time_to_exp = time_to_exp
        self.risk_free_rate = risk_free_rate
        self.min_stock_price = min_stock_price
        self.max_stock_price = max_stock_price
        self.min_volatility = min_volatility
        self.max_volatility = max_volatility
        self.base_call_price = base_call_price
        self.base_put_price = base_put_price
        self.call_heatmap = Heatmap(self.strike_price, self.time_to_exp, self.risk_free_rate, self.min_stock_price, self.max_stock_price, self.min_volatility, self.max_volatility, OptionType.CALL_OPTION, base_price=0)
        self.put_heatmap = Heatmap(self.strike_price, self.time_to_exp, self.risk_free_rate, self.min_stock_price, self.max_stock_price, self.min_volatility, self.max_volatility, OptionType.PUT_OPTION, base_price=0)
        self.call_pnl_heatmap = Heatmap(self.strike_price, self.time_to_exp, self.risk_free_rate, self.min_stock_price, self.max_stock_price, self.min_volatility, self.max_volatility, OptionType.CALL_OPTION, base_price=base_call_price, pnl=True)
        self.put_pnl_heatmap = Heatmap(self.strike_price, self.time_to_exp, self.risk_free_rate, self.min_stock_price, self.max_stock_price, self.min_volatility, self.max_volatility, OptionType.PUT_OPTION, base_price=base_put_price, pnl=True)
    
    def compute_heatmaps(self):
        [self.stock_prices, self.volatilities] = self.call_heatmap.generate_grid()
        self.put_heatmap.generate_grid()
        self.call_pnl_heatmap.generate_grid()
        self.put_pnl_heatmap.generate_grid()

        self.call_heatmap_values = self.call_heatmap.compute_matrix()
        self.put_heatmap_values = self.put_heatmap.compute_matrix()
        self.call_pnl_heatmap_values = self.call_pnl_heatmap.compute_matrix()
        self.put_pnl_heatmap_values = self.put_pnl_heatmap.compute_matrix()

    def _graph_heatmap(self, values, title, attr_name):
        sns.set_theme(style="white")
        fig, ax = plt.subplots(figsize=(8, 6))

        sns.heatmap(
            values,
            ax=ax,
            xticklabels=[round(s, 2) for s in self.stock_prices],
            yticklabels=[round(v, 2) for v in self.volatilities],
            cmap=pastel_r2g,
            annot=True,
            fmt=".2f",
            cbar=True,
            linecolor='gray'
        )
        ax.set_title(title, fontsize=14)
        ax.set_xlabel("Stock Price")
        ax.set_ylabel("Volatility")
        ax.tick_params(axis='x', rotation=0)
        ax.tick_params(axis='y', rotation=0)
        ax.xaxis.tick_bottom()
        ax.yaxis.tick_left()

        plt.tight_layout()
        setattr(self, attr_name, fig)
        plt.close(fig)

    def graph_all_heatmaps(self):
        self._graph_heatmap(self.call_heatmap_values, "CALL", "call_graph")
        self._graph_heatmap(self.put_heatmap_values, "PUT", "put_graph")
        self._graph_heatmap(self.call_pnl_heatmap_values, "CALL P&L Ratio", "call_pnl_graph")
        self._graph_heatmap(self.put_pnl_heatmap_values, "PUT P&L Ratio", "put_pnl_graph")

    def save_heatmaps(self, save_dir="heatmaps"):
        os.makedirs(save_dir, exist_ok=True)

        save_map = {
            "call_graph": "call_heatmap.png",
            "put_graph": "put_heatmap.png",
            "call_pnl_graph": "call_pnl_heatmap.png",
            "put_pnl_graph": "put_pnl_heatmap.png",
        }

        for attr, filename in save_map.items():
            if hasattr(self, attr):
                fig = getattr(self, attr)
                fig.savefig(os.path.join(save_dir, filename), dpi=300)



if __name__ == "__main__":
    heatmap_generator = HeatmapGenerator(70.00, 1.10, 0.10, 79.94, 119.92, 0.17, 0.38, 4.581680167540007, 6.989220930514925)
    heatmap_generator.compute_heatmaps()
    heatmap_generator.graph_all_heatmaps()
    heatmap_generator.save_heatmaps()
