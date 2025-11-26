
# ai_assistente.py 

# Universidade Federal De Santa Catarina

# Projeto Final de Banco de Dados

# Nome: Balduino José Da Silva.



import os
import json
import re
import unicodedata
import requests
from datetime import datetime
from dotenv import load_dotenv

from db import execute_query, execute_dml  

load_dotenv()
OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL    = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

WHITELIST_TABLES = {
    "Funcionario", "Doenca", "Especialidade", "Medico", "Convenio",
    "Clinica_Parceira", "Equipamento", "Tipo_Exame", "Medicamento",
    "Paciente", "Consulta", "Medico_Especialidade", "Paciente_Doenca",
    "Consulta_Exame", "Consulta_Equipamento", "Prescricao",
    "Encaminhamento", "SugestaoIA", "relatorio_ia"
}

# ---------- utilidades de texto ----------

def _strip_accents_lower(s: str) -> str:
    if not isinstance(s, str): return s
    s = s.lower()
    s = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in s if unicodedata.category(ch) != "Mn")

def _clean_user_sql(s: str) -> str:
    """Remove cercas de código e prefixos 'sql\\n'."""
    s = s.strip()
    
   
    
    if s.startswith("```"):
        s = s.strip("`").strip()
        
      
        
        if s.splitlines() and _strip_accents_lower(s.splitlines()[0]) == "sql":
            s = "\n".join(s.splitlines()[1:])
            
  
    
    if _strip_accents_lower(s).startswith("sql\n"):
        s = s.split("\n", 1)[1]
    return s.strip()

# ---------- introspecção de schema ----------

def _schema_snapshot():
    sql = """
    SELECT TABLE_NAME, COLUMN_NAME
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
    """
    _, rows = execute_query(sql)
    schema = {}
    for t, c in rows:
        if t in WHITELIST_TABLES:
            schema.setdefault(t, set()).add(c)
    return schema

def _table_exists(schema, tname: str) -> bool:
    return tname in schema

def _col_exists(schema, tname: str, col: str) -> bool:
    return _table_exists(schema, tname) and (col in schema[tname])




def _is_safe_select(user_sql: str) -> bool:
    s = _clean_user_sql(user_sql)

   
    
    if not s[:6].lower() == "select":
        return False

    # sem múltiplas instruções; permite ; apenas ao final
    
    body = s[:-1] if s.endswith(";") else s
    if ";" in body:
        return False

  
    
    s_low = s.lower()
    if "--" in s_low or "/*" in s_low or "#" in s_low:
        return False

    # bloquear palavras de escrita/DDL
    
    banned = (" insert ", " update ", " delete ", " drop ", " alter ",
              " create ", " truncate ", " grant ", " revoke ", " replace ", " call ", " do ")
    wrapped = " " + s_low + " "
    return not any(b in wrapped for b in banned)

# ---------- padrões auxiliares ----------

_ano_re   = re.compile(r"\b(20\d{2}|19\d{2})\b")
_data_re  = re.compile(r"\d{4}-\d{2}-\d{2}")
_num_re   = re.compile(r"\b\d+\b")

def _datas_na_pergunta(q: str):
    datas = _data_re.findall(q)
    return datas[:2] if len(datas) >= 2 else (None, None)

def _ano_na_pergunta(q: str):
    m = _ano_re.search(q)
    return m.group(1) if m else None

def _numero_na_pergunta(q: str, default=None):
    m = _num_re.findall(q)
    if m:
        try: return int(m[0])
        except: pass
    return default

# ---------- mapeamento de intents ----------

def _guess_intent_to_sql(question: str, schema):
    q_raw = question.strip()
    q = _strip_accents_lower(q_raw)

    # normalizações/sinnimos
    
    q = q.replace("clinica", "clinica")
    q = q.replace("convenio", "convênio")  
    nome_tbl = {
        "medicos": "Medico", "medico": "Medico",
        "pacientes": "Paciente", "paciente": "Paciente",
        "funcionarios": "Funcionario", "funcionario": "Funcionario",
        "convenios": "Convenio", "convenio": "Convenio",
        "consultas": "Consulta", "consulta": "Consulta",
        "equipamentos": "Equipamento", "equipamento": "Equipamento",
        "exames": "Tipo_Exame", "tipo de exame": "Tipo_Exame", "tipo_exame": "Tipo_Exame",
        "clinica_parceira": "Clinica_Parceira", "clinicas parceiras": "Clinica_Parceira",
        "doencas": "Doenca", "doenca": "Doenca",
        "prescricoes": "Prescricao", "prescricao": "Prescricao",
        "encaminhamentos": "Encaminhamento", "encaminhamento": "Encaminhamento",
    }

    # -------- intents específicas úteis no seu trabalho --------

    # Faturamento total (todas datas)
    
    if "faturamento" in q and ("ate agora" in q or "total" in q or "geral" in q):
        return ("Soma dos valores de todas as consultas.", 
                "SELECT SUM(COALESCE(valor,0)) AS faturamento_total FROM Consulta")

    # Faturamento mensal no ano "YYYY"
    
    if "faturamento mensal" in q:
        ano = _ano_na_pergunta(q) or "YEAR(CURDATE())"
        return (f"Faturamento por mês no ano {ano}.",
                "SELECT DATE_FORMAT(data_consulta, '%Y-%m') AS ano_mes, "
                "       SUM(COALESCE(valor,0)) AS total "
                "FROM Consulta "
                f"WHERE YEAR(data_consulta) = {ano} "
                "GROUP BY DATE_FORMAT(data_consulta, '%Y-%m') "
                "ORDER BY DATE_FORMAT(data_consulta, '%Y-%m')")

    # Faturamento por dia em um período (se a pergunta tiver duas datas)
    
    if "faturamento" in q and ("entre" in q or "no periodo" in q or "no período" in q):
        ini, fim = _datas_na_pergunta(q)
        if ini and fim:
            return (f"Faturamento (soma de valor) por dia entre {ini} e {fim}.",
                    "SELECT DATE(data_consulta) AS dia, "
                    "       SUM(COALESCE(valor,0)) AS total "
                    "FROM Consulta "
                    f"WHERE data_consulta BETWEEN '{ini}' AND '{fim}' "
                    "GROUP BY DATE(data_consulta) "
                    "ORDER BY DATE(data_consulta)")

    # Total de consultas
    
    if "quantas consultas" in q or "numero de consultas" in q or "total de consultas" in q:
        return ("Conta de linhas na tabela Consulta.",
                "SELECT COUNT(*) AS total_consultas FROM Consulta")

    # Total de pacientes
    
    if "quantos pacientes" in q or "numero de pacientes" in q or "total de pacientes" in q:
        return ("Conta de linhas na tabela Paciente.",
                "SELECT COUNT(*) AS total_pacientes FROM Paciente")

    # Total de médicos
    
    if "quantos medicos" in q or "quantos médicos" in q or "total de medicos" in q:
        return ("Conta de linhas na tabela Medico.",
                "SELECT COUNT(*) AS total_medicos FROM Medico")

    # Consultas entre datas
    
    if "consultas entre" in q and " e " in q:
        ini, fim = _datas_na_pergunta(q)
        if ini and fim:
            try:
                datetime.strptime(ini, "%Y-%m-%d")
                datetime.strptime(fim, "%Y-%m-%d")
                return (f"Consultas entre {ini} e {fim}.",
                        "SELECT id_consulta, id_paciente, id_medico_crm, data_consulta, valor "
                        "FROM Consulta "
                        f"WHERE data_consulta BETWEEN '{ini}' AND '{fim}' "
                        "ORDER BY data_consulta")
            except Exception:
                pass

    # Consultas por convênio (qtd e total)
    
    if "consultas por convenio" in q or "consultas por convênio" in q or "por convenio" in q:
        return ("Agrupa consultas por convênio (NULL = Particular).",
                "SELECT COALESCE(cv.nome_convenio,'Particular') AS convenio, "
                "       COUNT(*) AS qtd, SUM(COALESCE(c.valor,0)) AS total "
                "FROM Consulta c "
                "LEFT JOIN Convenio cv ON cv.id_convenio = c.id_convenio "
                "GROUP BY COALESCE(cv.nome_convenio,'Particular') "
                "ORDER BY total DESC")

    # Consultas por médico (qtd e total)
    
    if "consultas por medico" in q or "consultas por médico" in q or "por medico" in q:
        return ("Agrupa consultas por médico.",
                "SELECT m.nome_medico, COUNT(*) AS qtd, SUM(COALESCE(c.valor,0)) AS total "
                "FROM Consulta c "
                "JOIN Medico m ON m.id_medico_crm = c.id_medico_crm "
                "GROUP BY m.nome_medico "
                "ORDER BY qtd DESC, m.nome_medico")

    # Consultas por funcionário (registro)
    
    if "consultas por funcionario" in q or "consultas por funcionário" in q:
        return ("Agrupa consultas pelo funcionário que registrou.",
                "SELECT f.nome_funcionario, COUNT(*) AS qtd "
                "FROM Funcionario f "
                "LEFT JOIN Consulta c ON c.id_func_registro = f.id_funcionario "
                "GROUP BY f.id_funcionario, f.nome_funcionario "
                "ORDER BY qtd DESC, f.nome_funcionario")

    # Médicos sem consultas
    if "medicos sem consultas" in q or "médicos sem consultas" in q:
        return ("Lista médicos sem qualquer consulta.",
                "SELECT m.id_medico_crm, m.nome_medico "
                "FROM Medico m "
                "LEFT JOIN Consulta c ON c.id_medico_crm = m.id_medico_crm "
                "WHERE c.id_medico_crm IS NULL "
                "ORDER BY m.nome_medico")

    # Pacientes e suas doenças
    if "pacientes com doencas" in q or "pacientes e suas doencas" in q:
        return ("Lista pacientes e (se houver) suas doenças.",
                "SELECT p.id_paciente, p.nome, d.nome_doenca "
                "FROM Paciente p "
                "LEFT JOIN Paciente_Doenca pd ON pd.id_paciente = p.id_paciente "
                "LEFT JOIN Doenca d ON d.id_doenca = pd.id_doenca "
                "ORDER BY p.nome")

    # Consultas por equipamento
    if "consultas por equipamento" in q or "equipamentos por consulta" in q or "consultas e equipamentos" in q:
        return ("Lista consultas e seus equipamentos vinculados.",
                "SELECT c.id_consulta, c.data_consulta, e.nome_equipamento "
                "FROM Consulta c "
                "JOIN Consulta_Equipamento ce ON ce.id_consulta = c.id_consulta "
                "JOIN Equipamento e ON e.id_equipamento = ce.id_equipamento "
                "ORDER BY c.data_consulta DESC")

    # Top N médicos por quantidade de consultas
    if "top" in q and ("medicos" in q or "médicos" in q):
        n = _numero_na_pergunta(q, default=5)
        return (f"Top {n} médicos por número de consultas.",
                "SELECT m.nome_medico, COUNT(*) AS qtd "
                "FROM Consulta c "
                "JOIN Medico m ON m.id_medico_crm = c.id_medico_crm "
                "GROUP BY m.nome_medico "
                f"ORDER BY qtd DESC LIMIT {n}")

    # Últimas consultas
    if "ultimas consultas" in q or "últimas consultas" in q:
        n = _numero_na_pergunta(q, default=10)
        return (f"Últimas {n} consultas por data.",
                "SELECT id_consulta, id_paciente, id_medico_crm, data_consulta, valor "
                "FROM Consulta "
                "ORDER BY data_consulta DESC, id_consulta DESC "
                f"LIMIT {n}")

    # ---------- fallbacks genéricos úteis ----------

    # “listar <tabela>”
    if q.startswith("listar "):
        alvo = q.replace("listar ", "").strip()
        tname = nome_tbl.get(alvo, None)
        if tname and _table_exists(schema, tname):
            # pega até 50 para segurança
            # escolhe algumas colunas comuns se existirem
            cols = list(schema[tname])
            cols_sel = ", ".join(cols[:6]) if cols else "*"
            return (f"Lista de {tname} (até 50).",
                    f"SELECT {cols_sel} FROM {tname} LIMIT 50")

    # “contar <tabela>”
    if q.startswith("contar ") or q.startswith("quantos "):
        alvo = q.replace("contar ", "").replace("quantos ", "").strip()
        tname = nome_tbl.get(alvo, None)
        if tname and _table_exists(schema, tname):
            return (f"Total de linhas em {tname}.",
                    f"SELECT COUNT(*) AS total FROM {tname}")

    # “colunas de <tabela> / esquema de <tabela>”
    if "colunas de " in q or "esquema de " in q or "descricao de " in q or "descrição de " in q:
        alvo = q.split(" de ", 1)[1].strip() if " de " in q else ""
        tname = nome_tbl.get(alvo, None)
        if tname and _table_exists(schema, tname):
            return (f"Colunas de {tname} a partir do information_schema.",
                    "SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_KEY "
                    "FROM information_schema.COLUMNS "
                    f"WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = '{tname}' "
                    "ORDER BY ORDINAL_POSITION")

    # Se usuário colou um SELECT direto
    cleaned = _clean_user_sql(q_raw)
    if cleaned.lower().startswith("select"):
        return ("Consulta fornecida pelo usuário.", cleaned)

    return (None, None)

# ---------- execução: Perguntar ao banco ----------

def _pretty_print(cols, rows):
    if not rows:
        print("\n(nenhum registro)\n")
        return
    widths = [max(len(str(c)), max(len(str(r[i])) for r in rows)) for i, c in enumerate(cols)]
    sep = "+" + "+".join("-"*(w+2) for w in widths) + "+"
    header = "|" + "|".join(" " + str(c).ljust(w) + " " for c, w in zip(cols, widths)) + "|"
    print("\n" + sep)
    print(header)
    print(sep)
    for r in rows:
        print("|" + "|".join(" " + str(v).ljust(w) + " " for v, w in zip(r, widths)) + "|")
    print(sep + "\n")

def perguntar_ao_banco():
    """
    Recebe a pergunta, mapeia ou aceita SELECT (único), valida e EXECUTA de imediato.
    """
    print("\n=== ASSISTENTE SQL (IA) — Somente Leitura ===")
    print("Exemplos:")
    print('- "Qual foi o faturamento da clínica até agora?"')
    print('- "Faturamento mensal em 2025"')
    print('- "Consultas entre 2025-01-01 e 2025-12-31"')
    print('- "Consultas por convênio"')
    print('- "Top 5 médicos" / "Últimas 10 consultas"')
    print('- "Listar pacientes" / "Contar consultas"')
    print('- "Colunas de Consulta"')
    print('- Ou cole um SELECT (apenas leitura).')

    pergunta = input("\nPergunta: ").strip()
    if not pergunta:
        print("Pergunta vazia.\n"); return

    schema = _schema_snapshot()
    explicacao, sql = _guess_intent_to_sql(pergunta, schema)

    if not sql:
        print("\nNão entendi ainda. Tente algo como:")
        print("- Qual foi o faturamento da clínica até agora?")
        print("- Faturamento mensal em 2025")
        print("- Consultas entre 2025-01-01 e 2025-12-31")
        print("- Consultas por convênio / por médico / por funcionário")
        print("- Top 5 médicos / Últimas 10 consultas")
        print("- Listar pacientes / Contar consultas")
        print("- Colunas de Consulta\n")
        return

    if not _is_safe_select(sql):
        print("\n[ERRO] OBS A consulta precisa ser um único SELECT, sem DDL/DML, sem múltiplas instruções ou comentários.\n")
        print("SQL detectada:\n" + sql + "\n")
        return

    print("\n--- Plano da IA ---")
    print(f"Explicação: {explicacao}")
    print("SQL que será executada:")
    print(sql)

    try:
        cols, rows = execute_query(sql)
        _pretty_print(cols, rows)
    except Exception as e:
        print(f"\nFalha ao executar a consulta: {e}\n")

# ---------- caso clínico (sem alterações de lógica de segurança) ----------

def _assert_api_key():
    if not OPENAI_API_KEY:
        raise RuntimeError(
            "Variável de ambiente OPENAI_API_KEY não definida."
        )

def _chat_completion(messages, temperature=0.2, max_tokens=800):
    _assert_api_key()
    url = f"{OPENAI_BASE_URL}/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": OPENAI_MODEL, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}

    resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
    if resp.status_code == 404:
        raise RuntimeError("404 ao chamar /v1/chat/completions. Verifique OPENAI_BASE_URL.")
    if resp.status_code == 429:
        raise RuntimeError("429 Too Many Requests. Limite/cota excedida.")
    if not resp.ok:
        raise RuntimeError(f"Erro HTTP {resp.status_code}: {resp.text}")

    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        raise RuntimeError(f"Resposta inesperada da API: {data}")

def sugestao_para_caso_clinico():
    print("\n=== ASSISTENTE IA – SUGESTÃO PARA CASO CLÍNICO ===")
    id_paciente = input("ID do paciente (enter se não quiser informar): ").strip() or None
    id_consulta = input("ID da consulta (enter se não quiser informar): ").strip() or None

    print("\nDescreva o caso do paciente (sintomas, histórico, etc.).")
    print("Finalize com uma linha em branco.\n")

    linhas = []
    while True:
        linha = input()
        if not linha:
            break
        linhas.append(linha)
    descricao = "\n".join(linhas).strip()
    if not descricao:
        print("\nDescrição vazia. Operação cancelada.\n")
        return

    system_prompt = (
        "Você é um assistente clínico que sugere, de forma sucinta e organizada, "
        "especialidades recomendadas, exames iniciais, diagnósticos diferenciais e "
        "orientações gerais. Não faça prescrições específicas nem diagnósticos definitivos."
    )
    user_prompt = (
        f"Caso: {descricao}\n\n"
        "Retorne em 4 blocos numerados: (1) Especialidades, (2) Exames, "
        "(3) Diferenciais, (4) Orientações."
    )
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user",    "content": user_prompt}]

    try:
        resposta = _chat_completion(messages, temperature=0.2, max_tokens=700)
    except Exception as e:
        print(f"\nErro ao chamar modelo de IA: {e}\n")
        return

    print("\n=== RESPOSTA DA IA ===\n")
    print(resposta)
    print("\n======================\n")

    sql = """
        INSERT INTO SugestaoIA (id_paciente, id_consulta, texto_pergunta, resposta_ia)
        VALUES (%s, %s, %s, %s)
    """
    try:
        execute_dml(sql, (id_paciente, id_consulta, descricao, resposta))
        print("Sugestão da IA registrada na tabela SugestaoIA.")
    except Exception as e:
        print(f"Falha ao salvar no banco: {e}")
