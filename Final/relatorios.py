# relatorios.py

from db import execute_query
from datetime import datetime
import os
import matplotlib.pyplot as plt

OUT_DIR = "saidas"
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------- helpers ----------------------------

def _print_table(cols, rows, max_rows=50):
    """Imprime uma amostra tabular (até max_rows linhas)."""
    print(" | ".join(cols))
    for r in rows[:max_rows]:
        print(" | ".join(str(x) for x in r))
    if len(rows) > max_rows:
        print(f"... (+{len(rows)-max_rows} linhas)")
    print()

def _ask_periodo(titulo: str):
    print(f"\n--- {titulo} ---")
    ini = input("Data inicial (AAAA-MM-DD): ").strip()
    fim = input("Data final   (AAAA-MM-DD): ").strip()

    for d in (ini, fim):
        try:
            datetime.strptime(d, "%Y-%m-%d")
        except ValueError:
            print("Data inválida! Use o formato AAAA-MM-DD")
            return None, None

    if ini > fim:
        print("Período inválido: a data inicial é maior que a final.")
        return None, None

    return ini, fim

def _bar(labels, values, title, xlabel, ylabel, filename):
    if not labels or not values:
        print("Sem dados para plotar.\n")
        return
    plt.figure()
    plt.bar(labels, values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    png = os.path.join(OUT_DIR, filename)
    plt.savefig(png, dpi=150)
    plt.show()
    plt.close()
    print(f"Gráfico salvo em: {png}")

# ------------------------ relatórios já existentes ------------------------

def total_consultas_periodo():
    ini, fim = _ask_periodo("TOTAL DE CONSULTAS NO PERÍODO (POR DIA)")
    if not ini:
        return

    sql = """
        SELECT DATE(c.data_consulta) AS dia,
               COUNT(*) AS total_consultas
        FROM Consulta c
        WHERE c.data_consulta BETWEEN %s AND %s
        GROUP BY DATE(c.data_consulta)
        ORDER BY DATE(c.data_consulta);
    """
    cols, rows = execute_query(sql, (ini, fim))
    if not rows:
        print("Sem dados no período.\n")
        return

    _print_table(cols, rows)
    dias   = [str(r[0]) for r in rows]
    totais = [int(r[1]) for r in rows]
    _bar(dias, totais,
         f"Total de Consultas por Dia ({ini} a {fim})",
         "Dia", "Consultas",
         f"total_consultas_{ini}_{fim}.png")

def faturamento_mensal_periodo():
    ini, fim = _ask_periodo("FATURAMENTO MENSAL NO PERÍODO")
    if not ini:
        return

    sql = """
        SELECT DATE_FORMAT(c.data_consulta, '%%Y-%%m') AS ano_mes,
               SUM(COALESCE(c.valor,0)) AS total_faturado
        FROM Consulta c
        WHERE c.data_consulta BETWEEN %s AND %s
        GROUP BY DATE_FORMAT(c.data_consulta, '%%Y-%%m')
        ORDER BY DATE_FORMAT(c.data_consulta, '%%Y-%%m');
    """
    cols, rows = execute_query(sql, (ini, fim))
    if not rows:
        print("Sem dados no período.\n")
        return

    _print_table(cols, rows)
    labels  = [r[0]        for r in rows]
    valores = [float(r[1]) for r in rows]
    _bar(labels, valores,
         f"Faturamento Mensal ({ini} a {fim})",
         "Mês (YYYY-MM)", "R$ (soma de valor)",
         f"faturamento_mensal_{ini}_{fim}.png")

def consultas_por_medico_periodo():
    ini, fim = _ask_periodo("CONSULTAS POR MÉDICO NO PERÍODO")
    if not ini:
        return

    sql = """
        SELECT m.nome_medico,
               COUNT(c.id_consulta) AS qtd_consultas,
               SUM(COALESCE(c.valor,0)) AS total_faturado
        FROM Medico m
        JOIN Consulta c ON c.id_medico_crm = m.id_medico_crm
        WHERE c.data_consulta BETWEEN %s AND %s
        GROUP BY m.nome_medico
        ORDER BY qtd_consultas DESC, m.nome_medico;
    """
    cols, rows = execute_query(sql, (ini, fim))
    if not rows:
        print("Sem dados no período.\n")
        return

    _print_table(cols, rows)
    nomes = [r[0]      for r in rows]
    qtd   = [int(r[1]) for r in rows]
    _bar(nomes, qtd,
         f"Consultas por Médico ({ini} a {fim})",
         "Médico", "Qtd de Consultas",
         f"consultas_por_medico_{ini}_{fim}.png")

def medicos_sem_consultas_no_periodo():
    ini, fim = _ask_periodo("MÉDICOS SEM CONSULTAS NO PERÍODO")
    if not ini:
        return

    sql_all = """
        SELECT m.nome_medico,
               COUNT(c.id_consulta) AS qtd_consultas
        FROM Medico m
        LEFT JOIN Consulta c
          ON c.id_medico_crm = m.id_medico_crm
         AND c.data_consulta BETWEEN %s AND %s
        GROUP BY m.id_medico_crm, m.nome_medico
        ORDER BY qtd_consultas ASC, m.nome_medico;
    """
    cols_all, rows_all = execute_query(sql_all, (ini, fim))
    if not rows_all:
        print("Não há médicos cadastrados.\n")
        return

    _print_table(cols_all, rows_all)

    sem = [r for r in rows_all if int(r[1]) == 0]
    if not sem:
        print("Todos os médicos possuem consultas no período informado.\n")
    else:
        print("Médicos SEM consultas no período:")
        for r in sem:
            print(f" - {r[0]}")
        print()

    nomes = [r[0]      for r in rows_all]
    qtd   = [int(r[1]) for r in rows_all]
    _bar(nomes, qtd,
         f"Consultas por Médico (inclui zero) — {ini} a {fim}",
         "Médico", "Qtd de Consultas",
         f"medicos_sem_consultas_{ini}_{fim}.png")

def consultas_por_funcionario_periodo():
    ini, fim = _ask_periodo("CONSULTAS POR FUNCIONÁRIO (REGISTRO) NO PERÍODO")
    if not ini:
        return

    sql = """
        SELECT f.nome_funcionario,
               COUNT(c.id_consulta) AS qtd
        FROM Funcionario f
        LEFT JOIN Consulta c
          ON c.id_func_registro = f.id_funcionario
         AND c.data_consulta BETWEEN %s AND %s
        GROUP BY f.id_funcionario, f.nome_funcionario
        ORDER BY qtd DESC, f.nome_funcionario;
    """
    cols, rows = execute_query(sql, (ini, fim))
    if not rows:
        print("Sem dados/funcionários cadastrados.\n")
        return

    _print_table(cols, rows)
    nomes = [r[0]      for r in rows]
    qtd   = [int(r[1]) for r in rows]
    _bar(nomes, qtd,
         f"Consultas por Funcionário ({ini} a {fim})",
         "Funcionário (registro)", "Qtd de Consultas",
         f"consultas_por_func_{ini}_{fim}.png")

# -------------------- novas consultas do requisito (3/3) --------------------

def req1_faturamento_mensal_por_convenio():
    """
    Objetivo: Somar o valor das consultas por mês e por convênio e
    exibir também quantos pacientes distintos foram atendidos.
    Tabelas: Consulta, Convenio, Paciente (3)
    """
    ini, fim = _ask_periodo("REQ1 — FATURAMENTO MENSAL POR CONVÊNIO")
    if not ini:
        return

    sql = """
        SELECT
          DATE_FORMAT(c.data_consulta, '%%Y-%%m') AS ano_mes,
          COALESCE(v.nome_convenio, 'Particular') AS nome_convenio,
          SUM(COALESCE(c.valor,0))                AS total_faturado,
          COUNT(DISTINCT c.id_paciente)           AS pacientes_atendidos
        FROM Consulta c
        LEFT JOIN Convenio v ON v.id_convenio = c.id_convenio
        JOIN Paciente p      ON p.id_paciente = c.id_paciente
        WHERE c.data_consulta BETWEEN %s AND %s
        GROUP BY DATE_FORMAT(c.data_consulta, '%%Y-%%m'),
                 COALESCE(v.nome_convenio, 'Particular')
        ORDER BY ano_mes, nome_convenio;
    """
    cols, rows = execute_query(sql, (ini, fim))
    if not rows:
        print("Sem dados no período.\n")
        return

    print("\n[Amostra — Req1]")
    _print_table(cols, rows)

    # Gráfico 1: soma por mês (todos convênios somados)
    by_month = {}
    for r in rows:
        mes   = r[0]
        total = float(r[2] or 0)
        by_month[mes] = by_month.get(mes, 0.0) + total

    labels = list(by_month.keys())
    values = list(by_month.values())
    _bar(labels, values,
         f"Req1: Faturamento Mensal ({ini} a {fim})",
         "Mês (YYYY-MM)", "R$",
         f"req1_faturamento_mensal_{ini}_{fim}.png")

def req2_consultas_receita_por_especialidade():
    """
    Objetivo: Quantidade de consultas e soma de valores por especialidade.
    Tabelas: Especialidade, Medico_Especialidade, Medico, Consulta (4)
    """
    ini, fim = _ask_periodo("REQ2 — CONSULTAS E RECEITA POR ESPECIALIDADE")
    if not ini:
        return

    sql = """
        SELECT
          e.nome_especialidade,
          COUNT(c.id_consulta)     AS qtd_consultas,
          SUM(COALESCE(c.valor,0)) AS total_faturado
        FROM Especialidade e
        JOIN Medico_Especialidade me ON me.id_especialidade = e.id_especialidade
        JOIN Medico m                ON m.id_medico_crm     = me.id_medico_crm
        LEFT JOIN Consulta c         ON c.id_medico_crm     = m.id_medico_crm
                                    AND c.data_consulta BETWEEN %s AND %s
        GROUP BY e.id_especialidade, e.nome_especialidade
        ORDER BY qtd_consultas DESC, total_faturado DESC;
    """
    cols, rows = execute_query(sql, (ini, fim))
    if not rows:
        print("Sem dados no período.\n")
        return

    print("\n[Amostra — Req2]")
    _print_table(cols, rows)

    labels = [r[0]      for r in rows]
    values = [int(r[1]) for r in rows]
    _bar(labels, values,
         f"Req2: Consultas por Especialidade ({ini} a {fim})",
         "Especialidade", "Qtd de Consultas",
         f"req2_consultas_especialidade_{ini}_{fim}.png")

def req3_uso_equipamentos_por_medico():
    """
    Objetivo: Quantas vezes equipamentos foram utilizados em consultas
    (total e nº de tipos distintos) por médico.
    Tabelas: Medico, Consulta, Consulta_Equipamento, Equipamento (4)
    """
    ini, fim = _ask_periodo("REQ3 — USO DE EQUIPAMENTOS POR MÉDICO")
    if not ini:
        return

    sql = """
        SELECT
          m.nome_medico,
          COUNT(*)                          AS usos_equipamentos,
          COUNT(DISTINCT ce.id_equipamento) AS tipos_equip_distintos
        FROM Medico m
        JOIN Consulta c              ON c.id_medico_crm  = m.id_medico_crm
        JOIN Consulta_Equipamento ce ON ce.id_consulta   = c.id_consulta
        JOIN Equipamento e           ON e.id_equipamento = ce.id_equipamento
        WHERE c.data_consulta BETWEEN %s AND %s
        GROUP BY m.id_medico_crm, m.nome_medico
        ORDER BY usos_equipamentos DESC, tipos_equip_distintos DESC, m.nome_medico;
    """
    cols, rows = execute_query(sql, (ini, fim))
    if not rows:
        print("Sem dados no período.\n")
        return

    print("\n[Amostra — Req3]")
    _print_table(cols, rows)

    labels = [r[0]      for r in rows]
    values = [int(r[1]) for r in rows]
    _bar(labels, values,
         f"Req3: Uso de Equipamentos por Médico ({ini} a {fim})",
         "Médico", "Usos de Equipamentos",
         f"req3_uso_equip_por_med_{ini}_{fim}.png")

