PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS terceirizados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    nome TEXT NOT NULL UNIQUE,
    telefone TEXT
);

CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    descricao TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cores_estampas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    produto_id INTEGER NOT NULL REFERENCES produtos(id),
    descricao TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS servicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    produto_id INTEGER NOT NULL REFERENCES produtos(id),
    descricao TEXT NOT NULL,
    valor REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS remessas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero INTEGER NOT NULL UNIQUE,
    terceirizado_id INTEGER NOT NULL REFERENCES terceirizados(id),
    data_envio TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS itens_remessa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    remessa_id INTEGER NOT NULL REFERENCES remessas(id),
    produto_id INTEGER NOT NULL REFERENCES produtos(id),
    cor_estampa_id INTEGER NOT NULL REFERENCES cores_estampas(id),
    servico_id INTEGER NOT NULL REFERENCES servicos(id),
    qtd_enviada INTEGER NOT NULL,
    finalizada INTEGER NOT NULL DEFAULT 0,
    prioridade INTEGER
);

CREATE TABLE IF NOT EXISTS retornos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero INTEGER NOT NULL UNIQUE,
    terceirizado_id INTEGER NOT NULL REFERENCES terceirizados(id),
    data_retorno TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS itens_retorno (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    retorno_id INTEGER NOT NULL REFERENCES retornos(id),
    item_remessa_id INTEGER NOT NULL REFERENCES itens_remessa(id),
    qtd_retornada INTEGER NOT NULL,
    finalizado INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS pagamentos_fechamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    terceirizado_id INTEGER NOT NULL REFERENCES terceirizados(id),
    mes TEXT NOT NULL,
    data_pagamento TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pagamentos_fechamento_retornos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pagamento_id INTEGER NOT NULL REFERENCES pagamentos_fechamento(id),
    retorno_id INTEGER NOT NULL REFERENCES retornos(id),
    UNIQUE(pagamento_id, retorno_id)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    criado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS materias_primas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    descricao TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produto_composicao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL REFERENCES produtos(id),
    materia_prima_id INTEGER NOT NULL REFERENCES materias_primas(id),
    quantidade REAL NOT NULL,
    UNIQUE(produto_id, materia_prima_id)
);

CREATE TABLE IF NOT EXISTS planos_corte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL UNIQUE REFERENCES produtos(id),
    tipo_tecido TEXT,
    fornecedores TEXT,
    largura_tecido REAL,
    comprimento_enfesto REAL,
    num_camadas INTEGER,
    pecas_por_enfesto INTEGER,
    aproveitamento REAL,
    observacoes TEXT
);
