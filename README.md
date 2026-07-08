# Web Scrapper 
Romulo Ferreira da Silva - email: romin.nf@gmail.com

Ciência de Dados-Universidade de São Paulo (USP) - Instituto de Ciências Matemáticas e de Computação

## Como utilizar:
```` bash
uv run main.py [link] [max_cuncorrency] [max_pages] 
````
## Principais pacotes.
- aiohttp (Sessions)
- asyncio (Semaphore, await)
- beautifulsoup4 (buscar tags)
- json (relatorio final)
- requests (urlparse)

Web scrapper que utiliza  asyncio , para realizar diversos fetchs em um unico site de maneira assincrona afim de encontrar links imagens e texto.
## testes
Os testes cobrem somente a parte sincrona do codigo.
````bash
uv run python -m unittest discover 
````
