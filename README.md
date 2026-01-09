

rm -rf .venv
# Elimina el entorno virtual existente para empezar desde cero

## init
uv init
# Inicializa un proyecto Python administrado por uv

uv venv
# Crea un nuevo entorno virtual (.venv)

# add dependencies
uv add --pre langgraph langchain langchain-openai
# Instala LangGraph, LangChain y la integración con OpenAI (permitiendo versiones pre-release)

uv add "langgraph-cli[inmem]"
# Instala el CLI de LangGraph con backend en memoria para desarrollo local

# run the agent
uv run langgraph dev
# Ejecuta el servidor de desarrollo de LangGraph y abre la interfaz web

# add ipykernel for jupyter
uv add ipykernel --dev
# Agrega soporte para usar el entorno virtual en Jupyter Notebook

# install the project
uv pip install -e .
# Instala el proyecto en modo editable para desarrollo


echo "# agentes_ia_langGraph" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/joem9819/agentes_ia_langGraph.git
git push -u origin main

git remote add origin https://github.com/joem9819/agentes_ia_langGraph.git
git branch -M main
git push -u origin main