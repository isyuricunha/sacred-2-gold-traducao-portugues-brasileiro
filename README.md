# Sacred 2 Gold — Tradução para português brasileiro

Projeto de tradução dos textos de **Sacred 2 Gold / Ice & Blood** para PT-BR,
usando os recursos do idioma inglês (`en_UK`). As vozes permanecem originais.

**Tradução textual concluída:** 58.913 entradas traduzidas e validadas, com
nove arquivos nativos gerados. O teste inicial dos menus carregou no jogo e
exibiu corretamente “Opções”; ainda é necessária a validação completa em jogo
pelo mantenedor.

## Download

As versões completas são publicadas automaticamente em
[GitHub Releases](https://github.com/isyuricunha/sacred-2-gold-traducao-portugues-brasileiro/releases/latest).
Baixe o arquivo **PTBR.zip** diretamente na seção *Assets* da versão mais recente.
A primeira publicação recebe a versão **v1.0.0**; cada nova alteração validada
nos arquivos PTBR gera a versão de correção seguinte (**v1.0.1**, **v1.0.2** etc.),
com changelog contendo alterações efetivas desde a Release anterior.

O GitHub Actions também mantém o artefato de workflow `traducao-ptbr`, mas o
arquivo público recomendado para instalação é o `PTBR.zip` da **Release**.
Uma alteração apenas nos documentos ou nos lotes de trabalho não cria Release;
o novo pacote é publicado somente após um build completo que altere PTBR/.

## Instalação

1. Feche o jogo e faça backup da pasta `locale/en_UK` da sua instalação.
2. Extraia **PTBR.zip** em uma pasta temporária. A raiz do ZIP terá `locale/`.
3. Copie **todo o conteúdo extraído** para a raiz do Sacred 2 Gold, a pasta que
   contém `system/`, `pak/` e `locale/`. Mescle as pastas e substitua os arquivos
   de idioma correspondentes. Não crie uma pasta `PTBR` dentro do jogo.
4. Use o idioma inglês que carrega `locale/en_UK`. O teste foi realizado nessa
   configuração, sem cadastrar um novo idioma no jogo.

O pacote substitui `locale/en_UK/global.res` e oito arquivos CSV dessa mesma
pasta. Para atualizar, feche o jogo e repita a cópia com um pacote compatível,
mantendo o backup inglês original. Para desinstalar, restaure os nove arquivos
do backup; não apague toda a pasta de idioma, que também contém áudio e fontes.

## Compatibilidade

A base analisada usa L10C versão 258; a tela do jogo testado informa
`v2.65.2 build 1837`. Existem mods na instalação analisada, mas sua presença
não comprova quais estavam ativos. A origem exata dessa base em relação a
patches ainda precisa ser confirmada. O projeto trabalha com **uma única base
inglesa**; não promete compatibilidade com Remaster, outras versões ou mods
que também substituam os arquivos de idioma. Instale a tradução apenas sobre
a base compatível e preserve seus backups.

## Projeto e apoio

Site: [traducao.yuricunha.com](https://traducao.yuricunha.com/).

Se quiser apoiar voluntariamente o projeto, a chave PIX é **pix@yuricunha.com**.

Mantido por [Yuri Cunha](https://github.com/isyuricunha). Sacred 2 e seus recursos
pertencem aos respectivos titulares. Não há licença própria definida para o
projeto neste momento.

Para trabalhar na tradução, veja o [guia interno](translation-work/README.md).
