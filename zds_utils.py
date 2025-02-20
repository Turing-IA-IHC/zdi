"""
This class was made for zero days ingularity project.
Athor: Gavit0
Mail: zerodaysingularity@gmail.com
"""
__version__ = "0.1"
__author__ = "Gavit0"

import os
import sys
import time
from pydub import AudioSegment, silence

# Función para mostrar milisegundos en formato hh:mm:ss.ms
def ms_to_time(ms, shortest=False):
	"""
	Convierte milisegundos a una cadena con el formato hh:mm:ss.ms
	
	Parámetros:
		ms (int): Duración en milisegundos
		shortest (bool): Si se desea mostrar solo las partes significativas del tiempo (por defecto False)
			
	Retorna:
		str: Cadena con el tiempo formateado
	"""
	hours = ms // 3600000
	minutes = (ms % 3600000) // 60000
	seconds = (ms % 60000) // 1000
	milliseconds = ms % 1000
	if shortest:
		if hours > 0:
			return f"{hours:02}:{minutes:02}:{seconds:02}"
		else:
			return f"{minutes:02}:{seconds:02}"
	else:
		if hours > 0:
			return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"
		else:
			return f"{minutes:02}:{seconds:02}.{milliseconds:03}"

# Función que recibe una hora en formato hh:mm:ss.ms y la convierte a milisegundos
def time_to_ms(hms):
	"""
	Convierte una cadenas con el formato hh:mm:ss.ms, hh:mm:ss o mm:ss a milisegundos.
	
	Parámetros:
		hms (str): Cadena con el tiempo formateado
	Retorna:
		int: Duración en milisegundos
	"""
	parts = hms.split(":")
	if len(parts) == 3:
		hours = int(parts[0])
		minutes = int(parts[1])
		seconds = float(parts[2])
	elif len(parts) == 2:
		hours = 0
		minutes = int(parts[0])
		seconds = float(parts[1])
	else:
		raise ValueError("Formato de tiempo incorrecto")
	return int((hours * 3600 + minutes * 60 + seconds) * 1000)


# Función para extraer audio de un archivo de video
def audio_from_video(video_path, audio_path=None, verbose=False):
	"""
	Extrae el audio de un archivo de video y lo guarda en un archivo mp3.
	
	Parámetros:
		video_path (str): Ruta del archivo de video.
		audio_path (str): Ruta del archivo de audio de salida. Si no se especifica, se guarda en el mismo directorio que el video.
		verbose (bool): Si se desea mostrar mensajes de información.

	Retorna:
		str: Ruta del archivo de audio de salida.
	"""
	ext = video_path.split(".")[-1]
	if audio_path is None:
		audio_path = video_path.replace(f".{ext}", ".mp3")

	AudioSegment.from_file(video_path).export(audio_path, format="mp3")
	if verbose:
		print(f"File {video_path} converted to {audio_path}")
	return audio_path

# Función para unir	los chunks y guardar de audio en un solo archivo
def audio_save(audio_chunks, output_file, verbose=False):
	"""
	Guarda los chunks de audio en un solo archivo.
	
	Parámetros:
		audio_chunks (tuple or list): Si es Tuple es el audio compilado si es List son los chuncks para unir.
		output_file (str): Nombre del archivo de salida.
		verbose (bool): Si se desea mostrar mensajes de	información.

	"""
	# Concatenar los chunks de audio si es una lista
	if isinstance(audio_chunks, list):
		audio = sum(audio_chunks)
	else:
		audio = audio_chunks
	# Guardar el archivo de audio
	audio.export(output_file)
	if verbose:
		print(f"Se ha guardado el archivo de audio en '{output_file}'")

# Función para cortar un archivo de audio
def audio_cut(file_path, start_time='00:00:00', end_time='59:59:59', 
							auto_save=True, new_file_path=None,
							fade_in=None, fade_out=None, verbose=False):
	"""
	Corta un archivo de audio en un rango de tiempo específico.

	Parámetros:
		file_path (str): Ruta del archivo de audio.
		start_time (str): Tiempo de inicio del corte en formato HH:MM:SS.
		end_time (str): Tiempo de fin del corte en formato HH:MM:SS.
		auto_save (bool): Si se desea guardar el archivo cortado.
		new_file_path (str): Ruta del archivo de salida.
		fade_in (int): Duración del fundido de entrada.
		fade_out (int): Duración del fundido de salida.
		verbose (bool): Si se desea mostrar mensajes de información.

	Retorna:
		AudioSegment: Fragmento de audio cortado.
		str: Ruta del archivo de salida.
	"""
	ext = file_path.split(".")[-1]
	audio = AudioSegment.from_file(file_path)
	start= time_to_ms(start_time)
	end = time_to_ms(end_time)
	audio = audio[start:end]
	if fade_in:
		audio = audio.fade_in(fade_in)
	if fade_out:
		audio = audio.fade_out(fade_out)
	if auto_save and new_file_path is None:
		new_file_path = file_path.replace(f".{ext}", f"_{start_time.replace(':','')}_{end_time.replace(':','')}.mp3")
	if new_file_path is not None:
		audio.export(new_file_path)
	if verbose:
		print(f"File {file_path} cut successfully. New file saved as {new_file_path}.")
	return audio, new_file_path

# Función para sobreponer un audio sobre otro
def audio_overlay(audio, background, audio_volume=0, background_volume=-20, 
									position=0, fade_in=None, fade_out=None):
	"""
	Sobreponer un audio sobre otro.

	Parámetros:
		audio (AudioSegment): Audio principal.
		background (AudioSegment): Audio de fondo.
		audio_volume (int): Reducción o aumento de volumen del audio principal (por defecto 0dB).
		background_volume (int): Reducción o aumento de volumen del fondo (por defecto -20dB).
		position (int): Posición en la que se superpondrá el audio de fondo.
		fade_in (int): Duración del fundido de entrada.
		fade_out (int): Duración del fundido de salida.

	Retorna:
		AudioSegment: Audio con la sobreposición.
	"""	
	audio = audio + audio_volume
	# Reducir el volumen del fondo (por ejemplo, -20dB)
	background_track = background + background_volume
	# Extender el audio de fondo para que cubra toda la duración del audio principal
	background_loop = background_track * (len(audio) // len(background_track) + 1)
		
	# Mezclar el fondo con el audio principal
	final_audio = audio.overlay(background_loop, position=position)

	if fade_in is not None:
		final_audio = final_audio.fade_in(fade_in)
	if fade_out is not None:
		final_audio = final_audio.fade_out(fade_out)
	return final_audio


# Función para agregar un intermedio entre 2 chunks de audio
def chuncks_insert(chunks, position, inter, fade_in=None, fade_out=None):
	"""
	Inserta un audio en una posición específica de la lista de chunks y aplica un fundido de salida.

	Parámetros:
		chunks (list): Lista de AudioSegment, fragmentos de audio.
		position (int): Índice donde se insertará el audio intermedio.
		inter (AudioSegment): Audio a insertar.
		fade_in (int): Duración del fundido de entrada.
		fade_out (int): Duración del fundido de salida.

	Retorna:
		list: Lista de AudioSegment con el audio intermedio insertado.
	"""
	if position < 0 or position >= len(chunks):
		raise ValueError("La posición está fuera del rango de los chunks disponibles.")
	
	if fade_in is not None:
		inter = inter.fade_in(fade_in)
	if fade_out is not None:
		inter = inter.fade_out(fade_out)
	
	# Insertar el audio en la posición deseada
	new_chunks = chunks[:position] + [inter] + chunks[position:]
	
	return new_chunks

# Función para alamcenar cada chunk en un archivo separado
def chunks_save(chunks, output_folder, format="mp3", verbose=False):
	"""
	Guarda cada chunk de audio en un archivo separado.

	Parámetros:
		chunks (list): Lista de AudioSegment, fragmentos de audio.
		output_folder (str): Carpeta de salida.
		format (str): Formato de los archivos de audio (por defecto 'mp3').
		verbose (bool): Si se desea mostrar mensajes de información.		
	"""
	# Crear la carpeta de salida si no existe
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)	
	# Guardar cada chunk de audio en un archivo separado
	for i, chunk in enumerate(chunks):
		chunk.export(f"{output_folder}/chunk_{i:03}.{format}")
		if verbose:
			print(f"Se ha guardado el chunk {i:03} en '{output_folder}/chunk_{i:03}.{format}'")

# Cargar los archivos de audio (chunks) en una sola variable
def chunks_load(folder_path, format="mp3", verbose=False):
	"""
	Carga los fragmentos de audio en una lista de AudioSegment.

	Parámetros:
		folder_path (str): Ruta de la carpeta con los fragmentos de audio.
		format (str): Formato de los archivos de audio (por defecto 'mp3').
		verbose (bool): Si se desea mostrar mensajes de información.

	Retorna:
		list: Lista de AudioSegment con los fragmentos de audio.
	"""
	chunks = []

	if not os.path.exists(folder_path):
		print(f"La carpeta '{folder_path}' no existe.")
		return chunks

	for file in sorted(os.listdir(folder_path)):
		if file.endswith(f".{format}"):
			chunk = AudioSegment.from_file(f"{folder_path}/{file}")
			chunks.append(chunk)
			if verbose:
				print(f"Se ha cargado el archivo '{file}'")
	return chunks


# Función para guardar la información de los silencios en un archivo de texto
def silences_save(silences, output_file, verbose=False):
	"""
	Guarda la información de los fragmentos de silencio en un archivo de texto.

	Parámetros:
		silences (list): Lista de tuplas con los fragmentos de silencio.
		output_file (str): Nombre del archivo de salida.
		verbose (bool): Si se desea mostrar mensajes de información.
	"""
	with open(output_file, "w") as file:
		file.write(f"Silence\tStart\tEnd\tDuration\n")
		for i, (start, end) in enumerate(silences):
			file.write(f"{i + 1}\t{start}\t{end}\t{end - start}\n")
		if verbose:
			print(f"Se ha guardado la información de los silencios en '{output_file}'")

			# Función para cargar la información de los silencios desde un archivo de texto

# Función para cargar la información de los silencios desde un archivo de texto
def silences_load(file_path, verbose=False):
	"""
	Carga la información de los fragmentos de silencio desde un archivo de texto.

	Parámetros:
		file_path (str): Ruta del archivo de texto.
		verbose (bool): Si se desea mostrar mensajes de información.

	Retorna:
		list: Lista de tuplas con los fragmentos de silencio.
	"""
	silences = []

	if not os.path.exists(file_path):
		print(f"El archivo '{file_path}' no existe.")
		return silences
	
	with open(file_path, "r") as file:
		lines = file.readlines()
		for line in lines[1:]:
			parts = line.strip().split("\t")
			start = int(parts[1])
			end = int(parts[2])
			silences.append((start, end))
		if verbose:
			print(f"Se han cargado los silencios del archivo '{file_path}'")
	return silences

# Función que retorna la posición de los silencios que superan el umbral de tiempo
def silences_of_length(silences, silence_length):
	"""
	Obtiene las posiciones de los fragmentos de silencio en el audio que superan el umbral de duración.

	Parámetros:
		silences (list): Lista de tuplas con los fragmentos de silencio.
		silence_length (int): Duración mínima de los fragmentos de silencio.
	"""
	return [(i, start, end, end - start) for i, (start, end) in enumerate(silences) if end - start >= silence_length]