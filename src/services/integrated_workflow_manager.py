#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v4.0 - Gerenciador de Workflow Integrado
Integra análise de documentos com workflow principal
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class IntegratedWorkflowManager:
    """Gerenciador que integra análise de documentos com workflow principal"""
    
    def __init__(self):
        self.upload_folder = 'uploads/documents'
        self.data_folder = 'analyses_data'
        
    def integrate_document_insights(self, session_id: str, document_session_id: str) -> Dict:
        """Integra insights dos documentos no workflow principal"""
        try:
            logger.info(f"Integrando insights de documentos para sessão {session_id}")
            
            # Carrega resultados da análise de documentos
            document_results = self._load_document_results(document_session_id)
            
            if not document_results:
                logger.warning(f"Nenhum resultado de documento encontrado para {document_session_id}")
                return {'success': False, 'error': 'Resultados de documentos não encontrados'}
            
            # Extrai insights principais
            key_insights = self._extract_key_insights_for_workflow(document_results)
            
            # Salva insights integrados
            integration_data = {
                'session_id': session_id,
                'document_session_id': document_session_id,
                'integrated_at': datetime.now().isoformat(),
                'document_insights': key_insights,
                'integration_summary': self._create_integration_summary(key_insights)
            }
            
            self._save_integration_data(session_id, integration_data)
            
            return {
                'success': True,
                'insights_integrated': len(key_insights.get('insights', [])),
                'recommendations_count': len(key_insights.get('recommendations', [])),
                'integration_summary': integration_data['integration_summary']
            }
            
        except Exception as e:
            logger.error(f"Erro na integração de insights: {e}")
            return {'success': False, 'error': str(e)}
    
    def enhance_market_analysis_with_documents(self, market_data: Dict, document_session_id: str) -> Dict:
        """Enriquece análise de mercado com insights dos documentos"""
        try:
            document_results = self._load_document_results(document_session_id)
            
            if not document_results:
                return market_data
            
            # Extrai insights relevantes para mercado
            market_insights = self._extract_market_relevant_insights(document_results)
            
            # Enriquece dados de mercado
            enhanced_data = market_data.copy()
            enhanced_data['document_enhanced'] = True
            enhanced_data['document_insights'] = market_insights
            enhanced_data['enhanced_segments'] = self._enhance_segments_with_documents(
                market_data.get('segments', {}), market_insights
            )
            enhanced_data['enhanced_opportunities'] = self._enhance_opportunities_with_documents(
                market_data.get('opportunities', []), market_insights
            )
            
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Erro ao enriquecer análise de mercado: {e}")
            return market_data
    
    def generate_integrated_recommendations(self, session_id: str) -> Dict:
        """Gera recomendações integradas baseadas em documentos e mercado"""
        try:
            # Carrega dados de integração
            integration_data = self._load_integration_data(session_id)
            
            if not integration_data:
                return {'recommendations': [], 'confidence': 0.0}
            
            document_insights = integration_data.get('document_insights', {})
            
            # Gera recomendações integradas
            integrated_recommendations = []
            
            # Recomendações baseadas em insights de documentos
            for insight in document_insights.get('insights', []):
                recommendation = self._convert_insight_to_recommendation(insight)
                if recommendation:
                    integrated_recommendations.append(recommendation)
            
            # Recomendações baseadas em correlações
            for correlation in document_insights.get('correlations', []):
                recommendation = self._convert_correlation_to_recommendation(correlation)
                if recommendation:
                    integrated_recommendations.append(recommendation)
            
            # Recomendações baseadas em oportunidades identificadas
            for opportunity in document_insights.get('opportunities', []):
                recommendation = self._convert_opportunity_to_recommendation(opportunity)
                if recommendation:
                    integrated_recommendations.append(recommendation)
            
            # Calcula score de confiança
            confidence_score = self._calculate_recommendation_confidence(
                integrated_recommendations, document_insights
            )
            
            return {
                'recommendations': integrated_recommendations[:10],  # Top 10
                'confidence': confidence_score,
                'source': 'integrated_document_analysis',
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro ao gerar recomendações integradas: {e}")
            return {'recommendations': [], 'confidence': 0.0}
    
    def create_document_enhanced_modules(self, base_modules: List[Dict], document_session_id: str) -> List[Dict]:
        """Cria módulos enriquecidos com insights dos documentos"""
        try:
            document_results = self._load_document_results(document_session_id)
            
            if not document_results:
                return base_modules
            
            enhanced_modules = []
            
            for module in base_modules:
                enhanced_module = module.copy()
                
                # Adiciona seção de insights de documentos
                if module.get('type') in ['market_analysis', 'competitor_analysis', 'opportunity_analysis']:
                    enhanced_module['document_insights'] = self._get_relevant_document_insights(
                        document_results, module.get('type')
                    )
                    enhanced_module['enhanced'] = True
                
                enhanced_modules.append(enhanced_module)
            
            # Adiciona módulo específico de análise de documentos
            document_module = self._create_document_analysis_module(document_results)
            enhanced_modules.insert(0, document_module)  # Adiciona no início
            
            return enhanced_modules
            
        except Exception as e:
            logger.error(f"Erro ao criar módulos enriquecidos: {e}")
            return base_modules
    
    def _load_document_results(self, document_session_id: str) -> Optional[Dict]:
        """Carrega resultados da análise de documentos"""
        try:
            results_path = os.path.join(self.upload_folder, document_session_id, 'analysis_results.json')
            
            if not os.path.exists(results_path):
                return None
            
            with open(results_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            logger.error(f"Erro ao carregar resultados de documentos: {e}")
            return None
    
    def _extract_key_insights_for_workflow(self, document_results: Dict) -> Dict:
        """Extrai insights principais para integração no workflow"""
        insights = document_results.get('insights', {})
        synthesis = document_results.get('synthesis', {})
        
        return {
            'insights': insights.get('key_insights', [])[:5],
            'recommendations': insights.get('recommendations', [])[:5],
            'opportunities': insights.get('opportunities', [])[:3],
            'risks': insights.get('risks', [])[:3],
            'correlations': synthesis.get('correlations', [])[:3],
            'patterns': synthesis.get('patterns', [])[:3],
            'predictions': synthesis.get('predictions', [])[:3],
            'confidence_score': document_results.get('analysis_summary', {}).get('analysis_quality_score', 0.5)
        }
    
    def _extract_market_relevant_insights(self, document_results: Dict) -> Dict:
        """Extrai insights relevantes para análise de mercado"""
        all_insights = self._extract_key_insights_for_workflow(document_results)
        
        # Filtra insights relevantes para mercado
        market_keywords = [
            'mercado', 'cliente', 'concorrente', 'preço', 'demanda', 'oferta',
            'segmento', 'público', 'target', 'consumidor', 'vendas', 'receita'
        ]
        
        market_insights = {}
        
        for key, items in all_insights.items():
            if isinstance(items, list):
                market_items = []
                for item in items:
                    if any(keyword in item.lower() for keyword in market_keywords):
                        market_items.append(item)
                market_insights[key] = market_items
            else:
                market_insights[key] = items
        
        return market_insights
    
    def _enhance_segments_with_documents(self, segments: Dict, document_insights: Dict) -> Dict:
        """Enriquece segmentos de mercado com insights dos documentos"""
        enhanced_segments = segments.copy()
        
        # Adiciona insights de documentos aos segmentos
        for segment_name, segment_data in enhanced_segments.items():
            segment_data['document_insights'] = []
            
            # Busca insights relevantes para o segmento
            for insight in document_insights.get('insights', []):
                if any(keyword in insight.lower() for keyword in [segment_name.lower(), 'segmento', 'público']):
                    segment_data['document_insights'].append(insight)
        
        return enhanced_segments
    
    def _enhance_opportunities_with_documents(self, opportunities: List, document_insights: Dict) -> List:
        """Enriquece oportunidades com insights dos documentos"""
        enhanced_opportunities = opportunities.copy()
        
        # Adiciona oportunidades identificadas nos documentos
        for doc_opportunity in document_insights.get('opportunities', []):
            enhanced_opportunities.append({
                'title': 'Oportunidade Identificada em Documentos',
                'description': doc_opportunity,
                'source': 'document_analysis',
                'confidence': document_insights.get('confidence_score', 0.5)
            })
        
        return enhanced_opportunities
    
    def _convert_insight_to_recommendation(self, insight: str) -> Optional[Dict]:
        """Converte insight em recomendação acionável"""
        if len(insight.strip()) < 20:  # Muito curto
            return None
        
        return {
            'title': 'Recomendação baseada em Insight de Documento',
            'description': insight,
            'priority': 'medium',
            'category': 'document_insight',
            'actionable': True
        }
    
    def _convert_correlation_to_recommendation(self, correlation: str) -> Optional[Dict]:
        """Converte correlação em recomendação"""
        if len(correlation.strip()) < 20:
            return None
        
        return {
            'title': 'Aproveitar Correlação Identificada',
            'description': f"Explorar a correlação: {correlation}",
            'priority': 'high',
            'category': 'correlation',
            'actionable': True
        }
    
    def _convert_opportunity_to_recommendation(self, opportunity: str) -> Optional[Dict]:
        """Converte oportunidade em recomendação"""
        if len(opportunity.strip()) < 20:
            return None
        
        return {
            'title': 'Explorar Oportunidade Identificada',
            'description': opportunity,
            'priority': 'high',
            'category': 'opportunity',
            'actionable': True
        }
    
    def _calculate_recommendation_confidence(self, recommendations: List[Dict], insights: Dict) -> float:
        """Calcula score de confiança das recomendações"""
        base_confidence = insights.get('confidence_score', 0.5)
        
        # Ajusta baseado na quantidade de recomendações
        quantity_factor = min(len(recommendations) / 10, 1.0)
        
        # Ajusta baseado na diversidade de categorias
        categories = set(rec.get('category', 'unknown') for rec in recommendations)
        diversity_factor = min(len(categories) / 4, 1.0)
        
        return (base_confidence + quantity_factor + diversity_factor) / 3
    
    def _get_relevant_document_insights(self, document_results: Dict, module_type: str) -> List[str]:
        """Obtém insights relevantes para tipo específico de módulo"""
        all_insights = document_results.get('insights', {}).get('key_insights', [])
        
        # Palavras-chave por tipo de módulo
        keywords_map = {
            'market_analysis': ['mercado', 'demanda', 'oferta', 'tamanho', 'crescimento'],
            'competitor_analysis': ['concorrente', 'competição', 'rival', 'benchmark'],
            'opportunity_analysis': ['oportunidade', 'potencial', 'chance', 'nicho']
        }
        
        keywords = keywords_map.get(module_type, [])
        relevant_insights = []
        
        for insight in all_insights:
            if any(keyword in insight.lower() for keyword in keywords):
                relevant_insights.append(insight)
        
        return relevant_insights[:3]  # Top 3 mais relevantes
    
    def _create_document_analysis_module(self, document_results: Dict) -> Dict:
        """Cria módulo específico de análise de documentos"""
        summary = document_results.get('analysis_summary', {})
        insights = document_results.get('insights', {})
        
        return {
            'id': 'document_analysis',
            'title': 'Análise de Documentos com IA',
            'type': 'document_analysis',
            'content': {
                'summary': f"Análise de {summary.get('total_documents', 0)} documentos com IA",
                'key_insights': insights.get('key_insights', [])[:5],
                'recommendations': insights.get('recommendations', [])[:5],
                'quality_score': summary.get('analysis_quality_score', 0.0),
                'document_types': summary.get('document_types', [])
            },
            'enhanced': True,
            'source': 'document_ai_analysis',
            'generated_at': datetime.now().isoformat()
        }
    
    def _create_integration_summary(self, key_insights: Dict) -> Dict:
        """Cria resumo da integração"""
        return {
            'total_insights': len(key_insights.get('insights', [])),
            'total_recommendations': len(key_insights.get('recommendations', [])),
            'opportunities_identified': len(key_insights.get('opportunities', [])),
            'risks_identified': len(key_insights.get('risks', [])),
            'correlations_found': len(key_insights.get('correlations', [])),
            'confidence_level': key_insights.get('confidence_score', 0.5),
            'integration_quality': 'high' if key_insights.get('confidence_score', 0) > 0.7 else 'medium'
        }
    
    def _save_integration_data(self, session_id: str, integration_data: Dict):
        """Salva dados de integração"""
        try:
            session_dir = os.path.join(self.data_folder, session_id)
            os.makedirs(session_dir, exist_ok=True)
            
            integration_path = os.path.join(session_dir, 'document_integration.json')
            
            with open(integration_path, 'w', encoding='utf-8') as f:
                json.dump(integration_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Erro ao salvar dados de integração: {e}")
    
    def _load_integration_data(self, session_id: str) -> Optional[Dict]:
        """Carrega dados de integração"""
        try:
            integration_path = os.path.join(self.data_folder, session_id, 'document_integration.json')
            
            if not os.path.exists(integration_path):
                return None
            
            with open(integration_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            logger.error(f"Erro ao carregar dados de integração: {e}")
            return None

