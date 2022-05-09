from os import close
from sqlite3.dbapi2 import connect
import sys, banco, datetime
from PyQt5 import uic, QtWidgets 
from classe import Usuario, Cliente, Macros,Tmb, Alimentos
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 

# Tela Logar
def logar():
    usuario = tela_logar.inputUsuario.text()
    senha = tela_logar.InputSenha.text()
    usuario_login = banco.buscar_usuario(usuario)
    if usuario == '' and senha == '':
        tela_aviso.show()
        tela_aviso.label.setText(f'COLOQUE SEUS DADOS!')
    elif usuario_login is None or usuario_login[2] != senha:
        tela_aviso.show()
        tela_aviso.label.setText(f"USUÁRIO NÃO ENCONTRADO")
        tela_logar.inputUsuario.setText('')
        tela_logar.InputSenha.setText('')
    else:
        usuario_1.banco_para_modelo(usuario_login)
        if usuario_1.adm == 1:
            tela_logar.close()
            tela_adm.show()
            inserir_dados_na_tabela_adm()
        else:
            tela_logar.close()
            tela_conexoes.show()

# Tela ADM
def cadastrar_login_senha_temporario():
    usuario_1.usuario = tela_adm.inputUsuario.text()
    usuario_1.senha = tela_adm.inputSenha.text()
    if usuario_1.usuario == '' and usuario_1.senha == '':
        tela_aviso.show()
        tela_aviso.label.setText(f'PREENCHA TODOS OS CAMPOS!')
    else:
        banco.inserir_usuario_por_modelo(usuario_1)
        tela_adm.inputUsuario.setText('')
        tela_adm.inputSenha.setText('')
        tela_aviso.show()
        tela_aviso.label.setText(f'USUÁRIO INSERIDO!')

def inserir_dados_na_tabela_adm():
    clientes = banco.buscar_todos_os_clientes()
    tabela = tela_adm.tableWidget
    tabela.setRowCount(len(clientes))
    row = 0
    for cl in clientes:
        tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{cl[0]}'))
        tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{cl[1]}'))
        tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{cl[2]}'))
        tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'{cl[3]}'))
        row += 1

def buscar_cliente_por_nome():
    nome = tela_adm.inputNome.text()
    cliente = banco.buscar_cliente_por_nome(nome)
    if cliente == None:
        tela_aviso.show()
        tela_aviso.label.setText(f'Usuário não encontrado!')
    else:
        tabela = tela_adm.tableWidget
        tabela.setRowCount(len(cliente))
        row = 0
        for cl in cliente:
            tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{cl[0]}'))
            tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{cl[1]}'))
            tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{cl[2]}'))
            tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'{cl[3]}'))
            row += 1

def logout_tela_adm():
    tela_logar.inputUsuario.setText('')
    tela_logar.InputSenha.setText('')
    tela_adm.close()
    tela_logar.show()

def logout_tela_adm_usuario():
    tela_logar.inputUsuario.setText('')
    tela_logar.InputSenha.setText('')
    tela_adm.close()
    tela_logar.show()

def excluir_cliente():
    tabela = tela_adm.tableWidget
    linha = tabela.currentRow()
    if linha < 0:
        tela_aviso.show()
        tela_aviso.label.setText(f"SELECIONE UM NOME PARA EXCLUIR")
    else:
        nome_funcionario = tabela.item(linha,0).text()
        usuario_banco = banco.buscar_cliente_por_nome_1(nome_funcionario)
        cliente_id = usuario_banco[5]
        tabela.removeRow(linha)
        banco.remover_usuario_por_cliente_id(cliente_id)
        banco.remover_cliente_por_nome(nome_funcionario)
        banco.remover_refeicao_po_usuario(cliente_id)
        banco.remover_tmb_por_id(cliente_id)
        banco.remover_dieta_por_cliente_id(cliente_id)
        banco.remover_calorias_por_cliente_id(cliente_id)
        inserir_dados_na_tabela_adm()
        tela_aviso.show()
        tela_aviso.label.setText(f"CLIENTE EXCLUIDO")

# Tela conexoes
def atualizar():
    tela_conexoes.close()
    tela_cliente.show()

def inicio():
    cliente = banco.buscar_usuario(usuario_1.usuario)
    cpf_banco = banco.buscar_cliente_id(cliente[0])
    if cpf_banco == None:
        tela_aviso.show()
        tela_aviso.label.setText(f"Atualize seu cadastro")
    else:
        tela_conexoes.close()
        tela_introduçao.show()

def rever_dieta():
    cliente = banco.buscar_usuario(usuario_1.usuario)
    cpf_banco = banco.buscar_cliente_id(cliente[0])
    if cpf_banco == None:
        tela_aviso.show()
        tela_aviso.label.setText(f"Atualize seu cadastro")
    else:
        tela_conexoes.close()
        tela_macros.show()
        tela_macros.widget.hide()
        tela_macros.widget_2.hide()
        tela_macros.widget_3.hide()
        tela_macros.widget_4.hide()
        inserir_dados_tabela_taco()

        tabelas_ref_1("0")
        tabelas_ref_2("0")
        tabelas_ref_3("0")
        tabelas_ref_4("0")
        tabelas_ref_5("0")
        tabelas_ref_6("0")
        limpar_labels()

def logout_tela_conexoes():
    tela_conexoes.close()
    tela_logar.show()
    tela_logar.inputUsuario.setText('')
    tela_logar.InputSenha.setText('')
    limpar_labels()

# Tela aviso
def avisador():
    tela_aviso.close()
    tela_aviso.label.setFont(QFont('MS Shell Dlg 2',10,75))

# Tela Cliente
def cadastrar_usuario_cliente():
    # Classe Cliente
    cliente_1.nome = tela_cliente.inputNome.text()
    cliente_1.email = tela_cliente.inputEmail.text()
    cliente_1.cpf = tela_cliente.inputCpf.text()
    cliente_1.telefone = tela_cliente.inputTelefone.text()
    # Classe Usuario
    usuario_1.usuario = tela_cliente.inputUsuario.text()
    usuario_1.senha = tela_cliente.inputSenha.text()
    conf_senha = tela_cliente.inputConfSenha.text()
    cpf_cliente = banco.buscar_cliente_por_cpf(cliente_1.cpf)
    senha_cliente = banco.buscar_usuario_por_senha(usuario_1.senha)
    if cliente_1.nome == '' or cliente_1.email == '' or cliente_1.cpf == '' or cliente_1.telefone == '' or usuario_1.usuario == '' or usuario_1.senha == '' or conf_senha == '':
        tela_aviso.show()
        tela_aviso.label.setText(f'PREENCHA TODOS OS CAMPOS!')
    elif usuario_1.senha != conf_senha:
        tela_aviso.show()
        tela_aviso.label.setText(f'CREDENCIAIS NÃO CONFEREM!')
    elif len(conf_senha) < 8:
        tela_aviso.show()
        tela_aviso.label.setText(f'SENHA DEVE TER 8 OU MAIS CARÁCTERES!')
    elif len(usuario_1.usuario) < 6:
        tela_aviso.show()
        tela_aviso.label.setText(f'USUÁRIO DEVE TER 6 OU MAIS CARÁCTERES!')
    elif cpf_cliente is None:
        if senha_cliente is None:
            banco.alterar_login_senha(usuario_1)
            usuario_banco = banco.buscar_usuario(usuario_1.usuario)
            cliente_1.cliente_id = usuario_banco[0]
            banco.inserir_cliente_por_modelo(cliente_1)
            tela_cliente.inputNome.setText('')
            tela_cliente.inputEmail.setText('')
            tela_cliente.inputCpf.setText('')
            tela_cliente.inputTelefone.setText('')
            tela_cliente.inputUsuario.setText('')
            tela_cliente.inputSenha.setText('')
            tela_cliente.inputConfSenha.setText('')
            tela_aviso.show()
            tela_aviso.label.setText(f'DADOS CADASTRADOS COM SUCESSO!')
        else:
            tela_aviso.show()
            tela_aviso.label.setText(f'SENHA JÁ CADASTRADA!')   
    else:
        tela_aviso.show()
        tela_aviso.label.setText(f'CPF JÁ CADASTRADO!')
        
def atualizar_dados_cliente():
    cpf = tela_cliente.inputCpf.text()
    cliente_banco = banco.buscar_cliente_id(usuario_1.id)
    # Classe Cliente
    cliente_1.nome = tela_cliente.inputNome.text()
    cliente_1.email = tela_cliente.inputEmail.text()
    cliente_1.cpf = tela_cliente.inputCpf.text()
    cliente_1.telefone = tela_cliente.inputTelefone.text()
    # Classe Usuario
    usuario_1.usuario = tela_cliente.inputUsuario.text()
    usuario_1.senha = tela_cliente.inputSenha.text()
    conf_senha = tela_cliente.inputConfSenha.text()
    if cliente_1.nome == '' or cliente_1.email == '' or cliente_1.cpf == '' or cliente_1.telefone == '' or usuario_1.usuario == '' or usuario_1.senha == '' or conf_senha == '':
        tela_aviso.show()
        tela_aviso.label.setText(f'PREENCHA TODOS OS CAMPOS!')
    elif cliente_banco is None:
        tela_aviso.show()
        tela_aviso.label.setText(f'CLIENTE NÃO CADASTRADO')
    else:
        banco.alterar_login_senha(usuario_1)
        banco.alterar_dados_cleinte(cliente_1)
        tela_cliente.inputNome.setText('')
        tela_cliente.inputEmail.setText('')
        tela_cliente.inputCpf.setText('')
        tela_cliente.inputTelefone.setText('')
        tela_cliente.inputUsuario.setText('')
        tela_cliente.inputSenha.setText('')
        tela_cliente.inputConfSenha.setText('')
        tela_aviso.show()
        tela_aviso.label.setText(f'DADOS ATUALIZADOS COM SUCESSO')
        
def logout_tela_cliente():
    tela_cliente.close()
    tela_conexoes.show()

# Tela Introdução
def escolha_cutting():
    tela_introduçao.close()
    tela_cutting.show()

def escolha_bulking():
    tela_introduçao.close()
    tela_bulking.show()

def escolha_manter():
    tela_introduçao.close()
    tela_manter.show()

def logout_tela_introducao():
    tela_introduçao.close()
    tela_conexoes.show()

# Tela Cutting
def gerar_tmb_cutting():
    peso_usuario = tela_cutting.input_peso.text()
    verificar_peso=(peso_usuario.isdigit())
    altura_usuario = tela_cutting.input_altura.text()
    verificar_altura=(altura_usuario.isdigit())
    idade_usuario = tela_cutting.input_idade.text()
    verificar_idade=(idade_usuario.isdigit())
    verificar_dieta = banco.buscar_tmb_por_id(usuario_1.id)
    atividade_usuario = tela_cutting.comboatividade.currentText()
    verificar_genero_masculino=tela_cutting.boxMasculino.isChecked()
    verificar_genero_feminino=tela_cutting.boxFeminino.isChecked()
    if peso_usuario == '' or altura_usuario == '' or idade_usuario == '':
        tela_aviso.show()
        tela_aviso.label.setText("Preencha os Campos")
    elif verificar_peso == False or verificar_altura == False or verificar_idade == False :
        tela_aviso.show()
        tela_aviso.label.setText(f"Preencha em Números Inteiros")
    elif verificar_genero_masculino == False and verificar_genero_masculino == False:
        tela_aviso.show()
        tela_aviso.label.setText(f"Preencha seu Gênero")
    elif verificar_genero_masculino== True and verificar_genero_feminino==True:
        tela_aviso.show()
        tela_aviso.label.setText(f"Escolhar uma opção de Gênero")
    elif verificar_dieta is not None:
        tela_aviso.show()
        tela_aviso.label.setText(f"Você já possue dieta,\ncaso queira modificar aperte (Atualizar)")
    else:
        peso=int(peso_usuario)
        idade=int(idade_usuario)
        altura=int(altura_usuario)
        imc=round((peso/(altura*altura))*10000)
        if imc<=19:
            tela_cutting.close()
            tela_bulking.show()
            tela_aviso.show()
            tela_aviso.label.setText(f"Recomendamos a tela Bulking,\nvocê possui um peso muito baixo,\nseu IMC é {round(imc)}kg")
        elif peso>=634:
            tela_aviso.show()
            tela_aviso.label.setText(f"Nem o homem mais pesado do mundo tem este peso,\nJon Brower foi o ser humano mais pesado da história,\ncom um peso de aproximadamente 634 kg")
        elif peso > 150:
            peso == 100
        else:
            if verificar_genero_masculino==True:
                valor_tmb = int((10 *peso) + (6.25 *altura) - (5 *idade) + 5)
                tela_cutting.label_resultado_valores.setText(f"{valor_tmb} Kcal")
                if atividade_usuario == "Sedentario":
                    tela_cutting.label_get.setText(f"{round((valor_tmb * 1.4)-500)} Kcal")
                    Cutting = int((valor_tmb * 1.3) - 500)
                    if Cutting < 0:
                        Cutting = Cutting * -1
                    else:
                        proteina_usuario = int(peso * 2)
                        gordura_usuario = int(peso * 0.8)
                        carbo_usuario =int(((proteina_usuario*4)+(gordura_usuario*9)-Cutting)/4*-1)
                        banco.inserir_dieta_usuario(proteina_usuario, carbo_usuario, gordura_usuario, Cutting, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        banco.inserir_caloria_usuario(kcal_da_proteina, kcal_do_carbo, kcal_de_gordura, usuario_1.id)
                        banco.inserir_tmb(Cutting, 'Cutting', peso, altura, idade, 'Masculino', "Sedentario", valor_tmb, usuario_1.id)
                elif atividade_usuario == "Ativo":
                    tela_cutting.label_get.setText(f"{round((valor_tmb * 1.5)-500)}")
                    Cutting = int((valor_tmb * 1.5) - 500)
                    if Cutting < 0:
                        Cutting = Cutting * -1
                    else:
                        proteina_usuario = int(peso * 2)
                        gordura_usuario = int(peso * 0.8)
                        carbo_usuario =int(((proteina_usuario*4)+(gordura_usuario*9)-Cutting)/4*-1)
                        banco.inserir_dieta_usuario(proteina_usuario, carbo_usuario, gordura_usuario, Cutting, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        banco.inserir_caloria_usuario(kcal_da_proteina, kcal_do_carbo, kcal_de_gordura, usuario_1.id)
                        banco.inserir_tmb(Cutting, 'Cutting', peso, altura, idade, 'Masculino', "Ativo", valor_tmb, usuario_1.id)
                elif atividade_usuario == "Bastante Ativo":
                    tela_cutting.label_get.setText(f"{round((valor_tmb * 1.8)-500)}")
                    Cutting = int((valor_tmb * 1.8) - 500)
                    if Cutting < 0:
                        Cutting = Cutting * -1
                    else:
                        proteina_usuario = int(peso * 2)
                        gordura_usuario = int(peso * 0.8)
                        carbo_usuario =int(((proteina_usuario*4)+(gordura_usuario*9)-Cutting)/4*-1)
                        banco.inserir_dieta_usuario(proteina_usuario, carbo_usuario, gordura_usuario, Cutting, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        banco.inserir_caloria_usuario(kcal_da_proteina, kcal_do_carbo, kcal_de_gordura, usuario_1.id)
                        banco.inserir_tmb(Cutting, 'Cutting', peso, altura, idade, 'Masculino', "Bastante Ativo", valor_tmb, usuario_1.id)
            elif verificar_genero_feminino==True:
                valor_tmb=int((10*peso) + (6.25*altura) - (5 * idade_usuario)- 161)
                tela_cutting.label_resultado_valores.setText(f"{valor_tmb} Kcal")
                if atividade_usuario == "Sedentario":
                    tela_cutting.label_get.setText(f"{round((valor_tmb*1.4)-500)}")
                    Cutting= int((valor_tmb*1.3)-500)
                    if Cutting < 0:
                        Cutting = Cutting * -1
                    else:
                        proteina_usuario=int(peso*2)
                        gordura_usuario=int(peso*0.8)
                        carbo_usuario =int(((proteina_usuario*4)+(gordura_usuario*9)-Cutting)/4*-1)
                        banco.inserir_dieta_usuario(proteina_usuario,carbo_usuario,gordura_usuario,Cutting, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        banco.inserir_caloria_usuario(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                        banco.inserir_tmb(Cutting, 'Cutting', peso, altura, idade, 'Feminino', "Sedentario", valor_tmb, usuario_1.id)
                elif atividade_usuario == "Ativo":
                    tela_cutting.label_get.setText(f"{round((valor_tmb*1.5)-500)}")
                    Cutting= int((valor_tmb*1.5)-500)
                    if Cutting < 0:
                        Cutting = Cutting * -1
                    else:
                        proteina_usuario=int(peso*2)
                        gordura_usuario=int(peso*0.8)
                        carbo_usuario =int(((proteina_usuario*4)+(gordura_usuario*9)-Cutting)/4*-1)
                        banco.inserir_dieta_usuario(proteina_usuario,carbo_usuario,gordura_usuario,Cutting, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        banco.inserir_caloria_usuario(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                        banco.inserir_tmb(Cutting, 'Cutting', peso, altura, idade, 'Feminino', "Ativo", valor_tmb, usuario_1.id)
                elif atividade_usuario == "Bastante Ativo":
                    tela_cutting.label_get.setText(f"{round((valor_tmb*1.8)-500)}")
                    Cutting= int((valor_tmb*1.8)-500)
                    if Cutting < 0:
                        Cutting = Cutting * -1
                    else:
                        proteina_usuario=int(peso*2)
                        gordura_usuario=int(peso*0.8)
                        carbo_usuario =int(((proteina_usuario*4)+(gordura_usuario*9)-Cutting)/4*-1)
                        banco.inserir_dieta_usuario(proteina_usuario,carbo_usuario,gordura_usuario,Cutting, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        banco.inserir_caloria_usuario(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                        banco.inserir_tmb(Cutting, 'Cutting', peso, altura, idade, 'Feminino', "Bastante Ativo", valor_tmb, usuario_1.id)
            tela_cutting.transicao_macro.setEnabled(True)
            
def atualizar_cutting():
    peso_usuario = tela_cutting.input_peso.text()
    verificar_peso = peso_usuario.isdigit()
    altura_usuario = tela_cutting.input_altura.text()
    verificar_altura = altura_usuario.isdigit()
    idade_usuario = tela_cutting.input_idade.text()
    verificar_idade = idade_usuario.isdigit()
    verificar_dieta=banco.buscar_tmb_por_id(usuario_1.id)
    atividade_usuario = tela_cutting.comboatividade.currentText()
    verificar_genero_masculino=tela_cutting.boxMasculino.isChecked()
    verificar_genero_feminino=tela_cutting.boxFeminino.isChecked()
    if peso_usuario == '' or altura_usuario == '' or idade_usuario == '':
        tela_aviso.show()
        tela_aviso.label.setText("Preencha os Campos")
    elif verificar_peso == False or verificar_altura == False or verificar_idade == False:
        tela_aviso.show()
        tela_aviso.label.setText(f"Preencha em Números Inteiros")
    elif verificar_genero_feminino == False and verificar_genero_masculino == False:
        tela_aviso.show()
        tela_aviso.label.setText(f"Preencha seu Gênero")
    elif verificar_genero_masculino== True and verificar_genero_feminino==True:
        tela_aviso.show()
        tela_aviso.label.setText(f"Escolhar uma opção de Gênero")
    elif verificar_dieta==None:
        tela_aviso.show()
        tela_aviso.label.setText(f"Você Não possui uma Dieta")
    else:
        peso = int(peso_usuario)
        idade = int(idade_usuario)
        altura = int(altura_usuario)
        imc = (peso / (altura * altura)) * 10000
        if imc <= 19:
            tela_cutting.close()
            tela_bulking.show()
            tela_aviso.show()
            tela_aviso.label.setText(f"Recomendamos a tela Bulking,\nVocê Possui um peso Muito Baixo\nSeu IMC é {round(imc)}%")
        elif peso >= 634:
            tela_aviso.show()
            tela_aviso.label.setText(f"Nem o homem mais pesado do mundo tem este peso,\nJon Brower foi o ser humano mais pesado da história,\ncom um peso de aproximadamente 634 kg")
        elif peso > 150:
            peso == 100
        else:
            if verificar_genero_masculino==True:
                valor_tmb = int((10 *peso) + (6.25 *altura) - (5 *idade) + 5)
                tela_cutting.label_resultado_valores.setText(f"{valor_tmb} Kcal")
                if atividade_usuario == "Sedentario":
                    tela_cutting.label_get.setText(f"{round((valor_tmb * 1.3)-500)}")
                    Cutting = int((valor_tmb * 1.3) - 500)
                    if Cutting < 0:
                        Cutting = Cutting * -1
                    else:
                        proteina_usuario = int(peso * 2)
                        gordura_usuario = int(peso * 0.8)
                        carbo_usuario =int(((proteina_usuario*4)+(gordura_usuario*9)-Cutting)/4*-1)
                        banco.alterar_dados_dieta(proteina_usuario, carbo_usuario, gordura_usuario, Cutting, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        banco.alterar_dados_calorico(kcal_da_proteina, kcal_do_carbo, kcal_de_gordura, usuario_1.id)
                        banco.alterar_dados_tmb(Cutting, 'Cutting', peso, altura, idade, 'Masculino', "Sedentario", valor_tmb, usuario_1.id)
                elif atividade_usuario == "Ativo":
                    tela_cutting.label_get.setText(f"{round((valor_tmb * 1.5)-500)}")
                    Cutting = int((valor_tmb * 1.5) - 500)
                    if Cutting < 0:
                        Cutting = Cutting * -1
                    else:
                        proteina_usuario = int(peso * 2)
                        gordura_usuario = int(peso * 0.8)
                        carbo_usuario =int(((proteina_usuario*4)+(gordura_usuario*9)-Cutting)/4*-1)
                        banco.alterar_dados_dieta(proteina_usuario, carbo_usuario, gordura_usuario, Cutting, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        banco.alterar_dados_calorico(kcal_da_proteina, kcal_do_carbo, kcal_de_gordura, usuario_1.id)
                        banco.alterar_dados_tmb(Cutting, 'Cutting', peso, altura, idade, 'Masculino', "Ativo", valor_tmb, usuario_1.id)
                elif atividade_usuario == "Bastante Ativo":
                    tela_cutting.label_get.setText(f"{round((valor_tmb * 1.8)-500)}")
                    Cutting = int((valor_tmb * 1.8) - 500)
                    if Cutting < 0:
                        Cutting = Cutting * -1
                    else:
                        proteina_usuario = int(peso * 2)
                        gordura_usuario = int(peso * 0.8)
                        carbo_usuario =int(((proteina_usuario*4)+(gordura_usuario*9)-Cutting)/4*-1)
                        banco.alterar_dados_dieta(proteina_usuario, carbo_usuario, gordura_usuario, Cutting, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        banco.alterar_dados_calorico(kcal_da_proteina, kcal_do_carbo, kcal_de_gordura, usuario_1.id)
                        banco.alterar_dados_tmb(Cutting, 'Cutting', peso, altura, idade, 'Masculino', "Bastante Ativo", valor_tmb, usuario_1.id)
            elif verificar_genero_feminino==True:
                valor_tmb=int((10*peso) + (6.25*altura) - (5 * idade)- 161)
                tela_cutting.label_resultado_valores.setText(f"{valor_tmb} Kcal")
                if atividade_usuario == "Sedentario":
                    tela_cutting.label_get.setText(f"{round((valor_tmb*1.3)-500)*-1}")
                    Cutting= int((valor_tmb*1.3)-500)
                    if Cutting < 0:
                        Cutting = Cutting * -1
                    else:
                        proteina_usuario=int(peso*2)
                        gordura_usuario=int(peso*0.8)
                        carbo_usuario =int(((proteina_usuario*4)+(gordura_usuario*9)-Cutting)/4*-1)
                        banco.alterar_dados_dieta(proteina_usuario,carbo_usuario,gordura_usuario,Cutting, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        banco.alterar_dados_calorico(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                        banco.alterar_dados_tmb(Cutting, 'Cutting', peso, altura, idade, 'Feminino', "Sedentario", valor_tmb, usuario_1.id)
                elif atividade_usuario == "Ativo":
                    tela_cutting.label_get.setText(f"{round((valor_tmb*1.5)-500)}")
                    Cutting= int((valor_tmb*1.5)-500)
                    if Cutting < 0:
                        Cutting = Cutting * -1
                    else:
                        proteina_usuario=int(peso*2)
                        gordura_usuario=int(peso*0.8)
                        carbo_usuario =int(((proteina_usuario*4)+(gordura_usuario*9)-Cutting)/4*-1)
                        banco.alterar_dados_dieta(proteina_usuario,carbo_usuario,gordura_usuario,Cutting, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        banco.alterar_dados_calorico(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                        banco.alterar_dados_tmb(Cutting, 'Cutting', peso, altura, idade, 'Feminino', "Ativo", valor_tmb, usuario_1.id)
                elif atividade_usuario == "Bastante Ativo":
                    tela_cutting.label_get.setText(f"{round((valor_tmb*1.8)-500)}")
                    Cutting= int((valor_tmb*1.8)-500)
                    if Cutting < 0:
                        Cutting = Cutting * -1
                    else:
                        proteina_usuario=int(peso*2)
                        gordura_usuario=int(peso*0.8)
                        carbo_usuario =int(((proteina_usuario*4)+(gordura_usuario*9)-Cutting)/4*-1)
                        banco.alterar_dados_dieta(proteina_usuario,carbo_usuario,gordura_usuario,Cutting, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        banco.alterar_dados_calorico(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                        banco.alterar_dados_tmb(Cutting, 'Cutting', peso, altura, idade, 'Feminino', "Bastante Ativo", valor_tmb, usuario_1.id)
            tela_cutting.transicao_macro.setEnabled(True)
            tela_aviso.show()
            tela_aviso.label.setText(f'Dieta Atualizada')


def logout_tela_cutting():
    tela_cutting.close()
    tela_introduçao.show()
    limpar_labels()

# Tela Bulking
def gerar_tmb_bulking():
    peso_usuario = tela_bulking.input_peso.text()
    verificar_peso=peso_usuario.isdigit()
    altura_usuario = tela_bulking.input_altura.text()
    verificar_altura=altura_usuario.isdigit()
    idade_usuario = tela_bulking.input_idade.text()
    verificar_idade=idade_usuario.isdigit()
    atividade_usuario = tela_bulking.comboatividade.currentText()
    verificar_genero_masculino=tela_bulking.boxMasculino.isChecked()
    verificar_genero_feminino=tela_bulking.boxFeminino.isChecked()
    verificar_dieta = banco.buscar_tmb_por_id(usuario_1.id)
    if peso_usuario == '' or altura_usuario == '' or idade_usuario == '':
        tela_aviso.show()
        tela_aviso.label.setText("Preencha os Campos")
    elif verificar_peso == False or verificar_altura == False or verificar_idade == False :
        tela_aviso.show()
        tela_aviso.label.setText(f"Preencha em Números Inteiros")
    elif verificar_genero_feminino == False and verificar_genero_masculino == False:
        tela_aviso.show()
        tela_aviso.label.setText(f"Preencha seu Gênero")
    elif verificar_genero_masculino== True and verificar_genero_feminino==True:
        tela_aviso.show()
        tela_aviso.label.setText(f"Escolhar uma opção de Gênero")
    elif verificar_dieta is not None:
        tela_aviso.show()
        tela_aviso.label.setText(f"Você já possue dieta,\ncaso queira modificar aperte (Atualizar)")
    else:
        peso=int(peso_usuario)
        idade=int(idade_usuario)
        altura=int(altura_usuario)
        imc=int((peso/(altura*altura))*1000)
        if imc>30:
            tela_cutting.show()
            tela_bulking.close()
            tela_aviso.show()
            tela_aviso.label.setText(f"Recomendamos a tela Cutting,\nvocê possui um Peso Muito alto,\nseu IMC é {imc}")
            limpar_labels()
        elif peso>634:
            tela_aviso.show()
            tela_aviso.label.setText(f"Nem o homem mais pesado do mundo tem este peso,\nJon Brower foi o ser humano mais pesado da história,\ncom um peso de aproximadamente 634 kg")
        elif peso > 150:
            peso == 100
        elif verificar_genero_masculino==True:
            valor_tmb = int((10 * peso) + (6.25 * altura) - (5 * idade) + 5)
            tela_bulking.label_resultado_valores.setText(f"{valor_tmb} Kcal")
            if atividade_usuario == "Sedentario":
                tela_bulking.label_get.setText(f"{round((valor_tmb*1.3)+500)}")
                Bulking= int((valor_tmb*1.3)+500)
                if Bulking < 0:
                    Bulking = Bulking * -1
                else:
                    proteina_usuario=int(peso*2)
                    gordura_usuario=int(peso*1)
                    carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Bulking)/4*-1)
                    banco.inserir_dieta_usuario(proteina_usuario,carbo_usuario,gordura_usuario,Bulking, usuario_1.id)
                    kcal_da_proteina = int(proteina_usuario * 4)
                    kcal_do_carbo = int(carbo_usuario * 4)
                    kcal_de_gordura = int(gordura_usuario * 9)
                    banco.inserir_caloria_usuario(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                    banco.inserir_tmb(Bulking, 'Bulking', peso, altura, idade, 'Masculino', "Sedentario", valor_tmb, usuario_1.id)
            elif atividade_usuario == "Ativo":
                tela_bulking.label_get.setText(f"{round((valor_tmb*1.5)+500)}")
                Bulking= int((valor_tmb*1.5)+500)
                if Bulking < 0:
                    Bulking = Bulking * -1
                else:
                    proteina_usuario=int(peso*2)
                    gordura_usuario=int(peso*1)
                    carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Bulking)/4*-1)
                    banco.inserir_dieta_usuario(proteina_usuario,carbo_usuario,gordura_usuario,Bulking, usuario_1.id)
                    kcal_da_proteina = int(proteina_usuario * 4)
                    kcal_do_carbo = int(carbo_usuario * 4)
                    kcal_de_gordura = int(gordura_usuario * 9)
                    banco.inserir_caloria_usuario(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                    banco.inserir_tmb(Bulking, 'Bulking', peso, altura, idade, 'Masculino', "Ativo", valor_tmb, usuario_1.id)
            elif atividade_usuario == "Bastante Ativo":
                tela_bulking.label_get.setText(f"{round((valor_tmb*1.8)+500)}")
                Bulking= int((valor_tmb*1.8)+500)
                if Bulking < 0:
                    Bulking = Bulking * -1
                else:
                    proteina_usuario=int(peso*2)
                    gordura_usuario=int(peso*1)
                    carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Bulking)/4*-1)
                    banco.inserir_dieta_usuario(proteina_usuario,carbo_usuario,gordura_usuario,Bulking, usuario_1.id)
                    kcal_da_proteina = int(proteina_usuario * 4)
                    kcal_do_carbo = int(carbo_usuario * 4)
                    kcal_de_gordura = int(gordura_usuario * 9)
                    banco.inserir_caloria_usuario(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                    banco.inserir_tmb(Bulking, 'Bulking', peso, altura, idade, 'Masculino', "Muito Ativo", valor_tmb, usuario_1.id)
        elif verificar_genero_feminino==True:
            valor_tmb=int((10*peso) + (6.25*altura) - (5 * idade_usuario)- 161)
            tela_bulking.label_resultado_valores.setText(f"{valor_tmb} Kcal")
            if atividade_usuario == "Sedentario":
                tela_bulking.label_get.setText(f"{round((valor_tmb*1.3)+500)}")
                Bulking= int((valor_tmb*1.3)+500)
                if Bulking < 0:
                    Bulking = Bulking * -1
                else:
                    proteina_usuario=int(peso*2)
                    gordura_usuario=int(peso*1)
                    carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Bulking)/4*-1)
                    banco.inserir_dieta_usuario(proteina_usuario,carbo_usuario,gordura_usuario,Bulking, usuario_1.id)
                    kcal_da_proteina = int(proteina_usuario * 4)
                    kcal_do_carbo = int(carbo_usuario * 4)
                    kcal_de_gordura = int(gordura_usuario * 9)
                    banco.inserir_caloria_usuario(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                    banco.inserir_tmb(Bulking, 'Bulking', peso, altura, idade, 'Feminino', "Sedentário", valor_tmb, usuario_1.id)
            elif atividade_usuario == "Ativo":
                tela_bulking.label_get.setText(f"{round((valor_tmb*1.5)+500)}")
                Bulking= int((valor_tmb*1.5)+500)
                if Bulking < 0:
                    Bulking = Bulking * -1
                else:
                    proteina_usuario=int(peso*2)
                    gordura_usuario=int(peso*1)
                    carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Bulking)/4*-1)
                    banco.inserir_dieta_usuario(proteina_usuario,carbo_usuario,gordura_usuario,Bulking, usuario_1.id)
                    kcal_da_proteina = int(proteina_usuario * 4)
                    kcal_do_carbo = int(carbo_usuario * 4)
                    kcal_de_gordura = int(gordura_usuario * 9)
                    banco.inserir_caloria_usuario(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                    banco.inserir_tmb(Bulking, 'Bulking', peso, altura, idade, 'Feminino', "Ativo", valor_tmb, usuario_1.id)
            elif atividade_usuario == "Bastante Ativo":
                tela_bulking.label_get.setText(f"{round((valor_tmb*1.8)+500)}")
                Bulking= int((valor_tmb*1.8)+500)
                if Bulking < 0:
                    Bulking = Bulking * -1
                else:
                    proteina_usuario=int(peso*2)
                    gordura_usuario=int(peso*1)
                    carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Bulking)/4*-1)
                    banco.inserir_dieta_usuario(proteina_usuario,carbo_usuario,gordura_usuario,Bulking, usuario_1.id)
                    kcal_da_proteina = int(proteina_usuario * 4)
                    kcal_do_carbo = int(carbo_usuario * 4)
                    kcal_de_gordura = int(gordura_usuario * 9)
                    banco.inserir_caloria_usuario(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                    banco.inserir_tmb(Bulking, 'Bulking', peso, altura, idade, 'Feminino', "Muito Ativo", valor_tmb, usuario_1.id)           
    tela_bulking.transicao_macro.setEnabled(True)

def atualizar_Bulking():
    peso_usuario = tela_bulking.input_peso.text()
    verificar_peso=(peso_usuario.isdigit())
    altura_usuario = tela_bulking.input_altura.text()
    verificar_altura=(altura_usuario.isdigit())
    idade_usuario = tela_bulking.input_idade.text()
    verificar_idade=(idade_usuario.isdigit())
    verificar_dieta=banco.buscar_tmb_por_id(usuario_1.id)
    atividade_usuario = tela_bulking.comboatividade.currentText()
    verificar_genero_masculino=tela_bulking.boxMasculino.isChecked()
    verificar_genero_feminino=tela_bulking.boxFeminino.isChecked()
    if peso_usuario == '' or altura_usuario == '' or idade_usuario == '':
        tela_aviso.show()
        tela_aviso.label.setText("Preencha os Campos")
    elif verificar_peso==False or verificar_altura==False or verificar_idade==False :
        tela_aviso.show()
        tela_aviso.label.setText(f"Preencha em Números Inteiros")
    elif verificar_genero_feminino == False and verificar_genero_masculino == False:
        tela_aviso.show()
        tela_aviso.label.setText(f"Preencha seu Gênero")
    elif verificar_genero_masculino== True and verificar_genero_feminino==True:
        tela_aviso.show()
        tela_aviso.label.setText(f"Escolhar uma opção de Gênero")
    elif verificar_dieta==None:
        tela_aviso.show()
        tela_aviso.label.setText(f"Você não possui uma dieta")
    else:
        peso=int(peso_usuario)
        idade=int(idade_usuario)
        altura=int(altura_usuario)
        imc=int((peso/(altura*altura))*10000)
        if imc>30:
            tela_cutting.show()
            tela_bulking.close()
            tela_aviso.show()
            tela_aviso.label.setText(f"Recomendamos a tela Cutting,\nvocê possui um Peso Muito alto,\nseu IMC é {imc}")
            limpar_labels()
        elif peso>634:
            tela_aviso.show()
            tela_aviso.label.setText(f"Nem o homem mais pesado do mundo tem este peso,\nJon Brower foi o ser humano mais pesado da história,\ncom um peso de aproximadamente 634 kg")
        elif peso > 150:
            peso == 100
        elif verificar_genero_masculino==True:
            valor_tmb = int((10 * peso) + (6.25 * altura) - (5 * idade) + 5)
            tela_bulking.label_resultado_valores.setText(f"{valor_tmb} Kcal")
            if atividade_usuario == "Sedentario":
                tela_bulking.label_get.setText(f"{round((valor_tmb*1.3)+500)}")
                Bulking= int((valor_tmb*1.3)+500)
                if Bulking < 0:
                    Bulking = Bulking * -1
                else:
                    proteina_usuario=int(peso*2)
                    gordura_usuario=int(peso*1)
                    carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Bulking)/4*-1)
                    banco.alterar_dados_dieta(proteina_usuario,carbo_usuario,gordura_usuario,Bulking, usuario_1.id)
                    kcal_da_proteina = int(proteina_usuario * 4)
                    kcal_do_carbo = int(carbo_usuario * 4)
                    kcal_de_gordura = int(gordura_usuario * 9)
                    banco.alterar_dados_calorico(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                    banco.alterar_dados_tmb(Bulking, 'Bulking', peso, altura, idade, 'Masculino', "Sedentario", valor_tmb, usuario_1.id)
            elif atividade_usuario == "Ativo":
                tela_bulking.label_get.setText(f"{round((valor_tmb*1.5)+500)}")
                Bulking= int((valor_tmb*1.5)+500)
                if Bulking < 0:
                    Bulking = Bulking * -1
                else:
                    proteina_usuario=int(peso*2)
                    gordura_usuario=int(peso*1)
                    carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Bulking)/4*-1)
                    banco.alterar_dados_dieta(proteina_usuario,carbo_usuario,gordura_usuario,Bulking, usuario_1.id)
                    kcal_da_proteina = int(proteina_usuario * 4)
                    kcal_do_carbo = int(carbo_usuario * 4)
                    kcal_de_gordura = int(gordura_usuario * 9)
                    banco.alterar_dados_calorico(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                    banco.alterar_dados_tmb(Bulking, 'Bulking', peso, altura, idade, 'Masculino', "Ativo", valor_tmb, usuario_1.id)
            elif atividade_usuario == "Bastante Ativo":
                tela_bulking.label_get.setText(f"{round((valor_tmb*1.8)+500)}")
                Bulking= int((valor_tmb*1.8)+500)
                if Bulking < 0:
                    Bulking = Bulking * -1
                else:
                    proteina_usuario=int(peso*2)
                    gordura_usuario=int(peso*1)
                    carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Bulking)/4*-1)
                    banco.alterar_dados_dieta(proteina_usuario,carbo_usuario,gordura_usuario,Bulking, usuario_1.id)
                    kcal_da_proteina = int(proteina_usuario * 4)
                    kcal_do_carbo = int(carbo_usuario * 4)
                    kcal_de_gordura = int(gordura_usuario * 9)
                    banco.alterar_dados_calorico(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                    banco.alterar_dados_tmb(Bulking, 'Bulking', peso, altura, idade, 'Masculino', "Muito Ativo", valor_tmb, usuario_1.id)
        elif verificar_genero_feminino==True:
            valor_tmb=int((10*peso) + (6.25*altura) - (5 * idade_usuario)- 161)
            tela_bulking.label_resultado_valores.setText(f"{valor_tmb} Kcal")
            if atividade_usuario == "Sedentario":
                tela_bulking.label_get.setText(f"{round((valor_tmb*1.3)+500)}")
                Bulking= int((valor_tmb*1.3)+500)
                if Bulking < 0:
                    Bulking = Bulking * -1
                else:
                    proteina_usuario=int(peso*2)
                    gordura_usuario=int(peso*1)
                    carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Bulking)/4*-1)
                    banco.alterar_dados_dieta(proteina_usuario,carbo_usuario,gordura_usuario,Bulking, usuario_1.id)
                    kcal_da_proteina = int(proteina_usuario * 4)
                    kcal_do_carbo = int(carbo_usuario * 4)
                    kcal_de_gordura = int(gordura_usuario * 9)
                    banco.alterar_dados_calorico(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                    banco.alterar_dados_tmb(Bulking, 'Bulking', peso, altura, idade, 'Feminino', "Sedentário", valor_tmb, usuario_1.id)
            elif atividade_usuario == "Ativo":
                tela_bulking.label_get.setText(f"{round((valor_tmb*1.5)+500)}")
                Bulking= int((valor_tmb*1.5)+500)
                if Bulking < 0:
                    Bulking = Bulking * -1
                else:
                    proteina_usuario=int(peso*2)
                    gordura_usuario=int(peso*1)
                    carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Bulking)/4*-1)
                    banco.alterar_dados_dieta(proteina_usuario,carbo_usuario,gordura_usuario,Bulking, usuario_1.id)
                    kcal_da_proteina = int(proteina_usuario * 4)
                    kcal_do_carbo = int(carbo_usuario * 4)
                    kcal_de_gordura = int(gordura_usuario * 9)
                    banco.alterar_dados_calorico(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                    banco.alterar_dados_tmb(Bulking, 'Bulking', peso, altura, idade, 'Feminino', "Ativo", valor_tmb, usuario_1.id)
            elif atividade_usuario == "Bastante Ativo":
                tela_bulking.label_get.setText(f"{round((valor_tmb*1.8)+500)}")
                Bulking= int((valor_tmb*1.8)+500)
                if Bulking < 0:
                    Bulking = Bulking * -1
                else:
                    proteina_usuario=int(peso*2)
                    gordura_usuario=int(peso*1)
                    carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Bulking)/4*-1)
                    banco.alterar_dados_dieta(proteina_usuario,carbo_usuario,gordura_usuario,Bulking, usuario_1.id)
                    kcal_da_proteina = int(proteina_usuario * 4)
                    kcal_do_carbo = int(carbo_usuario * 4)
                    kcal_de_gordura = int(gordura_usuario * 9)
                    banco.alterar_dados_calorico(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                    banco.alterar_dados_tmb(Bulking, 'Bulking', peso, altura, idade, 'Feminino', "Muito Ativo", valor_tmb, usuario_1.id)           
        tela_bulking.transicao_macro.setEnabled(True)
        tela_aviso.show()
        tela_aviso.label.setText(f'Dieta Atualizada')


def logout_tela_bulking():
    tela_bulking.close()
    tela_introduçao.show()
    limpar_labels()

# Tela Manter
def gerar_tmb_manter():
    peso_usuario = tela_manter.input_peso.text()
    verificar_peso=(peso_usuario.isdigit())
    altura_usuario = tela_manter.input_altura.text()
    verificar_altura=(altura_usuario.isdigit())
    idade_usuario = tela_manter.input_idade.text()
    verificar_idade=(idade_usuario.isdigit())
    verificar_dieta=banco.buscar_tmb_por_id(usuario_1.id)
    atividade_usuario = tela_manter.comboatividade.currentText()
    verificar_genero_masculino=tela_manter.boxMasculino.isChecked()
    verificar_genero_feminino=tela_manter.boxFeminino.isChecked()
    if peso_usuario == '' or altura_usuario == '' or idade_usuario == '':
        tela_aviso.show()
        tela_aviso.label.setText("Preencha os Campos")
    elif verificar_peso==False or verificar_altura==False or verificar_idade==False :
        tela_aviso.show()
        tela_aviso.label.setText(f"Preencha em Números Inteiros")
    elif verificar_genero_feminino == False and verificar_genero_masculino == False:
        tela_aviso.show()
        tela_aviso.label.setText(f"Preencha seu Gênero")
    elif verificar_genero_masculino== True and verificar_genero_feminino==True:
        tela_aviso.show()
        tela_aviso.label.setText(f"Escolhar uma opção de Gênero")
    elif verificar_dieta is not None:
        tela_aviso.show()
        tela_aviso.label.setText(f"Você já possue dieta,\nCaso queira modificar aperte (Atualizar)")
    else:
        peso=int(peso_usuario)
        idade=int(idade_usuario)
        altura=int(altura_usuario)
        imc=int((peso/(altura*altura))*10000)
        if imc>30:
            tela_cutting.show()
            tela_bulking.close()
            tela_aviso.show()
            tela_aviso.label.setText(f"Recomendamos a tela Cutting,\nvocê possui o peso muito alto,\nseu IMC é {imc}")
            limpar_labels()
        elif peso>634:
            tela_aviso.show()
            tela_aviso.label.setText(f"Nem o homem mais pesado do mundo tem este peso,\nJon Brower foi o ser humano mais pesado da história,\ncom um peso de aproximadamente 634 kg")
            limpar_labels()
        elif imc>30:
            tela_cutting.show()
            tela_bulking.close()
            tela_aviso.show()
            tela_aviso.label.setText(f"Recomendamos a tela Cutting,\nvocê possui o peso muito alto,\nseu IMC é {imc}")
        elif peso > 150:
            peso == 100
        else:
            if verificar_genero_masculino==True:
                valor_tmb=int((10 *peso) + (6.25 *altura) - (5 *idade)+5)
                tela_manter.label_resultado_valores.setText(f"{valor_tmb} Kcal")
                if atividade_usuario == "Sedentario":
                    tela_manter.label_get.setText(f"{round(valor_tmb*1.3)}")
                    Manter= int((valor_tmb*1.3))
                    if Manter < 0:
                        Manter = Manter * -1
                    else:
                        proteina_usuario=int(peso*2)
                        gordura_usuario=int(peso*0.6)
                        carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Manter)/4*-1)
                        banco.inserir_dieta_usuario(proteina_usuario,carbo_usuario,gordura_usuario,Manter, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        banco.inserir_caloria_usuario(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                        banco.inserir_tmb(Manter, 'Manter', peso, altura, idade, 'Masculino', "Sedentário", valor_tmb, usuario_1.id)
                elif atividade_usuario == "Ativo":
                    tela_manter.label_get.setText(f"{round(valor_tmb*1.5)}")
                    Manter= int((valor_tmb*1.5))
                    if Manter < 0:
                        Manter = Manter * -1
                    else:
                        proteina_usuario=int(peso*2)
                        gordura_usuario=int(peso*1)
                        carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Manter)/4*-1)
                        banco.inserir_dieta_usuario(proteina_usuario,carbo_usuario,gordura_usuario,Manter, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        banco.inserir_caloria_usuario(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                        banco.inserir_tmb(Manter, 'Manter', peso, altura, idade, 'Masculino', "Ativo", valor_tmb, usuario_1.id)
                elif atividade_usuario == "Bastante Ativo":
                    tela_manter.label_get.setText(f"{round(valor_tmb*1.8)}")
                    Manter= int((valor_tmb*1.8))
                    if Manter < 0:
                        Manter = Manter * -1
                    else:
                        proteina_usuario=int(peso*2)
                        gordura_usuario=int(peso*1)
                        carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Manter)/4*-1)
                        banco.inserir_dieta_usuario(proteina_usuario,carbo_usuario,gordura_usuario,Manter, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        banco.inserir_caloria_usuario(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                        banco.inserir_tmb(Manter, 'Manter', peso, altura, idade, 'Masculino', "Muito Ativo", valor_tmb, usuario_1.id)
            elif verificar_genero_feminino==True:
                valor_tmb=int((10*peso) + (6.25*altura) - (5 * idade_usuario)- 161)
                tela_manter.label_resultado_valores.setText(f"{valor_tmb:.2f} Kcal")
                if atividade_usuario == "Sedentario":
                    tela_manter.label_get.setText(f"{round(valor_tmb*1.3)}")
                    Manter= int((valor_tmb*1.3))
                    if Manter < 0:
                        Manter = Manter * -1
                    else:
                        proteina_usuario=int(peso*2)
                        gordura_usuario=int(peso*1)
                        carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Manter)/4*-1)
                        banco.inserir_dieta_usuario(proteina_usuario,carbo_usuario,gordura_usuario,Manter, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        tmb_1(cliente_1.email,peso,altura,idade,"Feminino","Sedentario",valor_tmb,Manter)
                        banco.inserir_caloria_usuario(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                        banco.inserir_tmb(Manter, 'Manter', peso, altura, idade, 'Feminino', "Sedentário", valor_tmb, usuario_1.id)
                elif atividade_usuario == "Ativo":
                    tela_manter.label_get.setText(f"{round(valor_tmb*1.5)}")
                    Manter= int((valor_tmb*1.5))
                    if Manter < 0:
                        Manter = Manter * -1
                    else:
                        proteina_usuario=int(peso*2)
                        gordura_usuario=int(peso*1)
                        carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Manter)/4*-1)
                        banco.inserir_dieta_usuario(proteina_usuario,carbo_usuario,gordura_usuario,Manter, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        tmb_1(cliente_1.email,peso,altura,idade,"Feminino","Sedentario",valor_tmb,Manter)
                        banco.inserir_caloria_usuario(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                        banco.inserir_tmb(Manter, 'Manter', peso, altura, idade, 'Feminino', "Ativo", valor_tmb, usuario_1.id)
                elif atividade_usuario == "Bastante Ativo":
                    tela_manter.label_get.setText(f"{round(valor_tmb*1.8)}")
                    Manter= int((valor_tmb*1.8))
                    if Manter < 0:
                        Manter = Manter * -1
                    else:
                        proteina_usuario=int(peso*2)
                        gordura_usuario=int(peso*1)
                        carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Manter)/4*-1)
                        banco.inserir_dieta_usuario("manter",proteina_usuario,carbo_usuario,gordura_usuario,Manter, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        tmb_1(cliente_1.email,peso,altura,idade,"Feminino","Bastante Ativo",valor_tmb,Manter)
                        banco.inserir_caloria_usuario(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                        banco.inserir_tmb(Manter, 'Manter', peso, altura, idade, 'Feminino', "Muito Ativo", valor_tmb, usuario_1.id)
            tela_manter.transicao_macro.setEnabled(True)
            tela_manter.BtngerarTBM.setEnabled(False)
            
def atualizar_manter():
    peso_usuario = tela_manter.input_peso.text()
    verificar_peso=(peso_usuario.isdigit())
    altura_usuario = tela_manter.input_altura.text()
    verificar_altura=(altura_usuario.isdigit())
    idade_usuario = tela_manter.input_idade.text()
    verificar_idade=(idade_usuario.isdigit())
    verificar_dieta=banco.buscar_tmb_por_id(usuario_1.id)
    atividade_usuario = tela_manter.comboatividade.currentText()
    verificar_genero_masculino=tela_manter.boxMasculino.isChecked()
    verificar_genero_feminino=tela_manter.boxFeminino.isChecked()
    if peso_usuario == '' or altura_usuario == '' or idade_usuario == '':
        tela_aviso.show()
        tela_aviso.label.setText("Preencha os Campos")
    elif verificar_peso==False or verificar_altura==False or verificar_idade==False :
        tela_aviso.show()
        tela_aviso.label.setText(f"Preencha em Números Inteiros")
    elif verificar_genero_masculino == False and verificar_genero_feminino == False:
        tela_aviso.show()
        tela_aviso.label.setText(f"Preencha seu Gênero")
    elif verificar_genero_masculino== True and verificar_genero_feminino==True:
        tela_aviso.show()
        tela_aviso.label.setText(f"Escolhar uma opção de Gênero")
    elif verificar_dieta==None:
        tela_aviso.show()
        tela_aviso.label.setText(f"Você não possui uma dieta")
    else:
        peso=int(peso_usuario)
        idade=int(idade_usuario)
        altura=int(altura_usuario)
        imc=int((peso/(altura*altura))*10000)
        if imc>30:
            tela_cutting.show()
            tela_bulking.close()
            tela_aviso.show()
            tela_aviso.label.setText(f"Recomendamos a tela Cutting,\nvocê possui o peso muito alto,\nseu IMC é {imc}")
            limpar_labels()
        elif peso>634:
            tela_aviso.show()
            tela_aviso.label.setText(f"Nem o homem mais pesado do mundo tem este peso,\nJon Brower foi o ser humano mais pesado da história,\ncom um peso de aproximadamente 634 kg")
            limpar_labels()
        elif imc>30:
            tela_cutting.show()
            tela_bulking.close()
            tela_aviso.show()
            tela_aviso.label.setText(f"Recomendamos a tela Cutting,\nvocê possui o peso muito alto,\nseu IMC é {imc}")
        elif peso > 150:
            peso == 100
        else:
            if verificar_genero_masculino==True:
                valor_tmb=int((10 *peso) + (6.25 *altura) - (5 *idade)+5)
                tela_manter.label_resultado_valores.setText(f"{valor_tmb} Kcal")
                if atividade_usuario == "Sedentario":
                    tela_manter.label_get.setText(f"{round(valor_tmb*1.3)}")
                    Manter = int((valor_tmb * 1.3))
                    if Manter < 0:
                        Manter = Manter * -1
                    else:
                        proteina_usuario = int(peso*2)
                        gordura_usuario = int(peso*1)
                        carbo_usuario = int(((proteina_usuario*4)+(gordura_usuario*9)-Manter)/4*-1)
                        banco.alterar_dados_dieta(proteina_usuario,carbo_usuario,gordura_usuario,Manter, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        banco.alterar_dados_calorico(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                        banco.alterar_dados_tmb(Manter, 'Manter', peso, altura, idade, 'Masculino', "Sedentário", valor_tmb, usuario_1.id)
                elif atividade_usuario == "Ativo":
                    tela_manter.label_get.setText(f"{round(valor_tmb*1.5)}")
                    Manter= int((valor_tmb*1.5))
                    if Manter < 0:
                        Manter = Manter * -1
                    else:
                        proteina_usuario=int(peso*2)
                        gordura_usuario=int(peso*1)
                        carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Manter)/4*-1)
                        banco.alterar_dados_dieta(proteina_usuario,carbo_usuario,gordura_usuario,Manter, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        banco.alterar_dados_calorico(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                        banco.alterar_dados_tmb(Manter, 'Manter', peso, altura, idade, 'Masculino', "Ativo", valor_tmb, usuario_1.id)
                elif atividade_usuario == "Bastante Ativo":
                    tela_manter.label_get.setText(f"{round(valor_tmb*1.8)}")
                    Manter= int((valor_tmb*1.8))
                    if Manter < 0:
                        Manter = Manter * -1
                    else:
                        proteina_usuario=int(peso*2)
                        gordura_usuario=int(peso*1)
                        carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Manter)/4*-1)
                        banco.alterar_dados_dieta(proteina_usuario,carbo_usuario,gordura_usuario,Manter, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        banco.alterar_dados_calorico(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                        banco.alterar_dados_tmb(Manter, 'Manter', peso, altura, idade, 'Masculino', "Muito Ativo", valor_tmb, usuario_1.id)
            elif verificar_genero_feminino==True:
                valor_tmb=int((10*peso) + (6.25*altura) - (5 * idade_usuario)- 161)
                tela_manter.label_resultado_valores.setText(f"{valor_tmb:.2f} Kcal")
                if atividade_usuario == "Sedentario":
                    tela_manter.label_get.setText(f"{round(valor_tmb*1.3)}")
                    Manter= int((valor_tmb*1.3))
                    if Manter < 0:
                        Manter = Manter * -1
                    else:
                        proteina_usuario=int(peso*2)
                        gordura_usuario=int(peso*1)
                        carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Manter)/4*-1)
                        banco.alterar_dados_dieta(proteina_usuario,carbo_usuario,gordura_usuario,Manter, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        tmb_1(cliente_1.email,peso,altura,idade,"Feminino","Sedentario",valor_tmb,Manter)
                        banco.alterar_dados_calorico(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                        banco.alterar_dados_tmb(Manter, 'Manter', peso, altura, idade, 'Feminino', "Sedentário", valor_tmb, usuario_1.id)
                elif atividade_usuario == "Ativo":
                    tela_manter.label_get.setText(f"{round(valor_tmb*1.5)}")
                    Manter= int((valor_tmb*1.5))
                    if Manter < 0:
                        Manter = Manter * -1
                    else:
                        proteina_usuario=int(peso*2)
                        gordura_usuario=int(peso*1)
                        carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Manter)/4*-1)
                        banco.alterar_dados_dieta(proteina_usuario,carbo_usuario,gordura_usuario,Manter, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        tmb_1(cliente_1.email,peso,altura,idade,"Feminino","Sedentario",valor_tmb,Manter)
                        banco.alterar_dados_calorico(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                        banco.alterar_dados_tmb(Manter, 'Manter', peso, altura, idade, 'Feminino', "Ativo", valor_tmb, usuario_1.id)
                elif atividade_usuario == "Bastante Ativo":
                    tela_manter.label_get.setText(f"{round(valor_tmb*1.8)}")
                    Manter= int((valor_tmb*1.8))
                    if Manter < 0:
                        Manter = Manter * -1
                    else:
                        proteina_usuario=int(peso*2)
                        gordura_usuario=int(peso*1)
                        carbo_usuario=int(((proteina_usuario*4)+(gordura_usuario*9)-Manter)/4*-1)
                        banco.alterar_dados_dieta("manter",proteina_usuario,carbo_usuario,gordura_usuario,Manter, usuario_1.id)
                        kcal_da_proteina = int(proteina_usuario * 4)
                        kcal_do_carbo = int(carbo_usuario * 4)
                        kcal_de_gordura = int(gordura_usuario * 9)
                        tmb_1(cliente_1.email,peso,altura,idade,"Feminino","Bastante Ativo",valor_tmb,Manter)
                        banco.alterar_dados_calorico(kcal_da_proteina,kcal_do_carbo,kcal_de_gordura, usuario_1.id)
                        banco.alterar_dados_tmb(Manter, 'Manter', peso, altura, idade, 'Feminino', "Muito Ativo", valor_tmb, usuario_1.id)
            tela_manter.transicao_macro.setEnabled(True)
            tela_aviso.show()
            tela_aviso.label.setText(f'Dieta Atualizada')
        

def logout_tela_manter():
    tela_manter.close()
    tela_introduçao.show()
    limpar_labels()

# Tela Macros
def buscar_alimento_por_nome():
    alimento = tela_macros.inputAlimento.text()
    if alimento == '':
        inserir_dados_tabela_taco()
        tela_aviso.show()
        tela_aviso.label.setText("INFORME O NOME DO ALIMENTO")
    else:
        alimentos = banco.buscar_alimento_por_nome(alimento)
        tabela = tela_macros.tabela_taco
        tabela.setRowCount(len(alimentos))
        row = 0
        for al in alimentos:
            tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{al[0]}'))
            tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{al[1]}'))
            tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{al[2]}'))
            tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'{al[3]}'))
            tabela.setItem(row, 4, QtWidgets.QTableWidgetItem(f'{al[4]}'))
            row += 1

def inserir_dados_tabela_taco():
    alimentos = banco.buscar_aliemtos()
    tabela = tela_macros.tabela_taco
    tabela.setRowCount(len(alimentos))
    row = 0
    for al in alimentos:
        tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{al[0]}'))
        tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{al[1]}'))
        tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{al[2]}'))
        tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f'{al[3]}'))
        tabela.setItem(row, 4, QtWidgets.QTableWidgetItem(f'{al[4]}'))
        row += 1

def abrir_macros():
    tela_bulking.close()
    tela_cutting.close()
    tela_manter.close()
    tela_macros.show()
    inserir_dados_tabela_taco()
    tabelas_ref_1("0")
    tabelas_ref_2("0")
    tabelas_ref_3("0")
    tabelas_ref_4("0")
    tabelas_ref_5("0")
    tabelas_ref_6("0")
    limpar_labels()
    tela_macros.widget.hide()
    tela_macros.widget_2.hide()
    tela_macros.widget_3.hide()
    tela_macros.widget_4.hide()

def quantidae_de_refeições():
    quantidade = tela_macros.quantidade_de_refeicao.currentText()
    verificar_dieta = banco.buscar_dieta(usuario_1.id)
    if verificar_dieta is None:
        tela_macros.close()
        tela_introduçao.show()
        tela_aviso.label.setText("Você não possue dieta,\necolha seu objetivo.\n-> Cutting\n-> Bulking\n-> Manter Peso")
        tela_aviso.show()
    else:
        if quantidade == '2':
            limpar_ref_3()
            limpar_ref_4()
            limpar_ref_5()
            limpar_ref_6()
            tela_macros.widget.hide()
            tela_macros.widget_2.hide()
            tela_macros.widget_3.hide()
            tela_macros.widget_4.hide()
            inserir_macros_diarios()
            inserir_fracionamento(2)
        elif quantidade == '3':
            limpar_ref_4()
            limpar_ref_5()
            limpar_ref_6()
            tela_macros.widget.show()
            tela_macros.widget_2.hide()
            tela_macros.widget_3.hide()
            tela_macros.widget_4.hide()
            inserir_macros_diarios()
            inserir_fracionamento(3)
        elif quantidade == '4':
            limpar_ref_5()
            limpar_ref_6()
            tela_macros.widget.show()
            tela_macros.widget_2.show()
            tela_macros.widget_3.hide()
            tela_macros.widget_4.hide()
            inserir_macros_diarios()
            inserir_fracionamento(4)
        elif quantidade == '5':
            limpar_ref_6()
            tela_macros.widget.show()
            tela_macros.widget_2.show()
            tela_macros.widget_3.show()
            tela_macros.widget_4.hide()
            inserir_macros_diarios()
            inserir_fracionamento(5)
        elif quantidade == '6':
            tela_macros.widget.show()
            tela_macros.widget_2.show()
            tela_macros.widget_3.show()
            tela_macros.widget_4.show()
            inserir_macros_diarios()
            inserir_fracionamento(6)
    
def inserir_macros_diarios():
    calorias = banco.buscar_dieta(usuario_1.id)
    if calorias is None:
        tela_aviso.label.setText('Você não possue dieta')
        tela_aviso.show()
    else:
        tela_macros.proteina_ref_2.setText(f'{round(calorias[0])}g')
        tela_macros.carboidrato_ref_2.setText(f'{round(calorias[1])}g')
        tela_macros.gordura_ref_2.setText(f'{round(calorias[2])}g')
        tela_macros.calorias_total_2.setText(f'{round(calorias[3])}')

def inserir_fracionamento(v):
    calorias = banco.buscar_dieta(usuario_1.id)
    if calorias is None:
        tela_aviso.label.setText('Você não possue dieta')
        tela_aviso.show()
    else:
        tela_macros.proteina_ref.setText(f'{round(calorias[0] / v)}g')
        tela_macros.carboidrato_ref.setText(f'{round(calorias[1] / v)}g')
        tela_macros.gordura_ref.setText(f'{round(calorias[2] / v)}g')
        tela_macros.media_calorico_ref.setText(f'{round(calorias[3] / v)}')

def proteinas_explicaçao():
    tela_aviso.label.setText("As proteínas são substâncias que exercem as mais diversas funções\n no organismo,participando inclusive da composição das células.\n Não existe nenhum processo biológico em que uma proteína não esteja envolvida")
    tela_aviso.label.setFont (QFont ('Arial', 7))
    tela_aviso.show()

def carboidratos_explicaçao():
    tela_aviso.label.setText("Os carboidratos são as principais fontes de energia de uma célula,\nalém de fazerem parte da composição de ácidos nucleicos e da parede celular.\nChamados também de glicídios,hidratos de carbono e açúcares,essas substâncias \nsão encontradas geralmente em alimentos de origem vegetal, como batatas e feijão")
    tela_aviso.label.setFont (QFont ('Arial', 7))
    tela_aviso.show()

def gordura_explicaçao():
    tela_aviso.label.setText("Gorduras são nutrientes que consistem em diferentes ácidos gordos.\n Podem ser distinguidas umas das outras como gorduras insaturadas e saturadas,\ncom base na sua estrutura química.")
    tela_aviso.label.setFont (QFont ('Arial', 7))
    tela_aviso.show()

def fibra_explicaçao():
    tela_aviso.label.setText("As fibras alimentares compreendem as partes comestíveis dos vegetais presentes\nnas frutas, legumes, verduras e hortaliças e do amido resistente encontrado em\nleguminosas e grãos (cereais integrais) que resistem ao processo de digestão, ou seja,elas\npassam quase intactas pelo sistema digestivo chegando ao intestino grosso\ninalteradas.Também não têm valor nutritivo, nem energético (não têm calorias). ")
    tela_aviso.label.setFont (QFont ('Arial', 6,75))
    tela_aviso.show()

def logout_tela_macros():
    tela_macros.close()
    tela_conexoes.show()
    limpar_ref_1()
    limpar_ref_2()
    limpar_ref_3()
    limpar_ref_4()
    limpar_ref_5()
    limpar_ref_6()
    limpar_tabela_ref_1()
    limpar_tabela_ref_2()
    limpar_tabela_ref_3()
    limpar_tabela_ref_4()
    limpar_tabela_ref_5()
    limpar_tabela_ref_6()
    tabelas_ref_1("0")
    tabelas_ref_2("0")
    tabelas_ref_3("0")
    tabelas_ref_4("0")
    tabelas_ref_5("0")
    tabelas_ref_6("0")
    limpar_labels()

def adicionar_alimento_por_nome():
    quantidade = tela_macros.quantidade_de_refeicao.currentText()
    tabela = tela_macros.tabela_taco
    linha = tabela.currentRow()
    objetivo = tela_macros.proteina_ref_2.text()
    if objetivo == '':
        tela_aviso.show()
        tela_aviso.label.setText(f"INSIRA A QUANTIDADE DE REFEIÇÕES DIÁRIAS")
    elif linha < 0:
        tela_aviso.show()
        tela_aviso.label.setText(f"SELECIONE O NOME DO ALIMENTO PARA ADICONAR")
    else:
        nome_alimento = tabela.item(linha, 0).text()
        alimento = banco.buscar_alimento_por_nome_1(nome_alimento)
        alimento_1 = tela_macros.alimento_ref_1.text()
        alimento_2 = tela_macros.alimento_ref_2.text()
        alimento_3 = tela_macros.alimento_ref_3.text()
        alimento_4 = tela_macros.alimento_ref_4.text()
        alimento_5 = tela_macros.alimento_ref_5.text()
        alimento_6 = tela_macros.alimento_ref_6.text()
        alimento_7 = tela_macros.alimento_ref_9.text()
        alimento_8 = tela_macros.alimento_ref_8.text()
        alimento_9 = tela_macros.alimento_ref_7.text()
        alimento_10 = tela_macros.alimento_ref_12.text()
        alimento_11 = tela_macros.alimento_ref_11.text()
        alimento_12 = tela_macros.alimento_ref_10.text()
        alimento_13 = tela_macros.alimento_ref_15.text()
        alimento_14 = tela_macros.alimento_ref_14.text()
        alimento_15 = tela_macros.alimento_ref_13.text()
        alimento_16 = tela_macros.alimento_ref_18.text()
        alimento_17 = tela_macros.alimento_ref_17.text()
        alimento_18 = tela_macros.alimento_ref_16.text()
        if alimento_1 == '':
            tela_macros.alimento_ref_1.setText(f"{alimento[0]}")
        elif alimento_2 == '':
            tela_macros.alimento_ref_2.setText(f"{alimento[0]}")
        elif alimento_3 == '':
            tela_macros.alimento_ref_3.setText(f"{alimento[0]}")
        elif alimento_4 == '':
            tela_macros.alimento_ref_4.setText(f"{alimento[0]}")
        elif alimento_5 == '':
            tela_macros.alimento_ref_5.setText(f"{alimento[0]}")
        elif alimento_6 == '':
            tela_macros.alimento_ref_6.setText(f"{alimento[0]}") 
        elif quantidade == '3':      
            if alimento_7 == '':
                tela_macros.alimento_ref_9.setText(f"{alimento[0]}")            
            elif alimento_8 == '':
                tela_macros.alimento_ref_8.setText(f"{alimento[0]}")            
            elif alimento_9 == '':
                tela_macros.alimento_ref_7.setText(f"{alimento[0]}")            
        elif quantidade == '4':
            if alimento_7 == '':
                tela_macros.alimento_ref_9.setText(f"{alimento[0]}")            
            elif alimento_8 == '':
                tela_macros.alimento_ref_8.setText(f"{alimento[0]}")            
            elif alimento_9 == '':
                tela_macros.alimento_ref_7.setText(f"{alimento[0]}")
            elif alimento_10 == '':
                tela_macros.alimento_ref_12.setText(f"{alimento[0]}")
            elif alimento_11 == '':
                tela_macros.alimento_ref_11.setText(f"{alimento[0]}")
            elif alimento_12 == '':
                tela_macros.alimento_ref_10.setText(f"{alimento[0]}")
        elif quantidade == '5':
            if alimento_7 == '':
                tela_macros.alimento_ref_9.setText(f"{alimento[0]}")            
            elif alimento_8 == '':
                tela_macros.alimento_ref_8.setText(f"{alimento[0]}")            
            elif alimento_9 == '':
                tela_macros.alimento_ref_7.setText(f"{alimento[0]}")
            elif alimento_10 == '':
                tela_macros.alimento_ref_12.setText(f"{alimento[0]}")
            elif alimento_11 == '':
                tela_macros.alimento_ref_11.setText(f"{alimento[0]}")
            elif alimento_12 == '':
                tela_macros.alimento_ref_10.setText(f"{alimento[0]}")
            elif alimento_13 == '':
                tela_macros.alimento_ref_15.setText(f"{alimento[0]}")
            elif alimento_14 == '':
                tela_macros.alimento_ref_14.setText(f"{alimento[0]}")
            elif alimento_15 == '':
                tela_macros.alimento_ref_13.setText(f"{alimento[0]}")
        elif quantidade == '6':
            if alimento_7 == '':
                tela_macros.alimento_ref_9.setText(f"{alimento[0]}")            
            elif alimento_8 == '':
                tela_macros.alimento_ref_8.setText(f"{alimento[0]}")            
            elif alimento_9 == '':
                tela_macros.alimento_ref_7.setText(f"{alimento[0]}")
            elif alimento_10 == '':
                tela_macros.alimento_ref_12.setText(f"{alimento[0]}")
            elif alimento_11 == '':
                tela_macros.alimento_ref_11.setText(f"{alimento[0]}")
            elif alimento_12 == '':
                tela_macros.alimento_ref_10.setText(f"{alimento[0]}")
            elif alimento_13 == '':
                tela_macros.alimento_ref_15.setText(f"{alimento[0]}")
            elif alimento_14 == '':
                tela_macros.alimento_ref_14.setText(f"{alimento[0]}")
            elif alimento_15 == '':
                tela_macros.alimento_ref_13.setText(f"{alimento[0]}")
            elif alimento_16 == '':
                tela_macros.alimento_ref_18.setText(f"{alimento[0]}")
            elif alimento_17 == '':
                tela_macros.alimento_ref_17.setText(f"{alimento[0]}")
            elif alimento_18 == '':
                tela_macros.alimento_ref_16.setText(f"{alimento[0]}")

def calcular_ref_1():
    cont_k = 0
    cont_g = 0
    cont_p = 0
    cont_c = 0
    cont_q = 0
    nome_alimento_1 = tela_macros.alimento_ref_1.text()
    nome_alimento_2 = tela_macros.alimento_ref_2.text()
    nome_alimento_3 = tela_macros.alimento_ref_3.text()
    if nome_alimento_1 == '':
        tela_aviso.show()
        tela_aviso.label.setText(f"Insirar um alimento")
    elif nome_alimento_1 != '':
        quantidade_1 = tela_macros.quanti_ref_1.text()
        if quantidade_1 == '':
            tela_aviso.show()
            tela_aviso.label.setText(f"Insirar a QUANTIDADE do 1° alimento")
        else:
            quantidade_1 = int(tela_macros.quanti_ref_1.text())
            alimento = banco.buscar_alimento_por_nome_1(nome_alimento_1)
            tela_macros.kcal_ref_1.setText(f'{round(quantidade_1 / 100 * alimento[1])}')
            k1 = int(tela_macros.kcal_ref_1.text())
            tela_macros.prot_ref_1.setText(f'{round(quantidade_1 / 100 * alimento[2])}')
            p1 = int(tela_macros.prot_ref_1.text())
            tela_macros.carb_ref_1.setText(f'{round(quantidade_1 / 100 * alimento[4])}')
            c1 = int(tela_macros.carb_ref_1.text())
            tela_macros.gord_ref_1.setText(f'{round(quantidade_1 / 100 * alimento[3])}')
            g1 = int(tela_macros.gord_ref_1.text())
            cont_g = cont_g + g1
            cont_c = cont_c + c1
            cont_p = cont_p + p1
            cont_k = cont_k + k1
            cont_q = cont_q + quantidade_1
            tela_macros.soma_gord.setText(f'{round(cont_g)}')
            tela_macros.soma_carb.setText(f'{round(cont_c)}')
            tela_macros.soma_prot.setText(f'{round(cont_p)}')
            tela_macros.total_calorico_1.setText(f'{round(cont_k)}')
            tela_macros.soma_quantidade.setText(f'{round(cont_q)}')
    if nome_alimento_2 != '':
        quantidade_2 = tela_macros.quanti_ref_2.text()
        if quantidade_2 == '':
            tela_aviso.show()
            tela_aviso.label.setText(f"Insirar a QUANTIDADE do 2° alimento")
        else:
            quantidade_2 = int(tela_macros.quanti_ref_2.text())
            alimento_2 = banco.buscar_alimento_por_nome_1(nome_alimento_2)
            tela_macros.kcal_ref_3.setText(f'{round(quantidade_2 / 100 * alimento_2[1])}')
            k2 = int(tela_macros.kcal_ref_3.text())
            tela_macros.prot_ref_3.setText(f'{round(quantidade_2 / 100 * alimento_2[2])}')
            p2 = int(tela_macros.prot_ref_3.text())
            tela_macros.carb_ref_3.setText(f'{round(quantidade_2 / 100 * alimento_2[4])}')
            c2 = int(tela_macros.carb_ref_3.text())
            tela_macros.gord_ref_3.setText(f'{round(quantidade_2 / 100 * alimento_2[3])}')
            g2 = int(tela_macros.gord_ref_3.text())
            cont_g = cont_g + g2
            cont_c = cont_c + c2
            cont_p = cont_p + p2
            cont_k = cont_k + k2
            cont_q = cont_q + quantidade_2
            tela_macros.soma_gord.setText(f'{round(cont_g)}')
            tela_macros.soma_carb.setText(f'{round(cont_c)}')
            tela_macros.soma_prot.setText(f'{round(cont_p)}')
            tela_macros.total_calorico_1.setText(f'{round(cont_k)}')
            tela_macros.soma_quantidade.setText(f'{round(cont_q)}')
    if nome_alimento_3 != '':
        quantidade_3 = tela_macros.quanti_ref_3.text()
        if quantidade_3 == '':
            tela_aviso.show()
            tela_aviso.label.setText(f"Insirar a QUANTIDADE do 3° alimento")
        else:
            quantidade_3 = int(tela_macros.quanti_ref_3.text())
            alimento_3 = banco.buscar_alimento_por_nome_1(nome_alimento_3)
            tela_macros.kcal_ref_4.setText(f'{round(quantidade_3 / 100 * alimento_3[1])}')
            k3 = int(tela_macros.kcal_ref_4.text())
            tela_macros.prot_ref_4.setText(f'{round(quantidade_3 / 100 * alimento_3[2])}')
            p3 = int(tela_macros.prot_ref_4.text())
            tela_macros.carb_ref_4.setText(f'{round(quantidade_3 / 100 * alimento_3[4])}')
            c3 = int(tela_macros.carb_ref_4.text())
            tela_macros.gord_ref_4.setText(f'{round(quantidade_3 / 100 * alimento_3[3])}')
            g3 = int(tela_macros.gord_ref_4.text())
            cont_g = cont_g + g3
            cont_c = cont_c + c3
            cont_p = cont_p + p3
            cont_k = cont_k + k3
            cont_q = cont_q + quantidade_3
            tela_macros.soma_gord.setText(f'{round(cont_g)}')
            tela_macros.soma_carb.setText(f'{round(cont_c)}')
            tela_macros.soma_prot.setText(f'{round(cont_p)}')
            tela_macros.total_calorico_1.setText(f'{round(cont_k)}')
            tela_macros.soma_quantidade.setText(f'{round(cont_q)}')
    somar_todos_os_macros()

def calcular_ref_2():
    cont_k = 0
    cont_g = 0
    cont_p = 0
    cont_c = 0
    cont_q = 0
    nome_alimento_1 = tela_macros.alimento_ref_4.text()
    nome_alimento_2 = tela_macros.alimento_ref_5.text()
    nome_alimento_3 = tela_macros.alimento_ref_6.text()
    if nome_alimento_1 == '':
        tela_aviso.show()
        tela_aviso.label.setText(f"Insirar um alimento")
    elif nome_alimento_1 != '':
        quantidade_1 = tela_macros.quanti_ref_5.text()
        if quantidade_1 == '':
            tela_aviso.show()
            tela_aviso.label.setText(f"Insirar a QUANTIDADE do 1° alimento")
        else:
            quantidade_1 = int(tela_macros.quanti_ref_5.text())
            alimento = banco.buscar_alimento_por_nome_1(nome_alimento_1)
            tela_macros.kcal_ref_2.setText(f'{round(quantidade_1 / 100 * alimento[1])}')
            k1 = int(tela_macros.kcal_ref_2.text())
            tela_macros.prot_ref_2.setText(f'{round(quantidade_1 / 100 * alimento[2])}')
            p1 = int(tela_macros.prot_ref_2.text())
            tela_macros.carb_ref_2.setText(f'{round(quantidade_1 / 100 * alimento[4])}')
            c1 = int(tela_macros.carb_ref_2.text())
            tela_macros.gord_ref_2.setText(f'{round(quantidade_1 / 100 * alimento[3])}')
            g1 = int(tela_macros.gord_ref_2.text())
            cont_g = cont_g + g1
            cont_c = cont_c + c1
            cont_p = cont_p + p1
            cont_k = cont_k + k1
            cont_q = cont_q + quantidade_1
            tela_macros.soma_gord_2.setText(f'{round(cont_g)}')
            tela_macros.soma_carb_2.setText(f'{round(cont_c)}')
            tela_macros.soma_prot_2.setText(f'{round(cont_p)}')
            tela_macros.total_calorico_2.setText(f'{round(cont_k)}')
            tela_macros.soma_quantidade_2.setText(f'{round(cont_q)}')
    if nome_alimento_2 != '':
        quantidade_2 = tela_macros.quanti_ref_6.text()
        if quantidade_2 == '':
            tela_aviso.show()
            tela_aviso.label.setText(f"Insirar a QUANTIDADE do 2° alimento")
        else:
            quantidade_2 = int(tela_macros.quanti_ref_6.text())
            alimento_2 = banco.buscar_alimento_por_nome_1(nome_alimento_2)
            tela_macros.kcal_ref_6.setText(f'{round(quantidade_2 / 100 * alimento_2[1])}')
            k2 = int(tela_macros.kcal_ref_6.text())
            tela_macros.prot_ref_6.setText(f'{round(quantidade_2 / 100 * alimento_2[2])}')
            p2 = int(tela_macros.prot_ref_6.text())
            tela_macros.carb_ref_6.setText(f'{round(quantidade_2 / 100 * alimento_2[4])}')
            c2 = int(tela_macros.carb_ref_6.text())
            tela_macros.gord_ref_5.setText(f'{round(quantidade_2 / 100 * alimento_2[3])}')
            g2 = int(tela_macros.gord_ref_5.text())
            cont_g = cont_g + g2
            cont_c = cont_c + c2
            cont_p = cont_p + p2
            cont_k = cont_k + k2
            cont_q = cont_q + quantidade_2
            tela_macros.soma_gord_2.setText(f'{round(cont_g)}')
            tela_macros.soma_carb_2.setText(f'{round(cont_c)}')
            tela_macros.soma_prot_2.setText(f'{round(cont_p)}')
            tela_macros.total_calorico_2.setText(f'{round(cont_k)}')
            tela_macros.soma_quantidade_2.setText(f'{round(cont_q)}')
    if nome_alimento_3 != '':
        quantidade_3 = tela_macros.quanti_ref_4.text()
        if quantidade_3 == '':
            tela_aviso.show()
            tela_aviso.label.setText(f"Insirar a QUANTIDADE do 3° alimento")
        else:
            quantidade_3 = int(tela_macros.quanti_ref_4.text())
            alimento_3 = banco.buscar_alimento_por_nome_1(nome_alimento_3)
            tela_macros.kcal_ref_5.setText(f'{round(quantidade_3 / 100 * alimento_3[1])}')
            k3 = int(tela_macros.kcal_ref_5.text())
            tela_macros.prot_ref_5.setText(f'{round(quantidade_3 / 100 * alimento_3[2])}')
            p3 = int(tela_macros.prot_ref_5.text())
            tela_macros.carb_ref_5.setText(f'{round(quantidade_3 / 100 * alimento_3[4])}')
            c3 = int(tela_macros.carb_ref_5.text())
            tela_macros.gord_ref_6.setText(f'{round(quantidade_3 / 100 * alimento_3[3])}')
            g3 = int(tela_macros.gord_ref_6.text())
            cont_g = cont_g + g3
            cont_c = cont_c + c3
            cont_p = cont_p + p3
            cont_k = cont_k + k3
            cont_q = cont_q + quantidade_3
            tela_macros.soma_gord_2.setText(f'{round(cont_g)}')
            tela_macros.soma_carb_2.setText(f'{round(cont_c)}')
            tela_macros.soma_prot_2.setText(f'{round(cont_p)}')
            tela_macros.total_calorico_2.setText(f'{round(cont_k)}')
            tela_macros.soma_quantidade_2.setText(f'{round(cont_q)}')
    somar_todos_os_macros()
def calcular_ref_3():
    cont_k = 0
    cont_g = 0
    cont_p = 0
    cont_c = 0
    cont_q = 0
    nome_alimento_1 = tela_macros.alimento_ref_9.text()
    nome_alimento_2 = tela_macros.alimento_ref_8.text()
    nome_alimento_3 = tela_macros.alimento_ref_7.text()
    if nome_alimento_1 == '':
        tela_aviso.show()
        tela_aviso.label.setText(f"Insirar um alimento")
    elif nome_alimento_1 != '':
        quantidade_1 = tela_macros.quanti_ref_8.text()
        if quantidade_1 == '':
            tela_aviso.show()
            tela_aviso.label.setText(f"Insirar a QUANTIDADE do 1° alimento")
        else:
            quantidade_1 = int(tela_macros.quanti_ref_8.text())
            alimento = banco.buscar_alimento_por_nome_1(nome_alimento_1)
            tela_macros.kcal_ref_8.setText(f'{round(quantidade_1 / 100 * alimento[1])}')
            k1 = int(tela_macros.kcal_ref_8.text())
            tela_macros.prot_ref_9.setText(f'{round(quantidade_1 / 100 * alimento[2])}')
            p1 = int(tela_macros.prot_ref_9.text())
            tela_macros.carb_ref_8.setText(f'{round(quantidade_1 / 100 * alimento[4])}')
            c1 = int(tela_macros.carb_ref_8.text())
            tela_macros.gord_ref_7.setText(f'{round(quantidade_1 / 100 * alimento[3])}')
            g1 = int(tela_macros.gord_ref_7.text())
            cont_g = cont_g + g1
            cont_c = cont_c + c1
            cont_p = cont_p + p1
            cont_k = cont_k + k1
            cont_q = cont_q + quantidade_1
            tela_macros.soma_gord_3.setText(f'{round(cont_g)}')
            tela_macros.soma_carb_3.setText(f'{round(cont_c)}')
            tela_macros.soma_prot_3.setText(f'{round(cont_p)}')
            tela_macros.total_calorico_7.setText(f'{round(cont_k)}')
            tela_macros.soma_quantidade_3.setText(f'{round(cont_q)}')
    if nome_alimento_2 != '':
        quantidade_2 = tela_macros.quanti_ref_9.text()
        if quantidade_2 == '':
            tela_aviso.show()
            tela_aviso.label.setText(f"Insirar a QUANTIDADE do 2° alimento")
        else:
            quantidade_2 = int(tela_macros.quanti_ref_9.text())
            alimento_2 = banco.buscar_alimento_por_nome_1(nome_alimento_2)
            tela_macros.kcal_ref_9.setText(f'{round(quantidade_2 / 100 * alimento_2[1])}')
            k2 = int(tela_macros.kcal_ref_9.text())
            tela_macros.prot_ref_8.setText(f'{round(quantidade_2 / 100 * alimento_2[2])}')
            p2 = int(tela_macros.prot_ref_8.text())
            tela_macros.carb_ref_7.setText(f'{round(quantidade_2 / 100 * alimento_2[4])}')
            c2 = int(tela_macros.carb_ref_7.text())
            tela_macros.gord_ref_8.setText(f'{round(quantidade_2 / 100 * alimento_2[3])}')
            g2 = int(tela_macros.gord_ref_8.text())
            cont_g = cont_g + g2
            cont_c = cont_c + c2
            cont_p = cont_p + p2
            cont_k = cont_k + k2
            cont_q = cont_q + quantidade_2
            tela_macros.soma_gord_3.setText(f'{round(cont_g)}')
            tela_macros.soma_carb_3.setText(f'{round(cont_c)}')
            tela_macros.soma_prot_3.setText(f'{round(cont_p)}')
            tela_macros.total_calorico_7.setText(f'{round(cont_k)}')
            tela_macros.soma_quantidade_3.setText(f'{round(cont_q)}')
    if nome_alimento_3 != '':
        quantidade_3 = tela_macros.quanti_ref_7.text()
        if quantidade_3 == '':
            tela_aviso.show()
            tela_aviso.label.setText(f"Insirar a QUANTIDADE do 3° alimento")
        else:
            quantidade_3 = int(tela_macros.quanti_ref_7.text())
            alimento_3 = banco.buscar_alimento_por_nome_1(nome_alimento_3)
            tela_macros.kcal_ref_7.setText(f'{round(quantidade_3 / 100 * alimento_3[1])}')
            k3 = int(tela_macros.kcal_ref_7.text())
            tela_macros.prot_ref_7.setText(f'{round(quantidade_3 / 100 * alimento_3[2])}')
            p3 = int(tela_macros.prot_ref_7.text())
            tela_macros.carb_ref_9.setText(f'{round(quantidade_3 / 100 * alimento_3[4])}')
            c3 = int(tela_macros.carb_ref_9.text())
            tela_macros.gord_ref_9.setText(f'{round(quantidade_3 / 100 * alimento_3[3])}')
            g3 = int(tela_macros.gord_ref_9.text())
            cont_g = cont_g + g3
            cont_c = cont_c + c3
            cont_p = cont_p + p3
            cont_k = cont_k + k3
            cont_q = cont_q + quantidade_3
            tela_macros.soma_gord_3.setText(f'{round(cont_g)}')
            tela_macros.soma_carb_3.setText(f'{round(cont_c)}')
            tela_macros.soma_prot_3.setText(f'{round(cont_p)}')
            tela_macros.total_calorico_7.setText(f'{round(cont_k)}')
            tela_macros.soma_quantidade_3.setText(f'{round(cont_q)}')
    somar_todos_os_macros()
def calcular_ref_4():
    cont_k = 0
    cont_g = 0
    cont_p = 0
    cont_c = 0
    cont_q = 0
    nome_alimento_1 = tela_macros.alimento_ref_12.text()
    nome_alimento_2 = tela_macros.alimento_ref_11.text()
    nome_alimento_3 = tela_macros.alimento_ref_10.text()
    if nome_alimento_1 == '':
        tela_aviso.show()
        tela_aviso.label.setText(f"Insirar um alimento")
    elif nome_alimento_1 != '':
        quantidade_1 = tela_macros.quanti_ref_11.text()
        if quantidade_1 == '':
            tela_aviso.show()
            tela_aviso.label.setText(f"Insirar a QUANTIDADE do 1° alimento")
        else:
            quantidade_1 = int(tela_macros.quanti_ref_11.text())
            alimento = banco.buscar_alimento_por_nome_1(nome_alimento_1)
            tela_macros.kcal_ref_11.setText(f'{round(quantidade_1 / 100 * alimento[1])}')
            k1 = int(tela_macros.kcal_ref_11.text())
            tela_macros.prot_ref_12.setText(f'{round(quantidade_1 / 100 * alimento[2])}')
            p1 = int(tela_macros.prot_ref_12.text())
            tela_macros.carb_ref_11.setText(f'{round(quantidade_1 / 100 * alimento[4])}')
            c1 = int(tela_macros.carb_ref_11.text())
            tela_macros.gord_ref_10.setText(f'{round(quantidade_1 / 100 * alimento[3])}')
            g1 = int(tela_macros.gord_ref_10.text())
            cont_g = cont_g + g1
            cont_c = cont_c + c1
            cont_p = cont_p + p1
            cont_k = cont_k + k1
            cont_q = cont_q + quantidade_1
            tela_macros.soma_gord_4.setText(f'{round(cont_g)}')
            tela_macros.soma_carb_4.setText(f'{round(cont_c)}')
            tela_macros.soma_prot_4.setText(f'{round(cont_p)}')
            tela_macros.total_calorico_3.setText(f'{round(cont_k)}')
            tela_macros.soma_quantidade_4.setText(f'{round(cont_q)}')
    if nome_alimento_2 != '':
        quantidade_2 = tela_macros.quanti_ref_12.text()
        if quantidade_2 == '':
            tela_aviso.show()
            tela_aviso.label.setText(f"Insirar a QUANTIDADE do 2° alimento")
        else:
            quantidade_2 = int(tela_macros.quanti_ref_12.text())
            alimento_2 = banco.buscar_alimento_por_nome_1(nome_alimento_2)
            tela_macros.kcal_ref_12.setText(f'{round(quantidade_2 / 100 * alimento_2[1])}')
            k2 = int(tela_macros.kcal_ref_12.text())
            tela_macros.prot_ref_11.setText(f'{round(quantidade_2 / 100 * alimento_2[2])}')
            p2 = int(tela_macros.prot_ref_11.text())
            tela_macros.carb_ref_10.setText(f'{round(quantidade_2 / 100 * alimento_2[4])}')
            c2 = int(tela_macros.carb_ref_10.text())
            tela_macros.gord_ref_11.setText(f'{round(quantidade_2 / 100 * alimento_2[3])}')
            g2 = int(tela_macros.gord_ref_11.text())
            cont_g = cont_g + g2
            cont_c = cont_c + c2
            cont_p = cont_p + p2
            cont_k = cont_k + k2
            cont_q = cont_q + quantidade_2
            tela_macros.soma_gord_4.setText(f'{round(cont_g)}')
            tela_macros.soma_carb_4.setText(f'{round(cont_c)}')
            tela_macros.soma_prot_4.setText(f'{round(cont_p)}')
            tela_macros.total_calorico_3.setText(f'{round(cont_k)}')
            tela_macros.soma_quantidade_4.setText(f'{round(cont_q)}')
    if nome_alimento_3 != '':
        quantidade_3 = tela_macros.quanti_ref_10.text()
        if quantidade_3 == '':
            tela_aviso.show()
            tela_aviso.label.setText(f"Insirar a QUANTIDADE do 3° alimento")
        else:
            quantidade_3 = int(tela_macros.quanti_ref_10.text())
            alimento_3 = banco.buscar_alimento_por_nome_1(nome_alimento_3)
            tela_macros.kcal_ref_10.setText(f'{round(quantidade_3 / 100 * alimento_3[1])}')
            k3 = int(tela_macros.kcal_ref_10.text())
            tela_macros.prot_ref_10.setText(f'{round(quantidade_3 / 100 * alimento_3[2])}')
            p3 = int(tela_macros.prot_ref_10.text())
            tela_macros.carb_ref_12.setText(f'{round(quantidade_3 / 100 * alimento_3[4])}')
            c3 = int(tela_macros.carb_ref_12.text())
            tela_macros.gord_ref_12.setText(f'{round(quantidade_3 / 100 * alimento_3[3])}')
            g3 = int(tela_macros.gord_ref_12.text())
            cont_g = cont_g + g3
            cont_c = cont_c + c3
            cont_p = cont_p + p3
            cont_k = cont_k + k3
            cont_q = cont_q + quantidade_3
            tela_macros.soma_gord_4.setText(f'{round(cont_g)}')
            tela_macros.soma_carb_4.setText(f'{round(cont_c)}')
            tela_macros.soma_prot_4.setText(f'{round(cont_p)}')
            tela_macros.total_calorico_3.setText(f'{round(cont_k)}')
            tela_macros.soma_quantidade_4.setText(f'{round(cont_q)}')
    somar_todos_os_macros()

def calcular_ref_5():
    cont_k = 0
    cont_g = 0
    cont_p = 0
    cont_c = 0
    cont_q = 0
    nome_alimento_1 = tela_macros.alimento_ref_15.text()
    nome_alimento_2 = tela_macros.alimento_ref_14.text()
    nome_alimento_3 = tela_macros.alimento_ref_13.text()
    if nome_alimento_1 == '':
        tela_aviso.show()
        tela_aviso.label.setText(f"Insirar um alimento")
    elif nome_alimento_1 != '':
        quantidade_1 = tela_macros.quanti_ref_14.text()
        if quantidade_1 == '':
            tela_aviso.show()
            tela_aviso.label.setText(f"Insirar a QUANTIDADE do 1° alimento")
        else:
            quantidade_1 = int(tela_macros.quanti_ref_14.text())
            alimento = banco.buscar_alimento_por_nome_1(nome_alimento_1)
            tela_macros.kcal_ref_14.setText(f'{round(quantidade_1 / 100 * alimento[1])}')
            k1 = int(tela_macros.kcal_ref_14.text())
            tela_macros.prot_ref_15.setText(f'{round(quantidade_1 / 100 * alimento[2])}')
            p1 = int(tela_macros.prot_ref_15.text())
            tela_macros.carb_ref_14.setText(f'{round(quantidade_1 / 100 * alimento[4])}')
            c1 = int(tela_macros.carb_ref_14.text())
            tela_macros.gord_ref_13.setText(f'{round(quantidade_1 / 100 * alimento[3])}')
            g1 = int(tela_macros.gord_ref_13.text())
            cont_g = cont_g + g1
            cont_c = cont_c + c1
            cont_p = cont_p + p1
            cont_k = cont_k + k1
            cont_q = cont_q + quantidade_1
            tela_macros.soma_gord_5.setText(f'{round(cont_g)}')
            tela_macros.soma_carb_5.setText(f'{round(cont_c)}')
            tela_macros.soma_prot_5.setText(f'{round(cont_p)}')
            tela_macros.total_calorico_4.setText(f'{round(cont_k)}')
            tela_macros.soma_quantidade_5.setText(f'{round(cont_q)}')
    if nome_alimento_2 != '':
        quantidade_2 = tela_macros.quanti_ref_15.text()
        if quantidade_2 == '':
            tela_aviso.show()
            tela_aviso.label.setText(f"Insirar a QUANTIDADE do 2° alimento")
        else:
            quantidade_2 = int(tela_macros.quanti_ref_15.text())
            alimento_2 = banco.buscar_alimento_por_nome_1(nome_alimento_2)
            tela_macros.kcal_ref_15.setText(f'{round(quantidade_2 / 100 * alimento_2[1])}')
            k2 = int(tela_macros.kcal_ref_15.text())
            tela_macros.prot_ref_14.setText(f'{round(quantidade_2 / 100 * alimento_2[2])}')
            p2 = int(tela_macros.prot_ref_14.text())
            tela_macros.carb_ref_13.setText(f'{round(quantidade_2 / 100 * alimento_2[4])}')
            c2 = int(tela_macros.carb_ref_13.text())
            tela_macros.gord_ref_14.setText(f'{round(quantidade_2 / 100 * alimento_2[3])}')
            g2 = int(tela_macros.gord_ref_14.text())
            cont_g = cont_g + g2
            cont_c = cont_c + c2
            cont_p = cont_p + p2
            cont_k = cont_k + k2
            cont_q = cont_q + quantidade_2
            tela_macros.soma_gord_5.setText(f'{round(cont_g)}')
            tela_macros.soma_carb_5.setText(f'{round(cont_c)}')
            tela_macros.soma_prot_5.setText(f'{round(cont_p)}')
            tela_macros.total_calorico_4.setText(f'{round(cont_k)}')
            tela_macros.soma_quantidade_5.setText(f'{round(cont_q)}')
    if nome_alimento_3 != '':
        quantidade_3 = tela_macros.quanti_ref_13.text()
        if quantidade_3 == '':
            tela_aviso.show()
            tela_aviso.label.setText(f"Insirar a QUANTIDADE do 3° alimento")
        else:
            quantidade_3 = int(tela_macros.quanti_ref_13.text())
            alimento_3 = banco.buscar_alimento_por_nome_1(nome_alimento_3)
            tela_macros.kcal_ref_13.setText(f'{round(quantidade_3 / 100 * alimento_3[1])}')
            k3 = int(tela_macros.kcal_ref_13.text())
            tela_macros.prot_ref_13.setText(f'{round(quantidade_3 / 100 * alimento_3[2])}')
            p3 = int(tela_macros.prot_ref_13.text())
            tela_macros.carb_ref_15.setText(f'{round(quantidade_3 / 100 * alimento_3[4])}')
            c3 = int(tela_macros.carb_ref_15.text())
            tela_macros.gord_ref_15.setText(f'{round(quantidade_3 / 100 * alimento_3[3])}')
            g3 = int(tela_macros.gord_ref_15.text())
            cont_g = cont_g + g3
            cont_c = cont_c + c3
            cont_p = cont_p + p3
            cont_k = cont_k + k3
            cont_q = cont_q + quantidade_3
            tela_macros.soma_gord_5.setText(f'{round(cont_g)}')
            tela_macros.soma_carb_5.setText(f'{round(cont_c)}')
            tela_macros.soma_prot_5.setText(f'{round(cont_p)}')
            tela_macros.total_calorico_4.setText(f'{round(cont_k)}')
            tela_macros.soma_quantidade_5.setText(f'{round(cont_q)}')
    somar_todos_os_macros()

def calcular_ref_6():
    cont_k = 0
    cont_g = 0
    cont_p = 0
    cont_c = 0
    cont_q = 0
    nome_alimento_1 = tela_macros.alimento_ref_18.text()
    nome_alimento_2 = tela_macros.alimento_ref_17.text()
    nome_alimento_3 = tela_macros.alimento_ref_16.text()
    if nome_alimento_1 == '':
        tela_aviso.show()
        tela_aviso.label.setText(f"Insirar um alimento")
    elif nome_alimento_1 != '':
        quantidade_1 = tela_macros.quanti_ref_17.text()
        if quantidade_1 == '':
            tela_aviso.show()
            tela_aviso.label.setText(f"Insirar a QUANTIDADE do 1° alimento")
        else:
            quantidade_1 = int(tela_macros.quanti_ref_17.text())
            alimento = banco.buscar_alimento_por_nome_1(nome_alimento_1)
            tela_macros.kcal_ref_17.setText(f'{round(quantidade_1 / 100 * alimento[1])}')
            k1 = int(tela_macros.kcal_ref_17.text())
            tela_macros.prot_ref_18.setText(f'{round(quantidade_1 / 100 * alimento[2])}')
            p1 = int(tela_macros.prot_ref_18.text())
            tela_macros.carb_ref_17.setText(f'{round(quantidade_1 / 100 * alimento[4])}')
            c1 = int(tela_macros.carb_ref_17.text())
            tela_macros.gord_ref_16.setText(f'{round(quantidade_1 / 100 * alimento[3])}')
            g1 = int(tela_macros.gord_ref_16.text())
            cont_g = cont_g + g1
            cont_c = cont_c + c1
            cont_p = cont_p + p1
            cont_k = cont_k + k1
            cont_q = cont_q + quantidade_1
            tela_macros.soma_gord_6.setText(f'{round(cont_g)}')
            tela_macros.soma_carb_6.setText(f'{round(cont_c)}')
            tela_macros.soma_prot_6.setText(f'{round(cont_p)}')
            tela_macros.total_calorico_5.setText(f'{round(cont_k)}')
            tela_macros.soma_quantidade_6.setText(f'{round(cont_q)}')
    if nome_alimento_2 != '':
        quantidade_2 = tela_macros.quanti_ref_18.text()
        if quantidade_2 == '':
            tela_aviso.show()
            tela_aviso.label.setText(f"Insirar a QUANTIDADE do 2° alimento")
        else:
            quantidade_2 = int(tela_macros.quanti_ref_18.text())
            alimento_2 = banco.buscar_alimento_por_nome_1(nome_alimento_2)
            tela_macros.kcal_ref_18.setText(f'{round(quantidade_2 / 100 * alimento_2[1])}')
            k2 = int(tela_macros.kcal_ref_18.text())
            tela_macros.prot_ref_17.setText(f'{round(quantidade_2 / 100 * alimento_2[2])}')
            p2 = int(tela_macros.prot_ref_17.text())
            tela_macros.carb_ref_16.setText(f'{round(quantidade_2 / 100 * alimento_2[4])}')
            c2 = int(tela_macros.carb_ref_16.text())
            tela_macros.gord_ref_17.setText(f'{round(quantidade_2 / 100 * alimento_2[3])}')
            g2 = int(tela_macros.gord_ref_17.text())
            cont_g = cont_g + g2
            cont_c = cont_c + c2
            cont_p = cont_p + p2
            cont_k = cont_k + k2
            cont_q = cont_q + quantidade_2
            tela_macros.soma_gord_6.setText(f'{round(cont_g)}')
            tela_macros.soma_carb_6.setText(f'{round(cont_c)}')
            tela_macros.soma_prot_6.setText(f'{round(cont_p)}')
            tela_macros.total_calorico_5.setText(f'{round(cont_k)}')
            tela_macros.soma_quantidade_6.setText(f'{round(cont_q)}')
    if nome_alimento_3 != '':
        quantidade_3 = tela_macros.quanti_ref_16.text()
        if quantidade_3 == '':
            tela_aviso.show()
            tela_aviso.label.setText(f"Insirar a QUANTIDADE do 3° alimento")
        else:
            quantidade_3 = int(tela_macros.quanti_ref_16.text())
            alimento_3 = banco.buscar_alimento_por_nome_1(nome_alimento_3)
            tela_macros.kcal_ref_16.setText(f'{round(quantidade_3 / 100 * alimento_3[1])}')
            k3 = int(tela_macros.kcal_ref_16.text())
            tela_macros.prot_ref_16.setText(f'{round(quantidade_3 / 100 * alimento_3[2])}')
            p3 = int(tela_macros.prot_ref_16.text())
            tela_macros.carb_ref_18.setText(f'{round(quantidade_3 / 100 * alimento_3[4])}')
            c3 = int(tela_macros.carb_ref_18.text())
            tela_macros.gord_ref_18.setText(f'{round(quantidade_3 / 100 * alimento_3[3])}')
            g3 = int(tela_macros.gord_ref_18.text())
            cont_g = cont_g + g3
            cont_c = cont_c + c3
            cont_p = cont_p + p3
            cont_k = cont_k + k3
            cont_q = cont_q + quantidade_3
            tela_macros.soma_gord_6.setText(f'{round(cont_g)}')
            tela_macros.soma_carb_6.setText(f'{round(cont_c)}')
            tela_macros.soma_prot_6.setText(f'{round(cont_p)}')
            tela_macros.total_calorico_5.setText(f'{round(cont_k)}')
            tela_macros.soma_quantidade_6.setText(f'{round(cont_q)}')
    somar_todos_os_macros()

def somar_todos_os_macros():
    total_g = tela_macros.soma_gord.text()
    total_g2 = tela_macros.soma_gord_2.text()
    total_g3 = tela_macros.soma_gord_3.text()
    total_g4 = tela_macros.soma_gord_4.text()
    total_g5 = tela_macros.soma_gord_5.text()
    total_g6 = tela_macros.soma_gord_6.text()
    total_p = tela_macros.soma_prot.text()
    total_p2 = tela_macros.soma_prot_2.text()
    total_p3 = tela_macros.soma_prot_3.text()
    total_p4 = tela_macros.soma_prot_4.text()
    total_p5 = tela_macros.soma_prot_5.text()
    total_p6 = tela_macros.soma_prot_6.text()
    total_c = tela_macros.soma_carb.text()
    total_c2 = tela_macros.soma_carb_2.text()
    total_c3 = tela_macros.soma_carb_3.text()
    total_c4 = tela_macros.soma_carb_4.text()
    total_c5 = tela_macros.soma_carb_5.text()
    total_c6 = tela_macros.soma_carb_6.text()
    total_k = tela_macros.total_calorico_1.text()
    total_k2 = tela_macros.total_calorico_2.text()
    total_k3 = tela_macros.total_calorico_7.text()
    total_k4 = tela_macros.total_calorico_3.text()
    total_k5 = tela_macros.total_calorico_4.text()
    total_k6 = tela_macros.total_calorico_5.text()
    if total_g != "" and total_g2 == "" and total_g3 =="" and total_g4 =="" and total_g5 =="" and total_g6 =="":
        total_g = int(total_g)
        total_p = int(total_p)
        total_c = int(total_c)
        total_k = int(total_k)
        tela_macros.proteina_ref_3.setText(f'{round(total_p)}g')
        tela_macros.gordura_ref_3.setText(f'{round(total_g)}g')
        tela_macros.carboidrato_ref_3.setText(f'{round(total_c)}g')
        tela_macros.calorias_total_3.setText(f'{round(total_k)}')
    elif total_g != '' and total_g2!="" and total_g3=="" and total_g4 =="" and total_g5 =="" and total_g6 =="":
        total_g = int(total_g)
        total_g2 = int(total_g2)
        total_p = int(total_p)
        total_p2 = int(total_p2)
        total_c = int(total_c)
        total_c2 = int(total_c2)
        total_k = int(total_k)
        total_k2 = int(total_k2)
        soma_g2 = total_g + total_g2
        soma_p2 = total_p + total_p2
        soma_c2 = total_c + total_c2
        soma_k2 = total_k + total_k2
        tela_macros.proteina_ref_3.setText(f'{round(soma_p2)}g')
        tela_macros.gordura_ref_3.setText(f'{round(soma_g2)}g')
        tela_macros.carboidrato_ref_3.setText(f'{round(soma_c2)}g')
        tela_macros.calorias_total_3.setText(f'{round(soma_k2)}')
    elif total_g!='' and total_g2 != "" and total_g3!="" and total_g4 =="" and total_g5 == "" and total_g6 == "":
        total_g = int(total_g)
        total_g2 = int(total_g2)
        total_g3= int(total_g3)
        total_p = int(total_p)
        total_p2 = int(total_p2)
        total_p3 = int(total_p3)
        total_c = int(total_c)
        total_c2 = int(total_c2)
        total_c3 = int(total_c3)
        total_k = int(total_k)
        total_k2 = int(total_k2)
        total_k3 = int(total_k3)
        soma_3 = total_g + total_g2 + total_g3
        soma_p3 = total_p + total_p2 + total_p3
        soma_c3 = total_c + total_c2 + total_c3
        soma_k3 = total_k + total_k2 + total_k3
        tela_macros.gordura_ref_3.setText(f'{round(soma_3)}g')
        tela_macros.proteina_ref_3.setText(f'{round(soma_p3)}g')
        tela_macros.carboidrato_ref_3.setText(f'{round(soma_c3)}g')
        tela_macros.calorias_total_3.setText(f'{round(soma_k3)}')
    elif total_g!='' and total_g2 != "" and total_g3!="" and total_g4 != "" and total_g5 == "" and total_g6 == "" :
        total_g = int(total_g)
        total_g2 = int(total_g2)
        total_g3= int(total_g3)
        total_g4= int(total_g4)
        total_p = int(total_p)
        total_p2 = int(total_p2)
        total_p3 = int(total_p3)
        total_p4 = int(total_p4)
        total_c = int(total_c)
        total_c2 = int(total_c2)
        total_c3 = int(total_c3)
        total_c4 = int(total_c4)
        total_k = int(total_k)
        total_k2 = int(total_k2)
        total_k3 = int(total_k3)
        total_k4 = int(total_k4)
        soma_4 = total_g + total_g2 + total_g3 + total_g4
        soma_p4 = total_p + total_p2 + total_p3 + total_p4
        soma_c4 = total_c + total_c2 + total_c3 + total_c4
        soma_k4 = total_k + total_k2 + total_k3 + total_k4
        tela_macros.gordura_ref_3.setText(f'{round(soma_4)}g')
        tela_macros.proteina_ref_3.setText(f'{round(soma_p4)}g')
        tela_macros.carboidrato_ref_3.setText(f'{round(soma_c4)}g')
        tela_macros.calorias_total_3.setText(f'{round(soma_k4)}')
    elif total_g!='' and total_g2 != "" and total_g3!="" and total_g4 != "" and total_g5 != "" and total_g6 == "" :
        total_g = int(total_g)
        total_g2 = int(total_g2)
        total_g3 = int(total_g3)
        total_g4 = int(total_g4)
        total_g5 = int(total_g5)
        total_p = int(total_p)
        total_p2 = int(total_p2)
        total_p3 = int(total_p3)
        total_p4 = int(total_p4)
        total_p5 = int(total_p5)
        total_c = int(total_c)
        total_c2 = int(total_c2)
        total_c3 = int(total_c3)
        total_c4 = int(total_c4)
        total_c5 = int(total_c5)
        total_k = int(total_k)
        total_k2 = int(total_k2)
        total_k3 = int(total_k3)
        total_k4 = int(total_k4)
        total_k5 = int(total_k5)
        soma_5 = total_g + total_g2 + total_g3 + total_g4 + total_g5
        soma_p5 = total_p + total_p2 + total_p3 + total_p4 + total_p5
        soma_c5 = total_c + total_c2 + total_c3 + total_c4 + total_c5
        soma_k5 = total_k + total_k2 + total_k3 + total_k4 + total_k5
        tela_macros.gordura_ref_3.setText(f'{round(soma_5)}g')
        tela_macros.proteina_ref_3.setText(f'{round(soma_p5)}g')
        tela_macros.carboidrato_ref_3.setText(f'{round(soma_c5)}g')
        tela_macros.calorias_total_3.setText(f'{round(soma_k5)}')
    elif total_g!='' and total_g2 != "" and total_g3!="" and total_g4 != "" and total_g5 != "" and total_g6 != "" :
        total_g = int(total_g)
        total_g2 = int(total_g2)
        total_g3 = int(total_g3)
        total_g4 = int(total_g4)
        total_g5 = int(total_g5)
        total_g6 = int(total_g6)
        total_p = int(total_p)
        total_p2 = int(total_p2)
        total_p3 = int(total_p3)
        total_p4 = int(total_p4)
        total_p5 = int(total_p5)
        total_p6 = int(total_p6)
        total_c = int(total_c)
        total_c2 = int(total_c2)
        total_c3 = int(total_c3)
        total_c4 = int(total_c4)
        total_c5 = int(total_c5)
        total_c6 = int(total_c6)
        total_k = int(total_k)
        total_k2 = int(total_k2)
        total_k3 = int(total_k3)
        total_k4 = int(total_k4)
        total_k5 = int(total_k5)
        total_k6 = int(total_k6)
        soma_g6 = total_g + total_g2 + total_g3 + total_g4 + total_g5 + total_g6
        soma_p6 = total_p + total_p2 + total_p3 + total_p4 + total_p5 + total_p6
        soma_c6 = total_c + total_c2 + total_c3 + total_c4 + total_c5 + total_c6
        soma_k6 = total_k + total_k2 + total_k3 + total_k4 + total_k5 + total_k6
        tela_macros.gordura_ref_3.setText(f'{round(soma_g6)}g')
        tela_macros.proteina_ref_3.setText(f'{round(soma_p6)}g')
        tela_macros.carboidrato_ref_3.setText(f'{round(soma_c6)}g')
        tela_macros.calorias_total_3.setText(f'{round(soma_k6)}')

def inserir_todas_as_refeicoes():
    dieta = banco.buscar_refeicao_por_id(usuario_1.id)
    dieta = len(dieta)
    if dieta != 0:
        tela_aviso.show()
        tela_aviso.label.setText(f"Você já possue uma dieta")
    elif dieta == 0:
        caloria_alimento_1 = 0
        caloria_alimento_2 = 0
        caloria_alimento_3 = 0
        caloria_alimento_4 = 0 
        caloria_alimento_5 = 0
        caloria_alimento_6 = 0
        caloria_alimento_7 = 0
        caloria_alimento_8 = 0
        caloria_alimento_9 = 0
        caloria_alimento_10 = 0
        caloria_alimento_11 = 0
        caloria_alimento_12 = 0
        caloria_alimento_13 = 0
        caloria_alimento_14 = 0
        caloria_alimento_15 = 0
        caloria_alimento_16 = 0
        caloria_alimento_17 = 0
        caloria_alimento_18 = 0
        total_calorico_ref_1 = 0
        total_calorico_ref_2 = 0
        total_calorico_ref_3 = 0
        total_calorico_ref_4 = 0
        total_calorico_ref_5 = 0
        total_calorico_ref_6 = 0
        nome_alimento_1 = tela_macros.alimento_ref_1.text()
        nome_alimento_2 = tela_macros.alimento_ref_2.text()
        nome_alimento_3 = tela_macros.alimento_ref_3.text()
        nome_alimento_4 = tela_macros.alimento_ref_4.text()
        nome_alimento_5 = tela_macros.alimento_ref_5.text()
        nome_alimento_6 = tela_macros.alimento_ref_6.text()
        nome_alimento_7 = tela_macros.alimento_ref_9.text()
        nome_alimento_8 = tela_macros.alimento_ref_8.text()
        nome_alimento_9 = tela_macros.alimento_ref_7.text()
        nome_alimento_10 = tela_macros.alimento_ref_12.text()
        nome_alimento_11 = tela_macros.alimento_ref_11.text()
        nome_alimento_12 = tela_macros.alimento_ref_10.text()
        nome_alimento_13 = tela_macros.alimento_ref_15.text()
        nome_alimento_14 = tela_macros.alimento_ref_14.text()
        nome_alimento_15 = tela_macros.alimento_ref_13.text()
        nome_alimento_16 = tela_macros.alimento_ref_18.text()
        nome_alimento_17 = tela_macros.alimento_ref_17.text()
        nome_alimento_18 = tela_macros.alimento_ref_16.text()
        quantidade_1 = tela_macros.quanti_ref_1.text()
        quantidade_2 = tela_macros.quanti_ref_2.text()
        quantidade_3 = tela_macros.quanti_ref_3.text()
        quantidade_4 = tela_macros.quanti_ref_5.text()
        quantidade_5 = tela_macros.quanti_ref_6.text()
        quantidade_6 = tela_macros.quanti_ref_4.text()
        quantidade_7 = tela_macros.quanti_ref_8.text()
        quantidade_8 = tela_macros.quanti_ref_9.text()
        quantidade_9 = tela_macros.quanti_ref_7.text()
        quantidade_10 = tela_macros.quanti_ref_11.text()
        quantidade_11 = tela_macros.quanti_ref_12.text()
        quantidade_12 = tela_macros.quanti_ref_10.text()
        quantidade_13 = tela_macros.quanti_ref_14.text()
        quantidade_14 = tela_macros.quanti_ref_15.text()
        quantidade_15 = tela_macros.quanti_ref_13.text()
        quantidade_16 = tela_macros.quanti_ref_17.text()
        quantidade_17 = tela_macros.quanti_ref_18.text()
        quantidade_18 = tela_macros.quanti_ref_16.text()
        quantidade = tela_macros.proteina_ref_2.text()
        if quantidade == '':
            tela_aviso.show()
            tela_aviso.label.setText(f"INSIRA A QUANTIDADE DE REFEIÇÕES DIÁRIAS")
        elif nome_alimento_1 == '' and quantidade_1 == '':
            tela_aviso.show()
            tela_aviso.label.setText(f"Informe o alimento e a quantidade")
        else:
            if nome_alimento_1 != '' and quantidade_1 != '':
                alimento = banco.buscar_alimento_por_nome_1(nome_alimento_1)
                banco.inserir_refeicoes('1°', quantidade_1, alimento[0], alimento[1], alimento[2], alimento[4], alimento[3], usuario_1.id)
                quantidade_1 = int()
                caloria_alimento_1 =+ alimento[2] * quantidade_1 / 100
            if nome_alimento_2 != '' and quantidade_2 != '':
                nome_alimento_2 = tela_macros.alimento_ref_2.text()
                alimento2 = banco.buscar_alimento_por_nome_1(nome_alimento_2)
                banco.inserir_refeicoes('1°', quantidade_2, alimento2[0], alimento2[1], alimento2[2], alimento2[4], alimento2[3], usuario_1.id)
                quantidade_2 = int()
                caloria_alimento_2 =+ alimento2[2] * quantidade_2 / 100
            if nome_alimento_3 != '' and quantidade_3 != '':
                nome_alimento_3 = tela_macros.alimento_ref_3.text()
                alimento3 = banco.buscar_alimento_por_nome_1(nome_alimento_3)
                banco.inserir_refeicoes('1°', quantidade_3, alimento3[0], alimento3[1], alimento3[2], alimento3[4], alimento3[3], usuario_1.id)
                quantidade_3=int()
                caloria_alimento_3=+alimento3[2]*quantidade_3/100
            if nome_alimento_4 != '' and quantidade_4 != '':
                alimento4 = banco.buscar_alimento_por_nome_1(nome_alimento_4)
                banco.inserir_refeicoes('2°', quantidade_4, alimento4[0], alimento4[1], alimento4[2], alimento4[4], alimento4[3], usuario_1.id)
                quantidade_4=int()
                caloria_alimento_4=+alimento4[2]*quantidade_4/100
            if nome_alimento_5 != '' and quantidade_5 != '':
                alimento5 = banco.buscar_alimento_por_nome_1(nome_alimento_5)
                banco.inserir_refeicoes('2°', quantidade_5, alimento5[0], alimento5[1], alimento5[2], alimento5[4], alimento5[3], usuario_1.id)
                quantidade_5=int()
                caloria_alimento_5=+alimento5[2]*quantidade_5/100
            if nome_alimento_6 != '' and quantidade_6 != '':
                alimento6 = banco.buscar_alimento_por_nome_1(nome_alimento_6)
                banco.inserir_refeicoes('2°', quantidade_6, alimento6[0], alimento6[1], alimento6[2], alimento6[4], alimento6[3], usuario_1.id)
                quantidade_6=int()
                caloria_alimento_6=+alimento6[2]*quantidade_6/100
            if nome_alimento_7 != '' and quantidade_7 != '':
                alimento7 = banco.buscar_alimento_por_nome_1(nome_alimento_7)
                banco.inserir_refeicoes('3°', quantidade_7, alimento7[0], alimento7[1], alimento7[2], alimento7[4], alimento7[3], usuario_1.id)
                quantidade_7=int()
                caloria_alimento_7=+alimento7[2]*quantidade_7/100
            if nome_alimento_8 != '' and quantidade_8 != '':
                alimento8 = banco.buscar_alimento_por_nome_1(nome_alimento_8)
                banco.inserir_refeicoes('3°', quantidade_8, alimento8[0], alimento8[1], alimento8[2], alimento8[4], alimento8[3], usuario_1.id)
                quantidade_8=int()
                caloria_alimento_8=+alimento8[2]*quantidade_8/100
            if nome_alimento_9 != '' and quantidade_9 != '':
                alimento9 = banco.buscar_alimento_por_nome_1(nome_alimento_9)
                banco.inserir_refeicoes('3°', quantidade_9, alimento9[0], alimento9[1], alimento9[2], alimento9[4], alimento9[3], usuario_1.id)
                quantidade_9=int()
                caloria_alimento_9=+alimento9[2]*quantidade_9/100
            if nome_alimento_10 != '' and quantidade_10 != '':
                alimento10 = banco.buscar_alimento_por_nome_1(nome_alimento_10)
                banco.inserir_refeicoes('4°', quantidade_10, alimento10[0], alimento10[1], alimento10[2], alimento10[4], alimento10[3], usuario_1.id)
                quantidade_10=int()
                caloria_alimento_10=+alimento10[2]*quantidade_10/100
            if nome_alimento_11 != '' and quantidade_11 != '':
                alimento11 = banco.buscar_alimento_por_nome_1(nome_alimento_11)
                banco.inserir_refeicoes('4°', quantidade_11, alimento11[0], alimento11[1], alimento11[2], alimento11[4], alimento11[3], usuario_1.id)
                quantidade_11=int()
                caloria_alimento_11=+alimento11[2]*quantidade_11/100
            if nome_alimento_12 != '' and quantidade_12 != '':
                alimento12 = banco.buscar_alimento_por_nome_1(nome_alimento_12)
                banco.inserir_refeicoes('4°', quantidade_12, alimento12[0], alimento12[1], alimento12[2], alimento12[4], alimento12[3], usuario_1.id)
                quantidade_12=int()
                caloria_alimento_12=+alimento12[2]*quantidade_12/100
            if nome_alimento_13 != '' and quantidade_13 != '':
                alimento13 = banco.buscar_alimento_por_nome_1(nome_alimento_13)
                banco.inserir_refeicoes('5°', quantidade_13, alimento13[0], alimento13[1], alimento13[2], alimento13[4], alimento13[3], usuario_1.id)
                quantidade_13=int()
                caloria_alimento_13=+alimento13[2]*quantidade_13/100
            if nome_alimento_14 != '' and quantidade_14 != '':
                alimento14 = banco.buscar_alimento_por_nome_1(nome_alimento_14)
                banco.inserir_refeicoes('5°', quantidade_14, alimento14[0], alimento14[1], alimento14[2], alimento14[4], alimento14[3], usuario_1.id)
                quantidade_14=int()
                caloria_alimento_14=+alimento14[2]*quantidade_14/100
            if nome_alimento_15 != '' and quantidade_15 != '':
                alimento15 = banco.buscar_alimento_por_nome_1(nome_alimento_15)
                banco.inserir_refeicoes('5°', quantidade_15, alimento15[0], alimento15[1], alimento15[2], alimento15[4], alimento15[3], usuario_1.id)
                quantidade_15=int()
                caloria_alimento_15=+alimento15[2]*quantidade_15/100
            if nome_alimento_16 != '' and quantidade_16 != '':
                alimento16 = banco.buscar_alimento_por_nome_1(nome_alimento_16)
                banco.inserir_refeicoes('6°', quantidade_16, alimento16[0], alimento16[1], alimento16[2], alimento16[4], alimento16[3], usuario_1.id)
                quantidade_16=int()
                caloria_alimento_16=+alimento16[2]*quantidade_16/100
            if nome_alimento_17 != '' and quantidade_17 != '':
                alimento17 = banco.buscar_alimento_por_nome_1(nome_alimento_17)
                banco.inserir_refeicoes('6°', quantidade_17, alimento17[0], alimento17[1], alimento17[2], alimento17[4], alimento17[3], usuario_1.id)
                quantidade_17=int()
                caloria_alimento_17=+alimento17[2]*quantidade_17/100
            if nome_alimento_18 != '' and quantidade_18 != '':
                alimento18 = banco.buscar_alimento_por_nome_1(nome_alimento_18)
                banco.inserir_refeicoes('6°', quantidade_18, alimento18[0], alimento18[1], alimento18[2], alimento18[4], alimento18[3], usuario_1.id)
                quantidade_18=int()
                caloria_alimento_18 =+ alimento18[2] * quantidade_18 / 100
            if dieta == True:
                tela_aviso.show()
                tela_aviso.label.setText(f"Refeição inserida")
                limpar_ref_1()
                limpar_ref_2()
                limpar_ref_3()
                limpar_ref_4()
                limpar_ref_5()
                limpar_ref_6()
                limpar_labels()
            total_calorico_ref_1 = caloria_alimento_1 + caloria_alimento_2 + caloria_alimento_3
            total_calorico_ref_2 = caloria_alimento_4 + caloria_alimento_5 + caloria_alimento_6
            total_calorico_ref_3 = caloria_alimento_7 + caloria_alimento_8 + caloria_alimento_9
            total_calorico_ref_4 = caloria_alimento_10 + caloria_alimento_11 + caloria_alimento_12
            total_calorico_ref_5 = caloria_alimento_13 + caloria_alimento_14 + caloria_alimento_15
            total_calorico_ref_6 = caloria_alimento_16 + caloria_alimento_17 + caloria_alimento_18
            if total_calorico_ref_3 == None:
                calculos_calorico(total_calorico_ref_1,total_calorico_ref_2)
            elif total_calorico_ref_4 == None:
                calculos_calorico(total_calorico_ref_1,total_calorico_ref_2,total_calorico_ref_3)
            elif total_calorico_ref_5 == None:
                calculos_calorico(total_calorico_ref_1,total_calorico_ref_2,total_calorico_ref_3,total_calorico_ref_4)
            elif total_calorico_ref_6 == None:
                calculos_calorico(total_calorico_ref_1,total_calorico_ref_2,total_calorico_ref_3,total_calorico_ref_4,total_calorico_ref_5)
            else:
                calculos_calorico(total_calorico_ref_1, total_calorico_ref_2, total_calorico_ref_3, total_calorico_ref_4, total_calorico_ref_5, total_calorico_ref_6)          

def limpar_labels():
    tela_manter.input_peso.clear()
    tela_manter.input_altura.clear()
    tela_manter.input_idade.clear()
    tela_bulking.input_peso.clear()
    tela_bulking.input_altura.clear()
    tela_bulking.input_idade.clear()
    tela_cutting.input_peso.clear()
    tela_cutting.input_altura.clear()
    tela_cutting.input_idade.clear()
    tela_macros.proteina_ref_2.clear()
    tela_macros.carboidrato_ref_2.clear()
    tela_macros.gordura_ref_2.clear()
    tela_macros.calorias_total_2.clear()
    tela_macros.proteina_ref.clear()
    tela_macros.carboidrato_ref.clear()
    tela_macros.gordura_ref.clear()
    tela_macros.media_calorico_ref.clear()
    tela_macros.proteina_ref_3.clear()
    tela_macros.carboidrato_ref_3.clear()
    tela_macros.gordura_ref_3.clear()
    tela_macros.calorias_total_3.clear()

def limpar_ref_1():
    tela_macros.alimento_ref_1.clear(),tela_macros.quanti_ref_1.clear(),tela_macros.prot_ref_1.clear(),tela_macros.carb_ref_1.clear(),tela_macros.gord_ref_1.clear(),tela_macros.kcal_ref_1.clear(),tela_macros.soma_quantidade.clear(),tela_macros.soma_carb.clear()
    tela_macros.alimento_ref_2.clear(),tela_macros.quanti_ref_2.clear(),tela_macros.prot_ref_3.clear(),tela_macros.carb_ref_3.clear(),tela_macros.gord_ref_3.clear(),tela_macros.kcal_ref_3.clear(),tela_macros.soma_prot.clear(),tela_macros.soma_gord.clear()
    tela_macros.alimento_ref_3.clear(),tela_macros.quanti_ref_3.clear(),tela_macros.prot_ref_4.clear(),tela_macros.carb_ref_4.clear(),tela_macros.gord_ref_4.clear(),tela_macros.kcal_ref_4.clear(),tela_macros.total_calorico_1.clear()
    somar_todos_os_macros()

def limpar_ref_2():
    tela_macros.alimento_ref_4.clear(),tela_macros.quanti_ref_5.clear(),tela_macros.prot_ref_2.clear(),tela_macros.carb_ref_2.clear(),tela_macros.gord_ref_2.clear(),tela_macros.kcal_ref_2.clear(),tela_macros.soma_quantidade_2.clear(),tela_macros.soma_carb_2.clear()
    tela_macros.alimento_ref_5.clear(),tela_macros.quanti_ref_6.clear(),tela_macros.prot_ref_6.clear(),tela_macros.carb_ref_6.clear(),tela_macros.gord_ref_5.clear(),tela_macros.kcal_ref_6.clear(),tela_macros.soma_prot_2.clear(),tela_macros.soma_gord_2.clear()
    tela_macros.alimento_ref_6.clear(),tela_macros.quanti_ref_4.clear(),tela_macros.prot_ref_5.clear(),tela_macros.carb_ref_5.clear(),tela_macros.gord_ref_6.clear(),tela_macros.kcal_ref_5.clear(),tela_macros.total_calorico_2.clear()
    somar_todos_os_macros()

def limpar_ref_3():
    tela_macros.alimento_ref_7.clear(),tela_macros.quanti_ref_8.clear(),tela_macros.prot_ref_9.clear(),tela_macros.carb_ref_8.clear(),tela_macros.gord_ref_7.clear(),tela_macros.kcal_ref_8.clear(),tela_macros.soma_quantidade_3.clear(),tela_macros.soma_carb_3.clear()
    tela_macros.alimento_ref_8.clear(),tela_macros.quanti_ref_9.clear(),tela_macros.prot_ref_8.clear(),tela_macros.carb_ref_7.clear(),tela_macros.gord_ref_8.clear(),tela_macros.kcal_ref_9.clear(),tela_macros.soma_prot_3.clear(),tela_macros.soma_gord_3.clear()
    tela_macros.alimento_ref_9.clear(),tela_macros.quanti_ref_7.clear(),tela_macros.prot_ref_7.clear(),tela_macros.carb_ref_9.clear(),tela_macros.gord_ref_9.clear(),tela_macros.kcal_ref_7.clear(),tela_macros.total_calorico_7.clear()
    somar_todos_os_macros()

def limpar_ref_4():
    tela_macros.alimento_ref_10.clear(),tela_macros.quanti_ref_11.clear(),tela_macros.prot_ref_12.clear(),tela_macros.carb_ref_11.clear(),tela_macros.gord_ref_10.clear(),tela_macros.kcal_ref_11.clear(),tela_macros.soma_quantidade_4.clear(),tela_macros.soma_carb_4.clear()
    tela_macros.alimento_ref_11.clear(),tela_macros.quanti_ref_12.clear(),tela_macros.prot_ref_11.clear(),tela_macros.carb_ref_10.clear(),tela_macros.gord_ref_11.clear(),tela_macros.kcal_ref_12.clear(),tela_macros.soma_prot_4.clear(),tela_macros.soma_gord_4.clear()
    tela_macros.alimento_ref_12.clear(),tela_macros.quanti_ref_10.clear(),tela_macros.prot_ref_10.clear(),tela_macros.carb_ref_12.clear(),tela_macros.gord_ref_12.clear(),tela_macros.kcal_ref_10.clear(),tela_macros.total_calorico_3.clear()
    somar_todos_os_macros()

def limpar_ref_5():
    tela_macros.alimento_ref_13.clear(),tela_macros.quanti_ref_14.clear(),tela_macros.prot_ref_15.clear(),tela_macros.carb_ref_14.clear(),tela_macros.gord_ref_13.clear(),tela_macros.kcal_ref_14.clear(),tela_macros.soma_quantidade_5.clear(),tela_macros.soma_carb_5.clear()
    tela_macros.alimento_ref_14.clear(),tela_macros.quanti_ref_15.clear(),tela_macros.prot_ref_14.clear(),tela_macros.carb_ref_13.clear(),tela_macros.gord_ref_14.clear(),tela_macros.kcal_ref_15.clear(),tela_macros.soma_prot_5.clear(),tela_macros.soma_gord_5.clear()
    tela_macros.alimento_ref_15.clear(),tela_macros.quanti_ref_13.clear(),tela_macros.prot_ref_13.clear(),tela_macros.carb_ref_15.clear(),tela_macros.gord_ref_15.clear(),tela_macros.kcal_ref_13.clear(),tela_macros.total_calorico_4.clear()
    somar_todos_os_macros()

def limpar_ref_6():
    tela_macros.alimento_ref_16.clear(),tela_macros.quanti_ref_17.clear(),tela_macros.prot_ref_18.clear(),tela_macros.carb_ref_17.clear(),tela_macros.gord_ref_16.clear(),tela_macros.kcal_ref_17.clear(),tela_macros.soma_quantidade_6.clear(),tela_macros.soma_carb_6.clear()
    tela_macros.alimento_ref_17.clear(),tela_macros.quanti_ref_18.clear(),tela_macros.prot_ref_17.clear(),tela_macros.carb_ref_16.clear(),tela_macros.gord_ref_17.clear(),tela_macros.kcal_ref_18.clear(),tela_macros.soma_prot_6.clear(),tela_macros.soma_gord_6.clear()
    tela_macros.alimento_ref_18.clear(),tela_macros.quanti_ref_16.clear(),tela_macros.prot_ref_16.clear(),tela_macros.carb_ref_18.clear(),tela_macros.gord_ref_18.clear(),tela_macros.kcal_ref_16.clear(),tela_macros.total_calorico_5.clear()
    somar_todos_os_macros()

# Tela Macros / Imprimir Dieta
def imprimir_dieta_por_usuario():
    dieta = banco.buscar_tmb_por_id(usuario_1.id)
    refeicao = banco.buscar_refeicao_por_id(usuario_1.id)
    refeicao1 = banco.buscar_refeicao_por_id_2(usuario_1.id, '1°')
    refeicao2 = banco.buscar_refeicao_por_id_2(usuario_1.id, '2°')
    refeicao3 = banco.buscar_refeicao_por_id_2(usuario_1.id, '3°')
    refeicao4 = banco.buscar_refeicao_por_id_2(usuario_1.id, '4°')
    refeicao5 = banco.buscar_refeicao_por_id_2(usuario_1.id, '5°')
    refeicao6 = banco.buscar_refeicao_por_id_2(usuario_1.id, '6°')
    ref1 = len(refeicao1)
    ref2 = len(refeicao2)
    ref3 = len(refeicao3)
    ref4 = len(refeicao4)
    ref5 = len(refeicao5)
    ref6 = len(refeicao6)
    if dieta == None or dieta == []:
        tela_macros.close()
        tela_introduçao.show()
        tela_aviso.show()
        tela_aviso.label.setText(f"Você não possue dieta,\nescolha seu objetivo.\n-> Cutting\n-> Bulking\n-> Manter Peso")
    elif refeicao == []:
        tela_aviso.show()
        tela_aviso.label.setText(f"Você não possue Refeição")
    else:
        if ref1 != 0:
            if ref1 == 1:
                tabelas_ref_1('1')
                ref_1 = refeicao1[0]
                tela_macros.alimento_ref_19.setText(f"{ref_1[0]}")
                tela_macros.quanti_ref_19.setText(f"{ref_1[1]}g")
            elif ref1 == 2:
                tabelas_ref_1('2')
                ref_1 = refeicao1[0]
                ref_2 = refeicao1[1]
                tela_macros.alimento_ref_19.setText(f"{ref_1[0]}")
                tela_macros.quanti_ref_19.setText(f"{ref_1[1]}g")
                tela_macros.alimento_ref_20.setText(f"{ref_2[0]}")
                tela_macros.quanti_ref_20.setText(f"{ref_2[1]}g")
            elif ref1 == 3:
                tabelas_ref_1('3')
                ref_1 = refeicao1[0]
                ref_2 = refeicao1[1]
                ref_3 = refeicao1[2]
                tela_macros.alimento_ref_19.setText(f"{ref_1[0]}")
                tela_macros.quanti_ref_19.setText(f"{ref_1[1]}g")
                tela_macros.alimento_ref_20.setText(f"{ref_2[0]}")
                tela_macros.quanti_ref_20.setText(f"{ref_2[1]}g")
                tela_macros.alimento_ref_21.setText(f"{ref_3[0]}")
                tela_macros.quanti_ref_21.setText(f"{ref_3[1]}g")
        if ref2 != 0:
            if ref2 == 1:
                tabelas_ref_2('1')
                ref_4 = refeicao2[0]
                tela_macros.alimento_ref_23.setText(f"{ref_4[0]}")
                tela_macros.quanti_ref_23.setText(f"{ref_4[1]}g")
            elif ref2 == 2:
                tabelas_ref_2('2')
                ref_4 = refeicao2[0]
                ref_5 = refeicao2[1]
                tela_macros.alimento_ref_23.setText(f"{ref_4[0]}")
                tela_macros.quanti_ref_23.setText(f"{ref_4[1]}g")
                tela_macros.alimento_ref_22.setText(f"{ref_5[0]}")
                tela_macros.quanti_ref_22.setText(f"{ref_5[1]}g")
            elif ref2 == 3:
                tabelas_ref_2('3')
                ref_4 = refeicao2[0]
                ref_5 = refeicao2[1]
                ref_6 = refeicao2[2]
                tela_macros.alimento_ref_23.setText(f"{ref_4[0]}")
                tela_macros.quanti_ref_23.setText(f"{ref_4[1]}g")
                tela_macros.alimento_ref_22.setText(f"{ref_5[0]}")
                tela_macros.quanti_ref_22.setText(f"{ref_5[1]}g")
                tela_macros.alimento_ref_24.setText(f"{ref_6[0]}")
                tela_macros.quanti_ref_24.setText(f"{ref_6[1]}g")
        if ref3 != 0:
            if ref3 == 1:
                tabelas_ref_3('1')
                ref_7 = refeicao3[0]
                tela_macros.alimento_ref_25.setText(f"{ref_7[0]}")
                tela_macros.quanti_ref_25.setText(f"{ref_7[1]}g")
            elif ref3 == 2:
                tabelas_ref_3('2')
                ref_7 = refeicao3[0]
                ref_8 = refeicao3[1]
                tela_macros.alimento_ref_25.setText(f"{ref_7[0]}")
                tela_macros.quanti_ref_25.setText(f"{ref_7[1]}g")
                tela_macros.alimento_ref_26.setText(f"{ref_8[0]}")
                tela_macros.quanti_ref_26.setText(f"{ref_8[1]}g")
            elif ref3 == 3:
                tabelas_ref_3('3')
                ref_7 = refeicao3[0]
                ref_8 = refeicao3[1]
                ref_9 = refeicao3[2]
                tela_macros.alimento_ref_25.setText(f"{ref_7[0]}")
                tela_macros.quanti_ref_25.setText(f"{ref_7[1]}g")
                tela_macros.alimento_ref_26.setText(f"{ref_8[0]}")
                tela_macros.quanti_ref_26.setText(f"{ref_8[1]}g")
                tela_macros.alimento_ref_27.setText(f"{ref_9[0]}")
                tela_macros.quanti_ref_27.setText(f"{ref_9[1]}g")
        if ref4 != 0:
            if ref4 == 1:
                tabelas_ref_4('1')
                ref_10 = refeicao4[0]
                tela_macros.alimento_ref_31.setText(f"{ref_10[0]}")
                tela_macros.quanti_ref_31.setText(f"{ref_10[1]}g")
            elif ref4 == 2:
                tabelas_ref_4('2')
                ref_10 = refeicao4[0]
                ref_11 = refeicao4[1]
                tela_macros.alimento_ref_31.setText(f"{ref_10[0]}")
                tela_macros.quanti_ref_31.setText(f"{ref_10[1]}g")
                tela_macros.alimento_ref_32.setText(f"{ref_11[0]}")
                tela_macros.quanti_ref_32.setText(f"{ref_11[1]}g")
            elif ref4 == 3:
                tabelas_ref_4('3')
                ref_10 = refeicao4[0]
                ref_11 = refeicao4[1]
                ref_12 = refeicao4[2]
                tela_macros.alimento_ref_31.setText(f"{ref_10[0]}")
                tela_macros.quanti_ref_31.setText(f"{ref_10[1]}g")
                tela_macros.alimento_ref_32.setText(f"{ref_11[0]}")
                tela_macros.quanti_ref_32.setText(f"{ref_11[1]}g")
                tela_macros.alimento_ref_33.setText(f"{ref_12[0]}")
                tela_macros.quanti_ref_33.setText(f"{ref_12[1]}g")
        if ref5 != 0:
            if ref5 == 1:
                tabelas_ref_5('1')
                ref_13 = refeicao5[0]
                tela_macros.alimento_ref_31.setText(f"{ref_10[0]}")
                tela_macros.quanti_ref_31.setText(f"{ref_10[1]}g")
            elif ref5 == 2:
                tabelas_ref_5('2')
                ref_13 = refeicao5[0]
                ref_14 = refeicao5[1]
                tela_macros.alimento_ref_31.setText(f"{ref_10[0]}")
                tela_macros.quanti_ref_31.setText(f"{ref_10[1]}g")
                tela_macros.alimento_ref_32.setText(f"{ref_11[0]}")
                tela_macros.quanti_ref_32.setText(f"{ref_11[1]}g")
            elif ref5 == 3:
                tabelas_ref_5('3')
                ref_13 = refeicao5[0]
                ref_14 = refeicao5[1]
                ref_15 = refeicao5[2]
                tela_macros.alimento_ref_34.setText(f"{ref_13[0]}")
                tela_macros.quanti_ref_34.setText(f"{ref_13[1]}g")
                tela_macros.alimento_ref_35.setText(f"{ref_14[0]}")
                tela_macros.quanti_ref_35.setText(f"{ref_14[1]}g")
                tela_macros.alimento_ref_36.setText(f"{ref_15[0]}")
                tela_macros.quanti_ref_36.setText(f"{ref_15[1]}g")
        if ref6 != 0:
            if ref6 == 1:
                tabelas_ref_6('1')
                ref_16 = refeicao6[0]
                tela_macros.alimento_ref_31.setText(f"{ref_16[0]}")
                tela_macros.quanti_ref_31.setText(f"{ref_16[1]}g")
            elif ref6 == 2:
                tabelas_ref_6('2')
                ref_16 = refeicao6[0]
                ref_17 = refeicao6[1]
                tela_macros.alimento_ref_31.setText(f"{ref_16[0]}")
                tela_macros.quanti_ref_31.setText(f"{ref_16[1]}g")
                tela_macros.alimento_ref_32.setText(f"{ref_17[0]}")
                tela_macros.quanti_ref_32.setText(f"{ref_17[1]}g")
            elif ref6 == 3:
                tabelas_ref_6('3')
                ref_16 = refeicao6[0]
                ref_17 = refeicao6[1]
                ref_18 = refeicao6[2]
                tela_macros.alimento_ref_37.setText(f"{ref_16[0]}")
                tela_macros.quanti_ref_37.setText(f"{ref_16[1]}g")
                tela_macros.alimento_ref_38.setText(f"{ref_17[0]}")
                tela_macros.quanti_ref_38.setText(f"{ref_17[1]}g")
                tela_macros.alimento_ref_40.setText(f"{ref_18[0]}")
                tela_macros.quanti_ref_40.setText(f"{ref_18[1]}g")
        tela_macros.Calorias.setText(f'{dieta[0]}')
        tela_macros.Objetivo.setText(f'{dieta[1]}')
        tela_macros.Peso.setText(f'{dieta[2]}')
        tela_macros.Altura.setText(f'{dieta[3]}')
        tela_macros.Idade.setText(f'{dieta[4]}')
        tela_macros.Genero.setText(f'{dieta[5]}')
        tela_macros.Nivel_atividade.setText(f'{dieta[6]}')
        tela_macros.Taxa_metabolica.setText(f'{dieta[7]}')

def remover_refeicao_cliente():
    remover_ref = banco.buscar_refeicao_por_id(usuario_1.id)
    if remover_ref == None or len(remover_ref) == 0:
        tela_aviso.show()
        tela_aviso.label.setText(f"Você não possue refeição")
    else:
        remover_ref = banco.remover_refeicao_po_usuario(usuario_1.id)
        tela_aviso.show()
        tela_aviso.label.setText(f"Refeição deletada")
        limpar_tabela_ref_1()
        limpar_tabela_ref_2()
        limpar_tabela_ref_3()
        limpar_tabela_ref_4()
        limpar_tabela_ref_5()
        limpar_tabela_ref_6()
        tabelas_ref_1("0")
        tabelas_ref_2("0")
        tabelas_ref_3("0")
        tabelas_ref_4("0")
        tabelas_ref_5("0")
        tabelas_ref_6("0")
        limpar_labels()
        
def logout_tela_dieta():
    tela_macros.close()
    tela_conexoes.show()
    limpar_ref_1()
    limpar_ref_2()
    limpar_ref_3()
    limpar_ref_4()
    limpar_ref_5()
    limpar_ref_6()
    limpar_tabela_ref_1()
    limpar_tabela_ref_2()
    limpar_tabela_ref_3()
    limpar_tabela_ref_4()
    limpar_tabela_ref_5()
    limpar_tabela_ref_6()
    tabelas_ref_1("0")
    tabelas_ref_2("0")
    tabelas_ref_3("0")
    tabelas_ref_4("0")
    tabelas_ref_5("0")
    tabelas_ref_6("0")
    limpar_labels()

def calculos_calorico(soma_1 = 0, soma_2 = 0, soma_3 = 0, soma_4 = 0, soma_5 = 0, soma_6 = 0):
    total = soma_1 + soma_2 + soma_3 + soma_4 + soma_5 + soma_6
    calorias = banco.buscar_dieta(usuario_1.id)
    tela_macros.calorias_total_2.setText(f'{round(calorias[3])}')
    if total > calorias[3]:
        tela_aviso.show()
        tela_aviso.label.setText(f"Você ultrapassou as Calorias")
    else:
        tela_aviso.show()
        tela_aviso.label.setText(f"Diéta Inserida")
        limpar_ref_1()
        limpar_ref_2()
        limpar_ref_3()
        limpar_ref_4()
        limpar_ref_5()
        limpar_ref_6()
        limpar_tabela_ref_1()
        limpar_tabela_ref_2()
        limpar_tabela_ref_3()
        limpar_tabela_ref_4()
        limpar_tabela_ref_5()
        limpar_tabela_ref_6()
        tabelas_ref_1("0")
        tabelas_ref_2("0")
        tabelas_ref_3("0")
        tabelas_ref_4("0")
        tabelas_ref_5("0")
        tabelas_ref_6("0")
        limpar_labels()


def tabelas_ref_1(quantidade):
    if quantidade == '0':
        tela_macros.widget_5.hide()
        tela_macros.widget_8.hide()
        tela_macros.widget_7.hide()
        tela_macros.widget_9.hide()
    elif quantidade=='1':
        tela_macros.widget_5.show()
        tela_macros.widget_8.hide()
        tela_macros.widget_7.hide()
        tela_macros.widget_9.show()
    elif quantidade=='2':
        tela_macros.widget_5.show()
        tela_macros.widget_8.show()
        tela_macros.widget_7.hide()
        tela_macros.widget_9.show()
    elif quantidade=='3':
        tela_macros.widget_5.show()
        tela_macros.widget_8.show()
        tela_macros.widget_7.show()
        tela_macros.widget_9.show()

def tabelas_ref_2(quantidade):
    if quantidade == '0':
        tela_macros.widget_6.hide()
        tela_macros.widget_10.hide()
        tela_macros.widget_11.hide()
        tela_macros.widget_12.hide()
    elif quantidade == '1':
        tela_macros.widget_6.show()
        tela_macros.widget_10.hide()
        tela_macros.widget_11.hide()
        tela_macros.widget_12.show()
    elif quantidade == '2':
        tela_macros.widget_6.show()
        tela_macros.widget_10.show()
        tela_macros.widget_11.hide()
        tela_macros.widget_12.show()
    elif quantidade == '3':
        tela_macros.widget_6.show()
        tela_macros.widget_10.show()
        tela_macros.widget_11.show()
        tela_macros.widget_12.show()

def tabelas_ref_3(quantidade):
    if quantidade == '0':
        tela_macros.widget_14.hide()
        tela_macros.widget_15.hide()
        tela_macros.widget_16.hide()
        tela_macros.widget_13.hide()
    elif quantidade == '1':
        tela_macros.widget_14.show()
        tela_macros.widget_15.hide()
        tela_macros.widget_16.hide()
        tela_macros.widget_13.show()
    elif quantidade == '2':
        tela_macros.widget_14.show()
        tela_macros.widget_15.show()
        tela_macros.widget_16.hide()
        tela_macros.widget_13.show()
    elif quantidade == '3':
        tela_macros.widget_14.show()
        tela_macros.widget_15.show()
        tela_macros.widget_16.show()
        tela_macros.widget_13.show()

def tabelas_ref_4(quantidade):
    if quantidade == '0':
        tela_macros.widget_17.hide()
        tela_macros.widget_19.hide()
        tela_macros.widget_20.hide()
        tela_macros.widget_18.hide()
    elif quantidade == '1':
        tela_macros.widget_17.show()
        tela_macros.widget_19.hide()
        tela_macros.widget_20.hide()
        tela_macros.widget_18.show()
    elif quantidade == '2':
        tela_macros.widget_17.show()
        tela_macros.widget_19.show()
        tela_macros.widget_20.hide()
        tela_macros.widget_18.show()
    elif quantidade == '3':
        tela_macros.widget_17.show()
        tela_macros.widget_19.show()
        tela_macros.widget_20.show()
        tela_macros.widget_18.show()

def tabelas_ref_5(quantidade):
    if quantidade == '0':
        tela_macros.widget_21.hide()
        tela_macros.widget_22.hide()
        tela_macros.widget_23.hide()
        tela_macros.widget_24.hide()
    elif quantidade == '1':
        tela_macros.widget_21.show()
        tela_macros.widget_22.hide()
        tela_macros.widget_23.hide()
        tela_macros.widget_24.show()
    elif quantidade == '2':
        tela_macros.widget_21.show()
        tela_macros.widget_22.show()
        tela_macros.widget_23.hide()
        tela_macros.widget_24.show()
    elif quantidade == '3':
        tela_macros.widget_21.show()
        tela_macros.widget_22.show()
        tela_macros.widget_23.show()
        tela_macros.widget_24.show()

def tabelas_ref_6(quantidade):
    if quantidade == '0':
        tela_macros.widget_25.hide()
        tela_macros.widget_26.hide()
        tela_macros.widget_27.hide()
        tela_macros.widget_28.hide()
    elif quantidade == '1':
        tela_macros.widget_25.show()
        tela_macros.widget_26.hide()
        tela_macros.widget_27.hide()
        tela_macros.widget_28.show()
    elif quantidade == '2':
        tela_macros.widget_25.show()
        tela_macros.widget_26.show()
        tela_macros.widget_27.hide()
        tela_macros.widget_28.show()
    elif quantidade == '3':
        tela_macros.widget_25.show()
        tela_macros.widget_26.show()
        tela_macros.widget_27.show()
        tela_macros.widget_28.show()

def limpar_tabela_ref_1():
    tela_macros.alimento_ref_19.clear()
    tela_macros.quanti_ref_19.clear()
    tela_macros.alimento_ref_20.clear()
    tela_macros.quanti_ref_20.clear()
    tela_macros.alimento_ref_21.clear()
    tela_macros.quanti_ref_21.clear()

def limpar_tabela_ref_2():
    tela_macros.alimento_ref_23.clear()
    tela_macros.quanti_ref_23.clear()
    tela_macros.alimento_ref_22.clear()
    tela_macros.quanti_ref_22.clear()
    tela_macros.alimento_ref_24.clear()
    tela_macros.quanti_ref_24.clear()

def limpar_tabela_ref_3():
    tela_macros.alimento_ref_25.clear()
    tela_macros.quanti_ref_25.clear()
    tela_macros.alimento_ref_26.clear()
    tela_macros.quanti_ref_26.clear()
    tela_macros.alimento_ref_27.clear()
    tela_macros.quanti_ref_27.clear()

def limpar_tabela_ref_4():
    tela_macros.alimento_ref_31.clear()
    tela_macros.quanti_ref_31.clear()
    tela_macros.alimento_ref_32.clear()
    tela_macros.quanti_ref_32.clear()
    tela_macros.alimento_ref_33.clear()
    tela_macros.quanti_ref_33.clear()

def limpar_tabela_ref_5():
    tela_macros.alimento_ref_34.clear()
    tela_macros.quanti_ref_34.clear()
    tela_macros.alimento_ref_35.clear()
    tela_macros.quanti_ref_35.clear()
    tela_macros.alimento_ref_36.clear()
    tela_macros.quanti_ref_36.clear()

def limpar_tabela_ref_6():
    tela_macros.alimento_ref_37.clear()
    tela_macros.quanti_ref_37.clear()
    tela_macros.alimento_ref_38.clear()
    tela_macros.quanti_ref_38.clear()
    tela_macros.alimento_ref_40.clear()
    tela_macros.quanti_ref_40.clear()  

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=
if __name__ == "__main__":

    qt = QtWidgets.QApplication(sys.argv)

    # Classes
    usuario_1 = Usuario()
    cliente_1 = Cliente()
    macros_1 = Macros()
    alimentos_1 = Alimentos()
    tmb_1 = Tmb()
    # Telas
    tela_logar =uic.loadUi('tela_logar.ui')
    tela_aviso = uic.loadUi('tela_aviso.ui')
    tela_adm = uic.loadUi('tela_adm.ui')
    tela_cliente = uic.loadUi('tela_cliente.ui')
    tela_introduçao=uic.loadUi('tela_introduçao.ui')
    tela_cutting=uic.loadUi("tela_cutting.ui")
    tela_bulking=uic.loadUi("tela_bulking.ui")
    tela_manter=uic.loadUi("tela_manter_peso.ui")
    tela_conexoes=uic.loadUi('tela_conexoes.ui')
    tela_macros=uic.loadUi('tela_macros_usuarios.ui')

    # Tela para iniciar
    tela_logar.show()

    # BTN logar
    tela_logar.btnLogar.clicked.connect(logar)
    # BTN adm
    tela_adm.btnCadastrar.clicked.connect(cadastrar_login_senha_temporario)
    tela_adm.btnBuscar.clicked.connect(buscar_cliente_por_nome)
    tela_adm.btnLogout.clicked.connect(logout_tela_adm)
    tela_adm.btnLogout_4.clicked.connect(logout_tela_adm_usuario)
    tela_adm.btnExcluir.clicked.connect(excluir_cliente)
    # BTN conexões
    tela_conexoes.btn_atualizaao_dados.clicked.connect(atualizar)
    tela_conexoes.btn_inicio.clicked.connect(inicio)
    tela_conexoes.btn_rever.clicked.connect(rever_dieta)
    tela_conexoes.btnLogout.clicked.connect(logout_tela_conexoes)
    # BTN cliente
    tela_cliente.btnCriar.clicked.connect(cadastrar_usuario_cliente)
    tela_cliente.btnAtualizar.clicked.connect(atualizar_dados_cliente)
    tela_cliente.btnLogout.clicked.connect(logout_tela_cliente)
    # BTN cutting
    tela_cutting.btngerartmb.clicked.connect(gerar_tmb_cutting)
    tela_cutting.btnLogout.clicked.connect(logout_tela_cutting)
    tela_cutting.transicao_macro.clicked.connect(abrir_macros)
    tela_cutting.comboatividade.addItems(["Sedentario","Ativo","Bastante Ativo"])
    tela_cutting.btnAtualizar.clicked.connect(atualizar_cutting)
    # BTN bulking
    tela_bulking.BtngerarTBM.clicked.connect(gerar_tmb_bulking)
    tela_bulking.btnLogout.clicked.connect(logout_tela_bulking)
    tela_bulking.transicao_macro.clicked.connect(abrir_macros)
    tela_bulking.comboatividade.addItems(["Sedentario","Ativo","Bastante Ativo"])
    tela_bulking.btnAtualizar.clicked.connect(atualizar_Bulking)
    # BTN manter
    tela_manter.BtngerarTBM.clicked.connect(gerar_tmb_manter)
    tela_manter.btnLogout.clicked.connect(logout_tela_manter)
    tela_manter.transicao_macro.clicked.connect(abrir_macros)
    tela_manter.comboatividade.addItems(["Sedentario","Ativo","Bastante Ativo"])
    tela_manter.btnAtualizar.clicked.connect(atualizar_manter)
    # BTN introdução
    tela_introduçao.comandocutting.clicked.connect(escolha_cutting)
    tela_introduçao.comandobulking.clicked.connect(escolha_bulking)
    tela_introduçao.comandomanter.clicked.connect(escolha_manter)
    tela_introduçao.btnLogout.clicked.connect(logout_tela_introducao)
    # BTN aviso
    tela_aviso.avisado.clicked.connect(avisador)
    # BTN macro
    tela_macros.exp_prot.clicked.connect(proteinas_explicaçao)
    tela_macros.exp_carb.clicked.connect(carboidratos_explicaçao)
    tela_macros.exp_gord.clicked.connect(gordura_explicaçao)
    tela_macros.btnLogout.clicked.connect(logout_tela_macros)
    tela_macros.quantidade_de_refeicao.addItems(['2','3','4','5','6'])
    tela_macros.btn_ok.clicked.connect(quantidae_de_refeições)
    tela_macros.btn_calcular_ref.clicked.connect(calcular_ref_1)
    tela_macros.btn_calcular_ref_2.clicked.connect(calcular_ref_2)
    tela_macros.btn_calcular_ref_3.clicked.connect(calcular_ref_3)
    tela_macros.btn_calcular_ref_4.clicked.connect(calcular_ref_4)
    tela_macros.btn_calcular_ref_5.clicked.connect(calcular_ref_5)
    tela_macros.btn_calcular_ref_6.clicked.connect(calcular_ref_6)
    tela_macros.btn_buscar.clicked.connect(buscar_alimento_por_nome)
    tela_macros.btn_Adicionar.clicked.connect(adicionar_alimento_por_nome)
    tela_macros.btn_buscar_2.clicked.connect(imprimir_dieta_por_usuario)
    tela_macros.btn_criar_dieta.clicked.connect(inserir_todas_as_refeicoes)
    tela_macros.btnLogout_2.clicked.connect(logout_tela_dieta)
    tela_macros.btn_excluir.clicked.connect(remover_refeicao_cliente)
    tela_macros.btn_limpar.clicked.connect(limpar_ref_1)
    tela_macros.btn_limpar_2.clicked.connect(limpar_ref_2)
    tela_macros.btn_limpar_3.clicked.connect(limpar_ref_3)
    tela_macros.btn_limpar_4.clicked.connect(limpar_ref_4)
    tela_macros.btn_limpar_5.clicked.connect(limpar_ref_5)
    tela_macros.btn_limpar_6.clicked.connect(limpar_ref_6)
    qt.exec_()
