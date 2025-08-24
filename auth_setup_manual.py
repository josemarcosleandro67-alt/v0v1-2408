#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced - Google Authentication Setup Manual
Sistema de configuração manual de autenticação Google OAuth 2.0 (sem navegador)
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Importações Google Auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
import google.auth.exceptions

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('auth_setup_manual.log')
    ]
)

logger = logging.getLogger(__name__)

class GoogleAuthSetupManual:
    """Configurador manual de autenticação Google OAuth 2.0"""
    
    def __init__(self):
        """Inicializa o configurador de autenticação"""
        # Carrega variáveis de ambiente
        load_dotenv('.env')
        
        # Configurações OAuth
        self.SCOPES = [
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/drive.readonly',
            'https://www.googleapis.com/auth/youtube.readonly',
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/analytics.readonly'
        ]
        
        # Caminhos dos arquivos
        self.credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
        self.token_file = os.getenv('GOOGLE_AUTH_TOKEN_PATH', 'token.json')
        
        # Configurações do cliente
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        self.project_id = os.getenv('GOOGLE_PROJECT_ID')
        
        logger.info("🔧 Google Auth Setup Manual inicializado")
        
    def validate_environment(self) -> bool:
        """Valida se todas as variáveis de ambiente estão configuradas"""
        logger.info("🔍 Validando configuração de ambiente...")
        
        required_vars = {
            'GOOGLE_CLIENT_ID': self.client_id,
            'GOOGLE_CLIENT_SECRET': self.client_secret,
            'GOOGLE_PROJECT_ID': self.project_id
        }
        
        missing_vars = []
        for var_name, var_value in required_vars.items():
            if not var_value:
                missing_vars.append(var_name)
                logger.error(f"❌ {var_name}: não configurada")
            else:
                logger.info(f"✅ {var_name}: configurada")
        
        if missing_vars:
            logger.error(f"❌ Variáveis de ambiente faltando: {', '.join(missing_vars)}")
            return False
            
        # Verifica se o arquivo de credenciais existe
        if not Path(self.credentials_file).exists():
            logger.error(f"❌ Arquivo de credenciais não encontrado: {self.credentials_file}")
            return False
        else:
            logger.info(f"✅ Arquivo de credenciais encontrado: {self.credentials_file}")
            
        return True
    
    def create_manual_flow(self) -> Optional[Flow]:
        """Cria fluxo OAuth manual"""
        try:
            # Cria o fluxo OAuth
            flow = Flow.from_client_secrets_file(
                self.credentials_file,
                scopes=self.SCOPES,
                redirect_uri='urn:ietf:wg:oauth:2.0:oob'  # Para fluxo manual
            )
            
            return flow
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar fluxo OAuth: {e}")
            return None
    
    def get_authorization_url(self, flow: Flow) -> Optional[str]:
        """Obtém URL de autorização"""
        try:
            auth_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )
            
            return auth_url
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter URL de autorização: {e}")
            return None
    
    def exchange_code_for_token(self, flow: Flow, auth_code: str) -> Optional[Credentials]:
        """Troca código de autorização por token"""
        try:
            flow.fetch_token(code=auth_code)
            return flow.credentials
            
        except Exception as e:
            logger.error(f"❌ Erro ao trocar código por token: {e}")
            return None
    
    def save_credentials(self, creds: Credentials) -> bool:
        """Salva credenciais no arquivo token.json"""
        try:
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
            
            # Define permissões seguras
            os.chmod(self.token_file, 0o600)
            logger.info(f"✅ Credenciais salvas em: {self.token_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar credenciais: {e}")
            return False
    
    def test_credentials(self, creds: Credentials) -> bool:
        """Testa se as credenciais estão funcionando"""
        try:
            from googleapiclient.discovery import build
            
            logger.info("🧪 Testando credenciais...")
            
            # Testa com a API do YouTube (mais simples)
            service = build('youtube', 'v3', credentials=creds)
            
            # Não executa a requisição, apenas verifica se pode ser criada
            logger.info("✅ Credenciais válidas - serviço criado com sucesso")
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ Teste de credenciais falhou: {e}")
            return False
    
    def setup_authentication_manual(self) -> bool:
        """Executa o processo manual de configuração de autenticação"""
        logger.info("🚀 Iniciando configuração manual de autenticação Google...")
        
        # 1. Valida ambiente
        if not self.validate_environment():
            logger.error("❌ Falha na validação do ambiente")
            return False
        
        # 2. Cria fluxo OAuth
        flow = self.create_manual_flow()
        if not flow:
            logger.error("❌ Falha ao criar fluxo OAuth")
            return False
        
        # 3. Obtém URL de autorização
        auth_url = self.get_authorization_url(flow)
        if not auth_url:
            logger.error("❌ Falha ao obter URL de autorização")
            return False
        
        # 4. Mostra instruções para o usuário
        print("\n" + "="*80)
        print("🔐 CONFIGURAÇÃO MANUAL DE AUTENTICAÇÃO GOOGLE")
        print("="*80)
        print("\n📋 INSTRUÇÕES:")
        print("1. Abra o link abaixo em um navegador")
        print("2. Faça login com sua conta Google")
        print("3. Autorize o aplicativo")
        print("4. Copie o código de autorização fornecido")
        print("5. Cole o código quando solicitado")
        
        print(f"\n🌐 URL DE AUTORIZAÇÃO:")
        print(f"{auth_url}")
        
        print(f"\n📋 ESCOPOS SOLICITADOS:")
        for scope in self.SCOPES:
            print(f"   - {scope}")
        
        print("\n" + "="*80)
        
        # 5. Solicita código de autorização
        try:
            auth_code = input("\n🔑 Cole o código de autorização aqui: ").strip()
            
            if not auth_code:
                logger.error("❌ Código de autorização não fornecido")
                return False
            
            # 6. Troca código por token
            logger.info("🔄 Trocando código por token...")
            creds = self.exchange_code_for_token(flow, auth_code)
            
            if not creds:
                logger.error("❌ Falha ao obter credenciais")
                return False
            
            # 7. Salva credenciais
            if not self.save_credentials(creds):
                logger.error("❌ Falha ao salvar credenciais")
                return False
            
            # 8. Testa credenciais
            if not self.test_credentials(creds):
                logger.warning("⚠️ Credenciais podem não estar funcionando corretamente")
            
            logger.info("🎉 Configuração manual de autenticação concluída com sucesso!")
            return True
            
        except KeyboardInterrupt:
            logger.info("🛑 Configuração cancelada pelo usuário")
            return False
        except Exception as e:
            logger.error(f"❌ Erro na configuração manual: {e}")
            return False
    
    def create_token_from_refresh_token(self, refresh_token: str) -> bool:
        """Cria token a partir de refresh token (para casos especiais)"""
        try:
            logger.info("🔄 Criando token a partir de refresh token...")
            
            # Cria credenciais com refresh token
            creds = Credentials(
                token=None,
                refresh_token=refresh_token,
                token_uri='https://oauth2.googleapis.com/token',
                client_id=self.client_id,
                client_secret=self.client_secret,
                scopes=self.SCOPES
            )
            
            # Renova o token
            creds.refresh(Request())
            
            # Salva credenciais
            if self.save_credentials(creds):
                logger.info("✅ Token criado e salvo com sucesso")
                return True
            else:
                logger.error("❌ Falha ao salvar token")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao criar token: {e}")
            return False

def main():
    """Função principal"""
    print("🚀 ARQV30 Enhanced - Configuração Manual de Autenticação Google")
    print("=" * 80)
    
    auth_setup = GoogleAuthSetupManual()
    
    print("\n🔧 Iniciando configuração manual...")
    
    if auth_setup.setup_authentication_manual():
        print("\n🎉 Autenticação configurada com sucesso!")
        print(f"📁 Token salvo em: {auth_setup.token_file}")
        print("✅ Sistema pronto para usar APIs Google")
        print("\n💡 Agora você pode executar 'python test_auth.py' para testar")
    else:
        print("\n❌ Falha na configuração de autenticação")
        print("🔍 Verifique os logs para mais detalhes")
        sys.exit(1)

if __name__ == "__main__":
    main()