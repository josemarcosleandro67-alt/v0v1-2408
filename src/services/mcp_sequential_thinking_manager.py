import os
import requests
import logging

logger = logging.getLogger(__name__)

class MCPSequentialThinkingManager:
    def __init__(self):
        # CONFIGURAÇÃO SMITHERY AI CONFORME PLANO
        self.base_url = os.getenv(
            'MCP_SEQUENTIAL_THINKING_URL', 
            'https://smithery.ai/server/@smithery-ai/server-sequential-thinking'
        )
        if not self.base_url:
            logger.error("MCP_SEQUENTIAL_THINKING_URL não configurado nas variáveis de ambiente.")
            raise ValueError("MCP_SEQUENTIAL_THINKING_URL não configurado.")

    def start_thinking_process(self, problem_description: str, initial_context: dict = None) -> dict:
        """Inicia um novo processo de pensamento sequencial."""
        endpoint = f"{self.base_url}/start"
        payload = {
            "problem_description": problem_description,
            "initial_context": initial_context if initial_context else {}
        }
        try:
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()  # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao iniciar processo de pensamento sequencial: {e}")
            return {"error": str(e)}

    def advance_thinking_step(self, process_id: str, user_input: str = None) -> dict:
        """Avança para o próximo passo no processo de pensamento sequencial."""
        endpoint = f"{self.base_url}/advance"
        payload = {
            "process_id": process_id,
            "user_input": user_input
        }
        try:
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao avançar passo de pensamento sequencial: {e}")
            return {"error": str(e)}

    def get_process_status(self, process_id: str) -> dict:
        """Obtém o status atual de um processo de pensamento sequencial."""
        endpoint = f"{self.base_url}/status"
        payload = {"process_id": process_id}
        try:
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao obter status do processo de pensamento sequencial: {e}")
            return {"error": str(e)}

# Exemplo de uso (apenas para demonstração, remover em produção)
if __name__ == "__main__":
    # Para testar, defina a variável de ambiente antes de executar este script
    # Ex: export MCP_SEQUENTIAL_THINKING_URL="https://smithery.ai/server/@xinzhongyouhai/mcp-sequentialthinking-tools"
    # Ou adicione ao seu .env e carregue com python-dotenv
    from dotenv import load_dotenv
    load_dotenv()

    manager = MCPSequentialThinkingManager()

    # Exemplo de início de um processo
    print("Iniciando processo de pensamento...")
    result = manager.start_thinking_process("Como otimizar a busca de dados em uma aplicação Flask?")
    print(result)

    if "process_id" in result:
        process_id = result["process_id"]
        print(f"Processo iniciado com ID: {process_id}")

        # Exemplo de avanço de um passo
        print("Avançando para o próximo passo...")
        step_result = manager.advance_thinking_step(process_id)
        print(step_result)

        # Exemplo de obtenção de status
        print("Obtendo status do processo...")
        status = manager.get_process_status(process_id)
        print(status)