import re
import os
# Lista de papéis de partes processuais para buscar
roles = [
    "Autor", "Réu", "Embargante", "Embargado", "Exequente", "Executado"
]
def replace_party_names(html):
    # Substitui padrões com <span id=lblAtencao>...</span>
    html = re.sub(r'(<span[^>]*id=lblAtencao[^>]*>)[^<]+(</span>)', r'\1NOME DA PARTE\2', html)
    # Substitui após o marcador (ex: <b>Autor</b><br> ... <br>)
    for role in roles:
        html = re.sub(NOME DA PARTE, rf'\1NOME DA PARTE\3', html)
    # Substitui nomes soltos antes de CPF/CNPJ
    html = re.sub(r'(<br>\s*)[^<\(]+(<br>\([0-9\.\-/]+\)<br>X<br><b>[^<]+</b><br>)[^<]+(<br>)', r'\1NOME DA PARTE\2NOME DA PARTE\3', html)
    html = re.sub(r'(<br>\s*)[^<\(]+(<br>\([0-9\.\-/]+\)<br>)', r'\1NOME DA PARTE\2', html)
    return html
def process_html_files(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.html'):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    html = f.read()
                new_html = replace_party_names(html)
                if new_html != html:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_html)
                    print(f"Substituição concluída em: {file_path}")
if __name__ == "__main__":
    process_html_files(".")
    print("Processamento finalizado.")
