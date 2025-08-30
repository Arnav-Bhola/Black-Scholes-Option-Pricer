import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os
import numpy as np
from .heatmap import Heatmap
from .enums import OptionType

# Custom red -> yellow -> green colormap for P&L style visualization
pastel_r2g = LinearSegmentedColormap.from_list(
    "pastel_red_green", ["#ff9f9f", "#ffeeac", "#9eff9e"]
)

class HeatmapGenerator():
    """
    Generates and visualizes option price and P&L heatmaps.

    Attributes:
        strike_price (float): Strike/exercise price of the option.
        time_to_exp (float): Time to expiration (in years).
        risk_free_rate (float): Annual risk-free interest rate (as a decimal).
        min_stock_price (float): Minimum stock price for grid.
        max_stock_price (float): Maximum stock price for grid.
        min_volatility (float): Minimum volatility for grid.
        max_volatility (float): Maximum volatility for grid.
        base_call_price (float): Base price for call P&L calculations.
        base_put_price (float): Base price for put P&L calculations.
        call_heatmap, put_heatmap (Heatmap): Heatmap objects for option prices.
        call_pnl_heatmap, put_pnl_heatmap (Heatmap): Heatmap objects for P&L.
    """

    def __init__(self,  strike_price, time_to_exp, risk_free_rate, min_stock_price, max_stock_price, min_volatility, max_volatility, base_call_price=0, base_put_price=0):
        """Initialize heatmap generator with pricing parameters."""
        self.strike_price = strike_price
        self.time_to_exp = time_to_exp
        self.risk_free_rate = risk_free_rate
        self.min_stock_price = min_stock_price
        self.max_stock_price = max_stock_price
        self.min_volatility = min_volatility
        self.max_volatility = max_volatility
        self.base_call_price = base_call_price
        self.base_put_price = base_put_price

        # Heatmaps for call/put pricing and P&L
        self.call_heatmap = Heatmap(self.strike_price, self.time_to_exp, self.risk_free_rate, self.min_stock_price, self.max_stock_price, self.min_volatility, self.max_volatility, OptionType.CALL_OPTION, base_price=0)
        self.put_heatmap = Heatmap(self.strike_price, self.time_to_exp, self.risk_free_rate, self.min_stock_price, self.max_stock_price, self.min_volatility, self.max_volatility, OptionType.PUT_OPTION, base_price=0)
        self.call_pnl_heatmap = Heatmap(self.strike_price, self.time_to_exp, self.risk_free_rate, self.min_stock_price, self.max_stock_price, self.min_volatility, self.max_volatility, OptionType.CALL_OPTION, base_price=base_call_price, pnl=True)
        self.put_pnl_heatmap = Heatmap(self.strike_price, self.time_to_exp, self.risk_free_rate, self.min_stock_price, self.max_stock_price, self.min_volatility, self.max_volatility, OptionType.PUT_OPTION, base_price=base_put_price, pnl=True)
    
    def compute_heatmaps(self):
        """
        Compute option price and P&L heatmap matrices.

        Sets:
            self.stock_prices (ndarray): Grid of stock prices.
            self.volatilities (ndarray): Grid of volatilities.
            self.call_heatmap_values, self.put_heatmap_values (ndarray): Option price matrices.
            self.call_pnl_heatmap_values, self.put_pnl_heatmap_values (ndarray): P&L matrices.
        """
        # Generate shared grids for stock prices and volatilities
        [self.stock_prices, self.volatilities] = self.call_heatmap.generate_grid()
        self.put_heatmap.generate_grid()
        self.call_pnl_heatmap.generate_grid()
        self.put_pnl_heatmap.generate_grid()

        # Compute heatmap values
        self.call_heatmap_values = self.call_heatmap.compute_matrix()
        self.put_heatmap_values = self.put_heatmap.compute_matrix()
        self.call_pnl_heatmap_values = self.call_pnl_heatmap.compute_matrix()
        self.put_pnl_heatmap_values = self.put_pnl_heatmap.compute_matrix()

    def _graph_heatmap(self, values, title, attr_name):
        """
        Internal method: Create a heatmap figure and attach it as an attribute.

        Args:
            values (ndarray): Heatmap values to visualize.
            title (str): Title for the plot.
            attr_name (str): Attribute name to assign the figure to.
        """

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
        setattr(self, attr_name, fig)  # Store figure as attribute
        plt.close(fig)  # Prevents immediate display

    def graph_all_heatmaps(self):
        """
        Generate figures for all computed heatmaps.

        Sets:
            self.call_graph, self.put_graph, self.call_pnl_graph, self.put_pnl_graph
        """
        self._graph_heatmap(self.call_heatmap_values, "CALL", "call_graph")
        self._graph_heatmap(self.put_heatmap_values, "PUT", "put_graph")
        self._graph_heatmap(self.call_pnl_heatmap_values, "CALL P&L Ratio", "call_pnl_graph")
        self._graph_heatmap(self.put_pnl_heatmap_values, "PUT P&L Ratio", "put_pnl_graph")

    def save_heatmaps(self, save_dir="heatmaps"):
        """
        Save all generated heatmap figures to disk.

        Args:
            save_dir (str, optional): Directory to save PNG images. Defaults to "heatmaps".
        """
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