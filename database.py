"""
database.py - Módulo de persistência SQLite para a Escola Dominical — Ala Periperi
Gerencia as tabelas 'questoes' e 'ranking' com inicialização automática e sementes de estudo.
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_NAME = "escola_dominical_periperi.db"


def get_connection() -> sqlite3.Connection:
    """Retorna uma conexão SQLite com suporte a dicionários."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Cria as tabelas caso não existam e popula com 5 questões reais caso a tabela esteja vazia."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # 1. Tabela questoes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                livro_tema TEXT NOT NULL,
                capitulo_licao TEXT NOT NULL,
                enunciado TEXT NOT NULL,
                opcoes_json TEXT NOT NULL,
                correta TEXT NOT NULL,
                explicacao_referencia TEXT NOT NULL
            )
        """)

        # 2. Tabela ranking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ranking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_aluno TEXT NOT NULL,
                tema TEXT NOT NULL,
                acertos INTEGER NOT NULL,
                total INTEGER NOT NULL,
                porcentagem REAL NOT NULL,
                data_hora TEXT NOT NULL
            )
        """)

        conn.commit()

        # Verifica se há dados na tabela questoes; se não, insere as 5 sementes
        cursor.execute("SELECT COUNT(*) FROM questoes")
        total_questoes = cursor.fetchone()[0]

        if total_questoes == 0:
            seed_questoes(conn)


def seed_questoes(conn: sqlite3.Connection) -> None:
    """Popula 5 questões reais e inspiradoras das escrituras para a Ala Periperi."""
    questoes_iniciais = [
        {
            "livro_tema": "Vem, e Segue-Me — Livro de Mórmon",
            "capitulo_licao": "1 Néfi 3 (Obediência e Fé)",
            "enunciado": "Quando Leí instruiu seus filhos a retornarem a Jerusalém para obter as placas de latão de Labão, qual foi a corajosa resposta de fé proferida por Néfi?",
            "opcoes": {
                "A": "O Senhor proverá um caminho, mas devemos aguardar em nossa tenda até que Ele nos dê um sinal visível.",
                "B": "Eu irei e farei as coisas que o Senhor ordenou, porque sei que o Senhor nunca dá ordens aos filhos dos homens sem antes preparar um caminho.",
                "C": "É melhor que pereça um homem do que uma nação inteira pereça e definhe na incredulidade.",
                "D": "Despertai e levantai-vos do pó, meus irmãos, e sede homens fiéis perante a lei de Moisés."
            },
            "correta": "B",
            "explicacao_referencia": "1 Néfi 3:7 — Néfi expressou sua profunda confiança no Senhor ao declarar: 'Eu irei e farei as coisas que o Senhor ordenou, porque sei que o Senhor nunca dá ordens aos filhos dos homens sem antes preparar um caminho para que possam cumprir o que lhes ordena.'"
        },
        {
            "livro_tema": "Novo Testamento",
            "capitulo_licao": "Mateus 5 (Sermão da Montanha)",
            "enunciado": "No Sermão da Montanha, o Salvador Jesus Cristo ensinou sobre o papel e a influência transformadora dos Seus discípulos no mundo usando duas metáforas conhecidas. Quais são?",
            "opcoes": {
                "A": "O sal da terra e a luz do mundo",
                "B": "A videira verdadeira e os ramos frutíferos",
                "C": "O trigo precioso e o joio colhido",
                "D": "O bom pastor e as ovelhas pacificadoras"
            },
            "correta": "A",
            "explicacao_referencia": "Mateus 5:13-14 — Jesus ensinou: 'Vós sois o sal da terra (...) Vós sois a luz do mundo; não se pode esconder uma cidade edificada sobre um monte.'"
        },
        {
            "livro_tema": "Vem, e Segue-Me — Livro de Mórmon",
            "capitulo_licao": "Mosias 2 (Discurso do Rei Benjamim)",
            "enunciado": "Ao ensinar seu povo do alto de sua torre em Zaraenla, que princípio fundamental de serviço e caridade o Rei Benjamim enfatizou?",
            "opcoes": {
                "A": "A oração fervorosa e constante do homem reto pode muito em seus efeitos.",
                "B": "A glória de Deus é inteligência, luz e conhecimento eterno para todos os Seus filhos.",
                "C": "Quando estais a serviço de vosso próximo, estais somente a serviço de vosso Deus.",
                "D": "Nenhum sucesso mundano compensa o fracasso no ambiente familiar do lar."
            },
            "correta": "C",
            "explicacao_referencia": "Mosias 2:17 — O nobre Rei Benjamim declarou: 'E eis que vos digo estas coisas para que aprendais sabedoria; para que saibais que, quando estais a serviço de vosso próximo, estais somente a serviço de vosso Deus.'"
        },
        {
            "livro_tema": "Vem, e Segue-Me — Livro de Mórmon",
            "capitulo_licao": "Alma 32 (A Fé e a Palavra)",
            "enunciado": "Ao pregar aos zoramitas humildes que haviam sido desprezados e expulsos de suas sinagogas, como o profeta Alma ensinou a exercitar a fé e experimentar a palavra de Deus?",
            "opcoes": {
                "A": "Comparando a palavra a uma rocha firme sobre a qual os homens devem construir seus alicerces.",
                "B": "Comparando a palavra a uma semente que deve ser plantada no coração para que germine e cresça.",
                "C": "Comparando a palavra a uma lâmpada acesa que nunca se apaga nas noites escuras.",
                "D": "Comparando a palavra a um elmo de salvação para vencer as tentações do adversário."
            },
            "correta": "B",
            "explicacao_referencia": "Alma 32:28 — Alma aconselha: 'Ora, compararemos a palavra a uma semente. Se derdes lugar para que uma semente seja plantada em vosso coração (...) começará a inchar em vosso peito; e quando sentirdes essas sensações de crescimento, começareis a dizer a vós mesmos: Deve ser uma boa semente.'"
        },
        {
            "livro_tema": "Doutrinas e Princípios do Evangelho",
            "capitulo_licao": "Morôni 10 (A Promessa do Livro de Mórmon)",
            "enunciado": "De acordo com a promessa final do profeta Morôni, como uma pessoa pode receber um testemunho seguro da verdade das escrituras?",
            "opcoes": {
                "A": "Perguntando a Deus com um coração sincero, real intenção e fé em Cristo, e Ele manifestará a verdade pelo poder do Espírito Santo.",
                "B": "Lendo as escrituras rapidamente sem necessidade de orar ou meditar profundamente sobre as misericórdias do Senhor.",
                "C": "Aguardando um sinal miraculoso exterior que force o conhecimento intelectual do leitor.",
                "D": "Consultando apenas debates filosóficos e argumentos humanos sem buscar revelação espiritual pessoal."
            },
            "correta": "A",
            "explicacao_referencia": "Morôni 10:4-5 — Morôni convida: 'E quando receberdes estas coisas, eu vos exorto a que pergunteis a Deus, o Pai Eterno, em nome de Cristo, se estas coisas não são verdadeiras; e se perguntardes com um coração sincero e com real intenção, tendo fé em Cristo, ele vos manifestará a verdade delas pelo poder do Espírito Santo.'"
        }
    ]

    cursor = conn.cursor()
    for q in questoes_iniciais:
        cursor.execute("""
            INSERT INTO questoes (livro_tema, capitulo_licao, enunciado, opcoes_json, correta, explicacao_referencia)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            q["livro_tema"],
            q["capitulo_licao"],
            q["enunciado"],
            json.dumps(q["opcoes"], ensure_ascii=False),
            q["correta"],
            q["explicacao_referencia"]
        ))
    conn.commit()


# ==========================================
# FUNÇÕES CRUD: QUESTÕES
# ==========================================

def get_questoes(livro_tema: Optional[str] = None, capitulo_licao: Optional[str] = None) -> List[Dict[str, Any]]:
    """Recupera a lista de questões cadastradas, com filtros opcionais."""
    with get_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM questoes WHERE 1=1"
        params = []

        if livro_tema and livro_tema != "Todos":
            query += " AND livro_tema = ?"
            params.append(livro_tema)

        if capitulo_licao and capitulo_licao != "Todas":
            query += " AND capitulo_licao = ?"
            params.append(capitulo_licao)

        query += " ORDER BY id ASC"
        cursor.execute(query, params)
        rows = cursor.fetchall()

        result = []
        for r in rows:
            opcoes = {}
            try:
                opcoes = json.loads(r["opcoes_json"])
            except Exception:
                opcoes = {"A": "", "B": "", "C": "", "D": ""}

            result.append({
                "id": r["id"],
                "livro_tema": r["livro_tema"],
                "capitulo_licao": r["capitulo_licao"],
                "enunciado": r["enunciado"],
                "opcoes": opcoes,
                "correta": r["correta"],
                "explicacao_referencia": r["explicacao_referencia"]
            })
        return result


def get_temas() -> List[str]:
    """Retorna a lista de temas/livros distintos no banco."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT livro_tema FROM questoes ORDER BY livro_tema ASC")
        rows = cursor.fetchall()
        return [r["livro_tema"] for r in rows if r["livro_tema"]]


def get_capitulos(livro_tema: Optional[str] = None) -> List[str]:
    """Retorna os capítulos/lições disponíveis para um tema ou no total."""
    with get_connection() as conn:
        cursor = conn.cursor()
        if livro_tema and livro_tema != "Todos":
            cursor.execute("SELECT DISTINCT capitulo_licao FROM questoes WHERE livro_tema = ? ORDER BY capitulo_licao ASC", (livro_tema,))
        else:
            cursor.execute("SELECT DISTINCT capitulo_licao FROM questoes ORDER BY capitulo_licao ASC")
        rows = cursor.fetchall()
        return [r["capitulo_licao"] for r in rows if r["capitulo_licao"]]


def add_questao(
    livro_tema: str,
    capitulo_licao: str,
    enunciado: str,
    opcoes: Dict[str, str],
    correta: str,
    explicacao_referencia: str
) -> int:
    """Insere uma nova questão no banco de dados."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO questoes (livro_tema, capitulo_licao, enunciado, opcoes_json, correta, explicacao_referencia)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            livro_tema.strip(),
            capitulo_licao.strip(),
            enunciado.strip(),
            json.dumps(opcoes, ensure_ascii=False),
            correta.strip().upper(),
            explicacao_referencia.strip()
        ))
        conn.commit()
        return cursor.lastrowid


def delete_questao(questao_id: int) -> bool:
    """Remove uma questão pelo ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM questoes WHERE id = ?", (questao_id,))
        conn.commit()
        return cursor.rowcount > 0


# ==========================================
# FUNÇÕES CRUD: RANKING
# ==========================================

def save_ranking(nome_aluno: str, tema: str, acertos: int, total: int, porcentagem: float) -> int:
    """Registra uma tentativa de quiz no ranking."""
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ranking (nome_aluno, tema, acertos, total, porcentagem, data_hora)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            nome_aluno.strip(),
            tema.strip(),
            acertos,
            total,
            round(porcentagem, 1),
            data_hora
        ))
        conn.commit()
        return cursor.lastrowid


def get_ranking(tema: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
    """Retorna os registros do ranking ordenados por porcentagem decrescente e acertos."""
    with get_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM ranking WHERE 1=1"
        params = []

        if tema and tema != "Todos":
            query += " AND tema = ?"
            params.append(tema)

        query += " ORDER BY porcentagem DESC, acertos DESC, id DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [dict(r) for r in rows]


def get_estatisticas_ranking() -> Dict[str, Any]:
    """Calcula estatísticas gerais para os cards do quadro de destaque."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) AS total_tentativas,
                COUNT(DISTINCT nome_aluno) AS total_alunos,
                AVG(porcentagem) AS media_porcentagem,
                MAX(porcentagem) AS maior_porcentagem
            FROM ranking
        """)
        row = cursor.fetchone()
        return {
            "total_tentativas": row["total_tentativas"] or 0,
            "total_alunos": row["total_alunos"] or 0,
            "media_porcentagem": round(row["media_porcentagem"] or 0.0, 1),
            "maior_porcentagem": round(row["maior_porcentagem"] or 0.0, 1)
        }
