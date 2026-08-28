# -*- coding: utf-8 -*-
"""
Ponto de entrada unico do projeto ALEP / E.N.E.I.A.S.

Executa o pipeline completo, da coleta nos servicos publicos da Assembleia
Legislativa do Parana ate a geracao dos dossies consultaveis por IA.

    python executar.py              coleta os dados atuais e gera tudo
    python executar.py --snapshot   usa o universo congelado da pesquisa
    python executar.py --perfis     apenas regera os dossies

O modo padrao consulta a Assembleia e devolve o estado de hoje. O modo
--snapshot restaura o universo em que a monografia se baseia, e serve a quem
quer auditar os numeros publicados em vez de levantar os proprios.
"""

import os
import subprocess
import sys
import time

RAIZ = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable


def titulo(texto):
    print("\n" + "=" * 66)
    print(texto)
    print("=" * 66)


def rodar(caminho_rel, descricao):
    """Executa um script do pipeline, repassando a saida ao terminal."""
    titulo(descricao)
    inicio = time.time()
    r = subprocess.run([PY, os.path.join(RAIZ, caminho_rel)], cwd=RAIZ)
    dur = time.time() - inicio
    if r.returncode != 0:
        print("\n[!] '%s' terminou com pendencia (codigo %d) apos %.0fs."
              % (caminho_rel, r.returncode, dur))
        return False
    print("[.] concluido em %.0fs" % dur)
    return True


def conferir_ambiente():
    titulo("VERIFICACAO DO AMBIENTE")
    print("Python %d.%d.%d" % sys.version_info[:3])
    if sys.version_info < (3, 6):
        sys.exit("[ERRO] Requer Python 3.6 ou superior.")
    faltando = []
    for mod in ("requests", "urllib3"):
        try:
            __import__(mod)
            print("  %-10s ok" % mod)
        except ImportError:
            faltando.append(mod)
            print("  %-10s AUSENTE" % mod)
    if faltando:
        print("\n[ERRO] Dependencias ausentes. Instale com:")
        print("    pip install -r requirements.txt")
        sys.exit(1)


def main():
    args = set(sys.argv[1:])
    so_perfis = "--perfis" in args
    usar_snapshot = "--snapshot" in args

    conferir_ambiente()

    if so_perfis:
        rodar("execution/gerar_perfis.py", "GERACAO DE DOSSIES")
        final()
        return

    pendencias = []

    titulo("MODO DE EXECUCAO")
    if usar_snapshot:
        print("DADOS PUBLICADOS (--snapshot)")
        print("")
        print("  Restaura o universo de 15.369 proposicoes sobre o qual a monografia")
        print("  foi escrita, com integridade conferida por SHA-256. Serve para")
        print("  auditar os numeros publicados.")
        print("")
        print("  A Fase 1 e dispensada. As fases seguintes consultam a Assembleia")
        print("  para obter o estado processual de cada proposicao.")
        if not rodar("scripts_aux/restaurar_snapshot.py",
                     "FASE 1: restauracao do universo publicado (22/03/2026)"):
            sys.exit("[ERRO] Nao foi possivel restaurar o snapshot.")
    else:
        print("DADOS ATUAIS (padrao)")
        print("")
        print("  Coleta o estado de hoje diretamente do servico publico da ALEP.")
        print("  O universo sera maior que o da monografia, porque a legislatura")
        print("  segue em curso e novas proposicoes seguem sendo protocoladas.")
        print("")
        print("  Para auditar os numeros publicados, use:  python executar.py --snapshot")
        if not rodar("execution/coletar_proposicoes_api.py",
                     "FASE 1: ingestao das proposicoes"):
            pendencias.append("coleta de proposicoes")

    print("")
    print("[i] A proxima fase faz uma requisicao por proposicao. Numa coleta do")
    print("    zero isso leva cerca de 50 minutos. A rotina preserva o que ja")
    print("    baixou, entao pode ser interrompida e retomada sem perda.")

    if not rodar("execution/coletar_detalhes_api.py",
                 "FASE 2: enriquecimento (tramitacao e normas vinculadas)"):
        pendencias.append("coleta de detalhes")

    if not rodar("execution/coletar_normas_api.py",
                 "FASE 3: base de normas sancionadas"):
        pendencias.append("coleta de normas")

    if not rodar("execution/agrupar_dados_dashboard.py",
                 "FASE 4: consolidacao e carga util do painel"):
        sys.exit("[ERRO] A consolidacao falhou. Sem ela nao ha o que publicar.")

    if not rodar("execution/gerar_perfis.py",
                 "FASE 5: dossies para consulta com IA"):
        pendencias.append("geracao de dossies")

    final(pendencias)


def final(pendencias=()):
    titulo("PRONTO")
    print("Painel .......: abra index.html no navegador")
    print("Dossies ......: dados/perfis/")
    print("  _PANORAMA.md .... visao da Casa, para perguntas comparativas")
    print("  _CONSOLIDADO.csv  metricas de todos, para planilha")
    print("  <NOME>.md ....... dossie individual")
    print("")
    print("Para consultar com IA: anexe o arquivo do parlamentar a um assistente")
    print("e pergunte em linguagem natural. Instrucoes em dados/perfis/LEIAME.md")
    if pendencias:
        print("")
        print("[!] Etapas com pendencia: %s" % ", ".join(pendencias))
        print("    Reexecute para completar. As rotinas preservam o que ja foi obtido.")


if __name__ == "__main__":
    main()
