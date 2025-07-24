import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors
import seaborn as sns
import numpy as np
from matplotlib import dates as mdates
from .colormap_factory import get_default_colormap

# Enum of all bar chart types
class ChartType:
    HORIZONTAL_BAR = 1
    VERTICAL_BAR = 2

def plot_relative_distribution_horizontal_bar(dataframe, group_col, label_col, response_order, title, path = None, palette='coolwarm_r'):
    """
    Processes a DataFrame to plot the relative frequency of labels for each group in a horizontal bar chart.
    The group_col is used to segment the data into distinct sections for analysis. 
    Each unique value in this column defines a separate group for which the response distribution will be calculated and plotted. 
    
    :param dataframe: The DataFrame containing the data to plot.
    :param group_col: The name of the column representing the different groups or categories for comparison.
    :param label_col: The name of the column representing the responses.
    :param label_order: The order of responses for plotting (e.g., Likert scale) - also needed for colormap.
    :param title: The title of the plot.
    :param path: The path to save the plot (if None, plot will not be saved).
    :param palette: The name of a colormap from Matplotlib's palettes. See https://matplotlib.org/stable/users/explain/colors/colormaps.html
    """

    colors = get_default_colormap(response_order, palette=palette)

    # Group by condition and response, and count the occurrences
    grouped = dataframe.groupby([group_col, label_col]).size().reset_index(name='count')
    total_condition = grouped.groupby(group_col).aggregate({"count": "sum"}).reset_index()

    # Calculate relative response distribution
    grouped['relative_count'] = grouped.apply(lambda row: row['count'] / total_condition.loc[total_condition[group_col] == row[group_col], 'count'].values[0], axis=1)

    # Pivot the table to have condition as rows and response as columns
    pivoted = grouped.pivot(index=group_col, columns=label_col, values='relative_count')
    if response_order != None:
        pivoted = pivoted.reindex(columns=response_order)

    # Set the figure size
    fig, ax = plt.subplots(figsize=(6, 5))

    # Plot the DataFrame as a horizontal bar plot
    pivoted.plot(kind='barh', stacked=True, ax=ax, color=list(colors.values()))

    # Set plot labels and title
    plt.xlabel('Relative frequency')
    plt.xlabel('Relative frequency')
    plt.ylabel('Condition')

    # Remove the top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Adjust the figure margins
    plt.tight_layout()

    # Legend adjustments (if needed)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False, labelspacing = 0.7)

    plt.rcParams.update({'font.size': 16})

    if title:
        plt.title(title)
    
    if path:
        # Save the figure
        fig.savefig(path, dpi=300, bbox_inches='tight')
        
def plot_frequency_of_responses_bar(column, title, chart_type, file_path, legend = None, split = False, palette = 'PuBu'):
    """
    Converts a column of replies to a bar chart. The column's content is expected to be strings.
    A legend can be provided as a dictionary, where the key is the answer and the value is the legend.
    :param column: The column of replies
    :param title: The title of the chart
    :param chart_type: The type of chart
    :param file_path: The path to save the chart to
    :param legend: A custom legend of the chart (as dict, optional)
    :param split: Whether to split the column into multiple answers (default: False)
    :param palette: The name of a colormap from Matplotlib's palettes. See https://matplotlib.org/stable/users/explain/colors/colormaps.html
    :return: None
    """
    if split:
        all_answers = column.str.split(',').explode()
    else:
        all_answers = column

    # Count frequencies
    count_of_answers_given = {}
    for answer in all_answers:
        if answer in count_of_answers_given:
            count_of_answers_given[answer] += 1
        # elif pd.isna(answer):
        #     if 'nan' not in count_of_answers_given:
        #         count_of_answers_given['nan'] = 0
        #     count_of_answers_given['nan'] += 1
        else:
            count_of_answers_given[answer] = 1

    # Convert dictionary to Pandas Series for easier plotting
    count_series = pd.Series(count_of_answers_given).sort_index()

    # Plotting
    plt.figure()
    # Normalize the range and create a colormap for unique colors
    norm = matplotlib.colors.Normalize(vmin=0, vmax=len(count_series)-1)
    colormap = matplotlib.colormaps[palette]
    colors = [colormap(norm(value)) for value in range(len(count_series))]


    ax = None
    if chart_type == ChartType.HORIZONTAL_BAR:
        ax = count_series.plot(kind='barh', color=colors)
    elif chart_type == ChartType.VERTICAL_BAR:
        ax = count_series.plot(kind='bar', color=colors)

    plt.title(title)
    plt.rcParams['font.size'] = 14

    # Adding custom legends from JSON, if provided
    if isinstance(legend, dict):
        # Create a legend for each bar
        handles = []
        for answer, bar in zip(count_series.index, ax.patches):
            label = legend.get(answer, answer)
            handle = plt.Line2D([], [], color=bar.get_facecolor(), label=label, linewidth=5)
            handles.append(handle)
        plt.legend(handles=handles, loc='upper left', bbox_to_anchor=(1, 1))  # Move legend outside the plot
    # Add another legend type if needed
    elif legend != None:
        plt.legend([legend], loc='upper left', bbox_to_anchor=(1, 1))

    plt.xlabel('Frequency')
    plt.ylabel('Answer')
    if file_path:
        plt.savefig(file_path, bbox_inches='tight')  # Save the figure
        
# Function to plot KDE over a histogram with optional vertical lines and labels for specific dates
def plot_kde_over_hist(df, date_column, figsize=(10, 6), title=None, path=None, xlabel='', ylabel='', bins=None, kde=True, highlight_dates=None):
    """
    Plot a KDE over a bar chart with optional vertical lines and labels for specific dates.

    :param df: Pandas DataFrame containing the data.
    :param date_column: The column name for the date.
    :param figsize: Size of the figure (width, height).
    :param title: Title of the chart.
    :param path: Path to save the plot.
    :param highlight_dates: List of dates to highlight with vertical lines and labels.
    """
    plt.figure(figsize=figsize)

    # Histogram with KDE plot
    if bins is not None:
        sns.histplot(df, x=date_column, kde=kde, color='#77B5FE', bins=bins)
    else:
        sns.histplot(df, x=date_column, kde=kde, color='#77B5FE')

    # Formatting the plot
    plt.xlabel(xlabel or date_column)
    plt.ylabel(ylabel or 'Count')
    plt.title(title)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Remove right and upper spines
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Set major and minor locators for the x-axis
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=10))
    plt.gca().xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    
    # Add vertical lines and labels for highlight dates if provided
    if highlight_dates:
        for highlight_date in highlight_dates:
            highlight_date_dt = pd.to_datetime(highlight_date)
            plt.axvline(highlight_date_dt, color='red', linestyle='--', linewidth=1)
            
            # Add label with date text near the vertical line
            plt.text(highlight_date_dt - pd.Timedelta(days=1), plt.ylim()[1] * 0.78,  # Adjust the y position for better visibility
                     highlight_date_dt.strftime('%Y-%m-%d'),  # Format the date label
                     color='red', rotation=90, va='bottom', ha='center', fontsize=11)

    # Save or show plot
    if path:
        plt.savefig(path, bbox_inches='tight')
    else:
        plt.show()


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates

# Function to plot KDE over a histogram with optional vertical lines and labels for specific dates
# and an additional secondary y-axis for overall activity by intention
def plot_kde_hist_with_activity(df, date_column, activity_df, intention_column, figsize=(10, 6), title=None, path=None, xlabel='', ylabel='', bins=None, kde=True, highlight_dates=None, fontsize=14):
    """
    Plot a KDE over a histogram with optional vertical lines and labels for specific dates
    and a secondary y-axis to represent overall activity by intention using a stacked area chart.

    :param df: Pandas DataFrame containing the data for KDE and histogram.
    :param date_column: The column name for the date in the primary DataFrame.
    :param activity_df: Pandas DataFrame containing the overall activity data.
    :param intention_column: The column name for the intention data in the activity DataFrame.
    :param figsize: Size of the figure (width, height).
    :param title: Title of the chart.
    :param path: Path to save the plot.
    :param highlight_dates: List of dates to highlight with vertical lines and labels.
    :param fontsize: Font size for all text elements.
    """
    # Ensure date columns are in datetime format
    df[date_column] = pd.to_datetime(df[date_column])
    activity_df['conversation_time'] = pd.to_datetime(activity_df['conversation_time'])

    # Aggregate activity data by date and intention
    activity_agg = activity_df.groupby([activity_df['conversation_time'].dt.date, intention_column]).size().unstack(fill_value=0)
    
    # Create a plot with a secondary y-axis
    fig, ax1 = plt.subplots(figsize=figsize)

    # Primary y-axis: Histogram with KDE plot
    if bins is not None:
        sns.histplot(df, x=date_column, kde=kde, color='#77B5FE', bins=bins, ax=ax1)
    else:
        sns.histplot(df, x=date_column, kde=kde, color='#77B5FE', ax=ax1)

    # Formatting the primary y-axis plot
    ax1.set_xlabel(xlabel or date_column, fontsize=fontsize)
    ax1.set_ylabel(ylabel or 'Count', fontsize=fontsize)
    ax1.set_title(title, fontsize=fontsize)
    ax1.tick_params(axis='x', rotation=90, labelsize=fontsize)
    ax1.tick_params(axis='y', labelsize=fontsize)
    ax1.grid(True)
    
    # Remove right and upper spines for primary y-axis
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)

    # Set major and minor locators for the x-axis
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=10))
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Set the format to show full date

    # Secondary y-axis: Overall activity by intention using a stacked area chart
    ax2 = ax1.twinx()

    # Colors for the stacked area chart
    colors = [(0.09019607843137255, 0.7450980392156863, 0.8117647058823529, 1.0), (0.4980392156862745, 0.4980392156862745, 0.4980392156862745, 1.0), (0.5803921568627451, 0.403921568627451, 0.7411764705882353, 1.0), (0.17254901960784313, 0.6274509803921569, 0.17254901960784313, 1.0), (0.12156862745098039, 0.4666666666666667, 0.7058823529411765, 1.0)]
    
    # Convert the index to datetime for stackplot
    x = pd.to_datetime(activity_agg.index)

    # Plot each intention as a stacked area
    ax2.stackplot(x, activity_agg.T, labels=activity_agg.columns, colors=colors, alpha=0.25)

    ax2.set_ylabel('Amount of prompts by intention', fontsize=fontsize)
    ax2.tick_params(axis='y', labelsize=fontsize)
    ax2.legend(title='Intention', loc='upper right', fontsize=fontsize, title_fontsize=fontsize)
    
    # Add vertical lines and labels for highlight dates if provided
    if highlight_dates:
        for highlight_date in highlight_dates:
            highlight_date_dt = pd.to_datetime(highlight_date)
            ax1.axvline(highlight_date_dt, color='red', linestyle='--', linewidth=1)
            
            # Add label with date text near the vertical line
            ax1.text(highlight_date_dt - pd.Timedelta(days=1), ax1.get_ylim()[1] * 0.76,  # Adjust the y position for better visibility
                     highlight_date_dt.strftime('%Y-%m-%d'),  # Format the date label
                     color='red', rotation=90, va='bottom', ha='center', fontsize=14)

    # Save or show plot
    if path:
        plt.savefig(path, bbox_inches='tight')
    else:
        plt.show()