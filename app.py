import streamlit as st
from supabase import create_client, Client
import json
import os
import time
import base64
import re
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
# 2. DESIGN VISUAL E CSS INSTITUCIONAL
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

    div[data-testid="stRadio"] > div { gap: 10px; }
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

    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 3px solid #c5a059;
        padding: 18px;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
    }

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
# 3. FUNÇÕES AUXILIARES E BANCO SUPABASE
# =======================================================
@st.cache_resource
def get_supabase_client() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = get_supabase_client()

def normalizar_nome(nome: str) -> str:
    """Padroniza espaços duplos e capitalização do nome do membro."""
    return re.sub(r'\s+', ' ', nome.strip()).title()

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

aba_home, aba_quiz, aba_ranking, aba_professor = st.tabs([
    "🏠 Início & Galeria",
    "📖 Estudo & Quiz",
    "🏆 Quadro de Destaque",
    "🔐 Área da Presidência"
])

# =======================================================
# ABA 1: INÍCIO E SLIDESHOW DE FOTOS
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
        extensoes_validas = ('.png', '.jpg', '.jpeg', '.webp')
        fotos = [
            os.path.join(pasta_assets, f) 
            for f in os.listdir(pasta_assets) 
            if f.lower().endswith(extensoes_validas) and not f.startswith('.') and f != "README.md"
        ]

    st.divider()
    st.markdown("### 📸 Vem e Segue-Me")

    if fotos:
        slides_html = ""
        dots_html = ""
        for idx, fpath in enumerate(fotos):
            try:
                with open(fpath, "rb") as img_file:
                    b64_str = base64.b64encode(img_file.read()).decode()
                ext = os.path.splitext(fpath)[1].replace(".", "").lower()
                nome_legenda = os.path.splitext(os.path.basename(fpath))[0].replace("_", " ").replace("-", " ").title()

                display_style = "block" if idx == 0 else "none"
                slides_html += f"""
                <div class="slide fade" style="display: {display_style};">
                    <img src="data:image/{ext};base64,{b64_str}" style="width:100%; height:420px; object-fit: cover; border-radius: 12px;">
                    <div class="caption-text">{nome_legenda}</div>
                </div>
                """
                active_class = "active" if idx == 0 else ""
                dots_html += f'<span class="dot {active_class}" onclick="currentSlide({idx+1})"></span>'
            except Exception:
                pass

        carrossel_codigo = f"""
        <style>
        .slideshow-container {{
            max-width: 850px;
            position: relative;
            margin: auto;
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 8px 24px rgba(11, 37, 69, 0.15);
            background-color: #0b2545;
        }}
        .caption-text {{
            color: #ffffff;
            font-size: 16px;
            font-weight: 600;
            padding: 12px 20px;
            position: absolute;
            bottom: 0px;
            width: 100%;
            text-align: center;
            background: linear-gradient(to top, rgba(11, 37, 69, 0.85), transparent);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        .prev, .next {{
            cursor: pointer;
            position: absolute;
            top: 50%;
            width: auto;
            padding: 14px 18px;
            margin-top: -22px;
            color: white;
            font-weight: bold;
            font-size: 20px;
            transition: 0.3s;
            user-select: none;
            background-color: rgba(0,0,0,0.35);
            border-radius: 50%;
            text-decoration: none;
            margin-left: 10px;
            margin-right: 10px;
        }}
        .next {{ right: 0; }}
        .prev:hover, .next:hover {{ background-color: rgba(197, 160, 89, 0.85); color: #0b2545; }}
        .dots-container {{ text-align: center; margin-top: 12px; }}
        .dot {{
            cursor: pointer;
            height: 11px;
            width: 11px;
            margin: 0 4px;
            background-color: #cbd5e1;
            border-radius: 50%;
            display: inline-block;
            transition: background-color 0.3s ease;
        }}
        .active, .dot:hover {{ background-color: #c5a059; }}
        .fade {{
            animation-name: fade;
            animation-duration: 1.0s;
        }}
        @keyframes fade {{
            from {{opacity: .4}} 
            to {{opacity: 1}}
        }}
        </style>

        <div class="slideshow-container">
            {slides_html}
            <a class="prev" onclick="plusSlides(-1)">&#10094;</a>
            <a class="next" onclick="plusSlides(1)">&#10095;</a>
        </div>
        <div class="dots-container">
            {dots_html}
        </div>

        <script>
        let slideIndex = 1;
        let timer = null;

        function showSlides(n) {{
            let i;
            let slides = document.getElementsByClassName("slide");
            let dots = document.getElementsByClassName("dot");
            if (n > slides.length) {{slideIndex = 1}}    
            if (n < 1) {{slideIndex = slides.length}}
            for (i = 0; i < slides.length; i++) {{
                slides[i].style.display = "none";  
            }}
            for (i = 0; i < dots.length; i++) {{
                dots[i].className = dots[i].className.replace(" active", "");
            }}
            slides[slideIndex-1].style.display = "block";  
            dots[slideIndex-1].className += " active";
        }}

        function plusSlides(n) {{
            clearInterval(timer);
            showSlides(slideIndex += n);
            iniciarAutoSlide();
        }}

        function currentSlide(n) {{
            clearInterval(timer);
            showSlides(slideIndex = n);
            iniciarAutoSlide();
        }}

        function iniciarAutoSlide() {{
            timer = setInterval(function() {{
                slideIndex++;
                showSlides(slideIndex);
            }}, 4000);
        }}

        iniciarAutoSlide();
        </script>
        """
        import streamlit.components.v1 as components
        components.html(carrossel_codigo, height=480)
    else:
        st.info("💡 Coloque fotos na pasta `assets/` do projeto no GitHub para exibi-las no show de fotos.")

# =======================================================
# ABA 2: ESTUDO & QUIZ DO ALUNO
# =======================================================
with aba_quiz:
    st.subheader("Caderno de Estudos e Perguntas")
    col1, col2 = st.columns(2)

    # Identificar tema destaque definido pelo professor
    tema_destaque = ""
    try:
        cfg = supabase.table("configuracoes").select("valor").eq("chave", "tema_destaque").execute()
        if cfg.data:
            tema_destaque = cfg.data[0]["valor"]
    except Exception:
        pass

    with col1:
        nome_aluno_raw = st.text_input("Seu Nome e Sobrenome:", placeholder="Ex: Lucas Santana")
        nome_aluno = normalizar_nome(nome_aluno_raw) if nome_aluno_raw else ""

    with col2:
        try:
            res_temas = supabase.table("questoes").select("livro_tema").execute()
            temas_disponiveis = sorted(list(set([item["livro_tema"] for item in res_temas.data]))) if res_temas.data else []
        except Exception:
            temas_disponiveis = []

        idx_padrao = 0
        if tema_destaque in temas_disponiveis:
            idx_padrao = temas_disponiveis.index(tema_destaque)

        tema_selecionado = st.selectbox(
            "Lição / Tema:", 
            temas_disponiveis if temas_disponiveis else ["Nenhum tema cadastrado"],
            index=idx_padrao if temas_disponiveis else 0
        )

    if not nome_aluno:
        st.info("👆 Por favor, preencha o seu nome acima para iniciar as perguntas.")
    else:
        res_questoes = supabase.table("questoes").select("*").eq("livro_tema", tema_selecionado).execute()
        questoes = res_questoes.data

        if not questoes:
            st.warning("Ainda não há perguntas cadastradas para este tema.")
        else:
            with st.form("form_estudo_dominical"):
                respostas_usuario = {}
                for idx, q in enumerate(questoes, 1):
                    q_id = q["id"]
                    opcoes = q["opcoes_json"] if isinstance(q["opcoes_json"], dict) else json.loads(q["opcoes_json"])

                    st.markdown(f"""
                        <div class="quiz-card">
                            <div class="quiz-title">📖 Pergunta {idx:02d} — {q['capitulo_licao']}</div>
                            <div style="font-size: 15px; line-height: 1.6;">{q['enunciado']}</div>
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
                        "correta": q["correta"],
                        "explicacao": q["explicacao_referencia"]
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

                    # Verificação de Envio Único / Atualização pela Maior Nota
                    res_anterior = supabase.table("ranking").select("id, acertos, porcentagem").eq("nome_aluno", nome_aluno).eq("tema", tema_selecionado).execute()
                    
                    if res_anterior.data:
                        reg_antigo = res_anterior.data[0]
                        if porcentagem > float(reg_antigo["porcentagem"]):
                            supabase.table("ranking").update({
                                "acertos": acertos,
                                "total": total,
                                "porcentagem": porcentagem,
                                "data_hora": agora_iso
                            }).eq("id", reg_antigo["id"]).execute()
                            st.toast("Parabéns! Sua nota mais alta foi atualizada.", icon="📈")
                        else:
                            st.toast("Participação já computada! Sua nota anterior prevaleceu.", icon="ℹ️")
                    else:
                        supabase.table("ranking").insert({
                            "nome_aluno": nome_aluno,
                            "tema": tema_selecionado,
                            "acertos": acertos,
                            "total": total,
                            "porcentagem": porcentagem,
                            "data_hora": agora_iso
                        }).execute()
                        st.toast("Estudo salvo com sucesso!", icon="📖")

                    st.divider()
                    st.subheader("📊 Seu Desempenho")
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Acertos", f"{acertos} de {total}")
                    m2.metric("Aproveitamento", f"{porcentagem}%")
                    m3.metric("Mensagem", "Excelente estudo!" if porcentagem >= 70 else "Continue se aprofundando!")

                    st.subheader("📋 Gabarito e Escrituras de Referência")
                    for idx, q in enumerate(questoes, 1):
                        resp = respostas_usuario[q["id"]]
                        acertou = resp["escolha"] == resp["correta"]
                        icone = "✅" if acertou else "❌"

                        with st.expander(f"{icone} Pergunta {idx:02d} — Gabarito: {resp['correta']} (Sua resposta: {resp['escolha']})"):
                            st.write(f"**Pergunta:** {q['enunciado']}")
                            st.info(f"**Referência & Reflexão:** {resp['explicacao']}")

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

    res_ranking = supabase.table("ranking").select("*").execute()
    todos_registros = res_ranking.data

    if not todos_registros:
        st.info("Ainda não há participações registradas no banco de dados.")
    else:
        semanas_registradas_no_mes = set()
        dados_mes = {}
        dados_gerais = {}
        participacao_semanal = {}

        for reg in todos_registros:
            nome = reg["nome_aluno"]
            acertos = reg["acertos"]
            porcentagem = float(reg["porcentagem"])
            data_h = reg["data_hora"]
            
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

        st.markdown(f"#### 📅 Desempenho do Mês ({nome_mes_extenso} / {ano_atual})")
        if alunos_todas_semanas:
            nomes_constantes = ", ".join([f"**{a}**" for a in alunos_todas_semanas])
            st.markdown(f"""
                <div class="constancia-box">
                    ⭐ <b>Constância Exemplar:</b> Participaram em <b>todas as semanas</b> de {nome_mes_extenso}:<br>
                    {nomes_constantes} 👏
                </div>
            """, unsafe_allow_html=True)

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
            temas_contador = {}
            for reg in todos_registros:
                t = reg["tema"]
                temas_contador[t] = temas_contador.get(t, 0) + 1
            if temas_contador:
                st.bar_chart(temas_contador)

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
# ABA 4: ÁREA DO PROFESSOR
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

        # Definição do Tema da Semana
        st.markdown("### 📌 Lição Ativa da Semana")
        try:
            res_t = supabase.table("questoes").select("livro_tema").execute()
            todos_temas = sorted(list(set([it["livro_tema"] for it in res_t.data]))) if res_t.data else []
        except Exception:
            todos_temas = []

        if todos_temas:
            col_t1, col_t2 = st.columns([3, 1])
            with col_t1:
                novo_destaque = st.selectbox("Escolha a lição que abrirá selecionada para os alunos:", todos_temas)
            with col_t2:
                st.write("")
                st.write("")
                if st.button("Fixar Lição da Semana", use_container_width=True):
                    supabase.table("configuracoes").upsert({"chave": "tema_destaque", "valor": novo_destaque}).execute()
                    st.toast("Lição da semana atualizada com sucesso!", icon="📌")
        st.divider()

        sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
            "📋 Importar Questões Prontas",
            "⚡ Gerar com IA (Manual/PDF)",
            "✍️ Cadastro Manual",
            "🗑️ Gerenciar / Excluir Questões"
        ])

        # SUB-ABA 1: IMPORTAR
        with sub_tab1:
            st.markdown("#### Importar Questionário Pronto")
            tema_import = st.text_input("Livro / Tema:", placeholder="Ex: Isaías 1-12", key="imp_tema")
            cap_import = st.text_input("Capítulo / Lição:", placeholder="Ex: Vem, e Segue-Me", key="imp_cap")
            origem_import = st.radio("Origem das questões:", ["📄 Upload de PDF", "📝 Colar Texto"], horizontal=True)
            
            conteudo_texto = ""
            if origem_import == "📄 Upload de PDF":
                pdf_questoes = st.file_uploader("Selecione o PDF com as perguntas:", type=["pdf"], key="pdf_pronto")
                if pdf_questoes:
                    try:
                        import pypdf
                        leitor = pypdf.PdfReader(pdf_questoes)
                        for p in leitor.pages:
                            conteudo_texto += (p.extract_text() or "") + "\n"
                    except Exception as e:
                        st.error(f"Erro ao ler PDF: {e}")
            else:
                conteudo_texto = st.text_area("Cole as perguntas com opções e gabarito:", height=200)

            if st.button("Processar e Salvar Questões Prontas", use_container_width=True):
                chave_api = st.secrets.get("GEMINI_API_KEY", "")
                if not chave_api:
                    st.error("Chave GEMINI_API_KEY ausente nos Secrets!")
                elif not tema_import or not conteudo_texto.strip():
                    st.warning("Preencha o Tema e forneça o conteúdo.")
                else:
                    try:
                        from google import genai
                        client = genai.Client(api_key=chave_api)
                        prompt_parser = (
                            "Você é um assistente de banco de dados. Extraia cada questão com enunciado, opções (A, B, C, D), "
                            "correta e explicacao. Retorne ESTRITAMENTE um array JSON puro:\n"
                            '[{"enunciado": "...", "opcoes": {"A": "...", "B": "...", "C": "...", "D": "..."}, "correta": "A", "explicacao": "..."}]'
                        )
                        with st.spinner("Processando e gravando no Supabase..."):
                            resp = client.models.generate_content(
                                model="gemini-2.5-flash",
                                contents=[prompt_parser, conteudo_texto]
                            )
                            texto_limpo = resp.text.replace("```json", "").replace("```", "").strip()
                            questoes_extraidas = json.loads(texto_limpo)

                            for q in questoes_extraidas:
                                supabase.table("questoes").insert({
                                    "livro_tema": tema_import.strip(),
                                    "capitulo_licao": cap_import.strip() if cap_import else "Geral",
                                    "enunciado": q["enunciado"],
                                    "opcoes_json": q["opcoes"],
                                    "correta": q["correta"].upper().strip(),
                                    "explicacao_referencia": q.get("explicacao", "")
                                }).execute()

                            st.success(f"✅ {len(questoes_extraidas)} questões gravadas com sucesso!")
                            st.rerun()
                    except Exception as err:
                        st.error(f"Erro ao processar: {err}")

        # SUB-ABA 2: GERADOR COM IA
        with sub_tab2:
            st.markdown("#### Gerar Perguntas Inéditas de um Manual/PDF")
            tema_ia = st.text_input("Tema / Livro:", placeholder="Ex: Isaías 1-12", key="ia_tema")
            cap_ia = st.text_input("Capítulo / Lição:", placeholder="Ex: Deus é a minha salvação", key="ia_cap")
            qtd_questoes = st.slider("Quantidade de perguntas:", min_value=1, max_value=8, value=4)
            arquivo_manual = st.file_uploader("Upload do Manual (PDF):", type=["pdf"], key="pdf_manual")

            if st.button("⚡ Gerar Perguntas com Gemini", use_container_width=True):
                chave_api = st.secrets.get("GEMINI_API_KEY", "")
                if not chave_api:
                    st.error("Chave GEMINI_API_KEY ausente nos Secrets!")
                elif not arquivo_manual:
                    st.warning("Selecione o arquivo PDF.")
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
                            f"Você é um professor da Escola Dominical de A Igreja de Jesus Cristo dos Santos dos Últimos Dias. "
                            f"Crie exatamente {qtd_questoes} perguntas edificantes de múltipla escolha com 4 opções (A, B, C, D), "
                            f"correta e referência nas escrituras. Retorne ESTRITAMENTE um array JSON puro:\n"
                            '[{"enunciado": "...", "opcoes": {"A": "...", "B": "...", "C": "...", "D": "..."}, "correta": "A", "explicacao": "..."}]'
                        )

                        with st.spinner("Gerando questões e salvando no Supabase..."):
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

                            for item in perguntas_novas:
                                supabase.table("questoes").insert({
                                    "livro_tema": tema_ia if tema_ia else "Escola Dominical",
                                    "capitulo_licao": cap_ia if cap_ia else "Geral",
                                    "enunciado": item["enunciado"],
                                    "opcoes_json": item["opcoes"],
                                    "correta": item["correta"].upper().strip(),
                                    "explicacao_referencia": item.get("explicacao", "")
                                }).execute()

                            st.success(f"✅ {len(perguntas_novas)} perguntas geradas com sucesso!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao gerar: {e}")

        # SUB-ABA 3: MANUAL
        with sub_tab3:
            st.markdown("#### Inserir Pergunta Manualmente")
            with st.form("form_manual_novo"):
                tema_m = st.text_input("Livro / Tema:", placeholder="Ex: Livro de Mórmon")
                cap_m = st.text_input("Lição ou Capítulo:", placeholder="Ex: 2 Néfi 2")
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
                
                btn_salvar_manual = st.form_submit_button("Salvar Pergunta na Nuvem")

            if btn_salvar_manual:
                if tema_m and enun_m and op_a and op_b and op_c and op_d:
                    supabase.table("questoes").insert({
                        "livro_tema": tema_m.strip(),
                        "capitulo_licao": cap_m.strip(),
                        "enunciado": enun_m.strip(),
                        "opcoes_json": {"A": op_a, "B": op_b, "C": op_c, "D": op_d},
                        "correta": correta_m,
                        "explicacao_referencia": explic_m.strip()
                    }).execute()
                    st.success("Pergunta cadastrada com sucesso!")
                    st.rerun()
                else:
                    st.error("Preencha todos os campos obrigatórios.")

        # SUB-ABA 4: GERENCIAR
        with sub_tab4:
            st.markdown("#### ⚙️ Gerenciamento do Banco (Supabase)")
            col_z1, col_z2 = st.columns(2)
            with col_z1:
                if st.button("🔄 Zerar Ranking / Participantes", type="secondary"):
                    supabase.table("ranking").delete().neq("id", 0).execute()
                    st.toast("Ranking zerado!", icon="🔄")
                    st.rerun()
            with col_z2:
                if st.button("🚨 Limpar Todas as Questões", type="primary"):
                    supabase.table("questoes").delete().neq("id", 0).execute()
                    st.toast("Todas as questões foram apagadas!", icon="🗑️")
                    st.rerun()

            st.divider()
            st.markdown("#### Questões Cadastradas")
            res_all_q = supabase.table("questoes").select("id, livro_tema, capitulo_licao, enunciado").order("id", desc=True).execute()
            todas_questoes = res_all_q.data

            if not todas_questoes:
                st.info("Nenhuma questão cadastrada.")
            else:
                for item_q in todas_questoes:
                    col_texto, col_btn = st.columns([5, 1])
                    with col_texto:
                        st.markdown(f"**[{item_q['livro_tema']} — {item_q['capitulo_licao']}]** (ID #{item_q['id']})")
                        st.caption(item_q['enunciado'][:130] + "..." if len(item_q['enunciado']) > 130 else item_q['enunciado'])
                    with col_btn:
                        if st.button("🗑️ Excluir", key=f"del_q_{item_q['id']}"):
                            supabase.table("questoes").delete().eq("id", item_q['id']).execute()
                            st.toast(f"Questão #{item_q['id']} excluída!", icon="🗑️")
                            st.rerun()
                    st.divider()
