# Progresso — Sacred 2 Gold PT-BR

Registro vivo da Ella. Atualizar a cada checkpoint validado. O estado técnico
de verdade é `python translation-work/toolkit.py status`; este arquivo guarda
decisões, problemas e a próxima etapa.

## Estado

- Geração: 52ac93bbf34f8812a15ea2a3025c5e07c06f4cd7724b114ca6c49539f1c79fdd
- Corpus: 58.913 entradas, 118 lotes (RES 57.989 + CSVs 924)
- Traduzido: 18.500/58.913
- Última etapa concluída: leitura dos docs; diretrizes e glossário iniciais

## Lotes concluídos

- 0001 (500 entradas) - 4 payloads aplicados sem rejeicoes apos fix de anotacoes <...> protegidas
- 0002 (500 entradas) - 1 rejeicao: "5% do" criou token falso % d; fix "5 por cento do". Termos novos no glossario pendentes de patch: flores-de-anel, bateda (drive), Gargantopode, aspectos Piromante Absoluto/Tecnologia Venerada/Supremacia Astuta/Submundo Nefasto
- 0003 (500 entradas) - aplicado sem rejeicoes; textos em alemao (122143345) e TODO/TEST mantidos como no EN
- 0004 (500 entradas) - aplicado sem rejeicoes; termos novos pendentes de patch no glossario: erutraia, Tempestino Mistico, aspectos/mods do Inquisidor e Guardiao do Templo
- 0005 (500 entradas) - aplicado sem rejeicoes; dois livros longos (receitas, anatomia) e varios textos de ajuda de interface traduzidos
- 0006 (500 entradas) - aplicado sem rejeicoes; livro de Bengaresh e segundo livro de receitas; placeholders dev (yalla yalla, asdf, asdfasdf) mantidos exatos
- 0007 (500 entradas) - aplicado; 1 rejeicao: lapide de Chevy Chase tem newline real no EN (mudanca de contagem de quebras nativas); corrigida com newline real
- 0008 (500 entradas) - aplicado sem rejeicoes; telas de erro de rede multiplayer traduzidas; alemaes e notas dev mantidos
- 0009 (500 entradas) - aplicado; 1 rejeicao persistente: EN com newlines reais internos e final (missao do nargutz); causa raiz era strip() do helper remover newline final; helper corrigido (sem strip) e entrada aceita
- 0010 (500 entradas) - aplicado sem rejeicoes; primeiro marco de 5.000 entradas
- 0011 (500 entradas) - aplicado sem rejeicoes; livro do ervanario, caderno de Diaanja, guia de banquete e guia de mortos-vivos traduzidos
- 0012 (500 entradas) - aplicado; 1 rejeicao: ordem de tags </i><br></b> no titulo Mead do livro de bebidas divergia; replicada a ordem exata do EN
- 0013 (500 entradas) - aplicado sem rejeicoes; dialogo com polemica de fe da sacerdotisa e goblinada mantidas no tom
- 0014 (500 entradas) - aplicado sem rejeicoes; livro de armas (Book 1) traduzido integralmente; falas de Ogro mantidas goblinadas
- 0015 (500 entradas) - aplicado; 2 erros meus: ID 668471123 digitado errado (o real e 668471122, Martelo) e 15 IDs de Coracao de Esportista Orc inventados no grupo d; helper recusou ambos e corrigi; lote 0015 fechado em commit separado (79cf92c)
- 0016 (500 entradas) - aplicado sem rejeicoes; itens de teste TESTE mantidos com rotulos de teste; nomes de item consistentes
- 0017 (500 entradas) - aplicado sem rejeicoes; lapides de jogadores e dialogo de casamento de guerreiro Orc no tom; libras convertidas (300 pounds -> 150 quilos, six feet -> dois metros)
- 0018 (500 entradas) - aplicado sem rejeicoes; servidores de paises por regiao; marcador de 9.000 entradas
- 0019 (500 entradas) - aplicado sem rejeicoes; nomes estilizados de jogadores mantidos; alemaes (tote das pack, Leber, Barenzahn) mantidos
- 0020 (500 entradas) - aplicado sem rejeicoes; marco de 10.000 entradas; livro 1 de Kybele e tela de atributos traduzidos
- 0021 (500 entradas) - aplicado sem rejeicoes; concordias de aspectos padronizadas (Concordia de X); alemaes mantidos
- 0022 (500 entradas) - aplicado; 2 rejeicoes corrigidas: sobra de newline que eu mesma inseri (935340693) e, antes, trocada a palavra potions (0021); livro de cozinha Orc e livro 2 de Testa traduzidos
- 0023 (500 entradas) - aplicado; 2 rejeicoes corrigidas: <Deep sigh> e sintaxe protegida (copiado exato) e 1000376612 texto grego/arameu misto de dev (definido igual ao EN); creditos da equipe de localizacao PT mantidos
- 0024 (500 entradas) - aplicado sem rejeicoes; livro dos Anoes e textos de testemunho de seletor de gladiadores traduzidos; marco de 12.000 entradas
- 0025 (500 entradas) - aplicado sem rejeicoes; lapides humoristicas e creditos em frances mantidos; notas de som <...> copiadas exatas
- 0026 (500 entradas) - aplicado; grupo c tinha 124 entradas (1 entrada faltava, 1129089054 AH! Droga!), aplicada depois; marco de 13.000 entradas; concordia Senhor Astral adicionada
- 0027 (500 entradas) - aplicado sem rejeicoes; ordem do usuario: commit por lote SEM push (push unico no fim do projeto)
- 0028 (500 entradas) - aplicado sem rejeicoes; marco de 14.000 entradas; falas goblinizadas de Goblin e Trolls mantidas
- 0029 (500 entradas) - aplicado; 1 erro meu: chave locau/Ue digitada errada e faltou 1244357989; corrigi antes do apply; lotes de conjuntos de itens (Sarakis, Armantin, Lucretis, Denderan, Endijian/Niokaste/Celestial, Celdrahil/Faladal, Daerwain, Detheya, T-Energy, Demiurgo) padronizados
- 0030 (500 entradas) - aplicado sem rejeicoes; marco de 15.000 entradas (25,5%); conjuntos de Natal (Branco/Feliz/Sombrio) e conjuntos Velaria/Virgo/Perdicao padronizados
- 0031 (500 entradas) - aplicado; 1 rejeicao: cita de Archilochus tinha <br> protegido que eu quebrei em linha a mais; corrigi; oito feet na fala de arvore convertidos para metros e meios (2,5 m)
- 0032 (500 entradas) - aplicado sem rejeicoes; conjuntos Dimiona/Arbereth/Tallin/Glimborin/Megalcarwen/Mormorin padronizados; marcador de 16.000
- 0033 (500 entradas) - aplicado; 2 correcoes: chave errada minha (9b/9x, removidas antes do apply) e tag </b> faltando em Memorizar runa; discurso de Sophia versao feminina aplicado
- 0034 (500 entradas) - aplicado; 1 rejeicao: newline final meu em lembrancas de zumbi; removi; manual da Rainha da Caça (Plano de Cristal) traduzido; 9 feet -> ~3 m na planta Phylitos
- 0035 (500 entradas) - aplicado; 2 rejeicoes corrigidas: tag </b> em Equipar poção e 20 % -> 20 por cento; caminho das elfas meninas (Como Enfeitiçar Aristocratas) traduzido
- 0036 (500 entradas) - aplicado; marco de 18.000 entradas (30,6%); livro de magia (Livro 1) e Livro 4 Dyr Lain traduzidos; falas de Ogre goblinadas
- 0037 (500 entradas) - aplicado; 1 correcao de redacao propria (1517408408); saga do Beltorak e entrada de Lumen traduzidas
- 0009 (500 entradas) - aplicado sem rejeicoes; fala boba de Troll/Orc goblinizada propositalmente; notas de som <...> copiadas exatas

## Decisões e problemas abertos

- Glossário semente criado com as decisões do briefing (T-Energia, classes,
  deuses, sistemas). Ajustes entram como patches no glossário.
- Confirmar rótulos exatos de "Crystal region" e "The Bloodwood" no corpus
  antes de fixar a tradução (glossário marca para conferir).
- "Testa" (deus da ciência) mantém a grafia EN; colisão com "testa" é aceita
  como nome próprio.

## Próxima etapa

Traduzir batch-0038 (grupos pequenos, apply por payload, commit por lote). POLITICA DE PUSH: commits locais por lote; push unico nos tres remotes somente no final, por ordem de Yuri (2026-10-22). LOTE 0015 CONCLUIDO (7.500/58.913): o commit da874a3 foi feito com so 375 strings aplicadas; as 125 finais entraram em commit separado.
