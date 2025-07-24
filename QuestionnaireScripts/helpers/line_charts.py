import matplotlib.pyplot as plt
from .colormap_factory import get_first_colors_from_palette_as_colorlist, get_first_colors_from_palette_as_colorlist, get_default_colorlist
import matplotlib
import numpy as np

def plot_line_chart(pivot_df, figsize=(10, 6), title=None, path=None, palette='plasma', ylabel='Count', xlabel='Date'):
    """
    Plot a line chart with the DataFrame provided.

    :param pivot_df: Pandas DataFrame containing the pivoted data for plotting.
    :param figsize: Size of the figure (width, height).
    :param title: Title of the chart.
    :param path: If provided, the path where the chart image will be saved.
    :param palette: The color palette for the lines in the chart.
    :param ylabel: The label for the y-axis.
    :param xlabel: The label for the x-axis.
    """
    # Set the color palette for the lines
    colors = plt.get_cmap(palette)(range(len(pivot_df.columns)))

    # Plot the line chart
    ax = pivot_df.plot(kind='line', figsize=figsize, color=colors, title=title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    # Explicitly set the x-ticks to match the dates in your DataFrame
    plt.xticks(ticks=range(len(pivot_df.index)), labels=pivot_df.index, rotation=45)

    plt.xticks(rotation=45)  # Adjust as necessary for your x-labels
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper right')
    plt.grid(True)
    plt.rcParams['font.size'] = 14
    plt.tight_layout()
    
    if path:
        plt.savefig(path, bbox_inches='tight')

def plot_mean_per_group(df, group_column, mean_column, figsize=(10, 6), title=None, path=None, palette='plasma', ylabel=''):
    """
    Plot a bar chart of conversation lengths per condition.

    :param df: Pandas DataFrame containing the data.
    :param group_column: The column name that is used to group the data.
    :param mean_column: The column that should be meaned (y-axis).
    :param figsize: Size of the figure (width, height).
    :param rotation: Rotation angle for x-axis labels.
    :param title: Title of the chart.
    """
    # Group by the condition and calculate the mean conversation length
    grouped = df.groupby(group_column)[mean_column].mean().reset_index(name='meaned')

    # Sort the results
    grouped = grouped.sort_values(by=group_column)

    colors = get_first_colors_from_palette_as_colorlist(len(grouped['meaned']), palette)

    grouped.plot(x=group_column, y='meaned' or 'average_length', kind='bar', figsize=figsize, color=colors, legend=None)
    plt.xlabel(group_column)
    plt.ylabel(ylabel)
    plt.title(title or f'Average Conversation Length per {group_column}')
    plt.rcParams['font.size'] = 14
    plt.xticks(range(len(grouped[group_column])), grouped[group_column])
    plt.tight_layout()
    
    if path:
        plt.savefig(path, bbox_inches='tight')
    

def plot_sum_per_group(df, group_column, mean_column, figsize=(10, 6), title=None, path=None, palette='plasma', ylabel='', xlabel=''):
    """
    Plot a line chart of conversation lengths per condition.

    :param df: Pandas DataFrame containing the data.
    :param group_column: The column name that is used to group the data.
    :param mean_column: The column that should be meaned (y-axis).
    :param figsize: Size of the figure (width, height).
    :param rotation: Rotation angle for x-axis labels.
    :param title: Title of the chart.
    :param palette: The name of a Matplotlib colormap.
    """
    # Group by the condition and calculate the mean conversation length
    grouped = df.groupby(group_column)[mean_column].sum().reset_index(name='length')

    # Sort the results
    grouped = grouped.sort_values(by=group_column)
    

    colors = get_first_colors_from_palette_as_colorlist(len(grouped['length']), palette)

    # Plot the line chart
    grouped.plot(x=group_column, y='length', kind='bar', figsize=figsize, color=colors, legend=None)
    
    plt.xlabel(xlabel or group_column)
    plt.ylabel(ylabel)
    plt.title(title or f'Sum per {group_column}')
    plt.rcParams['font.size'] = 14
    plt.xticks(range(len(grouped[group_column])), grouped[group_column])
    plt.tight_layout()
    
    if path:
        plt.savefig(path, bbox_inches='tight')
    

def plot_median_per_group(df, group_column, median_column, figsize=(10, 6), title=None, path=None, palette='plasma', ylabel='', xlabel=''):
    """
    Plot a line chart of conversation lengths per condition.

    :param df: Pandas DataFrame containing the data.
    :param group_column: The column name that is used to group the data.
    :param median_column: The column that should be meaned (y-axis).
    :param figsize: Size of the figure (width, height).
    :param rotation: Rotation angle for x-axis labels.
    :param title: Title of the chart.
    :param palette: The name of a Matplotlib colormap.
    """
    # Group by the condition and calculate the mean conversation length
    grouped = df.groupby(group_column)[median_column].median().reset_index(name='length')

    # Sort the results
    grouped = grouped.sort_values(by=group_column)
    

    colors = get_first_colors_from_palette_as_colorlist(len(grouped['length']), palette)

    # Plot the line chart
    grouped.plot(x=group_column, y='length', kind='bar', figsize=figsize, color=colors, legend=None)
    
    plt.xlabel(xlabel or group_column)
    plt.ylabel(ylabel)
    plt.title(title or f'Sum per {group_column}')
    plt.rcParams['font.size'] = 14
    plt.xticks(range(len(grouped[group_column])), grouped[group_column])
    plt.tight_layout()
    
    if path:
        plt.savefig(path, bbox_inches='tight')

# Example usage:
# plot_conversation_length_per_condition(your_dataframe, 'group_column', 'mean_column')

def plot_aggregated_line_chart(df, group_column, aggregate_column, threshold=5, figsize=(10, 6), rotation=90, reorder=None, title=None, path=None, palette='tab10', type='bar', xlabel='', legend_position = 'upper right', ylabel='', define_y_axis = None, columns = None, min_occurences = 0, stacked = False):
    """
    Plot an aggregated line chart from a DataFrame.
    """
    print(f'x label: {xlabel}')  # Debug statement
    print(f'y label: {ylabel}')  # Debug statement
    
    # Group by the specified columns and count the occurrences
    grouped = df.groupby([group_column, aggregate_column]).size().reset_index(name='counts')

    # Sum counts for each group and apply threshold filter for 'others'
    total_counts = grouped.groupby(group_column)['counts'].sum().reset_index()
    relevant_groups = total_counts[total_counts['counts'] > threshold][group_column]
    grouped.loc[~grouped[group_column].isin(relevant_groups), group_column] = 'others'

    # Aggregate again based on updated groupings
    grouped = grouped.groupby([group_column, aggregate_column]).sum().reset_index()

    # Pivot the DataFrame for plotting
    pivot_df = grouped.pivot(index=group_column, columns=aggregate_column, values='counts')

    # Filter out columns with all NaN values or a total of less than 15 in the column aggregate_column
    pivot_df = pivot_df.dropna(axis=1, how='all')
    print(min_occurences)
    pivot_df = pivot_df.loc[:, pivot_df.sum() > min_occurences]
    
    if columns is not None:
        for col in columns:
            if col not in pivot_df.columns:
                pivot_df[col] = np.nan  # add empty column
        pivot_df = pivot_df[columns]
    
    colors = get_first_colors_from_palette_as_colorlist(len(pivot_df.columns), palette)
    
    if reorder != None:
        # Map colors to pivot_df columns
        colors = dict(zip(pivot_df.columns, colors))
        pivot_df = pivot_df[reorder]
        
        # reorder colors
        colors = [colors[col] for col in reorder]

    # Plotting
    # plt.figure(figsize=figsize)
    # Plot stacked bar chart
    pivot_df.plot(kind=type, color=colors, figsize=figsize, stacked=stacked)
    
    # Ensure first and last x-values are always labeled in the plot
    # Get the current xticks and labels
    xticks, xlabels = plt.xticks()

    # Add the last index of your dataframe to the xticks and xlabels
    xticks = np.append(xticks, len(pivot_df.index) - 1)
    xlabels = np.append(xlabels, pivot_df.index[-1])
    
    plt.xlabel(xlabel or group_column)
    plt.ylabel(ylabel or 'Counts')
    plt.title(title)
    plt.legend(title=aggregate_column, bbox_to_anchor=(1.05, 1), loc=legend_position)
    plt.rcParams['font.size'] = 14
    # plt.xticks(rotation=rotation)
    # plt.tight_layout()
    plt.grid(True)
    
    if define_y_axis != None:
        plt.ylim(define_y_axis[0], define_y_axis[1])

    if path:
        plt.savefig(path, bbox_inches='tight')

    plt.show()
    return pivot_df.columns

def plot_percentage_stacked_bar_chart(df, group_column, aggregate_column, reorder=None, group_reorder = None, threshold=5, figsize=(10, 6), rotation=0, title=None, path=None, palette='tab10', xlabel=None, x=0, y=0, fontsize = 12):
    df[group_column] = df[group_column].astype(str).apply(lambda x: x.replace('_', ' ').capitalize())
    # print(df[group_column].unique())

    # Group by the specified columns and count the occurrences
    grouped = df.groupby([group_column, aggregate_column]).size().reset_index(name='counts')

    # Sum counts for each group and apply threshold filter for 'Other'
    total_counts = grouped.groupby(group_column)['counts'].sum().reset_index()
    relevant_groups = total_counts[total_counts['counts'] > threshold][group_column]
    grouped.loc[~grouped[group_column].isin(relevant_groups), group_column] = 'Other'

    # Aggregate again based on updated groupings
    grouped = grouped.groupby([group_column, aggregate_column]).sum().reset_index()

    # Pivot the DataFrame for plotting
    pivot_df = grouped.pivot(index=group_column, columns=aggregate_column, values='counts')

    if group_reorder != None:
        # Order group_column based on the reorder list
        pivot_df = pivot_df.reindex(group_reorder)

    # Calculate percentages
    pivot_df_percentage = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100

    # Filter out columns with all NaN values
    pivot_df_percentage = pivot_df_percentage.dropna(axis=1, how='all')
    
    # if reorder != None:
    #     pivot_df_percentage = pivot_df_percentage[reorder]

    # Get the correct colors in the same order as the columns
    colors = get_first_colors_from_palette_as_colorlist(len(pivot_df.columns), palette)

    # Plotting
    ax = pivot_df_percentage.plot(kind='barh', stacked=True, color=colors, figsize=figsize)

    # Add total values and actual values on the bars
    for container in ax.containers:
        for i, rect in enumerate(container):
            width = rect.get_width()
            actual_value = pivot_df.iloc[i, ax.containers.index(container)]
            if width > 0:
                ax.annotate(f'{int(actual_value)}',
                            xy=(rect.get_x() + width / 2, rect.get_y() + rect.get_height() / 2),
                            xytext=(0, 0),
                            textcoords='offset points',
                            ha='center', va='center', fontsize=(fontsize-2), color='black')

    # Annotate the total count at the end of each bar
    for i, (index, row) in enumerate(pivot_df.iterrows()):
        total = row.sum()
        ax.annotate(f'{int(total)}',
                    xy=(100, i),
                    xytext=(5, 0),
                    textcoords='offset points',
                    va='center', ha='left', fontsize=(fontsize-2), color='black')

    ax.spines['right'].set_visible(False)
    
    if xlabel:
        plt.xlabel(xlabel)
    plt.grid(axis="x")
    plt.ylabel(group_column)
    plt.title(title)
    plt.text(x, y, 'Total', fontsize=(fontsize-2))
    plt.rcParams['font.size'] = fontsize

    # Modify legend layout and location
    handles, labels = ax.get_legend_handles_labels()
    labels = [label for label in pivot_df.columns]
    ax.legend_.remove()
    fig = ax.get_figure()
    
    fig.legend(handles, labels, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.05))
    plt.tight_layout()

    if path:
        plt.savefig(path, bbox_inches='tight')

    plt.show()




def plot_aggregated_sum_line_chart(df, group_column, aggregate_column, mean_column, threshold=5, figsize=(10, 6), rotation=90, title=None, path=None, palette='plasma'):
    """
    Plot an aggregated line chart representing the total sum of a mean_column for a grouped dataframe (group column) per category (aggregate_column).

    :param df: Pandas DataFrame containing the data.
    :param group_column: The column name to group by (similar to 'intention').
    :param aggregate_column: The column name to aggregate on (similar to 'condition_name').
    :param mean_column: The column storing the length of each conversation.
    :param threshold: The threshold for filtering; categories with summed lengths <= this will be aggregated into 'others'.
    :param figsize: Size of the figure (width, height).
    :param rotation: Rotation angle for x-axis labels.
    """
    # Step 1: Group by the specified columns and sum the lengths
    grouped = df.groupby([group_column, aggregate_column])[mean_column].sum().reset_index(name='total_length')

    # Step 2: Filter and aggregate
    # Create a mask for summed lengths > threshold
    mask = grouped.groupby(group_column)['total_length'].transform('sum') > threshold

    # Replace values with low sums with 'others'
    grouped.loc[~mask, group_column] = 'others'

    # Re-group and sum the lengths after the replacement
    grouped = grouped.groupby([group_column, aggregate_column]).sum().reset_index()

    # Step 3: Pivot the DataFrame for plotting
    pivot_df = grouped.pivot(index=group_column, columns=aggregate_column, values='total_length')

    # Sort the DataFrame based on the total lengths for each category
    pivot_df['total'] = pivot_df.sum(axis=1)
    pivot_df = pivot_df.sort_values(by='total', ascending=False)
    pivot_df.drop('total', axis=1, inplace=True)

    # Generate color list
    colors = get_first_colors_from_palette_as_colorlist(len(pivot_df.columns), palette)

    # Plot the line chart
    pivot_df.plot(kind='line', figsize=figsize, color=colors)
    plt.xlabel(group_column)
    plt.ylabel('Total Length of ' + group_column)
    plt.title(title)
    plt.rcParams['font.size'] = 14

    # Show all x-axis labels
    plt.xticks(range(len(pivot_df.index)), pivot_df.index, rotation=rotation)

    plt.tight_layout()
    
    if path:
        plt.savefig(path, bbox_inches='tight')
import pandas as pd

def plot_average_chart(df, group_column, aggregate_column, data_column, upper_legend=False, colors=None, threshold=5, figsize=(10, 6), rotation=90, title=None, path=None, palette='plasma', reorder = None, xlabel = None, ylabel = None, define_y_axis = None, type='line', reverse=False):
    """
    Plot an aggregated line chart from a DataFrame, averaging the specified data.

    :param df: Pandas DataFrame containing the data.
    :param group_column: The column name to group by (e.g., 'intention').
    :param aggregate_column: The column name to aggregate on (e.g., 'condition_name').
    :param data_column: The column containing the data to be averaged.
    :param threshold: The threshold for filtering; groups below this will be aggregated into 'others'.
    :param figsize: Size of the figure (width, height).
    :param rotation: Rotation angle for x-axis labels.
    """
    # Step 1: Group by the specified columns and compute the average
    grouped = df.groupby([group_column, aggregate_column])[data_column].mean().reset_index(name='average_data')

    # Step 2: Identify groups with a total count less than the threshold and aggregate them into 'others'
    counts = df[group_column].value_counts()
    others = counts[counts <= threshold].index
    grouped[group_column] = grouped[group_column].replace(others, 'others')

    # Step 3: Re-group and compute the average again including 'others'
    grouped = grouped.groupby([group_column, aggregate_column]).mean().reset_index()

    # Step 4: Pivot the DataFrame for plotting
    pivot_df = grouped.pivot(index=group_column, columns=aggregate_column, values='average_data')

    # Sort the DataFrame based on the maximum average for each category
    # pivot_df['max'] = pivot_df.max(axis=1)
    # pivot_df = pivot_df.sort_values(by='max', ascending=False)
    # pivot_df.drop('max', axis=1, inplace=True)

    if reorder != None:
        pivot_df = pivot_df.reindex(reorder)
    # Generate color list
    color_list = get_first_colors_from_palette_as_colorlist(len(pivot_df.columns), palette)
        
    if colors != None:
        color_list = colors
        
    # Reverse the column order
    if reverse == True:
        pivot_df = pivot_df.iloc[::-1]

    # Plot using the color list
    ax = pivot_df.plot(kind=type, figsize=figsize, color=color_list)
    plt.xlabel(xlabel or group_column)
    plt.ylabel(ylabel or 'Average ' + data_column)
    plt.title(title)
    plt.rcParams['font.size'] = 14

    plt.xticks(ticks=range(len(pivot_df.index)), labels=pivot_df.index, rotation=rotation)
    if upper_legend == True:
        ax.legend_.remove()
        handles, labels = ax.get_legend_handles_labels()
        labels = [label for label in pivot_df.columns]
        fig = ax.get_figure()
        
        fig.legend(handles, labels, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.05))
    
    plt.tight_layout()
    
    plt.grid(True, axis='y')
    
    # Move legend to the right upper corner
    
    
    if define_y_axis != None:
        ax.set_ylim(define_y_axis[0], define_y_axis[1])

    
    if path:
        plt.savefig(path, bbox_inches='tight')

def plot_median_chart(df, group_column, aggregate_column, data_column, threshold=5, figsize=(10, 6), rotation=90, title=None, path=None, palette='plasma', reorder = None, xlabel = None, ylabel = None, define_y_axis = None, type='line'):
    """
    Plot an aggregated line chart from a DataFrame, averaging the specified data.

    :param df: Pandas DataFrame containing the data.
    :param group_column: The column name to group by (e.g., 'intention').
    :param aggregate_column: The column name to aggregate on (e.g., 'condition_name').
    :param data_column: The column containing the data to be averaged.
    :param threshold: The threshold for filtering; groups below this will be aggregated into 'others'.
    :param figsize: Size of the figure (width, height).
    :param rotation: Rotation angle for x-axis labels.
    """
    # Step 1: Group by the specified columns and compute the average
    grouped = df.groupby([group_column, aggregate_column])[data_column].median().reset_index(name='average_data')

    # Step 2: Identify groups with a total count less than the threshold and aggregate them into 'others'
    counts = df[group_column].value_counts()
    others = counts[counts <= threshold].index
    grouped[group_column] = grouped[group_column].replace(others, 'others')

    # Step 3: Re-group and compute the average again including 'others'
    grouped = grouped.groupby([group_column, aggregate_column]).median().reset_index()

    # Step 4: Pivot the DataFrame for plotting
    pivot_df = grouped.pivot(index=group_column, columns=aggregate_column, values='average_data')

    # Sort the DataFrame based on the maximum average for each category
    pivot_df['max'] = pivot_df.max(axis=1)
    pivot_df = pivot_df.sort_values(by='max', ascending=False)
    pivot_df.drop('max', axis=1, inplace=True)

    if reorder != None:
        pivot_df = pivot_df.reindex(reorder)
    # Generate color list
    color_list = get_first_colors_from_palette_as_colorlist(len(pivot_df.columns), palette)

    # Plot using the color list
    ax = pivot_df.plot(kind=type, figsize=figsize, color=color_list)
    plt.xlabel(xlabel or group_column)
    plt.ylabel(ylabel or 'Average ' + data_column)
    plt.title(title)
    plt.rcParams['font.size'] = 14

    plt.xticks(ticks=range(len(pivot_df.index)), labels=pivot_df.index, rotation=rotation)
    plt.tight_layout()
    
    plt.grid(True)
    
    # Move legend to the right upper corner
    
    
    if define_y_axis != None:
        ax.set_ylim(define_y_axis[0], define_y_axis[1])

    
    if path:
        plt.savefig(path, bbox_inches='tight')
