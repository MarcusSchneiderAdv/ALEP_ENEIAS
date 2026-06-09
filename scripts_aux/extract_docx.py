import docx
doc = docx.Document('Projeto ALEP_VFinal.docx')
with open('doc_content.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join([p.text for p in doc.paragraphs if p.text.strip()]))
