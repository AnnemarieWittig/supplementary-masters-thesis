import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_scatter(df, x_column, y_column, group_column, figsize=(10, 6), title=None, path=None, palette='tab10', xlabel=None, ylabel=None):
    """
    Plot a scatter plot from a DataFrame with color-coded groups.

    :param df: Pandas DataFrame containing the data.
    :param x_column: The column name for the x-axis data (e.g., 'number of commits').
    :param y_column: The column name for the y-axis data (e.g., 'used budget').
    :param group_column: The column name for the group data (e.g., 'group name').
    :param figsize: Size of the figure (width, height).
    :param title: Title of the plot.
    :param path: Path to save the plot.
    :param palette: Color palette for the groups.
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    """
    plt.figure(figsize=figsize)
    plt.rcParams['font.size'] = 14
    
    # Generate color palette
    unique_groups = df[group_column].unique()
    color_list = plt.get_cmap(palette).colors[:len(unique_groups)]
    color_dict = dict(zip(unique_groups, color_list))
    
    # Plot each group
    for group in unique_groups:
        subset = df[df[group_column] == group]
        plt.scatter(subset[x_column], subset[y_column], label=group, color=color_dict[group])
    
    # Set labels and title
    plt.xlabel(xlabel or x_column)
    plt.ylabel(ylabel or y_column)
    plt.title(title)
    
    # Display legend
    plt.legend(title=group_column)
    
    # Tight layout for better spacing
    plt.tight_layout()
    
    # Save plot if path is provided
    if path:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path, bbox_inches='tight')
    
    # Show the plot
    plt.show()


def plot_likert_scatter(df, group_column, likert_columns, figsize=(10, 6), title=None, path=None, palette='tab10', xlabel=None, ylabel=None, rotation=45, legend = False, likert_order = None):
    """
    Plot a scatter plot from a DataFrame with Likert scale responses.

    :param df: Pandas DataFrame containing the data.
    :param group_column: The column name for the group data (e.g., 'group name').
    :param likert_columns: List of column names for Likert scale questions.
    :param figsize: Size of the figure (width, height).
    :param title: Title of the plot.
    :param path: Path to save the plot.
    :param palette: Color palette for the Likert questions.
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    :param rotation: Rotation angle for the x-axis labels.
    """
    plt.figure(figsize=figsize)
    plt.rcParams['font.size'] = 14
    
    # Generate color palette
    color_list = plt.get_cmap(palette).colors[:len(likert_columns)]
    color_dict = dict(zip(likert_columns, color_list))
    
    # Plot each Likert question
    for column in likert_columns:
        if likert_order != None:
            df[column] = pd.Categorical(df[column], categories=likert_order, ordered=True)
        else:
            df[column] = pd.Categorical(df[column], ordered=True)
        plt.scatter(df[group_column], df[column], label=column, color=color_dict[column])
    
    # Set labels and title
    plt.xlabel(xlabel or group_column)
    plt.ylabel(ylabel or "Likert Scale Responses")
    plt.title(title)
    
    # Rotate x-axis labels
    plt.xticks(rotation=rotation)
    
    # Display legend
    if legend == True:
        plt.legend(title="Likert question", loc='center', ncol=2)
    else:
        plt.legend().set_visible(False)
    
    # Tight layout for better spacing
    plt.tight_layout()
    
    # Save plot if path is provided
    if path:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path, bbox_inches='tight')
    
    # Show the plot
    plt.show()


def plot_numeric_scatter(df, group_column, value_columns, figsize=(10, 6), title=None, path=None, palette='tab10', xlabel=None, ylabel=None, rotation=45, legend=False):
    """
    Plot a scatter plot from a DataFrame with numeric responses.

    :param df: Pandas DataFrame containing the data.
    :param group_column: The column name for the group data (e.g., 'group name').
    :param value_columns: List of column names for numeric questions.
    :param figsize: Size of the figure (width, height).
    :param title: Title of the plot.
    :param path: Path to save the plot.
    :param palette: Color palette for the questions.
    :param xlabel: Label for the x-axis.
    :param ylabel: Label for the y-axis.
    :param rotation: Rotation angle for the x-axis labels.
    """
    plt.figure(figsize=figsize)
    plt.rcParams['font.size'] = 14
    
    # Generate color palette
    color_list = plt.get_cmap(palette).colors[:len(value_columns)]
    color_dict = dict(zip(value_columns, color_list))
    
    # Plot each question
    for column in value_columns:
        plt.scatter(df[group_column], df[column], label=column, color=color_dict[column])
    
    # Set labels and title
    plt.xlabel(xlabel or group_column)
    plt.ylabel(ylabel or "Numeric Responses")
    plt.title(title)
    
    # Rotate x-axis labels
    plt.xticks(rotation=rotation)
    
    # Display legend
    if legend:
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.5),
            fancybox=True, shadow=True, ncol=1)
    else:
        plt.legend().set_visible(False)
    
    # Tight layout for better spacing
    plt.tight_layout()
    
    # Save plot if path is provided
    if path:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path, bbox_inches='tight')
    
    # Show the plot
    plt.show()