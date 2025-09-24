import os
import re
import unicodedata

# Caminho da pasta sidebar
sidebar_dir = "sidebar"

def slugify(value):
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    value = re.sub(r'[-\s]+', '-', value)
    return value

for filename in os.listdir(sidebar_dir):
    if filename.endswith(".html"):
        # Extrai o nome base sem data/hora
        base = filename.split('：')[1] if '：' in filename else filename
        base = base.split('(')[0].strip()
        novo_nome = slugify(base) + ".html"
        old_path = os.path.join(sidebar_dir, filename)
        new_path = os.path.join(sidebar_dir, novo_nome)
        if not os.path.exists(new_path):
            os.rename(old_path, new_path)
            print(f"{filename} -> {novo_nome}")
        else:
            print(f"Arquivo já existe: {novo_nome}")
print("Renomeação concluída.")
