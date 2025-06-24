from flask import Flask, request, render_template_string
from wakeonlan import send_magic_packet
import os
import subprocess
import getpass

app = Flask(__name__)

MAC_ADDRESS = '74:56:3C:68:50:22'
IP_PC = '192.168.1.91'

USERNAME = getpass.getuser()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>PC Remote Control</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-black text-white flex items-center justify-center min-h-screen p-4">
    <div class="text-center space-y-6">
        <h1 class="text-2xl font-bold text-yellow-400">PC Remote Control</h1>
        <p class="text-sm" style="color: {{ status_color }}">{{ status }}</p>
        <form action="/wake" method="post">
            <button class="w-full py-3 px-8 bg-green-600 hover:bg-green-700 rounded-lg font-semibold">Wake</button>
        </form>
        <footer class="text-xs text-gray-400 mt-4">Powered by Flask • {{ username }}'s Panel</footer>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    response = os.system(f"ping -c 1 -W 1 {IP_PC} > /dev/null 2>&1")
    status = "PC is Online" if response == 0 else "PC is Offline"
    status_color = "#22c55e" if response == 0 else "#ef4444"
    return render_template_string(HTML_TEMPLATE, status=status, status_color=status_color, username=USERNAME)

@app.route('/wake', methods=['POST'])
def wake():
    send_magic_packet(MAC_ADDRESS)
    return 'Sent magic packet!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=41264)
