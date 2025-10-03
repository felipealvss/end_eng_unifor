import streamlit as st
import subprocess
import os

st.set_page_config(page_title="📊 Dashboard Principal", layout="wide")

# Diretório base
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

st.title("🚀 Pipeline de ETL")
st.subheader("Orquestração de Etapas")

# Área centralizada de log
st.markdown("### 📜 Painel de Logs")
log_area = st.empty()

# Mapeamento de botões e scripts
pipeline_steps = {
    "1. Ingestão da API": "01_ingestao_api.py",
    "2. Envio para Landing Zone": "02_envio_landingzone_aws.py",
    "3. Carga Bronze": "03_carga_bronze_aws.py",
    "4. Transformação Silver": "04_transform_silver_aws.py",
    "5. Geração Gold": "05_gera_gold_aws.py"
}

# CSS customizado para botões
st.markdown("""
<style>
/* Estilo padrão dos botões individuais */
div[data-testid^="stButton"] > button {
    height: auto;
    width: auto;
    min-height: 120px;
    min-width: 160px;
    border-radius: 16px;
    font-weight: 600;
    font-size: 16px;
    margin: 6px;
    color: black;
    white-space: normal;
}

/* Estilo especial do botão Executar Pipeline Completo */
div[data-testid="stButton"][key="pipeline_completo"] > button {
    height: 160px !important;
    width: 100% !important;
    border-radius: 20px !important;
    font-weight: 700 !important;
    font-size: 20px !important;
    background-color: #4CAF50 !important; /* verde destaque */
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# Centralizar botões individuais
left_space, buttons_area, right_space = st.columns([1, 3, 1])

with buttons_area:
    # Botões individuais em linha
    cols = st.columns(len(pipeline_steps))
    for i, (step_name, script_file) in enumerate(pipeline_steps.items()):
        with cols[i]:
            if st.button(step_name, key=step_name):
                try:
                    with st.spinner(f"Executando {step_name}..."):
                        result = subprocess.run(
                            ["poetry", "run", "python", os.path.join(SCRIPT_DIR, "python", script_file)],
                            check=True,
                            capture_output=True,
                            text=True,
                        )
                    st.success(f"✅ Etapa '{step_name}' concluída com sucesso!")
                    log_area.code(result.stdout or "Sem saída gerada", language="bash")
                except subprocess.CalledProcessError as e:
                    st.error(f"❌ Erro na etapa '{step_name}'!")
                    log_area.code(e.stderr or "Sem log de erro", language="bash")
                except Exception as e:
                    st.error(f"❌ Ocorreu um erro inesperado: {e}")
                    log_area.code(str(e), language="bash")

# --- Botão único fora do bloco, centralizado na tela ---
st.markdown("---")  # linha divisória opcional
left, center, right = st.columns([1, 2, 1])
with center:
    if st.button("Executar Pipeline Completo", key="pipeline_completo"):
        logs = ""
        try:
            for step_name, script_file in pipeline_steps.items():
                with st.spinner(f"Executando {step_name}..."):
                    result = subprocess.run(
                        ["poetry", "run", "python", os.path.join(SCRIPT_DIR, "python", script_file)],
                        check=True,
                        capture_output=True,
                        text=True,
                    )
                st.success(f"✅ Etapa '{step_name}' concluída com sucesso!")
                logs += f"### {step_name}\n{result.stdout or 'Sem saída gerada'}\n\n"

        except subprocess.CalledProcessError as e:
            st.error(f"❌ Erro na etapa '{step_name}'!")
            logs += f"### {step_name} (ERRO)\n{e.stderr or 'Sem log de erro'}\n\n"

        except Exception as e:
            st.error(f"❌ Ocorreu um erro inesperado: {e}")
            logs += f"### Erro inesperado\n{str(e)}\n\n"

        log_area.markdown(logs)
