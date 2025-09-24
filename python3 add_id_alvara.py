import os
import re

# Caminho da pasta sidebar
sidebar_dir = "sidebar"

# Regex para encontrar o <a ...> com o texto desejado
link_regex = re.compile(
    r'(<a\s+[^>]*)(href="[^"]*alvara_eletronico[^"]*"[^>]*)(>[\s\S]*?Consultar Alvará Eletrônico Automatizado[\s\S]*?</a>)',
    re.IGNORECASE
)

for filename in os.listdir(sidebar_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(sidebar_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Adiciona ou substitui o id no <a>
        def add_id(match):
            tag_start, href_part, tag_end = match.groups()
            # Remove id existente
            tag_start = re.sub(r'id="[^"]*"', '', tag_start)
            # Adiciona id
            return f'{tag_start} id="btn-alvara-eletronico" {href_part}{tag_end}'

        new_content = link_regex.sub(add_id, content)

        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Atualizado: {filepath}")

print("Processo concluído.")