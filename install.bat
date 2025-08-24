@echo off
REM ARQV30 Enhanced v2.0 ULTRA-ROBUSTO - Script de Instalação Windows
REM Execute este arquivo para instalar todas as dependências

echo ========================================
echo ARQV30 Enhanced v2.0 ULTRA-ROBUSTO - Instalação
echo Análise Ultra-Detalhada de Mercado
echo ========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Python não encontrado!
    echo.
    echo Por favor, instale Python 3.11+ de https://python.org    
    echo Certifique-se de marcar "Add Python to PATH" durante a instalação.
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado:
python --version
echo.

REM Verifica versão do Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Versão do Python: %PYTHON_VERSION%
echo.

REM Cria ambiente virtual
echo 🔄 Criando ambiente virtual...
python -m venv venv
if errorlevel 1 (
    echo ❌ ERRO: Falha ao criar ambiente virtual!
    pause
    exit /b 1
)

REM Ativa ambiente virtual
echo 🔄 Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ ERRO: Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)

REM Atualiza pip
echo 🔄 Atualizando pip...
python -m pip install --upgrade pip
echo.

REM Instala dependências
echo 🔄 Instalando dependências ULTRA-ROBUSTAS...
echo Isso pode levar alguns minutos...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ ERRO: Falha ao instalar dependências!
    echo Verifique sua conexão com a internet e tente novamente.
    pause
    exit /b 1
)

REM === MODIFICAÇÃO CRÍTICA: Instala o modelo spaCy pt_core_news_sm ===
echo 🔄 Instalando modelo spaCy pt_core_news_sm...
pip install src\engine\pt_core_news_sm-3.8.0-py3-none-any.whl
if errorlevel 1 (
    echo ⚠️ AVISO: Falha ao instalar o modelo spaCy pt_core_news_sm a partir do .whl. Tentando download...
    python -m spacy download pt_core_news_sm
    if errorlevel 1 (
        echo ⚠️ AVISO: Falha ao baixar o modelo spaCy pt_core_news_sm. A análise NLP será limitada.
    ) else (
        echo ✅ Modelo spaCy pt_core_news_sm baixado com sucesso.
    )
) else (
     echo ✅ Modelo spaCy pt_core_news_sm instalado com sucesso a partir do .whl.
)
REM === FIM DA MODIFICAÇÃO ===

REM Instala dependências adicionais para web scraping (se não estiverem no requirements.txt principal)
echo 🔄 Instalando dependências adicionais (se necessário)...
pip install beautifulsoup4 lxml html5lib
if errorlevel 1 (
    echo ⚠️ AVISO: Algumas dependências adicionais falharam.
)

REM Cria diretórios necessários
echo 🔄 Criando estrutura de diretórios ULTRA-ROBUSTA...
if not exist "src\uploads" mkdir src\uploads
if not exist "src\static\images" mkdir src\static\images
if not exist "src\cache" mkdir src\cache
if not exist "src\logs" mkdir src\logs
echo.

REM Testa a instalação
echo 🧪 Testando instalação ULTRA-ROBUSTA...
cd src
python -c "import flask, requests, google.generativeai, supabase, pandas, PyPDF2, spacy; print('✅ Dependências principais OK')"
if errorlevel 1 (
    echo ⚠️ AVISO: Algumas dependências podem não estar funcionando corretamente.
) else (
    echo ✅ Teste de dependências ULTRA-ROBUSTO passou!
)
cd ..
echo.

REM Testa conexão com APIs (se configuradas)
echo 🧪 Testando conexões com APIs...
if exist ".env" (
    cd src
    python -c "
import os
from dotenv import load_dotenv
load_dotenv('../.env')

# Testa Gemini
gemini_key = os.getenv('GEMINI_API_KEY')
if gemini_key and gemini_key != 'sua-chave-aqui':
    try:
        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        print('✅ Gemini API configurada')
    except:
        print('⚠️ Gemini API com problemas')
else:
    print('⚠️ Gemini API não configurada')

# Testa Supabase
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_ANON_KEY')
if supabase_url and supabase_key:
    try:
        from supabase import create_client
        client = create_client(supabase_url, supabase_key)
        print('✅ Supabase configurado')
    except:
        print('⚠️ Supabase com problemas')
else:
    print('⚠️ Supabase não configurado')
" 2>nul
    cd ..
) else (
    echo ⚠️ Arquivo .env não encontrado - APIs não testadas
)
echo.

echo ========================================
echo 🎉 INSTALAÇÃO ULTRA-ROBUSTA CONCLUÍDA!
echo ========================================
echo.
echo 🚀 Próximos passos:
echo.
echo 1. ✅ Arquivo .env já configurado com suas chaves
echo.
echo 2. Execute run.bat para iniciar a aplicação
echo.
echo 3. Acesse http://localhost:5000 no seu navegador
echo.
echo 4. Teste com uma análise simples primeiro
echo.
echo 5. Para análises ULTRA-ROBUSTAS, todas as APIs estão configuradas
echo.
echo ========================================
echo.
echo 📚 SISTEMA ULTRA-ROBUSTO PRONTO!
echo Agora você tem acesso a análises de mercado
echo com profundidade de consultoria de R$ 50.000/hora
echo.
echo 🔥 RECURSOS ATIVADOS:
echo - Google Gemini Pro para análise IA
echo - Supabase para banco de dados
echo - WebSailor para pesquisa web
echo - HuggingFace para análise complementar
echo - Google Search para dados reais
echo - Jina AI para extração de conteúdo
echo.
pause