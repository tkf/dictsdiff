from subprocess import check_output


def get_terminal_size_stty():
    with open('/dev/tty') as stdin:
        out = check_output(['stty', 'size'], stdin=stdin)
    rows, columns = map(int, out.decode().strip().split())
    return columns, rows
