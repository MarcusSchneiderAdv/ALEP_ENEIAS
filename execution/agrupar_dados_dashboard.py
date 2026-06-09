import os
import json
import glob
import re

# Configuração de Caminhos
WORKSPACE_ROOT = r"c:\Users\Marcus Schneider\Documents\Marcus\2026\Projetos\Fase_final_Apresentação\ALEP"
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
                tramites_simplificados = [
                    {"data": t.get('dataPublicacaoOrdemDia'), "local": t.get('orgao'), "acao": t.get('descricao')}
                    for t in tramites_raw if t.get('dataPublicacaoOrdemDia')
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
                        deputados_data[autor_atual]["leis_count"] += 1
                    
                    # ─── CONSTRUÇÃO DO REGISTRO DE LEI ───
                    leis_formatadas = []
                    for n in normas:
                        desc = n.get('descricao')
                        num_lei = n.get('numeroLei')
                        ano_lei = n.get('anoLei')
                        
                        # Evitar "Lei None/None" e usar fallback inteligente
                        if desc and str(desc).lower() not in ('null', 'none', ''):
                            lei_desc = desc
                        elif num_lei and ano_lei:
                            lei_desc = f"Lei {num_lei}/{ano_lei}"
                        elif num_lei:
                            lei_desc = f"Lei N° {num_lei}"
                        else:
                            # Usar dados da proposição original como fallback final
                            lei_desc = f"Norma vinculada ao {p.get('tipoProposicao', 'Projeto')} {p.get('numero', '')}/{p.get('ano', '')}"
                        
                        leis_formatadas.append({
                            "desc": lei_desc,
                            "data": n.get('dataPublicacao') or n.get('dataLei')
                        })
                    
                    # Padronizar campos para o dashboard
                    item_dash = {
                        "id": p.get('codigo'),
                        "numero": p.get('numero'),
                        "ano": p.get('ano'),
                        "tipo": p.get('tipoProposicao'),
                        "tema": p.get('assunto') or "OUTROS",
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
    
    # Salvar como JS
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("const DADOS = ")
        json.dump(output_list, f, ensure_ascii=False, indent=2)
        f.write(";")
    
    print(f"\n{'='*60}")
    print(f"CONSOLIDAÇÃO FINALIZADA")
    print(f"{'='*60}")
    print(f"Total de proposições brutas: {stats['total']}")
    print(f"Institucionais filtrados: {stats['institucionais_filtrados']}")
    print(f"Proposições com co-autoria válida: {stats['coautorias_validas']}")
    print(f"Duplicatas removidas: {stats['duplicatas_removidas']}")
    print(f"Deputados consolidados: {len(output_list)}")
    print(f"Arquivo salvo: {OUTPUT_FILE}")

if __name__ == "__main__":
    processar()
