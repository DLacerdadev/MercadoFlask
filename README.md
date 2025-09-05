# ERP Sistema de Mercado

Um sistema ERP simples e completo para gerenciamento de mercados, desenvolvido com Flask e SQLite.

## Funcionalidades

### 🔐 Autenticação
- Sistema de login seguro
- Sessão de usuário com proteção de rotas

### 📦 Gestão de Produtos
- Cadastro, edição e exclusão de produtos
- Controle de categorias e preços
- Sistema de busca e filtros

### 📊 Controle de Estoque
- Visualização em tempo real do estoque
- Alertas de estoque baixo
- Atualização automática após vendas e compras

### 🛒 Gestão de Compras
- Registro de compras com fornecedor
- Entrada automática no estoque
- Histórico completo de compras

### 💰 Gestão de Vendas
- Registro de vendas com validação de estoque
- Saída automática do estoque
- Histórico de vendas por período

### 📈 Relatórios
- Dashboard com métricas principais
- Vendas diárias e mensais
- Produtos mais vendidos
- Relatórios de movimentação

## Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Banco de Dados**: SQLite
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Ícones**: Font Awesome

## Como Executar

### 1. Instalação das Dependências

```bash
pip install flask flask-sqlalchemy werkzeug
