import sys
import re

# pip install markdown
from markdown import markdown


class AlertStyler:

    _style = {
        'margin-bottom': '20px',
        'border': '1px solid transparent',
        'border-radius': '4px',
        'padding': '15px',
    }

    _style_code_area = {
        'font-family': 'Consolas',
        'padding': '0',
        'padding-top': '.2em',
        'padding-bottom': '.2em',
        'margin': '0',
        # 'font-size': '85%',
        'background-color': 'rgba( 0, 0, 0, .04 )',
        'border-radius': '3px',
        'border': 0
    }

    def get_alert_area_style(self):
        return AlertStyler._style

    def get_code_area_style(self):
        return AlertStyler._style_code_area


class AlertStylerWarning(AlertStyler):

    _style = {
        'color': '#8a6d3b',
        'background-color': '#fcf8e3',
        'border-color': '#faebcc',
    }

    def get_alert_area_style(self):
        return {
            **super().get_alert_area_style(),
            **AlertStylerWarning._style,
        }


class AlertStylerInfo(AlertStyler):

    _style = {
        'color': '#31708f',
        'background-color': '#d9edf7',
        'border-color': '#bce8f1',
    }

    def get_alert_area_style(self):
        return {
            **super().get_alert_area_style(),
            **AlertStylerInfo._style,
        }


class AlertStylerSuccess(AlertStyler):

    _style = {
        'color': '#3c763d',
        'background-color': '#dff0d8',
        'border-color': '#d6e9c6',
    }

    def get_alert_area_style(self):
        return {
            **super().get_alert_area_style(),
            **AlertStylerSuccess._style,
        }


class AlertStylerDanger(AlertStyler):

    _style = {
        'color': '#a94442',
        'background-color': '#f2dede',
        'border-color': '#ebccd1',
    }

    def get_alert_area_style(self):
        return {
            **super().get_alert_area_style(),
            **AlertStylerDanger._style,
        }


def format_style(style_dict):
    return '; '.join("%s: %s" % (val, prop) for val, prop in style_dict.items())


def get_alert_styler(alert_type):
    if alert_type == 'info':
        return AlertStylerInfo()
    elif alert_type == 'warning':
        return AlertStylerWarning()
    elif alert_type == 'success':
        return AlertStylerSuccess()
    else:  # alert_type == 'danger'
        return AlertStylerDanger()


def convert_to_html(content, styler):

    alert_style = format_style(styler.get_alert_area_style())
    code_style = format_style(styler.get_code_area_style())

    html = markdown(content)
    html = html.replace('<code>', f'<code style="{code_style}">')
    html = html.replace('<p>', f'<p style="margin: 0">')

    return f'<div style="{alert_style}">{html}</div>'


def main(filename_in, filename_out):

    with open(filename_in, encoding='UTF-8') as f:
        content = f.read()

    pos = 0
    flags = re.MULTILINE | re.DOTALL
    regex = re.compile(r'^(:::(info|warning|success|danger)\n.*?\n:::)', flags)

    with open(filename_out, 'w', encoding='UTF-8') as of:
        for match in re.finditer(regex, content):
            alert_content = match.group()[3:-3]
            first_newline = alert_content.find('\n')
            alert_type = alert_content[:first_newline]
            alert_payload = alert_content[first_newline:]

            html = convert_to_html(alert_payload, get_alert_styler(alert_type))
            of.write(content[pos:match.start()])
            pos = match.end() + 1
            of.write(html)

            print('\rProcessing item at: %i' % pos, end='')


def usage():
    print('Usage: python3 alert-styler.py <input-file> <output-file>')

if __name__ == "__main__":

    if len(sys.argv) != 3:
        usage()
        exit(1)

    main(sys.argv[1], sys.argv[2])
    print('\rFinished%s\n' % (' ' * 30))
