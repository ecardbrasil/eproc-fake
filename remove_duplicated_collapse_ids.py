import os
import re
# Caminho da pasta onde estão os arquivos HTML
root_dir = "."
# Regex para encontrar <ul class="collapse" id="algum-id">
ul_collapse_re = re.compile(r'(<ul\s+class="collapse"\s+id="([^"]+)")', re.IGNORECASE)
# Dicionário para rastrear IDs já usados
seen_ids = set()
for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(subdir, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            def repl(match):
                full_tag, ul_id = match.groups()
                if ul_id in seen_ids:
                    # Remove o id duplicado
                    return full_tag.replace(f' id="{ul_id}"', "")
                else:
                    seen_ids.add(ul_id)
                    return match.group(0)
            new_content = ul_collapse_re.sub(repl, content)
            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Corrigido: {path}")
print("Remoção de IDs duplicados concluída.")
