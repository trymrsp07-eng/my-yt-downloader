from flask import Flask, render_template_string, request, send_file
import yt_dlp
    if file_format == 'audio':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(downloads_dir, '%(id)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            },
        }
    else:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(downloads_dir, '%(id)s.%(ext)s'),
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            },
        }

import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="gu">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Downloader</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-white min-h-screen flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-gray-800 p-6 rounded-xl shadow-lg">
        <h1 class="text-2xl font-bold text-center mb-6 text-red-500">YouTube Downloader</h1>
        
        <form action="/download" method="POST" class="space-y-4">
            <input type="text" name="url" placeholder="YouTube લિંક અહીં પેસ્ટ કરો..." required
                class="w-full p-3 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:border-red-500 text-white">
            
            <select name="format" class="w-full p-3 rounded bg-gray-700 border border-gray-600 focus:outline-none focus:border-red-500 text-white">
                <option value="video">MP4 (Video)</option>
                <option value="audio">MP3 (Audio)</option>
            </select>
            
            <button type="submit" 
                class="w-full bg-red-600 hover:bg-red-700 text-white font-bold p-3 rounded transition duration-200">
                ડાઉનલોડ કરો
            </button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    file_format = request.form.get('format')
    
    downloads_dir = 'downloads'
    os.makedirs(downloads_dir, exist_ok=True)
    
    if file_format == 'audio':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(downloads_dir, '%(id)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(downloads_dir, '%(id)s.%(ext)s'),
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if file_format == 'audio':
                filename = os.path.splitext(filename)[0] + '.mp3'
            
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"ડાઉનલોડ કરતી વખતે ભૂલ આવી: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
