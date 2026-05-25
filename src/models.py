from database import get_conexao

class Task:
    """
    Modelo que representa uma Tarefa no sistema.
    Atributos:
        id         - identificador único (gerado automaticamente)
        titulo     - nome da tarefa (obrigatório)
        descricao  - detalhes da tarefa (opcional)
        status     - estado atual: 'a_fazer', 'em_progresso' ou 'concluido'
        prioridade - nível de urgência: 'alta', 'media' ou 'baixa'
    """

    STATUS_VALIDOS = ['a_fazer', 'em_progresso', 'concluido']
    PRIORIDADES_VALIDAS = ['alta', 'media', 'baixa']

    def __init__(self, id=None, titulo='', descricao='', status='a_fazer', prioridade='media'):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.status = status
        self.prioridade = prioridade

    @staticmethod
    def criar(titulo, descricao='', status='a_fazer', prioridade='media'):
        """Cria uma nova tarefa no banco de dados."""
        if not titulo or titulo.strip() == '':
            raise ValueError("O título da tarefa não pode ser vazio.")

        if status not in Task.STATUS_VALIDOS:
            raise ValueError(f"Status inválido. Use um dos seguintes: {Task.STATUS_VALIDOS}")

        if prioridade not in Task.PRIORIDADES_VALIDAS:
            raise ValueError(f"Prioridade inválida. Use: {Task.PRIORIDADES_VALIDAS}")

        conn = get_conexao()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tarefas (titulo, descricao, status, prioridade) VALUES (?, ?, ?, ?)',
            (titulo.strip(), descricao, status, prioridade)
        )
        conn.commit()
        tarefa_id = cursor.lastrowid
        conn.close()
        return tarefa_id

    @staticmethod
    def listar_todas():
        """Retorna todas as tarefas do banco de dados."""
        conn = get_conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tarefas ORDER BY criado_em DESC')
        linhas = cursor.fetchall()
        conn.close()
        return [dict(linha) for linha in linhas]

    @staticmethod
    def buscar_por_id(tarefa_id):
        """Busca uma tarefa específica pelo ID."""
        conn = get_conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tarefas WHERE id = ?', (tarefa_id,))
        linha = cursor.fetchone()
        conn.close()
        if linha is None:
            return None
        return dict(linha)

    @staticmethod
    def atualizar(tarefa_id, titulo=None, descricao=None, status=None, prioridade=None):
        """Atualiza os campos de uma tarefa existente."""
        tarefa = Task.buscar_por_id(tarefa_id)
        if tarefa is None:
            raise ValueError(f"Tarefa com ID {tarefa_id} não encontrada.")

        # mantém os valores antigos se nada for passado
        novo_titulo = titulo if titulo is not None else tarefa['titulo']
        nova_descricao = descricao if descricao is not None else tarefa['descricao']
        novo_status = status if status is not None else tarefa['status']
        nova_prioridade = prioridade if prioridade is not None else tarefa['prioridade']

        if novo_status not in Task.STATUS_VALIDOS:
            raise ValueError(f"Status inválido.")

        if nova_prioridade not in Task.PRIORIDADES_VALIDAS:
            raise ValueError(f"Prioridade inválida.")

        conn = get_conexao()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tarefas
            SET titulo = ?, descricao = ?, status = ?, prioridade = ?,
                atualizado_em = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (novo_titulo, nova_descricao, novo_status, nova_prioridade, tarefa_id))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def deletar(tarefa_id):
        """Remove uma tarefa do banco de dados."""
        tarefa = Task.buscar_por_id(tarefa_id)
        if tarefa is None:
            raise ValueError(f"Tarefa com ID {tarefa_id} não encontrada.")

        conn = get_conexao()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tarefas WHERE id = ?', (tarefa_id,))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def filtrar_por_status(status):
        """Filtra tarefas por status."""
        conn = get_conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tarefas WHERE status = ? ORDER BY criado_em DESC', (status,))
        linhas = cursor.fetchall()
        conn.close()
        return [dict(linha) for linha in linhas]

    @staticmethod
    def filtrar_por_prioridade(prioridade):
        """Filtra tarefas por prioridade."""
        conn = get_conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tarefas WHERE prioridade = ? ORDER BY criado_em DESC', (prioridade,))
        linhas = cursor.fetchall()
        conn.close()
        return [dict(linha) for linha in linhas]
