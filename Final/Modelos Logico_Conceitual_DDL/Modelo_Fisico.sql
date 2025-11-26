-- Geração de Modelo físico
-- Sql ANSI 2003 - brModelo.



CREATE TABLE Doenca (
Id_doenca Texto(1) PRIMARY KEY,
nome_doenca Texto(1)
)

CREATE TABLE Paciente (
CPF Texto(1),
Enderenco Texto(1),
Data_Nacimento Texto(1),
Telefone Texto(1),
Email Texto(1),
Nome Texto(1),
Id_Paciente Texto(1) PRIMARY KEY,
data_admissao Texto(1),
id_funcionario Texto(1)
)

CREATE TABLE Medico (
Id_Medico(CRM) Texto(1) PRIMARY KEY,
Telefone Texto(1),
nome_medico Texto(1)
)

CREATE TABLE Funcionario (
cargo Texto(1),
data_admissao Texto(1),
telefone Texto(1),
cpf Texto(1),
-- Erro: nome do campo duplicado nesta tabela!
cargo Texto(1),
email Texto(1),
id_funcionario Texto(1),
nome_funcionario Texto(1),
PRIMARY KEY(data_admissao,id_funcionario)
)

CREATE TABLE Especialidade (
id_especialidade Texto(1) PRIMARY KEY,
nome_especialidade Texto(1)
)

CREATE TABLE Convenio (
nome_convenio Texto(1),
tipo_convenio Texto(1),
id_convenio Texto(1) PRIMARY KEY,
cobertura Texto(1)
)

CREATE TABLE Clinicas_Parceiras (
nome_clinica Texto(1),
id_clinica Texto(1) PRIMARY KEY
)

CREATE TABLE Equipamento (
id_equipamento Texto(1) PRIMARY KEY,
nome_equipamneto Texto(1)
)

CREATE TABLE Tipo de Exame (
id_exame Texto(1) PRIMARY KEY,
nome_exame Texto(1),
resultado_exame Texto(1)
)

CREATE TABLE Medicamento (
id_medicamento Texto(1) PRIMARY KEY,
nome_medicamento Texto(1)
)

CREATE TABLE consulta+ (
Id_Paciente Texto(1),
Id_Medico(CRM) Texto(1),
Valor Texto(1),
Observacao Texto(1),
Data_consulta Texto(1),
id_convenio Texto(1),
id_clinica Texto(1),
data_admissao Texto(1),
id_funcionario Texto(1),
FOREIGN KEY(Id_Paciente) REFERENCES Paciente (Id_Paciente),
FOREIGN KEY(Id_Medico(CRM)) REFERENCES Medico (Id_Medico(CRM)),
FOREIGN KEY(id_convenio) REFERENCES Convenio (id_convenio),
FOREIGN KEY(id_clinica) REFERENCES Clinicas_Parceiras (id_clinica),
FOREIGN KEY(/*erro: ??*/) REFERENCES Funcionario (data_admissao,id_funcionario)/*falha: chave estrangeira*/
)

CREATE TABLE Tem (
Id_Medico(CRM) Texto(1),
id_especialidade Texto(1),
FOREIGN KEY(Id_Medico(CRM)) REFERENCES Medico (Id_Medico(CRM)),
FOREIGN KEY(id_especialidade) REFERENCES Especialidade (id_especialidade)
)

CREATE TABLE Possui (
Id_Paciente Texto(1),
Id_doenca Texto(1),
FOREIGN KEY(Id_Paciente) REFERENCES Paciente (Id_Paciente),
FOREIGN KEY(Id_doenca) REFERENCES Doenca (Id_doenca)
)

CREATE TABLE Gera (
id_exame Texto(1),
FOREIGN KEY(id_exame) REFERENCES Tipo de Exame (id_exame)
)

CREATE TABLE Pescricao (
possologia Texto(1),
Quantidade Texto(1),
id_medicamento Texto(1),
FOREIGN KEY(id_medicamento) REFERENCES Medicamento (id_medicamento)
)

CREATE TABLE usa (
id_equipamento Texto(1),
FOREIGN KEY(id_equipamento) REFERENCES Equipamento (id_equipamento)
)

ALTER TABLE Paciente ADD FOREIGN KEY(id_funcionario,,) REFERENCES Funcionario (data_admissao,id_funcionario)
