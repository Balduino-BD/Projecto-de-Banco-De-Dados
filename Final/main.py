

# main.py

# Universidade Federal De Santa Catarina

# Projeto Final de Banco de Dados

# Nome: Balduino José Da Silva

from ai_assistente import (
    sugestao_para_caso_clinico,
    perguntar_ao_banco,          
)

from relatorios import (
    total_consultas_periodo,
    faturamento_mensal_periodo,
    consultas_por_medico_periodo,
    medicos_sem_consultas_no_periodo,
    consultas_por_funcionario_periodo,    
    req1_faturamento_mensal_por_convenio,
    req2_consultas_receita_por_especialidade,
    req3_uso_equipamentos_por_medico,
)

from setup_db import (
    criar_apenas_tabelas,
    criar_tabelas_e_carga,
    apagar_todas_tabelas,
)

from operacoes_entidades import (
    
    # Paciente
    
    inserir_paciente, listar_pacientes, atualizar_paciente, excluir_paciente,
    
    # Medico
    
    inserir_medico, listar_medicos, atualizar_medico, excluir_medico,
    
    # Funcionario
    
    inserir_funcionario, listar_funcionarios, atualizar_funcionario, excluir_funcionario,
    
    # Consulta
    
    inserir_consulta, listar_consultas, atualizar_consulta, excluir_consulta,
    vincular_exame_a_consulta, listar_exames_da_consulta,
    
    # Tipo_Exame
    
    inserir_exame, listar_exames, excluir_exame,
    
    # Prescricao
    
    inserir_prescricao, listar_prescricoes, excluir_prescricao,
    
    # Encaminhamento
    
    inserir_encaminhamento, listar_encaminhamentos, excluir_encaminhamento,
    
    # Clínica Parceira
    
    inserir_clinica, listar_clinicas, atualizar_clinica, excluir_clinica,
    
    # Convênio
    
    inserir_convenio, listar_convenios, atualizar_convenio, excluir_convenio,
    
    # Especialidade
    
    inserir_especialidade, listar_especialidades, vincular_especialidade_medico, listar_medico_especialidades,
    
    # Equipamento
    
    inserir_equipamento, listar_equipamentos, atualizar_equipamento, excluir_equipamento,
    
    # Doença
    
    inserir_doenca, listar_doencas, atualizar_doenca, excluir_doenca,
    
    # Histórico IA
    
    listar_sugestoes_ia,
)

# ============================= CRIAÇÂO DOS MENUS PARCIALMENTE =============================

def menu_paciente():
    while True:
        print("\n--- MENU PACIENTE ---")
        print("1 - Inserir paciente")
        print("2 - Listar pacientes")
        print("3 - Atualizar paciente")
        print("4 - Excluir paciente")
        print("0 - Voltar")
        op = input("Opção: ").strip()
        if op == "1": inserir_paciente()
        elif op == "2": listar_pacientes()
        elif op == "3": atualizar_paciente()
        elif op == "4": excluir_paciente()
        elif op == "0": break
        else: print("Opção inválida")

def menu_medico():
    while True:
        print("\n--- MENU MÉDICO ---")
        print("1 - Inserir médico")
        print("2 - Listar médicos")
        print("3 - Atualizar médico")
        print("4 - Excluir médico")
        print("0 - Voltar")
        op = input("Opção: ").strip()
        if op == "1": inserir_medico()
        elif op == "2": listar_medicos()
        elif op == "3": atualizar_medico()
        elif op == "4": excluir_medico()
        elif op == "0": break
        else: print("Opção inválida")

def menu_funcionario():
    while True:
        print("\n--- MENU FUNCIONÁRIO ---")
        print("1 - Inserir funcionário")
        print("2 - Listar funcionários")
        print("3 - Atualizar funcionário")
        print("4 - Excluir funcionário")
        print("0 - Voltar")
        op = input("Opção: ").strip()
        if op == "1": inserir_funcionario()
        elif op == "2": listar_funcionarios()
        elif op == "3": atualizar_funcionario()
        elif op == "4": excluir_funcionario()
        elif op == "0": break
        else: print("Opção inválida")

def menu_consulta():
    while True:
        print("\n--- MENU CONSULTA ---")
        print("1 - Inserir consulta")
        print("2 - Listar consultas")
        print("3 - Atualizar consulta")
        print("4 - Excluir consulta")
        print("5 - Vincular exame a consulta")
        print("6 - Listar exames de uma consulta")
        print("0 - Voltar")
        op = input("Opção: ").strip()
        if op == "1": inserir_consulta()
        elif op == "2": listar_consultas()
        elif op == "3": atualizar_consulta()
        elif op == "4": excluir_consulta()
        elif op == "5": vincular_exame_a_consulta()
        elif op == "6": listar_exames_da_consulta()
        elif op == "0": break
        else: print("Opção inválida")

def menu_exame():
    while True:
        print("\n--- MENU TIPO DE EXAME ---")
        print("1 - Inserir tipo de exame")
        print("2 - Listar tipos de exame")
        print("3 - Excluir tipo de exame")
        print("0 - Voltar")
        op = input("Opção: ").strip()
        if op == "1": inserir_exame()
        elif op == "2": listar_exames()
        elif op == "3": excluir_exame()
        elif op == "0": break
        else: print("Opção inválida")

def menu_prescricao():
    while True:
        print("\n--- MENU PRESCRIÇÃO ---")
        print("1 - Inserir prescrição")
        print("2 - Listar prescrições")
        print("3 - Excluir prescrição")
        print("0 - Voltar")
        op = input("Opção: ").strip()
        if op == "1": inserir_prescricao()
        elif op == "2": listar_prescricoes()
        elif op == "3": excluir_prescricao()
        elif op == "0": break
        else: print("Opção inválida")

def menu_encaminhamento():
    while True:
        print("\n--- MENU ENCAMINHAMENTO ---")
        print("1 - Inserir encaminhamento")
        print("2 - Listar encaminhamentos")
        print("3 - Excluir encaminhamento")
        print("0 - Voltar")
        op = input("Opção: ").strip()
        if op == "1": inserir_encaminhamento()
        elif op == "2": listar_encaminhamentos()
        elif op == "3": excluir_encaminhamento()
        elif op == "0": break
        else: print("Opção inválida")

def menu_clinica():
    while True:
        print("\n--- MENU CLÍNICA PARCEIRA ---")
        print("1 - Inserir clínica")
        print("2 - Listar clínicas")
        print("3 - Atualizar clínica")
        print("4 - Excluir clínica")
        print("0 - Voltar")
        op = input("Opção: ").strip()
        if op == "1": inserir_clinica()
        elif op == "2": listar_clinicas()
        elif op == "3": atualizar_clinica()
        elif op == "4": excluir_clinica()
        elif op == "0": break
        else: print("Opção inválida")

def menu_convenio():
    while True:
        print("\n--- MENU CONVÊNIO ---")
        print("1 - Inserir convênio")
        print("2 - Listar convênios")
        print("3 - Atualizar convênio")
        print("4 - Excluir convênio")
        print("0 - Voltar")
        op = input("Opção: ").strip()
        if op == "1": inserir_convenio()
        elif op == "2": listar_convenios()
        elif op == "3": atualizar_convenio()
        elif op == "4": excluir_convenio()
        elif op == "0": break
        else: print("Opção inválida")

def menu_especialidade():
    while True:
        print("\n--- MENU ESPECIALIDADE ---")
        print("1 - Inserir especialidade")
        print("2 - Listar especialidades")
        print("3 - Vincular especialidade a médico")
        print("4 - Listar médico ↔ especialidades")
        print("0 - Voltar")
        op = input("Opção: ").strip()
        if op == "1": inserir_especialidade()
        elif op == "2": listar_especialidades()
        elif op == "3": vincular_especialidade_medico()
        elif op == "4": listar_medico_especialidades()
        elif op == "0": break
        else: print("Opção inválida")

def menu_equipamento():
    while True:
        print("\n--- MENU EQUIPAMENTOS ---")
        print("1 - Inserir equipamento")
        print("2 - Listar equipamentos")
        print("3 - Atualizar equipamento")
        print("4 - Excluir equipamento")
        print("0 - Voltar")
        op = input("Opção: ").strip()
        if op == "1": inserir_equipamento()
        elif op == "2": listar_equipamentos()
        elif op == "3": atualizar_equipamento()
        elif op == "4": excluir_equipamento()
        elif op == "0": break
        else: print("Opção inválida")

def menu_doenca():
    while True:
        print("\n--- MENU DOENÇAS ---")
        print("1 - Inserir doença")
        print("2 - Listar doenças")
        print("3 - Atualizar doença")
        print("4 - Excluir doença")
        print("0 - Voltar")
        op = input("Opção: ").strip()
        if op == "1": inserir_doenca()
        elif op == "2": listar_doencas()
        elif op == "3": atualizar_doenca()
        elif op == "4": excluir_doenca()
        elif op == "0": break
        else: print("Opção inválida")

def menu_relatorios():
    while True:
        print("\n--- RELATÓRIOS ---")
        print("1 - Total de consultas por dia (período)")
        print("2 - Faturamento mensal (período)")
        print("3 - Consultas por médico (período)")
        print("4 - Médicos sem consultas (período)")
        print("5 - Consultas por funcionário (período)")
        print("6 - [REQ1] Faturamento mensal por convênio")
        print("7 - [REQ2] Consultas e receita por especialidade")
        print("8 - [REQ3] Uso de equipamentos por médico")
        print("0 - Voltar")
        op = input("Opção: ").strip()

        if op == "1": total_consultas_periodo()
        elif op == "2": faturamento_mensal_periodo()
        elif op == "3": consultas_por_medico_periodo()
        elif op == "4": medicos_sem_consultas_no_periodo()
        elif op == "5": consultas_por_funcionario_periodo()
        elif op == "6": req1_faturamento_mensal_por_convenio()
        elif op == "7": req2_consultas_receita_por_especialidade()
        elif op == "8": req3_uso_equipamentos_por_medico()
        elif op == "0": break
        else: print("Opção inválida")

def menu_criacao():
    print("\n--- CRIAÇÃO DE ESTRUTURA ---")
    print("1 - Criar apenas tabelas (sem seed)")
    print("2 - Criar tabelas + carga inicial (seed)")
    sub = input("Opção: ").strip()
    if sub == "1":
        criar_apenas_tabelas()
    elif sub == "2":
        criar_tabelas_e_carga()
    else:
        print("Opção inválida")

# ============================= MENU PRINCIPAL =============================

def main():
    while True:
        print("\n===== SISTEMA CLÍNICA =====")
        print("1 - Gerenciar Pacientes")
        print("2 - Gerenciar Médicos")
        print("3 - Gerenciar Funcionários")
        print("4 - Gerenciar Consultas")
        print("5 - Gerenciar Tipos de Exame")
        print("6 - Gerenciar Prescrições")
        print("7 - Gerenciar Encaminhamentos")
        print("8 - Relatórios")
        print("9 - Criar estrutura (tabelas/seed)")
        print("10 - Apagar todas as tabelas")
        print("11 - Assistente IA (caso clínico)")
        print("12 - Listar sugestões IA (histórico)")
        print("13 - Gerenciar Clínicas Parceiras")
        print("14 - Gerenciar Convênios")
        print("15 - Especialidade")
        print("16 - Equipamentos")
        print("17 - Doenças")
        print("18 - Perguntar ao banco (IA → SQL somente leitura)")
        print("0 - Sair")
        op = input("Opção: ").strip()

        if op == "1":  menu_paciente()
        elif op == "2":  menu_medico()
        elif op == "3":  menu_funcionario()
        elif op == "4":  menu_consulta()
        elif op == "5":  menu_exame()
        elif op == "6":  menu_prescricao()
        elif op == "7":  menu_encaminhamento()
        elif op == "8":  menu_relatorios()
        elif op == "9":  menu_criacao()
        elif op == "10": apagar_todas_tabelas()
        elif op == "11": sugestao_para_caso_clinico()
        elif op == "12": listar_sugestoes_ia()
        elif op == "13": menu_clinica()
        elif op == "14": menu_convenio()
        elif op == "15": menu_especialidade()
        elif op == "16": menu_equipamento()
        elif op == "17": menu_doenca()
        elif op == "18": perguntar_ao_banco()
        elif op == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida")

if __name__ == "__main__":
    main()
