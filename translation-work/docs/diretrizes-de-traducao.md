# Diretrizes de tradução — Sacred 2 Gold (PT-BR)

Decisões de estilo e procedimento da Ella, baseadas no briefing da Sayuri e no
formato técnico da toolkit. O glossário do projeto é `glossario-ptbr.md`; este
documento define as regras, aquele define os termos.

## Público e tom

- RPG de ação com humor, sátira e crueldade. Não impor solenidade medieval a
  todo texto; cada voz segue o personagem e a situação (orção, etiqueta, diário
  de missão, provocação que quebra a quarta parede).
- Tratamento: **você** em falas e interface. "You" isolado não define número nem
  papel: inferir do contexto (missão, classe, campanha) antes de escolher.
- Diário de missão em primeira pessoa não é fala em voz alta: manter o registro
  do EN (pendência como ordem, conclusão como relato).
- Nada de caricatura regional brasileira para simular diferença cultural.

## Termos do sistema (ver glossário para a forma final)

- `skill` = habilidade; `combat art` = arte de combate; `aspect` = aspecto;
  `attribute` = atributo. Não usar esses termos como sinônimos.
- `regeneration time` de arte de combate = tempo de regeneração (disponibilidade
  de uso), não recuperação de vida.
- Campanha **Luz / Sombras** (Light / Shadow) é dimensão própria, distinta de
  dificuldade e de Hardcore. Luz/sombra comuns ficam minúsculas.
- Great Machine = Grande Máquina; Creator = Criador: conceitos próprios, nunca
  confundir com os seis deuses nem com máquinas genéricas.

## Nomes próprios

- Pessoas, deuses e lugares com forma consagrada no glossário. Sem decisão
  registrada, mantém-se a grafia inglesa.
- Grafias divergentes no EN (Dyr Lain / Dyr-Lain, Artamark / Aramark): o PT usa
  a forma padronizada do glossário em todos os casos; o EN não é corrigido.
- Blind Guardian é a banda (missão própria no jogo): nunca traduzir.
- Povos e classes com maiúscula (Altos Elfos, Dríades). Singular/plural e gênero
  seguem o referente da frase, não a palavra inglesa.

## Interface e itens

- Title Case do EN vira "Primeira Maiúscula" em PT-BR (Salvar jogo, não Salvar
  Jogo), salvo nome próprio.
- Nomes de itens são compostos por fragmentos (CSV/NameGen): revisar o nome
  montado (gênero, número, preposição), não só a palavra isolada. Prefixo e
  sufixo precisam concordar com o nome base.
- `hasGender=false`, sufixos numéricos `,1` e células vazias são estrutura:
  nunca alterar.

## Codificação e sintaxe (obrigatório)

- Saída estrita em Windows-1252 para CSV; o RES codifica UTF-16 internamente.
  Acentos PT-BR são permitidos e desejados; nada de caracteres fora do 1252
  (sem travessão longo, sem aspas curvas, sem ellipsis "…" se o EN não usa).
- Preservar tags e sua ordem: `<br>`, `<b>`, `<AlignH Value=Center/>`,
  `<$ID_CUI_...>` e anotações desconhecidas entre `<...>` (copiar, não traduzir
  nem "consertar").
- Preservar formatos printf e parâmetros: `%1`, `%d`, `%{###,###}1`, URLs.
  O validador confere multiplicidade e ordem dos não posicionais.
- Markup legado desequilibrado do EN permanece desequilibrado. Não corrigir o
  inglês nem adicionar tags que o original não tem.
- Números, moedas e unidades seguem o padrão do próprio texto (não converter
  sistema métrico/imperial nem moeda).

## Procedimento de trabalho

- Tradução manual, sem API ou serviço externo; grupos pequenos com contexto
  lido antes (a frase vizinha importa).
- Aplicar por `toolkit.py apply --payload`, apenas o campo `PTBR`; rejeição é
  corrigida e reenviada; nunca editar EN, key, row, source_file ou fingerprint.
- Reaproveitar texto repetido só quando semanticamente equivalente no mesmo
  contexto; as 63 traduções de `reference/menu-sample.json` são referência a
  revisar, não aprovadas.
- `apply --replace` apenas em revisão deliberada (o anterior vai para history).
- Checkpoint por lote: commit + push nos três remotes após validar.
- Registro de progresso: `translation-work/PROGRESS.md`, atualizado por marco.
- Nunca gerar PTBR/ parcial; nunca alegar teste in-game (é do Yuri).
