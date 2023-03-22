import websockets
import asyncio
import base64
import json
from configure import auth_key
from windows_pipe import pipe_server_init, pipe_server_send, pipe_server_close
import numpy as np
from matplotlib import pyplot as plt
from urllib.parse import urlencode

import pyaudio
 
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()
 
# starts recording
stream = p.open(
	format=FORMAT,
	channels=CHANNELS,
	rate=RATE,
	input=True,
	frames_per_buffer=FRAMES_PER_BUFFER
)
 
# the AssemblyAI endpoint we're going to hit
sample_rate = 16000
word_boost = ["c", "d", "h", "k", "n", "o", "r", "s", "v", "z"]
params = {"sample_rate": sample_rate, "word_boost": json.dumps(word_boost)}

URL = f"wss://api.assemblyai.com/v2/realtime/ws?{urlencode(params)}"

# URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
 
async def send_receive(pipe):

	print(f'Connecting websocket to url ${URL}')

	async with websockets.connect(
		URL,
		extra_headers=(("Authorization", auth_key),),
		ping_interval=5,
		ping_timeout=20
	) as _ws:

		await asyncio.sleep(0.1)
		print("Receiving SessionBegins ...")

		session_begins = await _ws.recv()
		print(session_begins)
		print("Sending messages ...")


		async def send():
			while True:
				try:
					data = stream.read(FRAMES_PER_BUFFER)
					numpydata = np.frombuffer(data, dtype=np.int16)

					loudness = max(np.max(numpydata), -np.min(numpydata))
					data = base64.b64encode(data).decode("utf-8")
					# print('data', data)
					json_data = json.dumps({"audio_data":str(data)})
					await _ws.send(json_data)

				except websockets.exceptions.ConnectionClosedError as e:
					print(e)
					assert e.code == 4008
					break

				except Exception as e:
					assert False, "Not a websocket 4008 error"

				await asyncio.sleep(0.01)
		  
			return True
	  

		async def receive():
			while True:
				try:
					result_str = await _ws.recv()
					# print(json.loads(result_str)['text'])
					if json.loads(result_str)['text'] != '':
						pipe_server_send(pipe, json.loads(result_str)['text'])

				except websockets.exceptions.ConnectionClosedError as e:
					print(e)
					assert e.code == 4008
					break

				except Exception as e:
					assert False, "Not a websocket 4008 error"
	  
		send_result, receive_result = await asyncio.gather(send(), receive())

		print(receive_result)

while True:
	pipe = pipe_server_init()
	try:
		asyncio.run(send_receive(pipe))
	finally:
		pipe_server_close(pipe)