import streamlit as st
import subprocess
import os

st.set_page_config(page_title="📊 Dashboard Principal", layout="wide")

# Diretório base
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

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

# Renderiza botões
for step_name, script_file in pipeline_steps.items():
    st.divider()
    if st.button(step_name, use_container_width=True):
        try:
            with st.spinner(f"Executando {step_name}..."):
                result = subprocess.run(
                    ["poetry", "run", "python", os.path.join(SCRIPT_DIR, script_file)],
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

# Visualização de dados da camada Gold
#st.subheader("Visualização Camada Gold")
#st.info("Aqui você pode adicionar código para ler os dados da sua camada Gold e exibir um resumo ou gráfico.")
