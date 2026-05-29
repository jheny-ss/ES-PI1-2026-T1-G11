INSERT INTO eleitores
(nome, titulo_eleitor, cpf, chave_acesso, status_votacao, status_mesario)
VALUES

(
    'Carlos José',
    'ZSVMOAIZHYOC', 
    'L6N7PBTK1UN5',
    'EGKLYOL2', 
    FALSE,
    TRUE
),

(
    'Jhenyfer Souza',
    'WOXQN83ZHYOC', 
    'WO3YPDWK1UDQ',
    'ZF1AO8VH', 
    FALSE,
    TRUE
),

(
    'Maria Aparecida',
    'RGTGRFK4HYOC', 
    'YOQDUHJ11UN5',
    'YA50QBP8', 
    FALSE,
    FALSE
),

(
    'Leticia Dias',
    'ZS1U2XHYHYOC',
    'UJQETHVJ2WTE',
    '0FB9HYHW', 
    FALSE,
    FALSE
),

(
    'Carla Dias',
    'SF0URFZRHYO9', 
    'XOUISEJ2ZQN5',
    'EGA7XORB', 
    FALSE,
    FALSE
),

(
    'Daiana Souza',
    'HYL5QBVJHYZR', 
    '3ZYNK2YNK4L2',
    'GJ3ESIP8', 
    FALSE,
    FALSE
),

(
    'Edson Silva',
    'O840XPQCHYOC', 
    'SG0SO9K4HYJZ',
    'LS2CZSVH', 
    FALSE,
    FALSE
);


INSERT INTO candidatos
(nome, numero_de_votacao, partido)
VALUES
('Helena Vargas', 20, 'PDS'),
('Valerius Kroeger', 30, 'ORDEM'),
('Aléxia Thorne', 60, 'VANGUARDA'),
('Odorico Neto', 50, 'PPU');