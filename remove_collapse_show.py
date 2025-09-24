import os
import re

# Caminho da pasta onde estão os arquivos HTML
root_dir = "."

# Regex para encontrar <ul class="collapse show" ...>
collapse_show_re = re.compile(r'(<ul\s+class="collapse) show(\s*"\s+id="[^"]+")', re.IGNORECASE)

for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(subdir, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            new_content = collapse_show_re.sub(r'\1\2', content)

            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Removido 'show' de: {path}")

print("Remoção da classe 'show' concluída.")
