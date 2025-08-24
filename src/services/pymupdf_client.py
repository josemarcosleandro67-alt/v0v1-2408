#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - PyMuPDF Client
Cliente para extração de PDF usando PyMuPDF
"""

import os
import logging
import requests
import tempfile
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class PyMuPDFClient:
    """Cliente para extração de PDF usando PyMuPDF"""
    
    def __init__(self):
        """Inicializa cliente PyMuPDF"""
        try:
            import fitz  # PyMuPDF
            self.available = True
            logger.info("✅ PyMuPDF Client disponível")
        except ImportError:
            self.available = False
            logger.warning("⚠️ PyMuPDF não instalado")
    
    def is_available(self) -> bool:
        """Verifica se PyMuPDF está disponível"""
        return self.available
    
    def extract_from_url(self, url: str) -> Dict[str, Any]:
        """Extrai texto de PDF via URL"""
        
        if not self.available:
            return {'success': False, 'error': 'PyMuPDF não disponível'}
        
        try:
            import fitz
            
            # Baixa PDF
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Salva temporariamente
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                temp_file.write(response.content)
                temp_path = temp_file.name
            
            try:
                # Abre PDF com PyMuPDF
                doc = fitz.open(temp_path)
                text = ""
                
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    page_text = page.get_text()
                    if page_text:
                        text += page_text + "\n"
                
                doc.close()
                
                return {
                    'success': True,
                    'text': text,
                    'metadata': {
                        'pages': len(doc),
                        'url': url,
                        'extractor': 'PyMuPDF'
                    }
                }
                
            finally:
                # Remove arquivo temporário
                try:
                    os.unlink(temp_path)
                except:
                    pass
                    
        except Exception as e:
            logger.error(f"❌ Erro PyMuPDF: {e}")
            return {'success': False, 'error': str(e)}

# Instância global
pymupdf_client = PyMuPDFClient()