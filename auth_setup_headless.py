#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced - Google Authentication Setup (Headless)
Sistema de configuração de autenticação Google para ambientes sem navegador
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class GoogleAuthSetupHeadless:
    """Configurador de autenticação Google para ambientes headless"""
    
    def __init__(self):
        """Inicializa o configurador"""
        load_dotenv('.env')
        
        self.credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
        self.token_file = os.getenv('GOOGLE_AUTH_TOKEN_PATH', 'token.json')
        
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        self.project_id = os.getenv('GOOGLE_PROJECT_ID')
        
        logger.info("🔧 Google Auth Setup Headless inicializado")
    
    def validate_environment(self) -> bool:
        """Valida configuração de ambiente"""
        logger.info("🔍 Validando configuração...")
        
        required_vars = {
            'GOOGLE_CLIENT_ID': self.client_id,
            'GOOGLE_CLIENT_SECRET': self.client_secret,
            'GOOGLE_PROJECT_ID': self.project_id
        }
        
        all_valid = True
        for var_name, var_value in required_vars.items():
            if var_value:
                logger.info(f"✅ {var_name}: configurada")
            else:
                logger.error(f"❌ {var_name}: não configurada")
                all_valid = False
        
        if Path(self.credentials_file).exists():
            logger.info(f"✅ Arquivo de credenciais: {self.credentials_file}")
        else:
            logger.error(f"❌ Arquivo de credenciais não encontrado: {self.credentials_file}")
            all_valid = False
        
        return all_valid
    
    def create_manual_token_template(self) -> str:
        """Cria template para token manual"""
        template = {
            "token": "YOUR_ACCESS_TOKEN_HERE",
            "refresh_token": "YOUR_REFRESH_TOKEN_HERE",
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scopes": [
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/drive.readonly",
                "https://www.googleapis.com/auth/youtube.readonly",
                "https://www.googleapis.com/auth/gmail.readonly",
                "https://www.googleapis.com/auth/analytics.readonly"
            ]
        }
        
        template_file = 'token_template.json'
        with open(template_file, 'w') as f:
            json.dump(template, f, indent=2)
        
        return template_file
    
    def generate_auth_url(self) -> str:
        """Gera URL de autenticação manual"""
        from urllib.parse import urlencode
        
        params = {
            'client_id': self.client_id,
            'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
            'scope': ' '.join([
                'https://www.googleapis.com/auth/cloud-platform',
                'https://www.googleapis.com/auth/drive.readonly',
                'https://www.googleapis.com/auth/youtube.readonly',
                'https://www.googleapis.com/auth/gmail.readonly',
                'https://www.googleapis.com/auth/analytics.readonly'
            ]),
            'response_type': 'code',
            'access_type': 'offline',
            'include_granted_scopes': 'true'
        }
        
        auth_url = f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"
        return auth_url
    
    def setup_manual_auth(self):
        """Configura autenticação manual"""
        print("\n🔧 CONFIGURAÇÃO MANUAL DE AUTENTICAÇÃO GOOGLE")
        print("=" * 60)
        
        if not self.validate_environment():
            print("❌ Configuração de ambiente inválida")
            return False
        
        # Gera URL de autenticação
        auth_url = self.generate_auth_url()
        
        print("\n📋 INSTRUÇÕES PARA AUTENTICAÇÃO MANUAL:")
        print("-" * 40)
        print("1. Abra o seguinte link em um navegador:")
        print(f"\n{auth_url}\n")
        print("2. Faça login com sua conta Google")
        print("3. Autorize o aplicativo")
        print("4. Copie o código de autorização fornecido")
        print("5. Use o código para obter tokens de acesso")
        
        # Cria template
        template_file = self.create_manual_token_template()
        print(f"\n📁 Template criado: {template_file}")
        print("   Edite este arquivo com seus tokens reais")
        
        print("\n💡 ALTERNATIVAS:")
        print("- Execute em um ambiente com navegador")
        print("- Use Google Cloud Shell")
        print("- Configure tokens manualmente via API")
        
        return True

def main():
    """Função principal"""
    print("🚀 ARQV30 Enhanced - Configuração Google (Headless)")
    print("=" * 60)
    
    setup = GoogleAuthSetupHeadless()
    setup.setup_manual_auth()

if __name__ == "__main__":
    main()