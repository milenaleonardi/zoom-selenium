# Webscraping Zoom.com.br com Selenium

Este projeto realiza webscraping no site Zoom.com.br utilizando Selenium para automatizar a busca de produtos, aplicar filtros e coletar resultados de múltiplas páginas.

## Pré-requisitos

- Python 3.8+
- Microsoft Edge instalado
- [Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) compatível com sua versão do Edge
- Ambiente virtual Python (recomendado)

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/milenaleonardi/zoom-selenium.git
   cd zoom-selenium
   ```
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install selenium
   ```

## Como rodar

1. Certifique-se de que o Edge WebDriver está instalado e no PATH.
2. Execute o script principal:
   ```bash
   python main.py
   ```
3. O script irá:
   - Abrir o site do Zoom
   - Pesquisar por "bike"
   - Alterar o filtro de busca para "Melhor Avaliados"
   - Coletar os resultados das 3 primeiras páginas
   - Exibir os títulos e links dos produtos encontrados

## Observações
- O site Zoom pode alterar seus seletores ou estrutura a qualquer momento. Caso o script pare de funcionar, inspecione os elementos e ajuste os seletores no código.
- O uso de webscraping deve respeitar os Termos de Uso do site.

## Licença
MIT
