#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v4.0 - OpenRouter API Manager
Gerenciador de rotação de APIs do OpenRouter com fallback automático
"""

import os
import logging
import time
import random
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import openai
from openai import OpenAI

logger = logging.getLogger(__name__)

class OpenRouterAPIManager:
    """Gerenciador de rotação de APIs do OpenRouter"""
    
    def __init__(self):
        self.base_url = "https://openrouter.ai/api/v1"
        self.api_keys = self._load_api_keys()
        self.current_key_index = 0
        self.key_usage_stats = {}
        self.key_cooldowns = {}
        self.max_retries = 3
        self.retry_delay = 2
        
        # Inicializa estatísticas para cada chave
        for key in self.api_keys:
            self.key_usage_stats[key] = {
                'requests': 0,
                'errors': 0,
                'last_used': None,
                'credits_exhausted': False,
                'rate_limited': False
            }
        
        logger.info(f"🔄 OpenRouter API Manager inicializado com {len(self.api_keys)} chaves")
    
    def _load_api_keys(self) -> List[str]:
        """Carrega todas as chaves de API disponíveis"""
        keys = []
        
        # Chave principal
        main_key = os.getenv('OPENROUTER_API_KEY')
        if main_key:
            keys.append(main_key)
        
        # Chaves adicionais
        for i in range(1, 10):  # Suporte até 10 chaves
            key = os.getenv(f'OPENROUTER_API_KEY_{i}')
            if key:
                keys.append(key)
        
        if not keys:
            raise ValueError("Nenhuma chave OpenRouter encontrada nas variáveis de ambiente")
        
        return keys
    
    def _get_next_available_key(self) -> str:
        """Obtém a próxima chave disponível na rotação"""
        attempts = 0
        initial_index = self.current_key_index
        
        while attempts < len(self.api_keys):
            key = self.api_keys[self.current_key_index]
            stats = self.key_usage_stats[key]
            
            # Verifica se a chave está em cooldown
            if key in self.key_cooldowns:
                cooldown_until = self.key_cooldowns[key]
                if datetime.now() < cooldown_until:
                    logger.debug(f"Chave {key[:10]}... em cooldown até {cooldown_until}")
                    self._rotate_to_next_key()
                    attempts += 1
                    continue
                else:
                    # Remove do cooldown
                    del self.key_cooldowns[key]
                    stats['credits_exhausted'] = False # Resetar após cooldown
                    stats['rate_limited'] = False # Resetar após cooldown
            
            # Verifica se a chave não está com problemas permanentes (créditos esgotados)
            if not stats['credits_exhausted'] and not stats['rate_limited']:
                return key
            
            # Se chegou aqui, a chave tem problemas, tenta a próxima
            self._rotate_to_next_key()
            attempts += 1
            
            # Se todas as chaves foram verificadas e nenhuma está disponível
            if attempts == len(self.api_keys) and self.current_key_index == initial_index:
                self._notify_all_keys_exhausted()
                # Fallback: tenta usar a chave com menos erros ou a primeira disponível que não esteja em cooldown
                for k in self.api_keys:
                    if k not in self.key_cooldowns and not self.key_usage_stats[k]['credits_exhausted']:
                        logger.warning(f"⚠️ Todas as chaves com problemas, usando a primeira disponível: {k[:10]}...")
                        return k
                # Se realmente todas estão esgotadas ou em cooldown, retorna a primeira para forçar o erro
                logger.error("❌ Todas as chaves OpenRouter estão esgotadas ou em cooldown. Nenhuma chave disponível.")
                raise Exception("Todas as chaves OpenRouter estão esgotadas ou em cooldown.") # Levanta exceção para indicar falha

        # Se todas as chaves têm problemas, usa a com menos erros (caso de fallback extremo)
        best_key = min(self.api_keys, key=lambda k: self.key_usage_stats[k]['errors'])
        logger.warning(f"⚠️ Todas as chaves têm problemas, usando a melhor: {best_key[:10]}...")
        return best_key
    
    def _rotate_to_next_key(self):
        """Rotaciona para a próxima chave"""
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
    
    def _handle_api_error(self, key: str, error: Exception):
        """Trata erros de API e atualiza estatísticas"""
        stats = self.key_usage_stats[key]
        stats['errors'] += 1
        
        error_str = str(error).lower()
        
        # Erro 402 - Créditos insuficientes (cooldown mais longo)
        if '402' in error_str or 'credit' in error_str or 'payment' in error_str:
            stats['credits_exhausted'] = True
            # Cooldown de 1 hora para chaves sem créditos
            self.key_cooldowns[key] = datetime.now() + timedelta(hours=1)
            logger.warning(f"💳 Chave {key[:10]}... sem créditos. Cooldown de 1 hora.")
        
        # Erro 429 - Rate limit
        elif '429' in error_str or 'rate limit' in error_str:
            stats['rate_limited'] = True
            # Cooldown de 5 minutos para rate limit
            self.key_cooldowns[key] = datetime.now() + timedelta(minutes=5)
            logger.warning(f"⏱️ Chave {key[:10]}... em rate limit. Cooldown de 5 minutos.")
        
        # Outros erros - cooldown menor
        else:
            self.key_cooldowns[key] = datetime.now() + timedelta(seconds=30)
            logger.warning(f"⚠️ Erro na chave {key[:10]}...: {error}. Cooldown de 30 segundos.")
    
    def _notify_all_keys_exhausted(self):
        """Notifica quando todas as chaves estão esgotadas ou em cooldown"""
        all_exhausted = True
        for key in self.api_keys:
            stats = self.key_usage_stats[key]
            if not stats['credits_exhausted'] and key not in self.key_cooldowns:
                all_exhausted = False
                break
        
        if all_exhausted:
            logger.critical("🚨 ATENÇÃO: Todas as chaves OpenRouter estão esgotadas ou em cooldown. A análise pode ser comprometida. Por favor, recarregue seus créditos ou adicione novas chaves.")

    def _create_client(self, api_key: str) -> OpenAI:
        """Cria cliente OpenAI com a chave especificada"""
        return OpenAI(
            base_url=self.base_url,
            api_key=api_key
        )
    
    async def chat_completion(self, **kwargs) -> Any:
        """Executa chat completion com rotação automática de chaves"""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                # Obtém chave disponível
                api_key = self._get_next_available_key()
                client = self._create_client(api_key)
                
                # Atualiza estatísticas
                stats = self.key_usage_stats[api_key]
                stats['requests'] += 1
                stats['last_used'] = datetime.now()
                
                logger.debug(f"🔑 Usando chave {api_key[:10]}... (tentativa {attempt + 1})")
                
                # Faz a requisição
                response = client.chat.completions.create(**kwargs)
                
                # Sucesso - rotaciona para próxima chave para distribuir carga
                self._rotate_to_next_key()
                
                return response
                
            except openai.APIStatusError as e:
                last_error = e
                self._handle_api_error(api_key, e)
                if e.status_code == 402: # Erro 402 é fatal para a chave
                    logger.error(f"❌ Erro 402 (Pagamento Requerido) na chave {api_key[:10]}.... Abortando tentativas com esta chave.")
                    raise # Propaga o erro 402 imediatamente
                
                # Se não é o último attempt, aguarda antes de tentar novamente
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt) + random.uniform(0, 1)
                    logger.info(f"⏳ Aguardando {delay:.1f}s antes da próxima tentativa...")
                    time.sleep(delay)
                
                continue
            except Exception as e:
                last_error = e
                self._handle_api_error(api_key, e)
                
                # Se não é o último attempt, aguarda antes de tentar novamente
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt) + random.uniform(0, 1)
                    logger.info(f"⏳ Aguardando {delay:.1f}s antes da próxima tentativa...")
                    time.sleep(delay)
                
                continue
        
        # Se chegou aqui, todas as tentativas falharam
        logger.error(f"❌ Todas as tentativas falharam. Último erro: {last_error}")
        raise last_error
    
    def get_api_status(self) -> Dict[str, Any]:
        """Retorna status das APIs"""
        status = {
            'total_keys': len(self.api_keys),
            'current_key_index': self.current_key_index,
            'keys_status': []
        }
        
        for i, key in enumerate(self.api_keys):
            stats = self.key_usage_stats[key]
            key_status = {
                'index': i,
                'key_preview': f"{key[:10]}...{key[-4:]}",
                'requests': stats['requests'],
                'errors': stats['errors'],
                'last_used': stats['last_used'].isoformat() if stats['last_used'] else None,
                'credits_exhausted': stats['credits_exhausted'],
                'rate_limited': stats['rate_limited'],
                'in_cooldown': key in self.key_cooldowns,
                'available': not stats['credits_exhausted'] and not stats['rate_limited'] and key not in self.key_cooldowns
            }
            
            if key in self.key_cooldowns:
                key_status['cooldown_until'] = self.key_cooldowns[key].isoformat()
            
            status['keys_status'].append(key_status)
        
        # Estatísticas gerais
        total_requests = sum(stats['requests'] for stats in self.key_usage_stats.values())
        total_errors = sum(stats['errors'] for stats in self.key_usage_stats.values())
        available_keys = sum(1 for key_status in status['keys_status'] if key_status['available'])
        
        status['summary'] = {
            'total_requests': total_requests,
            'total_errors': total_errors,
            'error_rate': (total_errors / total_requests * 100) if total_requests > 0 else 0,
            'available_keys': available_keys,
            'health_status': 'healthy' if available_keys > 0 else 'degraded'
        }
        
        return status
    
    def reset_key_status(self, key_index: Optional[int] = None):
        """Reseta status de uma chave específica ou todas"""
        if key_index is not None:
            if 0 <= key_index < len(self.api_keys):
                key = self.api_keys[key_index]
                self.key_usage_stats[key].update({
                    'credits_exhausted': False,
                    'rate_limited': False
                })
                if key in self.key_cooldowns:
                    del self.key_cooldowns[key]
                logger.info(f"✅ Status da chave {key[:10]}... resetado")
            else:
                logger.error(f"❌ Índice de chave inválido: {key_index}")
        else:
            # Reseta todas as chaves
            for key in self.api_keys:
                self.key_usage_stats[key].update({
                    'credits_exhausted': False,
                    'rate_limited': False
                })
            self.key_cooldowns.clear()
            logger.info("✅ Status de todas as chaves resetado")

# Instância global
openrouter_manager = OpenRouterAPIManager()



