import requests
import os
import time
from urllib.parse import quote

# ================= CONFIGURAÇÃO =================
CATEGORIA = "Coats of arms of municipalities of Paraná"
PASTA = "brasoes_parana"
DELAY = 3          # segundos entre downloads (aumente se continuar dando 429)
MAX_RETRIES = 5
# ===============================================

os.makedirs(PASTA, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
}

def get_all_files(category):
    print("🔍 Buscando lista de arquivos...")
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmtype": "file",
        "cmlimit": 500,
        "format": "json"
    }
    
    files = []
    while True:
        r = requests.get(url, params=params, headers=headers, timeout=30)
        data = r.json()
        new_files = [item['title'] for item in data.get('query', {}).get('categorymembers', [])]
        files.extend(new_files)
        print(f"   → {len(files)} arquivos encontrados até agora")
        
        if 'continue' not in data:
            break
        params['cmcontinue'] = data['continue']['cmcontinue']
        time.sleep(1)
    
    print(f"✅ Total: {len(files)} arquivos")
    return files

def download_with_retry(filename, pasta, delay=DELAY):
    if filename.startswith("File:"):
        filename = filename[5:]
    
    safe_name = quote(filename.replace(" ", "_"))
    url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{safe_name}"
    
    filepath = os.path.join(pasta, filename.replace("/", "_").replace(":", "_"))
    
    print(f"⬇️  Baixando: {filename[:70]}...")
    
    for tentativa in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(url, headers=headers, stream=True, timeout=60)
            
            if r.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content(128*1024):
                        f.write(chunk)
                return True
            elif r.status_code == 429:
                wait = delay * tentativa
                print(f"   ⏳ 429 - Esperando {wait} segundos... (tentativa {tentativa})")
                time.sleep(wait)
            else:
                print(f"   Erro {r.status_code}")
                time.sleep(delay)
        except Exception as e:
            print(f"   Erro de conexão: {e}")
        
        time.sleep(delay)
    
    print(f"   ❌ Falhou após {MAX_RETRIES} tentativas")
    return False

# ================= EXECUÇÃO =================
arquivos = get_all_files(CATEGORIA)

print(f"\n🚀 Iniciando download de {len(arquivos)} brasões...\n")

sucesso = 0
for i, arq in enumerate(arquivos, 1):
    if download_with_retry(arq, PASTA):
        sucesso += 1
    
    if i % 15 == 0:
        print(f"   📊 Progresso: {i}/{len(arquivos)} | Sucesso: {sucesso}")
    
    time.sleep(DELAY)   # Delay principal entre cada arquivo

print(f"\n🎉 CONCLUÍDO!")
print(f"   Total baixado com sucesso: {sucesso}/{len(arquivos)}")
print(f"   Pasta: {os.path.abspath(PASTA)}")