
def getBarColor(charge: float):
    bar_color_component = int(charge * 255)
    bar_color = (bar_color_component, 0, 255 - bar_color_component)
    return bar_color
