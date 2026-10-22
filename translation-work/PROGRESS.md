# Progresso — Sacred 2 Gold PT-BR

Registro vivo da Ella. Atualizar a cada checkpoint validado. O estado técnico
de verdade é `python translation-work/toolkit.py status`; este arquivo guarda
decisões, problemas e a próxima etapa.

## Estado

- Geração: 52ac93bbf34f8812a15ea2a3025c5e07c06f4cd7724b114ca6c49539f1c79fdd
- Corpus: 58.913 entradas, 118 lotes (RES 57.989 + CSVs 924)
- Traduzido: 2.000/58.913
- Última etapa concluída: leitura dos docs; diretrizes e glossário iniciais

## Lotes concluídos

- 0001 (500 entradas) - 4 payloads aplicados sem rejeicoes apos fix de anotacoes <...> protegidas
- 0002 (500 entradas) - 1 rejeicao: "5% do" criou token falso % d; fix "5 por cento do". Termos novos no glossario pendentes de patch: flores-de-anel, bateda (drive), Gargantopode, aspectos Piromante Absoluto/Tecnologia Venerada/Supremacia Astuta/Submundo Nefasto
- 0003 (500 entradas) - aplicado sem rejeicoes; textos em alemao (122143345) e TODO/TEST mantidos como no EN
- 0004 (500 entradas) - aplicado sem rejeicoes; termos novos pendentes de patch no glossario: erutraia, Tempestino Mistico, aspectos/mods do Inquisidor e Guardiao do Templo

## Decisões e problemas abertos

- Glossário semente criado com as decisões do briefing (T-Energia, classes,
  deuses, sistemas). Ajustes entram como patches no glossário.
- Confirmar rótulos exatos de "Crystal region" e "The Bloodwood" no corpus
  antes de fixar a tradução (glossário marca para conferir).
- "Testa" (deus da ciência) mantém a grafia EN; colisão com "testa" é aceita
  como nome próprio.

## Próxima etapa

Traduzir batch-0005 (grupos pequenos, apply por payload, checkpoint por lote).
