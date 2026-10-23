# Toolkit de localização — Sacred 2 Gold

Python **3.10+**, somente biblioteca padrão. Execute da raiz do repositório;
o script também resolve corretamente os caminhos quando chamado de outro diretório.
Não há tradução automática, serviços externos ou escrita na instalação do jogo.

## Estrutura e fonte aceita

- `EN/locale/en_UK/`: nove recursos ingleses, com caminhos nativos.
- `accepted-sources/`: cópia versionada da última fonte aceita, independente de EN.
- `translations/`: manifesto e JSONL UTF-8 de até 500 registros por lote.
- `reports/`: diffs completos e histórico versionado de alterações/remoções.
- `.state/`: estado local ignorado, locks, staging e snapshots de recuperação.
- `build-manifest.json`: recibo versionado do último build, quando houver.
- `../PTBR/`: saída completa; **ausente enquanto a tradução estiver pendente**.

O `global.res` inicial veio do backup preservado antes da amostra PT-BR e teve
SHA-256 conferido. Os oito CSVs ASCII vieram da instalação sem edição. Não
importamos a amostra instalada como inglês. A base não é classificada como
vanilla nem como mod específico sem comprovação. Não existem variantes.

As 63 traduções anteriores estão em `reference/menu-sample.json`, apenas como
referência não aprovada para Ella. Os campos PTBR ativos começam vazios.

## Comandos

```sh
python translation-work/toolkit.py status
python translation-work/toolkit.py check
python translation-work/toolkit.py diff
python translation-work/toolkit.py extract --source-root /originais-com-caminhos-nativos
python translation-work/toolkit.py sync
python translation-work/toolkit.py sync --source-file /originais/global.res
python translation-work/toolkit.py sync --source-root /originais-com-caminhos-nativos --dry-run
python translation-work/toolkit.py update-sources --dry-run
python translation-work/toolkit.py update-sources --game-root "/caminho/Sacred 2 Gold" --dry-run
python translation-work/toolkit.py update-sources --game-root "/caminho/Sacred 2 Gold"
python translation-work/toolkit.py apply --payload /traducoes/lote.json
python translation-work/toolkit.py build
python translation-work/toolkit.py verify-output
python translation-work/toolkit.py package
```

Todos os comandos imprimem JSON (também aceitam `--json`). Falha retorna 1;
aplicação parcialmente aceita retorna 2, com IDs e motivos. `extract` recusa
progresso existente; use `sync` nas atualizações. `diff` sem caminho mostra o
último relatório aceito, cuja geração está no próprio relatório; com caminho
compara o candidato sem gravar. `sync --dry-run` também compara EN editado.

`update-sources` tenta o caminho já verificado em `.state/machine.json` ou os
metadados locais Steam do AppID 225640. Não faz varredura de discos. Em Linux
remoto não enxerga a instalação do Windows: forneça os originais por
`--source-root`, ou um `--game-root` realmente acessível. Nenhuma localização
absoluta pessoal é versionada. Caminhos com espaços são aceitos.

Um diretório de jogo precisa de `system/sacred2.exe`, do conjunto completo de
recursos e de um fingerprint original conhecido. A toolkit recusa a amostra
PT-BR conhecida. **Não é possível provar que bytes desconhecidos são inglês
original apenas lendo o cabeçalho RES.** Para uma edição nova, investigue sua
procedência e use `--approve-source HASH` com o hash exato mostrado pelo erro.
Essa opção é uma declaração explícita do operador, não um detector de idioma.
O caminho `--source-root`/`--source-file` também declara que você forneceu
originais; não aponte para uma tradução. O conjunto gerenciado é fechado:
arquivos faltantes ou extras exigem adaptação técnica, não são exclusões implícitas.

## Aplicação segura

Leia `translations/manifest.json`, escolha IDs do lote e monte um payload:

```json
{
  "generation": "copiar-do-manifesto",
  "entries": [
    {
      "id": "copiar-do-registro",
      "source_fingerprint": "copiar-do-registro",
      "PTBR": "texto manualmente traduzido"
    }
  ]
}
```

Somente PTBR pode ser alterado. IDs desconhecidos/duplicados, geração e
fingerprints incorretos abortam todo o payload. Depois disso, textos inválidos
são rejeitados individualmente e os demais são aceitos juntos. Reenvie apenas
os rejeitados corrigidos. Reaplicar o mesmo texto é idempotente. Para substituir
PTBR existente após revisão, use `apply --replace`; o anterior vai para history.
Uma expressão inglesa deliberadamente mantida deve ser escrita em PTBR;
vazio sempre significa pendente. Não há aprovação linguística automática.

## Atualizações, checkpoints e recuperação

O sync compara IDs com `accepted-sources` e JSONL, mesmo se EN já foi
sobrescrito. Alteração de um texto não invalida um arquivo inteiro. Mantém
PTBR, IDs e lote dos inalterados; registra mudança de posição; limpa PTBR de
modificados, guardando EN/PTBR anteriores em `history`. Remoções e renomes
(remoção + adição) ficam em `reports/history`. Novos registros usam o último
lote com espaço ou lotes sequenciais. Linhas duplicadas de texto com hashes
diferentes continuam independentes.

Cada operação mutável usa lock do sistema operacional, staging local,
comparação antes da promoção, journal durável e backups da geração anterior.
As renomeações de várias raízes **não são atomicidade física conjunta**:
o journal é o protocolo de recuperação. Leitores recusam estado interrompido;
a próxima operação mutável restaura os alvos anteriores antes de continuar.

```sh
python translation-work/toolkit.py recover
python translation-work/toolkit.py rollback --snapshot ID_DE_TRANSACAO
python translation-work/toolkit.py gc --dry-run
python translation-work/toolkit.py gc
```

### Eficiência e retenção das transações

Em aplicações parciais, a toolkit agora **substitui e mantém para rollback apenas os JSONL realmente alterados**; o manifesto e todos os lotes intactos conservam os mesmos bytes e mtimes. Operações de sincronização de originais e geração final podem afetar outras árvores, conforme seus arquivos reais.

Após uma transação concluída e verificada, a limpeza automática mantém até **10 snapshots finalizados** e **512 MiB** no total. `gc --dry-run` mostra o que pode ser recuperado sem apagar nada; `gc` remove apenas snapshots concluídos além da retenção, sob lock. Uma transação interrompida, sem recibo ou dependente de journal **não é descartada**. Quando existir journal, recupere antes de usar `gc`.

Os snapshots locais são recuperação rápida de operações recentes, **não um histórico ilimitado**. Para recuperar estados mais antigos, utilize as versões commitadas dos JSONL e fontes no Git, verificando antes se esses commits já foram enviados aos remotes. A limpeza não modifica EN, PTBR, traduções ativas, glossário ou arquivos do jogo.

Snapshots ficam em `.state/transactions/ID/old`, com `receipt.json`. Rollback
recusa sobrescrever progresso posterior e cria outro snapshot recuperável.
Uma extração inicial não tem geração anterior. Em conflito com edição manual,
preserve a edição antes de recuperar: a toolkit não a descarta. Esses snapshots
são locais; para checkpoints portáveis, versionar EN, accepted-sources, JSONL,
manifestos e relatórios juntos conforme a política Git de Yuri. Nenhum commit
ou push é feito pela toolkit.

## Build e distribuição

**Publicação automática no GitHub:** depois que a Ella concluir uma versão,
execute `check`, `build`, `verify-output`, `package`, commite `PTBR/` e
`translation-work/build-manifest.json` juntos e envie a `main` ao GitHub.
O workflow `.github/workflows/release.yml` verifica a integridade, empacota o
ZIP e **cria uma GitHub Release automaticamente**. A primeira é `v1.0.0`, as
seguintes incrementam o patch SemVer (`v1.0.1`, `v1.0.2` etc.).
As notas da Release são geradas comparando os registros PTBR e os arquivos
nativos com a última Release publicada. Reexecuções sem mudanças de PTBR não
geram outra versão. A introdução desse workflow após um build já publicado em
Git pode ser inicializada uma vez com `workflow_dispatch` na `main`.

Somente `build` toca PTBR. Exige todos os registros preenchidos, valida a sintaxe,
reconstrói em memória/staging e verifica a equivalência por parse nativo. Publica
o conjunto inteiro e seu recibo pela mesma transação recuperável. Falha preserva
a última saída. Um build repetido com o mesmo conteúdo é um no-op. O recibo liga
fontes, geração JSONL, versão do código e hashes de cada saída.

`verify-output` é offline e barato: verifica inventários/hashes/recibo sem
decodificar RES nem fazer novo build. Recusa saída antiga, faltante, extra,
editada ou sem recibo nativo. O recibo evita erros de publicação; não é uma
assinatura contra um mantenedor que altere deliberadamente código e manifesto.

`package` verifica novamente e cria `PTBR.zip` determinístico e ignorado pelo Git,
com `locale/...` diretamente na raiz, sem pasta PTBR. Reabre o ZIP, confere
membros únicos, integridade e hashes. O workflow em `.github/workflows/release.yml`
executa apenas em push de PTBR na `main` ou manualmente, com permissão somente
de leitura. Commits dos lotes não empacotam nada. Além do artefato, cria a GitHub Release com PTBR.zip e changelog.
Depois de um build concluído, versionar PTBR e build-manifest no mesmo commit.

Para baixar normalmente: GitHub → Releases → versão mais recente → Assets → PTBR.zip.\nO artefato do workflow também permanece disponível em Actions. A validação real\nda publicação deve ser conferida no GitHub após o primeiro acionamento.

## Primeiros passos da Ella

1. Ler este guia, `docs/formato-localizacao.md` e o [briefing pesquisado por Sayuri](docs/briefing-do-jogo.md).
2. Consultar as fontes e dúvidas registradas no briefing. Sayuri é responsável pela
   pesquisa e redação desse documento; Ella deve usá-lo como contexto e registrar
   descobertas ou necessidades de aprofundamento durante a tradução.
3. Criar `docs/diretrizes-de-traducao.md` e `docs/glossario-ptbr.md`, registrando decisões próprias.
4. Rodar status/check/diff; ler `translations/batch-0001.jsonl` e o contexto relacionado.
5. Traduzir manualmente em grupos pequenos. O lote de 500 é armazenamento, não
   tamanho obrigatório de uma etapa de tradução. Revisar a amostra anterior antes de reutilizar.
6. Aplicar por payload, validar, corrigir rejeições e salvar checkpoints.
7. Revisar concordância de nomes montados, personagens e termos entre lotes.
8. Em atualizações, sync e relatório orientam apenas o que precisa retradução/revisão.
9. Ao terminar todos os lotes: check, build, verify-output e package.
10. Yuri testa no jogo. **Não abrir nem controlar a interface do computador.**

O briefing foi pesquisado e escrito por Sayuri. Glossário e diretrizes linguísticas
serão escritos pela Ella, com decisões próprias antes da tradução em escala.
O briefing não aprova traduções nem substitui esses dois documentos.

## Testes

```sh
python -B -m unittest discover -s translation-work/tests -v
python -B translation-work/toolkit.py check
git diff --check
```

Veja `reports/engineering-validation.json` para evidências reais e limitações.
