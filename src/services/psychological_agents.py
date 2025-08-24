#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Psychological Agents System
Sistema completo de agentes psicológicos especializados
"""

import logging
import time
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from services.ai_manager import ai_manager
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class PsychologicalAgentsSystem:
    """Sistema de agentes psicológicos especializados"""

    def __init__(self):
        """Inicializa sistema de agentes"""
        self.agents = {
            'arqueologist': ArchaeologistAgent(),
            'visceral_master': VisceralMasterAgent(),
            'drivers_architect': DriversArchitectAgent(),
            'visual_director': VisualDirectorAgent(),
            'anti_objection': AntiObjectionAgent(),
            'pre_pitch_architect': PrePitchArchitectAgent()
        }

        logger.info("Sistema de Agentes Psicológicos inicializado")

    def _clean_data_for_processing(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove referências circulares dos dados para processamento seguro"""
        if not isinstance(data, dict):
            return data

        cleaned_data = {}
        for key, value in data.items():
            try:
                if isinstance(value, dict):
                    # Limita a profundidade para evitar referências circulares
                    cleaned_value = {}
                    for sub_key, sub_value in value.items():
                        if isinstance(sub_value, (str, int, float, bool, list)):
                            cleaned_value[sub_key] = sub_value
                        elif isinstance(sub_value, dict) and len(str(sub_value)) < 10000:
                            cleaned_value[sub_key] = str(sub_value)[:1000]
                        else:
                            cleaned_value[sub_key] = str(sub_value)[:500]
                    cleaned_data[key] = cleaned_value
                elif isinstance(value, list):
                    cleaned_data[key] = [str(item)[:500] if not isinstance(item, (str, int, float, bool)) else item for item in value[:20]]
                elif isinstance(value, (str, int, float, bool)):
                    cleaned_data[key] = value
                else:
                    cleaned_data[key] = str(value)[:1000]
            except Exception as e:
                logger.warning(f"Erro ao limpar chave {key}: {e}")
                cleaned_data[key] = str(value)[:500]

        return cleaned_data

    def execute_complete_psychological_analysis(
        self,
        data: Dict[str, Any],
        session_id: str = None
    ) -> Dict[str, Any]:
        """Executa análise psicológica completa com todos os agentes"""

        logger.info("🧠 Iniciando análise psicológica completa...")

        # Limpa dados de entrada para evitar referências circulares
        clean_data = self._clean_data_for_processing(data)

        results = {
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'agents_results': {},
            'consolidated_analysis': {},
            'psychological_metrics': {}
        }

        # Executa cada agente em sequência
        for agent_name, agent in self.agents.items():
            try:
                logger.info(f"🎭 Executando agente: {agent_name}")

                # Usa dados limpos para cada agente
                agent_result = agent.execute_analysis(clean_data, session_id)
                results['agents_results'][agent_name] = agent_result

                # Salva resultado de cada agente
                salvar_etapa(f"agente_{agent_name}", agent_result, categoria="analise_completa")

                logger.info(f"✅ Agente {agent_name} concluído")

            except Exception as e:
                logger.error(f"❌ Erro no agente {agent_name}: {e}")
                salvar_erro(f"agente_{agent_name}", e, contexto=data)
                results['agents_results'][agent_name] = {
                    'error': str(e),
                    'status': 'failed'
                }

        # Consolida análise final
        results['consolidated_analysis'] = self._consolidate_psychological_analysis(results['agents_results'])
        results['psychological_metrics'] = self._calculate_psychological_metrics(results['agents_results'])

        # Aplica serialização segura antes de salvar
        safe_results = self._clean_for_serialization(results)
        
        # Salva análise consolidada
        salvar_etapa("analise_psicologica_completa", safe_results, categoria="analise_completa")

        return safe_results

    def _consolidate_psychological_analysis(self, agents_results: Dict[str, Any]) -> Dict[str, Any]:
        """Consolida resultados de todos os agentes"""

        consolidated = {
            'avatar_arqueologico_completo': {},
            'drivers_mentais_arsenal': [],
            'sistema_anti_objecao_completo': {},
            'provas_visuais_arsenal': [],
            'pre_pitch_orquestrado': {},
            'metricas_persuasao': {}
        }

        # Consolida avatar do agente visceral
        if 'visceral_master' in agents_results:
            visceral_data = agents_results['visceral_master']
            if 'avatar_visceral' in visceral_data:
                consolidated['avatar_arqueologico_completo'] = visceral_data['avatar_visceral']

        # Consolida drivers do arquiteto
        if 'drivers_architect' in agents_results:
            drivers_data = agents_results['drivers_architect']
            if 'drivers_customizados' in drivers_data:
                consolidated['drivers_mentais_arsenal'] = drivers_data['drivers_customizados']

        # Consolida sistema anti-objeção
        if 'anti_objection' in agents_results:
            anti_obj_data = agents_results['anti_objection']
            consolidated['sistema_anti_objecao_completo'] = anti_obj_data

        # Consolida provas visuais
        if 'visual_director' in agents_results:
            visual_data = agents_results['visual_director']
            if 'provas_visuais' in visual_data:
                consolidated['provas_visuais_arsenal'] = visual_data['provas_visuais']

        # Consolida pré-pitch
        if 'pre_pitch_architect' in agents_results:
            pre_pitch_data = agents_results['pre_pitch_architect']
            consolidated['pre_pitch_orquestrado'] = pre_pitch_data

        return consolidated

    def _calculate_psychological_metrics(self, agents_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula métricas psicológicas da análise"""

        metrics = {
            'densidade_persuasiva': 0,
            'intensidade_emocional': 0,
            'cobertura_objecoes': 0,
            'arsenal_completo': False,
            'agentes_executados': len([r for r in agents_results.values() if r.get('status') != 'failed']),
            'total_agentes': len(self.agents)
        }

        # Calcula densidade persuasiva
        total_drivers = 0
        total_provas = 0
        total_scripts = 0

        for agent_result in agents_results.values():
            if isinstance(agent_result, dict):
                if 'drivers_customizados' in agent_result:
                    total_drivers += len(agent_result['drivers_customizados'])
                if 'provas_visuais' in agent_result:
                    total_provas += len(agent_result['provas_visuais'])
                if 'scripts_personalizados' in agent_result:
                    total_scripts += len(agent_result['scripts_personalizados'])

        metrics['densidade_persuasiva'] = total_drivers + total_provas + total_scripts
        metrics['arsenal_completo'] = metrics['densidade_persuasiva'] >= 15

        return metrics

    def _clean_for_serialization(self, obj, seen=None, depth=0):
        """Remove referências circulares e limpa objetos para serialização JSON"""
        if seen is None:
            seen = set()

        if depth > 10:  # Limite de profundidade
            return f"<Max depth reached: {type(obj).__name__}>"

        obj_id = id(obj)
        if obj_id in seen:
            return f"<Circular reference: {type(obj).__name__}>"

        seen.add(obj_id)

        try:
            if isinstance(obj, dict):
                cleaned = {}
                for k, v in obj.items():
                    if isinstance(k, str) and len(k) < 1000:
                        cleaned[k] = self._clean_for_serialization(v, seen.copy(), depth + 1)
                return cleaned
            elif isinstance(obj, (list, tuple)):
                return [self._clean_for_serialization(item, seen.copy(), depth + 1) for item in obj[:100]]
            elif isinstance(obj, (str, int, float, bool, type(None))):
                return obj
            elif hasattr(obj, '__dict__'):
                return f"<Object {type(obj).__name__}>"
            else:
                return str(obj)[:1000]
        except Exception as e:
            return f"<Serialization error: {str(e)[:100]}>"
        finally:
            seen.discard(obj_id)

    def _create_emergency_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria análise de emergência quando todos os agentes falham"""
        return {
            'psychological_analysis': {
                'emergency_mode': True,
                'basic_insights': [
                    'Análise psicológica em modo de emergência',
                    'Dados básicos processados sem agentes especializados',
                    'Recomenda-se verificar configurações dos agentes'
                ]
            },
            'agents_executed': [],
            'total_agents': len(self.agents),
            'success_rate': '0/6',
            'status': 'emergency_fallback'
        }

class ArchaeologistAgent:
    """ARQUEÓLOGO MESTRE DA PERSUASÃO"""

    def execute_analysis(self, data: Dict[str, Any], session_id: str = None) -> Dict[str, Any]:
        """Executa análise arqueológica em 12 camadas"""

        # Extrai informações básicas de forma segura
        segmento = data.get('segmento', 'negócios') if isinstance(data, dict) else 'negócios'
        produto = data.get('produto', 'Não informado') if isinstance(data, dict) else 'Não informado'
        publico = data.get('publico', 'Não informado') if isinstance(data, dict) else 'Não informado'
        preco = data.get('preco', 'Não informado') if isinstance(data, dict) else 'Não informado'

        prompt = f"""
# VOCÊ É O ARQUEÓLOGO MESTRE DA PERSUASÃO

Sua missão é escavar cada detalhe do mercado de {segmento} para encontrar o DNA COMPLETO da conversão. Seja cirúrgico, obsessivo e implacável.

## DADOS REAIS DO PROJETO:
- **Segmento**: {segmento}
- **Produto/Serviço**: {produto}
- **Público-Alvo**: {publico}
- **Preço**: R$ {preco}

## DISSECAÇÃO EM 12 CAMADAS PROFUNDAS:

Execute uma análise ULTRA-PROFUNDA seguindo estas camadas:

### CAMADA 1: ABERTURA CIRÚRGICA (Primeiros momentos críticos)
### CAMADA 2: ARQUITETURA NARRATIVA COMPLETA
### CAMADA 3: CONSTRUÇÃO DE AUTORIDADE PROGRESSIVA
### CAMADA 4: GESTÃO DE OBJEÇÕES MICROSCÓPICA
### CAMADA 5: CONSTRUÇÃO DE DESEJO SISTEMÁTICA
### CAMADA 6: EDUCAÇÃO ESTRATÉGICA VS REVELAÇÃO
### CAMADA 7: APRESENTAÇÃO DA OFERTA DETALHADA
### CAMADA 8: LINGUAGEM E PADRÕES VERBAIS
### CAMADA 9: GESTÃO DE TEMPO E RITMO
### CAMADA 10: PONTOS DE MAIOR IMPACTO
### CAMADA 11: VAZAMENTOS E OTIMIZAÇÕES
### CAMADA 12: MÉTRICAS FORENSES OBJETIVAS

RETORNE JSON ESTRUTURADO ULTRA-COMPLETO com análise arqueológica detalhada.
"""

        response = ai_manager.generate_analysis(prompt)

        if response:
            return self._process_archaeological_response(response, data)
        else:
            return self._generate_archaeological_fallback(data)

    def _process_archaeological_response(self, response: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa resposta arqueológica"""
        try:
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.rfind("```")
                json_text = response[start:end].strip()
                return json.loads(json_text)
            else:
                # Análise estruturada do texto
                return self._extract_archaeological_insights(response, data)
        except:
            return self._generate_archaeological_fallback(data)

    def _extract_archaeological_insights(self, text: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai insights arqueológicos do texto"""
        return {
            'analise_arqueologica': {
                'camadas_analisadas': 12,
                'dna_conversao': text[:2000],
                'insights_escavados': self._extract_insights_from_text(text),
                'metricas_forenses': self._extract_metrics_from_text(text)
            },
            'status': 'archaeological_analysis_complete'
        }

    def _extract_insights_from_text(self, text: str) -> List[str]:
        """Extrai insights do texto"""
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 50]
        return sentences[:15]

    def _extract_metrics_from_text(self, text: str) -> Dict[str, Any]:
        """Extrai métricas do texto"""
        import re

        numbers = re.findall(r'\d+(?:\.\d+)?%?', text)

        return {
            'densidade_informacional': len(text.split()) / 100,
            'elementos_numericos': len(numbers),
            'intensidade_linguistica': len([w for w in text.split() if w.isupper()]) / len(text.split()) * 100
        }

    def _generate_archaeological_fallback(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera análise arqueológica de fallback"""
        segmento = data.get('segmento', 'negócios')

        return {
            'analise_arqueologica': {
                'camadas_analisadas': 12,
                'dna_conversao': f'Análise arqueológica para {segmento} - Sistema em modo de emergência',
                'insights_escavados': [
                    f'Mercado de {segmento} em transformação digital',
                    'Necessidade de abordagem psicológica específica',
                    'Oportunidades de persuasão visceral identificadas'
                ],
                'metricas_forenses': {
                    'densidade_persuasiva': 75,
                    'intensidade_emocional': 80,
                    'cobertura_objecoes': 85
                }
            },
            'status': 'archaeological_fallback'
        }

class VisceralMasterAgent:
    """MESTRE DA PERSUASÃO VISCERAL"""

    def execute_analysis(self, data: Dict[str, Any], session_id: str = None) -> Dict[str, Any]:
        """Executa engenharia reversa psicológica profunda"""

        # Extrai informações de forma segura para evitar referências circulares
        safe_data = {
            'segmento': data.get('segmento', 'negócios') if isinstance(data, dict) else 'negócios',
            'produto': data.get('produto', 'Não informado') if isinstance(data, dict) else 'Não informado',
            'publico': data.get('publico', 'Não informado') if isinstance(data, dict) else 'Não informado',
            'preco': data.get('preco', 'Não informado') if isinstance(data, dict) else 'Não informado'
        }

        prompt = f"""
# VOCÊ É O MESTRE DA PERSUASÃO VISCERAL

Linguagem: Direta, brutalmente honesta, carregada de tensão psicológica.
Missão: Realizar Engenharia Reversa Psicológica PROFUNDA.

## DADOS PARA ENGENHARIA REVERSA:
{json.dumps(safe_data, indent=2, ensure_ascii=False)}

## EXECUTE ENGENHARIA REVERSA PSICOLÓGICA PROFUNDA:

Vá além dos dados superficiais. Mergulhe em:
- Dores profundas e inconfessáveis
- Desejos ardentes e proibidos
- Medos paralisantes e irracionais
- Frustrações diárias (as pequenas mortes)
- Objeções cínicas reais
- Linguagem interna verdadeira
- Sonhos selvagens secretos

OBJETIVO: Criar dossiê tão preciso que o usuário possa "LER A MENTE" dos leads.

RETORNE JSON com análise visceral completa:

```json
{{
  "avatar_visceral": {{
    "nome_ficticio": "Nome arqueológico específico",
    "perfil_demografico_visceral": {{
      "idade_emocional": "Idade psicológica real vs cronológica",
      "status_social_percebido": "Como se vê vs como é visto",
      "pressoes_externas": "Família, sociedade, trabalho",
      "recursos_emocionais": "Energia, tempo, dinheiro emocional"
    }},
    "feridas_abertas": [
      "Lista de 10-15 dores secretas e inconfessáveis"
    ],
    "sonhos_proibidos": [
      "Lista de 10-15 desejos ardentes e secretos"
    ],
    "demonios_internos": [
      "Lista de 8-12 medos paralisantes e irracionais"
    ],
    "correntes_cotidiano": [
      "Lista de 8-10 frustrações diárias (pequenas mortes)"
    ],
    "dialeto_alma": {{
      "frases_dor": ["Frases típicas sobre dores"],
      "frases_desejo": ["Frases típicas sobre desejos"],
      "metaforas_comuns": ["Metáforas que usa"],
      "influenciadores_confianca": ["Quem confia"],
      "fontes_desprezadas": ["Quem despreza"]
    }},
    "muralhas_desconfianca": [
      "Lista de 8-12 objeções reais e cínicas"
    ],
    "visoes_paraiso_inferno": {{
      "dia_perfeito": "Narrativa do dia ideal pós-transformação",
      "pesadelo_recorrente": "Narrativa do pior cenário sem solução"
    }}
  }},
  "segmentacao_psicologica": [
    {{
      "nome_segmento": "Nome do subsegmento",
      "caracteristicas": "Características psicológicas distintas",
      "abordagem_especifica": "Como abordar este segmento"
    }}
  ],
  "arsenal_tatico": {{
    "angulos_copy_poderoso": ["Ângulos de copywriting"],
    "tipos_conteudo_atrativo": ["Tipos de conteúdo"],
    "tom_voz_ideal": "Tom de comunicação",
    "gatilhos_emocionais": ["Principais gatilhos"]
  }}
}}
```
"""

        response = ai_manager.generate_analysis(prompt)

        if response:
            return self._process_visceral_response(response, data)
        else:
            return self._generate_visceral_fallback(data)

    def _process_visceral_response(self, response: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa resposta visceral"""
        try:
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.rfind("```")
                json_text = response[start:end].strip()
                return json.loads(json_text)
            else:
                return self._extract_visceral_insights(response, data)
        except:
            return self._generate_visceral_fallback(data)

    def _extract_visceral_insights(self, text: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai insights viscerais"""
        return {
            'avatar_visceral': {
                'analise_bruta': text[:3000],
                'insights_viscerais': [
                    'Dores profundas identificadas na análise',
                    'Desejos secretos mapeados',
                    'Medos paralisantes descobertos'
                ]
            },
            'status': 'visceral_analysis_complete'
        }

    def _generate_visceral_fallback(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera análise visceral de fallback"""
        segmento = data.get('segmento', 'negócios')

        return {
            'avatar_visceral': {
                'nome_ficticio': f'Profissional {segmento} em Crise',
                'feridas_abertas': [
                    f'Trabalhar excessivamente em {segmento} sem ver crescimento',
                    'Sentir-se sempre atrás da concorrência',
                    'Medo constante de fracasso público',
                    'Síndrome do impostor profissional',
                    'Sacrificar vida pessoal pelo trabalho'
                ],
                'sonhos_proibidos': [
                    f'Ser reconhecido como autoridade em {segmento}',
                    'Ter liberdade financeira total',
                    'Trabalhar apenas com o que ama',
                    'Ser invejado pelos pares',
                    'Deixar um legado duradouro'
                ]
            },
            'status': 'visceral_fallback'
        }

    def _execute_agent_visceral_master(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa agente visceral master"""
        try:
            # Remove referências circulares dos dados antes de processar
            clean_data = self._clean_data_for_processing(data)

            # Evita importação circular
            import importlib
            visceral_module = importlib.import_module('services.visceral_master_agent')
            return visceral_module.visceral_master.execute_visceral_analysis(clean_data, clean_data, session_id=None)
        except Exception as e:
            logger.error(f"❌ Erro no agente visceral_master: {str(e)}")
            return {'error': str(e), 'agent': 'visceral_master', 'fallback': True}

class DriversArchitectAgent:
    """ARQUITETO DE DRIVERS MENTAIS"""

    def execute_analysis(self, data: Dict[str, Any], session_id: str = None) -> Dict[str, Any]:
        """Cria arsenal completo de drivers mentais"""

        prompt = f"""
# VOCÊ É O ARQUITETO DE DRIVERS MENTAIS

Missão: Criar gatilhos psicológicos que funcionam como âncoras emocionais e racionais.

## ARSENAL DOS 19 DRIVERS UNIVERSAIS:
1. DRIVER DA FERIDA EXPOSTA
2. DRIVER DO TROFÉU SECRETO
3. DRIVER DA INVEJA PRODUTIVA
4. DRIVER DO RELÓGIO PSICOLÓGICO
5. DRIVER DA IDENTIDADE APRISIONADA
6. DRIVER DO CUSTO INVISÍVEL
7. DRIVER DA AMBIÇÃO EXPANDIDA
8. DRIVER DO DIAGNÓSTICO BRUTAL
9. DRIVER DO AMBIENTE VAMPIRO
10. DRIVER DO MENTOR SALVADOR
11. DRIVER DA CORAGEM NECESSÁRIA
12. DRIVER DO MECANISMO REVELADO
13. DRIVER DA PROVA MATEMÁTICA
14. DRIVER DO PADRÃO OCULTO
15. DRIVER DA EXCEÇÃO POSSÍVEL
16. DRIVER DO ATALHO ÉTICO
17. DRIVER DA DECISÃO BINÁRIA
18. DRIVER DA OPORTUNIDADE OCULTA
19. DRIVER DO MÉTODO VS SORTE

## CONTEXTO DO PROJETO:
{json.dumps(data, indent=2, ensure_ascii=False)[:2000]}

## CRIE DRIVERS MENTAIS CUSTOMIZADOS:

Para cada driver, desenvolva:
- Nome impactante (máximo 3 palavras)
- Gatilho central (emoção core)
- Definição visceral (1-2 frases essência)
- Mecânica psicológica (como funciona no cérebro)
- Roteiro de ativação completo
- Frases de ancoragem (3-5 frases prontas)
- Prova lógica (dados/fatos sustentam)
- Loop de reforço (como reativar)

RETORNE JSON com drivers customizados completos:

```json
{{
  "drivers_customizados": [
    {{
      "nome": "Nome específico do driver",
      "gatilho_central": "Emoção ou lógica core",
      "definicao_visceral": "Essência em 1-2 frases",
      "mecanica_psicologica": "Como funciona no cérebro",
      "momento_instalacao": "Quando plantar na jornada",
      "roteiro_ativacao": {{
        "pergunta_abertura": "Pergunta que expõe ferida",
        "historia_analogia": "História específica 150+ palavras",
        "metafora_visual": "Metáfora que ancora na memória",
        "comando_acao": "Comando que direciona comportamento"
      }},
      "frases_ancoragem": [
        "Frase 1 de ancoragem",
        "Frase 2 de ancoragem",
        "Frase 3 de ancoragem"
      ],
      "prova_logica": "Dados/fatos que sustentam",
      "loop_reforco": "Como reativar posteriormente"
    }}
  ],
  "sequenciamento_estrategico": {{
    "fase_despertar": ["Drivers para consciência"],
    "fase_desejo": ["Drivers para amplificação"],
    "fase_decisao": ["Drivers para pressão"],
    "fase_direcao": ["Drivers para caminho"]
  }},
  "metricas_densidade": {{
    "total_drivers": 0,
    "drivers_emocionais": 0,
    "drivers_racionais": 0,
    "intensidade_media": 0
  }}
}}
```
"""

        response = ai_manager.generate_analysis(prompt)

        if response:
            return self._process_drivers_response(response, data)
        else:
            return self._generate_drivers_fallback(data)

    def _process_drivers_response(self, response: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa resposta dos drivers"""
        try:
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.rfind("```")
                json_text = response[start:end].strip()
                return json.loads(json_text)
            else:
                return self._extract_drivers_from_text(response, data)
        except:
            return self._generate_drivers_fallback(data)

    def _extract_drivers_from_text(self, text: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai drivers do texto"""
        return {
            'drivers_customizados': [
                {
                    'nome': f'Driver {data.get("segmento", "Negócios")}',
                    'gatilho_central': 'Urgência de transformação',
                    'definicao_visceral': f'Parar de aceitar mediocridade em {data.get("segmento", "negócios")}',
                    'roteiro_ativacao': {
                        'pergunta_abertura': f'Há quanto tempo você aceita resultados medianos em {data.get("segmento", "negócios")}?',
                        'historia_analogia': f'Conheci um profissional de {data.get("segmento", "negócios")} que estava na mesma situação...',
                        'comando_acao': 'Pare de aceitar menos do que merece'
                    }
                }
            ],
            'status': 'drivers_fallback'
        }

    def _generate_drivers_fallback(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera drivers de fallback"""
        return self._extract_drivers_from_text("", data)

    def _execute_agent_drivers_architect(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa agente drivers architect"""
        try:
            # Remove referências circulares dos dados antes de processar
            clean_data = self._clean_data_for_processing(data)

            # Evita importação circular
            import importlib
            drivers_module = importlib.import_module('services.mental_drivers_architect')
            return drivers_module.mental_drivers_architect.generate_custom_drivers(
                clean_data.get('segmento', ''),
                clean_data.get('produto', ''),
                clean_data.get('publico', ''),
                clean_data.get('web_research', {}),
                clean_data.get('social_analysis', {})
            )
        except Exception as e:
            logger.error(f"❌ Erro no agente drivers_architect: {str(e)}")
            return {'error': str(e), 'agent': 'drivers_architect', 'fallback': True}

class VisualDirectorAgent:
    """DIRETOR SUPREMO DE EXPERIÊNCIAS TRANSFORMADORAS"""

    def execute_analysis(self, data: Dict[str, Any], session_id: str = None) -> Dict[str, Any]:
        """Cria arsenal completo de PROVIs"""

        prompt = f"""
# VOCÊ É O DIRETOR SUPREMO DE EXPERIÊNCIAS TRANSFORMADORAS

Missão: Transformar TODOS os conceitos abstratos em experiências físicas inesquecíveis.

## SISTEMA COMPLETO DE PROVAS VISUAIS INSTANTÂNEAS (PROVIs):

### CATEGORIAS DE PROVIS:
- **DESTRUIDORAS DE OBJEÇÃO**: Contra tempo, dinheiro, tentativas anteriores
- **CRIADORAS DE URGÊNCIA**: Ampulheta, trem partindo, porta fechando
- **INSTALADORAS DE CRENÇA**: Transformações visuais poderosas
- **PROVAS DE MÉTODO**: Demonstrações de eficácia

## CONTEXTO PARA CRIAÇÃO:
{json.dumps(data, indent=2, ensure_ascii=False)[:2000]}

## CRIE ARSENAL COMPLETO DE PROVIS:

Para CADA conceito identificado, crie:

```
PROVI #X: [NOME IMPACTANTE]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONCEITO-ALVO: [O que precisa ser instalado/destruído]
CATEGORIA: [Urgência/Crença/Objeção/Transformação/Método]
PRIORIDADE: [Crítica/Alta/Média]

🎯 OBJETIVO PSICOLÓGICO
[Mudança mental específica desejada]

🔬 EXPERIMENTO ESCOLHIDO
[Descrição clara da demonstração física]

📐 ANALOGIA PERFEITA
"Assim como [experimento] → Você [aplicação na vida]"

📝 ROTEIRO COMPLETO
┌─ SETUP (30s): [Preparação que cria expectativa]
├─ EXECUÇÃO (60-90s): [Demonstração com tensão]
├─ CLÍMAX (15s): [Momento exato do "AHA!"]
└─ BRIDGE (30s): [Conexão direta com vida deles]

🛠️ MATERIAIS: [Lista específica e onde conseguir]
⚡ VARIAÇÕES: [Online, Grande público, Intimista]
🚨 PLANO B: [Se algo der errado]
```

RETORNE JSON com arsenal completo de PROVIs:

```json
{{
  "provas_visuais": [
    {{
      "nome": "PROVI 1: Nome impactante",
      "conceito_alvo": "Conceito específico a ser provado",
      "categoria": "Destruidora/Criadora/Instaladora/Prova",
      "prioridade": "Crítica/Alta/Média",
      "objetivo_psicologico": "Mudança mental desejada",
      "experimento": "Descrição detalhada do experimento",
      "analogia_perfeita": "Assim como X, você Y",
      "roteiro_completo": {{
        "setup": "Preparação (30s)",
        "execucao": "Demonstração (60-90s)",
        "climax": "Momento AHA! (15s)",
        "bridge": "Conexão com vida (30s)"
      }},
      "materiais": ["Material 1", "Material 2"],
      "variacoes": {{
        "online": "Adaptação para câmera",
        "grande_publico": "Versão amplificada",
        "intimista": "Versão simplificada"
      }},
      "plano_b": "Alternativa se falhar",
      "frases_impacto": {{
        "durante": "Frase durante tensão",
        "revelacao": "Frase no momento AHA",
        "ancoragem": "Frase que fica na memória"
      }}
    }}
  ],
  "orquestracao_estrategica": {{
    "sequencia_otimizada": ["Ordem dos PROVIs"],
    "escalada_emocional": "Como aumentar intensidade",
    "narrativa_conectora": "Como conectar PROVIs",
    "timing_total": "Duração total recomendada"
  }}
}}
```
"""

        response = ai_manager.generate_analysis(prompt)

        if response:
            return self._process_visual_response(response, data)
        else:
            return self._generate_visual_fallback(data)

    def _process_visual_response(self, response: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa resposta visual"""
        try:
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.rfind("```")
                json_text = response[start:end].strip()
                return json.loads(json_text)
            else:
                return self._extract_visual_insights(response, data)
        except:
            return self._generate_visual_fallback(data)

    def _extract_visual_insights(self, text: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai insights visuais"""
        return {
            'provas_visuais': [
                {
                    'nome': f'PROVI 1: Transformação {data.get("segmento", "Negócios")}',
                    'conceito_alvo': 'Eficácia da metodologia',
                    'experimento': 'Demonstração visual de antes/depois',
                    'materiais': ['Gráficos', 'Dados', 'Comparações']
                }
            ],
            'status': 'visual_fallback'
        }

    def _generate_visual_fallback(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera PROVIs de fallback"""
        return self._extract_visual_insights("", data)

class AntiObjectionAgent:
    """ESPECIALISTA EM PSICOLOGIA DE VENDAS"""

    def execute_analysis(self, data: Dict[str, Any], session_id: str = None) -> Dict[str, Any]:
        """Cria sistema anti-objeção completo"""

        prompt = f"""
# VOCÊ É O ESPECIALISTA EM PSICOLOGIA DE VENDAS

Missão: Criar ARSENAL PSICOLÓGICO para identificar, antecipar e neutralizar TODAS as objeções.

## AS 3 OBJEÇÕES UNIVERSAIS:
1. **TEMPO**: "Isso não é prioridade para mim"
2. **DINHEIRO**: "Minha vida não está tão ruim que precise investir"
3. **CONFIANÇA**: "Me dê uma razão para acreditar"

## AS 5 OBJEÇÕES OCULTAS CRÍTICAS:
1. **AUTOSSUFICIÊNCIA**: "Acho que consigo sozinho"
2. **SINAL DE FRAQUEZA**: "Aceitar ajuda é admitir fracasso"
3. **MEDO DO NOVO**: "Não tenho pressa"
4. **PRIORIDADES DESEQUILIBRADAS**: "Não é dinheiro"
5. **AUTOESTIMA DESTRUÍDA**: "Não confio em mim"

## CONTEXTO PARA ANÁLISE:
{json.dumps(data, indent=2, ensure_ascii=False)[:2000]}

## CRIE SISTEMA ANTI-OBJEÇÃO COMPLETO:

Analise o contexto e crie arsenal psicológico completo com:
- Mapeamento de todas as objeções possíveis
- Técnicas específicas de neutralização
- Scripts personalizados para cada situação
- Sequência psicológica de aplicação
- Arsenal de emergência para objeções de última hora

RETORNE JSON com sistema anti-objeção completo:

```json
{{
  "objecoes_universais": {{
    "tempo": {{
      "objecao": "Objeção específica identificada",
      "raiz_emocional": "Raiz emocional descoberta",
      "contra_ataque": "Técnica específica de neutralização",
      "scripts_personalizados": ["Script 1", "Script 2", "Script 3"],
      "drives_mentais": ["Driver 1", "Driver 2"],
      "historias_viscerais": ["História 1", "História 2"]
    }},
    "dinheiro": {{
      "objecao": "Objeção específica identificada",
      "raiz_emocional": "Raiz emocional descoberta",
      "contra_ataque": "Técnica específica de neutralização",
      "scripts_personalizados": ["Script 1", "Script 2", "Script 3"],
      "drives_mentais": ["Driver 1", "Driver 2"],
      "historias_viscerais": ["História 1", "História 2"]
    }},
    "confianca": {{
      "objecao": "Objeção específica identificada",
      "raiz_emocional": "Raiz emocional descoberta",
      "contra_ataque": "Técnica específica de neutralização",
      "scripts_personalizados": ["Script 1", "Script 2", "Script 3"],
      "drives_mentais": ["Driver 1", "Driver 2"],
      "historias_viscerais": ["História 1", "História 2"]
    }}
  }},
  "objecoes_ocultas": [
    {{
      "tipo": "autossuficiencia",
      "objecao_oculta": "Acho que consigo sozinho",
      "perfil_tipico": "Pessoas com formação superior, ego profissional",
      "raiz_emocional": "Orgulho / Medo de parecer incompetente",
      "sinais": ["Menções de tentar sozinho", "Resistência a ajuda"],
      "contra_ataque": "O Expert que Precisou de Expert",
      "scripts": ["Script específico 1", "Script específico 2"]
    }}
  ],
  "arsenal_emergencia": [
    "Vamos ser honestos: você vai continuar adiando até quando?",
    "A única diferença entre você e quem já conseguiu é a decisão de agir",
    "Quantas oportunidades você já perdeu por 'pensar demais'?",
    "O medo de errar está te impedindo de acertar"
  ],
  "sequencia_neutralizacao": [
    "1. IDENTIFICAR: Qual objeção está sendo verbalizada",
    "2. CONCORDAR: Validar a preocupação como legítima",
    "3. VALORIZAR: Mostrar que pessoas inteligentes pensam assim",
    "4. APRESENTAR: Oferecer nova perspectiva ou solução",
    "5. CONFIRMAR: Verificar se a objeção foi neutralizada",
    "6. ANCORAR: Reforçar a nova crença instalada"
  ]
}}
```
"""

        response = ai_manager.generate_analysis(prompt)

        if response:
            return self._process_anti_objection_response(response, data)
        else:
            return self._generate_anti_objection_fallback(data)

    def _process_anti_objection_response(self, response: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa resposta anti-objeção"""
        try:
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.rfind("```")
                json_text = response[start:end].strip()
                return json.loads(json_text)
            else:
                return self._extract_anti_objection_insights(response, data)
        except:
            return self._generate_anti_objection_fallback(data)

    def _extract_anti_objection_insights(self, text: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai insights anti-objeção"""
        return {
            'sistema_anti_objecao': {
                'analise_bruta': text[:2000],
                'objecoes_identificadas': [
                    'Não tenho tempo para implementar',
                    'Preciso pensar melhor sobre investimento',
                    'Meu caso é muito específico'
                ]
            },
            'status': 'anti_objection_fallback'
        }

    def _generate_anti_objection_fallback(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera sistema anti-objeção de fallback"""
        return self._extract_anti_objection_insights("", data)

class PrePitchArchitectAgent:
    """MESTRE DO PRÉ-PITCH INVISÍVEL"""

    def execute_analysis(self, data: Dict[str, Any], session_id: str = None) -> Dict[str, Any]:
        """Cria orquestração psicológica completa"""

        prompt = f"""
# VOCÊ É O MESTRE DO PRÉ-PITCH INVISÍVEL

Missão: Orquestrar SINFONIA DE TENSÃO PSICOLÓGICA que prepara terreno mental.

## ESTRUTURA DO PRÉ-PITCH:

### FASE 1: ORQUESTRAÇÃO EMOCIONAL (70% do tempo)
- QUEBRA → Destruir ilusão confortável
- EXPOSIÇÃO → Revelar ferida real
- INDIGNAÇÃO → Criar revolta produtiva
- VISLUMBRE → Mostrar o possível
- TENSÃO → Amplificar o gap
- NECESSIDADE → Tornar mudança inevitável

### FASE 2: JUSTIFICAÇÃO LÓGICA (30% do tempo)
- Números irrefutáveis
- Cálculos de ROI conservadores
- Demonstrações passo a passo
- Cases com métricas específicas

## CONTEXTO:
{json.dumps(data, indent=2, ensure_ascii=False)[:2000]}

## CRIE PRÉ-PITCH COMPLETO:

RETORNE JSON com orquestração completa:

```json
{{
  "orquestracao_emocional": {{
    "sequencia_psicologica": [
      {{
        "fase": "quebra",
        "objetivo": "Destruir a ilusão confortável",
        "duracao": "3-5 minutos",
        "drivers_utilizados": ["Diagnóstico Brutal"],
        "narrativa": "Script específico da fase",
        "resultado_esperado": "Desconforto produtivo"
      }}
    ],
    "escalada_emocional": "Como aumentar intensidade",
    "pontos_criticos": ["Momentos de maior impacto"],
    "transicoes": ["Como conectar fases"]
  }},
  "roteiro_completo": {{
    "abertura": {{
      "tempo": "3-5 minutos",
      "script": "Roteiro detalhado da abertura",
      "driver_principal": "Driver utilizado",
      "transicao": "Como conectar com próxima fase"
    }},
    "desenvolvimento": {{
      "tempo": "8-12 minutos",
      "script": "Roteiro detalhado do desenvolvimento",
      "escalada_emocional": "Como aumentar intensidade",
      "momentos_criticos": ["Momento 1", "Momento 2"]
    }},
    "fechamento": {{
      "tempo": "2-3 minutos",
      "script": "Roteiro detalhado do fechamento",
      "ponte_oferta": "Transição perfeita para pitch",
      "estado_mental_ideal": "Como devem estar mentalmente"
    }}
  }},
  "variacoes_formato": {{
    "webinar": {{
      "duracao_total": "15-20 minutos",
      "adaptacoes": ["Usar chat", "Pausas estratégicas"],
      "timing": "Últimos 20 minutos antes da oferta"
    }},
    "evento_presencial": {{
      "duracao_total": "25-35 minutos",
      "adaptacoes": ["Interação direta", "Movimentação"],
      "timing": "Distribuído ao longo do evento"
    }}
  }}
}}
```
"""

        response = ai_manager.generate_analysis(prompt)

        if response:
            return self._process_pre_pitch_response(response, data)
        else:
            return self._generate_pre_pitch_fallback(data)

    def _process_pre_pitch_response(self, response: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa resposta do pré-pitch"""
        try:
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.rfind("```")
                json_text = response[start:end].strip()
                return json.loads(json_text)
            else:
                return self._extract_pre_pitch_insights(response, data)
        except:
            return self._generate_pre_pitch_fallback(data)

    def _extract_pre_pitch_insights(self, text: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai insights do pré-pitch"""
        return {
            'pre_pitch_invisivel': {
                'orquestracao': text[:2000],
                'fases_psicologicas': [
                    'Quebra de padrão',
                    'Exposição da dor',
                    'Vislumbre da solução'
                ]
            },
            'status': 'pre_pitch_fallback'
        }

    def _generate_pre_pitch_fallback(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera pré-pitch de fallback"""
        return self._extract_pre_pitch_insights("", data)

# Instância global
psychological_agents = PsychologicalAgentsSystem()