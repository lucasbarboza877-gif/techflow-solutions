from flask import Blueprint, request, jsonify
from models import Task

tarefas_bp = Blueprint('tarefas', __name__)


@tarefas_bp.route('/tarefas', methods=['GET'])
def listar_tarefas():
    """Lista todas as tarefas. Aceita filtros por status e prioridade."""
    status = request.args.get('status')
    prioridade = request.args.get('prioridade')

    if status:
        tarefas = Task.filtrar_por_status(status)
    elif prioridade:
        tarefas = Task.filtrar_por_prioridade(prioridade)
    else:
        tarefas = Task.listar_todas()

    return jsonify({'tarefas': tarefas, 'total': len(tarefas)}), 200


@tarefas_bp.route('/tarefas/<int:tarefa_id>', methods=['GET'])
def buscar_tarefa(tarefa_id):
    """Busca uma tarefa específica pelo ID."""
    tarefa = Task.buscar_por_id(tarefa_id)
    if tarefa is None:
        return jsonify({'erro': 'Tarefa não encontrada'}), 404
    return jsonify(tarefa), 200


@tarefas_bp.route('/tarefas', methods=['POST'])
def criar_tarefa():
    """Cria uma nova tarefa."""
    dados = request.get_json()

    if not dados or 'titulo' not in dados:
        return jsonify({'erro': 'O campo título é obrigatório'}), 400

    try:
        tarefa_id = Task.criar(
            titulo=dados['titulo'],
            descricao=dados.get('descricao', ''),
            status=dados.get('status', 'a_fazer'),
            prioridade=dados.get('prioridade', 'media')
        )
        tarefa = Task.buscar_por_id(tarefa_id)
        return jsonify({'mensagem': 'Tarefa criada com sucesso!', 'tarefa': tarefa}), 201

    except ValueError as e:
        return jsonify({'erro': str(e)}), 400


@tarefas_bp.route('/tarefas/<int:tarefa_id>', methods=['PUT'])
def atualizar_tarefa(tarefa_id):
    """Atualiza os dados de uma tarefa existente."""
    dados = request.get_json()

    if not dados:
        return jsonify({'erro': 'Nenhum dado enviado para atualização'}), 400

    try:
        Task.atualizar(
            tarefa_id=tarefa_id,
            titulo=dados.get('titulo'),
            descricao=dados.get('descricao'),
            status=dados.get('status'),
            prioridade=dados.get('prioridade')
        )
        tarefa = Task.buscar_por_id(tarefa_id)
        return jsonify({'mensagem': 'Tarefa atualizada com sucesso!', 'tarefa': tarefa}), 200

    except ValueError as e:
        return jsonify({'erro': str(e)}), 404


@tarefas_bp.route('/tarefas/<int:tarefa_id>', methods=['DELETE'])
def deletar_tarefa(tarefa_id):
    """Remove uma tarefa do sistema."""
    try:
        Task.deletar(tarefa_id)
        return jsonify({'mensagem': f'Tarefa {tarefa_id} removida com sucesso!'}), 200
    except ValueError as e:
        return jsonify({'erro': str(e)}), 404


# --- nova rota adicionada após mudança de escopo ---
@tarefas_bp.route('/estatisticas', methods=['GET'])
def estatisticas():
    """
    Retorna um resumo das tarefas por status e prioridade.
    Essa rota foi adicionada como parte da mudança de escopo solicitada pelo cliente.
    """
    todas = Task.listar_todas()

    resumo = {
        'total': len(todas),
        'por_status': {
            'a_fazer': len([t for t in todas if t['status'] == 'a_fazer']),
            'em_progresso': len([t for t in todas if t['status'] == 'em_progresso']),
            'concluido': len([t for t in todas if t['status'] == 'concluido']),
        },
        'por_prioridade': {
            'alta': len([t for t in todas if t['prioridade'] == 'alta']),
            'media': len([t for t in todas if t['prioridade'] == 'media']),
            'baixa': len([t for t in todas if t['prioridade'] == 'baixa']),
        }
    }

    return jsonify(resumo), 200


 

