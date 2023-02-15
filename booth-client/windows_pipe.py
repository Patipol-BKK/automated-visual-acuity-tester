import time
import sys
import win32pipe, win32file, pywintypes


def pipe_server_init():
    print("Opening Pipe")
    count = 0
    pipe = win32pipe.CreateNamedPipe(
        r'\\.\pipe\Foo',
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1, 65536, 65536,
        0,
        None)
    try:
        print("Waiting for client connection")
        win32pipe.ConnectNamedPipe(pipe, None)
        print("Client Connected")

        return pipe
    except:
        win32file.CloseHandle(pipe)

def pipe_server_send(pipe, msg):
    try:
        # print(msg)
        # convert to bytes
        some_data = str.encode(msg)
        win32file.WriteFile(pipe, some_data)
    except:
        print("Error sending")

def pipe_server_close(pipe):
    win32file.CloseHandle(pipe)

def pipe_client_init():
    try:
        handle = win32file.CreateFile(
                r'\\.\pipe\Foo',
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None
            )
        res = win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
        if res == 0:
            print(f"SetNamedPipeHandleState return code: {res}")

        return handle
    except pywintypes.error as e:
        if e.args[0] == 2:
            print("No pipe, trying to reconnect...")
            time.sleep(1)
        elif e.args[0] == 109:
            print("Broken pipe, exiting program...")
            quit = True
def pipe_client_read(handle):
    resp = win32file.ReadFile(handle, 64*1024)
    # print(f"Recieved: {resp}")
    return resp[1].decode("ascii")
    