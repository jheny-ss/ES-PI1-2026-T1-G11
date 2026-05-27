INSERT INTO eleitores
(nome, titulo_eleitor, cpf, chave_acesso, status_votacao, status_mesario)
VALUES

(
    'Carlos José',
    'ZSVMOAIZHYOC', -- 674724100108
    'L6N7PBTK1UN5',
    'EGKLYOL2', -- CAJ2824
    FALSE,
    TRUE
),

(
    'Jhenyfer Souza',
    'WOXQN83ZHYOC', -- 484923790108
    'WO3YPDWK1UDQ',
    'ZF1AO8VH', -- JHS1409
    FALSE,
    TRUE
),

(
    'Maria Aparecida',
    'RGTGRFK4HYOC', -- 276135040108
    'YOQDUHJ11UN5',
    'YA50QBP8', -- MAA5506
    FALSE,
    FALSE
),

(
    'Leticia Dias',
    'ZS1U2XHYHYOC', -- 678578010108
    'UJQETHVJ2WTE',
    '0FB9HYHW', -- LED5012
    FALSE,
    FALSE
),

(
    'Carla Dias',
    'SF0URFZRHYO9', -- 526835750132
    'XOUISEJ2ZQN5',
    'EGA7XORB', -- CAD4657
    FALSE,
    FALSE
),

(
    'Daiana Souza',
    'HYL5QBVJHYZR', -- 011350710175
    '3ZYNK2YNK4L2',
    'GJ3ESIP8', -- DAS3286
    FALSE,
    FALSE
),

(
    'Edson Silva',
    'O840XPQCHYOC', -- 408857420108
    'SG0SO9K4HYJZ',
    'LS2CZSVH', -- EDS2679
    FALSE,
    FALSE
);
-- ============================================================
-- INSERTS CANDIDATOS
-- ============================================================

INSERT INTO candidatos
(nome, numero_de_votacao, partido)
VALUES
('Helena Vargas', 20, 'PDS'),
('Valerius Kroeger', 30, 'ORDEM'),
('Aléxia Thorne', 60, 'VANGUARDA'),
('Odorico Neto', 50, 'PPU');