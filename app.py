from flask import Flask, request, Response, render_template_string
import yt_dlp
from io import BytesIO
import os

app = Flask(__name__)

# Configurações do yt_dlp
ydl_opts = {
    'format': '233',
    'merge_output_format': 'mp4',
    'noplaylist': True,
    'progress_hooks': [lambda d: d.get('status') == 'finished']
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            # Usa um buffer em memória para o vídeo
            buffer = BytesIO()

            # Faz o download do vídeo para o buffer
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_file = ydl.prepare_filename(info)

                with open(video_file, 'rb') as f:
                    buffer.write(f.read())

                buffer.seek(0)
                os.remove(video_file)  # Remove o arquivo temporário após o download

            # Envia o buffer como resposta
            return Response(
                buffer,
                mimetype='video/mp4',
                headers={'Content-Disposition': f'attachment; filename="{info["title"]}.mp4"'}
            )
        except Exception as e:
            return f"An error occurred: {e}"
    
    # HTML para o formulário de entrada
    html_form = '''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Download YouTube Video</title>
    </head>
    <body>
        <h1>Download YouTube Video</h1>
        <form method="post">
            <label for="url">YouTube URL:</label>
            <input type="text" id="url" name="url" required>
            <button type="submit">Download</button>
        </form>
    </body>
    </html>
    '''
    return render_template_string(html_form)

if __name__ == '__main__':
    app.run(debug=True)
