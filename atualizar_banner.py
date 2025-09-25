import os
import re
# Banner padronizado
banner = '''<div style="background:#ffeb3b;color: #736920;padding: 1px;text-align:center;font-weight:bold;font-size: 0.8em;/* border-bottom:2px solid #fbc02d; */z-index:9999;position:fixed;top:0;left:0;width:100%;box-shadow:0 2px 6px rgba(0,0,0,0.1);">Este ambiente é uma simulação para fins exclusivamente educacionais, sem vínculo com o sistema oficial do Poder Judiciário (eproc).</div>\n<script>document.body.style.paddingTop = '20px';</script>\n'''
# Regex para encontrar todos os banners antigos (variações de estilos, textos e scripts)
banner_regex = re.compile(r'<div[^>]*background:#ffeb3b[^>]*>.*?educacionais, sem vínculo com o sistema oficial do Poder Judiciário \(eproc\)\..*?</div>\s*<script>document.body.style.paddingTop ?= ?["\']?\d+px["\']?;?</script>\s*', re.DOTALL)
pastas = ['eventos', 'sidebar']
for pasta in pastas:
    for root, dirs, files in os.walk(pasta):
        for file in files:
            if file.endswith('.html'):
                caminho = os.path.join(root, file)
                with open(caminho, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                # Remove todos os banners antigos
                conteudo_limpo = re.sub(banner_regex, '', conteudo)
                # Remove banners que estejam sem o script (caso algum escape)
                conteudo_limpo = re.sub(r'<div[^>]*background:#ffeb3b[^>]*>.*?educacionais, sem vínculo com o sistema oficial do Poder Judiciário \(eproc\)\..*?</div>\s*', '', conteudo_limpo, flags=re.DOTALL)
                # Remove scripts isolados
                conteudo_limpo = re.sub(r'<script>document.body.style.paddingTop ?= ?["\']?\d+px["\']?;?</script>\s*', '', conteudo_limpo)
                # Insere o banner padronizado após <body>
                if '<body' in conteudo_limpo:
                    conteudo_final = re.sub(r'(<body[^>]*>)', r'\1\n' + banner, conteudo_limpo, count=1)
                else:
                    conteudo_final = banner + conteudo_limpo
                with open(caminho, 'w', encoding='utf-8') as f:
                    f.write(conteudo_final)
                print(f'Banner atualizado em: {caminho}')
