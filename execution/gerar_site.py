# -*- coding: utf-8 -*-
"""
FASE 6: monta o site publicavel em docs/, para o GitHub Pages.

Por que existe
    O GitHub guarda codigo, nao executa. Para que o cidadao veja o painel sem
    instalar nada, o painel precisa ser hospedado como site estatico, e o
    Pages serve a pasta docs/ do repositorio.

Por que a versao publicada e mais leve
    A carga util completa tem cerca de 23 MB, dos quais aproximadamente 62%
    sao as linhas do tempo de tramitacao. Versionar isso a cada regeracao
    incharia o repositorio sem limite. A versao do site omite os tramites e
    fica em torno de 9 MB, mantendo numeros, especies, familias, assuntos e
    normas sancionadas. O painel ja trata a ausencia de tramites sem quebrar:
    a linha do tempo simplesmente nao aparece.

    Quem precisar do historico processual roda o pipeline e usa a versao
    completa localmente, ou abre o registro na fonte, cujo endereco consta
    dos dossies em dados/perfis/.
"""

import hashlib
import json
import os
import re
import shutil

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAYLOAD = os.path.join(RAIZ, "DADOS_ALEP_20.js")
PAINEL = os.path.join(RAIZ, "index.html")
SITE = os.path.join(RAIZ, "docs")

AVISO = """  <div style="background:#1e2430; border:1px solid #2a313d; border-left:3px solid #f5a623;
       border-radius:8px; padding:0.9rem 1.2rem; margin:0 2rem 1.5rem; font-size:0.78rem;
       color:#8892a4; line-height:1.5; max-width:1500px; margin-left:auto; margin-right:auto;">
    <strong style="color:#e2e8f0">Versão publicada.</strong>
    Para caber na hospedagem, esta versão omite o histórico de tramitação de cada proposição.
    Todo o restante está íntegro. Para ver a linha do tempo completa, rode o projeto na sua
    máquina, ou abra o registro na fonte pelos endereços indicados nos dossiês em
    <code>dados/perfis/</code>.
  </div>
"""


def carregar():
    with open(PAYLOAD, encoding="utf-8") as f:
        bruto = f.read()
    meta = bruto.split("const META = ", 1)[1].split(";\n", 1)[0]
    dados = json.loads(bruto.split("const DADOS = ", 1)[1].rsplit(";", 1)[0])
    return meta, dados


def enxugar(dados):
    """Remove os tramites, preservando todo o resto."""
    for dep in dados:
        for p in dep["proposicoes_lista"]:
            p["tramites"] = []
    return dados


def gerar():
    if not os.path.exists(PAYLOAD):
        raise SystemExit("[ERRO] %s nao encontrado. Rode agrupar_dados_dashboard.py antes."
                         % os.path.basename(PAYLOAD))
    if not os.path.exists(PAINEL):
        raise SystemExit("[ERRO] index.html nao encontrado na raiz.")

    os.makedirs(SITE, exist_ok=True)
    meta, dados = carregar()

    destino_payload = os.path.join(SITE, "DADOS_ALEP_20.js")
    with open(destino_payload, "w", encoding="utf-8") as f:
        f.write("const META = ")
        f.write(meta)
        f.write(";\nconst DADOS = ")
        json.dump(enxugar(dados), f, ensure_ascii=False, separators=(",", ":"))
        f.write(";")

    with open(destino_payload, "rb") as f:
        versao = hashlib.sha256(f.read()).hexdigest()[:8]

    with open(PAINEL, encoding="utf-8") as f:
        html = f.read()
    html = re.sub(r'src="DADOS_ALEP_20\.js(?:\?v=[0-9a-f]+)?"',
                  'src="DADOS_ALEP_20.js?v=%s"' % versao, html)
    # O aviso entra logo apos a abertura do conteudo principal.
    html = html.replace("<main>", "<main>\n" + AVISO, 1)

    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    # O Pages usa Jekyll por padrao e ignora pastas iniciadas por underscore.
    # O arquivo abaixo desliga esse processamento e serve os arquivos como estao.
    with open(os.path.join(SITE, ".nojekyll"), "w", encoding="utf-8") as f:
        f.write("")

    completo = os.path.getsize(PAYLOAD) / 1e6
    leve = os.path.getsize(destino_payload) / 1e6
    print("[OK] site gerado em docs/")
    print("     payload completo %.1f MB -> publicado %.1f MB (%.0f%% menor)"
          % (completo, leve, (1 - leve / completo) * 100))
    print("     para publicar: Settings > Pages > Source: branch main, pasta /docs")


if __name__ == "__main__":
    gerar()
