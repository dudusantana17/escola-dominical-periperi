"""
app.py - Sistema Web para Estudo das Escrituras da Escola Dominical (Ala Periperi)
Desenvolvido em Python com Streamlit, SQLite e Google Gemini AI.
"""

import os
import json
import glob
from pathlib import Path
from datetime import datetime
import streamlit as st
import pandas as pd
from PIL import Image

import database

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Escola Dominical — Ala Periperi",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicializa banco de dados e questões sementes se necessário
database.init_db()

# ==========================================
# ESTILIZAÇÃO VISUAL CUSTOMIZADA (CSS)
# ==========================================
st.markdown("""
<style>
    /* Variáveis e paleta com tons serenos de azul e dourado/areia */
    :root {
        --cor-primaria: #1a365d;
        --cor-secundaria: #2b6cb0;
        --cor-azul-claro: #ebf8ff;
        --cor-dourado: #d69e2e;
        --cor-dourado-claro: #fefcbf;
        --cor-areia: #fbf7ee;
        --cor-cinza-borda: #e2e8f0;
    }

    /* Otimizações globais de layout */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Banner Superior Acolhedor */
    .periperi-banner {
        background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 65%, #2c5282 100%);
        color: #ffffff;
        padding: 2.2rem 2.4rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(26, 54, 93, 0.25);
        border-bottom: 4px solid #d69e2e;
        position: relative;
    }

    .periperi-banner h1 {
        font-size: 2.4rem;
        font-weight: 800;
        margin: 0;
        color: #ffffff !important;
        letter-spacing: -0.5px;
    }

    .periperi-banner p.subtitulo {
        font-size: 1.25rem;
        color: #feebc8;
        margin-top: 0.6rem;
        margin-bottom: 0;
        font-style: italic;
        font-weight: 400;
    }

    .periperi-banner p.lema {
        font-size: 0.95rem;
        color: #e2e8f0;
        margin-top: 0.4rem;
        margin-bottom: 0;
        opacity: 0.9;
    }

    /* Cartão de Boas-Vindas e Aviso Amigável para Fotos */
    .empty-assets-card {
        background-color: #fbf7ee;
        border: 2px dashed #d69e2e;
        border-radius: 14px;
        padding: 1.8rem;
        text-align: center;
        margin-bottom: 2rem;
    }

    .empty-assets-card h3 {
        color: #1a365d;
        margin-top: 0;
        font-size: 1.3rem;
        font-weight: 700;
    }

    .empty-assets-card p {
        color: #4a5568;
        font-size: 1rem;
        margin-bottom: 0;
    }

    /* Cartões da Galeria de Fotos */
    .photo-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.06);
        transition: transform 0.2s ease;
        margin-bottom: 1rem;
    }

    .photo-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
    }

    /* Cartões de Questão */
    .quiz-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 6px solid #2b6cb0;
        border-radius: 12px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }

    .quiz-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.8rem;
    }

    .badge-tema {
        background-color: #ebf8ff;
        color: #2b6cb0;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
        border: 1px solid #bee3f8;
    }

    .badge-capitulo {
        background-color: #fefcbf;
        color: #975a16;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
        border: 1px solid #faf089;
        margin-left: 0.5rem;
    }

    .enunciado-text {
        font-size: 1.15rem;
        font-weight: 600;
        color: #1a202c;
        line-height: 1.5;
        margin-bottom: 1.2rem;
    }

    /* Cartões de Resultado do Quiz */
    .result-box-correct {
        background-color: #f0fff4;
        border: 1px solid #9ae6b4;
        border-left: 6px solid #38a169;
        border-radius: 10px;
        padding: 1.2rem;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }

    .result-box-incorrect {
        background-color: #fff5f5;
        border: 1px solid #feb2b2;
        border-left: 6px solid #e53e3e;
        border-radius: 10px;
        padding: 1.2rem;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }

    /* Pódio do Quadro de Destaque */
    .podium-box {
        border-radius: 14px;
        padding: 1.6rem 1.2rem;
        text-align: center;
        box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.08);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .podium-gold {
        background: linear-gradient(180deg, #fffaf0 0%, #ffffff 100%);
        border: 2px solid #d69e2e;
    }

    .podium-silver {
        background: linear-gradient(180deg, #f7fafc 0%, #ffffff 100%);
        border: 2px solid #a0aec0;
    }

    .podium-bronze {
        background: linear-gradient(180deg, #fffaf0 0%, #ffffff 100%);
        border: 2px solid #dd6b20;
    }

    .podium-medal {
        font-size: 2.8rem;
        line-height: 1;
        margin-bottom: 0.5rem;
    }

    .podium-name {
        font-size: 1.25rem;
        font-weight: 800;
        color: #1a365d;
        margin-bottom: 0.3rem;
    }

    .podium-score {
        font-size: 1.6rem;
        font-weight: 900;
        color: #2b6cb0;
    }

    .podium-tema {
        font-size: 0.85rem;
        color: #718096;
        margin-top: 0.3rem;
    }

    /* Cartão de Estatística */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }

    /* Abas estilizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        background-color: #f7fafc;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
        color: #4a5568;
    }

    .stTabs [aria-selected="true"] {
        background-color: #ebf8ff !important;
        color: #1a365d !important;
        border-bottom: 3px solid #2b6cb0 !important;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# COMPONENTE: BANNER & GALERIA DE FOTOS
# ==========================================
def render_header_e_galeria():
    """Renderiza o banner principal acolhedor e a galeria de fotos da pasta assets/."""
    # Banner Principal
    st.markdown("""
    <div class="periperi-banner">
        <h1>📖 Escola Dominical — Ala Periperi</h1>
        <p class="subtitulo">"Venham e Aprendam Comigo" (Mateus 11:28-30)</p>
        <p class="lema">Fortalecendo a fé através do estudo diário e conjunto das escrituras sagradas.</p>
    </div>
    """, unsafe_allow_html=True)

    # Leitura da pasta assets/
    assets_dir = Path("assets")
    extensoes_validas = ("*.jpg", "*.jpeg", "*.png", "*.webp", "*.avif", "*.gif")
    arquivos_fotos = []
    if assets_dir.exists() and assets_dir.is_dir():
        for ext in extensoes_validas:
            arquivos_fotos.extend(assets_dir.glob(ext))
            arquivos_fotos.extend(assets_dir.glob(ext.upper()))

    # Se houver fotos na pasta
    if arquivos_fotos:
        with st.expander("📸 Galeria de Fotos e Momentos da Ala Periperi", expanded=True):
            cols = st.columns(min(len(arquivos_fotos), 4))
            for idx, foto_path in enumerate(arquivos_fotos):
                col = cols[idx % len(cols)]
                with col:
                    try:
                        img = Image.open(foto_path)
                        nome_legenda = foto_path.stem.replace("_", " ").replace("-", " ").title()
                        st.image(img, use_container_width=True, caption=nome_legenda)
                    except Exception as e:
                        st.caption(f"Erro ao carregar imagem: {foto_path.name}")
    else:
        # Layout receptivo e amigável quando assets/ está vazia
        st.markdown("""
        <div class="empty-assets-card">
            <h3>📷 Bem-vindo à Galeria da Ala Periperi!</h3>
            <p>
                Ainda não há fotos adicionadas na pasta <code>assets/</code>.<br>
                Professores e membros podem adicionar fotos das aulas da Escola Dominical, confraternizações e momentos especiais 
                diretamente na pasta <strong>assets/</strong> ou pelo painel do professor para que elas apareçam aqui com destaque.
            </p>
        </div>
        """, unsafe_allow_html=True)


render_header_e_galeria()


# ==========================================
# ABAS PRINCIPAIS DO SISTEMA
# ==========================================
tab_estudo, tab_destaque, tab_professor = st.tabs([
    "📚 Estudo & Quiz",
    "🏆 Quadro de Destaque",
    "🎓 Área do Professor"
])


# ==============================================================================
# ABA 1: ESTUDO & QUIZ
# ==============================================================================
with tab_estudo:
    st.subheader("📝 Questionário de Estudo das Escrituras")
    st.caption("Responda às questões propostas para aprofundar seu conhecimento doutrinário.")

    # Filtros e Identificação do Aluno
    col_aluno, col_tema, col_cap = st.columns([1.5, 1.2, 1.2])

    with col_aluno:
        nome_aluno = st.text_input(
            "👤 Nome do Aluno(a):",
            placeholder="Ex: Irmão Silva, Irmã Oliveira...",
            key="quiz_nome_aluno",
            help="Seu nome será registrado no Quadro de Destaque após o término."
        )

    # Opções dinâmicas de temas
    temas_disponiveis = ["Todos"] + database.get_temas()
    with col_tema:
        tema_selecionado = st.selectbox("📖 Tema / Livro:", temas_disponiveis, key="filtro_tema")

    # Opções dinâmicas de capítulos/lições
    capitulos_disponiveis = ["Todas"] + database.get_capitulos(tema_selecionado)
    with col_cap:
        capitulo_selecionado = st.selectbox("📑 Lição / Capítulo:", capitulos_disponiveis, key="filtro_capitulo")

    # Recupera questões filtradas
    questoes = database.get_questoes(tema_selecionado, capitulo_selecionado)

    if not questoes:
        st.info("ℹ️ Nenhuma questão encontrada para os filtros selecionados. Selecione outro tema ou lição.")
    else:
        st.markdown(f"**Total de perguntas para este estudo:** {len(questoes)}")

        # Formulário do Quiz
        with st.form("form_quiz_periperi"):
            respostas_usuario = {}

            for idx, q in enumerate(questoes, 1):
                st.markdown(f"""
                <div class="quiz-card">
                    <div class="quiz-card-header">
                        <span style="font-weight: 700; color: #1a365d; font-size: 1.1rem;">Questão #{idx}</span>
                        <div>
                            <span class="badge-tema">{q['livro_tema']}</span>
                            <span class="badge-capitulo">{q['capitulo_licao']}</span>
                        </div>
                    </div>
                    <div class="enunciado-text">{q['enunciado']}</div>
                </div>
                """, unsafe_allow_html=True)

                opcoes_formatadas = [
                    f"A) {q['opcoes'].get('A', '')}",
                    f"B) {q['opcoes'].get('B', '')}",
                    f"C) {q['opcoes'].get('C', '')}",
                    f"D) {q['opcoes'].get('D', '')}"
                ]

                # Radio button de resposta
                escolha = st.radio(
                    f"Selecione sua resposta para a Questão #{idx}:",
                    options=opcoes_formatadas,
                    index=None,
                    key=f"radio_q_{q['id']}"
                )
                respostas_usuario[q["id"]] = escolha

                st.markdown("---")

            submeter_quiz = st.form_submit_button("✨ Finalizar e Ver Gabarito Comentado", use_container_width=True)

        # Processamento das Respostas
        if submeter_quiz:
            if not nome_aluno.strip():
                st.error("⚠️ Por favor, informe seu nome acima no campo 'Nome do Aluno(a)' antes de enviar o quiz!")
            else:
                acertos = 0
                total = len(questoes)

                st.markdown("## 📊 Resultado e Gabarito Comentado")

                for idx, q in enumerate(questoes, 1):
                    resposta_sel = respostas_usuario.get(q["id"])
                    letra_sel = resposta_sel[0] if resposta_sel else None
                    letra_correta = q["correta"].upper()

                    is_correta = (letra_sel == letra_correta)
                    if is_correta:
                        acertos += 1

                    # Card de correção individual
                    if is_correta:
                        st.markdown(f"""
                        <div class="result-box-correct">
                            <h4 style="color: #276749; margin-top:0;">✅ Questão #{idx} — Resposta Correta!</h4>
                            <p><strong>Sua resposta:</strong> {resposta_sel}</p>
                            <p><strong>📖 Explicação & Referência:</strong> {q['explicacao_referencia']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="result-box-incorrect">
                            <h4 style="color: #9b2c2c; margin-top:0;">❌ Questão #{idx} — Resposta Incorreta</h4>
                            <p><strong>Sua escolha:</strong> {resposta_sel if resposta_sel else 'Nenhuma resposta selecionada'}</p>
                            <p><strong>Gabarito Correto:</strong> Letra {letra_correta}) {q['opcoes'].get(letra_correta, '')}</p>
                            <p><strong>📖 Explicação & Referência:</strong> {q['explicacao_referencia']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                porcentagem = (acertos / total) * 100

                # Gravação no SQLite
                tema_registro = tema_selecionado if tema_selecionado != "Todos" else "Estudo Geral"
                database.save_ranking(
                    nome_aluno=nome_aluno,
                    tema=tema_registro,
                    acertos=acertos,
                    total=total,
                    porcentagem=porcentagem
                )

                # Destaque de comemoração
                if porcentagem >= 80:
                    st.balloons()
                    st.success(f"🎉 Parabéns, **{nome_aluno}**! Excelente estudo! Você acertou **{acertos} de {total}** ({porcentagem:.1f}%). Seu resultado foi salvo no Quadro de Destaque!")
                elif porcentagem >= 50:
                    st.info(f"👏 Muito bem, **{nome_aluno}**! Bom aproveitamento: **{acertos} de {total}** ({porcentagem:.1f}%). Continue estudando as escrituras!")
                else:
                    st.warning(f"📖 Obrigado pela dedicação, **{nome_aluno}**! Você acertou **{acertos} de {total}** ({porcentagem:.1f}%). Que tal revisar os capítulos e tentar novamente?")


# ==============================================================================
# ABA 2: QUADRO DE DESTAQUE (RANKING)
# ==============================================================================
with tab_destaque:
    st.subheader("🏆 Quadro de Destaque da Ala Periperi")
    st.caption("Reconhecendo a dedicação e o empenho dos alunos no estudo das escrituras.")

    # Filtro de tema para o ranking
    temas_ranking = ["Todos"] + database.get_temas()
    col_filtro_r, col_limite = st.columns([2.5, 1.5])
    with col_filtro_r:
        filtro_tema_rank = st.selectbox("Filtrar Ranking por Tema:", temas_ranking, key="rank_filtro_tema")
    with col_limite:
        limite_rank = st.selectbox("Exibir:", [10, 25, 50, 100], index=1, key="rank_limite")

    ranking_data = database.get_ranking(tema=filtro_tema_rank, limit=limite_rank)
    stats = database.get_estatisticas_ranking()

    # Cards de Estatísticas Globais
    st.markdown("### 📈 Estatísticas da Classe")
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    with col_stat1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin:0; color:#718096; font-size:0.9rem;">TENTATIVAS</h4>
            <span style="font-size:1.8rem; font-weight:800; color:#1a365d;">{stats['total_tentativas']}</span>
        </div>
        """, unsafe_allow_html=True)
    with col_stat2:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin:0; color:#718096; font-size:0.9rem;">ALUNOS ÚNICOS</h4>
            <span style="font-size:1.8rem; font-weight:800; color:#2b6cb0;">{stats['total_alunos']}</span>
        </div>
        """, unsafe_allow_html=True)
    with col_stat3:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin:0; color:#718096; font-size:0.9rem;">MÉDIA DA ALA</h4>
            <span style="font-size:1.8rem; font-weight:800; color:#d69e2e;">{stats['media_porcentagem']}%</span>
        </div>
        """, unsafe_allow_html=True)
    with col_stat4:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin:0; color:#718096; font-size:0.9rem;">MAIOR NOTA</h4>
            <span style="font-size:1.8rem; font-weight:800; color:#38a169;">{stats['maior_porcentagem']}%</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # PÓDIO COM TOP 3 (🥇, 🥈, 🥉)
    if ranking_data:
        st.markdown("### 🥇 Pódio de Honra (Top 3)")
        podium_cols = st.columns(3)

        # 1º Lugar
        top1 = ranking_data[0] if len(ranking_data) > 0 else None
        # 2º Lugar
        top2 = ranking_data[1] if len(ranking_data) > 1 else None
        # 3º Lugar
        top3 = ranking_data[2] if len(ranking_data) > 2 else None

        # Exibição: 2º Lugar na esquerda, 1º no centro, 3º na direita (estilo olímpico)
        with podium_cols[0]:
            if top2:
                st.markdown(f"""
                <div class="podium-box podium-silver">
                    <div class="podium-medal">🥈</div>
                    <div style="font-weight:700; color:#718096; font-size:0.9rem;">2º LUGAR</div>
                    <div class="podium-name">{top2['nome_aluno']}</div>
                    <div class="podium-score">{top2['porcentagem']}%</div>
                    <div class="podium-tema">{top2['acertos']}/{top2['total']} acertos • {top2['tema']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Aguardando 2º colocado...")

        with podium_cols[1]:
            if top1:
                st.markdown(f"""
                <div class="podium-box podium-gold">
                    <div class="podium-medal">🥇</div>
                    <div style="font-weight:700; color:#d69e2e; font-size:0.95rem;">CAMPEÃO(Ã)</div>
                    <div class="podium-name">{top1['nome_aluno']}</div>
                    <div class="podium-score">{top1['porcentagem']}%</div>
                    <div class="podium-tema">{top1['acertos']}/{top1['total']} acertos • {top1['tema']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Aguardando 1º colocado...")

        with podium_cols[2]:
            if top3:
                st.markdown(f"""
                <div class="podium-box podium-bronze">
                    <div class="podium-medal">🥉</div>
                    <div style="font-weight:700; color:#dd6b20; font-size:0.9rem;">3º LUGAR</div>
                    <div class="podium-name">{top3['nome_aluno']}</div>
                    <div class="podium-score">{top3['porcentagem']}%</div>
                    <div class="podium-tema">{top3['acertos']}/{top3['total']} acertos • {top3['tema']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Aguardando 3º colocado...")

        st.markdown("<br>", unsafe_allow_html=True)

        # TABELA COMPLETA COM MÉDIAS E ACERTOS
        st.markdown("### 📋 Classificação Completa")
        df_ranking = pd.DataFrame(ranking_data)
        df_ranking["Posição"] = [f"#{i+1}" for i in range(len(df_ranking))]
        df_display = df_ranking[["Posição", "nome_aluno", "tema", "acertos", "total", "porcentagem", "data_hora"]].copy()
        df_display.columns = ["Posição", "Aluno", "Tema / Lição", "Acertos", "Total de Questões", "Aproveitamento (%)", "Data/Hora"]

        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Aproveitamento (%)": st.column_config.ProgressColumn(
                    "Aproveitamento (%)",
                    help="Percentual de acertos no quiz",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                ),
            }
        )
    else:
        st.info("🌟 Seja o primeiro a completar um quiz para inaugurar o Quadro de Destaque da Ala Periperi!")


# ==============================================================================
# ABA 3: ÁREA DO PROFESSOR (SENHA: periperi2026)
# ==============================================================================
with tab_professor:
    st.subheader("🔒 Área Exclusiva do Professor")
    st.caption("Gerenciamento de conteúdos, criação manual de questões e geração inteligente via IA.")

    # Autenticação por Senha
    senha_digitada = st.text_input("Digite a senha do professor:", type="password", key="senha_prof")

    if senha_digitada == "periperi2026":
        st.success("🔓 Acesso autorizado! Bem-vindo, professor da Escola Dominical.")

        prof_tab_manual, prof_tab_ia, prof_tab_gerenciar, prof_tab_fotos = st.tabs([
            "✍️ Cadastrar Pergunta Manual",
            "🤖 Importar via PDF com Gemini IA",
            "🗂️ Gerenciar Questões",
            "🖼️ Gerenciar Fotos (Assets)"
        ])

        # ----------------------------------------------------------------------
        # SUB-ABA 1: CADASTRO MANUAL
        # ----------------------------------------------------------------------
        with prof_tab_manual:
            st.markdown("#### ✍️ Cadastrar Nova Pergunta no Banco")
            with st.form("form_cadastrar_questao"):
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    novo_tema = st.text_input(
                        "Livro / Tema Principal:",
                        placeholder="Ex: Vem, e Segue-Me — Livro de Mórmon",
                        help="Nome do livro canônico ou foco temático da aula."
                    )
                with col_m2:
                    novo_capitulo = st.text_input(
                        "Capítulo / Lição:",
                        placeholder="Ex: 2 Néfi 2 (O Plano de Salvação)",
                        help="Referência específica da lição ou capítulo estudado."
                    )

                novo_enunciado = st.text_area(
                    "Enunciado da Questão:",
                    placeholder="Digite a pergunta clara sobre o princípio doutrinário ou narrativa..."
                )

                st.markdown("**Opções de Resposta:**")
                col_o1, col_o2 = st.columns(2)
                with col_o1:
                    op_a = st.text_input("Opção A:", placeholder="Texto da alternativa A")
                    op_b = st.text_input("Opção B:", placeholder="Texto da alternativa B")
                with col_o2:
                    op_c = st.text_input("Opção C:", placeholder="Texto da alternativa C")
                    op_d = st.text_input("Opção D:", placeholder="Texto da alternativa D")

                col_correta, col_espaco = st.columns([1, 3])
                with col_correta:
                    nova_correta = st.selectbox("Alternativa Correta:", ["A", "B", "C", "D"])

                nova_explicacao = st.text_area(
                    "Explicação Doutrinária e Referência Escriturística:",
                    placeholder="Ex: Alma 32:21 — A fé não é ter um perfeito conhecimento das coisas..."
                )

                salvar_manual = st.form_submit_button("💾 Salvar Questão no Banco de Dados", use_container_width=True)

                if salvar_manual:
                    if not novo_tema or not novo_capitulo or not novo_enunciado or not op_a or not op_b or not op_c or not op_d:
                        st.error("⚠️ Por favor, preencha todos os campos obrigatórios e as 4 opções de resposta!")
                    else:
                        opcoes_dict = {"A": op_a, "B": op_b, "C": op_c, "D": op_d}
                        nova_id = database.add_questao(
                            livro_tema=novo_tema,
                            capitulo_licao=novo_capitulo,
                            enunciado=novo_enunciado,
                            opcoes=opcoes_dict,
                            correta=nova_correta,
                            explicacao_referencia=nova_explicacao
                        )
                        st.success(f"✅ Questão #{nova_id} cadastrada com sucesso! Ela já está disponível no quiz.")
                        st.rerun()

        # ----------------------------------------------------------------------
        # SUB-ABA 2: IMPORTAÇÃO VIA PDF COM GEMINI IA (google-genai)
        # ----------------------------------------------------------------------
        with prof_tab_ia:
            st.markdown("#### 🤖 Geração Automática de Questões a partir de PDF (Google Gemini)")
            st.caption("Faça upload de um manual, lição ou texto do 'Vem, e Segue-Me' em PDF. O Gemini lerá o conteúdo e gerará questões fiéis às escrituras.")

            col_ia1, col_ia2 = st.columns([1.5, 1])
            with col_ia1:
                pdf_arquivo = st.file_uploader("Selecione o arquivo PDF da lição:", type=["pdf"])

            with col_ia2:
                # Permite usar variável de ambiente ou digitar chave
                chave_env = os.environ.get("GEMINI_API_KEY", "")
                gemini_api_key = st.text_input(
                    "Chave de API do Gemini (GEMINI_API_KEY):",
                    value=chave_env,
                    type="password",
                    help="Obtenha gratuitamente no Google AI Studio (aistudio.google.com)."
                )

            col_opt1, col_opt2, col_opt3 = st.columns(3)
            with col_opt1:
                tema_ia_sugerido = st.text_input("Tema / Livro para as questões:", value="Vem, e Segue-Me — Lição Atual")
            with col_opt2:
                capitulo_ia_sugerido = st.text_input("Capítulo / Lição:", value="Estudo da Semana")
            with col_opt3:
                qtd_questoes = st.slider("Quantidade de Questões:", min_value=2, max_value=10, value=3)

            if st.button("🚀 Processar PDF e Gerar Questões com IA", use_container_width=True):
                if not pdf_arquivo:
                    st.error("⚠️ Por favor, selecione um arquivo PDF antes de prosseguir!")
                elif not gemini_api_key.strip():
                    st.error("⚠️ Por favor, informe sua chave de API do Gemini (GEMINI_API_KEY)!")
                else:
                    try:
                        with st.spinner("📄 Extraindo texto do documento PDF com pypdf..."):
                            from pypdf import PdfReader
                            reader = PdfReader(pdf_arquivo)
                            texto_completo = ""
                            for page in reader.pages:
                                texto_extraido = page.extract_text()
                                if texto_extraido:
                                    texto_completo += texto_extraido + "\n"

                            if not texto_completo.strip():
                                st.error("❌ Não foi possível extrair texto do PDF (o arquivo pode conter apenas imagens digitalizadas).")
                                st.stop()

                            # Limita para não exceder limites de contexto razoáveis
                            texto_contexto = texto_completo[:15000]

                        with st.spinner("🧠 Consultando Google Gemini para formular perguntas fiéis ao evangelho..."):
                            from google import genai
                            from google.genai import types

                            client = genai.Client(api_key=gemini_api_key.strip())

                            prompt = f"""
Você é um especialista e instrutor da Escola Dominical de A Igreja de Jesus Cristo dos Santos dos Últimos Dias (Vem, e Segue-Me).
Com base exclusivamente no texto fornecido abaixo da lição, crie exatamente {qtd_questoes} questões de múltipla escolha fiéis aos princípios doutrinários e narrativas das escrituras presentes no texto.

TEXTO DA LIÇÃO:
{texto_contexto}

INSTRUÇÕES OBRIGATÓRIAS:
1. Gere cada questão com 4 alternativas: "A", "B", "C" e "D".
2. Indique exatamente uma alternativa correta ("A", "B", "C" ou "D").
3. Forneça uma explicação detalhada citando a escritura ou o princípio correspondente.
4. Responda ESTRITAMENTE em formato JSON com uma lista de objetos, sem blocos de texto adicionais além do JSON puro.

Formato JSON esperado:
[
  {{
    "enunciado": "Texto claro e inspirador da pergunta",
    "opcoes": {{
      "A": "Alternativa A",
      "B": "Alternativa B",
      "C": "Alternativa C",
      "D": "Alternativa D"
    }},
    "correta": "A",
    "explicacao_referencia": "Referência escriturística e explicação doutrinária"
  }}
]
"""
                            # Chamada à API oficial do Google Gemini
                            response = client.models.generate_content(
                                model="gemini-2.5-flash",
                                contents=prompt,
                                config=types.GenerateContentConfig(
                                    response_mime_type="application/json"
                                )
                            )

                            resposta_texto = response.text.strip()

                            # Tenta parsear o JSON retornado
                            questoes_ia = json.loads(resposta_texto)

                            if isinstance(questoes_ia, list) and len(questoes_ia) > 0:
                                st.session_state["questoes_geradas_ia"] = questoes_ia
                                st.session_state["tema_ia"] = tema_ia_sugerido
                                st.session_state["capitulo_ia"] = capitulo_ia_sugerido
                                st.success(f"🎉 Sucesso! {len(questoes_ia)} questões geradas pelo Gemini. Confira a pré-visualização abaixo:")
                            else:
                                st.error("A resposta da IA não continha a lista esperada de questões.")

                    except Exception as err:
                        st.error(f"Erro durante a geração com Gemini: {str(err)}")

            # Pré-visualização e confirmação de salvamento no SQLite
            if "questoes_geradas_ia" in st.session_state and st.session_state["questoes_geradas_ia"]:
                st.markdown("### 📋 Questões Geradas para Revisão:")
                for i, q in enumerate(st.session_state["questoes_geradas_ia"], 1):
                    with st.expander(f"Questão {i}: {q.get('enunciado')[:75]}...", expanded=True):
                        st.markdown(f"**Enunciado:** {q.get('enunciado')}")
                        ops = q.get("opcoes", {})
                        st.markdown(f"- **A:** {ops.get('A')}")
                        st.markdown(f"- **B:** {ops.get('B')}")
                        st.markdown(f"- **C:** {ops.get('C')}")
                        st.markdown(f"- **D:** {ops.get('D')}")
                        st.markdown(f"**Gabarito Correto:** {q.get('correta')}")
                        st.markdown(f"**Explicação:** {q.get('explicacao_referencia')}")

                col_salvar_ia, col_descarta_ia = st.columns([2, 1])
                with col_salvar_ia:
                    if st.button("💾 Salvar Todas as Questões no Banco de Dados", type="primary", use_container_width=True):
                        salvas = 0
                        for q in st.session_state["questoes_geradas_ia"]:
                            database.add_questao(
                                livro_tema=st.session_state.get("tema_ia", "Vem, e Segue-Me"),
                                capitulo_licao=st.session_state.get("capitulo_ia", "Lição Atual"),
                                enunciado=q.get("enunciado", ""),
                                opcoes=q.get("opcoes", {}),
                                correta=q.get("correta", "A"),
                                explicacao_referencia=q.get("explicacao_referencia", "")
                            )
                            salvas += 1
                        st.session_state["questoes_geradas_ia"] = []
                        st.success(f"✅ {salvas} questões salvas no banco de dados com sucesso!")
                        st.rerun()

                with col_descarta_ia:
                    if st.button("🗑️ Descartar", use_container_width=True):
                        st.session_state["questoes_geradas_ia"] = []
                        st.rerun()

        # ----------------------------------------------------------------------
        # SUB-ABA 3: GERENCIAR QUESTÕES EXISTENTES
        # ----------------------------------------------------------------------
        with prof_tab_gerenciar:
            st.markdown("#### 🗂️ Gerenciamento do Acervo de Perguntas")
            todas_questoes = database.get_questoes()
            st.write(f"**Total de perguntas ativas:** {len(todas_questoes)}")

            if todas_questoes:
                lista_tabela = []
                for q in todas_questoes:
                    lista_tabela.append({
                        "ID": q["id"],
                        "Tema": q["livro_tema"],
                        "Capítulo": q["capitulo_licao"],
                        "Enunciado": q["enunciado"],
                        "Correta": q["correta"],
                        "Explicação": q["explicacao_referencia"]
                    })
                st.dataframe(pd.DataFrame(lista_tabela), use_container_width=True, hide_index=True)

                st.markdown("---")
                st.markdown("##### 🗑️ Excluir Pergunta")
                col_del_id, col_del_btn = st.columns([2, 1])
                with col_del_id:
                    id_para_excluir = st.selectbox(
                        "Selecione o ID da pergunta a ser excluída:",
                        options=[q["id"] for q in todas_questoes],
                        format_func=lambda x: f"ID #{x} - {next((q['enunciado'][:60] + '...' for q in todas_questoes if q['id'] == x), '')}"
                    )
                with col_del_btn:
                    st.write("")
                    st.write("")
                    if st.button("Confirmar Exclusão", type="secondary", use_container_width=True):
                        sucesso = database.delete_questao(id_para_excluir)
                        if sucesso:
                            st.success(f"Questão #{id_para_excluir} removida com sucesso!")
                            st.rerun()
                        else:
                            st.error("Não foi possível excluir a questão.")
            else:
                st.warning("O banco de questões está vazio.")

        # ----------------------------------------------------------------------
        # SUB-ABA 4: GERENCIAR FOTOS (ASSETS)
        # ----------------------------------------------------------------------
        with prof_tab_fotos:
            st.markdown("#### 🖼️ Gerenciamento da Galeria de Fotos (pasta `assets/`)")
            st.caption("Adicione fotos das aulas, atividades dominicais e momentos inspiradores da Ala Periperi.")

            upload_foto = st.file_uploader("Enviar nova foto para a galeria:", type=["jpg", "jpeg", "png", "webp"])
            if upload_foto is not None:
                nome_foto = upload_foto.name
                col_save_f1, col_save_f2 = st.columns([2, 1])
                with col_save_f1:
                    legenda_custom = st.text_input("Nome/Legenda para o arquivo:", value=Path(nome_foto).stem)
                with col_save_f2:
                    st.write("")
                    st.write("")
                    if st.button("Salvar Foto na Galeria", use_container_width=True):
                        extensao = Path(nome_foto).suffix.lower()
                        novo_caminho = Path("assets") / f"{legenda_custom.strip().replace(' ', '_')}{extensao}"
                        os.makedirs("assets", exist_ok=True)
                        with open(novo_caminho, "wb") as f:
                            f.write(upload_foto.getbuffer())
                        st.success(f"Foto salva com sucesso como `{novo_caminho.name}`!")
                        st.rerun()

            # Lista de fotos existentes
            fotos_salvas = list(Path("assets").glob("*.*"))
            if fotos_salvas:
                st.markdown("##### Fotos Atualmente na Galeria:")
                for f_item in fotos_salvas:
                    if f_item.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif"]:
                        c_img, c_info, c_btn = st.columns([1, 2, 1])
                        with c_img:
                            st.image(str(f_item), width=100)
                        with c_info:
                            st.write(f"**Arquivo:** `{f_item.name}`")
                        with c_btn:
                            if st.button(f"Excluir", key=f"del_foto_{f_item.name}"):
                                try:
                                    f_item.unlink()
                                    st.success(f"Foto `{f_item.name}` removida!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Erro ao remover: {e}")

    elif senha_digitada != "":
        st.error("❌ Senha incorreta. Por favor, verifique a senha informada.")
    else:
        st.info("🔑 Digite a senha do professor para desbloquear as ferramentas administrativas.")
