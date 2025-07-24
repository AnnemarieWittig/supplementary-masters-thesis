
import plot_likert
import warnings
import matplotlib.pyplot as plt
from .colormap_factory import get_default_colorlist
import os

LIKERT_SCALES = {
    'HELPFUL':  { 
        'likert': ["Not helpful at all", "Not very helpful", "Somewhat helpful", "Helpful", "Very helpful"],
        'legend': ["Not helpful at all", "Very helpful"] 
        },
    'EXPERIENCE': {
        'likert': ["Very inexperienced", "Inexperienced", "Neither inexperienced nor experienced", "Experienced", "Very experienced"],
        'legend': ["Very inexperienced", "Very experienced"]
        },
    'COMPARED': {
        'likert': ["Much worse", "Worse", "Neither worse nor better", "Better", "Much better"],
        'legend': ["Much worse", "Much better"]
        },
    'AGREE': {
        'likert': ["Strongly disagree", "Disagree", "Neither agree nor disagree", "Agree", "Strongly agree"],
        'legend': ["Strongly disagree", "Strongly agree"]
        },
    'TIME': {
        'likert': ["Daily", "Several times a week", "Several times a month", "Less often", "Never"],
        'legend': ["Daily", "Never"]
        }
    }

def translate_to_agreeing(column):
    column = column.replace("stimme voll zu", "Strongly agree").replace("stimme eher zu", "Agree").replace("stimme weder zu noch lehne ich ab", "Neither agree nor disagree").replace("stimme eher nicht zu", "Disagree").replace("stimme überhaupt nicht zu", "Strongly disagree")
    return column

def translate_to_time(column):
    column = column.replace("täglich", "Daily").replace("mehrmals pro Woche", "Several times a week").replace("mehrmals pro Monat", "Several times a month").replace("seltener", "Less often").replace("nie", "Never")
    return column

def translate_to_comparison(column):
    column = (column.replace("deutlich schlechter", "Much worse")
        .replace("schlechter", "Worse")
        .replace("gleich", "Neither worse nor better")
        .replace("besser", "Better")
        .replace("deutlich besser", "Much better"))
    return column
        
def translate_to_experience(column):
    column = (column.replace("sehr unerfahren", "Very inexperienced")
        .replace("unerfahren", "Inexperienced")
        .replace("mittel", "Neither inexperienced nor experienced")
        .replace("erfahren", "Experienced")
        .replace("sehr erfahren", "Very experienced"))
    return column

def plot_likert_response(columns, column_titles, likert_scale, likert_legend_labels, title, file_path, palette='coolwarm_r'):
    colors = get_default_colorlist(len(likert_scale), palette)
    colors.insert(0, (1.0,1.0,1.0))
    print(colors)
    # plot_likert uses deprecated functions, so we ignore the warnings
    warnings.filterwarnings("ignore", category=FutureWarning)
    
        # Set a fixed width and dynamic height before plotting
    fixed_width = 10  # Fixed width in inches
    dynamic_height = 0.5 * len(columns)  # Adjust height based on the number of rows
    plt.figure(figsize=(fixed_width, int(dynamic_height)))
    
    # Plot configuration
    params = {'axes.labelsize': 14.0,'axes.titlesize':14.0, 'font.size': 14.0, 'legend.fontsize': 14.0, 'xtick.labelsize': 14.0, 'ytick.labelsize': 14.0}
    plt.rcParams.update(params)
    
    ax = plot_likert.plot_likert(columns, likert_scale, plot_percentage=True, colors=colors)
    ax.figure.set_size_inches(4, 1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    legend_handles = [plt.Rectangle((0, 0), 10, 10, color=colors[1]),  # Set width to half using the scale parameter
        plt.Rectangle((0, 0), 10, 1, color=colors[-1])]
    ax.legend(legend_handles, likert_legend_labels,  bbox_to_anchor=(1, 1), markerfirst=False)
    ticks = ax.get_xticks()[::2]
    ax.set_xticks(ticks)
    ax.tick_params(axis='y', length=0)
    ax.set_yticklabels(column_titles)
    ax.set_title(title)
    if len(columns) > 2:
        height = 0.3 * len(columns.columns)
        ax.figure.set_size_inches(4, height)
        
    plt.rcParams['font.size'] = 14.0

    if file_path:
        plt.savefig(file_path, bbox_inches='tight')  # Save the figure
        

def plot_likert_response_without_text(columns, column_titles, likert_scale, likert_legend_labels, title, file_path, palette='coolwarm_r', no_text=False):
    # Add mapping for numerical values back to labels for the plot
    numerical_likert_scale = [1, 2, 3, 4, 5]
    colors = get_default_colorlist(len(numerical_likert_scale), palette)
    colors.insert(0, (1.0, 1.0, 1.0))  # Adding a neutral color for missing data (optional)
    
    # Ignore warnings related to deprecated functions
    warnings.filterwarnings("ignore", category=FutureWarning)

    # Set a fixed width and dynamic height before plotting
    fixed_width = 10
    dynamic_height = 0.5 * len(columns)
    plt.figure(figsize=(fixed_width, int(dynamic_height)))

    # Update plot configuration based on text requirements
    if not no_text:
        params = {
            'axes.labelsize': 14.0,
            'axes.titlesize': 14.0,
            'font.size': 14.0,
            'legend.fontsize': 14.0,
            'xtick.labelsize': 14.0,
            'ytick.labelsize': 14.0
        }
        plt.rcParams.update(params)

    # Plot using numerical data but display original likert labels
    ax = plot_likert.plot_likert(columns, numerical_likert_scale, plot_percentage=True, colors=colors)
    ax.figure.set_size_inches(4, 1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    if not no_text:
        # Use the original text labels for legend
        legend_handles = [
            plt.Rectangle((0, 0), 10, 10, color=colors[1]),
            plt.Rectangle((0, 0), 10, 10, color=colors[-1])
        ]
        ax.legend(legend_handles, likert_legend_labels, bbox_to_anchor=(1, 1), markerfirst=False)
        ticks = ax.get_xticks()[::2]
        ax.set_xticks(ticks)
        ax.set_yticklabels(column_titles)
        ax.set_title(title)
    else:
        ax.set_xticks([])
        ax.set_yticklabels([])
        ax.set_title("")

    ax.tick_params(axis='y', length=0)

    if len(columns) > 2:
        height = 0.3 * len(columns.columns)
        ax.figure.set_size_inches(4, height)

    if file_path:
        plt.savefig(file_path, bbox_inches='tight')  # Save the figure
    plt.show()
