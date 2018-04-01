import subprocess


def get_clipboard():
    p = subprocess.Popen(['xclip','-selection', 'clipboard', '-o'], stdout=subprocess.PIPE)
    p.wait()
    data = p.stdout.read()
    return data.decode(encoding="utf-8")