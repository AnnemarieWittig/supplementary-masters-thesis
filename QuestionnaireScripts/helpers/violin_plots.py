import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from .colormap_factory import get_first_colors_from_palette_as_colorlist, get_first_colors_from_palette_as_colorlist
import seaborn as sns

def plot_violin_per_group_with_seaborn(df, group_column, value_column, figsize=(10, 6), title=None, path=None, palette='tab10', ylabel='', xlabel='', edge_color='black', median_color='red', mean_color='blue'):
    # Initialize the plot
    plt.figure(figsize=figsize)
    
    # Create the violin plot
    sns.violinplot(x=group_column, y=value_column, data=df, palette=palette, inner=None)

    # Overlay quartiles, whiskers, means, medians, 1.5x IQR, and min/max
    for i, condition in enumerate(sorted(df[group_column].unique())):
        data = df[df[group_column] == condition][value_column]
        print(data.sort_values())
        quartile1, median, quartile3 = np.percentile(data, [25, 50, 75])
        median = np.median(data)
        iqr = quartile3 - quartile1
        lower_fence = quartile1 - 1.5 * iqr
        upper_fence = quartile3 + 1.5 * iqr
        mean = np.mean(data)
        min_val = np.min(data)
        print(min_val)
        max_val = np.max(data)
        print(max_val)

        plt.plot([i - 0.25, i + 0.25], [median, median], color=median_color, lw=2)
        plt.plot([i - 0.2, i + 0.2], [mean, mean], color=mean_color, lw=2)
        plt.plot([i, i], [lower_fence, upper_fence], color=edge_color, lw=1, linestyle='--')
        plt.plot([i, i], [min_val, max_val], color=edge_color, lw=1)
        plt.plot([i, i], [quartile1, quartile3], color=edge_color, lw=5)
        plt.plot([i - 0.1, i + 0.1], [lower_fence, lower_fence], color=edge_color, lw=1, linestyle='--')
        plt.plot([i - 0.1, i + 0.1], [upper_fence, upper_fence], color=edge_color, lw=1, linestyle='--')
        plt.plot([i - 0.1, i + 0.1], [min_val, min_val], color=edge_color, lw=1)
        plt.plot([i - 0.1, i + 0.1], [max_val, max_val], color=edge_color, lw=1)
    
    # Customize the plot
    plt.title(title or f'{value_column.replace("_", " ").title()} per {group_column.replace("_", " ").title()}')
    plt.ylabel(ylabel or value_column.replace("_", " ").title())
    plt.xlabel(xlabel or group_column.replace("_", " ").title())
    plt.xticks(np.arange(len(df[group_column].unique())), sorted(df[group_column].unique()))

    # Add legend
    handles = [
        plt.Line2D([0], [0], color=median_color, lw=2, label='Median'),
        plt.Line2D([0], [0], color=mean_color, lw=2, label='Mean'),
        plt.Line2D([0], [0], color=edge_color, lw=1, label='Min/Max'),
        plt.Line2D([0], [0], color=edge_color, lw=1, linestyle='--', label='1.5x IQR'),
        plt.Line2D([0], [0], color=edge_color, lw=5, label='Interquartile Range')
    ]
    plt.legend(handles=handles, loc='upper right')
    
    plt.tight_layout()
    
    if path:
        plt.savefig(path, bbox_inches='tight')
    else:
        plt.show()

def plot_violin_per_group(df, group_column, value_column, figsize=(10, 6), title=None, path=None, palette='tab10', ylabel='', xlabel='', edge_color='black', median_color='red', mean_color='blue', legend=True, yrange = None, legend_loc='upper right', padding_left=""):
    """
    Plot a violin chart of a value column per group column and include IQR.

    :param df: Pandas DataFrame containing the data.
    :param group_column: The column name that is used to group the data.
    :param value_column: The column that should be plotted (y-axis).
    :param figsize: Size of the figure (width, height).
    :param title: Title of the chart.
    :param path: Path to save the plot.
    :param palette: Color palette for the plot.
    :param ylabel: Label for the y-axis.
    :param xlabel: Label for the x-axis.
    :param edge_color: Color for the edges of the violins.
    :param median_color: Color for the median lines.
    :param mean_color: Color for the mean lines.
    """
    # Prepare the data for plotting
    conditions = df[group_column].unique()
    data = [df[df[group_column] == condition][value_column] for condition in conditions]

    # Create the violin plot
    fig, ax = plt.subplots(figsize=figsize)
    # Set the position of the axes to ensure consistent drawing area
    ax.set_position([0.1, 0.1, 0.8, 0.8])  
    
    parts = ax.violinplot(data, showmeans=True, showmedians=True)

    colors = get_first_colors_from_palette_as_colorlist(len(conditions), palette=palette)
    counter = 0
    # Customize the plot
    for pc in parts['bodies']:
        pc.set_facecolor(colors[counter])
        pc.set_edgecolor(edge_color)
        pc.set_linewidth(0.5)
        pc.set_alpha(1)
        counter += 1

    parts['cbars'].set_edgecolor(edge_color)
    parts['cmins'].set_edgecolor(edge_color)
    parts['cmaxes'].set_edgecolor(edge_color)
    parts['cmeans'].set_edgecolor(mean_color)
    parts['cmedians'].set_edgecolor(median_color)

    # Calculate and plot IQR
    for i, condition in enumerate(conditions):
        quartile1, median, quartile3 = np.percentile(data[i], [25, 50, 75])
        whisker1 = np.percentile(data[i], 10)
        whisker3 = np.percentile(data[i], 90)
        ax.plot([i + 1, i + 1], [quartile1, quartile3], color='black', lw=5)
        ax.plot([i + 1, i + 1], [whisker1, whisker3], color='lightblue', lw=1, linestyle='--')

    if legend:
        # Add legend
        handles = [
            plt.Line2D([0], [0], color=median_color, lw=2, label='Median'),
            plt.Line2D([0], [0], color=edge_color, lw=2, label='Min/Max'),
            plt.Line2D([0], [0], color='black', lw=5, label='Interquartile range'),
            plt.Line2D([0], [0], color=mean_color, lw=2, label='Mean'),
            plt.Line2D([0], [0], color='lightblue', lw=1, label='1.5x IQR', linestyle='--'),
        ]
        if legend_loc == 'outside':
            ax.legend(handles=handles, loc='center left', bbox_to_anchor=(1, 0.5))
        elif legend_loc == 'below':
            ax.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=2)
        else:
            ax.legend(handles=handles, loc=legend_loc)
    # else: 
    #     ax.get_legend().remove()
    if padding_left != "":
        ax.text(1.0, 0.5, f"{padding_left}{padding_left}", transform=ax.transAxes, fontsize=12, verticalalignment='center', color='white')
        ax.text(-0.15, 0.5, padding_left, transform=ax.transAxes, fontsize=12, verticalalignment='center', color='white', ha='right')
    
    ax.set_title(title)
    ax.set_ylabel(ylabel or value_column.replace("_", " ").title())
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,.0f}k".format(x / 1000) if x >= 1000 else "{:,.0f}".format(x)))
    if max(df[value_column]) < 15:
        ax.set_yticks(np.arange(0, max(df[value_column])+2, 5))
    elif max(df[value_column]) < 50:
        ax.set_yticks(np.arange(0, max(df[value_column])+2, 10))
    ax.set_xticks(np.arange(1, len(conditions) + 1))
    ax.set_xticklabels(conditions)
    ax.set_xlabel(xlabel or group_column.replace("_", " ").title())
    
    if yrange:
        ax.set_ylim(yrange[0], yrange[1])

    plt.rcParams['font.size'] = 14
    plt.tight_layout()

    if path:
        plt.savefig(path, bbox_inches='tight')
        
    return fig, ax

