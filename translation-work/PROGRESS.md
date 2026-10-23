# Progresso — Sacred 2 Gold PT-BR

Registro vivo da Ella. Atualizar a cada checkpoint validado. O estado técnico
de verdade é `python translation-work/toolkit.py status`; este arquivo guarda
decisões, problemas e a próxima etapa.

## Estado

- Geração: 52ac93bbf34f8812a15ea2a3025c5e07c06f4cd7724b114ca6c49539f1c79fdd
- Corpus: 58.913 entradas, 118 lotes (RES 57.989 + CSVs 924)
- Traduzido: 48.000/58.913 (81,5%)
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
- 0061 (500 entradas) - aplicado; 1 rejeicao corrigida (ordem de tags em Cerveja no Livro 3); marco de 30.500 entradas (51,8%); Livro 3 Nor Plat e Livro 3 Bebendo em Ancaria traduzidos na integra; etiqueta de Kobold com reversos mantidos
- 0062 (500 entradas) - aplicado; marco de 31.000 entradas (52,6%); Livro 3 Bebendo em Ancaria concluido; lapides de easter eggs (42, De nihilo nihil) traduzidas
- 0063 (500 entradas) - aplicado; marco de 31.500 entradas (53,5%); nomes de NPCs em serie (Badawi e soldadas de Orc) padronizados; 2 grupos com entradas a mais corrigidos por casamento EN->PT antes do apply
- 0064 (500 entradas) - aplicado; marco de 32.000 entradas (54,1% conferida no status: 31.875+125); nomes de NPCs da ilha das Dríades e do casamento traduzidos; desenhos de atores mantidos em EN; hashes de nomes conferidos por casamento EN->id antes do apply; 4 hashes de nomes com off-by-one corrigidos contra a listagem do lote
- 0065 (500 entradas) - aplicado; marco de 32.500 entradas (55%); nomes de NPCs Orcs/Inquisição/deserto padronizados; Testquestgeber e Testkobold mantidos
- 0066 (500 entradas) - aplicado; marco de 33.000 entradas (56%); dezenas de nomes de NPCs (salteadores, monges, mito de Fausto) traduzidos; blocos TEST: mantidos exatos
- 0067 (500 entradas) - aplicado; marco de 33.500 entradas (56,9%); quase todo o lote sao placeholders TEST: mantidos exatos; NPC nomeados (Thelal, Gahanka, Panton, Buddix) traduzidos
- 0068 (500 entradas) - aplicado; marco de 34.000 entradas (57,7%); nomes de NPCs (refugiados, nômades, casamento de Isadora) traduzidos; placeholders de animacao mantidos
- 0069 (500 entradas) - aplicado; marco de 34.500 entradas (58,5%); NPC nomes de aranhas/culto/Cruzada Impia/Clãs Orc padronizados; AMENDMENT: grupo b do lote 0059 (125 itens) estava faltando e foi aplicado agora; contagem conferida por contagem direta dos JSONL
- 0070 (500 entradas) - aplicado; marco de 35.000 entradas (59,4%); nomes de NPCs (clãs Nur-Trak, trolls da montanha, camarada de comercio) padronizados
- 0071 (500 entradas) - aplicado; marco de 35.500 entradas (60,3%); Cruzada Impia e Sem-Nome padronizados; frase de Four My Sons e incantacoes convertidas
- 0072 (500 entradas) - aplicado; marco de 36.000 entradas (61,1%); creditos reais da equipe mantidos; dialogo do amuleto de joias e sacerdote Sem-Nome traduzidos
- 0073 (500 entradas) - aplicado; marco de 36.500 entradas (62%); negociadores, Guardas do Templo vintage (DX4/PIII) e sacerdotes por divindade padronizados; grupos cd aplicados apos corrigir entradas faltantes (Slave Theodus, Theodore)
- 0074 (500 entradas) - aplicado; marco de 37.000 entradas (62,8%); creditos de Localizacao e Fans de Blind Guardian mantidos; Membros da gangue de Alibaba em serie; grupos cd aplicados apos adicionar entradas genericas faltantes (Portal Cat, Guard, Hare, Inquisitor)
- 0075 (500 entradas) - aplicado; marco de 37.500 entradas (63,7%); Du Rach em serie, T-Energy Creature, vitimas de Kulghar, Old Stag e Brother Fiandral padronizados
- 0076 (500 entradas) - aplicado; marco de 38.000 entradas (64,5%); grupo a estava faltando e foi aplicado depois; ilha de Natal (Fantasmas do Natal, Fadas Sombrias) e criaturas de cristal padronizadas; entradas avulsas (Ice Hydra, Easter Cult Runner, Seraphim Amicia, Gerund, Servant of the Harbinger of Death, Diaanja/Khormynth, Sister Alesia) adicionadas
- 0077 (500 entradas) - aplicado; marco de 38.500 entradas (65,4%); Visao geral de Valores de Combate e chef Poul Brotheuse traduzidos; dialogo do black metal e ferido escavador traduzidos; apóstrofos tipograficos do EN copiados na chave (lookup com canonicalização de apostrofo)
- 0078 (500 entradas) - aplicado; marco de 39.000 entradas (66,2%); Livro 5 Arqueiraria e Livro 4 Modos a Mesa traduzidos; sao de John Lennon e lapide da sogra; grupos b e cd concluidos apos adicionar entradas faltantes (pasto, cisma)
- 0079 (500 entradas) - aplicado; marco de 39.500 entradas (67%); menu do Hearth (Musse au Salive) e rito da Grande Rata traduzidos; artes da Inquisidora em serie padronizadas
- 0080 (500 entradas) - aplicado; marco de 40.000 entradas (67,9%); Livro 2 Magia de Fogo e Livro 6 T-Energia traduzidos na integra; dialogo de fantasmas do fogo (Antonio Bloise) traduzido; grupos b e cd concluidos apos corrigir espaco final e adicionar faltantes
- 0081 (500 entradas) - aplicado; marco de 40.500 entradas (68,7%); Diario da Zumbi na integra; dialogo do agiota e dobrado do Xeque traduzidos
- 0082 (500 entradas) - aplicado; marco de 41.000 entradas (69,6%); Livro 3 Forens traduzido na integra; tutorial do manual em dicas incluido; proprios das lapides de dev em serie
- 0083 (500 entradas) - aplicado; marco de 41.500 entradas (70,5%); converas de namoraco do Xeque e anecdotas de dentista (sotaque) traduzidos; nomes de itens de conjunto em serie padronizados
- 0084 (500 entradas) - aplicado; marco de 42.000 entradas (71,3%); dialogo do Goldman/Jana e grilhoes do Brutus completados apos rejeicoes de protecao; 3 rejeicoes corrigidas com apply --replace
- 0085 (500 entradas) - aplicado; marco de 42.500 entradas (72,1%); apoio da limpeza do acampamento e ritual do Abishai da Discordia traduzidos; guia Súcuba - Criação e Nutrição mantido o livro com aspas tipograficas exatas
- 0086 (500 entradas) - aplicado; marco de 43.000 entradas (73%); dialogo dos fantoches do Octagolamus e ferido de mao do DeMordrey traduzidos; manual de dicas de multijogador em serie traduzido
- 0087 (500 entradas) - aplicado; marco de 43.500 entradas (73,8%); diario do mago (Tyrbor 129) e Livro 1 Culinaria Orc traduzidos na integra; mapa das localizacoes da Diaanja em serie
- 0088 (500 entradas) - aplicado; marco de 44.000 entradas (74,7%); Livro Kuan deus da Guerra e abertura de Gelo e Sangue traduzidos; caso do EN de espaco unico (3234860071) resolvido com regra de espaco espelhado em build_payload/native.py (25 testes OK)
- 0089 (500 entradas) - aplicado; marco de 44.500 entradas (75,5%); conversas de casamento/divorcio e doiscoes de Orcweiser traduzidos; nomes de reputacao (Reputada ate Perseveranca Heroica) em serie
- 0090 (500 entradas) - aplicado; marco de 45.000 entradas (76,4%); carta do faroleiro e dialogo do enxofre da Serafim traduzidos; caso do 50 % (token printf falso) corrigido com por cento
- 0091 (500 entradas) - aplicado; marco de 45.500 entradas (77,2%); dialogo de brigas na taverna e caçadora de fantasmas Retilynen traduzidos; demolido do Demiurgo e ritual do Abishai em serie
- 0092 (500 entradas) - aplicado; marco de 46.000 entradas (78,1%); notas de Kragik (Zumbis Orc) e dialogo do Rumple (facetteleon) traduzidos; diario de trincheira (Dias 9-11) em serie
- 0093 (500 entradas) - aplicado; marco de 46.500 entradas (78,9%); dialogo dos cangaceiros/deserticos e sessao do espirito de Namiel traduzidos; fabrica de chocolate e OF 3.12-4 em serie
- 0094 (500 entradas) - aplicado; marco de 47.000 entradas (79,8%); catalogo grande de criaturas/npcs (Aguia ate Tartaruga Pesada) traduzido; Casa do Segundo Circulo e Demiurgo em serie
- 0095 (500 entradas) - aplicado; marco de 47.500 entradas (80,6%); lote inteiro de catalogo de criaturas/npcs (de Piratas de Pedra-Azul a clãs Orc Nur-Trak/Ore-Thag/Grurag) em uma unica passada
- 0096 (500 entradas) - aplicado; marco de 48.000 entradas (81,5%); A Jogadora Vencedora (manual de tramposo) traduzido na integra; nbsp no fim de Transformers tratado com chave tipografica exata

## Decisões e problemas abertos

- Glossário semente criado com as decisões do briefing (T-Energia, classes,
  deuses, sistemas). Ajustes entram como patches no glossário.
- Confirmar rótulos exatos de "Crystal region" e "The Bloodwood" no corpus
  antes de fixar a tradução (glossário marca para conferir).
- "Testa" (deus da ciência) mantém a grafia EN; colisão com "testa" é aceita
  como nome próprio.

## Próxima etapa

Traduzir batch-0097 (grupos pequenos, apply por payload, commit por lote). POLITICA DE PUSH: commits locais por lote; push unico nos tres remotes somente no final, por ordem de Yuri (2026-10-22).
