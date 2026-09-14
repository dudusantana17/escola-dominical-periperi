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
        padding: 18px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }
    .podio-pos { font-size: 28px; margin-bottom: 4px; }
    .podio-nome { font-weight: 700; font-size: 16px; color: #0b2545; }
    .podio-media { font-size: 20px; font-weight: 700; color: #133b68; margin-top: 4px; }

    /* Destaque de Constância */
    .constancia-box {
        background: linear-gradient(135deg, #fef9c3 0%, #fef08a 100%);
        border: 1px solid #eab308;
        border-left: 6px solid #ca8a04;
        padding: 14px 20px;
        border-radius: 10px;
        margin: 15px 0;
        color: #713f12;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# =======================================================
# 3. BANCO DE DADOS (SQLite Local - Sem inserções automáticas)
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
    conn.commit()
    conn.close()

init_db()

# =======================================================
# 4. CABEÇALHO HERO INSTITUCIONAL
# =======================================================
st.markdown("""
    <div class="church-header">
        <div class="sub-sub">A Igreja de Jesus Cristo dos Santos dos Últimos Dias</div>
        <h1>Escola Dominical — Ala Periperi</h1>
        <p>“Aprendei de mim e ouvi minhas palavras; andai na mansidão de meu Espírito e tereis paz em mim.” — D&C 19:23</p>
    </div>
""", unsafe_allow_html=True)

# Navegação em Abas
aba_home, aba_quiz, aba_ranking, aba_professor = st.tabs([
    "🏠 Início & Galeria",
    "📖 Estudo & Quiz",
    "🏆 Quadro de Destaque",
    "🔐 Área do Professor"
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

    pasta_assets = "assets"
    fotos = []
    if os.path.exists(pasta_assets):
        fotos = [os.path.join(pasta_assets, f) for f in os.listdir(pasta_assets) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    st.divider()
    st.markdown("### 📸 Nossa Unidade e Atividades")
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

                    agora_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    conn = sqlite3.connect(DB_FILE)
                    c = conn.cursor()
                    c.execute('''
                        INSERT INTO ranking (nome_aluno, tema, acertos, total, porcentagem, data_hora)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (nome_aluno.strip().title(), tema_selecionado, acertos, total, porcentagem, agora_iso))
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
# ABA 3: QUADRO DE DESTAQUE (MENSAL, GRÁFICOS E GERAL)
# =======================================================
with aba_ranking:
    st.subheader("Quadro de Participação e Destaque")
    
    agora = datetime.now()
    ano_atual = agora.strftime("%Y")
    mes_atual = agora.strftime("%m")
    prefixo_mes = f"{ano_atual}-{mes_atual}"
    nome_mes_extenso = agora.strftime("%B").capitalize()

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, nome_aluno, tema, acertos, total, porcentagem, data_hora FROM ranking")
    todos_registros = c.fetchall()
    conn.close()

    if not todos_registros:
        st.info("Ainda não há participações registradas. O ranking aparecerá aqui assim que os primeiros estudos forem realizados.")
    else:
        semanas_registradas_no_mes = set()
        dados_mes = {}
        dados_gerais = {}
        participacao_semanal = {}

        for reg in todos_registros:
            _, nome, tema, acertos, total, porcentagem, data_h = reg
            
            dt_obj = None
            for fmt in ("%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M"):
                try:
                    dt_obj = datetime.strptime(data_h, fmt)
                    break
                except Exception:
                    pass

            if nome not in dados_gerais:
                dados_gerais[nome] = {"estudos": 0, "acertos": 0, "porcentagens": []}
            dados_gerais[nome]["estudos"] += 1
            dados_gerais[nome]["acertos"] += acertos
            dados_gerais[nome]["porcentagens"].append(porcentagem)

            if dt_obj and dt_obj.strftime("%Y-%m") == prefixo_mes:
                sem_ano = dt_obj.isocalendar()[1]
                semanas_registradas_no_mes.add(sem_ano)

                if nome not in participacao_semanal:
                    participacao_semanal[nome] = set()
                participacao_semanal[nome].add(sem_ano)

                if nome not in dados_mes:
                    dados_mes[nome] = {"estudos": 0, "acertos": 0, "porcentagens": []}
                dados_mes[nome]["estudos"] += 1
                dados_mes[nome]["acertos"] += acertos
                dados_mes[nome]["porcentagens"].append(porcentagem)

        alunos_todas_semanas = []
        if semanas_registradas_no_mes:
            total_semanas = len(semanas_registradas_no_mes)
            for aluno, sems in participacao_semanal.items():
                if len(sems) == total_semanas:
                    alunos_todas_semanas.append(aluno)

        lista_geral = []
        for n, d in dados_gerais.items():
            media = round(sum(d["porcentagens"]) / len(d["porcentagens"]), 1)
            selo = " ⭐ (Todas as semanas)" if n in alunos_todas_semanas else ""
            lista_geral.append((f"{n}{selo}", d["estudos"], d["acertos"], media))
        lista_geral.sort(key=lambda x: (x[3], x[2]), reverse=True)

        # 1. Constância
        st.markdown(f"#### 📅 Desempenho do Mês ({nome_mes_extenso} / {ano_atual})")
        if alunos_todas_semanas:
            nomes_constantes = ", ".join([f"**{a}**" for a in alunos_todas_semanas])
            st.markdown(f"""
                <div class="constancia-box">
                    ⭐ <b>Constância Exemplar:</b> Participaram em <b>todas as semanas</b> de {nome_mes_extenso}:<br>
                    {nomes_constantes} 👏
                </div>
            """, unsafe_allow_html=True)

        # 2. Pódio do Mês
        if dados_mes:
            lista_mes = []
            for n, d in dados_mes.items():
                media = round(sum(d["porcentagens"]) / len(d["porcentagens"]), 1)
                lista_mes.append((n, d["estudos"], d["acertos"], media))
            lista_mes.sort(key=lambda x: (x[3], x[2]), reverse=True)

            col_m1, col_m2, col_m3 = st.columns(3)
            if len(lista_mes) >= 1:
                with col_m1:
                    st.markdown(f"""
                        <div class="podio-card" style="border-top: 4px solid #d4af37;">
                            <div class="podio-pos">🥇</div>
                            <div class="podio-nome">{lista_mes[0][0]}</div>
                            <div class="podio-media">{lista_mes[0][3]}%</div>
                            <div style="font-size:12px; color:#64748b;">1º Lugar do Mês</div>
                        </div>
                    """, unsafe_allow_html=True)
            if len(lista_mes) >= 2:
                with col_m2:
                    st.markdown(f"""
                        <div class="podio-card" style="border-top: 4px solid #94a3b8;">
                            <div class="podio-pos">🥈</div>
                            <div class="podio-nome">{lista_mes[1][0]}</div>
                            <div class="podio-media">{lista_mes[1][3]}%</div>
                            <div style="font-size:12px; color:#64748b;">2º Lugar do Mês</div>
                        </div>
                    """, unsafe_allow_html=True)
            if len(lista_mes) >= 3:
                with col_m3:
                    st.markdown(f"""
                        <div class="podio-card" style="border-top: 4px solid #b45309;">
                            <div class="podio-pos">🥉</div>
                            <div class="podio-nome">{lista_mes[2][0]}</div>
                            <div class="podio-media">{lista_mes[2][3]}%</div>
                            <div style="font-size:12px; color:#64748b;">3º Lugar do Mês</div>
                        </div>
                    """, unsafe_allow_html=True)

        # 3. Gráficos de Engajamento
        st.write("")
        st.markdown("#### 📊 Gráficos de Engajamento da Ala")
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            st.caption("📈 **Média de Aproveitamento dos Alunos (%)**")
            nomes_grafico = [item[0].split(" ⭐")[0] for item in lista_geral[:10]]
            medias_grafico = [item[3] for item in lista_geral[:10]]
            dados_chart_media = dict(zip(nomes_grafico, medias_grafico))
            st.bar_chart(dados_chart_media)

        with col_g2:
            st.caption("📚 **Estudos Realizados por Livro / Tema**")
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("SELECT tema, COUNT(id) FROM ranking GROUP BY tema")
            dados_temas = dict(c.fetchall())
            conn.close()
            if dados_temas:
                st.bar_chart(dados_temas)
            else:
                st.info("Aguardando mais estudos para gerar o gráfico de temas.")

        # 4. Tabela Geral
        st.divider()
        st.markdown("#### 🌟 Classificação Geral Acumulada")
        tabela = []
        for pos, linha in enumerate(lista_geral, 1):
            tabela.append({
                "Posição": f"{pos}º",
                "Membro / Aluno": linha[0],
                "Estudos Feitos": linha[1],
                "Total Acertos": linha[2],
                "Média Geral": f"{linha[3]}%"
            })
        st.dataframe(tabela, use_container_width=True, hide_index=True)

# =======================================================
# ABA 4: ÁREA DO PROFESSOR (CADASTRO, IA E GERENCIAMENTO)
# =======================================================
with aba_professor:
    st.subheader("Painel do Professor e Liderança")
    
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
        col_ok.success("Acesso autorizado como liderança/professor!")
        if col_sair.button("Sair / Bloquear"):
            st.session_state.admin_logado = False
            st.rerun()

        sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
            "📋 Importar Questões Prontas",
            "⚡ Gerar com IA (Manual/PDF)",
            "✍️ Cadastro Manual",
            "🗑️ Gerenciar / Excluir Questões"
        ])

        # SUB-ABA 1: IMPORTAR
        with sub_tab1:
            st.markdown("#### Importar Questionário Pronto")
            st.write("Envie um PDF ou cole um texto com perguntas e respostas já prontas. A IA estrutura e salva no banco.")

            tema_import = st.text_input("Livro / Tema:", placeholder="Ex: Livro de Mórmon ou Vem, e Segue-Me", key="imp_tema")
            cap_import = st.text_input("Capítulo / Lição:", placeholder="Ex: Alma 32 ou Lição 14", key="imp_cap")
            origem_import = st.radio("Origem das questões:", ["📄 Upload de PDF", "📝 Colar Texto"], horizontal=True)
            
            conteudo_texto = ""
            if origem_import == "📄 Upload de PDF":
                pdf_questoes = st.file_uploader("Selecione o PDF contendo as perguntas:", type=["pdf"], key="pdf_pronto")
                if pdf_questoes:
                    try:
                        import pypdf
                        leitor = pypdf.PdfReader(pdf_questoes)
                        for p in leitor.pages:
                            conteudo_texto += (p.extract_text() or "") + "\n"
                    except Exception as e:
                        st.error(f"Erro ao ler PDF: {e}")
            else:
                conteudo_texto = st.text_area("Cole aqui as perguntas com alternativas e gabarito:", height=200, placeholder="1. Pergunta...\nA) Opção\nB) Opção\nGabarito: A\nRef: Escritura...")

            btn_importar = st.button("Processar e Salvar Questões Prontas", use_container_width=True)

            if btn_importar:
                chave_api = st.secrets.get("GEMINI_API_KEY", "")
                if not chave_api:
                    st.error("Chave GEMINI_API_KEY ausente nos Secrets!")
                elif not tema_import or not conteudo_texto.strip():
                    st.warning("Preencha o Tema e informe o texto ou PDF com as questões.")
                else:
                    try:
                        from google import genai
                        client = genai.Client(api_key=chave_api)
                        
                        prompt_parser = (
                            "Você é um assistente de banco de dados. O usuário forneceu perguntas e respostas prontas. "
                            "Sua tarefa é extrair cada questão separando: enunciado, opções (A, B, C, D), alternativa correta e explicação/referência. "
                            "Retorne ESTRITAMENTE um array JSON puro sem marcadores markdown ```json no formato:\n"
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

                            st.success(f"✅ {len(questoes_extraidas)} questões importadas com sucesso!")
                            st.rerun()
                    except Exception as err:
                        st.error(f"Erro ao processar: {err}")

        # SUB-ABA 2: GERADOR IA
        with sub_tab2:
            st.markdown("#### Gerar Perguntas Inéditas de um Manual/PDF")
            st.write("Envie o PDF da lição e o Gemini criará novas perguntas de múltipla escolha.")

            tema_ia = st.text_input("Tema / Livro:", placeholder="Ex: Doutrina e Convênios", key="ia_tema")
            cap_ia = st.text_input("Capítulo / Lição:", placeholder="Ex: Seções 20 a 22", key="ia_cap")
            qtd_questoes = st.slider("Quantidade de perguntas:", min_value=1, max_value=8, value=3)
            arquivo_manual = st.file_uploader("Upload do Manual / Texto (PDF):", type=["pdf"], key="pdf_manual")

            btn_gerar_ia = st.button("⚡ Gerar Perguntas com Gemini", use_container_width=True)

            if btn_gerar_ia:
                chave_api = st.secrets.get("GEMINI_API_KEY", "")
                if not chave_api:
                    st.error("Chave GEMINI_API_KEY ausente nos Secrets!")
                elif not arquivo_manual:
                    st.warning("Selecione o arquivo PDF do manual.")
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
                            f"com 4 opções (A, B, C, D), indicando a correta e a referência nas escrituras. "
                            f"Retorne ESTRITAMENTE um JSON puro sem marcadores markdown ```json no formato:\n"
                            '[{"enunciado": "...", "opcoes": {"A": "...", "B": "...", "C": "...", "D": "..."}, "correta": "A", "explicacao": "..."}]'
                        )

                        with st.spinner("O Gemini está lendo o manual e gerando perguntas..."):
                            if len(texto_manual.strip()) > 80:
                                resposta = client.models.generate_content(
                                    model="gemini-3.6-flash",
                                    contents=[prompt_instrucao, texto_manual]
                                )
                            else:
                                arquivo_manual.seek(0)
                                pdf_bytes = arquivo_manual.read()
                                resposta = client.models.generate_content(
                                    model="gemini-3.6-flash",
                                    contents=[
                                        types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
                                        prompt_instrucao
                                    ]
                                )

                            texto_limpo = resposta.text.replace("
