

import re
import unicodedata

def remover_acentos(txt):
    return ''.join(c for c in unicodedata.normalize('NFD', txt)
                   if unicodedata.category(c) != 'Mn')

def gerar_regex_nome(nome):
    # Divide o nome em partes e permite qualquer quantidade de espaços, quebras de linha ou tags HTML entre elas
    partes = nome.strip().split()
    # Permite espaços, quebras de linha, <br>, </span>, etc. entre as partes do nome
    separador = r'(?:\s|<[^>]+>|\n|\r)*'
    regex = separador.join(map(re.escape, partes))
    return regex

def replace_party_names(text, nomes):
    log = []
    for nome in nomes:
        encontrado = False
        # Estratégia 1: Regex robusto (case/acento-insensitive, ignora tags e quebras de linha)
        regex_nome = gerar_regex_nome(nome)
        pattern = re.compile(regex_nome, re.IGNORECASE)
        def _sub_nome(m):
            nonlocal encontrado
            encontrado = True
            return 'NOME DA PARTE'
        text, count = pattern.subn(_sub_nome, text)
        if encontrado:
            log.append(f"Substituído (regex robusto): {nome}")
            continue
        # Estratégia 2: Regex robusto sem acento
        regex_nome_sem_acento = gerar_regex_nome(remover_acentos(nome))
        text_sem_acento = remover_acentos(text)
        pattern2 = re.compile(regex_nome_sem_acento, re.IGNORECASE)
        def _sub_nome2(m):
            nonlocal encontrado
            encontrado = True
            return 'NOME DA PARTE'
        text2, count2 = pattern2.subn(_sub_nome2, text_sem_acento)
        if encontrado:
            # Não é trivial mapear de volta para o texto original, então apenas loga
            log.append(f"Encontrado apenas sem acento (não substituído): {nome}")
            continue
        log.append(f"Não encontrado: {nome}")
    return text, log

if __name__ == "__main__":
    # Lê o arquivo HTML
    with open('sidebar/eproc-processos-com-prazo-em-aberto.html', 'r', encoding='utf-8') as f:
        texto = f.read()

    # Regex para capturar nomes de partes processuais (pessoas físicas/jurídicas)
    padrao_nome = r'([A-ZÁÉÍÓÚÂÊÔÃÕÇ]{2,}(?:\s|<[^>]+>|\n|\r)+(?:[A-ZÁÉÍÓÚÂÊÔÃÕÇ]{2,}(?:\s|<[^>]+>|\n|\r)+)*[A-ZÁÉÍÓÚÂÊÔÃÕÇ]{2,})'
    nomes_encontrados = set()
    termos_genericos = set([
        'CUMPRIMENTO DE SENTENÇA', 'PROCEDIMENTO COMUM CÍVEL', 'PROCEDIMENTO DO JUIZADO ESPECIAL CÍVEL',
        'PROCEDIMENTO ORDINÁRIO', 'EMBARGOS À EXECUÇÃO', 'EXECUÇÃO FISCAL', 'ALIMENTOS', 'AÇÃO PENAL',
        'RITO ORDINÁRIO', 'EMBARGANTE', 'EMBARGADO', 'AUTOR', 'RÉU', 'EXEQUENTE', 'EXECUTADO',
        'PRIMEIRO GRAU', 'TURMA RECURSAL', 'JUIZADO ESPECIAL ESTADUAL', 'LEI ESPECIAL N',
        'ESTADO DO RIO GRANDE DO SUL', 'RS', 'S/A', 'LTDA', 'SIMPLES', 'SOCIEDADE', 'ADVOGADO',
        'MINISTÉRIO PÚBLICO', 'BANRISUL', 'BANCO', 'MUNICÍPIO', 'CONDOMÍNIO', 'CONDOMINIO',
        'CENTRO', 'HOME', 'COOPERATIVA', 'COOP', 'IMPAR', 'PRAIA', 'HOTEL', 'EDIFÍCIO', 'EDIFICIO',
        'RESIDENCIAL', 'PARIS', 'IBIZA', 'TRISTEZA', 'MUNDO VIP', 'VIP', 'TRISTEZA', 'FRIES', 'FERREIRA',
        'CARDOSO', 'SILVA', 'SANTOS', 'DE', 'DO', 'DA', 'DOS', 'DAS', 'E', 'A', 'O', 'X', 'NOME DA PARTE'
    ])
    for m in re.finditer(padrao_nome, texto):
        nome = re.sub(r'(?:<[^>]+>|\s|\n|\r)+', ' ', m.group(0)).strip()
        # Filtra nomes muito curtos, genéricos ou compostos só de termos processuais
        if len(nome.split()) >= 2 and len(nome) > 6:
            partes = set(nome.split())
            if not partes.issubset(termos_genericos):
                nomes_encontrados.add(nome)

    nomes = sorted(nomes_encontrados)
    print(f"Nomes extraídos: {len(nomes)}")
    for nome in nomes:
        print(f"- {nome}")

    texto_substituido, log = replace_party_names(texto, nomes)
    with open('sidebar/eproc-processos-com-prazo-em-aberto_saida.html', 'w', encoding='utf-8') as f:
        f.write(texto_substituido)
    print("\n".join(log))
    print(f"\nTotal substituídos: {sum('Substituído' in l for l in log)} de {len(nomes)} nomes.")