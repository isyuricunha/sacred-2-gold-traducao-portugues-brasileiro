# Progresso — Sacred 2 Gold PT-BR

Registro vivo da Ella. Atualizar a cada checkpoint validado. O estado técnico
de verdade é `python translation-work/toolkit.py status`; este arquivo guarda
decisões, problemas e a próxima etapa.

## Estado

- Geração: 52ac93bbf34f8812a15ea2a3025c5e07c06f4cd7724b114ca6c49539f1c79fdd
- Corpus: 58.913 entradas, 118 lotes (RES 57.989 + CSVs 924)
- Traduzido: 30.000/58.913 (50,9%)
- Última etapa concluída: lote 0058 aplicado e commitado (29.000/58.913)

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
- 0038 (500 entradas) - aplicado sem rejeicoes; marco de 19.000 entradas; tirano discursa do 339 feminizado
- 0039 (500 entradas) - aplicado; grupo a ficou com 100 entradas na primeira escrita (25 faltavam), completado antes do apply; Livro 6 (Magia Proibida) e Livro 4 Lumen traduzidos
- 0040 (500 entradas) - aplicado; marco de 20.000 entradas (34%); Livro 2 (ervas) e Livro Goblinoide traduzidos; percentuais literais convertidos para por cento
- 0041 (500 entradas) - aplicado; 2 rejeicoes corrigidas (newline meu em Cripta dos Condenados e br faltando); Livro de Goblinoide detalhado e Funerarios Unidos traduzidos
- 0042 (500 entradas) - aplicado; marco de 21.000 entradas (35,6%); duas frases fracas minhas corrigidas antes do apply (1758516603, 1760529810); Cripta dos Condenados completa traduzida
- 0043 (500 entradas) - aplicado; texto do Fantasma da cama de 1816309966 mantido em EN (EN igual), sem traducao inventada; Guilhotina do Veredicto traduzida
- 0044 (500 entradas) - aplicado; marco de 22.000 entradas (37,3%); discurso do bibliotecario e 1895682754 (Dranaigh) traduzidos; fala de Troll mantida goblinizada
- 0045 (500 entradas) - aplicado; Livro 5 (Kuan) e diario do arqueologo traduzidos; 80 % e 100 por cento convertidos em por cento
- 0046 (500 entradas) - aplicado sem rejeicoes; marco de 23.000 entradas (39%); Livro 5 Kuan versao longa; perguntas politicas de escravos traduzidas
- 0047 (500 entradas) - aplicado; marco de 23.500 entradas (39,9%); diario do mago (31 Tyrbor a 25 Yal) e Livro 5 Kuan longo traduzidos; livreto da arte da armadilha traduzido
- 0048 (500 entradas) - aplicado; marco de 24.000 entradas (40,7%); salarios de soldadas, santificacao de Orczinhos e doacoes politicas traduzidos; falas com sotaque Mantling e Alemao mantidas
- 0049 (500 entradas) - aplicado; marco de 24.500 entradas (41,6%); livreto de Pesca e dialogo do bar do fado traduzidos; linha do mestre do desenho mantida em Alemao
- 0050 (500 entradas) - aplicado; marco de 25.000 entradas (42,4%); entrada de Gaia completa traduzida; focos e concordias de aspectos padronizados
- 0051 (500 entradas) - aplicado; 2 rejeicoes corrigidas (b tag em Equipar item, e 38 IDs inventados no grupo b removidos antes do apply); diario do mago dragao traduzido; 50 % convertido em por cento
- 0052 (500 entradas) - aplicado; 1 erro meu corrigido antes do apply (newline dentro de string em 2263944713); tela de personagem Guerreiro das Sombras e aviso de seguranca Wi-Fi ad hoc traduzidos; linha de tabs alema mantida exata
- 0053 (500 entradas) - aplicado; marco de 26.500 entradas (45%); dialogo A Revolutionary Idea (2302679868) traduzido na integra; dialogo do dragao e conselho do produtor traduzidos
- 0054 (500 entradas) - aplicado; marco de 27.000 entradas (45,8%); conquistas de trajetoria (Portadora da Luz, Cartografa etc) padronizadas; conversas de cauda do Homem-Lagarto traduzidas; 20 pounds convertido
- 0055 (500 entradas) - aplicado sem rejeicoes; marco de 27.500 entradas (46,7%); abertura da campanha (2373488556-62) e Livro 5 (banquete) traduzidos; falas de Trolls goblinadas mantidas
- 0056 (500 entradas) - aplicado; 1 erro meu corrigido antes do apply (3 chaves com general.res em vez de global.res); guia Seduzir Aristocratas e casamento adiado traduzidos; sotaque alemao do Ze mantido
- 0057 (500 entradas) - aplicado sem rejeicoes; marco de 28.500 entradas (48,4%); Livro 3 (Venenos de Ancaria) traduzido na integra; nomes de lugares do mapa padronizados
- 0058 (500 entradas) - aplicado sem rejeicoes; marco de 29.000 entradas (49,2%); itens de missao em serie (discos de identificacao, jade, pelos) padronizados; grupo d reconstruido casando a ordem do lote apos IDs com sufixo errado
- 0059 (500 entradas) - aplicado sem rejeicoes; itens de missao em serie em massa (400+ nomes de item); par com chaves falsas reconstruido casando a ordem do lote
- 0060 (500 entradas) - aplicado; marco de 30.000 entradas (50,9%): metade do corpus alcancada; Livro 6 (Ker) traduzido na integra; sobrenome de assassinio e conselho de estepes traduzidos

## Decisões e problemas abertos

- Glossário semente criado com as decisões do briefing (T-Energia, classes,
  deuses, sistemas). Ajustes entram como patches no glossário.
- Confirmar rótulos exatos de "Crystal region" e "The Bloodwood" no corpus
  antes de fixar a tradução (glossário marca para conferir).
- "Testa" (deus da ciência) mantém a grafia EN; colisão com "testa" é aceita
  como nome próprio.

## Próxima etapa

Traduzir batch-0061 (grupos pequenos, apply por payload, commit por lote). POLITICA DE PUSH: commits locais por lote; push unico nos tres remotes somente no final, por ordem de Yuri (2026-10-22).
