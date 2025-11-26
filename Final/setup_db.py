

# setup_db.py


from db import execute_ddl, execute_dml, execute_query

# ---------- helpers ----------


def _col_exists(table: str, column: str) -> bool:
    sql = """
        SELECT COUNT(*) 
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = %s
          AND COLUMN_NAME = %s
    """
    _, rows = execute_query(sql, (table, column))
    return rows[0][0] > 0

def add_column_if_missing(table: str, column: str, definition_sql: str):
    if not _col_exists(table, column):
        execute_ddl(f"ALTER TABLE `{table}` ADD COLUMN `{column}` {definition_sql}")

def _table_exists(table: str) -> bool:
    sql = """
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = %s
    """
    _, rows = execute_query(sql, (table,))
    return rows[0][0] > 0

# ---------- DDL base  ----------


TABLES_SQL = """
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

-- ATENÇÃO: nome da tabela com underscore, conforme teu banco
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

CREATE TABLE IF NOT EXISTS SugestaoIA (
    id_sugestao INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NULL,
    id_consulta INT NULL,
    texto_pergunta VARCHAR(2000) NOT NULL,
    resposta_ia TEXT NOT NULL,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente),
    FOREIGN KEY (id_consulta) REFERENCES Consulta(id_consulta)
);

CREATE TABLE IF NOT EXISTS relatorio_ia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT,
    id_consulta INT,
    descricao TEXT NOT NULL,
    resposta_ia TEXT NOT NULL,
    data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_paciente) REFERENCES Paciente(id_paciente),
    FOREIGN KEY (id_consulta) REFERENCES Consulta(id_consulta)
);
"""

SEED_SQL = [
  
    # Funcionário 
    
    """
    INSERT INTO Funcionario (nome_funcionario, cargo, data_admissao, telefone, email)
    SELECT * FROM (
        SELECT 'Ana Recepcionista','Atendente','2024-01-10','48999990001','ana@clinica.com'
    ) AS tmp
    WHERE NOT EXISTS (
        SELECT 1 FROM Funcionario f WHERE f.nome_funcionario='Ana Recepcionista'
    );
    """,
    """
    INSERT INTO Funcionario (nome_funcionario, cargo, data_admissao, telefone, email)
    SELECT * FROM (
        SELECT 'João Atendente','Atendente','2024-02-15','48999990002','joao@clinica.com'
    ) AS tmp
    WHERE NOT EXISTS (
        SELECT 1 FROM Funcionario f WHERE f.nome_funcionario='João Atendente'
    );
    """,
    
    # Médicos
    
    """
    INSERT INTO Medico (id_medico_crm, nome_medico, telefone)
    SELECT * FROM (SELECT '1111111111','Enzo Fernandes','48999990010') AS tmp
    WHERE NOT EXISTS (SELECT 1 FROM Medico m WHERE m.id_medico_crm='1111111111');
    """,
    """
    INSERT INTO Medico (id_medico_crm, nome_medico, telefone)
    SELECT * FROM (SELECT '2222222222','Mariana Costa','48999990011') AS tmp
    WHERE NOT EXISTS (SELECT 1 FROM Medico m WHERE m.id_medico_crm='2222222222');
    """,
    """
    INSERT INTO Medico (id_medico_crm, nome_medico, telefone)
    SELECT * FROM (SELECT '3333333333','Dentista Carla','48999990012') AS tmp
    WHERE NOT EXISTS (SELECT 1 FROM Medico m WHERE m.id_medico_crm='3333333333');
    """,
    # Especialidades 
    
    "INSERT INTO Especialidade (nome_especialidade) SELECT 'Clínica Geral' WHERE NOT EXISTS (SELECT 1 FROM Especialidade WHERE nome_especialidade='Clínica Geral');",
    "INSERT INTO Especialidade (nome_especialidade) SELECT 'Pediatria' WHERE NOT EXISTS (SELECT 1 FROM Especialidade WHERE nome_especialidade='Pediatria');",
    "INSERT INTO Especialidade (nome_especialidade) SELECT 'Odontologia' WHERE NOT EXISTS (SELECT 1 FROM Especialidade WHERE nome_especialidade='Odontologia');",
]

def criar_apenas_tabelas():
    print("Criando/atualizando tabelas (idempotente)...")
    execute_ddl(TABLES_SQL)

    
    # Medico: + especialidade/email
    
    add_column_if_missing("Medico", "especialidade", "VARCHAR(100) NULL")
    add_column_if_missing("Medico", "email", "VARCHAR(100) NULL")

    # Convenio: + cnpj/telefone/email
    
    add_column_if_missing("Convenio", "cnpj", "VARCHAR(20) NULL")
    add_column_if_missing("Convenio", "telefone", "VARCHAR(20) NULL")
    add_column_if_missing("Convenio", "email", "VARCHAR(100) NULL")

    # Clinica_Parceira: + cnpj/telefone/email/endereco
    
    add_column_if_missing("Clinica_Parceira", "cnpj", "VARCHAR(20) NULL")
    add_column_if_missing("Clinica_Parceira", "telefone", "VARCHAR(20) NULL")
    add_column_if_missing("Clinica_Parceira", "email", "VARCHAR(100) NULL")
    add_column_if_missing("Clinica_Parceira", "endereco", "VARCHAR(200) NULL")

    print("OK.\n")

def criar_tabelas_e_carga():
    criar_apenas_tabelas()
    print("Inserindo carga inicial (sem duplicar)...")
    for s in SEED_SQL:
        execute_dml(s)
    print("Seed concluído.\n")

def apagar_todas_tabelas():
    print("Apagando todas as tabelas (cuidado!)...")

    # 1) Desliga verificação de FKs para evitar erro 3730 na ordem de drop
    execute_ddl("SET FOREIGN_KEY_CHECKS = 0")

    # 2) Dropar primeiro tabelas FILHAS, depois as PAIS (ordem segura)
    drop_order = [
        # filhas diretas
        "Prescricao",
        "Consulta_Equipamento",
        "Consulta_Exame",
        "Paciente_Doenca",
        "Medico_Especialidade",
        "Encaminhamento",       # <-- FALTAVA ESTA!
        "SugestaoIA",
        "relatorio_ia",

        # dependem de várias acima
        "Consulta",

        # bases de dados de itens
        "Medicamento",
        "Tipo_Exame",
        "Equipamento",

        # pais de encaminhamento
        "Clinica_Parceira",

        # pais de consulta
        "Convenio",
        "Paciente",
        "Medico",

        # dimensões restantes
        "Especialidade",
        "Doenca",
        "Funcionario",
    ]

    for t in drop_order:
        if _table_exists(t):
            execute_ddl(f"DROP TABLE IF EXISTS `{t}`")

    # 3) Religa verificação de FKs
    execute_ddl("SET FOREIGN_KEY_CHECKS = 1")
    print("Tabelas removidas.\n")

