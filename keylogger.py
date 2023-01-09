import keyboard

LOGFILE_PATH = '/home/jorge/fun/kbfrequency/keys.txt'

logfile = open('/home/jorge/fun/keys.txt', 'w')

def callback(ev):
    text =  f'{ev.name}-{ev.scan_code}\n'
    print(text, end='')
    logfile.write(text)
    logfile.flush()

if __name__ == '__main__':
    keyboard.on_release(callback)
    keyboard.wait()
