import os
import re

sidebar_dir = "sidebar"

# Mapeia nomes antigos para novos nomes amigáveis
file_map = {}
for filename in os.listdir(sidebar_dir):
    if filename.endswith(".html"):
        # Gera um padrão para busca baseado no nome amigável
        base = filename.replace('.html', '')
        # Remove prefixos comuns para facilitar o match
        base_clean = re.sub(r'^eproc-|^sistema-eproc-', '', base)
        file_map[base_clean.replace('-', ' ')] = filename

# Atualiza os links internos em todos os arquivos HTML
for filename in os.listdir(sidebar_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(sidebar_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        original_content = content
        # Substitui links antigos por novos nomes amigáveis
        for key, new_name in file_map.items():
            # Regex para encontrar links que contenham parte do nome antigo
            content = re.sub(r'href=["\"][^"\"]*' + re.escape(key) + r'[^"\"]*["\"]', f'href="{new_name}"', content, flags=re.IGNORECASE)
        if content != original_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Links atualizados em: {filename}")
print("Atualização de links concluída.")
