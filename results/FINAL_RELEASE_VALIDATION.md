# Validação técnica final do artigo A — v0.9.4

**27 de novembro de 2026 · Manuscrito preliminar em preparação**

## Parecer

**GO técnico para divulgação preliminar da v0.9.4 com o histórico Git atual.** O autor autorizou que seu endereço pessoal fique visível nos metadados dos commits caso o histórico seja divulgado. O endereço consta no campo de autoria dos três commits e no campo de committer de dois.

Os arquivos do pacote foram aprovados nas verificações técnicas descritas abaixo. A revisão matemática independente do manuscrito completo pelo autor permanece pendente, e o manuscrito segue sem revisão por pares. Esta validação foi realizada localmente. O manuscrito permanece em preparação.

## Compilação e verificadores

- O manifesto recebido conferia os 22 arquivos originais. Os logs recebidos registravam 22 páginas no último passe e `TOTAL FAILURES: 0` em cada verificador.
- O PDF foi recompilado após o preenchimento dos metadados, com três passes de pdfLaTeX 1.40.22 e um passe de BibTeX 0.99d no TeX Live 2022. Uma segunda execução em cópia limpa, sem auxiliares, também completou os três passes e produziu o mesmo texto paginado.
- O último passe e o log do BibTeX foram conferidos. A bibliografia tem 17 entradas. No passe final não houve citações ou referências indefinidas, mensagens de rótulos instáveis, caixas `Overfull` ou erros. As referências indefinidas nos passes intermediários da compilação limpa resolveram-se no passe final.
- Permanecem avisos tipográficos de `Underfull \vbox` na saída da p. 4, `Underfull \hbox` na primeira entrada de Kallat na p. 22 e um aviso de expansão de fonte no trecho da bibliografia. A inspeção das duas páginas confirmou texto legível e dentro da área de composição.
- Os dois verificadores são idênticos byte a byte aos da v0.9.3. Executados com Python 3.10.12, em modo isolado e com os parâmetros padrão, ambos terminaram com código 0 e registraram uma única linha `TOTAL FAILURES: 0`. Os logs da execução em cópia limpa coincidiram com os finais, descontados os tempos de execução.

| Verificador | Cobertura finita conferida nos logs |
| --- | --- |
| [`verificar_A2.py`](../code/verificar_A2.py) | Aritmética racional exata, momentos até 26, sistema de razões módulo a décima potência do ideal maximal, raízes módulo 3²⁰, certificado racional, denominadores, diferenças finitas e isometria nas faixas do programa. A configuração fora do padrão testada retornou código 2. |
| [`conferir_kallat_focal_v0_9_1.py`](../code/conferir_kallat_focal_v0_9_1.py) | Expoentes e fator dominante do produto de Euler até índice 600, congruências e identidades truncadas em grau abaixo de 30 e testes exatos de razões e da lei no índice para 11 parâmetros. |

As oito linhas da tabela da §9.1 foram confrontadas com as frações e fatorações do log A2. Os dois vetores numéricos da §9.2 e o valor e a valuação de `W_5(2)` do certificado também coincidem com o log. As execuções verificam os casos finitos implementados.

## Preservação do conteúdo matemático da v0.9.3

Comparei os arquivos históricos na cópia privada local com os arquivos preparados para divulgação. Os arquivos usados como referência coincidiram com a revisão registrada naquela cópia. No LaTeX, comparei o resumo, as definições tipográficas matemáticas e todo o corpo científico até as declarações. Após a remoção dos comentários de trabalho e a normalização de dois trechos de disponibilidade do código na §9, os textos coincidiram integralmente. A comparação cobre definições, enunciados, demonstrações, fórmulas, tabelas, notas matemáticas, conclusão e comandos de citação. As 17 entradas do BibTeX coincidiram integralmente, desconsiderado o comentário de cabeçalho. A alteração final no LaTeX consiste no bloco de metadados do PDF. Esta etapa foi uma comparação de versões.

## Inspeção visual do PDF final

Cada página foi rasterizada em 120 dpi e inspecionada em tamanho de página. As 22 imagens coincidiram byte a byte com as imagens produzidas a partir do PDF recebido pelo mesmo renderizador. A numeração corre de 1 a 22, em A4. Na inspeção das fórmulas foram observados índices, expoentes, frações e alinhamento. Nenhuma página apresentou fórmula cortada, conteúdo sobreposto ou glifo ausente.

| Página | Elementos conferidos |
| --- | --- |
| 1 | Título, autoria, fórmulas do resumo, início do sumário, versão e nota de revisão. |
| 2 | Continuação do sumário, recorrência (1), início do Teorema A e referências cruzadas. |
| 3 | Tabela de classificação do Teorema A, fórmulas do Teorema B e Corolário C. |
| 4 | Citações e notação da discussão de literatura, incluindo o início da comparação com Kallat. |
| 5 | Continuação da comparação, convenções e fórmulas da construção formal. |
| 6 | Primeiros coeficientes e paginação da realização analítica. |
| 7 | Continuação da prova, notação de Hurwitz e fórmulas de partições. |
| 8 | Polinomialidade, recorrência (2), coeficientes (3) e localização. |
| 9 | Desigualdades (4) e fórmulas das leis para primos não excepcionais. |
| 10 | Notação da seção 3-ádica, cumulantes e congruências da forma normal. |
| 11 | Raízes excepcionais, valuação assinada (5) e exemplo de ordem 726. |
| 12 | Recorrências (6) e (7), definições e fórmulas de filtração. |
| 13 | Séries de Bernoulli, continuação das estimativas e resíduos (8). |
| 14 | Comparação com Kallat, referências, produtos, frações e lei no índice. |
| 15 | Conclusão da comparação e alinhamento das três equações do sistema (9). |
| 16 | Identificação na fronteira, redução módulo 3 e início do Teorema 7.4. |
| 17 | Continuação da prova, séries, resíduos e início do Corolário 7.7. |
| 18 | Continuação do corolário, diferenças finitas, fórmulas de Mahler e início do certificado. |
| 19 | Certificado, recorrência (10), valores racionais e Teorema 8.5. |
| 20 | Tabela de ordens compostas, vetores, precisão e pontuação das fórmulas. |
| 21 | Continuação da §9, disponibilidade do código, conclusão e todas as declarações. |
| 22 | As 17 referências numeradas, URLs quebradas entre linhas e afiliação. |

## Declarações, licenças e citação

- **Autoria e IA.** A página de título, as declarações, o README, a nota de proveniência e a citação preferida identificam Patrick E. Scuracchio como único autor. A afiliação é `Independent researcher`. A declaração descreve o uso substancial de IA generativa na pesquisa, no desenvolvimento e na checagem matemática, no código, na literatura e na redação e revisão de todo o manuscrito. A concepção e a direção da pesquisa são atribuídas ao autor. [Proveniência de IA](../docs/AI_PROVENANCE.md)
- **Financiamento e conflitos.** As declarações do autor na p. 21 registram ausência de financiamento específico e de conflitos de interesse. A nota de rosto, a declaração final, o README e a proveniência são coerentes sobre a revisão humana incompleta e o estado preliminar.
- **Licenças.** A aprovação autoral da divisão está registrada na documentação de licenciamento e no histórico. CC BY 4.0 cobre o manuscrito em LaTeX e PDF e a documentação original, incluindo as porções licenciáveis da bibliografia e das saídas. MIT cobre os verificadores e o código de compilação. O aviso CC BY aponta para o texto legal oficial e registra atribuição e escopo. O arquivo MIT contém o texto de concessão, a exigência de retenção do aviso e a cláusula de garantia do texto padrão. A documentação preserva os direitos de terceiros e limita a concessão aos direitos do licenciante. [Escopo local](../LICENSE.md) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode.en) · [MIT](https://opensource.org/license/mit)
- **CFF.** O campo raiz `type: article` do arquivo recebido não satisfazia o esquema CFF 1.2.0. O arquivo final passou em validação JSON Schema Draft 7 com checagem de formatos após a leitura do YAML. A raiz descreve o código MIT como `software`. A citação preferida descreve o manuscrito como `unpublished`, com título, autor, afiliação, versão 0.9.4 e CC BY 4.0. O arquivo não atribui DOI ou data de publicação. [CITATION.cff](../CITATION.cff) · [Esquema oficial CFF 1.2.0](https://raw.githubusercontent.com/citation-file-format/citation-file-format/1.2.0/schema.json)

## Links e metadados

- Os links relativos da documentação do pacote foram resolvidos localmente. No PDF, a leitura estrutural encontrou 148 destinos nomeados, 253 anotações de links internos e 38 marcadores de navegação. Os destinos levam a páginas válidas. A paginação do sumário e das seções de declarações e referências foi conferida com os marcadores e com a inspeção visual.
- As sete anotações externas do PDF correspondem a quatro URIs HTTPS, incluindo segmentos de URLs que quebram entre linhas. Conferi os destinos como registrados no PDF. A disponibilidade externa das referências bibliográficas e do repositório está fora da validação de links internos.
- O PDF final tem título completo, autor, assunto com a versão 0.9.4 e o estado preliminar, cinco palavras-chave e idioma `en`. A data de criação e de modificação registradas são da compilação local. As fontes têm subconjuntos incorporados e mapeamento Unicode. O arquivo está sem criptografia, anexos, formulários e JavaScript.

## Histórico Git, privacidade e material de terceiros

- Conferi todos os três commits locais, `bae79d1`, `5755e9b` e `2e21be8`, incluindo metadados, mensagens, caminhos, alterações e os 26 blobs únicos alcançáveis por branches e referências remotas locais. A inspeção também abrangeu os reflogs, a árvore auxiliar de captura local e seus cinco blobs adicionais, entre eles o PDF e os logs recebidos. O inventário total inspecionado foi de 31 blobs, 15 árvores e três commits. `git fsck --full --strict` passou.
- A busca nos arquivos e metadados incluiu padrões de chaves, tokens, senhas, URLs autenticadas, caminhos pessoais e identificadores privados. Não identifiquei credenciais nem exposição indevida de dados pessoais nos conteúdos destinados à divulgação. A autorização do autor cobre o e-mail nos metadados dos commits. A configuração local do remoto usa transporte SSH e um alias de host e fica na configuração do clone.
- Examinei o log de compilação recebido, o log recompilado, os logs dos verificadores e os logs auxiliares de pdfLaTeX e BibTeX. O log de compilação contém caminhos absolutos genéricos da instalação do TeX no sistema. Os logs examinados não revelaram diretório pessoal, caminho privado do projeto ou credencial. O texto, os metadados e as anotações de link dos PDFs também foram examinados.
- O inventário do histórico e do pacote não revelou anexos privados, arquivos de terceiros redistribuídos como fontes do projeto ou PDFs de referência. As referências aparecem como citações e dados bibliográficos. Os verificadores usam a biblioteca padrão do Python. O PDF incorpora subconjuntos tipográficos da instalação TeX, incluindo Latin Modern, AMSFonts e RSFS. Esses componentes conservam seus termos próprios. [RSFS e condições da versão Type 1](https://ctan.org/tex-archive/fonts/rsfs/type1)

## Artefatos finais e integridade

Os READMEs e o CHANGELOG registram as verificações concluídas e o estado preliminar. O script tem um modo de geração exclusiva do manifesto para registrar o relatório sem alterar o PDF e os logs já inspecionados. Os quatro artefatos diretamente inspecionados nesta execução têm os seguintes SHA-256.

```text
8ff43e1a7fd19dcf9a77a11397171cf5b0a89edbb513e44989c0c43b628aad6e  paper/manuscript_A.pdf
e19cb602a88c6db0691836ae8adde704106972fa9046a47bfd2150c130d6a05f  results/compilation.log
cbbe42fbfe76f192f955809692bd74d776ab7f6b84d3f0ee1608d752403c2021  results/verificar_A2.log
4d4f0ff13d3e171accd11b24296380c20b7b428b8646b041a198634d56278bde  results/conferir_kallat_focal_v0_9_1.log
```

O manifesto final cobre os 23 arquivos do pacote, incluindo este relatório. Exclui o próprio manifesto, o diretório Git e os auxiliares de compilação. A conferência final foi feita da raiz com `sha256sum --strict -c results/SHA256SUMS`. [Manifesto SHA-256](SHA256SUMS)
