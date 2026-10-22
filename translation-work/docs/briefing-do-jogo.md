# Briefing do jogo: Sacred 2 Gold

Pesquisa e redação: **Sayuri Mizuki**. Consulta: **22/10/2026**.

Este documento prepara a leitura da base inglesa pela Ella. Reúne contexto
narrativo, sistemas, evidências e questões de localização. **Não é glossário
aprovado nem tradução dos lotes.** As observações de linguagem indicam o que
precisa de decisão e revisão, sem preencher PTBR.

Contém informações sobre a premissa e personagens das campanhas. Não é um
walkthrough e não pretende revelar ou explicar todos os finais.

## 1. Qual jogo estamos traduzindo

O projeto trabalha com **Sacred 2 Gold**, que reúne **Sacred 2: Fallen Angel** e
a expansão **Ice & Blood**. É um RPG de ação de exploração, combate e coleta de
equipamentos em Ancaria. A expansão acrescenta uma sétima classe e duas regiões.
Essa composição consta na [página oficial da Gold no Steam][S1].

Há uma distinção editorial importante: a criação histórica está ligada à Ascaron;
a loja atual credita Studio II como desenvolvedor e THQ Nordic como publicadora.
O manual de época e a entrevista com o representante da Ascaron são fontes sobre
o jogo original; os créditos comerciais atuais não devem ser usados para apagar
essa história. [S1, S2, M1]

Apesar do número 2, a história ocorre aproximadamente **dois mil anos antes** das
aventuras do primeiro Sacred, segundo Alan Wild, então representante da Ascaron.
Não presumir que personagens, instituições ou lugares estejam no mesmo estado
da época do primeiro jogo. A entrevista é anterior ao lançamento: vale como
contexto declarado, não como prova de implementação de cada recurso anunciado. [S2]

**Base efetiva do repositório:** um conjunto inglês `en_UK`, com RES L10C versão
258 e oito CSVs. O manifesto registra 58.913 unidades: 57.989 textos no RES e 924
nos CSVs, divididos em 118 lotes. Esses números descrevem esta extração, não uma
edição universal do jogo. [R1]

O teste de Yuri mostra `v2.65.2 build 1837`. O Readme da instalação é mais antigo
e se identifica como 2.65.1; não substituir a versão vista na tela pela versão
desse documento. Há mods disponíveis na instalação, mas ainda não foi provado
quais afetaram a base inglesa. **Não chamar esta base de vanilla, Community Patch
ou Enhanced Edition sem comparação adicional.** Não usar material de Sacred 2
Remaster como autoridade automática para esta versão. [R2]

## 2. Premissa, conflito e regras do mundo

### Ancaria e a T-Energy

Ancaria é um mundo de povos, cultos e interesses rivais, no qual existe uma força
chamada **T-Energy**. Ela sustenta realizações mágicas e tecnológicas, mas sua
propagação fora de controle também contamina ambientes e transforma criaturas.
O elemento fantástico não exclui máquinas, armamentos avançados ou seres
artificiais. Tratar toda tecnologia como metáfora de feitiçaria distorceria o
cenário. [M1, introdução, p. 6; M1, Temple Guardian, pp. 30–31]

Segundo a introdução do manual, as Seraphim guardavam essa energia e transferiram
responsabilidades aos High Elves. O domínio da energia ajudou a tornar essa
civilização predominante. Houve oposição e uma guerra anterior envolvendo outros
povos; posteriormente, a disputa entre aristocracia e clero élficos pelo controle
da energia ameaça causar outra catástrofe. O perigo político e a deterioração do
próprio sistema energético se sobrepõem. [M1, p. 6]

As Dryads têm ligação histórica com os Elves, mas constituem uma cultura própria,
com relação particular com a natureza e com o culto de Kybele. Não tratá-las como
simples nome alternativo de High Elves. A descrição de Dyr Lain reforça essa
separação cultural. [M1, p. 6; R3, `1415182016`]

### Light e Shadow

Existem duas campanhas, **Light** e **Shadow**, com posições distintas diante da
crise. Não são apenas dificuldade, aparência, turno do dia ou tipo de dano.
Compartilham o mundo, mas a disposição do protagonista e os objetivos de algumas
missões mudam. Também há missões pessoais de classe, tarefas paralelas e cadeias
de missões. [M1, pp. 8–9; S2]

As Seraphim estão restritas à campanha Light; o Inquisitor, à Shadow. Outras
escolhas de classe e campanha influenciam as opções religiosas. Não concluir que
uma referência a Shadow transforma qualquer personagem em adepto de uma facção,
nem que todo uso de light significa a campanha. [M1, pp. 9, 25, 40]

### Verdade do mundo e ponto de vista

Livros, sacerdotes, registros de missão e falas podem narrar o mundo por perspectivas
diferentes. Uma afirmação de um personagem não deve ser promovida silenciosamente
a fato neutro do narrador. Há referências ao Creator, à Great Machine e às crenças
das Seraphim: esses conceitos devem permanecer distintos dos nomes dos seis deuses
selecionáveis. O registro `306329762`, por exemplo, relata o que Sophia teria dito
ao protagonista; isso é evidência de discurso atribuído. [M1, pp. 30–31; R3]

## 3. Povos, regiões e relações

O mapa abaixo é um roteiro de leitura do corpus, não uma ordem obrigatória de
viagem. As grafias são as inglesas; equivalentes PT-BR ainda dependem da Ella.

| Nome na fonte | Contexto confirmado | Evidência |
|---|---|---|
| Tyr Lysia | Região dos High Elves, com povoamento, rios e estruturas defensivas. | Livro geográfico `656824381`, lote 0015. |
| Thylysium | Nome de cidade associado à sociedade élfica; as instituições e seus papéis devem ser conferidos por missão. | Rótulo `140866065`, lote 0004; menções em livros do RES. |
| Artamark | Região humana descrita em um livro geográfico. A prosa também contém a variante “Aramark”. | `3772921790`, lote 0103. |
| Nor Plat | Região dos Orcs, no norte, com planícies frias e montanhas. | `2594051903`, lote 0061. |
| Bengaresh | Região desértica; o livro descreve clima, habitantes e costumes. | `236312129`, lote 0006. |
| Dyr Lain / Dyr-Lain | Ilha ligada às Dryads; o livro aborda isolamento, natureza e tensões com uma ocupação élfica. | `1415182016`, lote 0034; rótulo `250974483`, lote 0006. |
| Crystal region / The Bloodwood | Referências aos ambientes associados à expansão; conferir a forma exata de cada rótulo no contexto. | `56891204`, lote 0002; `710668046`, lote 0017; expansão confirmada em S1. |
| Wastelands | Região nomeada na base; não presumir que seja sinônimo dos ambientes de Ice & Blood. | `514089874`, lote 0012. |

Todos os IDs da tabela pertencem a `locale/en_UK/global.res`. Os livros são
documentos internos do mundo: podem incluir opiniões culturais, exageros ou
inconsistências editoriais. Ler o texto completo antes de padronizar sua voz.

As tensões não se resumem a “Elves bons versus Orcs maus”. Há conflitos internos
élficos, interesses humanos, comunidades de Dryads, dragões e estruturas antigas.
Evitar acrescentar uma moral uniforme onde a missão apresenta interesses locais.
Isso é uma consequência de leitura do manual e das missões, não uma facção nova
proposta pelo briefing. [M1, p. 6; R3]

## 4. Classes e protagonistas

O manual de PC cobre as seis classes de Fallen Angel. Para Dragon Mage, a fonte
mais direta desta base são os textos de apresentação da própria expansão. A
documentação promocional de 2008 ajuda a reconhecer arquétipos, mas contém nomes
de habilidades de pré-lançamento: o RES aceito prevalece para o texto efetivo. [M1, S3, R3]

| Classe inglesa | Identidade e contexto | Atenção na leitura |
|---|---|---|
| Seraphim | Guerreiras de aparência angelical, associadas à proteção de Ancaria; combinam armas, magia e tecnologia. Só Light. | A personagem jogável é feminina; a aparência celestial não elimina armas tecnológicas. Não confundir espécie/coletivo com nome próprio individual. |
| High Elf | Personagem feminina com longa formação mágica e diferentes especializações. | Distinguir a protagonista, o povo e títulos institucionais; podem exigir gêneros e números diferentes em PT-BR. |
| Dryad | Personagem feminina ligada à natureza, ao combate à distância e a práticas mágicas próprias. | Não apagar elementos de voodoo e hostilidade por presumir uma figura sempre dócil. |
| Temple Guardian | Ser parcialmente orgânico e tecnológico, ligado à proteção da Great Machine e da T-Energy. | Não é apenas um soldado que guarda um templo. Braço integrado, bateria e montaria mecânica têm significado literal. |
| Shadow Warrior | Combatente morto e trazido de volta por ritual, com experiência militar e ligação com os mortos. | Não presumir que o nome da classe obrigue à campanha Shadow. Morte anterior e retorno fazem parte da identidade. |
| Inquisitor | Figura masculina do clero élfico, ambiciosa e cruel, capaz de empregar forças sombrias e mortos. Só Shadow. | Diferenciar classe jogável, cargo religioso e o NPC Grand Inquisitor. |
| Dragon Mage | Classe de Ice & Blood; aspirante aos conhecimentos e poderes dos dragões. A apresentação fala em Dragon Magic, Elemental Magic e Mentalism. | Duas apresentações em primeira pessoa expressam ambição e vocação; não assumir que sejam falas do mesmo momento ou do mesmo percurso. |

Fontes: manual, pp. 24–35; apresentações `154472996` (lote 0004) e `282973926`
(lote 0007). A tabela descreve papéis; não fixa uma voz idêntica para todas as
falas de uma classe nem aprova traduções dos nomes.

### Figuras que merecem rastreamento entre lotes

- **Sophia:** interlocutora associada às Seraphim. Uma missão atribui a ela uma
  decisão contra o dragão Magmadur após ataques e a morte de uma emissária.
  Conservar quem ordena, quem relata e quem executa a tarefa. [R3, `55255625`, lote 0002]
- **Liosilath:** interlocutor e referência recorrente na investigação da campanha.
  As entradas consultadas mostram outros personagens encaminhando o protagonista
  até ele. Sua função em cada etapa precisa ser reconstruída pela cadeia de missões,
  sem inferir alinhamento só pelo tratamento cordial. [R3, `81394101`, lote 0002;
  `257815911`, lote 0006]
- **Mer-Kil:** dragão antigo que fornece informações, abre passagem e negocia
  condições com o protagonista. Não é intercambiável com qualquer dragão inimigo.
  [R3, `84645384`, lote 0002; `138381191`, lote 0003]
- **Grand Inquisitor:** título de um NPC relevante, distinto da escolha de classe.
  Confirmar referentes antes de traduzir uma fala dirigida ao “Inquisitor”.
  [R3, rótulo `2694673119`, lote 0065; missão `289740427`, lote 0007]

Esses apontamentos são um índice inicial, não biografias completas ou revelações
de identidade. Relações e motivações posteriores devem ser documentadas conforme
as missões forem lidas.

## 5. Divindades e religião

O manual descreve seis divindades selecionáveis e um poder especial concedido
pela escolha religiosa. São personagens do cenário, não simples nomes de elementos.
O gênero abaixo é sustentado pelos títulos ingleses e pelo manual. [M1, p. 40; R3]

| Nome | Domínio na fonte | Referência do RES |
|---|---|---|
| Lumen | Deus da luz. | `39003190`, lote 0001. |
| Kybele | Deusa da natureza. | `51989263`, lote 0002. |
| Forens | Deusa da filosofia e sabedoria. | Descrição `194738937`, lote 0005. |
| Testa | Deus da ciência. | `222693490`, lote 0005. |
| Kuan | Deus da guerra. | `107861816`, lote 0003. |
| Ker | Deusa do caos. | `22248227`, lote 0001. |

Os poderes incluem efeitos como proteção, cura, reflexão de ataques ou intervenção
ofensiva, com tempo de regeneração próprio. A escolha de campanha e algumas
classes restringem a escolha religiosa. **Não aplicar números, regras de balanceamento
ou listas de disponibilidade de mods a esta base sem verificar seus textos.** [M1, p. 40]

Culto, templo, sacerdote e oferenda têm função narrativa e também mecânica.
Forens, por exemplo, aparece em uma descrição extensa de mitologia e culto;
isso exige voz diferente de um tooltip curto do poder divino. [R3, `194738937`]

## 6. Sistemas e onde os textos aparecem

### Progressão e combate

O manual distingue **attributes**, **skills**, **combat arts** e **aspects**.
Não tratar as quatro categorias como sinônimos. Há artes aprendidas ou elevadas
por runas, grupos de especialização, pontos de modificação e efeitos associados
a habilidades. O jogador também combina artes e mantém efeitos do tipo buff.
[M1, pp. 14–17, 22–23, 38–39]

**Regeneration time** em descrições de artes diz respeito à disponibilidade de
uso, não necessariamente à recuperação de vida. A base contém descrições que
reduzem o tempo de um aspecto e elevam o limite sem penalidade. Um equivalente
PT-BR deve deixar clara a mecânica em cada contexto. [R3, `34014526`, lote 0001;
`57948169`, lote 0002]

Outros sistemas que precisam de consistência incluem equipamento e modificadores,
resistências, forja e encaixes, montarias, inventário, troca de runas, missões,
mapa, pontos de retorno e modos de jogo. O **carrier imp** presta uma função de
transporte de itens; não é outro nome do Temple Guardian. O Readme de Ice & Blood
registra mudanças nesse companheiro e na personalização. [M1; R2]

**Hardcore** é uma regra de morte permanente, distinta do nível de dificuldade.
**Light/Shadow** é outra dimensão, a campanha. Não fundir essas três escolhas.
O **Survival Bonus** é um rótulo próprio do sistema, e também aparece em uma
provocação que quebra a imersão de propósito. [M1, p. 9; R3, `1117117040`, lote
0026; `232300801`, lote 0005]

### Tipos de texto

| Tipo | Como reconhecer e revisar |
|---|---|
| Menus e rótulos | Frases curtas, frequentemente isoladas. Verificar o espaço disponível e o que o botão faz. |
| Tooltips e atributos | Precisão mecânica; preservar valores, parâmetros, condições e nomes de sistemas relacionados. |
| Falas de NPCs e do protagonista | Identificar emissor, destinatário, classe, campanha e atitude antes de escolher tratamento e tom. |
| Objetivos e diário de missão | Distinguir ordem ainda pendente de relato do que já aconteceu; a primeira pessoa do diário não é automaticamente fala em voz alta. |
| Livros e inscrições | Voz de autor interno ao mundo, descrição cultural ou relato histórico; podem conter narradores parciais e humor. |
| Nomes de itens e fragmentos CSV | Testar o nome composto, não apenas a tradução isolada de cada palavra. |
| Ajuda e mensagens técnicas | Traduzir o texto visível sem inventar teclas, ícones, caminhos, parâmetros ou funcionamento de serviços. |

Os hashes identificam textos, mas não codificam por si só quem fala ou em que
missão aparecem. A proximidade entre linhas ou lotes não prova sequência de
diálogo. Localizar referências relacionadas no corpus e, se necessário, investigar
scripts em modo de leitura; nunca reordenar IDs para “organizar” uma conversa.
[R1; formato-localizacao.md]

## 7. Tom, humor e consequências para PT-BR

**Observações de pesquisa, sujeitas à revisão da Ella:**

- O jogo mistura ameaça épica, sátira, crueldade e humor cotidiano. Não impor
  solenidade medieval a toda frase. O livro de etiqueta `10697463` (lote 0001)
  associa etiqueta e conflitos absurdos; a piada é intencional no contexto do livro.
- Há vozes cínicas e autodepreciativas. O texto `79662329` (lote 0002) apresenta uma
  High Elf reclamando da própria imagem; isso não autoriza a mesma informalidade
  em uma oração ou registro oficial.
- O jogo faz referências ao próprio funcionamento. A provocação sobre o Survival
  Bonus (`232300801`) deve ser lida como tal, não “corrigida” para algo mais realista.
- **Blind Guardian** existe no conteúdo como banda, com missão e instrumentos.
  A ajuda `223097526` (lote 0005) e o diário `1788219232` (lote 0042) sustentam
  essa presença. Não confundir o nome com uma categoria de guardiões do mundo.
  Não copiar letras de músicas para o briefing.
- O vocabulário religioso é ficcional e varia por culto e personagem. Não substituir
  os deuses do cenário por referências religiosas externas nem suavizar uma fala
  cruel por parecer inadequada ao personagem heroico de outra campanha.

Para PT-BR, a revisão precisa resolver sujeitos omitidos, gênero da personagem,
plural de povos, títulos, tratamento e referência de pronomes. A palavra **you**
isolada não resolve quem fala nem quantas pessoas são interpeladas. A voz deve
acompanhar o personagem e a situação, sem simular diferenças culturais por meio
de caricaturas regionais brasileiras não sustentadas pelo original.

Essas são implicações de leitura, não um conjunto de traduções aprovadas. A Ella
deve registrar suas decisões em diretrizes e glossário, incluindo exceções e dúvidas.

## 8. Termos que exigem decisão linguística

| Inglês/contexto | Questão para a Ella |
|---|---|
| T-Energy | Escolher forma PT-BR, capitalização e composição com outros termos, sem apagar a relação entre magia e tecnologia. |
| Light / Shadow | Distinguir campanha, luz/sombra comuns, alinhamento e eventual efeito de combate. |
| High Elf / Seraphim / Dryad | Distinguir classe jogável, indivíduo e coletivo; definir gênero e plural conforme o referente. |
| Inquisitor / Grand Inquisitor | Separar classe, título e NPC. |
| skill / combat art / aspect / attribute | Reservar termos distintos para as categorias do sistema. |
| regeneration | Separar tempo de reutilização de arte de recuperação de vida ou outros recursos. |
| lore / focus | Identificar habilidades específicas antes de padronizar o sentido de palavras comuns. |
| buff / Divine Gift / Survival Bonus | Definir tratamento coerente entre interface, tooltip e menção em diálogo. |
| Great Machine / Creator | Definir tratamento de conceitos próprios sem confundi-los com divindades ou máquinas genéricas. |
| Dyr Lain / Dyr-Lain; Artamark / Aramark | Registrar grafias divergentes, evidência e decisão editorial sem modificar EN. |
| Prefixos e sufixos de itens | Rever combinações de gênero, número e preposição no nome final. |

Os CSVs podem montar um nome com fragmentos independentes. Preservar delimitadores,
chaves e metadados é uma obrigação técnica; isso não garante concordância. Não
alterar o gerador, `hasGender=false` ou gameplay para contornar um problema de
redação. Rever exemplos compostos e registrar limites. [R1; formato-localizacao.md]

## 9. Lacunas e cuidados antes de traduzir em escala

1. **Afiliação da base a patches:** confirmar a origem exata se isso se tornar
   necessário para compatibilidade ou publicação. Não anunciar suporte a mod por
   encontrar sua pasta na instalação.
2. **Contexto de diálogos:** os IDs não identificam automaticamente os emissores.
   Registrar dúvidas por ID e buscar a cadeia de missão correspondente.
3. **Grafias e nomes localizáveis:** não resolver divergências do inglês por
   substituição global; aprovar decisões no glossário com seus contextos.
4. **Expansão:** o manual de 2008 não cobre Dragon Mage nem todas as mudanças de
   Ice & Blood. Usar os textos aceitos e o Readme adicional para esse conteúdo.
5. **Markup e anotações:** `<br>`, tags de interface e referências a ícones são
   protegidos. Descrições entre sinais de menor/maior também podem ser marcações
   de gravação; a toolkit as preserva conservadoramente. Investigar antes de
   propor sua tradução ou de alterar o validador.
6. **Interfaces de console dentro do corpus:** referências a botões Xbox existem
   no RES de PC. Não trocar ícones por teclas arbitrárias nem concluir que toda
   entrada esteja visível nesta plataforma.
7. **Serviços históricos:** OpenNet, ClosedNet, ativação e suporte do manual são
   conteúdo de época. A tradução de um texto não comprova a disponibilidade atual
   do serviço. Não transformar esses trechos em instruções atuais ao usuário.
8. **Verificação visual:** o teste anterior confirma somente uma amostra de menus
   e glifos. Yuri testa os arquivos no jogo; não abrir nem controlar a interface.
9. **Cobertura da pesquisa:** este briefing é uma base de trabalho, não uma leitura
   integral das 58.913 entradas. Novas relações, piadas e exceções devem ser
   acrescentadas com evidências conforme os lotes avançarem.

## 10. Sequência de trabalho e responsabilidades

**Sayuri** pesquisa e escreve o briefing; corrige e complementa o contexto quando
necessário. **Ella** usa essa pesquisa, consulta as fontes e assume a tradução,
o glossário, as diretrizes linguísticas e a revisão. **Yuri** testa no jogo e decide
questões de escopo e publicação. A toolkit apenas organiza e valida o trabalho.

Antes de começar, a Ella deve ler este documento e `formato-localizacao.md`,
consultar `status`/`diff`, definir as primeiras decisões de terminologia e estilo
e então abrir `batch-0001.jsonl`. Traduzir em grupos pequenos com contexto,
aplicar apenas PTBR, validar e salvar checkpoints. Não é necessário refazer do
zero a pesquisa já documentada aqui; dúvidas novas devem ser registradas e
investigadas, sem inventar respostas.

## Fontes e como conferir

**[S1]** [Sacred 2 Gold — Steam](https://store.steampowered.com/app/225640/Sacred_2_Gold/).
Página oficial de distribuição: composição Gold, expansão e créditos atuais.
Consultada em 22/10/2026. Não usada para afirmar a afiliação da instalação a mods.

**[S2]** [Entrevista com Alan Wild — GameWatcher, 16/11/2007](https://www.gamewatcher.com/interviews/sacred-2-fallen-angel-interview/11457).
Depoimento de um representante da Ascaron: cronologia, duas campanhas e estrutura
de missões. Fonte primária em entrevista, anterior ao lançamento; promessas de
recursos não substituem o conteúdo efetivo. Consultada em 22/10/2026.

**[S3]** [Ascaron, The Characters — material promocional de Fallen Angel, arquivo GC2008](https://sacred-tribute.com/webarchive/GC2008/content/Game%20Information/S2FA_Characters.pdf).
Documento primário preservado por um arquivo comunitário; identifica os seis
arquétipos originais e a mistura de tecnologia e magia. Consultado em 22/10/2026.
Nomes de artes de pré-lançamento não são adotados como cânone da base atual.

**[M1]** Manual de PC incluído na instalação, `locale/en_UK/Manual.pdf`, lido
diretamente em modo somente leitura. A paginação citada é **a impressa no manual**:
o PDF tem 33 páginas, com várias páginas duplas. Partes consultadas: introdução
(p. 6), criação (pp. 8–9), interface e sistemas (pp. 14–23), classes (pp. 24–35),
runas e modificações (pp. 38–39), divindades e forja (pp. 40–41).
Não é copiado para o repositório. Como referência pública complementar, existe
um [manual oficial da versão Xbox 360 preservado no mesmo arquivo](https://sacred-tribute.com/archive/SACRED/SACRED2/Documents/Ascaron/Manuals/XBOX360/Sacred_2_XBox360_EN.pdf);
ele não substitui os controles nem a paginação da edição PC.

**[R1]** [Manifesto aceito](../translations/manifest.json),
[catálogo inglês](../../EN/locale/en_UK/) e
[documentação do formato](formato-localizacao.md).
Geração consultada: `52ac93bbf34f8812a15ea2a3025c5e07c06f4cd7724b114ca6c49539f1c79fdd`.

**[R2]** Readme original de Ice & Blood, `Readme.txt` na instalação, datado de
18/10/2009 e identificado como 2.65.1; captura de tela fornecida por Yuri nesta
conversa, com `v2.65.2 build 1837`; limites técnicos registrados no
[relatório de validação](../reports/engineering-validation.json).
Arquivos externos e imagem não são presumidos disponíveis em um clone novo.

**[R3]** Registros ingleses versionados em [translations/](../translations/).
Para conferir uma referência, abrir o lote indicado e buscar o ID completo:
`locale/en_UK/global.res#NUMERO`. Os trechos foram usados como evidência interna,
sem modificar EN ou PTBR. Números de lote refletem a geração acima e podem deixar
de localizar uma entrada após reorganizações futuras; o ID nativo é a referência
principal. As interpretações de voz, tom e consequências linguísticas deste
briefing são análise de Sayuri, distinguida dos fatos explícitos das fontes.

[S1]: https://store.steampowered.com/app/225640/Sacred_2_Gold/
