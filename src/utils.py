'''Utils for convenience'''

from click import style

# Console ascii-color helpers
def error(string, bg=False):
    return style(string, bg='red', bold=True) if bg else style(string, fg='red', bold=True)

def success(string, bg=False):
    return style(string, bg='green', bold=True) if bg else style(string, fg='green', bold=True)

def warning(string, bg=False):
    return style(string, bg='yellow', bold=True) if bg else style(string, fg='yellow', bold=True)
