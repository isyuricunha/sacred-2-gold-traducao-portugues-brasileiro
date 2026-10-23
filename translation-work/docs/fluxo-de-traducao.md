# Fluxo manual

O guia operacional e a sequência de handoff estão em [../README.md](../README.md).
Sayuri pesquisa o jogo e escreve o [briefing](briefing-do-jogo.md), com fontes e
dúvidas. Ella usa essa pesquisa, define diretrizes e glossário antes de traduzir
em escala; depois lê lotes e contexto, aplica apenas PTBR, revisa e faz checkpoints.
Questões novas podem exigir aprofundamento da pesquisa. O desenvolvimento da
toolkit não preenche nem aprova traduções. Yuri realiza os testes no jogo.

Enquanto houver pendências, `check` pode passar, mas `build` deve falhar. Não
edite PTBR como área de trabalho. Revisão de atualização usa `sync --dry-run`,
`sync`, `diff` e `reports/sync-latest.json`. O relatório inclui geração antiga/nova,
IDs, lotes, EN anterior/atual e PTBR anterior. Não confunda relatório de geração
anterior com uma tentativa nova que falhou: compare seu generation com o manifest.

Payloads parciais recebem status individual. Nunca corrija campos EN, key, row,
source_file ou source_fingerprint para contornar uma rejeição. Corrija a tradução
ou investigue a fonte e execute sync. `apply --replace` é para revisão deliberada.

Atualização do PROGRESS.md: nunca confie em `str.replace` com âncora de memória.
Python não avisa quando o trecho procurado não existe e o lote sai do registro em
silêncio. Antes de gravar, confirme que cada âncora existe no arquivo (assert) ou
insira a linha nova em posição determinística (logo após a última entrada de lote
achada por regex). O contador do cabeçalho deve ser conferido contra
`toolkit.py status`, nunca encadeado de edição em edição.
