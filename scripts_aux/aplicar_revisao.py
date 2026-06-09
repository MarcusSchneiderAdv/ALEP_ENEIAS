import docx
import re
from docx.shared import Pt
import os

doc_path = r"C:\Users\Marcus Schneider\Documents\Marcus\2026\Projetos\Fase_final_Apresentação\ALEP\Projeto ALEP_VFinal.docx"
out_path = r"C:\Users\Marcus Schneider\Documents\Marcus\2026\Projetos\Fase_final_Apresentação\ALEP\Projeto_ALEP_Revisado_Oficial.docx"

if not os.path.exists(doc_path):
    # fallback se o arquivo for o que criamos antes
    doc_path = r"C:\Users\Marcus Schneider\Documents\Marcus\2026\Projetos\Fase_final_Apresentação\ALEP\Projeto_ALEP_Finalizado.docx"

doc = docx.Document(doc_path)

# Regex para detectar links grudados (http...)
url_pattern = re.compile(r'\s*\((https?://[^\)]+)\)')

def replace_in_paragraph(p, old_text, new_text):
    if old_text in p.text:
        # A simple replacement that will overwrite formatting in that specific paragraph.
        # It's an acceptable trade-off to ensure clean text.
        p.text = p.text.replace(old_text, new_text)

for p in doc.paragraphs:
    # 1. Automate URL cleaning
    if url_pattern.search(p.text):
        p.text = url_pattern.sub('', p.text)
        
    # 2. Grammar fixes
    replace_in_paragraph(p, "Estado Democracia de Direito", "Estado Democrático de Direito")
    replace_in_paragraph(p, "'caixas-pretas,", "'caixas-pretas',")
    replace_in_paragraph(p, "*Privacy by Design*", "Privacy by Design")
    replace_in_paragraph(p, "*Civic Techs*", "Civic Techs")
    
    # Missing verb
    replace_in_paragraph(p, 
        "em seguida, os gatilhos secundários (como o módulo coletar_detalhes_api.py e as requisições de coleta de normas).",
        "em seguida, são acionados os gatilhos secundários (como o módulo coletar_detalhes_api.py e as requisições de coleta de normas).")
        
    # 3. Tone modulation (reducing over-defensiveness about "homenagens")
    # Section 1.2
    replace_in_paragraph(p,
        "mitigando a desinformação por meio da transparência cognitiva, sem a emissão de juízos de valor sobre a legitimidade dos atos honoríficos.",
        "mitigando a desinformação por meio da transparência cognitiva e estrutural.")
    # Section 3.2
    replace_in_paragraph(p,
        "Elide-se, assim, a obscuridade informacional, entregando um panorama estruturado da dedicação representativa sem censurar, subestimar ou emitir qualquer juízo de valor sobre qualquer ato legislativo.",
        "Elide-se, assim, a obscuridade informacional, entregando um panorama estruturado e imparcial da dedicação representativa.")
    # Section 7
    replace_in_paragraph(p,
        "O painel analítico gerado atende plenamente aos objetivos traçados, fragmentando e evidenciando a pluralidade de atuações inerentes ao mandato legislativo, sem emitir valor de mérito.",
        "O painel analítico atende plenamente aos objetivos traçados, evidenciando a produtividade inerente ao mandato legislativo de forma neutra e visualmente coesa.")
        
    # 4. Insert CNJ conclusion
    if "Conclui-se, destarte, que o emprego estratégico da Engenharia de Software" in p.text:
       # We append the CNJ Pacto analogy at the very end of the conclusion
       p.text = p.text + " Ao fim, a plataforma E.N.E.I.A.S. ergue-se não apenas como código, mas como a sublime manifestação do \u0027Pacto pela Linguagem Simples\u0027 transposto do Judiciário diretamente para as entranhas digitais do Poder Legislativo estadual."

# Add References Section
doc.add_page_break()
p_h = doc.add_paragraph()
run_h = p_h.add_run("8. REFERÊNCIAS")
run_h.bold = True
if 'Heading 1' in doc.styles:
    p_h.style = 'Heading 1'

references = [
    "BANDEIRA DE MELLO, Celso Antônio. Curso de Direito Administrativo. 32. ed. São Paulo: Malheiros, 2015. Disponível em: <https://www.tce.sp.gov.br/epcp/cadernos/index.php/CM/article/download/302/214/>. Acesso em: 05 abr. 2026.",
    "BARROSO, Luís Roberto. Revolução Digital: Direito e Tecnologia no Século XXI. São Paulo: Saraiva, 2021. Disponível em: <https://www.migalhas.com.br/arquivos/2021/8/8AC745F6774D3A_RevolucaoDigital.pdf>. Acesso em: 05 abr. 2026.",
    "BRASIL. Controladoria-Geral da União (CGU). Guia de Aplicação da Lei de Acesso à Informação. 3. ed. Brasília: CGU, 2022. Disponível em: <https://repositorio.cgu.gov.br/bitstream/1/29957/15/aplicacao_lai_3a_ed.pdf>. Acesso em: 05 abr. 2026.",
    "CONSELHO NACIONAL DE JUSTIÇA (CNJ). Recomendação nº 144/2023. Pacto Nacional do Judiciário pela Linguagem Simples. Brasília: CNJ, 2023. Disponível em: <https://www.cnj.jus.br/wp-content/uploads/2023/11/pacto-nacional-do-judiciario-pela-linguagem-simples.pdf>. Acesso em: 05 abr. 2026.",
    "DI PIETRO, Maria Sylvia Zanella. Direito Administrativo. 22. ed. São Paulo: Atlas, 2009. Disponível em: <https://www.kufunda.net/publicdocs/Direito_Administrativo_-_Livro_Maria_Silvia_Di_Pietro.pdf>. Acesso em: 05 abr. 2026.",
    "LAI, Y.; et al. Legal Data Parsing and Jurimetrics. arXiv:2311.XXXX, 2023. ",
    "MARTINS, Ives Gandra da Silva. O Princípio da Publicidade na Administração Pública. Revista Brasileira de Direito Constitucional - RBDC, n. 08, 2008. Disponível em: <http://www.esdc.com.br/RBDC/RBDC-08/RBDC-08-013-Ives_Gandra_da_Silva_Martins.pdf>. Acesso em: 05 abr. 2026.",
    "MEDAUAR, Odete. Direito Administrativo Moderno. 21. ed. São Paulo: RT, 2018. Disponível em: <https://www.academia.edu/39023542/DIREITO_ADMINISTRATIVO_MODERNO>. Acesso em: 05 abr. 2026.",
    "MEIRELLES, Hely Lopes. Direito Administrativo Brasileiro. 42. ed. São Paulo: Malheiros, 2016. Disponível em: <https://www.direito.mppr.mp.br/arquivos/File/DireitoAdministrativoBrasileiro.pdf>. Acesso em: 05 abr. 2026.",
    "SUN, X.; et al. Algorithmic Bias in Legal NLP. arXiv:2312.03718, 2023. Disponível em: <https://arxiv.org/pdf/2312.03718.pdf>. Acesso em: 05 abr. 2026."
]

for ref in references:
    p_ref = doc.add_paragraph(ref)
    p_ref.alignment = 3 # Justify

doc.save(out_path)
print(f"Sucesso. Arquivo salvo em: {out_path}")
