"""
File to add all functionality to create custom colormaps. 
"""
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm

custom_color_palettes = {
    "greenvibes": ["#14342B", "#439A86", "#BAB700"],
    "greenvibes_pastel": ["#5E8B7A", "#A1D3C3", "#E5E5A1"],
    "aubergine": ["#472C4C", "#439A86", "#BAB700"],
    "aubergine2": ["#653F6C", "#439A86", "#BAB700"],
    "aubergine2_pastel": ["#A583A2", "#A1D3C3", "#E5E5A1"],
    "aubergine2_pastel2" : ["#98719B", "#69B09D", "#D2D23F"], # Hauptfarben
    "aubergine2_pastel3" : ["#98719B", "#8FC6B4", "#D2D23F"],
    "aubergine3": ["#7e6b81", "#439A86", "#BAB700"],
    "aubergine_triad": ["#472c4c",	"#4c472c",	"#2c4c47"],
    "aubergine_triad_pastel": ["#8D748C", "#8C8D74", "#748C8D"],
    "multicolor": ["#442B48", "#79B791", "#F3CA40"],
    "multicolor_pastel": ["#8B6988", "#B2D8BE", "#F9E8A8"],
    "multicolor2": ["#B56576", "#79B791", "#F3CA40"],
    "multicolor2_pastel": ["#D8A4AD", "#B2D8BE", "#F9E8A8"],
    "teaparty":["#442B48", "#439A86", "#BAB700"],
    "teaparty_pastel" : ["#8B6988", "#A1D3C3", "#E5E5A1"],
    "teaparty2":["#004643", "#FCBA04", "#442B48"],
    "teaparty2_pastel" : ["#66A3A1", "#FFE28A", "#8B6988"],
    "pastel": ["#424B54", "#E1CE7A", "#B56576"],
    "pastel2": ["#8A929B", "#E1CE7A", "#D8A4AD"],
    "pastel3": ["#8A929B", "#F2EBC1", "#D8A4AD"],
    "pastel4": ["#B2D8BE", "#F2EBC1", "#D8A4AD"],
    "pastel5": ["#8B9556", "#E1CE7A", "#D8A4AD"],
    "indifferent": ["#566246", "#D8BFAA", "#542344", "#BFD1E5", "#FED894"],
    "indifferent_pastel": [ "#879970", "#D8BFAA", "##896279", "#BFD1E5","#808080"],
    "powerpoint": ["#7DB182", "#FED894", "#8497B0", "#C9A6B7", "#BFBFBF"],
    "powerpoint_reorder": ["#7DB182", "#C9A6B7", "#8497B0", "#FED894", "#BFBFBF"],
    "powerpoint_reorder_r": ["#C9A6B7", "#7DB182", "#8497B0", "#FED894", "#BFBFBF"],
    "indifferent_mod": ["#542344", "#BFD1E5", "#79B98A", "#D8BFAA", "#808080"],
    "indifferent_mod_pastel": ["#DBA9CA", "#BFD1E5", "#D7EADC", "#D8BFAA", "#808080"],
    "likert_colors": ["#3D0B37", "#c4c2c2", "#304A47"]
}

def get_default_colormap(labels, palette='coolwarm'):
    """
    Generates a default colormap for a given set of labels.

    :param labels: A list of unique labels for which colors are needed.
    :param palette: The name of a colormap from Matplotlib's palettes. See https://matplotlib.org/stable/users/explain/colors/colormaps.html
    :return: A dictionary mapping each label to a color.
    """
    # Create a colormap using a set of colors from Matplotlib's palette
    colormap = plt.cm.get_cmap(palette, len(labels)) 

    # Assign a color to each label
    color_map = {label: colormap(i) for i, label in enumerate(labels)}

    return color_map

def get_first_colors_from_palette_as_colorlist(length, palette='tab10'):
    """
    Generates a colorlist of a set length, reommended for palettes with solid colors.

    :param length: The length of the map (integer).
    :param palette: The name of a colormap from Matplotlib's palettes. See https://matplotlib.org/stable/users/explain/colors/colormaps.html
    :return: A list of colors.
    """

    if palette in custom_color_palettes:
        colors = custom_color_palettes[palette]
        return colors[:length]
    
    cmap = plt.get_cmap(palette) # Get the 'tab10' colormap
    colors = [cmap(i) for i in range(length)]

    return colors

def get_custom_palettes():
    """
    Returns the custom color palettes available in this script.

    :return: A list of custom color palettes.
    """
    return custom_color_palettes.keys()

def get_default_colorlist(length, palette='coolwarm'):
    """
    Generates a default colorlist for a given set of labels.

    :param length: The length of the map (integer).
    :param palette: The name of a colormap from Matplotlib's palettes. See https://matplotlib.org/stable/users/explain/colors/colormaps.html
    :return: A list of colors.
    """
    cmap = plt.get_cmap(palette, length)  # You can choose other color maps like 'viridis', 'plasma', etc.
    colors = [cmap(i) for i in range(length)]

    return colors

def get_colormap_from_latex(latex_colors, latex_colors_to_labels, default_color = "#d6d6d4"):
    colors = []

    # latex_cols = """\definecolor{docsquery}{HTML}{6D4B4B}
    # \definecolor{bugident}{HTML}{A86464}
    # \definecolor{codecomp}{HTML}{E4BCAD}
    # \definecolor{codegen}{HTML}{DEDAD2}
    # \definecolor{coderef}{HTML}{6CD4C5}
    # \definecolor{conceptcomp}{HTML}{599E94}
    # \definecolor{testing}{HTML}{466964}"""

    # latex_col_to_labels = {"codegen": "Code generation", "conceptcomp": "Concept comprehension", "codecomp": "Code comprehension", "bugident": "Bug identification", "docsquery": "Basic prog. knowledge", "testing": "Testing", "coderef": "Code refinement"}

    colors = {latex_colors_to_labels[define.split("color{")[1].split("}")[0]] :  "#" + define.split("HTML}{")[1].replace("}", "") for define in latex_colors.split("\n")}
    colors["Other"] = default_color

    colors = {key: value for key, value in sorted(colors.items())}

    return colors
    
def blend_hex_colors(hex_color1, hex_color2, percentage):
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(rgb):
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    rgb1 = hex_to_rgb(hex_color1)
    rgb2 = hex_to_rgb(hex_color2)

    weight1 = percentage / 100.0
    weight2 = 1 - weight1

    blended_rgb = tuple(int(weight1 * c1 + weight2 * c2) for c1, c2 in zip(rgb1, rgb2))

    return rgb_to_hex(blended_rgb)