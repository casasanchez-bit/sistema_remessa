# CLAUDE.md — Sistema Casa Sanchez (Controle de Remessa e Terceirização)

## Stack e Ambiente

- **Backend:** Python/Flask + SQLite3 (`controle_remessa.db`)
- **Frontend:** Jinja2 templates + CSS/JS inline (sem framework JS)
- **Produção:** PythonAnywhere — `/home/casasanchez/controle-remessa-terceirizacao/`
- **Deploy:** `git push` (local) → `git pull` (PythonAnywhere bash) → **Reload** na aba Web
- **Repositório:** github.com/casasanchez-bit/sistema_remessa (branch `main`)

## Fluxo de Deploy (sempre este, nunca outro)

1. Editar arquivos localmente
2. `git add` + `git commit` + `git push`
3. No PythonAnywhere: console Bash → `cd controle-remessa-terceirizacao && git pull`
4. Aba **Web** → botão **Reload**
5. F5 no navegador (ou Ctrl+Shift+R se mudou CSS/JS)

**NUNCA fazer upload manual de fotos pelo Git** — as fotos (`static/fotos_*`) existem só no PythonAnywhere. Commitar fotos vai sobrescrever dados reais.

---

## Arquitetura Crítica — Leia Antes de Tocar no Código

### Plano de Corte (`planos_corte`)

O schema passou por duas gerações. Há colunas legadas que coexistem com as novas:

| Coluna legada (TEXT) | Coluna nova (FK) | Situação |
|---|---|---|
| `fornecedor1`, `fornecedor2`, `fornecedor3` | `fornecedor1_id` … `fornecedor5_id` | Legado tem nomes concatenados; novo tem IDs para tabela `fornecedores` |

**Regra:** A query que carrega `plano` em `produto_plano_corte` **deve** fazer LEFT JOIN nas 5 colunas FK e expor os nomes como `forn1_label` a `forn5_label` com COALESCE para fallback no legado. Ver rota `produto_plano_corte` em `app.py`.

### Produtos Frente/Fundo (`tem_frente_fundo = 1`)

Produtos como almofadas com frente e fundo de tamanhos diferentes (ex: produtos 145, 146).

- `largura_corte_cm` e `comprimento_corte_cm` são **NULL** — isso é intencional
- As medidas reais estão em: `largura_frente_cm`, `comprimento_frente_cm`, `largura_fundo_cm`, `comprimento_fundo_cm`, `largura_fundo_menor_cm`, `comprimento_fundo_menor_cm`
- O canvas (`desenharDiagrama`) tem branch separado para este modo — **nunca usar `lc`/`cc` como guarda no early-exit** para esses produtos

### Canvas de Diagrama de Corte

Dois canvas no `produto_plano_corte.html`:
- `#cvDiagrama` — visualização principal (tela + imprimir completo)
- `#cvDiagramaSimples` — impressão simples (botão "Imprimir Desenho")

Ambos chamam a mesma função `desenharDiagrama(cv, W, H, ...)` definida no primeiro `<script>`. O segundo `<script>` tem só um wrapper fino `desenharDiagramaSimples()`.

---

## Regras de Desenvolvimento (aprendidas na prática)

### 1. Campo novo = cobertura completa
Todo campo novo deve ser implementado em **todos** os pontos de uso na mesma entrega:
- Formulário de criação
- Formulário de edição
- Visualização (tela)
- Impressão (completo + simples)
- Exportação/planilha (`gerar_planilha_importacao.py`)

### 2. Mudança de schema = atualizar template E query
Quando uma coluna nova é adicionada ao banco:
- Atualizar a query SQL que carrega o objeto no Flask
- Atualizar o template Jinja2 que exibe os dados
- Atualizar `gerar_planilha_importacao.py` se for campo exportável

### 3. Jinja2: nunca formatar NULL diretamente
`{{ '%.3f'|format(valor) }}` quebra com `TypeError` se `valor` for NULL.
Sempre usar: `{{ '%.3f'|format(valor or 0) }}`

### 4. Canvas: testar com produto normal E produto frente/fundo
Após qualquer alteração no canvas ou na função `desenharDiagrama`:
- Testar com produto **normal** (ex: produto com largura_corte_cm preenchida)
- Testar com produto **frente/fundo** (ex: produtos 145 ou 146 — CP ALMOF NAPOLI)
- Verificar que o diagrama aparece nos dois modos (tela e impressão)

---

## Checklist Pós-Alteração

Antes de dar a tarefa como concluída, verificar:

- [ ] `git push` feito e confirmado no terminal
- [ ] `git pull` feito no PythonAnywhere
- [ ] **Reload** feito na aba Web do PythonAnywhere
- [ ] Página testada no navegador (F5 ou Ctrl+Shift+R)
- [ ] Se mudou canvas: testar produto normal + produto frente/fundo
- [ ] Se mudou schema: verificar que query, template e planilha foram atualizados
- [ ] Se mudou impressão: abrir modal de impressão e conferir layout

---

## Armadilhas Conhecidas (já quebraram uma vez)

| Armadilha | O que aconteceu | Como evitar |
|---|---|---|
| Early-exit do canvas com `!lc` | Canvas ficou em branco para produtos frente/fundo porque `largura_corte_cm = NULL` | Usar `isFrFnd` para branch separado antes do early-exit |
| Template lendo `fornecedor1` (TEXT legado) | Todos os fornecedores apareciam concatenados no campo 1 | Query sempre com LEFT JOIN nos 5 IDs FK |
| `format()` com NULL no Jinja2 | Erro 500 em quantidade de matéria-prima NULL | Sempre usar `or 0` como guard |
| IIFE deixada no arquivo após edição parcial | Código duplicado causando comportamento imprevisível | Ao substituir funções JS grandes, verificar que o bloco antigo foi removido por completo |
| Foto cadastrada localmente mas não no servidor | Imagem quebrada em produção | Fotos só existem no PythonAnywhere — nunca commitar arquivos de `static/fotos_*` |

---

## Segurança (obrigatório antes de publicar na internet)

- [ ] `SECRET_KEY` configurada com valor seguro (não hardcoded)
- [ ] CSRF protection implementada em todos os formulários POST
- [ ] Variáveis de ambiente para credenciais sensíveis

---

## Produtos de Referência para Testes

| ID | Código | Descrição | Tipo |
|---|---|---|---|
| 145 | 12678 | CP ALMOF NAPOLI 40X40CM | Frente/Fundo |
| 146 | — | Similar ao 145 | Frente/Fundo |
| Qualquer outro | — | — | Normal (largura_corte_cm preenchida) |
