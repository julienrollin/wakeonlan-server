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
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Inter', sans-serif; }
    .fade-in { animation: fadeIn 0.8s ease-in-out; }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>
<body class="bg-[#0f1624] text-[#e5e5e5] flex items-center justify-center min-h-screen p-4">
  <div class="fade-in text-center space-y-6 bg-[#0a0b12] px-10 py-8 rounded-2xl shadow-xl border border-[#1c1f2e] max-w-md w-full">
    <h1 class="text-3xl font-bold text-[#2962ff] tracking-wide">PC Remote Control</h1>
    <p class="text-sm font-medium" style="color: {{ status_color }}">{{ status }}</p>
    <button id="wakeButton" onclick="sendMagicPacket()" class="w-full py-3 px-8 bg-[#2962ff] hover:bg-[#1e4ed8] transition-all duration-200 rounded-lg font-semibold shadow-md text-white">Wake</button>
    <footer class="text-xs text-gray-500 mt-4">Powered by Flask • {{ username }}'s Panel</footer>
  </div>

  <script>
    function sendMagicPacket() {
      const btn = document.getElementById('wakeButton');
      btn.disabled = true;
      btn.innerText = 'Sending...';
      fetch('/wake', { method: 'POST' })
        .then(res => {
          if (res.ok) {
            btn.innerText = 'Magic Packet Sent!';
            btn.classList.remove('bg-[#2962ff]');
            btn.classList.add('bg-green-600');
            setTimeout(() => {
              btn.innerText = 'Wake';
              btn.classList.remove('bg-green-600');
              btn.classList.add('bg-[#2962ff]');
              btn.disabled = false;
            }, 2000);
          } else {
            btn.innerText = 'Failed!';
            btn.classList.remove('bg-[#2962ff]');
            btn.classList.add('bg-red-600');
            setTimeout(() => {
              btn.innerText = 'Wake';
              btn.classList.remove('bg-red-600');
              btn.classList.add('bg-[#2962ff]');
              btn.disabled = false;
            }, 2000);
          }
        });
    }
  </script>
</body>
</html>
"""

@app.route('/')
def home():
    response = os.system(f"ping -c 1 -W 1 {IP_PC} > /dev/null 2>&1")
    status = "PC is Online" if response == 0 else "PC is Offline"
    status_color = "#00e676" if response == 0 else "#ff5252"
    return render_template_string(HTML_TEMPLATE, status=status, status_color=status_color, username=USERNAME)

@app.route('/wake', methods=['POST'])
def wake():
    send_magic_packet(MAC_ADDRESS)
    return 'Sent magic packet!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=41264)
