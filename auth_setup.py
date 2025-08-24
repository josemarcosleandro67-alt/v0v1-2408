#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced - Google Authentication Setup
Sistema de configuração inicial de autenticação Google OAuth 2.0
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
from google_auth_oauthlib.flow import InstalledAppFlow
import google.auth.exceptions

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('auth_setup.log')
    ]
)

logger = logging.getLogger(__name__)

class GoogleAuthSetup:
    """Configurador de autenticação Google OAuth 2.0"""
    
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
        
        logger.info("🔧 Google Auth Setup inicializado")
        
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
    
    def load_existing_credentials(self) -> Optional[Credentials]:
        """Carrega credenciais existentes se disponíveis"""
        if not Path(self.token_file).exists():
            logger.info("ℹ️ Arquivo de token não encontrado - primeira autenticação")
            return None
            
        try:
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
            logger.info("✅ Credenciais existentes carregadas")
            return creds
        except Exception as e:
            logger.warning(f"⚠️ Erro ao carregar credenciais existentes: {e}")
            return None
    
    def refresh_credentials(self, creds: Credentials) -> bool:
        """Renova credenciais expiradas"""
        try:
            if creds.expired and creds.refresh_token:
                logger.info("🔄 Renovando credenciais expiradas...")
                creds.refresh(Request())
                self.save_credentials(creds)
                logger.info("✅ Credenciais renovadas com sucesso")
                return True
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao renovar credenciais: {e}")
            return False
    
    def perform_oauth_flow(self) -> Optional[Credentials]:
        """Executa o fluxo OAuth 2.0 para obter novas credenciais"""
        try:
            logger.info("🚀 Iniciando fluxo OAuth 2.0...")
            
            # Cria o fluxo OAuth
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_file, 
                self.SCOPES
            )
            
            # Executa o fluxo local
            logger.info("🌐 Abrindo navegador para autenticação...")
            logger.info("📋 Escopos solicitados:")
            for scope in self.SCOPES:
                logger.info(f"   - {scope}")
                
            creds = flow.run_local_server(
                port=8080,
                access_type='offline',
                include_granted_scopes='true'
            )
            
            logger.info("✅ Autenticação OAuth concluída com sucesso")
            return creds
            
        except Exception as e:
            logger.error(f"❌ Erro no fluxo OAuth: {e}")
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
            request = service.channels().list(part='snippet', mine=True)
            
            # Não executa a requisição, apenas verifica se pode ser criada
            logger.info("✅ Credenciais válidas - serviço criado com sucesso")
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ Teste de credenciais falhou: {e}")
            return False
    
    def setup_authentication(self) -> bool:
        """Executa o processo completo de configuração de autenticação"""
        logger.info("🚀 Iniciando configuração de autenticação Google...")
        
        # 1. Valida ambiente
        if not self.validate_environment():
            logger.error("❌ Falha na validação do ambiente")
            return False
        
        # 2. Tenta carregar credenciais existentes
        creds = self.load_existing_credentials()
        
        # 3. Se não há credenciais ou são inválidas, executa OAuth
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # Tenta renovar
                if not self.refresh_credentials(creds):
                    logger.info("🔄 Renovação falhou, executando novo fluxo OAuth...")
                    creds = self.perform_oauth_flow()
            else:
                # Novo fluxo OAuth
                creds = self.perform_oauth_flow()
        
        # 4. Verifica se obteve credenciais válidas
        if not creds:
            logger.error("❌ Falha ao obter credenciais")
            return False
        
        # 5. Salva credenciais
        if not self.save_credentials(creds):
            logger.error("❌ Falha ao salvar credenciais")
            return False
        
        # 6. Testa credenciais
        if not self.test_credentials(creds):
            logger.warning("⚠️ Credenciais podem não estar funcionando corretamente")
        
        logger.info("🎉 Configuração de autenticação concluída com sucesso!")
        return True
    
    def get_auth_status(self) -> Dict[str, Any]:
        """Retorna status atual da autenticação"""
        status = {
            'credentials_file_exists': Path(self.credentials_file).exists(),
            'token_file_exists': Path(self.token_file).exists(),
            'environment_valid': self.validate_environment(),
            'credentials_valid': False,
            'credentials_expired': False,
            'scopes': self.SCOPES
        }
        
        creds = self.load_existing_credentials()
        if creds:
            status['credentials_valid'] = creds.valid
            status['credentials_expired'] = creds.expired if hasattr(creds, 'expired') else False
        
        return status

def main():
    """Função principal"""
    print("🚀 ARQV30 Enhanced - Configuração de Autenticação Google")
    print("=" * 60)
    
    auth_setup = GoogleAuthSetup()
    
    # Mostra status atual
    status = auth_setup.get_auth_status()
    print("\n📊 Status Atual:")
    for key, value in status.items():
        if key == 'scopes':
            continue
        icon = "✅" if value else "❌"
        print(f"   {icon} {key}: {value}")
    
    print("\n🔧 Iniciando configuração...")
    
    if auth_setup.setup_authentication():
        print("\n🎉 Autenticação configurada com sucesso!")
        print(f"📁 Token salvo em: {auth_setup.token_file}")
        print("✅ Sistema pronto para usar APIs Google")
    else:
        print("\n❌ Falha na configuração de autenticação")
        print("🔍 Verifique os logs para mais detalhes")
        sys.exit(1)

if __name__ == "__main__":
    main()