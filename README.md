# Controle de Remessa e Retorno — Terceirização da Produção

Sistema local (Flask + SQLite) para controlar remessas enviadas a terceirizados (costura de capas de almofada e outros itens) e os retornos da produção, com saldo pendente por terceirizado e fechamento mensal para pagamento.

## Como rodar

1. Abra o PowerShell nesta pasta.
2. Crie o ambiente virtual (só na primeira vez):
   ```
   python -m venv venv
   .\venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
3. Inicie o sistema:
   ```
   .\venv\Scripts\python.exe app.py
   ```
4. Abra o navegador em **http://127.0.0.1:5000**

O banco de dados (`controle_remessa.db`) é criado automaticamente na primeira execução. Para fazer backup, basta copiar esse arquivo.

## Cadastros

- **Terceirizados** (Prestadores de Serviço): código gerado automaticamente pelo sistema (bloqueado), nome e telefone.
- **Produtos**: código digitado pelo usuário (o mesmo já usado no ERP) e descrição.
- **Cores/Estampas**: cadastro independente de Produto, com código gerado automaticamente.
- **Serviços**: código automático, vinculado (atribuído) a um Produto, com descrição e valor em R$. O preço do serviço é o mesmo independente da cor/estampa.

Todos os cadastros têm botões **Visualizar**, **Editar** e **Excluir** (exclusão é bloqueada se o registro já estiver em uso em alguma remessa).

## Fluxo de uso

1. **Remessas**: escolha Terceirizado e Data, depois adicione um ou mais itens (Produto + Cor/Estampa + Serviço + Quantidade) na mesma remessa — gera um número sequencial automático para o cabeçalho. A lista de serviços de cada item é filtrada automaticamente pelos atribuídos ao Produto escolhido naquela linha. Cada item tem seu próprio saldo e status (Pendente/Parcial/Concluída), com botões individuais de Visualizar/Editar/Excluir.
2. **Retornos**: ao chegar o talão físico preenchido pelo terceirizado, lance o retorno no sistema referenciando os itens de remessa indicados no talão. Um único retorno pode trazer itens de remessas diferentes, mas só aparecem terceirizados com saldo pendente. O sistema valida que a quantidade não exceda o saldo do item, dá baixa automática e marca o item como concluído quando o total enviado é igualado.
3. **Dashboard**: acompanhe o saldo pendente (enviado − retornado) por terceirizado.
4. **Fechamento Mensal**: filtre por mês e veja o total a pagar por terceirizado/produto/cor/serviço, com base nas quantidades retornadas (baixas) no período.
