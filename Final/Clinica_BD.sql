


-- Universidade Federal de Santa
-- Engenhraia De Computação
-- Projeto final de Banco de Dados- Clinica Médica
-- Integrantes: Balduino, Andre e Maoisês


CREATE DATABASE clinica;
USE clinica;

CREATE TABLE Funcionario (
    id_funcionario INT AUTO_INCREMENT PRIMARY KEY,
    nome_funcionario VARCHAR(100) NOT NULL,
    data_admissao DATE,
    cargo VARCHAR(50),
    cpf VARCHAR(14),
    telefone VARCHAR(20),
    email VARCHAR(100)
) ENGINE=InnoDB;

CREATE TABLE Doenca (
    id_doenca INT AUTO_INCREMENT PRIMARY KEY,
    nome_doenca VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Especialidade (
    id_especialidade INT AUTO_INCREMENT PRIMARY KEY,
    nome_especialidade VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Medico (
    id_medico_crm VARCHAR(20) PRIMARY KEY,
    nome_medico VARCHAR(100) NOT NULL,
    telefone VARCHAR(20)
) ENGINE=InnoDB;

CREATE TABLE Convenio (
    id_convenio INT AUTO_INCREMENT PRIMARY KEY,
    nome_convenio VARCHAR(100) NOT NULL,
    cobertura VARCHAR(200),
    tipo_convenio VARCHAR(50)
) ENGINE=InnoDB;

CREATE TABLE Clinica_Parceira (
    id_clinica INT AUTO_INCREMENT PRIMARY KEY,
    nome_clinica VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Equipamento (
    id_equipamento INT AUTO_INCREMENT PRIMARY KEY,
    nome_equipamento VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Tipo_Exame (
    id_exame INT AUTO_INCREMENT PRIMARY KEY,
    nome_exame VARCHAR(100) NOT NULL,
    resultado_exame VARCHAR(255)
) ENGINE=InnoDB;

CREATE TABLE Medicamento (
    id_medicamento INT AUTO_INCREMENT PRIMARY KEY,
    nome_medicamento VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Paciente (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    data_nascimento DATE,
    telefone VARCHAR(20),
    email VARCHAR(100),
    cpf VARCHAR(14),
    endereco VARCHAR(200),
    id_func_atendimento INT,
    FOREIGN KEY (id_func_atendimento) REFERENCES Funcionario(id_funcionario)
) ENGINE=InnoDB;

CREATE TABLE Consulta (
    id_consulta INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_medico_crm VARCHAR(20) NOT NULL,
    id_func_registro INT NOT NULL,
    id_convenio INT,
    data_consulta DATE NOT NULL,
    valor DECIMAL(10,2),
    observacao VARCHAR(255),

    FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente),
    FOREIGN KEY (id_medico_crm) REFERENCES Medico(id_medico_crm),
    FOREIGN KEY (id_func_registro) REFERENCES Funcionario(id_funcionario),
    FOREIGN KEY (id_convenio) REFERENCES Convenio(id_convenio)
) ENGINE=InnoDB;

CREATE TABLE Medico_Especialidade (
    id_medico_crm VARCHAR(20) NOT NULL,
    id_especialidade INT NOT NULL,
    PRIMARY KEY (id_medico_crm, id_especialidade),
    FOREIGN KEY (id_medico_crm) REFERENCES Medico(id_medico_crm),
    FOREIGN KEY (id_especialidade) REFERENCES Especialidade(id_especialidade)
) ENGINE=InnoDB;

CREATE TABLE Paciente_Doenca (
    id_paciente INT NOT NULL,
    id_doenca INT NOT NULL,
    PRIMARY KEY (id_paciente, id_doenca),
    FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente),
    FOREIGN KEY (id_doenca) REFERENCES Doenca(id_doenca)
) ENGINE=InnoDB;

CREATE TABLE Consulta_Exame (
    id_consulta INT NOT NULL,
    id_exame INT NOT NULL,
    PRIMARY KEY (id_consulta, id_exame),
    FOREIGN KEY (id_consulta) REFERENCES Consulta(id_consulta),
    FOREIGN KEY (id_exame) REFERENCES Tipo_Exame(id_exame)
) ENGINE=InnoDB;

CREATE TABLE Consulta_Equipamento (
    id_consulta    INT NOT NULL,
    id_equipamento INT NOT NULL,
    PRIMARY KEY (id_consulta, id_equipamento),
    CONSTRAINT fk_ce_consulta
      FOREIGN KEY (id_consulta)    REFERENCES Consulta(id_consulta)
      ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_ce_equipamento
      FOREIGN KEY (id_equipamento) REFERENCES Equipamento(id_equipamento)
      ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Prescricao (
    id_consulta INT NOT NULL,
    id_medicamento INT NOT NULL,
    posologia VARCHAR(200),
    quantidade VARCHAR(50),

    PRIMARY KEY (id_consulta, id_medicamento),
    FOREIGN KEY (id_consulta) REFERENCES Consulta(id_consulta),
    FOREIGN KEY (id_medicamento) REFERENCES Medicamento(id_medicamento)
) ENGINE=InnoDB;

CREATE TABLE Encaminhamento (
    id_encaminhamento INT AUTO_INCREMENT PRIMARY KEY,
    id_funcionario INT NOT NULL,
    id_clinica INT NOT NULL,
    data_encaminhamento DATE,
    observacao VARCHAR(255),

    FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario),
    FOREIGN KEY (id_clinica) REFERENCES Clinica_Parceira(id_clinica)
) ENGINE=InnoDB;

CREATE TABLE SugestaoIA (
    id_sugestao INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NULL,
    id_consulta INT NULL,
    texto_pergunta VARCHAR(2000) NOT NULL,
    resposta_ia TEXT NOT NULL,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente),
    FOREIGN KEY (id_consulta) REFERENCES Consulta(id_consulta)
);

CREATE TABLE relatorio_ia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT,
    id_consulta INT,
    descricao TEXT NOT NULL,
    resposta_ia TEXT NOT NULL,
    data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente),
    FOREIGN KEY (id_consulta) REFERENCES consulta(id_consulta)
);

CREATE TABLE IF NOT EXISTS Consulta_Equipamento (
    id_consulta    INT NOT NULL,
    id_equipamento INT NOT NULL,
    PRIMARY KEY (id_consulta, id_equipamento),
    CONSTRAINT fk_ce_consulta
      FOREIGN KEY (id_consulta)    REFERENCES Consulta(id_consulta)
      ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_ce_equipamento
      FOREIGN KEY (id_equipamento) REFERENCES Equipamento(id_equipamento)
      ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;


-- Algumas operações feitas no Banco de Dados (Manipulações do Banco De Dados)


ALTER TABLE Medico
ADD COLUMN especialidade VARCHAR(100),
ADD COLUMN email VARCHAR(100);

ALTER TABLE Paciente_Doenca
  DROP FOREIGN KEY paciente_doenca_ibfk_1,
  DROP FOREIGN KEY paciente_doenca_ibfk_2;

ALTER TABLE Paciente_Doenca
  ADD INDEX idx_pd_paciente (id_paciente),
  ADD INDEX idx_pd_doenca   (id_doenca);

ALTER TABLE Paciente_Doenca
  ADD CONSTRAINT fk_pd_paciente
    FOREIGN KEY (id_paciente)
    REFERENCES Paciente(id_paciente)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  ADD CONSTRAINT fk_pd_doenca
    FOREIGN KEY (id_doenca)
    REFERENCES Doenca(id_doenca)
    ON DELETE RESTRICT
    ON UPDATE CASCADE;

ALTER TABLE Convenio
  ADD COLUMN cnpj     VARCHAR(20)  NULL AFTER nome_convenio;

ALTER TABLE Convenio
  ADD COLUMN telefone VARCHAR(20)  NULL;

ALTER TABLE Convenio
  ADD COLUMN email    VARCHAR(100) NULL;

ALTER TABLE Clinica_Parceira ADD COLUMN cnpj     VARCHAR(20)  NULL;
ALTER TABLE Clinica_Parceira ADD COLUMN telefone VARCHAR(20)  NULL;
ALTER TABLE Clinica_Parceira ADD COLUMN email    VARCHAR(100) NULL;
ALTER TABLE Clinica_Parceira ADD COLUMN endereco VARCHAR(200) NULL;

-- Exemplos de instruções(inserção, seleção ...):

DESCRIBE Clinica_Parceira;


INSERT INTO Convenio (nome_convenio, cnpj, telefone, email)
VALUES ('UFSC', '4444444444', '985477373737', 'ufsc@gmail.com'),
('Bradesco', '3333333333', '489877373737', 'Brad@gmail.com'),
('UNIMED', '2222222222', '716464744888', 'unim@gmail.com'),
('Ararangua', '1111111111', '567677373737', 'ara@gmail.com');

INSERT INTO Funcionario (nome_funcionario, cargo, data_admissao, telefone, email)
VALUES
('Ana Recepcionista', 'Atendente',        '2024-01-10', '48999990001', 'ana@clinica.com'),
('João Atendente',    'Atendente',        '2024-02-15', '48999990002', 'joao@clinica.com'),
('Jim Lau',           'Tesoureiro',       '2025-02-18', '48599990002', 'jim@clinica.com'),
('Gustavo Lima',      'Auxiliar técnico', '2021-02-10', '71999990002', 'gust@clinica.com'),
('Olga',              'Enfermeira',       '1996-02-29', '657599990002','olg@clinica.com'),
('Araranguá',         'Cidade',           '2024-02-15', '546499990002','ar@clinica.com');

INSERT INTO Paciente (nome, data_nascimento, telefone, email, cpf, endereco)
VALUES
  ('Andre Gaspar','2002-08-20','489988895','andregaspar@gmail.com','112233356','Rua 0987'),
  ('Antonio Sob','1500-05-30','719988895','anto@gmail.com','35353636363','Rua 0007'),
  ('Aline Barros','2022-08-23','44647848484','alin@gmail.com','464646646646','Rua 0008'),
  ('Mauricio Girard','1967-05-03','4569988895','mau@gmail.com','1647473356','Rua 07'),
  ('Balduino da Silva','1999-03-23','48982922220','bald@gmail.com','11227282920','Rua Girassol');

INSERT INTO Medico (id_medico_crm, nome_medico, telefone)
VALUES
  ('1111111111','Enzo Fernandes','48999990010'),
  ('2222222222','Mariana Costa','48999990011'),
  ('3333333333','Dentista Carla','48999990012');


INSERT INTO Doenca (nome_doenca) VALUES ('Hipertensão'), ('Diabetes');

INSERT INTO Paciente_Doenca (id_paciente, id_doenca) VALUES (1,1),(1,2);

INSERT INTO Equipamento (nome_equipamento) VALUES ('Eletrocardiógrafo'), ('Otoscópio');

INSERT INTO Consulta_Equipamento (id_consulta, id_equipamento) VALUES (1,1);

INSERT INTO relatorio_ia (id_paciente, id_consulta, descricao, resposta_ia)

INSERT INTO Medicamento (nome_medicamento) VALUES ('Dipirona 500mg');

INSERT INTO Prescricao (id_consulta, id_medicamento, posologia, quantidade)
VALUES (6, 1, '350 mg a cada 8h', '100 comprimidos');

VALUES (4, NULL, 'paciente com diarreia aguda', 'Sugestão gerada pela IA aqui...');

INSERT INTO Equipamento (nome_equipamento) VALUES
('ECG'),
('Bomba de Infusão'),
('Oxímetro de Pulso'),
('Ultrassom'),
('Esfigmomanômetro');

INSERT INTO Doenca (nome_doenca) VALUES
('Hipertensão'),
('Diabetes'),
('Asma'),
('Gastrite'),
('Depressão'),
('Enxaqueca'),
('Anemia')
ON DUPLICATE KEY UPDATE nome_doenca = VALUES(nome_doenca);

SELECT id_paciente, nome FROM Paciente ORDER BY id_paciente;
SELECT id_doenca, nome_doenca FROM Doenca ORDER BY id_doenca;

SHOW TABLES;
SHOW CREATE TABLE Consulta_Equipamento;
DROP TABLE IF EXISTS Consulta_Equipamento;

SELECT * FROM paciente;
SELECT * FROM Medico
SELECT * FROM SugestaoIA;
SELECT * FROM doenca;
SELECT * FROM Funcionario;

SELECT id_consulta, id_paciente, id_medico_crm, data_consulta
FROM Consulta
ORDER BY id_consulta;
select * from doenca;
SELECT id_medicamento, nome_medicamento
FROM Medicamento
ORDER BY id_medicamento;

USE clinica;