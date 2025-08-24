#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - TrendFinder MCP Client
Cliente para integração com TrendFinder MCP
"""

import os
import logging
import httpx
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class TrendFinderClient:
    """Cliente para TrendFinder MCP"""

    def __init__(self):
        """Inicializa o cliente TrendFinder"""
        self.mcp_url = os.getenv('TRENDFINDER_MCP_URL')
        self.base_url = self.mcp_url # Alias for compatibility with _check_connectivity
        self.timeout = 60

        if not self.mcp_url:
            logger.warning("⚠️ TRENDFINDER_MCP_URL não configurado")
        else:
            logger.info(f"🔍 TrendFinder Client inicializado: {self.mcp_url}")

    def _check_connectivity(self) -> bool:
        """Verifica se o serviço está acessível"""
        try:
            import requests
            response = requests.get(self.base_url, timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    async def search_trends(self, query: str) -> Dict[str, Any]:
        """Busca tendências para a query especificada"""
        logger.info(f"🔍 Buscando tendências para: {query}")

        # Verifica conectividade primeiro
        if not self._check_connectivity():
            logger.warning("⚠️ TrendFinder não acessível, usando dados simulados")
            return self._generate_fallback_trends(query)

        try:
            # Payload para o MCP
            payload = {
                'method': 'search_trends',
                'params': {
                    'query': query,
                    'platforms': ['twitter', 'instagram', 'tiktok', 'youtube'],
                    'limit': 50,
                    'time_range': '7d'  # últimos 7 dias
                }
            }

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.mcp_url,
                    json=payload,
                    headers={
                        'Content-Type': 'application/json',
                        'User-Agent': 'ARQV30-TrendFinder/1.0'
                    }
                )

                if response.status_code == 200:
                    data = response.json()

                    # Processa os resultados
                    trends_data = {
                        'success': True,
                        'source': 'TrendFinder',
                        'query': query,
                        'timestamp': datetime.now().isoformat(),
                        'platforms_searched': ['twitter', 'instagram', 'tiktok', 'youtube'],
                        'trends': data.get('result', {}).get('trends', []),
                        'hashtags': data.get('result', {}).get('hashtags', []),
                        'viral_content': data.get('result', {}).get('viral_content', []),
                        'influencers': data.get('result', {}).get('influencers', []),
                        'sentiment': data.get('result', {}).get('sentiment', {}),
                        'total_mentions': data.get('result', {}).get('total_mentions', 0),
                        'engagement_metrics': data.get('result', {}).get('engagement_metrics', {})
                    }

                    logger.info(f"✅ TrendFinder: {len(trends_data['trends'])} tendências encontradas")
                    return trends_data

                else:
                    error_msg = f"Erro HTTP {response.status_code}: {response.text}"
                    logger.error(f"❌ TrendFinder erro: {error_msg}")
                    return self._generate_fallback_trends(query)

        except httpx.TimeoutException:
            error_msg = f"Timeout após {self.timeout}s"
            logger.error(f"❌ TrendFinder timeout: {error_msg}")
            return self._generate_fallback_trends(query)

        except Exception as e:
            logger.error(f"❌ TrendFinder erro: {e}")
            return self._generate_fallback_trends(query)

    def _generate_fallback_trends(self, query: str) -> Dict[str, Any]:
        """Gera dados de tendências simulados quando o serviço não está disponível"""

        # Palavras-chave relacionadas ao MASI e empreendedorismo digital
        fallback_trends = [
            {
                'keyword': 'empreendedorismo digital',
                'trend_score': 85,
                'volume': 15000,
                'growth': '+25%',
                'related_terms': ['marketing digital', 'negócio online', 'renda extra']
            },
            {
                'keyword': 'gestão de PME',
                'trend_score': 78,
                'volume': 8500,
                'growth': '+18%',
                'related_terms': ['pequenas empresas', 'gestão empresarial', 'produtividade']
            },
            {
                'keyword': 'consultoria de negócios',
                'trend_score': 72,
                'volume': 6200,
                'growth': '+15%',
                'related_terms': ['consultoria empresarial', 'estratégia de negócios', 'mentoria']
            }
        ]

        return {
            'success': True,
            'source': 'fallback_data',
            'query': query,
            'trends': fallback_trends,
            'total_trends': len(fallback_trends),
            'timestamp': datetime.now().isoformat(),
            'note': 'Dados simulados - TrendFinder não disponível'
        }

    async def search_platform_specific(self, query: str, platform: str) -> Dict[str, Any]:
        """
        Busca específica para uma plataforma

        Args:
            query: Termo de busca
            platform: Plataforma específica ('twitter', 'instagram', etc.)
        """
        return await self.search_trends(query, [platform]) # Modified to call search_trends

    async def get_trending_hashtags(self, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtém hashtags em tendência

        Args:
            category: Categoria específica (opcional)
        """
        if not self.mcp_url:
            return {
                'success': False,
                'error': 'TRENDFINDER_MCP_URL não configurado',
                'source': 'TrendFinder'
            }

        try:
            payload = {
                'method': 'get_trending_hashtags',
                'params': {
                    'category': category,
                    'limit': 100,
                    'time_range': '24h'
                }
            }

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.mcp_url,
                    json=payload,
                    headers={'Content-Type': 'application/json'}
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        'success': True,
                        'source': 'TrendFinder',
                        'hashtags': data.get('result', {}).get('hashtags', []),
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    # Use fallback if service is unavailable
                    logger.error(f"❌ TrendFinder erro ao buscar hashtags: HTTP {response.status_code}")
                    return self._generate_fallback_trends_hashtags(category)

        except Exception as e:
            logger.error(f"❌ TrendFinder erro inesperado ao buscar hashtags: {e}")
            return self._generate_fallback_trends_hashtags(category)

    def _generate_fallback_trends_hashtags(self, category: Optional[str] = None) -> Dict[str, Any]:
        """Gera dados de hashtags simulados quando o serviço não está disponível"""
        fallback_hashtags = [
            {'hashtag': '#empreendedorismo', 'count': 12000},
            {'hashtag': '#marketingdigital', 'count': 9500},
            {'hashtag': '#negociosonline', 'count': 7800}
        ]
        if category:
            # Filter hashtags if a category is provided (simple example)
            filtered_hashtags = [ht for ht in fallback_hashtags if category.lower() in ht['hashtag'].lower()]
            return {
                'success': True,
                'source': 'fallback_data',
                'hashtags': filtered_hashtags,
                'timestamp': datetime.now().isoformat(),
                'note': f'Dados simulados para categoria {category} - TrendFinder não disponível'
            }
        else:
            return {
                'success': True,
                'source': 'fallback_data',
                'hashtags': fallback_hashtags,
                'timestamp': datetime.now().isoformat(),
                'note': 'Dados simulados - TrendFinder não disponível'
            }

    def is_available(self) -> bool:
        """Verifica se o serviço está disponível"""
        return bool(self.mcp_url) and self._check_connectivity()

# Instância global
trendfinder_client = TrendFinderClient()