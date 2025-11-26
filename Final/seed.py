


SEED_SQL = """
INSERT INTO Funcionario (nome_funcionario, data_admissao, cargo, cpf, telefone, email)
VALUES
 ('Maria Recepcionista', '2023-01-10', 'Recepcionista', '11111111111', '48999990001', 'maria@clinica.com'),
 ('João Admin',         '2022-03-15', 'Administrador', '22222222222', '48999990002', 'joao@clinica.com');

INSERT INTO Medico (id_medico_crm, nome_medico, telefone)
VALUES
 ('CRM1234', 'Dr. Pedro Cardio', '48999990003'),
 ('CRM5678', 'Dra. Ana Ortop',   '48999990004');

INSERT INTO Especialidade (nome_especialidade) VALUES
 ('Cardiologia'), ('Ortopedia');

INSERT INTO Medico_Especialidade (id_medico_crm, id_especialidade) VALUES
 ('CRM1234', 1),
 ('CRM5678', 2);

INSERT INTO Convenio (nome_convenio, cobertura, tipo_convenio) VALUES
 ('SaudePlus', 'Ambulatorial', 'Plano Empresa'),
 ('VidaBem',   'Ambulatorial e Hospitalar', 'Plano Individual');

INSERT INTO Paciente (nome, data_nascimento, telefone, email, cpf, endereco, id_func_atendimento) VALUES
 ('Carlos Silva','1990-05-10','48988880001','carlos@email.com','33333333333','Rua A, 123',1),
 ('Lucia Costa','1985-11-20','48988880002','lucia@email.com','44444444444','Rua B, 456',1);

INSERT INTO Doenca (nome_doenca) VALUES
 ('Hipertensao'), ('Diabetes Tipo 2');

INSERT INTO Paciente_Doenca (id_paciente, id_doenca) VALUES
 (1,1), (2,2);

INSERT INTO Equipamento (nome_equipamento) VALUES
 ('Aparelho de Pressao'), ('Eletrocardiograma');

INSERT INTO Tipo_Exame (nome_exame) VALUES
 ('Hemograma'), ('Eletrocardiograma');

INSERT INTO Medicamento (nome_medicamento) VALUES
 ('Losartana 50mg'), ('Metformina 850mg');

INSERT INTO Consulta (id_paciente, id_medico_crm, id_func_registro, id_convenio, data_consulta, valor, observacao)
VALUES
 (1, 'CRM1234', 1, 1, '2025-10-01', 300.00, 'Primeira consulta'),
 (2, 'CRM5678', 1, 2, '2025-10-02', 250.00, 'Retorno');

INSERT INTO Consulta_Exame (id_consulta, id_exame) VALUES
 (1,2),
 (2,1);

INSERT INTO Consulta_Equipamento (id_consulta, id_equipamento) VALUES
 (1,2),
 (2,1);

INSERT INTO Prescricao (id_consulta, id_medicamento, posologia, quantidade) VALUES
 (1,1,'1 comprimido 2x ao dia','30'),
 (2,2,'1 comprimido 1x ao dia','30');
"""
