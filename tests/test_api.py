import sys
import os
import pytest
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# precisa do banco temporário antes de importar o app
import database

@pytest.fixture
def app(tmp_path, monkeypatch):
    """Cria uma instância do Flask com banco em memória para os testes de API."""
    db_temp = str(tmp_path / 'test_api.db')
    monkeypatch.setattr(database, 'DB_PATH', db_temp)
    database.inicializar_banco()

    from app import app as flask_app
    flask_app.config['TESTING'] = True
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()


def test_health_check(client):
    """Endpoint /api/health deve retornar status ok."""
    resp = client.get('/api/health')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['status'] == 'ok'


def test_post_criar_tarefa(client):
    """POST /api/tarefas deve criar uma tarefa e retornar 201."""
    payload = {'titulo': 'Tarefa via API', 'prioridade': 'alta'}
    resp = client.post('/api/tarefas', json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['tarefa']['titulo'] == 'Tarefa via API'


def test_post_sem_titulo_retorna_400(client):
    """POST sem título deve retornar 400."""
    resp = client.post('/api/tarefas', json={'descricao': 'sem titulo'})
    assert resp.status_code == 400


def test_get_listar_tarefas(client):
    """GET /api/tarefas deve listar todas as tarefas."""
    client.post('/api/tarefas', json={'titulo': 'T1'})
    client.post('/api/tarefas', json={'titulo': 'T2'})

    resp = client.get('/api/tarefas')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['total'] == 2


def test_get_tarefa_por_id(client):
    """GET /api/tarefas/<id> deve retornar a tarefa correta."""
    post_resp = client.post('/api/tarefas', json={'titulo': 'Busca por ID'})
    tarefa_id = post_resp.get_json()['tarefa']['id']

    resp = client.get(f'/api/tarefas/{tarefa_id}')
    assert resp.status_code == 200
    assert resp.get_json()['titulo'] == 'Busca por ID'


def test_get_tarefa_inexistente_retorna_404(client):
    """GET de ID inexistente deve retornar 404."""
    resp = client.get('/api/tarefas/9999')
    assert resp.status_code == 404


def test_put_atualizar_tarefa(client):
    """PUT deve atualizar os campos da tarefa."""
    post_resp = client.post('/api/tarefas', json={'titulo': 'Antes'})
    tarefa_id = post_resp.get_json()['tarefa']['id']

    resp = client.put(f'/api/tarefas/{tarefa_id}', json={
        'titulo': 'Depois',
        'status': 'concluido'
    })
    assert resp.status_code == 200
    data = resp.get_json()['tarefa']
    assert data['titulo'] == 'Depois'
    assert data['status'] == 'concluido'


def test_delete_tarefa(client):
    """DELETE deve remover a tarefa."""
    post_resp = client.post('/api/tarefas', json={'titulo': 'Vai sumir'})
    tarefa_id = post_resp.get_json()['tarefa']['id']

    del_resp = client.delete(f'/api/tarefas/{tarefa_id}')
    assert del_resp.status_code == 200

    get_resp = client.get(f'/api/tarefas/{tarefa_id}')
    assert get_resp.status_code == 404


def test_filtro_por_status(client):
    """GET com ?status= deve filtrar corretamente."""
    client.post('/api/tarefas', json={'titulo': 'A', 'status': 'a_fazer'})
    client.post('/api/tarefas', json={'titulo': 'B', 'status': 'concluido'})

    resp = client.get('/api/tarefas?status=a_fazer')
    data = resp.get_json()
    assert data['total'] == 1
    assert data['tarefas'][0]['status'] == 'a_fazer'
