#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Auto Save Manager
Sistema de salvamento automático ultra-robusto
"""

import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

# Import do serviço preditivo (lazy loading para evitar circular imports)
_predictive_service = None

def get_predictive_service():
    """Lazy loading do serviço preditivo"""
    global _predictive_service
    if _predictive_service is None:
        try:
            from services.predictive_analytics_service import predictive_analytics_service
            _predictive_service = predictive_analytics_service
        except ImportError as e:
            logger.warning(f"⚠️ Serviço preditivo não disponível: {e}")
            _predictive_service = None
    return _predictive_service

def serializar_dados_seguros(dados: Any) -> Dict[str, Any]:
    """
    Serializa dados de forma segura para JSON, lidando com tipos não serializáveis.
    Se os dados já forem um dict com a chave 'data', assume que já é um formato esperado.
    """
    if isinstance(dados, dict) and "data" in dados:
        return dados

    serializable_data = {}
    if isinstance(dados, dict):
        serializable_data["data"] = dados
    elif isinstance(dados, list):
        serializable_data["data"] = dados
    else:
        serializable_data["data"] = str(dados)

    serializable_data["timestamp"] = datetime.now().isoformat()
    return serializable_data

class AutoSaveManager:
    """Gerenciador de salvamento automático ultra-robusto"""

    def __init__(self):
        """Inicializa o gerenciador de salvamento"""
        self.base_path = "relatorios_intermediarios"
        self.analyses_path = "analyses_data"
        self._ensure_directories()

        logger.info("🔧 Auto Save Manager inicializado")

    def _ensure_directories(self):
        """Garante que todos os diretórios necessários existem"""
        directories = [
            self.base_path,
            self.analyses_path,
            f"{self.base_path}/analise_completa",
            f"{self.base_path}/pesquisa_web", # Para logs do WebSailor
            f"{self.base_path}/logs",
            f"{self.base_path}/erros",
            f"{self.base_path}/workflow", # Para etapas do workflow
            f"{self.analyses_path}/analyses",
            f"{self.analyses_path}/anti_objecao",
            f"{self.analyses_path}/avatars",
            f"{self.analyses_path}/completas",
            f"{self.analyses_path}/concorrencia",
            f"{self.analyses_path}/drivers_mentais",
            f"{self.analyses_path}/files",
            f"{self.analyses_path}/funil_vendas",
            f"{self.analyses_path}/insights",
            f"{self.analyses_path}/logs",
            f"{self.analyses_path}/metadata",
            f"{self.analyses_path}/metricas",
            f"{self.analyses_path}/palavras_chave",
            f"{self.analyses_path}/pesquisa_web", # *** NOVO: Diretório principal para trechos de texto ***
            f"{self.analyses_path}/plano_acao",
            f"{self.analyses_path}/posicionamento",
            f"{self.analyses_path}/pre_pitch",
            f"{self.analyses_path}/predicoes_futuro",
            f"{self.analyses_path}/progress",
            f"{self.analyses_path}/provas_visuais",
            f"{self.analyses_path}/reports",
            f"{self.analyses_path}/users"
        ]

        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
            except Exception as e:
                logger.error(f"❌ Erro ao criar diretório {directory}: {e}")

    def salvar_etapa(self, nome_etapa: str, dados: Any, categoria: str = "analise_completa", session_id: str = None) -> str:
        """Salva uma etapa do processo com timestamp"""
        try:
            # Gera timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]

            # Define diretório base
            if session_id:
                diretorio = f"{self.base_path}/{categoria}/{session_id}"
            else:
                diretorio = f"{self.base_path}/{categoria}"

            os.makedirs(diretorio, exist_ok=True)

            # Nome do arquivo
            nome_arquivo = f"{nome_etapa}_{timestamp}"

            # Salva como JSON se possível
            try:
                arquivo_json = f"{diretorio}/{nome_arquivo}.json"

                # Serializa dados de forma segura
                dados_serializaveis = serializar_dados_seguros(dados)

                # Valida se há conteúdo nos dados
                if not dados_serializaveis or (isinstance(dados_serializaveis, dict) and not dados_serializaveis.get("data")):
                    logger.warning(f"⚠️ Dados vazios para {nome_etapa}, criando placeholder")
                    dados_serializaveis = {
                        "status": "empty_data",
                        "message": "Dados não disponíveis no momento",
                        "timestamp": datetime.now().isoformat(),
                        "original_data": dados_serializaveis
                    }

                with open(arquivo_json, 'w', encoding='utf-8') as f:
                    json.dump(dados_serializaveis, f, ensure_ascii=False, indent=2)

                logger.info(f"💾 Etapa '{nome_etapa}' salva: {arquivo_json}")

                # INTEGRAÇÃO COM ANÁLISE PREDITIVA
                self._trigger_predictive_analysis(nome_etapa, dados_serializaveis, categoria, session_id)

                # TAMBÉM salva na pasta analyses_data se for um módulo
                # Lista de categorias que devem ser salvas em analyses_data
                modulos_para_analyses_data = [
                    "avatars", "drivers_mentais", "anti_objecao", "provas_visuais",
                    "pre_pitch", "predicoes_futuro", "posicionamento", "concorrencia",
                    "palavras_chave", "funil_vendas", "insights", "plano_acao"
                ]

                # Verifica se a categoria atual está na lista de módulos a serem salvos em analyses_data
                if categoria in modulos_para_analyses_data:
                    try:
                        # Extrai nome do módulo da etapa (pode precisar de ajuste dependendo do prefixo)
                        # Assumindo que a categoria já é o nome base do módulo
                        nome_modulo_base = categoria

                        analyses_dir = f"{self.analyses_path}/{categoria}"
                        os.makedirs(analyses_dir, exist_ok=True)

                        analyses_arquivo_nome = f"{nome_modulo_base}_{timestamp}.json" if session_id is None else f"{nome_modulo_base}_{session_id}_{timestamp}.json"
                        analyses_arquivo = os.path.join(analyses_dir, analyses_arquivo_nome)

                        with open(analyses_arquivo, 'w', encoding='utf-8') as f:
                            json.dump(dados_serializaveis, f, ensure_ascii=False, indent=2)

                        logger.info(f"💾 Módulo também salvo em analyses_data: {analyses_arquivo}")

                    except Exception as e:
                        logger.warning(f"⚠️ Não foi possível salvar em analyses_data para a etapa {nome_etapa} (categoria: {categoria}): {e}")

                return arquivo_json

            except Exception as json_error:
                logger.warning(f"⚠️ Falha ao salvar como JSON ({json_error}), tentando salvar como texto...")
                # Fallback para texto se falhar ao salvar como JSON
                arquivo_txt = f"{diretorio}/{nome_arquivo}.txt"
                with open(arquivo_txt, 'w', encoding='utf-8') as f:
                    if isinstance(dados, str):
                        f.write(dados)
                    else:
                        f.write(str(dados))

                logger.info(f"💾 Etapa '{nome_etapa}' salva: {arquivo_txt}")
                return arquivo_txt

        except Exception as e:
            logger.error(f"❌ Erro ao salvar etapa {nome_etapa}: {e}")
            return ""

    # === NOVA FUNÇÃO: salvar_trecho_pesquisa_web ===
    def salvar_trecho_pesquisa_web(self, url: str, titulo: str, conteudo: str, metodo_extracao: str, qualidade: float, session_id: str) -> str:
        """
        Salva um trecho de texto extraído de uma pesquisa web.

        Args:
            url (str): A URL da página de origem.
            titulo (str): O título da página.
            conteudo (str): O conteúdo textual extraído.
            metodo_extracao (str): O método usado para extrair (e.g., 'jina', 'exa', 'readability').
            qualidade (float): Um score de qualidade do conteúdo (0-100).
            session_id (str): O ID da sessão de análise.

        Returns:
            str: O caminho do arquivo salvo, ou string vazia em caso de erro.
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            
            # Diretório específico para trechos de pesquisa web
            diretorio = f"{self.analyses_path}/pesquisa_web/{session_id}"
            os.makedirs(diretorio, exist_ok=True)

            # Nome do arquivo baseado na URL e timestamp para unicidade
            # Sanitiza a URL para nome de arquivo
            nome_arquivo_seguro = "".join(c for c in url if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()
            # Limita o tamanho do nome do arquivo
            nome_arquivo_seguro = nome_arquivo_seguro[:100] if len(nome_arquivo_seguro) > 100 else nome_arquivo_seguro
            # Substitui espaços por underscores
            nome_arquivo_seguro = nome_arquivo_seguro.replace(" ", "_")
            
            nome_arquivo = f"trecho_{nome_arquivo_seguro}_{timestamp}.json"
            arquivo_completo = os.path.join(diretorio, nome_arquivo)

            # Dados a serem salvos
            dados_trecho = {
                "url": url,
                "titulo": titulo,
                "conteudo": conteudo,
                "metodo_extracao": metodo_extracao,
                "qualidade": qualidade,
                "timestamp_extracao": timestamp,
                "session_id": session_id
            }

            with open(arquivo_completo, 'w', encoding='utf-8') as f:
                json.dump(dados_trecho, f, ensure_ascii=False, indent=2)

            logger.info(f"🔍 Trecho de pesquisa web salvo: {arquivo_completo} (Qualidade: {qualidade:.1f})")
            return arquivo_completo

        except Exception as e:
            logger.error(f"❌ Erro ao salvar trecho de pesquisa web para {url}: {e}")
            return ""

    def salvar_erro(self, nome_erro: str, erro: Exception, contexto: Dict[str, Any] = None, session_id: str = None) -> str:
        """Salva um erro com contexto"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]

            if session_id:
                diretorio = f"{self.base_path}/erros/{session_id}"
            else:
                diretorio = f"{self.base_path}/erros"

            os.makedirs(diretorio, exist_ok=True)

            erro_data = {
                "erro": str(erro),
                "tipo": type(erro).__name__,
                "timestamp": timestamp,
                "contexto": contexto or {}
            }

            arquivo_erro = f"{diretorio}/ERRO_{nome_erro}_{timestamp}.txt"
            with open(arquivo_erro, 'w', encoding='utf-8') as f:
                f.write(f"ERRO: {nome_erro}\n")
                f.write(f"Timestamp: {timestamp}\n")
                f.write(f"Tipo: {type(erro).__name__}\n")
                f.write(f"Mensagem: {str(erro)}\n")
                if contexto:
                    f.write(f"Contexto: {json.dumps(contexto, ensure_ascii=False, indent=2)}\n")

            logger.error(f"💾 Erro '{nome_erro}' salvo: {arquivo_erro}")
            return arquivo_erro

        except Exception as e:
            logger.error(f"❌ Erro ao salvar erro {nome_erro}: {e}")
            return ""

    def salvar_modulo_analyses_data(self, nome_modulo: str, dados: Any, session_id: str = None) -> str:
        """Salva módulo na pasta analyses_data"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]

            # Diretório específico do módulo - vamos usar a categoria 'geral' por padrão se não especificada
            # Ou, se quiser uma estrutura mais granular, pode passar a categoria como argumento
            categoria = "geral" # Valor padrão, pode ser ajustado se necessário

            # Tentativa de inferir categoria do nome_modulo se ele tiver o formato esperado
            if "_" in nome_modulo:
                parts = nome_modulo.split("_")
                if len(parts) > 1:
                    # Assumindo que a categoria é a parte antes do primeiro underscore, ex: "funil_vendas" -> "funil_vendas"
                    # Ou se for algo como "module_funil_vendas", a categoria seria "funil_vendas"
                    # Vamos simplificar e usar a categoria que foi passada na função salvar_etapa se ela existir.
                    # Se não, vamos usar uma categoria genérica ou o nome do módulo sem o prefixo se houver.
                    pass # Manteremos a lógica de categoria sendo passada de salvar_etapa

            diretorio = f"{self.analyses_path}/{categoria}"
            os.makedirs(diretorio, exist_ok=True)

            # Nome do arquivo
            if session_id:
                nome_arquivo = f"{nome_modulo}_{session_id}_{timestamp}.json"
            else:
                nome_arquivo = f"{nome_modulo}_{timestamp}.json"

            arquivo_completo = f"{diretorio}/{nome_arquivo}"

            # Salva como JSON
            with open(arquivo_completo, 'w', encoding='utf-8') as f:
                if isinstance(dados, (dict, list)):
                    json.dump(dados, f, ensure_ascii=False, indent=2)
                else:
                    json.dump({"modulo": nome_modulo, "dados": str(dados), "timestamp": timestamp}, f, ensure_ascii=False, indent=2)

            logger.info(f"📁 Módulo '{nome_modulo}' salvo em analyses_data: {arquivo_completo}")
            return arquivo_completo

        except Exception as e:
            logger.error(f"❌ Erro ao salvar módulo {nome_modulo} em analyses_data: {e}")
            return ""

    def salvar_json_gigante(self, dados: Dict[str, Any], session_id: str) -> str:
        """Salva JSON gigante com dados massivos"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dados_massivos_{session_id}_{timestamp}.json"
            filepath = os.path.join(self.base_path, "completas", filename)
            
            # Garante que o diretório existe
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Salva JSON com formatação
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            
            # Calcula estatísticas
            file_size = os.path.getsize(filepath)
            content_length = len(json.dumps(dados, ensure_ascii=False))
            
            logger.info(f"💾 JSON gigante salvo: {filepath}")
            logger.info(f"📊 Tamanho: {file_size:,} bytes ({content_length:,} caracteres)")
            
            return filepath
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar JSON gigante: {e}")
            raise

    def recuperar_etapa(self, nome_etapa: str, session_id: str = None) -> Dict[str, Any]:
        """Recupera dados de uma etapa salva"""
        try:
            if session_id:
                diretorio = f"{self.base_path}/{session_id}"
            else:
                diretorio = self.base_path
            
            # Procura arquivo da etapa
            import glob
            pattern = f"{diretorio}/*{nome_etapa}*.json"
            arquivos = glob.glob(pattern)
            
            if not arquivos:
                return {"status": "nao_encontrado", "dados": {}}
            
            # Pega o arquivo mais recente
            arquivo_mais_recente = max(arquivos, key=os.path.getctime)
            
            with open(arquivo_mais_recente, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            return {"status": "sucesso", "dados": dados, "arquivo": arquivo_mais_recente}
            
        except Exception as e:
            logger.error(f"❌ Erro ao recuperar etapa {nome_etapa}: {e}")
            return {"status": "erro", "erro": str(e), "dados": {}}

    def listar_etapas_salvas(self, session_id: str = None) -> Dict[str, str]:
        """Lista todas as etapas salvas"""
        etapas = {}

        try:
            if session_id:
                base_dir = f"{self.base_path}"
                for categoria in os.listdir(base_dir):
                    categoria_path = f"{base_dir}/{categoria}"
                    if os.path.isdir(categoria_path):
                        session_path = f"{categoria_path}/{session_id}"
                        if os.path.exists(session_path):
                            for arquivo in os.listdir(session_path):
                                if arquivo.endswith(('.json', '.txt')):
                                    nome_etapa = arquivo.split('_')[0]
                                    etapas[nome_etapa] = f"{session_path}/{arquivo}"

        except Exception as e:
            logger.error(f"❌ Erro ao listar etapas: {e}")

        return etapas

    def recuperar_etapa(self, nome_etapa: str, session_id: str = None) -> Dict[str, Any]:
        """Recupera dados de uma etapa salva"""
        try:
            etapas = self.listar_etapas_salvas(session_id)

            if nome_etapa in etapas:
                arquivo = etapas[nome_etapa]

                if arquivo.endswith('.json'):
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        dados = json.load(f)
                    return {"status": "sucesso", "dados": dados}
                else:
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        dados = f.read()
                    return {"status": "sucesso", "dados": dados}

            return {"status": "erro", "mensagem": "Etapa não encontrada"}

        except Exception as e:
            logger.error(f"❌ Erro ao recuperar etapa {nome_etapa}: {e}")
            return {"status": "erro", "mensagem": str(e)}

    def salvar_json_gigante(self, dados_massivos: Dict[str, Any], session_id: str) -> str:
        """Salva o JSON gigante com todos os dados coletados"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]

            diretorio = f"{self.analyses_path}/completas"
            os.makedirs(diretorio, exist_ok=True)

            arquivo = f"{diretorio}/dados_massivos_{session_id}_{timestamp}.json"

            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados_massivos, f, ensure_ascii=False, indent=2)

            logger.info(f"🗂️ JSON gigante salvo: {arquivo}")
            return arquivo

        except Exception as e:
            logger.error(f"❌ Erro ao salvar JSON gigante: {e}")
            return ""

    def salvar_relatorio_final(self, relatorio: str, session_id: str) -> str:
        """Salva o relatório final detalhado"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]

            diretorio = f"{self.analyses_path}/reports"
            os.makedirs(diretorio, exist_ok=True)

            # Salva também como .md para facilitar visualização
            arquivo_md = f"{diretorio}/relatorio_final_{session_id}_{timestamp}.md"
            with open(arquivo_md, 'w', encoding='utf-8') as f:
                f.write(relatorio)
            
            # Salva como .txt também, mantendo compatibilidade
            arquivo_txt = f"{diretorio}/relatorio_final_{session_id}_{timestamp}.txt"
            with open(arquivo_txt, 'w', encoding='utf-8') as f:
                f.write(relatorio)

            logger.info(f"📄 Relatório final salvo: {arquivo_md}")
            return arquivo_md

        except Exception as e:
            logger.error(f"❌ Erro ao salvar relatório final: {e}")
            return ""

    def _clean_for_serialization(self, obj, seen=None, depth=0):
        """Limpa objeto para serialização JSON removendo referências circulares e tipos não serializáveis"""
        if seen is None:
            seen = set()

        # Limite de profundidade para evitar recursão infinita
        if depth > 15:
            return {"__max_depth__": f"Depth limit reached at {depth}"}

        # Verifica referência circular
        obj_id = id(obj)
        if obj_id in seen:
            return {"__circular_ref__": f"{type(obj).__name__}_{obj_id}"}

        seen.add(obj_id)

        try:
            # Tipos primitivos - retorna direto
            if obj is None or isinstance(obj, (bool, int, float, str)):
                return obj

            # Dicionários - TRATAMENTO ESPECIAL PARA EVITAR unhashable type
            elif isinstance(obj, dict):
                result = {}
                for key, value in obj.items():
                    # Converte chaves para string segura
                    try:
                        if isinstance(key, (dict, list, set)):
                            # Se a chave é um tipo não hashable, converte para string
                            safe_key = f"key_{hash(str(key))}"
                        else:
                            safe_key = str(key)[:100]  # Limita tamanho da chave
                    except Exception:
                        safe_key = f"key_{obj_id}_{len(result)}"

                    try:
                        result[safe_key] = self._clean_for_serialization(value, seen.copy(), depth + 1)
                    except Exception as e:
                        result[safe_key] = f"<Error serializing: {str(e)[:50]}>"
                return result

            # Listas e tuplas
            elif isinstance(obj, (list, tuple)):
                result = []
                for i, item in enumerate(obj[:100]):  # Limita a 100 itens para evitar listas enormes
                    try:
                        result.append(self._clean_for_serialization(item, seen.copy(), depth + 1))
                    except Exception as e:
                        result.append(f"<Error at index {i}: {str(e)[:50]}>")
                return result

            # Sets - converte para lista
            elif isinstance(obj, set):
                try:
                    return [self._clean_for_serialization(item, seen.copy(), depth + 1) for item in list(obj)[:50]]
                except Exception:
                    return [f"<Set item {i}>" for i in range(min(len(obj), 50))]

            # Objetos com __dict__
            elif hasattr(obj, '__dict__'):
                try:
                    return self._clean_for_serialization(obj.__dict__, seen.copy(), depth + 1)
                except Exception:
                    return {"__object__": f"{type(obj).__name__}"}

            # Funções e métodos
            elif callable(obj):
                return f"<function {getattr(obj, '__name__', 'unknown')}>"

            # Tipos especiais (datetime, etc)
            elif hasattr(obj, 'isoformat'):  # datetime objects
                try:
                    return obj.isoformat()
                except Exception:
                    return str(obj)

            # Outros tipos - converte para string segura
            else:
                try:
                    # Tenta serializar diretamente primeiro
                    import json
                    json.dumps(obj)
                    return obj
                except (TypeError, ValueError):
                    # Se não conseguir, converte para string
                    try:
                        str_repr = str(obj)[:500]  # Limita tamanho
                        return {"__string_repr__": str_repr, "__type__": type(obj).__name__}
                    except Exception:
                        return {"__unserializable__": type(obj).__name__}

        except Exception as e:
            logger.warning(f"Erro crítico ao limpar objeto: {e}")
            return {"__serialization_error__": str(e)[:100]}
        finally:
            seen.discard(obj_id)

    def make_serializable(self, data):
        """
        Converte objetos não serializáveis para formatos JSON-compatíveis
        Versão otimizada para resolver problemas específicos de 'unhashable type: dict'
        """
        try:
            # Testa se já é serializável
            import json
            json.dumps(data)
            return data
        except (TypeError, ValueError) as e:
            if "unhashable type" in str(e):
                logger.warning(f"⚠️ Detectado problema 'unhashable type', aplicando correção...")
            return self._clean_for_serialization(data)

    def _trigger_predictive_analysis(self, nome_etapa: str, dados: Dict[str, Any], categoria: str, session_id: str):
        """
        Aciona análises preditivas automaticamente após salvar dados-chave.
        Implementa as especificações dos aprimoramentos.
        """
        if not session_id:
            return
        
        try:
            predictive_service = get_predictive_service()
            if not predictive_service:
                return
            
            # Condição 1: Após salvar dados da categoria 'pesquisa_web'
            if categoria == "pesquisa_web" or "websailor" in nome_etapa.lower():
                try:
                    # Extrai conteúdo para análise
                    content = ""
                    if isinstance(dados, dict):
                        if "data" in dados:
                            content = str(dados["data"])
                        elif "content" in dados:
                            content = str(dados["content"])
                        else:
                            content = str(dados)
                    else:
                        content = str(dados)
                    
                    # Calcula score de qualidade
                    qualidade_score = predictive_service.get_content_quality_score(content)
                    
                    # Salva o score
                    self.salvar_etapa(
                        f"{nome_etapa}_qualidade", 
                        {"score": qualidade_score, "content_length": len(content)}, 
                        "analise_qualidade", 
                        session_id
                    )
                    
                    logger.info(f"🔮 Score de qualidade calculado para {nome_etapa}: {qualidade_score:.1f}")
                    
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao calcular qualidade para {nome_etapa}: {e}")
            
            # Condição 2: Após salvar dados da categoria 'conteudo_sintetizado'
            elif categoria == "conteudo_sintetizado" or "sintese" in nome_etapa.lower():
                try:
                    # Extrai conteúdo principal
                    conteudo_principal = ""
                    if isinstance(dados, dict):
                        if "data" in dados and isinstance(dados["data"], dict):
                            conteudo_principal = dados["data"].get("conteudo_principal", "")
                        elif "conteudo_principal" in dados:
                            conteudo_principal = dados["conteudo_principal"]
                        else:
                            conteudo_principal = str(dados)
                    else:
                        conteudo_principal = str(dados)
                    
                    if conteudo_principal:
                        # Executa análise de chunk de forma assíncrona
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        try:
                            insights_parciais = loop.run_until_complete(
                                predictive_service.analyze_content_chunk(conteudo_principal)
                            )
                            
                            # Salva insights parciais
                            self.salvar_etapa(
                                f"{nome_etapa}_insights_parciais", 
                                insights_parciais, 
                                "insights_parciais", 
                                session_id
                            )
                            
                            logger.info(f"🔮 Insights parciais gerados para {nome_etapa}")
                            
                        finally:
                            loop.close()
                    
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao gerar insights parciais para {nome_etapa}: {e}")
            
        except Exception as e:
            logger.warning(f"⚠️ Erro na integração preditiva para {nome_etapa}: {e}")

# Instância global
auto_save_manager = AutoSaveManager()

# Funções de conveniência para importação direta
def salvar_etapa(nome_etapa: str, dados: Any, categoria: str = "analise_completa", session_id: str = None) -> str:
    """Função de conveniência para salvar etapa"""
    # A lógica de salvar em analyses_data já está dentro do método salvar_etapa
    return auto_save_manager.salvar_etapa(nome_etapa, dados, categoria, session_id)

# === NOVA FUNÇÃO DE CONVENIÊNCIA ===
def salvar_trecho_pesquisa_web(url: str, titulo: str, conteudo: str, metodo_extracao: str, qualidade: float, session_id: str) -> str:
    """Função de conveniência para salvar trecho de pesquisa web."""
    return auto_save_manager.salvar_trecho_pesquisa_web(url, titulo, conteudo, metodo_extracao, qualidade, session_id)

def salvar_erro(nome_erro: str, erro: Exception, contexto: Dict[str, Any] = None, session_id: str = None) -> str:
    """Função de conveniência para salvar erro"""
    return auto_save_manager.salvar_erro(nome_erro, erro, contexto, session_id)

def salvar_modulo_analyses_data(nome_modulo: str, dados: Any, session_id: str = None) -> str:
    """Função de conveniência para salvar módulo em analyses_data"""
    # Esta função pode ser mantida para uso explícito, mas a lógica principal está em salvar_etapa
    return auto_save_manager.salvar_modulo_analyses_data(nome_modulo, dados, session_id)
