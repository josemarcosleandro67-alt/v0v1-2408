"""
Sistema Avançado de Rotação de APIs - V3.0
Garante alta disponibilidade com fallback automático entre múltiplas APIs
"""

import os
import time
import random
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime, timedelta
import threading
import requests
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

logger = logging.getLogger(__name__)

class APIStatus(Enum):
    ACTIVE = "active"
    RATE_LIMITED = "rate_limited"
    ERROR = "error"
    OFFLINE = "offline"

@dataclass
class APIEndpoint:
    name: str
    api_key: str
    base_url: str
    status: APIStatus = APIStatus.ACTIVE
    last_used: datetime = None
    error_count: int = 0
    rate_limit_reset: datetime = None
    requests_made: int = 0
    max_requests_per_minute: int = 60

class EnhancedAPIRotationManager:
    """
    Gerenciador avançado de rotação de APIs com:
    - Fallback automático entre modelos
    - Rate limiting inteligente
    - Health checking
    - Balanceamento de carga
    """
    
    def __init__(self):
        self.apis = {
            'qwen': [],
            'gemini': [],
            'groq': [],
            'tavily': [],
            'exa': [],
            'serpapi': [],
            'youtube': []
        }
        self.current_api_index = {}
        self.lock = threading.Lock()
        self.health_check_interval = 300  # 5 minutos
        self.last_health_check = {}
        
        self._load_api_configurations()
        self._initialize_health_monitoring()
    
    def _load_api_configurations(self):
        """Carrega configurações de APIs do .env"""
        try:
            # Qwen (OpenRouter) - Usar as chaves reais
            openrouter_keys = [
                os.getenv('OPENROUTER_API_KEY'),
                os.getenv('OPENROUTER_API_KEY_1'),
                os.getenv('OPENROUTER_API_KEY_2')
            ]
            
            for i, key in enumerate(openrouter_keys, 1):
                if key and key not in ['your_openrouter_key_1', 'your_openrouter_key_2', None]:
                    self.apis['qwen'].append(APIEndpoint(
                        name=f"qwen_{i}",
                        api_key=key,
                        base_url=os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1'),
                        max_requests_per_minute=100
                    ))
            
            # Gemini - Usar as chaves reais
            gemini_keys = [
                os.getenv('GEMINI_API_KEY'),
                os.getenv('GEMINI_API_KEY_1')
            ]
            
            for i, key in enumerate(gemini_keys, 1):
                if key and key not in ['your_gemini_key_1', 'your_gemini_key_2', None]:
                    self.apis['gemini'].append(APIEndpoint(
                        name=f"gemini_{i}",
                        api_key=key,
                        base_url="https://generativelanguage.googleapis.com/v1beta",
                        max_requests_per_minute=60
                    ))
            
            # Groq - Usar as chaves reais
            groq_keys = [
                os.getenv('GROQ_API_KEY'),
                os.getenv('GROQ_API_KEY_1')
            ]
            
            for i, key in enumerate(groq_keys, 1):
                if key and key not in ['your_groq_key_1', 'your_groq_key_2', None]:
                    self.apis['groq'].append(APIEndpoint(
                        name=f"groq_{i}",
                        api_key=key,
                        base_url="https://api.groq.com/openai/v1",
                        max_requests_per_minute=30
                    ))
            
            # Tavily
            tavily_key = os.getenv('TAVILY_API_KEY')
            if tavily_key and tavily_key not in ['your_tavily_key_1', None]:
                self.apis['tavily'].append(APIEndpoint(
                    name="tavily_1",
                    api_key=tavily_key,
                    base_url="https://api.tavily.com",
                    max_requests_per_minute=100
                ))
            
            # EXA
            exa_keys = [
                os.getenv('EXA_API_KEY'),
                os.getenv('EXA_API_KEY_1')
            ]
            
            for i, key in enumerate(exa_keys, 1):
                if key and key not in ['your_exa_key_1', None]:
                    self.apis['exa'].append(APIEndpoint(
                        name=f"exa_{i}",
                        api_key=key,
                        base_url="https://api.exa.ai",
                        max_requests_per_minute=100
                    ))
            
            # SerpAPI (usando Serper)
            serper_key = os.getenv('SERPER_API_KEY')
            if serper_key and serper_key not in ['your_serpapi_key_1', None]:
                self.apis['serpapi'].append(APIEndpoint(
                    name="serper_1",
                    api_key=serper_key,
                    base_url="https://google.serper.dev/search",
                    max_requests_per_minute=100
                ))
            
            # YouTube
            youtube_key = os.getenv('YOUTUBE_API_KEY')
            if youtube_key and youtube_key not in ['your_youtube_key_1', None]:
                self.apis['youtube'].append(APIEndpoint(
                    name="youtube_1",
                    api_key=youtube_key,
                    base_url="https://www.googleapis.com/youtube/v3",
                    max_requests_per_minute=100
                ))
            
            # Inicializar índices
            for service in self.apis:
                self.current_api_index[service] = 0
                
            total_apis = sum(len(apis) for apis in self.apis.values())
            logger.info(f"✅ APIs carregadas: {total_apis} endpoints")
            
            # Log detalhado das APIs carregadas
            for service, apis in self.apis.items():
                if apis:
                    logger.info(f"  - {service}: {len(apis)} APIs")
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar configurações de API: {e}")
    
    def _get_base_url(self, service: str) -> str:
        """Retorna URL base para cada serviço"""
        urls = {
            'tavily': 'https://api.tavily.com',
            'exa': 'https://api.exa.ai',
            'serpapi': 'https://serpapi.com/search'
        }
        return urls.get(service, '')
    
    def _initialize_health_monitoring(self):
        """Inicializa monitoramento de saúde das APIs"""
        for service in self.apis:
            self.last_health_check[service] = datetime.now() - timedelta(minutes=10)
    
    def get_active_api(self, service: str, force_check: bool = False) -> Optional[APIEndpoint]:
        """
        Retorna API ativa para o serviço especificado
        """
        with self.lock:
            if service not in self.apis or not self.apis[service]:
                logger.warning(f"⚠️ Nenhuma API disponível para {service}")
                return None
            
            # Health check se necessário
            if force_check or self._needs_health_check(service):
                self._perform_health_check(service)
            
            # Encontrar API ativa
            apis = self.apis[service]
            start_index = self.current_api_index[service]
            
            for i in range(len(apis)):
                index = (start_index + i) % len(apis)
                api = apis[index]
                
                if self._is_api_available(api):
                    self.current_api_index[service] = index
                    api.last_used = datetime.now()
                    api.requests_made += 1
                    logger.info(f"🔄 Usando API {api.name} para {service}")
                    return api
            
            logger.error(f"❌ Nenhuma API disponível para {service}")
            return None
    
    def _needs_health_check(self, service: str) -> bool:
        """Verifica se precisa fazer health check"""
        last_check = self.last_health_check.get(service)
        if not last_check:
            return True
        return datetime.now() - last_check > timedelta(seconds=self.health_check_interval)
    
    def _perform_health_check(self, service: str):
        """Executa health check nas APIs do serviço"""
        try:
            for api in self.apis[service]:
                if api.status == APIStatus.OFFLINE:
                    continue
                
                # Reset rate limit se expirou
                if api.rate_limit_reset and datetime.now() > api.rate_limit_reset:
                    api.status = APIStatus.ACTIVE
                    api.rate_limit_reset = None
                    api.requests_made = 0
                
                # Verificar se está rate limited
                if api.requests_made >= api.max_requests_per_minute:
                    api.status = APIStatus.RATE_LIMITED
                    api.rate_limit_reset = datetime.now() + timedelta(minutes=1)
            
            self.last_health_check[service] = datetime.now()
            
        except Exception as e:
            logger.error(f"❌ Erro no health check de {service}: {e}")
    
    def _is_api_available(self, api: APIEndpoint) -> bool:
        """Verifica se API está disponível para uso"""
        if api.status == APIStatus.OFFLINE:
            return False
        
        if api.status == APIStatus.RATE_LIMITED:
            if api.rate_limit_reset and datetime.now() > api.rate_limit_reset:
                api.status = APIStatus.ACTIVE
                api.requests_made = 0
                return True
            return False
        
        if api.status == APIStatus.ERROR and api.error_count > 5:
            return False
        
        return True
    
    def mark_api_error(self, service: str, api_name: str, error: Exception):
        """Marca API como com erro"""
        with self.lock:
            for api in self.apis[service]:
                if api.name == api_name:
                    api.error_count += 1
                    if api.error_count > 3:
                        api.status = APIStatus.ERROR
                        logger.warning(f"⚠️ API {api_name} marcada como ERROR após {api.error_count} erros")
                    break
    
    def mark_api_rate_limited(self, service: str, api_name: str, reset_time: Optional[datetime] = None):
        """Marca API como rate limited"""
        with self.lock:
            for api in self.apis[service]:
                if api.name == api_name:
                    api.status = APIStatus.RATE_LIMITED
                    api.rate_limit_reset = reset_time or (datetime.now() + timedelta(minutes=1))
                    logger.warning(f"⚠️ API {api_name} rate limited até {api.rate_limit_reset}")
                    break
    
    def get_fallback_model(self, primary_service: str) -> Tuple[str, Optional[APIEndpoint]]:
        """
        Retorna modelo de fallback quando o primário falha
        """
        fallback_order = {
            'qwen': ['gemini', 'groq'],
            'gemini': ['qwen', 'groq'],
            'groq': ['qwen', 'gemini']
        }
        
        for fallback_service in fallback_order.get(primary_service, []):
            api = self.get_active_api(fallback_service)
            if api:
                logger.info(f"🔄 Fallback de {primary_service} para {fallback_service}")
                return fallback_service, api
        
        logger.error(f"❌ Nenhum fallback disponível para {primary_service}")
        return None, None
    
    def get_api_status_report(self) -> Dict[str, Any]:
        """Retorna relatório de status das APIs"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'services': {}
        }
        
        for service, apis in self.apis.items():
            service_status = {
                'total_apis': len(apis),
                'active': 0,
                'rate_limited': 0,
                'error': 0,
                'offline': 0,
                'apis': []
            }
            
            for api in apis:
                service_status[api.status.value] += 1
                service_status['apis'].append({
                    'name': api.name,
                    'status': api.status.value,
                    'error_count': api.error_count,
                    'requests_made': api.requests_made,
                    'last_used': api.last_used.isoformat() if api.last_used else None
                })
            
            report['services'][service] = service_status
        
        return report
    
    def reset_api_errors(self, service: str = None):
        """Reset contadores de erro"""
        services_to_reset = [service] if service else self.apis.keys()
        
        for svc in services_to_reset:
            for api in self.apis[svc]:
                api.error_count = 0
                if api.status == APIStatus.ERROR:
                    api.status = APIStatus.ACTIVE
        
        logger.info(f"✅ Erros resetados para: {', '.join(services_to_reset)}")

# Instância global
api_rotation_manager = EnhancedAPIRotationManager()

def get_api_manager() -> EnhancedAPIRotationManager:
    """Retorna instância do gerenciador de APIs"""
    return api_rotation_manager