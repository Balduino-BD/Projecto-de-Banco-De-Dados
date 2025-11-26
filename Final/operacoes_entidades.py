


# operacoes_entidades.py


from db import execute_query, execute_dml


# =============== PACIENTE ===============


def inserir_paciente():
    print()
    nome = input("Nome: ").strip()
    data_nasc = input("Data de nascimento (AAAA-MM-DD) [opcional]: ").strip() or None
    telefone = input("Telefone [opcional]: ").strip() or None
    email = input("Email [opcional]: ").strip() or None
    cpf = input("CPF [opcional]: ").strip() or None
    endereco = input("Endereço [opcional]: ").strip() or None
    id_func = input("ID do funcionário que atendeu [opcional]: ").strip() or None

    sql = """
        INSERT INTO Paciente (nome, data_nascimento, telefone, email, cpf, endereco, id_func_atendimento)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    execute_dml(sql, (nome, data_nasc, telefone, email, cpf, endereco, id_func))
    print("Paciente inserido!\n")

def listar_pacientes():
    print()
    cols, rows = execute_query("""
        SELECT id_paciente, nome, data_nascimento, telefone, email, cpf, endereco, id_func_atendimento
        FROM Paciente
        ORDER BY id_paciente
    """)
    print(" | ".join(cols))
    for r in rows: print(" | ".join(str(x) for x in r))
    print()

def atualizar_paciente():
    print()
    pid = input("ID do paciente a atualizar: ").strip()
    cols, rows = execute_query("SELECT id_paciente, nome, data_nascimento, telefone, email, cpf, endereco, id_func_atendimento FROM Paciente WHERE id_paciente=%s", (pid,))
    if not rows:
        print("Paciente não encontrado."); return

    print("Registro atual:")
    print(" | ".join(cols))
    print(" | ".join(str(x) for x in rows[0]))

    nome = input("Novo nome (enter p/ manter): ").strip()
    data_nasc = input("Nova data nascimento (AAAA-MM-DD) (enter p/ manter): ").strip()
    telefone = input("Novo telefone (enter p/ manter): ").strip()
    email = input("Novo email (enter p/ manter): ").strip()
    cpf = input("Novo CPF (enter p/ manter): ").strip()
    endereco = input("Novo endereço (enter p/ manter): ").strip()
    id_func = input("Novo id_func_atendimento (enter p/ manter): ").strip()

    campos, params = [], []
    if nome: campos.append("nome=%s"); params.append(nome)
    if data_nasc: campos.append("data_nascimento=%s"); params.append(data_nasc)
    if telefone: campos.append("telefone=%s"); params.append(telefone)
    if email: campos.append("email=%s"); params.append(email)
    if cpf: campos.append("cpf=%s"); params.append(cpf)
    if endereco: campos.append("endereco=%s"); params.append(endereco)
    if id_func: campos.append("id_func_atendimento=%s"); params.append(id_func)

    if not campos:
        print("Nada a atualizar."); return
    params.append(pid)
    sql = f"UPDATE Paciente SET {', '.join(campos)} WHERE id_paciente=%s"
    execute_dml(sql, tuple(params))
    print("Paciente atualizado!\n")

def excluir_paciente():
    print()
    pid = input("ID do paciente a excluir: ").strip()
    try:
        execute_dml("DELETE FROM Paciente WHERE id_paciente=%s", (pid,))
        print("Paciente excluído (se existia).")
    except Exception as e:
        print(f"Falha ao excluir paciente {pid}. Verifique vínculos. Detalhe: {e}")


# =============== MEDICO ===============
def inserir_medico():
    print()
    crm = input("CRM (id_medico_crm): ").strip()
    nome = input("Nome: ").strip()
    telefone = input("Telefone [opcional]: ").strip() or None

    sql = "INSERT INTO Medico (id_medico_crm, nome_medico, telefone) VALUES (%s, %s, %s)"
    execute_dml(sql, (crm, nome, telefone))
    print("Médico inserido!\n")

def listar_medicos():
    print()
    cols, rows = execute_query("SELECT id_medico_crm, nome_medico, telefone FROM Medico ORDER BY nome_medico")
    print(" | ".join(cols))
    for r in rows: print(" | ".join(str(x) for x in r))
    print()

def atualizar_medico():
    print()
    crm = input("CRM do médico a atualizar: ").strip()
    cols, rows = execute_query("SELECT id_medico_crm, nome_medico, telefone FROM Medico WHERE id_medico_crm=%s", (crm,))
    if not rows:
        print("Médico não encontrado."); return

    print("Registro atual:")
    print(" | ".join(cols))
    print(" | ".join(str(x) for x in rows[0]))

    nome = input("Novo nome (enter p/ manter): ").strip()
    telefone = input("Novo telefone (enter p/ manter): ").strip()

    campos, params = [], []
    if nome: campos.append("nome_medico=%s"); params.append(nome)
    if telefone: campos.append("telefone=%s"); params.append(telefone)

    if not campos:
        print("Nada a atualizar."); return
    params.append(crm)
    sql = f"UPDATE Medico SET {', '.join(campos)} WHERE id_medico_crm=%s"
    execute_dml(sql, tuple(params))
    print("Médico atualizado!\n")

def excluir_medico():
    print()
    crm = input("CRM do médico a excluir: ").strip()
    try:
        execute_dml("DELETE FROM Medico WHERE id_medico_crm=%s", (crm,))
        print("Médico excluído (se existia).")
    except Exception as e:
        print(f"Falha ao excluir médico {crm}. Verifique vínculos. Detalhe: {e}")


# =============== FUNCIONARIO ===============


def inserir_funcionario():
    print()
    nome = input("Nome: ").strip()
    data_adm = input("Data admissão (AAAA-MM-DD) [opcional]: ").strip() or None
    cargo = input("Cargo [opcional]: ").strip() or None
    telefone = input("Telefone [opcional]: ").strip() or None
    email = input("Email [opcional]: ").strip() or None

    sql = """
        INSERT INTO Funcionario (nome_funcionario, data_admissao, cargo, telefone, email)
        VALUES (%s, %s, %s, %s, %s)
    """
    execute_dml(sql, (nome, data_adm, cargo, telefone, email))
    print("Funcionário inserido!\n")

def listar_funcionarios():
    print()
    cols, rows = execute_query("""
        SELECT id_funcionario, nome_funcionario, data_admissao, cargo, telefone, email
        FROM Funcionario
        ORDER BY id_funcionario
    """)
    print(" | ".join(cols))
    for r in rows: print(" | ".join(str(x) for x in r))
    print()

def atualizar_funcionario():
    print()
    fid = input("ID do funcionário a atualizar: ").strip()
    cols, rows = execute_query("""
        SELECT id_funcionario, nome_funcionario, data_admissao, cargo, telefone, email
        FROM Funcionario WHERE id_funcionario=%s
    """, (fid,))
    if not rows:
        print("Funcionário não encontrado."); return

    print("Registro atual:")
    print(" | ".join(cols))
    print(" | ".join(str(x) for x in rows[0]))

    nome = input("Novo nome (enter p/ manter): ").strip()
    data_adm = input("Nova data admissão (AAAA-MM-DD) (enter p/ manter): ").strip()
    cargo = input("Novo cargo (enter p/ manter): ").strip()
    telefone = input("Novo telefone (enter p/ manter): ").strip()
    email = input("Novo email (enter p/ manter): ").strip()

    campos, params = [], []
    if nome: campos.append("nome_funcionario=%s"); params.append(nome)
    if data_adm: campos.append("data_admissao=%s"); params.append(data_adm)
    if cargo: campos.append("cargo=%s"); params.append(cargo)
    if telefone: campos.append("telefone=%s"); params.append(telefone)
    if email: campos.append("email=%s"); params.append(email)

    if not campos:
        print("Nada a atualizar."); return
    params.append(fid)
    sql = f"UPDATE Funcionario SET {', '.join(campos)} WHERE id_funcionario=%s"
    execute_dml(sql, tuple(params))
    print("Funcionário atualizado!\n")

def excluir_funcionario():
    print()
    fid = input("ID do funcionário a excluir: ").strip()
    try:
        execute_dml("DELETE FROM Funcionario WHERE id_funcionario=%s", (fid,))
        print("Funcionário excluído (se existia).")
    except Exception as e:
        print(f"Falha ao excluir funcionário {fid}. Verifique vínculos. Detalhe: {e}")


# =============== CONSULTA ===============


def inserir_consulta():
    print()
    id_paciente = input("ID do paciente: ").strip()
    id_medico = input("CRM do médico: ").strip()
    id_func = input("ID do funcionário (registro): ").strip()
    id_conv = input("ID do convênio [opcional]: ").strip() or None
    data_consulta = input("Data da consulta (AAAA-MM-DD): ").strip()
    valor = input("Valor (ex: 200.00) [opcional]: ").strip() or None
    observacao = input("Observação [opcional]: ").strip() or None

    sql = """
        INSERT INTO Consulta
        (id_paciente, id_medico_crm, id_func_registro, id_convenio, data_consulta, valor, observacao)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """
    execute_dml(sql, (id_paciente, id_medico, id_func, id_conv, data_consulta, valor, observacao))
    print("Consulta inserida!\n")

def listar_consultas():
    print()
    cols, rows = execute_query("""
        SELECT id_consulta, id_paciente, id_medico_crm, id_func_registro, id_convenio, data_consulta, valor, observacao
        FROM Consulta
        ORDER BY id_consulta
    """)
    print(" | ".join(cols))
    for r in rows: print(" | ".join(str(x) for x in r))
    print()

def atualizar_consulta():
    print()
    cid = input("ID da consulta a atualizar: ").strip()
    cols, rows = execute_query("""
        SELECT id_consulta, id_paciente, id_medico_crm, id_func_registro, id_convenio, data_consulta, valor, observacao
        FROM Consulta WHERE id_consulta=%s
    """, (cid,))
    if not rows:
        print("Consulta não encontrada."); return

    print("Registro atual:")
    print(" | ".join(cols))
    print(" | ".join(str(x) for x in rows[0]))

    id_paciente = input("Novo id_paciente (enter p/ manter): ").strip()
    id_medico = input("Novo id_medico_crm (enter p/ manter): ").strip()
    id_func = input("Novo id_func_registro (enter p/ manter): ").strip()
    id_conv = input("Novo id_convenio (enter p/ manter): ").strip()
    data_consulta = input("Nova data (AAAA-MM-DD) (enter p/ manter): ").strip()
    valor = input("Novo valor (enter p/ manter): ").strip()
    observacao = input("Nova observação (enter p/ manter): ").strip()

    campos, params = [], []
    if id_paciente: campos.append("id_paciente=%s"); params.append(id_paciente)
    if id_medico: campos.append("id_medico_crm=%s"); params.append(id_medico)
    if id_func: campos.append("id_func_registro=%s"); params.append(id_func)
    if id_conv: campos.append("id_convenio=%s"); params.append(id_conv)
    if data_consulta: campos.append("data_consulta=%s"); params.append(data_consulta)
    if valor: campos.append("valor=%s"); params.append(valor)
    if observacao: campos.append("observacao=%s"); params.append(observacao)

    if not campos:
        print("Nada a atualizar."); return
    params.append(cid)
    sql = f"UPDATE Consulta SET {', '.join(campos)} WHERE id_consulta=%s"
    execute_dml(sql, tuple(params))
    print("Consulta atualizada!\n")

def excluir_consulta():
    print()
    cid = input("ID da consulta a excluir: ").strip()
    try:
        execute_dml("DELETE FROM Consulta WHERE id_consulta=%s", (cid,))
        print("Consulta excluída (se existia).")
    except Exception as e:
        print(f"Falha ao excluir consulta {cid}. Verifique vínculos. Detalhe: {e}")


# =============== TIPO_EXAME ===============


def inserir_exame():
    print()
    nome = input("Nome do exame: ").strip()
    sql = "INSERT INTO Tipo_Exame (nome_exame) VALUES (%s)"
    execute_dml(sql, (nome,))
    print("Tipo de exame inserido!\n")

def listar_exames():
    print()
    cols, rows = execute_query("SELECT id_exame, nome_exame FROM Tipo_Exame ORDER BY id_exame")
    print(" | ".join(cols))
    for r in rows: print(" | ".join(str(x) for x in r))
    print()

def excluir_exame():
    print()
    ide = input("ID do exame a excluir: ").strip()
    try:
        execute_dml("DELETE FROM Tipo_Exame WHERE id_exame=%s", (ide,))
        print("Exame excluído (se existia).")
    except Exception as e:
        print(f"Falha ao excluir exame {ide}. Verifique vínculos. Detalhe: {e}")

# vínculo consulta-exame

def vincular_exame_a_consulta():
    print()
    cid = input("ID da consulta: ").strip()
    ide = input("ID do exame: ").strip()

    # checagens básicas
    
    if not execute_query("SELECT 1 FROM Consulta WHERE id_consulta=%s", (cid,))[1]:
        print("Consulta inexistente."); return
    if not execute_query("SELECT 1 FROM Tipo_Exame WHERE id_exame=%s", (ide,))[1]:
        print("Exame inexistente."); return

    # evita duplicidade
    
    
    if execute_query("SELECT 1 FROM Consulta_Exame WHERE id_consulta=%s AND id_exame=%s", (cid, ide))[1]:
        print("Já existe esse vínculo (consulta, exame)."); return

    execute_dml("INSERT INTO Consulta_Exame (id_consulta, id_exame) VALUES (%s,%s)", (cid, ide))
    print("Exame vinculado à consulta!\n")

def listar_exames_da_consulta():
    print()
    cid = input("ID da consulta: ").strip()
    sql = """
        SELECT ce.id_consulta, e.id_exame, e.nome_exame
        FROM Consulta_Exame ce
        JOIN Tipo_Exame e ON e.id_exame = ce.id_exame
        WHERE ce.id_consulta=%s
        ORDER BY e.nome_exame
    """
    cols, rows = execute_query(sql, (cid,))
    print(" | ".join(cols))
    for r in rows: print(" | ".join(str(x) for x in r))
    print()


# =============== PRESCRICAO ===============


def inserir_prescricao():
    print()
    id_consulta = input("ID da consulta: ").strip()
    id_medicamento = input("ID do medicamento: ").strip()
    posologia = input("Posologia: ").strip()
    quantidade = input("Quantidade: ").strip()

    # Verifica existência
    
    if not execute_query("SELECT 1 FROM Consulta WHERE id_consulta=%s", (id_consulta,))[1]:
        print(f"Consulta {id_consulta} não existe. Liste as consultas e tente novamente.")
        return
    if not execute_query("SELECT 1 FROM Medicamento WHERE id_medicamento=%s", (id_medicamento,))[1]:
        print(f"Medicamento {id_medicamento} não existe. Liste/insira o medicamento e tente novamente.")
        return

    # Evita duplicidade da PK composta
    
    if execute_query(
        "SELECT 1 FROM Prescricao WHERE id_consulta=%s AND id_medicamento=%s",
        (id_consulta, id_medicamento)
    )[1]:
        print("Já existe prescrição para esse par (consulta, medicamento).")
        return

    sql = """
        INSERT INTO Prescricao (id_consulta, id_medicamento, posologia, quantidade)
        VALUES (%s, %s, %s, %s)
    """
    execute_dml(sql, (id_consulta, id_medicamento, posologia, quantidade))
    print("Prescrição inserida!\n")

def listar_prescricoes():
    print()
    cols, rows = execute_query("SELECT id_consulta, id_medicamento, posologia, quantidade FROM Prescricao ORDER BY id_consulta, id_medicamento")
    print(" | ".join(cols))
    for r in rows: print(" | ".join(str(x) for x in r))
    print()

def excluir_prescricao():
    print()
    idc = input("ID da consulta: ").strip()
    idm = input("ID do medicamento: ").strip()
    try:
        execute_dml("DELETE FROM Prescricao WHERE id_consulta=%s AND id_medicamento=%s", (idc, idm))
        print("Prescrição excluída (se existia).")
    except Exception as e:
        print(f"Falha ao excluir prescrição. Detalhe: {e}")


# =============== ENCAMINHAMENTO ===============


def inserir_encaminhamento():
    print()
    id_func = input("ID do funcionário: ").strip()
    id_clinica = input("ID da clínica parceira: ").strip()
    data_enc = input("Data do encaminhamento (AAAA-MM-DD) [opcional]: ").strip() or None
    obs = input("Observação [opcional]: ").strip() or None

    sql = """
        INSERT INTO Encaminhamento (id_funcionario, id_clinica, data_encaminhamento, observacao)
        VALUES (%s, %s, %s, %s)
    """
    execute_dml(sql, (id_func, id_clinica, data_enc, obs))
    print("Encaminhamento inserido!\n")

def listar_encaminhamentos():
    print()
    sql = """
        SELECT e.id_encaminhamento,
               e.id_funcionario,
               f.nome_funcionario,
               e.id_clinica,
               cp.nome_clinica,
               e.data_encaminhamento,
               e.observacao
        FROM Encaminhamento e
        JOIN Funcionario f      ON f.id_funcionario = e.id_funcionario
        JOIN Clinica_Parceira cp ON cp.id_clinica   = e.id_clinica
        ORDER BY e.id_encaminhamento
    """
    cols, rows = execute_query(sql)
    print(" | ".join(cols))
    for r in rows: print(" | ".join(str(x) for x in r))
    print()

def excluir_encaminhamento():
    print()
    ide = input("ID do encaminhamento a excluir: ").strip()
    try:
        execute_dml("DELETE FROM Encaminhamento WHERE id_encaminhamento=%s", (ide,))
        print("Encaminhamento excluído (se existia).")
    except Exception as e:
        print(f"Falha ao excluir encaminhamento {ide}. Verifique vínculos. Detalhe: {e}")


# =============== CLINICA PARCEIRA  ===============

def inserir_clinica():
    print()
    nome = input("Nome da clínica: ").strip()
    cnpj = input("CNPJ (opcional): ").strip() or None
    telefone = input("Telefone (opcional): ").strip() or None
    email = input("Email (opcional): ").strip() or None
    endereco = input("Endereço (opcional): ").strip() or None
    sql = """
        INSERT INTO Clinica_Parceira (nome_clinica, cnpj, telefone, email, endereco)
        VALUES (%s, %s, %s, %s, %s)
    """
    execute_dml(sql, (nome, cnpj, telefone, email, endereco))
    print("Clínica parceira inserida!\n")

def listar_clinicas():
    print()
    cols, rows = execute_query("""
        SELECT id_clinica, nome_clinica, cnpj, telefone, email, endereco
        FROM Clinica_Parceira
        ORDER BY nome_clinica
    """)
    print(" | ".join(cols))
    for r in rows: print(" | ".join(str(x) for x in r))
    print()

def atualizar_clinica():
    print()
    idc = input("ID da clínica a atualizar: ").strip()
    cols, rows = execute_query("""
        SELECT id_clinica, nome_clinica, cnpj, telefone, email, endereco
        FROM Clinica_Parceira WHERE id_clinica=%s
    """, (idc,))
    if not rows:
        print("Clínica não encontrada."); return

    print("Registro atual:")
    print(" | ".join(cols))
    print(" | ".join(str(x) for x in rows[0]))

    nome = input("Novo nome (enter p/ manter): ").strip()
    cnpj = input("Novo CNPJ (enter p/ manter): ").strip()
    telefone = input("Novo telefone (enter p/ manter): ").strip()
    email = input("Novo email (enter p/ manter): ").strip()
    endereco = input("Novo endereço (enter p/ manter): ").strip()

    campos, params = [], []
    if nome: campos.append("nome_clinica=%s"); params.append(nome)
    if cnpj: campos.append("cnpj=%s"); params.append(cnpj)
    if telefone: campos.append("telefone=%s"); params.append(telefone)
    if email: campos.append("email=%s"); params.append(email)
    if endereco: campos.append("endereco=%s"); params.append(endereco)

    if not campos:
        print("Nada a atualizar."); return
    params.append(idc)
    sql = f"UPDATE Clinica_Parceira SET {', '.join(campos)} WHERE id_clinica=%s"
    execute_dml(sql, tuple(params))
    print("Clínica atualizada!\n")

def excluir_clinica():
    print()
    idc = input("ID da clínica a excluir: ").strip()
    try:
        execute_dml("DELETE FROM Clinica_Parceira WHERE id_clinica=%s", (idc,))
        print("Clínica excluída (se existia).")
    except Exception as e:
        print(f"Falha ao excluir clínica {idc}. Verifique vínculos. Detalhe: {e}")


# =============== CONVENIO  ===============


def inserir_convenio():
    print()
    nome = input("Nome do convênio: ").strip()
    cobertura = input("Cobertura (opcional): ").strip() or None
    tipo = input("Tipo do convênio (opcional): ").strip() or None
    sql = "INSERT INTO Convenio (nome_convenio, cobertura, tipo_convenio) VALUES (%s,%s,%s)"
    execute_dml(sql, (nome, cobertura, tipo))
    print("Convênio inserido!\n")

def listar_convenios():
    print()
    cols, rows = execute_query("SELECT id_convenio, nome_convenio, cobertura, tipo_convenio FROM Convenio ORDER BY nome_convenio")
    print(" | ".join(cols))
    for r in rows: print(" | ".join(str(x) for x in r))
    print()

def atualizar_convenio():
    print()
    cid = input("ID do convênio a atualizar: ").strip()
    cols, rows = execute_query("SELECT id_convenio, nome_convenio, cobertura, tipo_convenio FROM Convenio WHERE id_convenio=%s", (cid,))
    if not rows:
        print("Convênio não encontrado."); return

    print("Registro atual:")
    print(" | ".join(cols))
    print(" | ".join(str(x) for x in rows[0]))

    nome = input("Novo nome (enter p/ manter): ").strip()
    cobertura = input("Nova cobertura (enter p/ manter): ").strip()
    tipo = input("Novo tipo (enter p/ manter): ").strip()

    campos, params = [], []
    if nome: campos.append("nome_convenio=%s"); params.append(nome)
    if cobertura: campos.append("cobertura=%s"); params.append(cobertura)
    if tipo: campos.append("tipo_convenio=%s"); params.append(tipo)

    if not campos:
        print("Nada a atualizar."); return
    params.append(cid)
    sql = f"UPDATE Convenio SET {', '.join(campos)} WHERE id_convenio=%s"
    execute_dml(sql, tuple(params))
    print("Convênio atualizado!\n")

def excluir_convenio():
    print()
    cid = input("ID do convênio a excluir: ").strip()
    try:
        execute_dml("DELETE FROM Convenio WHERE id_convenio=%s", (cid,))
        print("Convênio excluído (se existia).")
    except Exception as e:
        print(f"Falha ao excluir convênio {cid}. Verifique vínculos. Detalhe: {e}")


# =============== ESPECIALIDADE  ===============


def inserir_especialidade():
    print()
    nome = input("Nome da especialidade: ").strip()
    execute_dml("INSERT INTO Especialidade (nome_especialidade) VALUES (%s)", (nome,))
    print("Especialidade inserida!\n")

def listar_especialidades():
    print()
    cols, rows = execute_query("SELECT id_especialidade, nome_especialidade FROM Especialidade ORDER BY nome_especialidade")
    print(" | ".join(cols))
    for r in rows: print(" | ".join(str(x) for x in r))
    print()

def vincular_especialidade_medico():
    print()
    crm = input("CRM do médico: ").strip()
    ide = input("ID da especialidade: ").strip()

    if not execute_query("SELECT 1 FROM Medico WHERE id_medico_crm=%s", (crm,))[1]:
        print("Médico inexistente."); return
    if not execute_query("SELECT 1 FROM Especialidade WHERE id_especialidade=%s", (ide,))[1]:
        print("Especialidade inexistente."); return

    if execute_query(
        "SELECT 1 FROM Medico_Especialidade WHERE id_medico_crm=%s AND id_especialidade=%s",
        (crm, ide)
    )[1]:
        print("Esse vínculo já existe."); return

    execute_dml("INSERT INTO Medico_Especialidade (id_medico_crm, id_especialidade) VALUES (%s,%s)", (crm, ide))
    print("Vínculo médico ↔ especialidade inserido!\n")

def listar_medico_especialidades():
    print()
    sql = """
        SELECT m.id_medico_crm, m.nome_medico, e.id_especialidade, e.nome_especialidade
        FROM Medico m
        JOIN Medico_Especialidade me ON me.id_medico_crm = m.id_medico_crm
        JOIN Especialidade e         ON e.id_especialidade = me.id_especialidade
        ORDER BY m.nome_medico, e.nome_especialidade
    """
    cols, rows = execute_query(sql)
    print(" | ".join(cols))
    for r in rows: print(" | ".join(str(x) for x in r))
    print()


# ====== EQUIPAMENTO ==================================================


from db import execute_query, execute_dml  

def inserir_equipamento():
    print()
    nome = input("Nome do equipamento: ").strip()
    if not nome:
        print("Nome não pode ser vazio.\n")
        return
    sql = "INSERT INTO Equipamento (nome_equipamento) VALUES (%s)"
    execute_dml(sql, (nome,))
    print("Equipamento inserido!\n")

def listar_equipamentos():
    print()
    cols, rows = execute_query(
        "SELECT id_equipamento, nome_equipamento FROM Equipamento ORDER BY nome_equipamento"
    )
    if not rows:
        print("Nenhum equipamento cadastrado.\n")
        return
    print(" | ".join(cols))
    for r in rows:
        print(" | ".join(str(x) for x in r))
    print()

def atualizar_equipamento():
    print()
    ide = input("ID do equipamento a atualizar: ").strip()
    if not ide:
        print("Informe um ID.\n"); return

    cols, rows = execute_query(
        "SELECT id_equipamento, nome_equipamento FROM Equipamento WHERE id_equipamento=%s",
        (ide,)
    )
    if not rows:
        print("Equipamento não encontrado.\n")
        return

    print("Registro atual:")
    print(" | ".join(cols))
    print(" | ".join(str(x) for x in rows[0]))

    novo_nome = input("Novo nome (enter p/ manter): ").strip()
    if not novo_nome:
        print("Nada a atualizar.\n")
        return

    execute_dml(
        "UPDATE Equipamento SET nome_equipamento=%s WHERE id_equipamento=%s",
        (novo_nome, ide)
    )
    print("Equipamento atualizado!\n")

def excluir_equipamento():
    print()
    ide = input("ID do equipamento a excluir: ").strip()
    if not ide:
        print("Informe um ID.\n"); return
    try:
        execute_dml("DELETE FROM Equipamento WHERE id_equipamento=%s", (ide,))
        print("Equipamento excluído (se existia).\n")
    except Exception as e:
        print(f"Falha ao excluir. Verifique vínculos (Consulta_Equipamento). Detalhe: {e}\n")


# ====== DOENÇA =======================================================


def inserir_doenca():
    print()
    nome = input("Nome da doença: ").strip()
    if not nome:
        print("Nome não pode ser vazio.\n"); return
    execute_dml("INSERT INTO Doenca (nome_doenca) VALUES (%s)", (nome,))
    print("Doença inserida!\n")

def listar_doencas():
    print()
    cols, rows = execute_query(
        "SELECT id_doenca, nome_doenca FROM Doenca ORDER BY nome_doenca"
    )
    if not rows:
        print("Nenhuma doença cadastrada.\n"); return
    print(" | ".join(cols))
    for r in rows:
        print(" | ".join(str(x) for x in r))
    print()

def atualizar_doenca():
    print()
    idd = input("ID da doença a atualizar: ").strip()
    if not idd:
        print("Informe um ID.\n"); return
    cols, rows = execute_query(
        "SELECT id_doenca, nome_doenca FROM Doenca WHERE id_doenca=%s",
        (idd,)
    )
    if not rows:
        print("Doença não encontrada.\n"); return
    print("Registro atual:")
    print(" | ".join(cols))
    print(" | ".join(str(x) for x in rows[0]))
    novo = input("Novo nome (enter p/ manter): ").strip()
    if not novo:
        print("Nada a atualizar.\n"); return
    execute_dml("UPDATE Doenca SET nome_doenca=%s WHERE id_doenca=%s", (novo, idd))
    print("Doença atualizada!\n")

def excluir_doenca():
    print()
    idd = input("ID da doença a excluir: ").strip()
    if not idd:
        print("Informe um ID.\n"); return
    try:
        execute_dml("DELETE FROM Doenca WHERE id_doenca=%s", (idd,))
        print("Doença excluída (se existia).\n")
    except Exception as e:
        print(f"Falha ao excluir. Verifique vínculos (Paciente_Doenca). Detalhe: {e}\n")

    print()


# =============== HISTÓRICO DE IA ===============


def listar_sugestoes_ia():
    print()
    cols, rows = execute_query("""
        SELECT id_sugestao, id_paciente, id_consulta, LEFT(texto_pergunta, 80) AS pergunta_80,
               LEFT(resposta_ia, 80) AS resposta_80, criado_em
        FROM SugestaoIA
        ORDER BY criado_em DESC
    """)
    print(" | ".join(cols))
    for r in rows: print(" | ".join(str(x) for x in r))
    print()

