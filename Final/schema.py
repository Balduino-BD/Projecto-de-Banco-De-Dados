
#SCHEMA SQL

DDL_CREATE = """
CREATE TABLE IF NOT EXISTS Funcionario (
    id_funcionario INT AUTO_INCREMENT PRIMARY KEY,
    nome_funcionario VARCHAR(100) NOT NULL,
    data_admissao DATE,
    cargo VARCHAR(50),
    cpf VARCHAR(14),
    telefone VARCHAR(20),
    email VARCHAR(100)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Doenca (
    id_doenca INT AUTO_INCREMENT PRIMARY KEY,
    nome_doenca VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Especialidade (
    id_especialidade INT AUTO_INCREMENT PRIMARY KEY,
    nome_especialidade VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Medico (
    id_medico_crm VARCHAR(20) PRIMARY KEY,
    nome_medico VARCHAR(100) NOT NULL,
    telefone VARCHAR(20)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Convenio (
    id_convenio INT AUTO_INCREMENT PRIMARY KEY,
    nome_convenio VARCHAR(100) NOT NULL,
    cobertura VARCHAR(200),
    tipo_convenio VARCHAR(50)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Clinica_Parceira (
    id_clinica INT AUTO_INCREMENT PRIMARY KEY,
    nome_clinica VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Equipamento (
    id_equipamento INT AUTO_INCREMENT PRIMARY KEY,
    nome_equipamento VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Tipo_Exame (
    id_exame INT AUTO_INCREMENT PRIMARY KEY,
    nome_exame VARCHAR(100) NOT NULL,
    resultado_exame VARCHAR(255)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Medicamento (
    id_medicamento INT AUTO_INCREMENT PRIMARY KEY,
    nome_medicamento VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Paciente (
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

CREATE TABLE IF NOT EXISTS Consulta (
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

CREATE TABLE IF NOT EXISTS Medico_Especialidade (
    id_medico_crm VARCHAR(20) NOT NULL,
    id_especialidade INT NOT NULL,
    PRIMARY KEY (id_medico_crm, id_especialidade),
    FOREIGN KEY (id_medico_crm) REFERENCES Medico(id_medico_crm),
    FOREIGN KEY (id_especialidade) REFERENCES Especialidade(id_especialidade)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Paciente_Doenca (
    id_paciente INT NOT NULL,
    id_doenca INT NOT NULL,
    PRIMARY KEY (id_paciente, id_doenca),
    FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente),
    FOREIGN KEY (id_doenca) REFERENCES Doenca(id_doenca)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Consulta_Exame (
    id_consulta INT NOT NULL,
    id_exame INT NOT NULL,
    PRIMARY KEY (id_consulta, id_exame),
    FOREIGN KEY (id_consulta) REFERENCES Consulta(id_consulta),
    FOREIGN KEY (id_exame) REFERENCES Tipo_Exame(id_exame)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Consulta_Equipamento (
    id_consulta INT NOT NULL,
    id_equipamento INT NOT NULL,
    PRIMARY KEY (id_consulta, id_equipamento),
    FOREIGN KEY (id_consulta) REFERENCES Consulta(id_consulta),
    FOREIGN KEY (id_equipamento) REFERENCES Equipamento(id_equipamento)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Prescricao (
    id_consulta INT NOT NULL,
    id_medicamento INT NOT NULL,
    posologia VARCHAR(200),
    quantidade VARCHAR(50),
    PRIMARY KEY (id_consulta, id_medicamento),
    FOREIGN KEY (id_consulta) REFERENCES Consulta(id_consulta),
    FOREIGN KEY (id_medicamento) REFERENCES Medicamento(id_medicamento)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Encaminhamento (
    id_encaminhamento INT AUTO_INCREMENT PRIMARY KEY,
    id_funcionario INT NOT NULL,
    id_clinica INT NOT NULL,
    data_encaminhamento DATE,
    observacao VARCHAR(255),
    FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario),
    FOREIGN KEY (id_clinica) REFERENCES Clinica_Parceira(id_clinica)
) ENGINE=InnoDB;
"""

# ordem inversa para não quebrar FKs


DDL_DROP = """
DROP TABLE IF EXISTS Encaminhamento;
DROP TABLE IF EXISTS Prescricao;
DROP TABLE IF EXISTS Consulta_Equipamento;
DROP TABLE IF EXISTS Consulta_Exame;
DROP TABLE IF EXISTS Paciente_Doenca;
DROP TABLE IF EXISTS Medico_Especialidade;
DROP TABLE IF EXISTS Consulta;
DROP TABLE IF EXISTS Paciente;
DROP TABLE IF EXISTS Medicamento;
DROP TABLE IF EXISTS Tipo_Exame;
DROP TABLE IF EXISTS Equipamento;
DROP TABLE IF EXISTS Clinica_Parceira;
DROP TABLE IF EXISTS Convenio;
DROP TABLE IF EXISTS Medico;
DROP TABLE IF EXISTS Especialidade;
DROP TABLE IF EXISTS Doenca;
DROP TABLE IF EXISTS Funcionario;
"""
