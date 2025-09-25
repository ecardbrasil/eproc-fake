import os
# Mensagem de aviso
aviso = '''\n<div style="background:#ffeb3b;color:#222;padding:12px;text-align:center;font-weight:bold;font-size:1.1em;border-bottom:2px solid #fbc02d;z-index:9999;position:fixed;top:0;left:0;width:100%;box-shadow:0 2px 6px rgba(0,0,0,0.1);">\nEste ambiente é uma simulação para fins exclusivamente educacionais, sem vínculo com o sistema oficial do Poder Judiciário (eproc).\n</div>\n<script>document.body.style.paddingTop = '56px';</script>\n'''
# Caminhos das pastas a serem processadas
pastas = ['eventos', 'sidebar']
for pasta in pastas:
    for root, dirs, files in os.walk(pasta):
        for file in files:
            if file.endswith('.html'):
                caminho = os.path.join(root, file)
                with open(caminho, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                if aviso.strip() not in conteudo:
                    novo_conteudo = conteudo.replace('</body>', aviso + '\n</body>')
                    with open(caminho, 'w', encoding='utf-8') as f:
                        f.write(novo_conteudo)
                    print(f'Aviso inserido em: {caminho}')
                else:
                    print(f'Aviso já presente em: {caminho}')
