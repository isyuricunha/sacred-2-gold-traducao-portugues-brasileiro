# Sacred 2 Gold — Tradução para português brasileiro

Projeto de tradução dos textos de **Sacred 2 Gold / Ice & Blood** para PT-BR,
usando os recursos do idioma inglês (`en_UK`). As vozes permanecem originais.

**Em preparação: a tradução completa ainda não está disponível.** O teste inicial
dos menus carregou no jogo e exibiu corretamente “Opções”. Isso não equivale à
revisão de todos os textos ou à compatibilidade com todas as edições.

## Download

Ainda não há pacote publicado. Quando um build completo for enviado ao projeto,
o pacote estará nos artefatos de uma execução bem-sucedida de
[Empacotar PTBR](https://github.com/isyuricunha/sacred-2-gold-traducao-portugues-brasileiro/actions/workflows/release.yml).
Abra a execução, baixe `traducao-ptbr` e extraia o `PTBR.zip` contido nesse download.
Não instale os arquivos de trabalho do repositório.

## Instalação do futuro pacote

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
