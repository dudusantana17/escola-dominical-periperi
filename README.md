# 📖 Escola Dominical — Ala Periperi

Sistema web interativo desenvolvido em Python com **Streamlit**, **SQLite** e inteligência artificial (**Google Gemini**) para o estudo semanal das escrituras e princípios do evangelho na Escola Dominical da **Ala Periperi**.

> *"Venham e Aprendam Comigo" (Mateus 11:28-30)*

---

## 🚀 Como Executar o Sistema

### 1. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 2. Inicie a Aplicação Streamlit
```bash
streamlit run app.py
```
O sistema abrirá automaticamente no seu navegador em `http://localhost:8501`.

---

## 🏛️ Arquitetura e Recursos

1. **Persistência SQLite (`escola_dominical_periperi.db`)**:
   - Tabela `questoes`: Armazena livro/tema, capítulo/lição, enunciado, 4 opções em JSON (`A`, `B`, `C`, `D`), resposta correta e explicação com referência das escrituras.
   - Tabela `ranking`: Histórico de estudos realizados com nome do aluno, tema, acertos, total, aproveitamento (%) e data/hora.
   - **Sementes Iniciais**: Inicialização automática com 5 questões autênticas das escrituras (1 Néfi 3, Mateus 5, Mosias 2, Alma 32 e Morôni 10).

2. **Design Visual Personalizado**:
   - Paleta serena de tons de azul (`#1a365d`, `#2b6cb0`) e dourado suave (`#d69e2e`, `#fbf7ee`).
   - Banner acolhedor da congregação.
   - Galeria responsiva conectada à pasta `assets/`, com fallback elegante quando vazia.

3. **Módulos do Sistema**:
   - **Aba 1 (Estudo & Quiz)**:
     - Identificação do aluno.
     - Filtros por Tema e Lição.
     - Cartões de perguntas com botões de rádio e submissão.
     - Gabarito comentado com explicações doutrinárias e referências escriturísticas.
     - Gravação automática de tentativas no banco de dados.
   - **Aba 2 (Quadro de Destaque)**:
     - Pódio estilizado Top 3 (🥇 1º Lugar, 🥈 2º Lugar, 🥉 3º Lugar).
     - Estatísticas da classe (total de tentativas, alunos únicos, média da ala e recorde).
     - Tabela de classificação com barra de progresso e filtro por tema.
   - **Aba 3 (Área do Professor)**:
     - Acesso protegido por senha: **`periperi2026`**.
     - **Cadastro Manual**: Formulário completo para novas perguntas.
     - **Importação via PDF com Gemini IA (`google-genai` e `pypdf`)**: Extração de texto e geração de perguntas automatizadas diretamente pelo Gemini 2.5 Flash.
     - **Gerenciamento de Questões**: Tabela completa com remoção de itens pelo ID.
     - **Gerenciamento de Fotos**: Upload de novas imagens diretamente para a pasta `assets/`.

---

## 🔒 Segurança e Segredos
- O arquivo `.gitignore` já vem configurado para proteger o banco de dados SQLite local, credenciais, segredos do Streamlit e chaves de API (`.env`).
