import streamlit as st
import time

# Configuração da página
st.set_page_config(
    page_title="Quiz do Pedro",
    page_icon="👶",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS personalizado com cores pastéis
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #A0D8F7 0%, #FFB6D9 50%, #FFF4A3 100%);
        padding: 20px;
    }
    
    .stButton > button {
        background-color: #FFE100;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px 30px;
        font-size: 16px;
        border: none;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #3E9EA3;
        transform: scale(1.05);
    }
    
    .stRadio > label {
        font-size: 16px;
        font-weight: 500;
    }
    
    h1 {
        text-align: center;
        color: #333;
        font-size: 36px;
        margin-bottom: 20px;
    }
    
    h2 {
        color: #555;
        text-align: center;
    }
    
    .resultado {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: #333;
        padding: 20px;
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        margin: 20px 0;
    }
    
    .x-vermelho {
        font-size: 120px;
        color: red;
        text-align: center;
        font-weight: bold;
        animation: piscar 1s;
    }
    
    .x-verde {
        font-size: 120px;
        color: green;
        text-align: center;
        font-weight: bold;
        animation: piscar 1s;
    }
    
    @keyframes piscar {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    </style>
""", unsafe_allow_html=True)

# Dados do quiz
quiz_data = [
    {
        "pergunta": "Qual o nome do nosso bebê?",
        "opcoes": ["Clovis", "Pedro", "Lucas", "Mateus"],
        "resposta_correta": 1
    },
    {
        "pergunta": "Quantos anos ele tem?",
        "opcoes": ["2", "10", "3", "11 meses"],
        "resposta_correta": 3
    },
    {
        "pergunta": "Qual o sobrenome dele?",
        "opcoes": ["Silva", "Pantuso", "Santos", "Oliveira"],
        "resposta_correta": 1
    },
    {
        "pergunta": "Quantos irmãos ele tem?",
        "opcoes": ["1", "5", "2", "0"],
        "resposta_correta": 3
    },
    {
        "pergunta": "Onde ele nasceu?",
        "opcoes": ["SP", "MG", "RJ", "PA"],
        "resposta_correta": 1
    }
]

# Inicializar session state
if "pergunta_atual" not in st.session_state:
    st.session_state.pergunta_atual = 0
    st.session_state.respostas = [None] * len(quiz_data)
    st.session_state.quiz_terminado = False
    st.session_state.nota = 0
    st.session_state.mostrar_feedback = False
    st.session_state.feedback_tipo = None

# Cabeçalho
st.markdown("<h1>👶 Quiz 👶</h1>", unsafe_allow_html=True)

# Se o quiz terminou, mostrar resultado
if st.session_state.quiz_terminado:
    st.markdown(f"<div class='resultado'>Sua nota: {st.session_state.nota}%</div>", unsafe_allow_html=True)
    
    st.info("🎉 Parabéns! Você completou o quiz do Pedro!")
    
    # Exibir imagem do Pedro
    try:
        st.image("FotoNN.png", 
                 caption="Nosso Pedro! 💕", 
                 use_container_width=True)
    except:
        st.warning("Imagem não encontrada. Coloque o arquivo na mesma pasta do app.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Jogar Novamente", use_container_width=True):
            st.session_state.pergunta_atual = 0
            st.session_state.respostas = [None] * len(quiz_data)
            st.session_state.quiz_terminado = False
            st.session_state.nota = 0
            st.session_state.mostrar_feedback = False
            st.session_state.feedback_tipo = None
            st.rerun()
    
    with col2:
        if st.button("❌ Sair", use_container_width=True):
            st.balloons()

# Quiz em andamento
else:
    # Mostrar feedback visual
    if st.session_state.mostrar_feedback:
        if st.session_state.feedback_tipo == "correto":
            st.markdown("<div class='x-verde'>✓</div>", unsafe_allow_html=True)
        elif st.session_state.feedback_tipo == "errado":
            st.markdown("<div class='x-vermelho'>✕</div>", unsafe_allow_html=True)
        
        time.sleep(1)
        
        # Passar para próxima pergunta
        if st.session_state.pergunta_atual < len(quiz_data) - 1:
            st.session_state.pergunta_atual += 1
        else:
            # Calcular nota e terminar
            acertos = sum(1 for r in st.session_state.respostas if r == True)
            st.session_state.nota = int((acertos / len(quiz_data)) * 100)
            st.session_state.quiz_terminado = True
        
        st.session_state.mostrar_feedback = False
        st.session_state.feedback_tipo = None
        st.rerun()
    
    # Barra de progresso
    progresso = (st.session_state.pergunta_atual + 1) / len(quiz_data)
    st.progress(progresso)
    st.markdown(f"**Pergunta {st.session_state.pergunta_atual + 1} de {len(quiz_data)}**")
    
    # Pergunta atual
    pergunta_info = quiz_data[st.session_state.pergunta_atual]
    st.markdown(f"<h2>{pergunta_info['pergunta']}</h2>", unsafe_allow_html=True)
    
    # Opções de resposta
    resposta_selecionada = st.radio(
        "Escolha uma opção:",
        options=range(len(pergunta_info['opcoes'])),
        format_func=lambda x: pergunta_info['opcoes'][x],
        key=f"resposta_{st.session_state.pergunta_atual}"
    )
    
    # Botão próxima
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⬅️ Anterior", use_container_width=True, disabled=(st.session_state.pergunta_atual == 0)):
            if st.session_state.pergunta_atual > 0:
                st.session_state.pergunta_atual -= 1
                st.rerun()
    
    with col2:
        if st.button("Próximo ➡️", use_container_width=True):
            pergunta_info = quiz_data[st.session_state.pergunta_atual]
            
            # Verificar resposta
            if resposta_selecionada == pergunta_info['resposta_correta']:
                st.session_state.respostas[st.session_state.pergunta_atual] = True
                st.session_state.feedback_tipo = "correto"
            else:
                st.session_state.respostas[st.session_state.pergunta_atual] = False
                st.session_state.feedback_tipo = "errado"
            
            st.session_state.mostrar_feedback = True
            st.rerun()
