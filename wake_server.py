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
  <title>PC Remote Panel</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Inter', sans-serif; }
    .fade-in {
      animation: fadeIn 0.8s ease-in-out;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>
<body class="bg-[#0f172a] text-white min-h-screen flex">
  <!-- Sidebar -->
  <aside class="w-20 bg-[#1e293b] flex flex-col items-center py-6 space-y-6">
    <div class="text-blue-400 text-3xl font-bold">⚡</div>
    <button title="Wake" class="text-blue-400 hover:text-white text-xl">🔌</button>
    <button title="Stats" class="text-blue-400 hover:text-white text-xl">📊</button>
    <button title="Settings" class="text-blue-400 hover:text-white text-xl">⚙️</button>
  </aside>

  <!-- Main panel -->
  <main class="flex-1 p-10 fade-in">
    <h1 class="text-4xl font-semibold text-cyan-300 mb-6">PC Remote Panel</h1>

    <!-- Status -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div class="bg-[#1e293b] rounded-xl p-6 shadow-md">
        <h2 class="text-lg font-semibold mb-2">Wake PC</h2>
        <p class="text-sm mb-4" style="color: {{ status_color }}">{{ status }}</p>
        <form action="/wake" method="post">
          <button class="w-full py-3 bg-blue-600 hover:bg-blue-500 rounded-lg font-semibold shadow">Wake</button>
        </form>
      </div>

      <div class="bg-[#1e293b] rounded-xl p-6 shadow-md">
        <h2 class="text-lg font-semibold mb-4">System Stats</h2>
        <p class="text-sm mb-2">CPU Usage: <span class="font-semibold text-cyan-300">{{ cpu }}%</span></p>
        <p class="text-sm">RAM: <span class="font-semibold text-cyan-300">{{ ram }}</span></p>
      </div>

      <div class="bg-[#1e293b] rounded-xl p-6 shadow-md">
        <h2 class="text-lg font-semibold mb-4">System Temperature</h2>
        <p class="text-sm">Coming soon...</p>
      </div>
    </div>

    <footer class="mt-10 text-xs text-gray-400">
      Powered by Flask • {{ username }}'s Panel
    </footer>
  </main>
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
