import streamlit as st

# 1. Configuração da página Streamlit
st.set_page_config(
    page_title="Quiz do Pedro",
    page_icon="👶",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. CSS personalizado com cores pastéis
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #A0D8F7 0%, #FFB6D9 50%, #FFF4A3 100%);
        padding: 20px;
        min-height: 100vh; /* Garante que o fundo cubra toda a altura */
    }
    
    .stButton > button {
        background-color: #FFB6D9; /* Rosa Pastel */
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px 30px;
        font-size: 16px;
        border: none;
        width: 100%;
        transition: background-color 0.3s ease, transform 0.3s ease;
    }
    
    .stButton > button:hover:not(:disabled) {
        background-color: #A0D8F7; /* Azul Pastel */
        transform: scale(1.02);
    }

    .stButton > button:disabled {
        background-color: #cccccc; /* Cinza para botões desabilitados */
        cursor: not-allowed;
    }
    
    .stRadio > label {
        font-size: 16px;
        font-weight: 500;
        color: #333;
    }
    
    h1 {
        text-align: center;
        color: #333;
        font-size: 36px;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    h2 {
        color: #555;
        text-align: center;
        margin-top: 30px;
        margin-bottom: 20px;
    }
    
    .resultado {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #333;
        padding: 25px;
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 15px;
        margin: 30px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .stProgress > div > div > div > div {
        background-color: #A0D8F7; /* Azul Pastel para a barra de progresso */
    }
    </style>
""", unsafe_allow_html=True)

# 3. Dados do quiz
quiz_data = [
    {
        "pergunta": "Qual o nome do nosso bebê?",
        "opcoes": ["João", "Clovis", "Pedro"],
        "resposta_correta": 3  # Índice de "Pedro"
    },
    {
        "pergunta": "Quantos anos ele tem?",
        "opcoes": ["2", "11 meses", "3", "10"],
        "resposta_correta": 1  # Índice de "11 meses"
    },
    {
        "pergunta": "Qual o sobrenome dele?",
        "opcoes": ["Silva", "Pantuso", "Santos", "Oliveira"],
        "resposta_correta": 1  # Índice de "Pantuso"
    },
    {
        "pergunta": "Quantos irmãos ele tem?",
        "opcoes": ["1", "0", "2", "3"],
        "resposta_correta": 1  # Índice de "0"
    },
    {
        "pergunta": "Ele nasceu em qual estado?",
        "opcoes": ["MG", "SP", "PA", "ES"],
        "resposta_correta": 0  # Índice de "MG"
    }
]

# 10. Session state para gerenciar o estado do quiz
if "pergunta_atual" not in st.session_state:
    st.session_state.pergunta_atual = 0
    # Armazena o índice da opção selecionada
    st.session_state.respostas_usuario = [None] * len(quiz_data)
    st.session_state.quiz_terminado = False
    st.session_state.nota = 0

# Função para reiniciar o quiz


def reset_quiz():
    st.session_state.pergunta_atual = 0
    st.session_state.respostas_usuario = [None] * len(quiz_data)
    st.session_state.quiz_terminado = False
    st.session_state.nota = 0


# Título do aplicativo
st.markdown("<h1>👶 Quiz do Pedro 👶</h1>", unsafe_allow_html=True)

# 7. Tela de resultado
if st.session_state.quiz_terminado:
    st.markdown(
        f"<div class='resultado'>Sua nota: {st.session_state.nota}%</div>", unsafe_allow_html=True)

    # Imagem do Pedro (placeholder)
    # Para usar uma imagem real:
    # 1. Coloque o arquivo da imagem (ex: pedro.png) na mesma pasta do seu script.
    # 2. Substitua a URL abaixo pelo nome do arquivo: st.image("pedro.png", ...)
    # Ou use uma URL de imagem online: st.image("https://sua-url-da-imagem.com/pedro.jpg", ...)
    st.image("charme.png",
             caption="Nosso Pedro! 💕",
             use_container_width=True)  # 9. Usar use_container_width=True
    st.info("Retire sua missão com os pais que estão ao seu lado, caso aceitem")

    col1, col2 = st.columns(2)
    with col1:
        # 9. Usar use_container_width=True
        if st.button("🔄 Jogar Novamente", use_container_width=True):
            reset_quiz()
            st.rerun()
    with col2:
        if st.button("❌ Sair", use_container_width=True):  # 9. Usar use_container_width=True
            st.balloons()
            st.stop()  # Encerra a execução do script

# Quiz em andamento
else:
    # 5. Sistema de progresso com barra
    progresso = (st.session_state.pergunta_atual + 1) / len(quiz_data)
    st.progress(progresso)
    st.markdown(f"**Pergunta {st.session_state.pergunta_atual + 1} de {len(quiz_data)}**",
                help=f"Progresso: {int(progresso * 100)}%")

    pergunta_info = quiz_data[st.session_state.pergunta_atual]
    st.markdown(
        f"<h2>{pergunta_info['pergunta']}</h2>", unsafe_allow_html=True)

    # Recupera a resposta previamente selecionada para a pergunta atual, se houver
    default_index = st.session_state.respostas_usuario[st.session_state.pergunta_atual]

    # Opções de resposta
    resposta_selecionada_idx = st.radio(
        "Escolha uma opção:",
        options=range(len(pergunta_info['opcoes'])),
        format_func=lambda x: pergunta_info['opcoes'][x],
        index=default_index,  # Define a opção selecionada por padrão
        # Chave única para cada grupo de rádio
        key=f"pergunta_{st.session_state.pergunta_atual}"
    )

    # Armazena a seleção atual do usuário no session state
    st.session_state.respostas_usuario[st.session_state.pergunta_atual] = resposta_selecionada_idx

    col1, col2 = st.columns(2)

    # 5. Navegação entre perguntas (anterior/próximo)
    with col1:
        # 9. Usar use_container_width=True
        if st.button("⬅️ Anterior", use_container_width=True, disabled=(st.session_state.pergunta_atual == 0)):
            st.session_state.pergunta_atual -= 1
            st.rerun()

    with col2:
        if st.button("Próximo ➡️", use_container_width=True):  # 9. Usar use_container_width=True
            # 11. Validação de resposta correta (verifica se uma opção foi selecionada)
            if st.session_state.respostas_usuario[st.session_state.pergunta_atual] is None:
                st.warning(
                    "Por favor, selecione uma opção antes de prosseguir.")
            else:
                if st.session_state.pergunta_atual < len(quiz_data) - 1:
                    st.session_state.pergunta_atual += 1
                    st.rerun()
                else:
                    # Fim do quiz, calcular nota
                    acertos = 0
                    for i, resposta_dada_idx in enumerate(st.session_state.respostas_usuario):
                        if resposta_dada_idx == quiz_data[i]["resposta_correta"]:
                            acertos += 1

                    # 6. Cálculo de nota final em porcentagem
                    st.session_state.nota = int(
                        (acertos / len(quiz_data)) * 100)
                    st.session_state.quiz_terminado = True
                    st.rerun()
