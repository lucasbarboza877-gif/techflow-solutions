import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import database
from database import inicializar_banco
from models import Task

@pytest.fixture(autouse=True)
def limpar_banco(tmp_path, monkeypatch):
    db_temp = str(tmp_path / 'test_taskflow.db')
    monkeypatch.setattr(database, 'DB_PATH', db_temp)
    inicializar_banco()
    yield

# ========================
# TESTES DE CRIAÇÃO
# ========================

def test_criar_tarefa_basica():
    id_tarefa = Task.criar(titulo='Implementar login')
    assert id_tarefa is not None and id_tarefa > 0


def test_criar_tarefa_completa():
    id_tarefa = Task.criar(
        titulo='Criar CRUD de tarefas',
        descricao='Desenvolver endpoints de criação, leitura, update e delete',
        status='em_progresso',
        prioridade='alta'
    )
    tarefa = Task.buscar_por_id(id_tarefa)
    assert tarefa['titulo'] == 'Criar CRUD de tarefas'
    assert tarefa['status'] == 'em_progresso'
    assert tarefa['prioridade'] == 'alta'


def test_criar_tarefa_sem_titulo_levanta_erro():
    with pytest.raises(ValueError, match='título'):
        Task.criar(titulo='')


def test_criar_tarefa_titulo_so_espacos():
    with pytest.raises(ValueError):
        Task.criar(titulo='   ')


def test_criar_tarefa_status_invalido():
    with pytest.raises(ValueError, match='Status'):
        Task.criar(titulo='Teste', status='nao_existe')


def test_criar_tarefa_prioridade_invalida():
    with pytest.raises(ValueError, match='Prioridade'):
        Task.criar(titulo='Teste', prioridade='urgentissima')


# ========================
# TESTES DE LEITURA
# ========================

def test_listar_tarefas_vazia():
    assert Task.listar_todas() == []


def test_listar_tarefas_com_dados():
    Task.criar('Tarefa 1')
    Task.criar('Tarefa 2')
    Task.criar('Tarefa 3')
    assert len(Task.listar_todas()) == 3


def test_buscar_por_id_existente():
    id_tarefa = Task.criar('Minha tarefa especial')
    tarefa = Task.buscar_por_id(id_tarefa)
    assert tarefa is not None
    assert tarefa['id'] == id_tarefa
    assert tarefa['titulo'] == 'Minha tarefa especial'


def test_buscar_por_id_inexistente():
    assert Task.buscar_por_id(9999) is None


# ========================
# TESTES DE ATUALIZAÇÃO
# ========================

def test_atualizar_status():
    id_tarefa = Task.criar('Tarefa para mover', status='a_fazer')
    Task.atualizar(id_tarefa, status='em_progresso')
    assert Task.buscar_por_id(id_tarefa)['status'] == 'em_progresso'


def test_atualizar_prioridade():
    id_tarefa = Task.criar('Tarefa urgente', prioridade='baixa')
    Task.atualizar(id_tarefa, prioridade='alta')
    assert Task.buscar_por_id(id_tarefa)['prioridade'] == 'alta'


def test_atualizar_tarefa_inexistente():
    with pytest.raises(ValueError):
        Task.atualizar(9999, titulo='Nao existe')


# ========================
# TESTES DE DELEÇÃO
# ========================

def test_deletar_tarefa():
    id_tarefa = Task.criar('Tarefa para deletar')
    Task.deletar(id_tarefa)
    assert Task.buscar_por_id(id_tarefa) is None


def test_deletar_tarefa_inexistente():
    with pytest.raises(ValueError):
        Task.deletar(9999)


# ========================
# TESTES DE FILTRO
# ========================

def test_filtrar_por_status():
    Task.criar('Tarefa A', status='a_fazer')
    Task.criar('Tarefa B', status='a_fazer')
    Task.criar('Tarefa C', status='em_progresso')
    assert len(Task.filtrar_por_status('a_fazer')) == 2


def test_filtrar_por_prioridade():
    Task.criar('Urgente 1', prioridade='alta')
    Task.criar('Urgente 2', prioridade='alta')
    Task.criar('Normal', prioridade='media')
    assert len(Task.filtrar_por_prioridade('alta')) == 2


# ========================
# TESTES DE FLUXO COMPLETO (novo)
# ========================

def test_ciclo_completo_tarefa():
    """Testa o fluxo completo: criar -> mover -> concluir -> deletar."""
    # cria
    id_tarefa = Task.criar('Feature completa', prioridade='alta')

    # move para em progresso
    Task.atualizar(id_tarefa, status='em_progresso')
    assert Task.buscar_por_id(id_tarefa)['status'] == 'em_progresso'

    # conclui
    Task.atualizar(id_tarefa, status='concluido')
    assert Task.buscar_por_id(id_tarefa)['status'] == 'concluido'

    # deleta
    Task.deletar(id_tarefa)
    assert Task.buscar_por_id(id_tarefa) is None
