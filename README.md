# Zero Day Singularity (ZDS) podcast editor

<!-- Logo -->

## 📌 Resumen

Este repositorio contiene una librería y herramientas para editar y procesar el audio del podcast Zero Day Singularity (ZDS). El podcast se enfoca en discusiones profundas sobre la singularidad tecnológica, el rápido avance de la inteligencia artificial (IA), y sus implicaciones en la sociedad, la economía y el futuro de la humanidad.

La librería está diseñada para facilitar la edición de audio, permitiendo tareas como la división del audio en segmentos basados en silencios, la inserción de pistas de fondo, la normalización de volumen, y la exportación del audio final. Además, se incluyen libros de Jupyter Notebook que permiten automatizar y personalizar el proceso de edición.

## 🎯 Características principales
Detección de silencios: Divide el audio en segmentos basados en silencios detectados, lo que facilita la edición y reorganización del contenido.

Inserción de pistas de fondo: Permite agregar música de fondo, efectos de sonido, o transiciones entre segmentos.

Corte y unión de audio: Corta y une segmentos de audio de manera sencilla, con opciones para aplicar fundidos de entrada y salida.

Exportación flexible: Exporta el audio final en formato MP3 o cualquier otro formato compatible con pydub.

Automatización: Los libros de Jupyter Notebook permiten automatizar el proceso de edición, lo que ahorra tiempo y esfuerzo en la producción del podcast.

## ✨ Ejemplos de uso

- 🔗 **[Notebook editor in GitHub](zds_editor.ipynb)**
- [![Open in Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Turing-IA-IHC/InfarctImage/blob/main/zds_editor.ipynb)

- 🔗 **[Notebook utils in GitHub](zds_utils.ipynb)**
- [![Open in Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Turing-IA-IHC/InfarctImage/blob/main/zds_utils.ipynb)


1. Carga de audios
```python
import zds_utils as zds
from pydub import AudioSegment

# Cargar el archivo de audio
audio = AudioSegment.from_file("podcast_episode.mp3")
```

2. Dividir y guardar el audio en segmentos basados en silencios
```python
# Detecta silencios y corta el audio
chunks = silence.split_on_silence(audio, min_silence_len=3000, silence_thresh=-40)

# Guardar los segmentos en archivos separados
zds.chunks_save(chunks, "output_folder")
```

3. Insertar música de fondo en segmentos específicos
```python
# Cargar una pista de fondo
background_music = AudioSegment.from_file("background_music.mp3")

# Insertar la pista de fondo en un segmento específico
final_audio = zds.audio_overlay(audio_segment, background_music, position=5000, fade_in=1000, fade_out=2000)
```

4. Cortar un segmento de audio y aplicar difuminación
```python
# Cortar un segmento de audio desde 00:01:00 hasta 00:02:30
cut_audio, new_file_path = zds.audio_cut("podcast_episode.mp3", start_time="00:01:00", end_time="00:02:30", fade_in=1000, fade_out=2000)

# Guardar el segmento cortado
cut_audio.export("cut_segment.mp3", format="mp3")
```

5. Compilar el audio final con introducción y cierre
```python
# Cargar los segmentos de introducción y cierre
intro = AudioSegment.from_file("intro.mp3")
outro = AudioSegment.from_file("outro.mp3")

# Compilar el audio final
final_audio = intro + audio_segment + outro

# Guardar el audio final
final_audio.export("final_podcast.mp3", format="mp3")
```

## 🏗️ Instalación
Para utilizar esta librería, necesitas instalar las dependencias necesarias. Puedes hacerlo ejecutando el siguiente comando:

```bash
pip install pydub scipy
```
Además, asegúrate de tener instalado ffmpeg o libav en tu sistema, ya que pydub lo requiere para manejar formatos de audio.

### En Ubuntu/Debian
```bash
sudo apt-get install ffmpeg
```

### En macOS (usando Homebrew)
```bash
brew install ffmpeg
```

## 🤝 Contribuciones
¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar la librería o quieres agregar nuevas funcionalidades, no dudes en hacer un fork del repositorio y enviar un pull request.

## 🧙‍♂️ Sobre el Podcast
Zero Day Singularity (ZDS) es un podcast que explora el futuro de la tecnología, la inteligencia artificial y la singularidad tecnológica. Cada episodio presenta discusiones profundas sobre cómo el rápido avance de la IA está transformando nuestra sociedad y qué podemos esperar en las próximas décadas.

Escucha el podcast aquí <!-- Agrega el enlace a tu podcast si lo tienes disponible -->

Síguenos en redes sociales <!-- Agrega enlaces a tus redes sociales si las tienes -->
