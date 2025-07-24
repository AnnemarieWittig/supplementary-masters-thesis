import pandas as pd

def escape_latex_special_chars(text):
    """
    Escapes LaTeX special characters in a text string.

    :param text: The text string to be escaped.
    :return: A string with LaTeX special characters escaped.
    """
    special_chars = {
        '\\': r'\textbackslash{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '^': r'\^{}',
        '~': r'\~{}'
    }
    for char, escape in special_chars.items():
        text = text.replace(char, escape)
    return text

def transform_df_column_to_latex(column):
    # Initialize a dictionary with each unique item in the column
    values = {value: 0 for value in column.unique()}
    values['total'] = 0

    # Count the occurrences of each value
    for value in column:
        values[value] += 1
        values['total'] += 1

    # Convert the dictionary into a DataFrame
    df = pd.DataFrame(list(values.items()), columns=['Value', 'Count'])

    df = df.applymap(lambda x: escape_latex_special_chars(str(x)) if isinstance(x, str) else x)


    # Convert DataFrame to LaTeX code
    latex_code = df.to_latex(index=False)

    return latex_code

import pandas as pd

def transform_df_to_latex(df, index=False, caption="Your Caption Here"):
    """
    Converts a Pandas DataFrame into a LaTeX formatted table.

    :param df: Pandas DataFrame to be converted.
    :param index: Boolean indicating whether to include the DataFrame's index in the LaTeX table.
    :param caption: String for the caption of the LaTeX table.
    :return: A string containing the LaTeX formatted table.
    """
    df = df.applymap(lambda x: escape_latex_special_chars(str(x)) if isinstance(x, str) else x)

    latex_str = df.to_latex(index=index, caption=caption)
    return latex_str

