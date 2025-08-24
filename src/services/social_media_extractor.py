#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Social Media Extractor
Extrator robusto para redes sociais
"""

import logging
import re
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import Counter, defaultdict

logger = logging.getLogger(__name__)

class SocialMediaExtractor:
    """Extrator para análise de redes sociais"""

    def __init__(self):
        """Inicializa o extrator de redes sociais"""
        self.enabled = True
        logger.info("✅ Social Media Extractor inicializado")

    async def extract_comprehensive_data(self, query: str, context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Extrai dados abrangentes REAIS de redes sociais com foco em engajamento"""
        logger.info(f"🔍 Extraindo dados abrangentes REAIS para: {query}")
        
        try:
            # Busca em todas as plataformas com dados de engajamento REAIS
            all_platforms_data = await self.search_all_platforms_enhanced(query, max_results_per_platform=15)
            
            # Analisa sentimento
            sentiment_analysis = self.analyze_sentiment_trends(all_platforms_data)
            
            # Identifica conteúdo de alto engajamento
            high_engagement_content = self.identify_high_engagement_content(all_platforms_data)
            
            # Extrai insights de hashtags e tendências
            hashtag_insights = self.extract_hashtag_insights(all_platforms_data)
            
            # Analisa padrões de timing
            timing_patterns = self.analyze_posting_patterns(all_platforms_data)
            
            return {
                "success": True,
                "query": query,
                "session_id": session_id,
                "all_platforms_data": all_platforms_data,
                "sentiment_analysis": sentiment_analysis,
                "high_engagement_content": high_engagement_content,
                "hashtag_insights": hashtag_insights,
                "timing_patterns": timing_patterns,
                "total_posts": all_platforms_data.get("total_results", 0),
                "platforms_analyzed": len(all_platforms_data.get("platforms", [])),
                "extracted_at": datetime.now().isoformat(),
                "engagement_metrics": {
                    "avg_likes": high_engagement_content.get("avg_likes", 0),
                    "avg_comments": high_engagement_content.get("avg_comments", 0),
                    "avg_shares": high_engagement_content.get("avg_shares", 0),
                    "top_performing_threshold": high_engagement_content.get("threshold", 0)
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na extração abrangente: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query,
                "session_id": session_id
            }

    async def search_all_platforms(self, query: str, max_results_per_platform: int = 10) -> Dict[str, Any]:
        """Busca REAL em todas as plataformas de redes sociais"""

        logger.info(f"🔍 Iniciando busca REAL em redes sociais para: {query}")

        results = {
            "query": query,
            "platforms": ["youtube", "twitter", "instagram", "linkedin"],
            "total_results": 0,
            "youtube": await self._extract_real_youtube_data(query, max_results_per_platform),
            "twitter": await self._extract_real_twitter_data(query, max_results_per_platform),
            "instagram": await self._extract_real_instagram_data(query, max_results_per_platform),
            "linkedin": await self._extract_real_linkedin_data(query, max_results_per_platform),
            "search_quality": "real_extraction",
            "generated_at": datetime.now().isoformat()
        }

        # Conta total de resultados
        for platform in results["platforms"]:
            platform_data = results.get(platform, {})
            if platform_data.get("results"):
                results["total_results"] += len(platform_data["results"])

        results["success"] = results["total_results"] > 0

        if results["total_results"] == 0:
            logger.error(f"❌ FALHA CRÍTICA: Nenhum dado real extraído para '{query}' - sistema configurado para APENAS dados reais")
        else:
            logger.info(f"✅ Busca REAL concluída: {results['total_results']} posts encontrados")

        return results

    async def _extract_real_youtube_data(self, query: str, max_results: int) -> Dict[str, Any]:
        """Extrai dados REAIS do YouTube usando busca no Google"""
        
        results = []
        
        try:
            # Importa dependências necessárias
            try:
                from playwright.async_api import async_playwright
                HAS_PLAYWRIGHT = True
            except ImportError:
                HAS_PLAYWRIGHT = False
            
            if not HAS_PLAYWRIGHT:
                logger.error("❌ Playwright não disponível - não é possível extrair dados reais do YouTube")
                return {
                    "success": False,
                    "platform": "youtube",
                    "results": [],
                    "total_found": 0,
                    "query": query,
                    "error": "Playwright não disponível"
                }
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # Busca vídeos do YouTube via Google
                search_url = f"https://www.google.com/search?q=site:youtube.com {query}&hl=pt-BR"
                await page.goto(search_url)
                await page.wait_for_timeout(3000)
                
                # Extrai links do YouTube
                youtube_links = await page.query_selector_all("a[href*='youtube.com/watch']")
                
                for i, link in enumerate(youtube_links[:max_results]):
                    try:
                        url = await link.get_attribute('href')
                        if not url:
                            continue
                            
                        # Extrai título do link
                        title_element = await link.query_selector("h3")
                        title = await title_element.inner_text() if title_element else f"Vídeo sobre {query}"
                        
                        # Vai para a página do vídeo para extrair dados reais
                        await page.goto(url)
                        await page.wait_for_timeout(2000)
                        
                        # Extrai dados reais do vídeo
                        video_data = await self._extract_youtube_video_data(page, url, title, query)
                        if video_data:
                            results.append(video_data)
                            
                    except Exception as e:
                        logger.debug(f"⚠️ Erro ao extrair vídeo {i}: {e}")
                        continue
                
                await browser.close()
                
        except Exception as e:
            logger.error(f"❌ Erro na extração do YouTube: {e}")
            
        return {
            "success": len(results) > 0,
            "platform": "youtube",
            "results": results,
            "total_found": len(results),
            "query": query
        }

    async def _extract_youtube_video_data(self, page, url: str, title: str, query: str) -> Dict[str, Any]:
        """Extrai dados reais de um vídeo do YouTube"""
        try:
            video_data = {
                'title': title,
                'url': url,
                'platform': 'youtube',
                'query': query
            }
            
            # Extrai visualizações
            try:
                views_element = await page.query_selector("span.view-count, #info-text span")
                if views_element:
                    views_text = await views_element.inner_text()
                    video_data['view_count'] = self._extract_number_from_text(views_text)
            except:
                pass
            
            # Extrai likes
            try:
                likes_element = await page.query_selector("#top-level-buttons-computed button[aria-label*='like'] span")
                if likes_element:
                    likes_text = await likes_element.inner_text()
                    video_data['like_count'] = self._extract_number_from_text(likes_text)
            except:
                pass
            
            # Extrai canal
            try:
                channel_element = await page.query_selector("#channel-name a, #owner-name a")
                if channel_element:
                    video_data['channel'] = await channel_element.inner_text()
            except:
                pass
            
            # Extrai descrição
            try:
                desc_element = await page.query_selector("#description-text, #meta-contents #description")
                if desc_element:
                    desc_text = await desc_element.inner_text()
                    video_data['description'] = desc_text[:200] + "..." if len(desc_text) > 200 else desc_text
            except:
                pass
            
            return video_data
            
        except Exception as e:
            logger.debug(f"⚠️ Erro ao extrair dados do vídeo: {e}")
            return None

    def _extract_number_from_text(self, text: str) -> int:
        """Extrai número de texto (ex: '1.2K' -> 1200, '500' -> 500)"""
        if not text:
            return 0
            
        text = text.strip().lower()
        
        import re
        pattern = r'(\d+(?:\.\d+)?)\s*([kmb])?'
        match = re.search(pattern, text)
        
        if match:
            number = float(match.group(1))
            suffix = match.group(2)
            
            if suffix == 'k':
                return int(number * 1000)
            elif suffix == 'm':
                return int(number * 1000000)
            elif suffix == 'b':
                return int(number * 1000000000)
            else:
                return int(number)
        
        return 0

    async def _extract_real_twitter_data(self, query: str, max_results: int) -> Dict[str, Any]:
        """Extrai dados REAIS do Twitter/X via busca no Google"""
        
        logger.error("❌ EXTRAÇÃO REAL DO TWITTER/X DESABILITADA")
        logger.error("❌ Twitter/X requer autenticação API complexa - não implementado para dados reais")
        
        return {
            "success": False,
            "platform": "twitter",
            "results": [],
            "total_found": 0,
            "query": query,
            "error": "Extração real do Twitter não implementada - requer API oficial"
        }

    async def _extract_real_instagram_data(self, query: str, max_results: int) -> Dict[str, Any]:
        """Extrai dados REAIS do Instagram via busca no Google"""
        
        logger.error("❌ EXTRAÇÃO REAL DO INSTAGRAM DESABILITADA")
        logger.error("❌ Instagram requer autenticação complexa e tem proteções anti-bot - não implementado para dados reais")
        
        return {
            "success": False,
            "platform": "instagram", 
            "results": [],
            "total_found": 0,
            "query": query,
            "error": "Extração real do Instagram não implementada - requer API oficial"
        }

    async def _extract_real_linkedin_data(self, query: str, max_results: int) -> Dict[str, Any]:
        """Extrai dados REAIS do LinkedIn via busca no Google"""
        
        logger.error("❌ EXTRAÇÃO REAL DO LINKEDIN DESABILITADA")
        logger.error("❌ LinkedIn requer autenticação e tem proteções anti-scraping - não implementado para dados reais")
        
        return {
            "success": False,
            "platform": "linkedin",
            "results": [],
            "total_found": 0,
            "query": query,
            "error": "Extração real do LinkedIn não implementada - requer API oficial"
        }

    def analyze_sentiment_trends(self, platforms_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa tendências de sentimento across platforms"""

        total_positive = 0
        total_negative = 0
        total_neutral = 0
        total_posts = 0

        platform_sentiments = {}

        for platform_name, platform_data in platforms_data.items():
            if platform_name in ['youtube', 'twitter', 'instagram', 'linkedin']:
                results = platform_data.get('results', [])

                platform_positive = 0
                platform_negative = 0
                platform_neutral = 0

                for post in results:
                    sentiment = post.get('sentiment', 'neutral')
                    if sentiment == 'positive':
                        platform_positive += 1
                        total_positive += 1
                    elif sentiment == 'negative':
                        platform_negative += 1
                        total_negative += 1
                    else:
                        platform_neutral += 1
                        total_neutral += 1

                total_posts += len(results)

                if len(results) > 0:
                    platform_sentiments[platform_name] = {
                        'positive_percentage': round((platform_positive / len(results)) * 100, 1),
                        'negative_percentage': round((platform_negative / len(results)) * 100, 1),
                        'neutral_percentage': round((platform_neutral / len(results)) * 100, 1),
                        'total_posts': len(results),
                        'dominant_sentiment': 'positive' if platform_positive > platform_negative and platform_positive > platform_neutral else 'negative' if platform_negative > platform_positive else 'neutral'
                    }

        overall_sentiment = 'neutral'
        if total_positive > total_negative and total_positive > total_neutral:
            overall_sentiment = 'positive'
        elif total_negative > total_positive and total_negative > total_neutral:
            overall_sentiment = 'negative'

        return {
            'overall_sentiment': overall_sentiment,
            'overall_positive_percentage': round((total_positive / total_posts) * 100, 1) if total_posts > 0 else 0,
            'overall_negative_percentage': round((total_negative / total_posts) * 100, 1) if total_posts > 0 else 0,
            'overall_neutral_percentage': round((total_neutral / total_posts) * 100, 1) if total_posts > 0 else 0,
            'total_posts_analyzed': total_posts,
            'platform_breakdown': platform_sentiments,
            'confidence_score': round(abs(total_positive - total_negative) / total_posts * 100, 1) if total_posts > 0 else 0,
            'analysis_timestamp': datetime.now().isoformat()
        }

    async def search_all_platforms_enhanced(self, query: str, max_results_per_platform: int = 15) -> Dict[str, Any]:
        """Busca aprimorada em todas as plataformas com dados de engajamento REAIS"""
        logger.info(f"🔍 Busca aprimorada REAL em plataformas para: {query}")
        
        # Usa o método existente como base e aprimora os dados
        base_data = await self.search_all_platforms(query, max_results_per_platform)
        
        # Adiciona métricas de engajamento específicas
        enhanced_data = base_data.copy()
        
        if "platforms" in enhanced_data:
            for platform_name, platform_data in enhanced_data["platforms"].items():
                if "results" in platform_data:
                    for result in platform_data["results"]:
                        # Adiciona métricas de engajamento calculadas
                        result["engagement_score"] = self._calculate_engagement_score(result)
                        result["viral_potential"] = self._calculate_viral_potential(result)
                        result["content_quality"] = self._assess_content_quality(result)
        
        return enhanced_data

    def identify_high_engagement_content(self, platforms_data: Dict[str, Any]) -> Dict[str, Any]:
        """Identifica conteúdo de alto engajamento (top 10% por plataforma)"""
        logger.info("📊 Identificando conteúdo de alto engajamento...")
        
        high_engagement = {
            "instagram": [],
            "youtube": [],
            "twitter": [],
            "linkedin": [],
            "avg_likes": 0,
            "avg_comments": 0,
            "avg_shares": 0,
            "threshold": 0
        }
        
        all_engagement_scores = []
        
        if "platforms" in platforms_data:
            for platform_name, platform_data in platforms_data["platforms"].items():
                if "results" in platform_data:
                    results = platform_data["results"]
                    
                    # Calcula scores de engajamento
                    engagement_scores = []
                    for result in results:
                        score = result.get("engagement_score", 0)
                        engagement_scores.append((result, score))
                        all_engagement_scores.append(score)
                    
                    # Ordena por engajamento
                    engagement_scores.sort(key=lambda x: x[1], reverse=True)
                    
                    # Pega top 10%
                    top_count = max(1, len(engagement_scores) // 10)
                    top_content = [item[0] for item in engagement_scores[:top_count]]
                    
                    high_engagement[platform_name] = top_content
        
        # Calcula métricas médias
        if all_engagement_scores:
            high_engagement["threshold"] = np.percentile(all_engagement_scores, 90) if len(all_engagement_scores) > 0 else 0
            
            # Calcula médias de likes, comentários, shares
            all_likes = []
            all_comments = []
            all_shares = []
            
            for platform_content in high_engagement.values():
                if isinstance(platform_content, list):
                    for content in platform_content:
                        if isinstance(content, dict):
                            all_likes.append(content.get("like_count", 0))
                            all_comments.append(content.get("comment_count", 0))
                            all_shares.append(content.get("shares", content.get("retweet_count", 0)))
            
            high_engagement["avg_likes"] = np.mean(all_likes) if all_likes else 0
            high_engagement["avg_comments"] = np.mean(all_comments) if all_comments else 0
            high_engagement["avg_shares"] = np.mean(all_shares) if all_shares else 0
        
        return high_engagement

    def extract_hashtag_insights(self, platforms_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai insights de hashtags e tendências"""
        logger.info("🏷️ Extraindo insights de hashtags...")
        
        hashtag_insights = {
            "trending_hashtags": [],
            "hashtag_performance": {},
            "recommended_hashtags": [],
            "hashtag_networks": {}
        }
        
        all_hashtags = []
        hashtag_engagement = defaultdict(list)
        
        if "platforms" in platforms_data:
            for platform_name, platform_data in platforms_data["platforms"].items():
                if "results" in platform_data:
                    for result in platform_data["results"]:
                        # Extrai hashtags do conteúdo
                        hashtags = result.get("hashtags", [])
                        if not hashtags:
                            # Tenta extrair do texto/caption
                            text = result.get("text", result.get("caption", ""))
                            hashtags = re.findall(r'#\w+', text)
                        
                        engagement_score = result.get("engagement_score", 0)
                        
                        for hashtag in hashtags:
                            all_hashtags.append(hashtag.lower())
                            hashtag_engagement[hashtag.lower()].append(engagement_score)
        
        # Analisa performance das hashtags
        if all_hashtags:
            hashtag_counter = Counter(all_hashtags)
            hashtag_insights["trending_hashtags"] = hashtag_counter.most_common(20)
            
            # Calcula performance média por hashtag
            for hashtag, scores in hashtag_engagement.items():
                if scores:
                    hashtag_insights["hashtag_performance"][hashtag] = {
                        "avg_engagement": np.mean(scores),
                        "usage_count": len(scores),
                        "max_engagement": max(scores),
                        "consistency": np.std(scores) if len(scores) > 1 else 0
                    }
            
            # Recomenda hashtags baseado em performance
            sorted_hashtags = sorted(
                hashtag_insights["hashtag_performance"].items(),
                key=lambda x: x[1]["avg_engagement"],
                reverse=True
            )
            hashtag_insights["recommended_hashtags"] = [
                {"hashtag": hashtag, "score": data["avg_engagement"]}
                for hashtag, data in sorted_hashtags[:10]
            ]
        
        return hashtag_insights

    def analyze_posting_patterns(self, platforms_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analisa padrões de timing de postagens"""
        logger.info("⏰ Analisando padrões de timing...")
        
        timing_patterns = {
            "best_posting_times": {},
            "day_of_week_analysis": {},
            "hourly_distribution": {},
            "seasonal_trends": {}
        }
        
        timestamps = []
        
        if "platforms" in platforms_data:
            for platform_name, platform_data in platforms_data["platforms"].items():
                if "results" in platform_data:
                    for result in platform_data["results"]:
                        timestamp_str = result.get("timestamp", result.get("created_at", result.get("published_at", "")))
                        if timestamp_str:
                            try:
                                # Tenta parsear diferentes formatos de timestamp
                                if "T" in timestamp_str:
                                    timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                                else:
                                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d")
                                
                                timestamps.append({
                                    "datetime": timestamp,
                                    "platform": platform_name,
                                    "engagement": result.get("engagement_score", 0)
                                })
                            except Exception as e:
                                logger.debug(f"Erro ao parsear timestamp {timestamp_str}: {e}")
        
        # Analisa padrões se há dados suficientes
        if timestamps:
            # Análise por hora do dia
            hourly_engagement = defaultdict(list)
            daily_engagement = defaultdict(list)
            
            for item in timestamps:
                hour = item["datetime"].hour
                day = item["datetime"].strftime("%A")
                engagement = item["engagement"]
                
                hourly_engagement[hour].append(engagement)
                daily_engagement[day].append(engagement)
            
            # Melhores horários
            timing_patterns["hourly_distribution"] = {
                hour: {
                    "avg_engagement": np.mean(scores),
                    "post_count": len(scores)
                }
                for hour, scores in hourly_engagement.items()
            }
            
            # Melhores dias da semana
            timing_patterns["day_of_week_analysis"] = {
                day: {
                    "avg_engagement": np.mean(scores),
                    "post_count": len(scores)
                }
                for day, scores in daily_engagement.items()
            }
            
            # Identifica melhores horários
            best_hours = sorted(
                timing_patterns["hourly_distribution"].items(),
                key=lambda x: x[1]["avg_engagement"],
                reverse=True
            )[:3]
            
            timing_patterns["best_posting_times"] = [
                {"hour": hour, "engagement": data["avg_engagement"]}
                for hour, data in best_hours
            ]
        
        return timing_patterns

    def _calculate_engagement_score(self, result: Dict[str, Any]) -> float:
        """Calcula score de engajamento para um post"""
        try:
            likes = result.get("like_count", 0)
            comments = result.get("comment_count", 0)
            shares = result.get("shares", result.get("retweet_count", 0))
            views = result.get("view_count", result.get("follower_count", 1000))
            
            # Converte strings para números se necessário
            if isinstance(likes, str):
                likes = int(likes.replace(",", "").replace(".", ""))
            if isinstance(comments, str):
                comments = int(comments.replace(",", "").replace(".", ""))
            if isinstance(shares, str):
                shares = int(shares.replace(",", "").replace(".", ""))
            if isinstance(views, str):
                views = int(views.replace(",", "").replace(".", ""))
            
            # Fórmula de engajamento ponderada
            engagement_score = (likes * 1.0 + comments * 2.0 + shares * 3.0) / max(views, 1) * 100
            
            return min(engagement_score, 100.0)  # Limita a 100
            
        except Exception as e:
            logger.debug(f"Erro ao calcular engagement score: {e}")
            return 0.0

    def _calculate_viral_potential(self, result: Dict[str, Any]) -> float:
        """Calcula potencial viral de um conteúdo"""
        try:
            engagement_score = result.get("engagement_score", 0)
            shares = result.get("shares", result.get("retweet_count", 0))
            comments = result.get("comment_count", 0)
            
            # Fatores que indicam potencial viral
            viral_indicators = 0
            
            # Alto número de shares
            if shares > 50:
                viral_indicators += 30
            elif shares > 20:
                viral_indicators += 20
            elif shares > 5:
                viral_indicators += 10
            
            # Alto engajamento
            if engagement_score > 5.0:
                viral_indicators += 25
            elif engagement_score > 2.0:
                viral_indicators += 15
            
            # Muitos comentários (indica discussão)
            if comments > 100:
                viral_indicators += 25
            elif comments > 50:
                viral_indicators += 15
            elif comments > 20:
                viral_indicators += 10
            
            # Presença de hashtags trending
            text = result.get("text", result.get("caption", ""))
            trending_keywords = ["viral", "trending", "breaking", "urgente", "exclusivo"]
            if any(keyword in text.lower() for keyword in trending_keywords):
                viral_indicators += 20
            
            return min(viral_indicators, 100.0)
            
        except Exception as e:
            logger.debug(f"Erro ao calcular potencial viral: {e}")
            return 0.0

    def _assess_content_quality(self, result: Dict[str, Any]) -> float:
        """Avalia qualidade do conteúdo"""
        try:
            quality_score = 0
            
            # Análise do texto/caption
            text = result.get("text", result.get("caption", result.get("title", "")))
            
            if text:
                # Comprimento adequado
                if 50 <= len(text) <= 500:
                    quality_score += 25
                elif len(text) > 500:
                    quality_score += 20
                elif len(text) > 20:
                    quality_score += 15
                
                # Presença de call-to-action
                cta_keywords = ["clique", "acesse", "saiba mais", "confira", "veja", "descubra"]
                if any(keyword in text.lower() for keyword in cta_keywords):
                    quality_score += 20
                
                # Uso de emojis (moderado)
                emoji_count = len(re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', text))
                if 1 <= emoji_count <= 5:
                    quality_score += 15
                elif emoji_count > 5:
                    quality_score += 5
                
                # Presença de hashtags relevantes
                hashtags = re.findall(r'#\w+', text)
                if 1 <= len(hashtags) <= 10:
                    quality_score += 20
                elif len(hashtags) > 10:
                    quality_score += 10
                
                # Ausência de spam
                spam_indicators = ["compre agora", "oferta limitada", "clique aqui", "ganhe dinheiro"]
                if not any(spam in text.lower() for spam in spam_indicators):
                    quality_score += 20
            
            return min(quality_score, 100.0)
            
        except Exception as e:
            logger.debug(f"Erro ao avaliar qualidade do conteúdo: {e}")
            return 0.0

# Instância global
social_media_extractor = SocialMediaExtractor()

# Função para compatibilidade
def get_social_media_extractor():
    """Retorna a instância global do social media extractor"""
    return social_media_extractor