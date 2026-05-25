# 📋 TechFlow Solutions - Sistema de Gerenciamento de Tarefas

Este repositório contém o projeto prático desenvolvido para a disciplina de Engenharia de Software da UniFECAF. O objetivo é aplicar conceitos de versionamento de código com Git, gerência de configuração, testes automatizados e esteira de CI/CD.

## 🚀 1. Descrição do Projeto e Escopo Inicial
A *TechFlow Solutions* é uma empresa especializada em soluções de software contratada para desenvolver um *Sistema de Gerenciamento de Tarefas* para uma startup de logística que busca uma plataforma para acompanhar o fluxo de trabalho em tempo real, priorizar tarefas críticas e monitorar o desempenho da equipe.

O escopo inicial contempla uma aplicação web em Python contendo um CRUD completo (Create, Read, Update, Delete) para as tarefas.

## 🔄 2. Metodologia Ágil e Organização (Kanban)
Utilizou-se a metodologia ágil *Kanban, integrada através do **GitHub Projects* com as colunas fundamentais: A Fazer (To Do), Em Progresso (In Progress) e Concluído (Done).

## 🧪 3. Controle de Qualidade e Integração Contínua (CI)
O projeto conta com um pipeline de *Integração Contínua (CI)* configurado via *GitHub Actions* em .github/workflows/ci.yml que instala as dependências do requirements.txt e executa testes estruturais com o framework *PyTest*.

## ⚠️ 4. Gestão de Mudanças (Mudança de Escopo)
*Justificativa:* Durante o ciclo de validação, a startup de logística identificou a necessidade de filtrar as ordens de serviço por impacto operacional. Para mitigar isso, foi aprovada uma *mudança de escopo* para incluir um campo obrigatório de *"Prioridade"* (Alta, Média, Baixa) na criação de cada tarefa.
