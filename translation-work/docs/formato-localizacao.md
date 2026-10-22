# Formato e limites técnicos

## Recursos gerenciados

`locale/en_UK/global.res`: L10C versão 258, little-endian. Cabeçalho de 16 bytes,
lista de hashes uint32, descritores (hash, offset de bits, comprimento em unidades
UTF-16), número de nós Huffman, nós de 8 bytes e fluxo de bits LSB-first. O hash
nativo é o ID, combinado com o caminho do recurso; a posição não define identidade.
Há 140.326 hashes de referência e 57.989 pares hash/texto na fonte inicial.
Não se tenta inventar nomes simbólicos a partir de hashes.

O original tem bytes opacos nos campos de alinhamento e filhos das folhas.
O codec da comunidade os ignora e o teste anterior no jogo aceitou sua normalização.
O parser próprio respeita filhos apenas em nós internos. Reconstrução sem alteração
de texto retorna os bytes originais integralmente. Com tradução, a árvore é refeita
deterministicamente: offsets e bytes de compressão podem mudar; hashes, ordem,
unidades Unicode e conteúdo são conferidos. Os bytes originais permanecem no
snapshot. O novo encoder Python tem teste de equivalência real; seu output
traduzido ainda precisa de um teste de runtime por Yuri.

Referência técnica inspecionada (sem dependência de runtime):
[sacred2-global-res-codec](https://github.com/sacred2-compendium/sacred2-global-res-codec),
commit `e23108d5adb9ae51d405975893ec2b6b7d52217a`, licença MIT.
Implementação local em Python, sem instalação de pacotes ou acesso à rede.

CSV nativo separado por `;`, sem quoting: AppendBonus, AppendMaterial,
AppendRare, DescriptionBonus, DescriptionMaterial, DescriptionRare, Itemnames
e Optional. Fontes são ASCII, saída usa Windows-1252 estrito; os acentos PT-BR
cabem nessa codificação. Linhas vazias, CRLF, células vazias, `hasGender=false`,
ordem e sufixos numéricos `,1` de Itemnames são mantidos. Optional está vazio e
continua como recurso nativo vazio. IDs: caminho + chave nativa da linha + slot
da alternativa. Duas linhas preenchidas com a mesma chave são rejeitadas.
O original AppendBonus repete NAME_BON_RESISTANCE numa linha totalmente vazia:
essa linha não é uma unidade textual, é preservada como estrutura.

Slots de alternativas não têm IDs nativos individuais. Reordenação/inserção dentro
da mesma linha pode mudar o sentido contextual de slots: o diff apresenta alterações
por slot e requer revisão; não há correspondência aproximada ou reaproveitamento
por texto. Reordenar linhas de chaves distintas preserva identidade. Arquivos novos
ou removidos são recusados até extensão explícita do perfil, evitando interpretar
cópias incompletas como exclusões. Versões RES desconhecidas também são recusadas.

## Sintaxe e contexto

Preservar tags e sua ordem, como `<br>`, `<b>`, `<AlignH Value=Center/>` e
`<$ID_CUI_...>`, formatos `%{###,###}1`, parâmetros `%1`, `%d` e URLs. A toolkit
valida multiplicidade e ordem de tags e de printf não posicionais. O original
possui markup legado desequilibrado; não se exige balanceamento inexistente nem
se corrige o inglês automaticamente. Anotações desconhecidas entre `<...>` são
preservadas conservadoramente; decidir se são texto visível requer investigação.

CSV é usado por NameGen.dll e NameGenConfig.txt para montar nomes por partes.
Esses arquivos de lógica não são traduzidos nem substituídos. `hasGender=false`
e sufixos permanecem; validação técnica não garante concordância de gênero,
número ou preposições. Ella deve revisar combinações e registrar limitações,
sem alterar gameplay ou o gerador como solução improvisada.

As fontes listadas em ListFontGroups.xml são ZabriskieScript-Bold e AntiquaSSK.
Ambas contêm os caracteres PT-BR verificados na etapa anterior. A captura de Yuri
confirmou o carregamento de uma amostra feita pelo codec JavaScript e os glifos
de “Opções”. Não é uma comprovação de todos os menus nem de todos os builds.

Fora do escopo: áudio, vídeos, PDF, créditos, código Lua, IDs técnicos e comentários
de scripts. A toolkit não afirma traduzir textos desenhados em imagens nem
textos eventualmente embutidos fora dos nove recursos conhecidos.
