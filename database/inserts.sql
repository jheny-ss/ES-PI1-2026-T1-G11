/**
 ============================================================
 INSERTS: ELEITORES
 ============================================================
*/

INSERT INTO eleitores (cpf, nome, titulo_eleitor, chave_acesso, status_votacao, status_mesario)
VALUES
('12345678901', 'Arthur Senna', '1111111111', 'AS1234', FALSE, TRUE),
('98765432100', 'Maria Silva', '2222222222', 'MS5678', FALSE, FALSE),
('45678912300', 'João Oliveira', '3333333333', 'JO9012', FALSE, FALSE),
('32165498700', 'Ana Souza', '4444444444', 'AS3456', FALSE, FALSE),
('15975348620', 'Carlos Pereira', '5555555555', 'CP7890', FALSE, FALSE);

/**
 ============================================================
 INSERTS: CANDIDATOS
 ============================================================
*/

INSERT INTO candidatos (nome, numero_de_votacao, partido)
VALUES
('Carlos Andrade', 10, 'Partido A'),
('Fernanda Lima', 20, 'Partido B'),
('Ricardo Gomes', 30, 'Partido C'),
('Juliana Rocha', 40, 'Partido D');


