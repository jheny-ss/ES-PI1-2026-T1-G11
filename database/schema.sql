/*
  BANCO DE DADOS: SISTEMA DE VOTAÇÃO

  Descrição:
  Banco responsável por gerenciar eleitores, candidatos e votos.
  Garante integridade dos dados, controle de votação única
  e rastreabilidade das operações.
 */

CREATE DATABASE sistema_de_votacao;
USE sistema_de_votacao;


/**
  TABELA: eleitores

  Descrição:
  Armazena os dados dos eleitores do sistema.
  Cada eleitor pode votar apenas uma vez.
 */
 
CREATE TABLE eleitores (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    nome            VARCHAR(100) NOT NULL,
    titulo_eleitor  VARCHAR(20)  NOT NULL UNIQUE,
    cpf             VARCHAR(100) NOT NULL UNIQUE,        -- criptografado com Cifra de Hill 
    chave_acesso    VARCHAR(100) NOT NULL UNIQUE,        -- criptografado com Cifra de Hill 
    status_votacao  BOOLEAN NOT NULL DEFAULT FALSE,      -- FALSE = não votou, TRUE = já votou
    status_mesario  BOOLEAN NOT NULL DEFAULT FALSE,      -- FALSE = eleitor comum, TRUE = mesário
    data_hora_voto  DATETIME NULL DEFAULT NULL           -- preenchido no momento do voto 
);

/**
 ============================================================
 TABELA: candidatos
 ============================================================
 Armazena os candidatos disponíveis para votação.
 */
CREATE TABLE candidatos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    numero_de_votacao INT NOT NULL UNIQUE,
    partido VARCHAR(100) NOT NULL
);


/**
 ============================================================
 TABELA: votacao
 ============================================================
 Registra os votos realizados pelos eleitores.
 Cada eleitor pode votar apenas uma vez.
 */
CREATE TABLE votacao (
    id                      INT AUTO_INCREMENT PRIMARY KEY,
    protocolo_criptografado VARCHAR(100) NOT NULL UNIQUE, -- comprovante embaralhado
    id_candidato            INT NULL, -- NULL significa voto nulo
    data_voto               DATE NOT NULL DEFAULT (CURRENT_DATE), -- sem hora para evitar rastreamento, preservando ao max o anonimato

    FOREIGN KEY (id_candidato)
        REFERENCES candidatos(id)
        ON DELETE SET NULL -- candidato removido vira voto nulo, não perde o registro
);

