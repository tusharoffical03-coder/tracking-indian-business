from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import pandas as pd
import os
from analyzer.sales_expert import SalesExpert

app = FastAPI()
expert = SalesExpert()
DATA_FILE = "leads_final.csv"

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    leads = []
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        leads = df.to_dict('records')

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"><title>LeadCommand AI</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest"></script>
    </head>
    <body class="bg-gray-900 text-gray-100 font-sans">
        <div class="max-w-7xl mx-auto p-6">
            <div class="flex justify-between items-center mb-10">
                <h1 class="text-3xl font-bold text-blue-400">LeadCommand AI</h1>
                <a href="/download" class="bg-gray-800 px-4 py-2 rounded-lg border border-gray-700 flex items-center">
                    <i data-lucide="download" class="mr-2"></i> Export CSV
                </a>
            </div>

            <div class="bg-gray-800 rounded-xl border border-gray-700 overflow-hidden">
                <table class="w-full text-left">
                    <thead class="bg-gray-900 text-gray-400 uppercase text-xs">
                        <tr>
                            <th class="px-6 py-4">Name</th><th class="px-6 py-4">Phone</th><th class="px-6 py-4">Status</th><th class="px-6 py-4">Action</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-700">
                        {"".join([f'''
                        <tr>
                            <td class="px-6 py-4">{l['business_name']}</td>
                            <td class="px-6 py-4">{l['phone']}</td>
                            <td class="px-6 py-4">{l['lead_score']}</td>
                            <td class="px-6 py-4">
                                <button onclick="showPitch('{l['business_name'].replace("'", "\\'")}', `{l['generated_pitch'].replace("`", "\\`")}`)" class="text-blue-400 underline mr-4">View Pitch</button>
                                <a href="https://wa.me/{str(l['phone']).replace('+','').replace(' ', '')}" target="_blank" class="text-green-400 underline">WhatsApp</a>
                            </td>
                        </tr>
                        ''' for l in leads])}
                    </tbody>
                </table>
            </div>

            <div class="mt-10 p-6 bg-blue-900/10 border border-blue-900/30 rounded-xl">
                <h3 class="text-lg font-bold mb-4">AI Objection Handler</h3>
                <div id="chat-box" class="h-32 overflow-y-auto mb-4 p-4 bg-gray-900 rounded border border-gray-700 text-sm">
                    <p class="text-gray-500 italic">Chat with the Sales Agent...</p>
                </div>
                <div class="flex space-x-2">
                    <input id="chat-input" type="text" placeholder="Type an objection (e.g. 'too expensive')..." class="bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 flex-grow">
                    <button onclick="askAI()" class="bg-blue-600 px-6 py-2 rounded-lg font-bold">Ask AI</button>
                </div>
            </div>
        </div>

        <!-- Modal -->
        <div id="modal" class="hidden fixed inset-0 bg-black/50 flex items-center justify-center p-4">
            <div class="bg-gray-800 p-8 rounded-xl max-w-lg border border-gray-700 shadow-2xl">
                <h2 id="modal-title" class="text-xl font-bold mb-4"></h2>
                <p id="modal-content" class="text-gray-300 leading-relaxed mb-6"></p>
                <button onclick="document.getElementById('modal').classList.add('hidden')" class="bg-blue-600 px-6 py-2 rounded-lg font-bold">Close</button>
            </div>
        </div>

        <script>
            lucide.createIcons();
            function showPitch(name, pitch) {{
                document.getElementById('modal-title').innerText = "Pitch for " + name;
                document.getElementById('modal-content').innerText = pitch;
                document.getElementById('modal').classList.remove('hidden');
            }}
            async function askAI() {{
                const input = document.getElementById('chat-input').value;
                const response = await fetch('/ask?q=' + encodeURIComponent(input));
                const data = await response.json();
                const box = document.getElementById('chat-box');
                box.innerHTML += `<p class='text-blue-400 font-bold'>You: </p><p class='mb-2'>${{input}}</p>`;
                box.innerHTML += `<p class='text-green-400 font-bold'>Agent: </p><p class='mb-4'>${{data.reply}}</p>`;
                document.getElementById('chat-input').value = "";
                box.scrollTop = box.scrollHeight;
            }}
        </script>
    </body>
    </html>
    """
    return html_content

@app.get("/ask")
async def ask(q: str):
    reply = expert.handle_objection(q)
    return JSONResponse({{"reply": reply}})

@app.get("/download")
async def download_csv():
    from fastapi.responses import FileResponse
    return FileResponse(DATA_FILE, media_type='text/csv', filename="leads_export.csv")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
