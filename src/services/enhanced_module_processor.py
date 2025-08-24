#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Enhanced Module Processor
Processador aprimorado de módulos com IA
"""

import os
import logging
import asyncio
import json
from typing import Dict, List, Any
from datetime import datetime
from pathlib import Path

# Import do AI Manager
from services.ai_manager import ai_manager
from services.auto_save_manager import salvar_etapa, salvar_erro
# CORREÇÃO 1: Importar a função com o nome correto
from modules.cpl_creator import create_devastating_cpl_protocol # Import do novo módulo

logger = logging.getLogger(__name__)

class EnhancedModuleProcessor:
    """Processador aprimorado de módulos"""

    def __init__(self):
        """Inicializa o processador"""
        self.ai_manager = ai_manager

        # Lista completa dos módulos (incluindo o novo módulo CPL)
        self.modules_config = {
            'anti_objecao': {
                'title': 'Sistema Anti-Objeção',
                'description': 'Sistema completo para antecipar e neutralizar objeções',
                'use_active_search': False,
                'type': 'standard'
            },
            'avatars': {
                'title': 'Avatares do Público-Alvo',
                'description': 'Personas detalhadas do público-alvo',
                'use_active_search': False,
                'type': 'standard'
            },
            'concorrencia': {
                'title': 'Análise Competitiva',
                'description': 'Análise completa da concorrência',
                'use_active_search': True,
                'type': 'standard'
            },
            'drivers_mentais': {
                'title': 'Drivers Mentais',
                'description': 'Gatilhos psicológicos e drivers de compra',
                'use_active_search': False,
                'type': 'standard'
            },
            'funil_vendas': {
                'title': 'Funil de Vendas',
                'description': 'Estrutura completa do funil de vendas',
                'use_active_search': False,
                'type': 'standard'
            },
            'insights_mercado': {
                'title': 'Insights de Mercado',
                'description': 'Insights profundos sobre o mercado',
                'use_active_search': True,
                'type': 'standard'
            },
            'palavras_chave': {
                'title': 'Estratégia de Palavras-Chave',
                'description': 'Estratégia completa de SEO e palavras-chave',
                'use_active_search': False,
                'type': 'standard'
            },
            'plano_acao': {
                'title': 'Plano de Ação',
                'description': 'Plano de ação detalhado e executável',
                'use_active_search': False,
                'type': 'standard'
            },
            'posicionamento': {
                'title': 'Estratégia de Posicionamento',
                'description': 'Posicionamento estratégico no mercado',
                'use_active_search': False,
                'type': 'standard'
            },
            'pre_pitch': {
                'title': 'Estrutura de Pré-Pitch',
                'description': 'Estrutura de pré-venda e engajamento',
                'use_active_search': False,
                'type': 'standard'
            },
            'predicoes_futuro': {
                'title': 'Predições de Mercado',
                'description': 'Predições e tendências futuras',
                'use_active_search': True,
                'type': 'standard'
            },
            'provas_visuais': {
                'title': 'Sistema de Provas Visuais',
                'description': 'Provas visuais e sociais',
                'use_active_search': False,
                'type': 'standard'
            },
            'metricas_conversao': {
                'title': 'Métricas de Conversão',
                'description': 'KPIs e métricas de conversão',
                'use_active_search': False,
                'type': 'standard'
            },
            'estrategia_preco': {
                'title': 'Estratégia de Precificação',
                'description': 'Estratégia de preços e monetização',
                'use_active_search': False,
                'type': 'standard'
            },
            'canais_aquisicao': {
                'title': 'Canais de Aquisição',
                'description': 'Canais de aquisição de clientes',
                'use_active_search': False,
                'type': 'standard'
            },
            'cronograma_lancamento': {
                'title': 'Cronograma de Lançamento',
                'description': 'Cronograma detalhado de lançamento',
                'use_active_search': False,
                'type': 'standard'
            },
            'cpl_completo': {
                'title': 'Protocolo Integrado de CPLs Devastadores',
                'description': 'Protocolo completo para criação de sequência de 4 CPLs de alta performance',
                'use_active_search': True,
                'type': 'specialized',
                'requires': ['sintese_master', 'avatar_data', 'contexto_estrategico', 'dados_web']
            }
        }

        logger.info("🚀 Enhanced Module Processor inicializado")

    async def generate_all_modules(self, session_id: str) -> Dict[str, Any]:
        """Gera todos os módulos (16 padrão + 1 especializado CPL)"""
        logger.info(f"🚀 Iniciando geração de todos os módulos para sessão: {session_id}")

        # Carrega dados base
        base_data = self._load_base_data(session_id)

        results = {
            "session_id": session_id,
            "successful_modules": 0,
            "failed_modules": 0,
            "modules_generated": [],
            "modules_failed": [],
            "total_modules": len(self.modules_config)
        }

        # Cria diretório de módulos
        modules_dir = Path(f"analyses_data/{session_id}/modules")
        modules_dir.mkdir(parents=True, exist_ok=True)

        # Gera cada módulo
        for module_name, config in self.modules_config.items():
            try:
                logger.info(f"📝 Gerando módulo: {module_name}")

                # Verifica se é o módulo especializado CPL
                if module_name == 'cpl_completo':
                    # CORREÇÃO 2: Chamar a função com o nome correto e argumentos ajustados
                    # Gera o módulo CPL especializado
                    cpl_content = await create_devastating_cpl_protocol(
                        sintese_master=base_data.get('sintese_master', {}),
                        avatar_data=base_data.get('avatar_data', {}),
                        contexto_estrategico=base_data.get('contexto_estrategico', {}),
                        dados_web=base_data.get('dados_web', {}),
                        session_id=session_id # session_id passado como keyword argument
                    )
                    
                    # Salva conteúdo do módulo CPL em formato JSON e Markdown
                    cpl_json_path = modules_dir / f"{module_name}.json"
                    with open(cpl_json_path, 'w', encoding='utf-8') as f:
                        json.dump(cpl_content, f, ensure_ascii=False, indent=2)
                    
                    # Cria versão Markdown do conteúdo CPL
                    cpl_md_content = self._format_cpl_content_to_markdown(cpl_content)
                    cpl_md_path = modules_dir / f"{module_name}.md"
                    with open(cpl_md_path, 'w', encoding='utf-8') as f:
                        f.write(cpl_md_content)
                else:
                    # CORREÇÃO: Sanitiza dados base ANTES de usar
                    sanitized_base_data = self._force_serialize(base_data)
                    
                    # Gera conteúdo do módulo padrão com retry mechanism
                    max_retries = 3
                    content = None
                    
                    for attempt in range(max_retries):
                        try:
                            if config.get('use_active_search', False):
                                content = await self.ai_manager.generate_with_tools(
                                    prompt=self._get_module_prompt(module_name, config, sanitized_base_data),
                                    context=sanitized_base_data.get('context', ''),
                                    tools=["google_search"],
                                    max_iterations=3
                                )
                            else:
                                content = await self.ai_manager.generate_text(
                                    prompt=self._get_module_prompt(module_name, config, sanitized_base_data)
                                )
                            
                            if content and content.strip():
                                break
                            else:
                                logger.warning(f"⚠️ Conteúdo vazio na tentativa {attempt + 1} para {module_name}")
                                
                        except Exception as retry_error:
                            error_msg = str(retry_error)
                            if "object" in error_msg.lower() and attempt < max_retries - 1:
                                logger.warning(f"⚠️ Erro 'object' na tentativa {attempt + 1} para {module_name}, tentando novamente...")
                                await asyncio.sleep(2)
                                continue
                            else:
                                raise retry_error
                    
                    if not content or not content.strip():
                        raise Exception(f"Falha ao gerar conteúdo após {max_retries} tentativas")

                    # Salva módulo padrão
                    module_path = modules_dir / f"{module_name}.md"
                    with open(module_path, 'w', encoding='utf-8') as f:
                        f.write(content)

                results["successful_modules"] += 1
                results["modules_generated"].append(module_name)

                logger.info(f"✅ Módulo {module_name} gerado com sucesso")

            except Exception as e:
                error_msg = str(e)
                logger.error(f"❌ Erro ao gerar módulo {module_name}: {error_msg}")
                
                # Diagnóstico detalhado do erro
                if "object" in error_msg.lower():
                    logger.error(f"❌ ERRO DE SERIALIZAÇÃO detectado no módulo {module_name}")
                    logger.error(f"❌ Tipo do erro: {type(e).__name__}")
                    logger.error(f"❌ Detalhes: {error_msg}")
                    
                    # Verifica se é problema com dados base
                    try:
                        json.dumps(base_data, default=str)
                        logger.info("✅ base_data é serializável")
                    except Exception as json_err:
                        logger.error(f"❌ base_data NÃO é serializável: {json_err}")
                
                salvar_erro(f"modulo_{module_name}", e, contexto={"session_id": session_id})
                results["failed_modules"] += 1
                results["modules_failed"].append({
                    "module": module_name,
                    "error": error_msg,
                    "error_type": type(e).__name__
                })

        # Gera relatório consolidado
        await self._generate_consolidated_report(session_id, results)

        logger.info(f"✅ Geração concluída: {results['successful_modules']}/{results['total_modules']} módulos")

        return results

    def _load_base_data(self, session_id: str) -> Dict[str, Any]:
        """Carrega dados base da sessão"""
        try:
            session_dir = Path(f"analyses_data/{session_id}")

            # Carrega sínteses
            synthesis_data = {}
            for synthesis_file in session_dir.glob("sintese_*.json"):
                try:
                    with open(synthesis_file, 'r', encoding='utf-8') as f:
                        synthesis_data[synthesis_file.stem] = json.load(f)
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao carregar síntese {synthesis_file}: {e}")

            # Carrega relatório de coleta
            coleta_content = ""
            coleta_file = session_dir / "relatorio_coleta.md"
            if coleta_file.exists():
                with open(coleta_file, 'r', encoding='utf-8') as f:
                    coleta_content = f.read()

            # Carrega dados específicos para o módulo CPL
            sintese_master = {}
            avatar_data = {}
            contexto_estrategico = {}
            dados_web = {}
            
            # Tenta carregar a síntese master (múltiplos formatos possíveis)
            sintese_master_files = [
                session_dir / "sintese_master_synthesis.json",
                session_dir / "sintese_master.json",
                session_dir / "sintese_master_data.json"
            ]
            
            for sintese_master_file in sintese_master_files:
                if sintese_master_file.exists():
                    try:
                        with open(sintese_master_file, 'r', encoding='utf-8') as f:
                            sintese_master = json.load(f)
                        logger.info(f"✅ Síntese master carregada de: {sintese_master_file.name}")
                        break
                    except Exception as e:
                        logger.warning(f"⚠️ Erro ao carregar síntese master de {sintese_master_file.name}: {e}")
            
            # Tenta carregar dados do avatar
            avatar_file = session_dir / "avatar_detalhado.json"
            if avatar_file.exists():
                try:
                    with open(avatar_file, 'r', encoding='utf-8') as f:
                        avatar_data = json.load(f)
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao carregar dados do avatar: {e}")
            
            # Tenta carregar contexto estratégico
            contexto_file = session_dir / "contexto_estrategico.json"
            if contexto_file.exists():
                try:
                    with open(contexto_file, 'r', encoding='utf-8') as f:
                        contexto_estrategico = json.load(f)
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao carregar contexto estratégico: {e}")
            
            # Tenta carregar dados da web
            web_data_file = session_dir / "dados_pesquisa_web.json"
            if web_data_file.exists():
                try:
                    with open(web_data_file, 'r', encoding='utf-8') as f:
                        dados_web = json.load(f)
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao carregar dados da web: {e}")

            # Sanitiza dados para garantir serialização
            base_data = {
                "synthesis_data": self._sanitize_data(synthesis_data),
                "coleta_content": str(coleta_content),
                "context": f"Dados de síntese: {len(synthesis_data)} arquivos. Relatório de coleta: {len(coleta_content)} caracteres.",
                "sintese_master": self._sanitize_data(sintese_master),
                "avatar_data": self._sanitize_data(avatar_data),
                "contexto_estrategico": self._sanitize_data(contexto_estrategico),
                "dados_web": self._sanitize_data(dados_web)
            }
            
            # Testa serialização
            try:
                json.dumps(base_data, default=str)
                logger.debug("✅ base_data é serializável")
            except Exception as e:
                logger.error(f"❌ base_data não é serializável: {e}")
                # Força conversão para string de todos os valores problemáticos
                base_data = self._force_serialize(base_data)
            
            return base_data

        except Exception as e:
            logger.error(f"❌ Erro ao carregar dados base: {e}")
            return {
                "synthesis_data": {}, 
                "coleta_content": "", 
                "context": "",
                "sintese_master": {},
                "avatar_data": {},
                "contexto_estrategico": {},
                "dados_web": {}
            }

    def _sanitize_data(self, data: Any) -> Any:
        """Sanitiza dados para garantir serialização JSON"""
        if data is None:
            return None
        elif isinstance(data, (str, int, float, bool)):
            return data
        elif isinstance(data, dict):
            return {str(k): self._sanitize_data(v) for k, v in data.items()}
        elif isinstance(data, (list, tuple)):
            return [self._sanitize_data(item) for item in data]
        else:
            # Converte objetos complexos para string
            return str(data)

    def _force_serialize(self, data: Any) -> Any:
        """Força serialização convertendo tudo para tipos básicos"""
        try:
            return json.loads(json.dumps(data, default=str))
        except Exception as e:
            logger.error(f"❌ Erro na serialização forçada: {e}")
            return str(data)

    def _get_module_prompt(self, module_name: str, config: Dict[str, Any], base_data: Dict[str, Any]) -> str:
        """Gera prompt para um módulo específico"""
        
        # CORREÇÃO: Garante que sempre há contexto suficiente
        context = base_data.get('context', 'Análise de mercado digital brasileiro')
        coleta_content = base_data.get('coleta_content', 'Dados de mercado digital e tendências atuais')
        
        # Se não há dados específicos, usa contexto genérico mas útil
        if not context or context == 'Dados limitados':
            context = f"Análise de {config['description'].lower()} no mercado brasileiro atual"
        
        if not coleta_content:
            coleta_content = f"Tendências atuais em {config['description'].lower()} e melhores práticas do mercado"

        base_prompt = f"""# {config['title']}

Você é um especialista em {config['description'].lower()} com vasta experiência no mercado brasileiro.

## CONTEXTO DA ANÁLISE:
{context}

## TAREFA:
Crie um módulo ultra-detalhado sobre {config['title']} com base nas melhores práticas e tendências atuais.

## ESTRUTURA OBRIGATÓRIA:
1. **Resumo Executivo** (200-300 palavras)
2. **Análise Detalhada** (500-700 palavras)
3. **Estratégias Específicas** (400-600 palavras)
4. **Implementação Prática** (300-500 palavras)
5. **Métricas e KPIs** (200-300 palavras)
6. **Cronograma de Execução** (200-300 palavras)

## REQUISITOS OBRIGATÓRIOS:
- MÍNIMO 2000 palavras no total
- Dados específicos do mercado brasileiro
- Estratégias acionáveis e práticas
- Métricas mensuráveis e realistas
- Formato markdown profissional
- Exemplos concretos e casos de uso

## DADOS DE REFERÊNCIA:
{coleta_content[:1000]}

## IMPORTANTE:
- SEMPRE gere conteúdo completo e detalhado
- Use dados reais do mercado brasileiro quando possível
- Inclua exemplos práticos e acionáveis
- Mantenha tom profissional e consultivo

COMECE AGORA a gerar o módulo completo:
"""

        return base_prompt

    def _format_cpl_content_to_markdown(self, cpl_content: Dict[str, Any]) -> str:
        """Formata o conteúdo do módulo CPL para Markdown"""
        try:
            markdown_content = f"""# {cpl_content.get('titulo', 'Protocolo de CPLs Devastadores')}

{cpl_content.get('descricao', '')}

"""

            # Adiciona cada fase do protocolo
            fases = cpl_content.get('fases', {})
            for fase_key, fase_data in fases.items():
                markdown_content += f"## {fase_data.get('titulo', fase_key)}\n\n"
                markdown_content += f"**{fase_data.get('descricao', '')}**\n\n"
                
                # Adiciona seções específicas de cada fase
                if 'estrategia' in fase_data:
                    markdown_content += f"### Estratégia\n{fase_data['estrategia']}\n\n"
                
                if 'versoes_evento' in fase_data:
                    markdown_content += "### Versões do Evento\n"
                    for versao in fase_data['versoes_evento']:
                        markdown_content += f"- **{versao.get('nome_evento', '')}** ({versao.get('tipo', '')}): {versao.get('justificativa_psicologica', '')}\n"
                    markdown_content += "\n"
                
                if 'teasers' in fase_data:
                    markdown_content += "### Teasers\n"
                    for teaser in fase_data['teasers']:
                        markdown_content += f"- {teaser.get('texto', '')} (*{teaser.get('justificativa', '')}*)\n"
                    markdown_content += "\n"
                
                if 'historia_transformacao' in fase_data:
                    ht = fase_data['historia_transformacao']
                    markdown_content += "### História de Transformação\n"
                    markdown_content += f"- **Antes**: {ht.get('antes', '')}\n"
                    markdown_content += f"- **Durante**: {ht.get('durante', '')}\n"
                    markdown_content += f"- **Depois**: {ht.get('depois', '')}\n\n"
                
                # Adiciona outras seções conforme necessário...
                markdown_content += "---\n\n"
            
            # Adiciona considerações finais
            consideracoes = cpl_content.get('consideracoes_finais', {})
            if consideracoes:
                markdown_content += "## Considerações Finais\n\n"
                markdown_content += f"**Impacto Previsto**: {consideracoes.get('impacto_previsto', '')}\n\n"
                
                if consideracoes.get('diferenciais'):
                    markdown_content += "### Diferenciais\n"
                    for diferencial in consideracoes['diferenciais']:
                        markdown_content += f"- {diferencial}\n"
                    markdown_content += "\n"
                
                if consideracoes.get('proximos_passos'):
                    markdown_content += "### Próximos Passos\n"
                    for passo in consideracoes['proximos_passos']:
                        markdown_content += f"- {passo}\n"
                    markdown_content += "\n"

            return markdown_content
            
        except Exception as e:
            logger.error(f"❌ Erro ao formatar conteúdo CPL para Markdown: {e}")
            return "# Protocolo de CPLs Devastadores\n\n*Erro ao gerar conteúdo formatado*"

    async def _generate_consolidated_report(self, session_id: str, results: Dict[str, Any]) -> None:
        """Gera relatório consolidado final"""
        try:
            logger.info("📋 Gerando relatório consolidado final...")

            # Carrega todos os módulos gerados
            modules_dir = Path(f"analyses_data/{session_id}/modules")
            consolidated_content = f"""# RELATÓRIO FINAL CONSOLIDADO - ARQV30 Enhanced v3.0

**Sessão:** {session_id}  
**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}  
**Módulos Gerados:** {results['successful_modules']}/{results['total_modules']}  
**Taxa de Sucesso:** {(results['successful_modules']/results['total_modules']*100):.1f}%

---

## SUMÁRIO EXECUTIVO

Este relatório consolida {results['successful_modules']} módulos especializados de análise estratégica gerados pelo sistema ARQV30 Enhanced v3.0.

## MÓDULOS INCLUÍDOS

"""

            # Adiciona cada módulo gerado (incluindo o novo CPL)
            for module_name in results['modules_generated']:
                # Trata o módulo CPL de forma especial
                if module_name == 'cpl_completo':
                    cpl_json_file = modules_dir / f"{module_name}.json"
                    if cpl_json_file.exists():
                        try:
                            with open(cpl_json_file, 'r', encoding='utf-8') as f:
                                cpl_data = json.load(f)
                                title = cpl_data.get('titulo', self.modules_config[module_name]['title'])
                                descricao = cpl_data.get('descricao', '')
                                consolidated_content += f"\n## {title}\n\n{descricao}\n\n"
                                
                                # Adiciona um resumo das fases
                                fases = cpl_data.get('fases', {})
                                if fases:
                                    consolidated_content += "### Fases do Protocolo:\n"
                                    for fase_key, fase_data in fases.items():
                                        consolidated_content += f"- **{fase_data.get('titulo', fase_key)}**: {fase_data.get('descricao', '')[:100]}...\n"
                                    consolidated_content += "\n"
                        except Exception as e:
                            logger.warning(f"⚠️ Erro ao carregar conteúdo CPL para relatório: {e}")
                            consolidated_content += f"\n## {self.modules_config[module_name]['title']}\n\n*Conteúdo não disponível*\n\n"
                    else:
                        consolidated_content += f"\n## {self.modules_config[module_name]['title']}\n\n*Conteúdo não gerado*\n\n"
                else:
                    # Trata módulos padrão
                    module_file = modules_dir / f"{module_name}.md"
                    if module_file.exists():
                        try:
                            with open(module_file, 'r', encoding='utf-8') as f:
                                content = f.read()
                                title = self.modules_config[module_name]['title']
                                # Extrai apenas o título e resumo executivo para o relatório consolidado
                                lines = content.split('\n')
                                summary_lines = []
                                in_executive_summary = False
                                
                                for line in lines:
                                    if line.startswith('# ') and 'Resumo Executivo' in line:
                                        in_executive_summary = True
                                        summary_lines.append(line)
                                    elif in_executive_summary and line.startswith('#') and 'Resumo Executivo' not in line:
                                        break
                                    elif in_executive_summary:
                                        summary_lines.append(line)
                                
                                if summary_lines:
                                    consolidated_content += f"\n## {title}\n\n" + '\n'.join(summary_lines[1:10]) + "\n\n"
                                else:
                                    # Se não encontrar resumo executivo, usa as primeiras linhas
                                    consolidated_content += f"\n## {title}\n\n" + '\n'.join(lines[:5]) + "\n\n"
                        except Exception as e:
                            logger.warning(f"⚠️ Erro ao carregar conteúdo do módulo {module_name} para relatório: {e}")
                            consolidated_content += f"\n## {self.modules_config[module_name]['title']}\n\n*Conteúdo não disponível*\n\n"
                consolidated_content += "---\n\n"

            # Adiciona informações de módulos falhados
            if results['modules_failed']:
                consolidated_content += "\n## MÓDULOS NÃO GERADOS\n\n"
                for failed in results['modules_failed']:
                    consolidated_content += f"- **{failed['module']}**: {failed['error']}\n"

            # Salva relatório consolidado
            consolidated_path = f"analyses_data/{session_id}/relatorio_final_completo.md"
            with open(consolidated_path, 'w', encoding='utf-8') as f:
                f.write(consolidated_content)

            logger.info(f"✅ Relatório consolidado salvo em: {consolidated_path}")

        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório consolidado: {e}")
            salvar_erro("relatorio_consolidado", e, contexto={"session_id": session_id})

# Instância global
enhanced_module_processor = EnhancedModuleProcessor()
