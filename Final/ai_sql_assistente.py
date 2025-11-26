

import os
import json
import re
import requests
from textwrap import dedent
from db import execute_query

# ==== CONFIG ====

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini") 

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}" if OPENAI_API_KEY else "",
    "Content-Type": "application/json",
}



SCHEMA_HINT = dedent("""
Base: clinica

Tabela Funcionario(
  id_funcionario INT PK,
  nome_funcionario VARCHAR(100) NOT NULL,
  data_admissao DATE,
  cargo VARCHAR(50),
  cpf VARCHAR(14),
  telefone VARCHAR(20),
  email VARCHAR(100)
)

Tabela Doenca(
  id_doenca INT PK,
  nome_doenca VARCHAR(100) NOT NULL
)

Tabela Especialidade(
  id_especialidade INT PK,
  nome_especialidade VARCHAR(100) NOT NULL
)

Tabela Medico(
  id_medico_crm VARCHAR(20) PK,
  nome_medico VARCHAR(100) NOT NULL,
  telefone VARCHAR(20)
)

Tabela Convenio(
  id_convenio INT PK,
  nome_convenio VARCHAR(100) NOT NULL,
  cobertura VARCHAR(200),
  tipo_convenio VARCHAR(50)
)

Tabela Clinica_Parceira(
  id_clinica INT PK,
  nome_clinica VARCHAR(100) NOT NULL
)

Tabela Equipamento(
  id_equipamento INT PK,
  nome_equipamento VARCHAR(100) NOT NULL
)

Tabela Tipo_Exame(
  id_exame INT PK,
  nome_exame VARCHAR(100) NOT NULL,
  resultado_exame VARCHAR(255)
)

Tabela Medicamento(
  id_medicamento INT PK,
  nome_medicamento VARCHAR(100) NOT NULL
)

Tabela Paciente(
  id_paciente INT PK,
  nome VARCHAR(100) NOT NULL,
  data_nascimento DATE,
  telefone VARCHAR(20),
  email VARCHAR(100),
  cpf VARCHAR(14),
  endereco VARCHAR(200),
  id_func_atendimento INT FK -> Funcionario(id_funcionario)
)

Tabela Consulta(
  id_consulta INT PK,
  id_paciente INT NOT NULL FK -> Paciente(id_paciente),
  id_medico_crm VARCHAR(20) NOT NULL FK -> Medico(id_medico_crm),
  id_func_registro INT NOT NULL FK -> Funcionario(id_funcionario),
  id_convenio INT NULL FK -> Convenio(id_convenio),
  data_consulta DATE NOT NULL,
  valor DECIMAL(10,2),
  observacao VARCHAR(255)
)

Tabela Medico_Especialidade(
  id_medico_crm VARCHAR(20) FK -> Medico(id_medico_crm),
  id_especialidade INT FK -> Especialidade(id_especialidade),
  PK (id_medico_crm, id_especialidade)
)

Tabela Paciente_Doenca(
  id_paciente INT FK -> Paciente(id_paciente),
  id_doenca INT FK -> Doenca(id_doenca),
  PK (id_paciente, id_doenca)
)

Tabela Consulta_Exame(
  id_consulta INT FK -> Consulta(id_consulta),
  id_exame INT FK -> Tipo_Exame(id_exame),
  PK (id_consulta, id_exame)
)

Tabela Consulta_Equipamento(
  id_consulta INT FK -> Consulta(id_consulta),
  id_equipamento INT FK -> Equipamento(id_equipamento),
  PK (id_consulta, id_equipamento)
)

Tabela Prescricao(
  id_consulta INT FK -> Consulta(id_consulta),
  id_medicamento INT FK -> Medicamento(id_medicamento),
  posologia VARCHAR(200),
  quantidade VARCHAR(50),
  PK (id_consulta, id_medicamento)
)

Tabela Encaminhamento(
  id_encaminhamento INT PK,
  id_funcionario INT NOT NULL FK -> Funcionario(id_funcionario),
  id_clinica INT NOT NULL FK -> Clinica_Parceira(id_clinica),
  data_encaminhamento DATE,
  observacao VARCHAR(255)
)

Tabela SugestaoIA(
  id_sugestao INT PK,
  id_paciente INT NULL FK -> Paciente(id_paciente),
  id_consulta INT NULL FK -> Consulta(id_consulta),
  texto_pergunta VARCHAR(2000) NOT NULL,
  resposta_ia TEXT NOT NULL,
  criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
)

Tabela relatorio_ia(
  id INT PK,
  id_paciente INT NULL FK -> Paciente(id_paciente),
  id_consulta INT NULL FK -> Consulta(id_consulta),
  descricao TEXT NOT NULL,
  resposta_ia TEXT NOT NULL,
  data_registro DATETIME DEFAULT CURRENT_TIMESTAMP
)
""").strip()


def _assert_key():
    if not OPENAI_API_KEY:
        raise RuntimeError("Variável de ambiente OPENAI_API_KEY não definida.")


def _call_openai_json(user_question: str) -> dict:
    """
    Pede ao modelo para responder com JSON contendo:
      - sql: SELECT seguro, aderente ao schema
      - explicacao: breve explicação do raciocínio
      - observacoes: notas (ex.: necessidades de filtro por data)
    """
    _assert_key()
    system = dedent(f"""
    Você é um gerador de SQL somente-LEITURA para MySQL.

    REGRAS:
    - Sempre devolver **apenas** SELECTs válidos para o schema abaixo.
    - Nunca gerar INSERT, UPDATE, DELETE, DROP, TRUNCATE, ALTER ou CREATE.
    - Use nomes de tabelas e colunas exatamente como no schema.
    - Se pedir "dentista", interprete como especialidade 'Dentista' ou 'Odontologia' via tabelas Especialidade e Medico_Especialidade.
    - Se pedirem "médicos sem agendamento", use Medico LEFT JOIN Consulta filtrando onde Consulta.id_consulta IS NULL.
    - Se o pedido for ambíguo, escolha uma interpretação razoável e mencione em 'observacoes'.

    Responda ESTRITAMENTE em JSON no formato:
    {{
      "sql": "<SQL SELECT ou vazio se não aplicável>",
      "explicacao": "<texto curto em PT-BR>",
      "observacoes": "<texto curto em PT-BR>"
    }}

    SCHEMA:
    {SCHEMA_HINT}
    """).strip()

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user_question},
        ],
        "temperature": 0.0,
        "max_tokens": 600,
        "response_format": {"type": "json_object"},
    }
    resp = requests.post(f"{OPENAI_BASE_URL}/chat/completions",
                         headers=HEADERS, data=json.dumps(payload), timeout=60)
    if not resp.ok:
        if resp.status_code == 404:
            raise RuntimeError("404 em /chat/completions. Verifique OPENAI_BASE_URL.")
        if resp.status_code == 429:
            raise RuntimeError("429 Too Many Requests (limite/cota).")
        raise RuntimeError(f"Erro HTTP {resp.status_code}: {resp.text}")

    data = resp.json()
    content = data["choices"][0]["message"]["content"]
    try:
        return json.loads(content)
    except Exception:
        # fallback: tentar extrair bloco JSON bruto
        m = re.search(r"\{.*\}", content, flags=re.S)
        if not m:
            raise RuntimeError(f"Resposta inesperada da API: {content}")
        return json.loads(m.group(0))


def _is_select_only(sql: str) -> bool:
    """Bloqueia comandos perigosos; permite só SELECT."""
    if not sql:
        return False
    forbidden = ("INSERT", "UPDATE", "DELETE", "DROP", "TRUNCATE", "ALTER", "CREATE")
    upper = sql.upper()
    if not upper.strip().startswith("SELECT"):
        return False
    return not any(tok in upper for tok in forbidden)


def _print_table(cols, rows):
    if not rows:
        print("\n(nenhum registro)\n")
        return
    # largura simples
    widths = [max(len(str(c)), *(len(str(r[i])) for r in rows)) for i, c in enumerate(cols)]
    line = "+".join("-" * (w + 2) for w in widths)
    print("\n" + line)
    print("| " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(cols)) + " |")
    print(line)
    for r in rows:
        print("| " + " | ".join(str(r[i]).ljust(widths[i]) for i in range(len(cols))) + " |")
    print(line + "\n")


def _fallback_sql(user_question: str) -> str | None:
    """Regras manuais para perguntas comuns quando o modelo não retornar SQL."""
    q = user_question.lower()

    # "médico dentista"
    if "dentist" in q or "odontolog" in q or "dentista" in q:
        return dedent("""
        SELECT m.id_medico_crm, m.nome_medico, m.telefone, e.nome_especialidade
        FROM Medico m
        JOIN Medico_Especialidade me ON me.id_medico_crm = m.id_medico_crm
        JOIN Especialidade e ON e.id_especialidade = me.id_especialidade
        WHERE e.nome_especialidade LIKE '%Dentist%' OR e.nome_especialidade LIKE '%Odontolog%' OR e.nome_especialidade LIKE '%Dentista%';
        """).strip()

    # "médicos sem agendamentos"
    if ("sem agend" in q) or ("sem consulta" in q) or ("sem atendimento" in q):
        return dedent("""
        SELECT m.id_medico_crm, m.nome_medico, m.telefone
        FROM Medico m
        LEFT JOIN Consulta c ON c.id_medico_crm = m.id_medico_crm
        WHERE c.id_consulta IS NULL
        ORDER BY m.nome_medico;
        """).strip()

    return None


def assistente_sql_clinica():
    print("\n=== ASSISTENTE SQL (IA) ===")
    print("Pergunte algo sobre o banco (apenas leitura).")
    print("Exemplos:")
    print("- \"Qual é o nome do médico dentista?\"")
    print("- \"Quais médicos não possuem agendamentos?\"")
    print("- \"Quantas consultas houve em 2025 por médico?\"\n")

    pergunta = input("Pergunta: ").strip()
    if not pergunta:
        print("Pergunta vazia. Cancelado.\n")
        return

    try:
        result = _call_openai_json(pergunta)
    except Exception as e:
        print(f"\nFalha ao gerar SQL pela IA: {e}")
        # tenta fallback
        sql_fb = _fallback_sql(pergunta)
        if not sql_fb:
            print("Sem fallback aplicável.\n")
            return
        print("\n[Fallback aplicado]\nSQL gerado:\n", sql_fb)
        if not _is_select_only(sql_fb):
            print("\nO SQL gerado não é apenas SELECT. Abortado por segurança.\n")
            return
        cols, rows = execute_query(sql_fb)
        _print_table(cols, rows)
        return

    sql = (result.get("sql") or "").strip()
    explicacao = (result.get("explicacao") or "").strip()
    observacoes = (result.get("observacoes") or "").strip()

    if not sql:
        # tenta fallback
        sql_fb = _fallback_sql(pergunta)
        if not sql_fb:
            print("\nA IA não retornou SQL. Tente reformular a pergunta.\n")
            return
        sql = sql_fb
        print("\n[Fallback aplicado]\n")

    print("\n--- Plano da IA ---")
    if explicacao:
        print("Explicação:", explicacao)
    if observacoes:
        print("Obs.:", observacoes)
    print("SQL:", sql, "\n")

    if not _is_select_only(sql):
        print("O SQL não é apenas SELECT. Operação bloqueada por segurança.\n")
        return

    try:
        cols, rows = execute_query(sql)
    except Exception as e:
        print(f"Erro ao executar SQL: {e}\n")
        return

    _print_table(cols, rows)
