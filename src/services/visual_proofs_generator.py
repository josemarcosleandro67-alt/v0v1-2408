
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Visual Proofs Generator
Sistema Completo de Geração de Provas Visuais Devastadoras
"""

import logging
import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
from services.ai_manager import ai_manager
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class VisualProofsGenerator:
    """Gerador de Provas Visuais Devastadoras"""

    def __init__(self, ai_manager_instance=None):
        """Inicializa o gerador"""
        self.logger = logging.getLogger(__name__)
        self.ai_manager = ai_manager_instance or ai_manager

    def generate_comprehensive_proofs(self, concepts, avatar_data, context_data) -> Dict[str, Any]:
        """Gera provas visuais compreensivas"""
        try:
            self.logger.info(f"🎯 Gerando provas visuais para {len(concepts)} conceitos")
            
            proofs_arsenal = []
            
            for i, concept in enumerate(concepts[:10]):  # Limita a 10 conceitos
                try:
                    proof = self._create_visual_proof(concept, avatar_data, context_data, i + 1)
                    if proof:
                        proofs_arsenal.append(proof)
                        salvar_etapa(f"prova_visual_{i+1}", proof, categoria="provas_visuais")
                        
                except Exception as e:
                    self.logger.error(f"❌ Erro ao criar prova {i+1}: {e}")
                    continue
            
            return {
                'provas_visuais_arsenal': proofs_arsenal,
                'total_proofs': len(proofs_arsenal),
                'concepts_processed': len(concepts),
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'success_rate': f"{len(proofs_arsenal)}/{len(concepts[:10])}"
                }
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro na geração de provas visuais: {e}")
            salvar_erro("visual_proofs_generation", str(e))
            return self._generate_emergency_proofs(concepts, avatar_data)

    def _create_visual_proof(self, concept: str, avatar_data: Dict[str, Any], context_data: Dict[str, Any], proof_number: int) -> Dict[str, Any]:
        """Cria uma prova visual individual"""
        
        prompt = f"""
# VOCÊ É O DIRETOR SUPREMO DE EXPERIÊNCIAS TRANSFORMADORAS

Crie uma PROVI (Prova Visual Instantânea) devastadoramente eficaz para o conceito: "{concept}"

## CONTEXTO:
- **Conceito Alvo**: {concept}
- **Número da PROVI**: {proof_number}
- **Segmento**: {context_data.get('segmento', 'negócios')}

## AVATAR ALVO:
- **Principais Dores**: {self._safe_get_list(avatar_data, 'dores_viscerais', ['Dor não identificada'])[:3]}
- **Desejos Principais**: {self._safe_get_list(avatar_data, 'desejos_secretos', ['Desejo não identificado'])[:3]}

## INSTRUÇÕES:
Crie uma PROVI que demonstre visualmente este conceito de forma IRREFUTÁVEL.

🎯 FÓRMULA DA PROVI:
1. **SETUP** (30s): Preparação que cria expectativa
2. **EXECUÇÃO** (60-90s): Demonstração com tensão crescente  
3. **CLÍMAX** (15s): Momento exato do "AHA!"
4. **BRIDGE** (30s): Conexão direta com a vida do avatar

RETORNE JSON:

```json
{{
  "nome": "PROVI {proof_number}: Nome Impactante",
  "conceito_alvo": "{concept}",
  "categoria": "Destruidora/Criadora/Instaladora/Prova",
  "prioridade": "Crítica/Alta/Média",
  "objetivo_psicologico": "Mudança mental específica desejada",
  "experimento": "Descrição detalhada do experimento físico",
  "analogia_perfeita": "Assim como X acontece, você Y",
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
    "abertura": "Frase de abertura",
    "durante": "Frase durante tensão",
    "revelacao": "Frase no momento AHA",
    "ancoragem": "Frase que fica na memória"
  }}
}}
```
"""

        try:
            response = self.ai_manager.generate_analysis(prompt)
            if response:
                return self._process_proof_response(response, concept, proof_number)
            else:
                return self._generate_fallback_proof(concept, proof_number)
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao gerar prova {proof_number}: {e}")
            return self._generate_fallback_proof(concept, proof_number)

    def _process_proof_response(self, response: str, concept: str, proof_number: int) -> Dict[str, Any]:
        """Processa resposta da IA para extrair JSON"""
        try:
            # Tenta extrair JSON da resposta
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.rfind("```")
                if end > start:
                    json_text = response[start:end].strip()
                    proof_data = json.loads(json_text)
                    return proof_data
            
            # Fallback: tenta encontrar JSON em qualquer lugar
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_text = json_match.group(0)
                proof_data = json.loads(json_text)
                return proof_data
                
            # Se não conseguir extrair, cria estrutura básica
            return self._generate_fallback_proof(concept, proof_number)
            
        except json.JSONDecodeError as e:
            self.logger.error(f"❌ Erro ao parsear JSON da prova {proof_number}: {e}")
            return self._generate_fallback_proof(concept, proof_number)
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar resposta da prova {proof_number}: {e}")
            return self._generate_fallback_proof(concept, proof_number)

    def _generate_fallback_proof(self, concept: str, proof_number: int) -> Dict[str, Any]:
        """Gera prova de fallback quando a IA falha"""
        return {
            'nome': f'PROVI {proof_number}: {concept[:30]}...',
            'conceito_alvo': concept,
            'categoria': 'Prova de Conceito',
            'prioridade': 'Alta',
            'objetivo_psicologico': f'Demonstrar a importância de {concept}',
            'experimento': f'Demonstração visual para provar {concept}',
            'analogia_perfeita': f'Assim como este experimento mostra, {concept} é fundamental',
            'roteiro_completo': {
                'setup': 'Preparação da demonstração',
                'execucao': 'Execução do experimento',
                'climax': 'Revelação do resultado',
                'bridge': 'Aplicação na vida real'
            },
            'materiais': ['Materiais básicos', 'Equipamento simples'],
            'variacoes': {
                'online': 'Versão adaptada para vídeo',
                'grande_publico': 'Versão para auditório',
                'intimista': 'Versão para grupo pequeno'
            },
            'plano_b': 'Explicação verbal caso experimento falhe',
            'frases_impacto': {
                'abertura': f'Vamos provar que {concept} é real',
                'durante': 'Observe o que acontece...',
                'revelacao': 'Voilà! A prova está aqui!',
                'ancoragem': f'{concept} é inegável'
            },
            'fallback': True,
            'generated_at': datetime.now().isoformat()
        }

    def _safe_get_list(self, data, key, default):
        """Safely get list data from dict"""
        try:
            if not isinstance(data, dict):
                return default
            value = data.get(key, default)
            if isinstance(value, list):
                return value
            return default
        except Exception:
            return default

    def _generate_emergency_proofs(self, concepts, avatar_data) -> Dict[str, Any]:
        """Gera provas de emergência quando tudo falha"""
        emergency_proofs = []
        
        for i, concept in enumerate(concepts[:5]):
            emergency_proof = {
                'nome': f'PROVI EMERGÊNCIA {i+1}: {concept[:20]}',
                'conceito_alvo': concept,
                'categoria': 'Emergência',
                'prioridade': 'Crítica',
                'status': 'emergency_generation',
                'experimento': f'Demonstração básica de {concept}',
                'objetivo': 'Manter funcionamento do sistema'
            }
            emergency_proofs.append(emergency_proof)
        
        return {
            'provas_visuais_arsenal': emergency_proofs,
            'total_proofs': len(emergency_proofs),
            'status': 'emergency_mode',
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'mode': 'emergency',
                'reason': 'AI generation failed'
            }
        }

# Instância global
visual_proofs_generator = VisualProofsGenerator()
