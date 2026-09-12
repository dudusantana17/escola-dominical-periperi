import streamlit as st
import sqlite3
import json
import os
from datetime import datetime
from PIL import Image

# =======================================================
# 1. CONFIGURAÇÃO DE PÁGINA
# =======================================================
st.set_page_config(
    page_title="Escola Dominical — Ala Periperi",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =======================================================
# 2. DESIGN VISUAL E CSS REFINADO (A IGREJA DE JESUS CRISTO)
# =======================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1e293b;
    }

    .stApp {
        background-color: #f8fafc;
    }

    /* Cabeçalho Hero Institucional */
    .church-header {
        background: linear-gradient(135deg, #0b2545 0%, #133b68 60%, #1d4e89 100%);
        border-bottom: 3px solid #c5a059;
        color: #ffffff;
        padding: 32px 30px;
        border-radius: 14px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(11, 37, 69, 0.25);
        text-align: center;
    }
    .church-header .sub-sub {
        text-transform: uppercase;
        letter-spacing: 2.5px;
        font-size: 11px;
        font-weight: 600;
        color: #e2c275;
        margin-bottom: 8px;
    }
    .church-header h1 {
        font-family: 'Cinzel', serif;
        font-size: 32px;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin: 0;
        color: #ffffff;
    }
    .church-header p {
        font-size: 15px;
        color: #e2e8f0;
        margin-top: 10px;
        font-style: italic;
    }

    /* Cartões de Questão */
    .quiz-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 5px solid #133b68;
        border-radius: 12px;
        padding: 22px 24px;
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }
    .quiz-title {
        font-weight: 700;
        color: #0b2545;
        font-size: 16px;
        margin-bottom: 8px;
    }

    /* Alternativas de Resposta (stRadio) */
    div[data-testid="stRadio"] > div {
        gap: 10px;
    }
    div[data-testid="stRadio"] label {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        padding: 12px 18px !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
        cursor: pointer;
        width: 100%;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }
    div[data-testid="stRadio"] label:hover {
        background: #f1f5f9 !important;
        border-color: #133b68 !important;
        transform: translateX(4px);
    }

    /* Botão Principal */
    .stButton > button {
        background: linear-gradient(135deg, #0b2545 0%, #133b68 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        letter-spacing: 0.3px !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        border: 1px solid #c5a059 !important;
        box-shadow: 0 4px 14px rgba(11, 37, 69, 0.2) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #133b68 0%, #1d4e89 100%) !important;
        box-shadow: 0 6px 20px rgba(11, 37, 69, 0.3) !important;
        color: #e2c275 !important;
        transform: translateY(-1px);
    }

    /* Cartões de Métricas */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 3px solid #c5a059;
        padding: 18px;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
    }

    /* Pódio do Ranking */
    .podio-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }
    .podio-pos { font-size: 32px; margin-bottom: 6px; }
    .podio-nome { font-weight: 700; font-size: 17px; color: #0b2545; }
    .podio-media { font-size: 22px; font-weight: 700; color: #133b68; margin-top: 4px; }
    </style>
""", unsafe_allow_html=True)

# =======================================================
# 3. BANCO DE DADOS (SQLite Local)
# =======================================================
DB_FILE = "escola_dominical_periperi.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS questoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livro_tema TEXT,
            capitulo_licao TEXT,
            enunciado TEXT,
            opcoes_json TEXT,
            correta TEXT,
            explicacao_referencia TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS ranking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_aluno TEXT,
            tema TEXT,
            acertos INTEGER,
            total INTEGER,
            porcentagem REAL,
            data_hora TEXT
        )
    ''')

    c.execute("SELECT COUNT(*) FROM questoes")
    if c.fetchone()[0] == 0:
        questoes_iniciais = [
            (
                "Livro de Mórmon",
                "1 Néfi 3",
                "Qual foi a memorável resposta dada por Néfi quando seu pai, Leí, pediu para que ele retornasse a Jerusalém para buscar as placas de latão?",
                json.dumps({
                    "A": "Irei e farei as coisas que o Senhor ordenou, pois sei que Ele nunca dá ordens sem preparar um caminho.",
                    "B": "Pedirei um sinal ao Senhor para saber se essa jornada é verdadeiramente necessária.",
                    "C": "Iremos somente se nossos irmãos Lamã e Lemuel concordarem em liderar o caminho.",
                    "D": "Esperaremos até que as tribulações no deserto diminuam antes de regressarmos."
                }),
                "A",
                "1 Néfi 3:7 — “Eu irei e farei as coisas que o Senhor ordenou, porque sei que o Senhor nunca dá ordens aos filhos dos homens sem antes preparar um caminho para que possam cumprir o que lhes ordena.”"
            ),
            (
                "Livro de Mórmon",
                "Mosias 2",
                "Ao discursar de sua torre para o povo, o que o Rei Benjamim ensinou a respeito do serviço ao próximo?",
                json.dumps({
                    "A": "Quem serve ao próximo adquire méritos para ser exaltado sem esforço pessoal.",
                    "B": "Quando estais a serviço de vosso próximo, estais somente a serviço de vosso Deus.",
                    "C": "O serviço é exigido apenas daqueles que possuem abundância de bens materiais.",
                    "D": "Devemos servir unicamente aos que compartilham das nossas mesmas crenças."
                }),
                "B",
                "Mosias 2:17 — “E eis que vos digo estas coisas para que aprendais sabedoria; para que saibais que, quando estais a serviço de vosso próximo, estais somente a serviço de vosso Deus.”"
            ),
            (
                "Doutrina e Convênios",
                "Seção 19",
                "O que o Senhor nos ensina sobre o discipulado e a paz pessoal em Doutrina e Convênios 19:23?",
                json.dumps({
                    "A": "Buscai primeiro as riquezas do mundo para depois edificar a Sião.",
                    "B": "Aprendei de mim e ouvi minhas palavras; andai na mansidão de meu Espírito e tereis paz em mim.",
                    "C": "Não façais orações em segredo, mas proclamai vosso conhecimento publicamente.",
                    "D": "O conhecimento secular precede os mandamentos espirituais."
                }),
                "B",
                "D&C 19:23 — “Aprendei de mim e ouvi minhas palavras; andai na mansidão de meu Espírito e tereis paz em mim.”"
            ),
            (
                "Vem, e Segue-Me",
                "Princípios do Evangelho",
                "De acordo com Tiago 1:5, o que devemos fazer se tivermos falta de sabedoria?",
                json.dumps({
                    "A": "Guardar a dúvida em segredo para não demonstrar fraqueza.",
                    "B": "Pedir a Deus, que a todos dá liberalmente e nada censura, e ser-nos-á dada.",
                    "C": "Aguardar anos até que surja uma resposta espontânea.",
                    "D": "Consultar unicamente filosofias dos homens."
                }),
                "B",
                "Tiago 1:5 — “E se algum de vós tem falta de sabedoria, peça-a a Deus, que a todos dá liberalmente e nada censura, e ser-lhe-á dada.” Essa passagem motivou Joseph Smith a orar no Bosque Sagrado."
            )
        ]
        c.executemany('''
            INSERT INTO questoes (livro_tema, capitulo_licao, enunciado, opcoes_json, correta, explicacao_referencia)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', questoes_iniciais)

    conn.commit()
    conn.close()

init_db()

# =======================================================
# 4. CABEÇALHO HERO INSTITUCIONAL
# =======================================================
st.markdown("""
    <div class="church-header">
        <div class="sub-sub"></div>
        <h1>Escola Dominical — Ala Periperi</h1>
        <p>“Aprendei de mim e ouvi minhas palavras; andai na mansidão de meu Espírito e tereis paz em mim.” — D&C 19:23</p>
    </div>
""", unsafe_allow_html=True)

# Navegação do Sistema em Abas
aba_home, aba_quiz, aba_ranking, aba_professor = st.tabs([
    "🏠 Início & Galeria",
    "📖 Estudo & Quiz",
    "🏆 Quadro de Destaque",
    "🔐 Área da Presidência"
])

# =======================================================
# ABA 1: INÍCIO E GALERIA DE FOTOS
# =======================================================
with aba_home:
    st.subheader("Bem-vindos à Escola Dominical da Ala Periperi")
    st.write(
        "Este portal foi desenvolvido para apoiar nosso estudo semanal do evangelho, "
        "reforçar as escrituras e incentivar a preparação de cada membro para as aulas de domingo."
    )

    # Verificação e Exibição de Fotos da pasta assets/
    pasta_assets = "assets"
    fotos = []
    if os.path.exists(pasta_assets):
        fotos = [os.path.join(pasta_assets, f) for f in os.listdir(pasta_assets) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    st.divider()
    st.markdown("###  Vem e Segue-me")
    if fotos:
        colunas = st.columns(min(len(fotos), 3))
        for idx, foto_path in enumerate(fotos):
            col = colunas[idx % 3]
            try:
                img = Image.open(foto_path)
                nome_arq = os.path.splitext(os.path.basename(foto_path))[0].replace("_", " ").title()
                col.image(img, caption=nome_arq, use_container_width=True)
            except Exception:
                pass
    else:
        st.info("💡 **Dica:** Coloque fotos de nossa capela, da classe ou de atividades na pasta `assets/` do projeto para exibi-las aqui na página inicial.")

# =======================================================
# ABA 2: ESTUDO & QUIZ DO ALUNO
# =======================================================
with aba_quiz:
    st.subheader("Caderno de Estudos e Perguntas")
    col1, col2 = st.columns(2)

    with col1:
        nome_aluno = st.text_input("Seu Nome (ou Nome Completo):", placeholder="Ex: Irmão Souza / Taís")

    with col2:
        conn = sqlite3.connect(DB_FILE)
        temas = [r[0] for r in conn.cursor().execute("SELECT DISTINCT livro_tema FROM questoes").fetchall()]
        conn.close()
        tema_selecionado = st.selectbox("Livro / Programa:", temas if temas else ["Nenhum tema cadastrado"])

    if not nome_aluno:
        st.info("👆 Por favor, preencha o seu nome acima para iniciar as perguntas.")
    else:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT id, capitulo_licao, enunciado, opcoes_json, correta, explicacao_referencia FROM questoes WHERE livro_tema = ?", (tema_selecionado,))
        questoes = c.fetchall()
        conn.close()

        if not questoes:
            st.warning("Ainda não há perguntas cadastradas para este tema.")
        else:
            with st.form("form_estudo_dominical"):
                respostas_usuario = {}
                for idx, q in enumerate(questoes, 1):
                    q_id, capitulo, enunciado, opcoes_str, correta, explicacao = q
                    opcoes = json.loads(opcoes_str)

                    st.markdown(f"""
                        <div class="quiz-card">
                            <div class="quiz-title">📖 Pergunta {idx:02d} — {capitulo}</div>
                            <div style="font-size: 15px; line-height: 1.6;">{enunciado}</div>
                        </div>
                    """, unsafe_allow_html=True)

                    opcoes_formatadas = [f"{letra}) {texto}" for letra, texto in opcoes.items()]
                    escolha = st.radio(
                        label=f"Q_{q_id}",
                        options=opcoes_formatadas,
                        index=None,
                        key=f"quiz_{q_id}",
                        label_visibility="collapsed"
                    )
                    respostas_usuario[q_id] = {
                        "escolha": escolha[0] if escolha else None,
                        "correta": correta,
                        "explicacao": explicacao
                    }
                    st.write("")

                btn_enviar = st.form_submit_button("Concluir Estudo e Ver Resumo", use_container_width=True)

            if btn_enviar:
                faltando = [k for k, v in respostas_usuario.items() if v["escolha"] is None]
                if faltando:
                    st.error("⚠️ Você deixou perguntas em branco! Responda todas antes de finalizar.")
                else:
                    acertos = sum(1 for v in respostas_usuario.values() if v["escolha"] == v["correta"])
                    total = len(questoes)
                    porcentagem = round((acertos / total) * 100, 1)

                    # Gravar no SQLite
                    conn = sqlite3.connect(DB_FILE)
                    c = conn.cursor()
                    c.execute('''
                        INSERT INTO ranking (nome_aluno, tema, acertos, total, porcentagem, data_hora)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (nome_aluno.strip().title(), tema_selecionado, acertos, total, porcentagem, datetime.now().strftime("%d/%m/%Y %H:%M")))
                    conn.commit()
                    conn.close()

                    st.toast("Estudo salvo com sucesso!", icon="📖")
                    st.divider()
                    st.subheader("📊 Seu Desempenho")
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Acertos", f"{acertos} de {total}")
                    m2.metric("Aproveitamento", f"{porcentagem}%")
                    m3.metric("Mensagem", "Excelente estudo!" if porcentagem >= 70 else "Continue se aprofundando!")

                    st.subheader("📋 Gabarito e Escrituras de Referência")
                    for idx, q in enumerate(questoes, 1):
                        q_id, capitulo, enunciado, _, correta, explicacao = q
                        resp = respostas_usuario[q_id]
                        acertou = resp["escolha"] == resp["correta"]
                        icone = "✅" if acertou else "❌"

                        with st.expander(f"{icone} Pergunta {idx:02d} — Gabarito: {correta} (Sua resposta: {resp['escolha']})"):
                            st.write(f"**Pergunta:** {enunciado}")
                            st.info(f"**Referência & Reflexão:** {explicacao}")

# =======================================================
# ABA 3: QUADRO DE DESTAQUE (RANKING)
# =======================================================
with aba_ranking:
    st.subheader("Quadro de Participação e Destaque")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        SELECT 
            nome_aluno,
            COUNT(id) as total_estudos,
            SUM(acertos) as total_acertos,
            ROUND(AVG(porcentagem), 1) as media_aproveitamento
        FROM ranking
        GROUP BY nome_aluno
        ORDER BY media_aproveitamento DESC, total_acertos DESC
    ''')
    dados_ranking = c.fetchall()
    conn.close()

    if dados_ranking:
        st.write("")
        col_p1, col_p2, col_p3 = st.columns(3)
        if len(dados_ranking) >= 1:
            with col_p1:
                st.markdown(f"""
                    <div class="podio-card" style="border-top: 4px solid #d4af37;">
                        <div class="podio-pos">🥇</div>
                        <div class="podio-nome">{dados_ranking[0][0]}</div>
                        <div class="podio-media">{dados_ranking[0][3]}%</div>
                        <div style="font-size:12px; color:#64748b; margin-top:4px;">1º Lugar Geral</div>
                    </div>
                """, unsafe_allow_html=True)
        if len(dados_ranking) >= 2:
            with col_p2:
                st.markdown(f"""
                    <div class="podio-card" style="border-top: 4px solid #94a3b8;">
                        <div class="podio-pos">🥈</div>
                        <div class="podio-nome">{dados_ranking[1][0]}</div>
                        <div class="podio-media">{dados_ranking[1][3]}%</div>
                        <div style="font-size:12px; color:#64748b; margin-top:4px;">2º Lugar Geral</div>
                    </div>
                """, unsafe_allow_html=True)
        if len(dados_ranking) >= 3:
            with col_p3:
                st.markdown(f"""
                    <div class="podio-card" style="border-top: 4px solid #b45309;">
                        <div class="podio-pos">🥉</div>
                        <div class="podio-nome">{dados_ranking[2][0]}</div>
                        <div class="podio-media">{dados_ranking[2][3]}%</div>
                        <div style="font-size:12px; color:#64748b; margin-top:4px;">3º Lugar Geral</div>
                    </div>
                """, unsafe_allow_html=True)

        st.write("")
        tabela = []
        for pos, linha in enumerate(dados_ranking, 1):
            tabela.append({
                "Posição": f"{pos}º",
                "Membro / Aluno": linha[0],
                "Estudos Realizados": linha[1],
                "Acertos Totais": linha[2],
                "Média de Acertos": f"{linha[3]}%"
            })
        st.dataframe(tabela, use_container_width=True, hide_index=True)
    else:
        st.info("Ainda não há participações registradas. O ranking aparecerá aqui assim que os primeiros estudos forem realizados.")

# =======================================================
# ABA 4: ÁREA DO PROFESSOR (CADASTRO, IMPORTAÇÃO E IA)
# =======================================================
with aba_professor:
    st.subheader("Painel do Professor e Liderança")
    
    # Controle de sessão para login
    if "admin_logado" not in st.session_state:
        st.session_state.admin_logado = False

    if not st.session_state.admin_logado:
        with st.form("form_login_prof"):
            senha = st.text_input("Digite a senha do professor:", type="password")
            btn_entrar = st.form_submit_button("Acessar Painel", use_container_width=True)
            if btn_entrar:
                if senha.strip() == "periperi2026":
                    st.session_state.admin_logado = True
                    st.rerun()
                else:
                    st.error("Senha incorreta. Tente novamente.")
    else:
        col_ok, col_sair = st.columns([4, 1])
        col_ok.success("Acesso autorizado com sucesso!")
        if col_sair.button("Sair / Bloquear"):
            st.session_state.admin_logado = False
            st.rerun()

        # Três opções de alimentação de dados
        sub_tab1, sub_tab2, sub_tab3 = st.tabs([
            "📋 Importar Questões Prontas (PDF / Texto)",
            "⚡ Gerar Novas Questões da Matéria (IA)",
            "✍️ Cadastro Manual"
        ])

        # ----------------------------------------------------
        # SUB-ABA 1: IMPORTAR QUESTÕES JÁ FEITAS
        # ----------------------------------------------------
        with sub_tab1:
            st.markdown("#### Importar Questionário Pronto")
            st.write("Suba um PDF com perguntas prontas ou cole o texto. A IA vai apenas ler, estruturar e salvar no banco de dados.")

            tema_import = st.text_input("Livro / Tema:", placeholder="Ex: Livro de Mórmon ou Vem, e Segue-Me", key="imp_tema")
            cap_import = st.text_input("Capítulo / Lição:", placeholder="Ex: Alma 32 ou Lição 14", key="imp_cap")
            
            origem_import = st.radio("Como deseja enviar as questões prontas?", ["📄 Upload de PDF", "📝 Colar Texto"], horizontal=True)
            
            conteudo_texto = ""
            if origem_import == "📄 Upload de PDF":
                pdf_questoes = st.file_uploader("Selecione o PDF contendo as perguntas prontas:", type=["pdf"], key="pdf_pronto")
                if pdf_questoes:
                    try:
                        import pypdf
                        leitor = pypdf.PdfReader(pdf_questoes)
                        for p in leitor.pages:
                            conteudo_texto += (p.extract_text() or "") + "\n"
                    except Exception as e:
                        st.error(f"Erro ao ler PDF: {e}")
            else:
                conteudo_texto = st.text_area("Cole aqui as perguntas com alternativas e gabarito:", height=220, placeholder="1. Qual o primeiro mandamento com promessa?\nA) Honra teu pai...\nB) Não matarás...\nGabarito: A\nRef: Efésios 6:2")

            btn_importar = st.button("Processar e Salvar Questões Prontas", use_container_width=True)

            if btn_importar:
                chave_api = st.secrets.get("GEMINI_API_KEY", "")
                if not chave_api:
                    st.error("Chave do Gemini não configurada nos Secrets!")
                elif not tema_import or not conteudo_texto.strip():
                    st.warning("Preencha o Tema e forneça o arquivo PDF ou texto com as questões.")
                else:
                    try:
                        from google import genai
                        client = genai.Client(api_key=chave_api)
                        
                        prompt_parser = (
                            "Você é um assistente de banco de dados. O usuário forneceu uma lista de perguntas e respostas já prontas. "
                            "Sua tarefa é ESTRITAMENTE extrair cada questão, separar o enunciado, as 4 opções (A, B, C, D), a alternativa correta e a explicação/referência. "
                            "Não invente novas perguntas. Retorne ESTRITAMENTE um JSON puro sem blocos markdown ```json no formato:\n"
                            '[{"enunciado": "...", "opcoes": {"A": "...", "B": "...", "C": "...", "D": "..."}, "correta": "A", "explicacao": "..."}]'
                        )

                        with st.spinner("Processando e estruturando as questões..."):
                            resp = client.models.generate_content(
                                model="gemini-3.6-flash",
                                contents=[prompt_parser, conteudo_texto]
                            )
                            texto_limpo = resp.text.replace("```json", "").replace("```", "").strip()
                            questoes_extraidas = json.loads(texto_limpo)

                            conn = sqlite3.connect(DB_FILE)
                            c = conn.cursor()
                            for q in questoes_extraidas:
                                c.execute('''
                                    INSERT INTO questoes (livro_tema, capitulo_licao, enunciado, opcoes_json, correta, explicacao_referencia)
                                    VALUES (?, ?, ?, ?, ?, ?)
                                ''', (
                                    tema_import.strip(),
                                    cap_import.strip() if cap_import else "Geral",
                                    q["enunciado"],
                                    json.dumps(q["opcoes"]),
                                    q["correta"].upper().strip(),
                                    q.get("explicacao", "")
                                ))
                            conn.commit()
                            conn.close()

                            st.success(f"✅ Sucesso! {len(questoes_extraidas)} questões prontas foram salvas no banco!")
                            st.rerun()
                    except Exception as err:
                        st.error(f"Erro ao processar: {err}")

        # ----------------------------------------------------
        # SUB-ABA 2: GERADOR COM IA (A PARTIR DA MATÉRIA)
        # ----------------------------------------------------
        with sub_tab2:
            st.markdown("#### Gerar Perguntas Inéditas de um Manual/PDF")
            st.write("Envie o manual da lição ou discurso e o Gemini criará perguntas inéditas de múltipla escolha.")

            tema_ia = st.text_input("Livro / Tema da Lição:", placeholder="Ex: Vem, e Segue-Me — D&C 20-22", key="ia_tema")
            cap_ia = st.text_input("Capítulo / Detalhe:", placeholder="Ex: Seções 20 a 22", key="ia_cap")
            qtd_questoes = st.slider("Quantidade de perguntas a gerar:", min_value=1, max_value=10, value=3)
            arquivo_manual = st.file_uploader("Suba o manual ou texto da lição (PDF):", type=["pdf"], key="pdf_manual")

            btn_gerar_ia = st.button("⚡ Gerar Questões Inéditas com Gemini", use_container_width=True)

            if btn_gerar_ia:
                chave_api = st.secrets.get("GEMINI_API_KEY", "")
                if not chave_api:
                    st.error("Chave GEMINI_API_KEY ausente!")
                elif not arquivo_manual:
                    st.warning("Envie o arquivo PDF do manual da aula.")
                else:
                    try:
                        from google import genai
                        from google.genai import types
                        import pypdf

                        leitor = pypdf.PdfReader(arquivo_manual)
                        texto_manual = ""
                        for pag in leitor.pages:
                            texto_manual += (pag.extract_text() or "") + "\n"

                        client = genai.Client(api_key=chave_api)
                        prompt_instrucao = (
                            f"Você é um professor de Escola Dominical de A Igreja de Jesus Cristo dos Santos dos Últimos Dias. "
                            f"Com base no texto fornecido, crie exatamente {qtd_questoes} perguntas edificantes de múltipla escolha "
                            f"com 4 alternativas (A, B, C, D), indicando a resposta correta e a referência nas escrituras. "
                            f"Retorne ESTRITAMENTE um JSON puro sem marcadores markdown ```json no formato:\n"
                            '[{"enunciado": "...", "opcoes": {"A": "...", "B": "...", "C": "...", "D": "..."}, "correta": "A", "explicacao": "..."}]'
                        )

                        with st.spinner("O Gemini está lendo o manual e gerando perguntas..."):
                            if len(texto_manual.strip()) > 80:
                                resposta = client.models.generate_content(
                                    model="gemini-2.5-flash",
                                    contents=[prompt_instrucao, texto_manual]
                                )
                            else:
                                arquivo_manual.seek(0)
                                pdf_bytes = arquivo_manual.read()
                                resposta = client.models.generate_content(
                                    model="gemini-2.5-flash",
                                    contents=[
                                        types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
                                        prompt_instrucao
                                    ]
                                )

                            texto_limpo = resposta.text.replace("```json", "").replace("```", "").strip()
                            perguntas_novas = json.loads(texto_limpo)

                            conn = sqlite3.connect(DB_FILE)
                            c = conn.cursor()
                            for item in perguntas_novas:
                                c.execute('''
                                    INSERT INTO questoes (livro_tema, capitulo_licao, enunciado, opcoes_json, correta, explicacao_referencia)
                                    VALUES (?, ?, ?, ?, ?, ?)
                                ''', (
                                    tema_ia if tema_ia else "Escola Dominical",
                                    cap_ia if cap_ia else "Geral",
                                    item["enunciado"],
                                    json.dumps(item["opcoes"]),
                                    item["correta"].upper().strip(),
                                    item.get("explicacao", "")
                                ))
                            conn.commit()
                            conn.close()

                            st.success(f"Foram criadas e cadastradas {len(perguntas_novas)} perguntas com sucesso!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao gerar com IA: {e}")

        # ----------------------------------------------------
        # SUB-ABA 3: CADASTRO MANUAL
        # ----------------------------------------------------
        with sub_tab3:
            st.markdown("#### Inserir Pergunta Manualmente")
            with st.form("form_manual_novo"):
                tema_m = st.text_input("Livro / Tema:", placeholder="Ex: Livro de Mórmon")
                cap_m = st.text_input("Lição ou Capítulo:", placeholder="Ex: Mosias 2")
                enun_m = st.text_area("Enunciado da Questão:")
                col_a, col_b = st.columns(2)
                with col_a:
                    op_a = st.text_input("Alternativa A:")
                    op_c = st.text_input("Alternativa C:")
                with col_b:
                    op_b = st.text_input("Alternativa B:")
                    op_d = st.text_input("Alternativa D:")
                correta_m = st.selectbox("Alternativa Correta:", ["A", "B", "C", "D"])
                explic_m = st.text_area("Referência de Escritura / Explicação:")
                
                btn_salvar_manual = st.form_submit_button("Salvar Pergunta no Banco")

            if btn_salvar_manual:
                if tema_m and enun_m and op_a and op_b and op_c and op_d:
                    conn = sqlite3.connect(DB_FILE)
                    c = conn.cursor()
                    json_op = json.dumps({"A": op_a, "B": op_b, "C": op_c, "D": op_d})
                    c.execute('''
                        INSERT INTO questoes (livro_tema, capitulo_licao, enunciado, opcoes_json, correta, explicacao_referencia)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (tema_m.strip(), cap_m.strip(), enun_m.strip(), json_op, correta_m, explic_m.strip()))
                    conn.commit()
                    conn.close()
                    st.success("Pergunta salva com sucesso!")
                    st.rerun()
                else:
                    st.error("Preencha todos os campos obrigatórios.")
