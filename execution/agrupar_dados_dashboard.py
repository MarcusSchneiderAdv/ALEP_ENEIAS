import os
import sys
import json
import glob
import re
import hashlib
from datetime import datetime

from familias import conferir_cobertura, familia_de

# Configuração de Caminhos
# Raiz do repositorio: este arquivo vive em <raiz>/execution/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PROPS_DIR = os.path.join(WORKSPACE_ROOT, ".tmp", "raw_proposicoes")
RAW_DETAILS_DIR = os.path.join(WORKSPACE_ROOT, ".tmp", "raw_detalhes")
OUTPUT_FILE = os.path.join(WORKSPACE_ROOT, "DADOS_ALEP_20.js")

# Mapeamento de Partidos (Atualizado Mar/2026 - Auditoria Completa)
PARTIDOS_MAP = {
    "ADÃO LITRO": "PSD", "ADEMAR TRAIANO": "PSD", "ADELINO RIBEIRO": "PSD",
    "ALEXANDRE AMARO": "REP", "ALEXANDRE CURI": "PSD", "ALISSON WANDSCHEER": "SD",
    "ANA JÚLIA": "PT", "ANIBELLI NETO": "MDB",
    "ARILSON MAROLDI CHIORATO": "PT", "ARILSON CHIORATO": "PT",
    "ARTAGÃO JÚNIOR": "PSD", "ARTAGÃO JUNIOR": "PSD",
    "BATATINHA": "MDB", "BAZANA": "PSD",
    "CANTORA MARA LIMA": "REP", "CLOARA PINHEIRO": "PSD",
    "COBRA REPÓRTER": "PSD", "CRISTINA SILVESTRI": "PP",
    "DELEGADO JACOVÓS": "PL", "DELEGADO TITO BARICHELLO": "UNIÃO",
    "DENIAN COUTO": "PL", "DO CARMO": "UNIÃO",
    "DOUGLAS FABRÍCIO": "CDN",
    "DOUTOR ANTENOR": "PT", "DR. ANTENOR": "PT", "DR. LEÔNIDAS": "CDN", "DR. LEONIDAS": "CDN",
    "EVANDRO ARAÚJO": "PSD", "EVANDRO ARAUJO": "PSD",
    "FABIO OLIVEIRA": "NOVO", "FLÁVIA FRANCISCHINI": "UNIÃO",
    "GALO": "PP", "GILBERTO RIBEIRO": "PL", "GILSON DE SOUZA": "PL",
    "GOURA": "PDT", "GUGU BUENO": "PSD", "GUTO SILVA": "PP",
    "HUSSEIN BAKRI": "PSD", "JAIRO TAMURA": "PL",
    "LUCIANA RAFAGNIN": "PT",
    "LUIS CORTI": "PSB", "LUIS RAIMUNDO CORTI": "PSB",
    "LUIZ CLAUDIO ROMANELLI": "PSD", "LUIZ FERNANDO GUERRA": "UNIÃO",
    "MABEL CANTO": "PSDB", "MARCEL MICHELETTO": "PL",
    "MARCELO RANGEL": "PSD", "MARCIA HUÇULAK": "PSD",
    "MARCIO NUNES": "PSD", "MARCIO PACHECO": "PP",
    "MARIA VICTORIA": "PP", "MARLI PAULINO": "SD",
    "MATHEUS VERMELHO": "PP", "MAURO MORAES": "UNIÃO",
    "MOACYR FADEL": "PSD", "NEREU MOURA": "MDB",
    "NELSON JUSTUS": "UNIÃO", "NEY LEPREVOST": "UNIÃO",
    "PAULO GOMES": "PP", "PEDRO PAULO BAZANA": "PSD",
    "PROFESSOR LEMOS": "PT",
    "REICHEMBACH": "PSD", "WILMAR REICHEMBACH": "PSD",
    "RENATO FREITAS": "PT", "REQUIÃO FILHO": "PDT", "RICARDO ARRUDA": "PL",
    "SAMUEL DANTAS": "SD",
    "SECRETÁRIA MÁRCIA": "PSD", "SECRETÁRIA MARCIA": "PSD",
    "SOLDADO ADRIANO JOSÉ": "PP",
    "TERCILIO TURINI": "MDB", "TERCÍLIO TURINI": "MDB",
    "THIAGO BÜHRER": "UNIÃO", "THIAGO BUHRER": "UNIÃO",
    "TIAGO AMARAL": "PSD",
}

# ── FILTRO DE AUTORES INSTITUCIONAIS (NÃO SÃO DEPUTADOS) ──
INSTITUCIONAL_KEYWORDS = [
    "PODER EXECUTIVO", "COMISSÃO", "MESA EXECUTIVA", "TRIBUNAL", "MINISTÉRIO",
    "DEFENSORIA", "SECRETARIA DE ESTADO", "PREFEITURA", "GOVERNO", "PROCURADORIA",
    "SENADO", "CONSELHO", "NOTA TÉCNICA", "INICIATIVA POPULAR", "OUTROS",
    "PROCON", "PARANACIDADE", "PARANAEDUCA", "CASA CIVIL", "PODER JUDICI",
    "PRESIDÊNCIA DA REPÚBLICA"
]

def is_institucional(nome):
    """Detecta entidades institucionais que não devem entrar como deputados."""
    nome_up = nome.upper()
    return any(kw in nome_up for kw in INSTITUCIONAL_KEYWORDS)

def limpar_nome_autor(nome):
    if not nome: return ""
    nome = nome.upper()
    nome = nome.replace("DEPUTADO ", "").replace("DEPUTADA ", "").strip()
    nome = re.sub(' +', ' ', nome)
    return nome

def carregar_detalhes():
    print(f"Buscando em: {RAW_DETAILS_DIR}")
    detalhes = {}
    files = glob.glob(os.path.join(RAW_DETAILS_DIR, "detalhe_*.json"))
    print(f"Arquivos encontrados pelo glob: {len(files)}")
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as j:
                data = json.load(j)
                valor = data.get('valor')
                if valor and isinstance(valor, dict):
                    codigo = valor.get('codigo')
                    if codigo: 
                        detalhes[str(codigo)] = valor
        except Exception as e:
            continue
    print(f"{len(detalhes)} detalhes processados.")
    return detalhes

def _origem_do_universo():
    """Data de fechamento do universo analisado.

    Duas origens sao possiveis. Se as matrizes forem as do snapshot publicado,
    a data e a do snapshot; se vierem de coleta propria, e a data do download.

    A distincao e feita por conteudo, comparando o SHA-256 de cada matriz com
    o registrado no manifesto. Datas de arquivo nao serviriam: restaurar o
    snapshot reescreve os arquivos com o horario da restauracao, e a heuristica
    apontaria hoje para um universo de marco.
    """
    arquivos = glob.glob(os.path.join(RAW_PROPS_DIR, "proposicoes_*_ws_raw.json"))
    if not arquivos:
        return "indeterminado"

    for manifesto in glob.glob(os.path.join(WORKSPACE_ROOT, "dados", "snapshot_*", "MANIFEST.md")):
        with open(manifesto, encoding="utf-8") as f:
            esperado = dict(re.findall(r"\|\s*(\d{4})\s*\|.*?`([0-9a-f]{64})`", f.read()))
        if not esperado:
            continue
        confere = True
        for caminho in arquivos:
            ano = os.path.basename(caminho).split("_")[1]
            with open(caminho, "rb") as f:
                sha = hashlib.sha256(f.read()).hexdigest()
            if esperado.get(ano) != sha:
                confere = False
                break
        if confere and len(arquivos) == len(esperado):
            marca = os.path.basename(os.path.dirname(manifesto)).replace("snapshot_", "")
            return "/".join(reversed(marca.split("-")))

    from datetime import date
    return date.fromtimestamp(max(os.path.getmtime(a) for a in arquivos)).strftime("%d/%m/%Y")


def atualizar_referencia_html():
    """Versiona a referencia ao payload no index.html pelo hash do conteudo.

    Sem isso, o navegador reaproveita indefinidamente a copia em cache: o
    pipeline roda, o arquivo muda no disco e o painel continua exibindo os
    dados antigos. O hash muda junto com o dado e forca a nova busca.
    """
    html = os.path.join(WORKSPACE_ROOT, "index.html")
    if not os.path.exists(html):
        return

    with open(OUTPUT_FILE, 'rb') as f:
        versao = hashlib.sha256(f.read()).hexdigest()[:8]

    with open(html, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    novo = re.sub(r'src="DADOS_ALEP_20\.js(?:\?v=[0-9a-f]+)?"',
                  'src="DADOS_ALEP_20.js?v=%s"' % versao, conteudo)
    if novo != conteudo:
        with open(html, 'w', encoding='utf-8') as f:
            f.write(novo)
        print(f"index.html: referencia do payload atualizada (v={versao})")


def processar():
    detalhes_map = carregar_detalhes()
    deputados_data = {}

    # Rastreio global de IDs de proposições para desduplicação
    proposicoes_processadas_por_deputado = {}

    print(f"Buscando proposições em: {RAW_PROPS_DIR}")
    prop_files = glob.glob(os.path.join(RAW_PROPS_DIR, "proposicoes_*_ws_raw.json"))
    print(f"Arquivos de proposições: {len(prop_files)}")
    
    stats = {"total": 0, "institucionais_filtrados": 0, "coautorias_validas": 0, "duplicatas_removidas": 0}
    
    for f in prop_files:
        with open(f, 'r', encoding='utf-8') as j:
            content = json.load(j)
            lista = content.get('lista', [])
            for p in lista:
                stats["total"] += 1
                autor_raw = p.get('autor', '')
                
                # Separar autores por vírgula e limpar nomes
                autores_raw_list = [limpar_nome_autor(a) for a in autor_raw.split(',')]
                
                # FILTRAR: remover entidades institucionais da lista de autores
                autores = [a for a in autores_raw_list if a and not is_institucional(a)]
                
                if not autores:
                    stats["institucionais_filtrados"] += 1
                    continue
                
                codigo = str(p.get('codigo'))
                detalhe = detalhes_map.get(codigo, {})
                
                # ─── NORMAS LEGAIS (Leis) ───
                # Priorizar dados do detalhe, mas ler também da proposição bruta
                normas = detalhe.get('normasLegais', []) or p.get('normasLegais', [])
                
                # Trâmites simplificados para a timeline do dash
                tramites_raw = detalhe.get('tramites', []) or p.get('tramites', [])
                # A API entrega tramites[].data / .local / .acoes[].descricao.
                # As acoes sao uma lista aninhada; consolidamos em string legivel.
                tramites_simplificados = [
                    {
                        "data": t.get('data'),
                        "local": t.get('local'),
                        "acao": " | ".join(
                            dict.fromkeys(
                                a.get('descricao') for a in (t.get('acoes') or [])
                                if a.get('descricao')
                            )
                        # ~60% dos eventos nao trazem descricao de acao. Para esses,
                        # data e local ja sao a informacao; o rotulo fica neutro.
                        ) or (t.get('observacao') or "Movimentação")
                    }
                    for t in sorted(tramites_raw, key=lambda x: (x.get('data') or ''))
                    if t.get('data')
                ]
                
                # Rastrear co-autoria
                if len(autores) > 1:
                    stats["coautorias_validas"] += 1
                
                for idx, autor_atual in enumerate(autores):
                    if not autor_atual:
                        continue
                    
                    # ── DESDUPLICAÇÃO ──
                    # Evitar que a mesma proposição seja atribuída 2x ao mesmo deputado
                    chave_dedup = f"{autor_atual}:{codigo}"
                    if chave_dedup in proposicoes_processadas_por_deputado:
                        stats["duplicatas_removidas"] += 1
                        continue
                    proposicoes_processadas_por_deputado[chave_dedup] = True
                    
                    if autor_atual not in deputados_data:
                        deputados_data[autor_atual] = {
                            "nome": autor_atual,
                            "partido": PARTIDOS_MAP.get(autor_atual, "S/P"),
                            "proposicoes_lista": [],
                            "leis_count": 0,
                            "proposicoes_count": 0
                        }
                    
                    if normas:
                        deputados_data[autor_atual]["leis_count"] += len(normas)
                    
                    # ─── CONSTRUÇÃO DO REGISTRO DE LEI ───
                    leis_formatadas = []
                    for n in normas:
                        num_lei = n.get('numero')
                        ano_lei = n.get('ano')
                        tipo_norma = n.get('descricaoTipoNormaLegal') or "Norma"

                        if num_lei and ano_lei:
                            lei_desc = f"{tipo_norma} {num_lei}/{ano_lei}"
                        elif num_lei:
                            lei_desc = f"{tipo_norma} n {num_lei}"
                        else:
                            # Fallback final: identifica pela proposicao de origem
                            lei_desc = f"Norma vinculada ao {p.get('tipoProposicao', 'Projeto')} {p.get('numero', '')}/{p.get('ano', '')}"

                        # Situacao oficial vem da ultima movimentacao (ex.: "Sancionada")
                        movs = n.get('movimentacoes') or []
                        situacao = movs[-1].get('conclusao') if movs else None

                        leis_formatadas.append({
                            "desc": lei_desc,
                            "data": n.get('data') or n.get('dataPublicacao'),
                            "ementa": n.get('ementa'),
                            "situacao": situacao,
                            "observacao": n.get('resumo')
                        })

                    # Padronizar campos para o dashboard
                    item_dash = {
                        "id": p.get('codigo'),
                        "numero": p.get('numero'),
                        "ano": p.get('ano'),
                        "tipo": p.get('tipoProposicao'),
                        "tema": p.get('assunto') or "OUTROS",
                        "familia": familia_de(p.get('assunto')),
                        "status": p.get('status'),
                        "localAtual": p.get('localAtual') or "Não informado",
                        "ementa": p.get('ementa'),
                        "tramites": tramites_simplificados,
                        "is_coautor": (idx > 0),
                        "leis": leis_formatadas
                    }
                    
                    deputados_data[autor_atual]["proposicoes_lista"].append(item_dash)
                    deputados_data[autor_atual]["proposicoes_count"] += 1

    # Converter para lista final
    output_list = list(deputados_data.values())

    # ─── METADADOS DA EXTRACAO ───
    # Gravados junto ao payload para que o painel informe, sem edicao manual,
    # quando os dados foram compilados e ate onde eles alcancam. Quem rodar o
    # pipeline passa a ver a propria data no rodape.
    anos, datas_tramite, datas_norma = set(), [], []
    for dep in output_list:
        for p in dep["proposicoes_lista"]:
            if p.get("ano"):
                anos.add(int(p["ano"]))
            for t in (p.get("tramites") or []):
                if t.get("data"):
                    datas_tramite.append(t["data"])
            for lei in (p.get("leis") or []):
                if lei.get("data"):
                    datas_norma.append(lei["data"])

    anos_ord = sorted(anos)
    meta = {
        "gerado_em": datetime.now().astimezone().isoformat(timespec="seconds"),
        "ano_inicio": anos_ord[0] if anos_ord else None,
        "ano_fim": anos_ord[-1] if anos_ord else None,
        "evento_mais_recente": max(datas_tramite) if datas_tramite else None,
        "norma_mais_recente": max(datas_norma) if datas_norma else None,
        "proposicoes_brutas": stats["total"],
        "deputados": len(output_list),
        "vinculos": sum(d["proposicoes_count"] for d in output_list),
        "leis": sum(d["leis_count"] for d in output_list),
        "fonte": "webservices.assembleia.pr.leg.br/api/public",
        "universo_fechado_em": _origem_do_universo(),
    }

    # Salvar como JS
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("const META = ")
        json.dump(meta, f, ensure_ascii=False)
        f.write(";\nconst DADOS = ")
        # Sem indent: o payload e consumido pelo navegador, nao lido por humanos.
        json.dump(output_list, f, ensure_ascii=False, separators=(',', ':'))
        f.write(";")

    atualizar_referencia_html()

    print(f"\n{'='*60}")
    print(f"CONSOLIDAÇÃO FINALIZADA")
    print(f"{'='*60}")
    print(f"Total de proposições brutas: {stats['total']}")
    print(f"Institucionais filtrados: {stats['institucionais_filtrados']}")
    print(f"Proposições com co-autoria válida: {stats['coautorias_validas']}")
    print(f"Duplicatas removidas: {stats['duplicatas_removidas']}")
    print(f"Deputados consolidados: {len(output_list)}")

    # Rotulo novo na origem nao e adivinhado: e reportado para decisao humana
    # em directives/familias_de_assunto.md.
    rotulos = {(q.get("tema") or "SEM ASSUNTO") for d in output_list
               for q in d["proposicoes_lista"]}
    sem_familia = conferir_cobertura(rotulos)
    if sem_familia:
        print(f"[!] {len(sem_familia)} rotulo(s) de assunto sem familia na diretriz:")
        for r in sem_familia:
            print(f"      {r}")
        print("    Classifique em directives/familias_de_assunto.md")
    else:
        print(f"Familias de assunto: {len(rotulos)} rotulos, todos classificados")
    print(f"Arquivo salvo: {OUTPUT_FILE}")

if __name__ == "__main__":
    processar()
