# Métodos Numéricos de Zero Real: Teoria, Implementação e Comparação

Este repositório contém o artigo *"Métodos Numéricos de Zero Real: Teoria,
Implementação e Comparação"*, onde comparamos diferentes métodos numéricos para
encontrar zeros de funções. Os métodos analisados são:

- ✂️ **Bisseção**
- 🎯 **Newton-Raphson**
- 🔄 **Falsa Posição**
- 🔗 **Ponto Fixo**
- 📈 **Secante**

Além da parte teórica e dos experimentos computacionais, o projeto inclui uma
aplicação Python para visualizar esses métodos em ação.

## 📂 Estrutura do Repositório

```
 .
├── code
│   ├── app.py              # Aplicação principal
│   ├── functions.py        # Implementação dos métodos numéricos
│   ├── insights.py         # Análise dos resultados
│   ├── install.sh          # Script para instalação de dependências
│   ├── requirements.txt    # Lista de dependências do Python
│   ├── results.csv         # Resultados dos testes
│   ├── run.sh              # Script para executar a aplicação
│   └── ui.py               # Interface gráfica para visualização
├── config
│   ├── config.tex      # Configuração do artigo em LaTeX
│   └── includes.tex    # Inclusões gerais
├── fig
│   ├── benchmark.png           # Comparação de desempenho
│   ├── demonstracao-app.png    # Demonstração da aplicação
│   ├── bissecao.png            # Demonstração do método da Bisseção
│   ├── newton-raphson.png      # Demonstração do método de Newton-Raphson
│   ├── ponto-falso.png         # Demonstração do método da Falsa Posição
│   ├── ponto-fixo.png          # Demonstração do método do Ponto Fixo
│   └── secante.png             # Demonstração do método da Secante
├── sections
│   ├── 01-introducao.tex           # Introdução
│   ├── 02-fundamentos-teoricos.tex # Fundamentos Teóricos
│   ├── 03-implementacao.tex        # Implementação Computacional
│   ├── 04-results.tex              # Resultados e Discussão
│   └── 05-conclusao.tex            # Conclusão
├── latexide    # Ambiente de trabalho para LaTeX
├── main.pdf    # Artigo compilado
├── main.tex    # Documento principal do artigo
├── ref.bib     # Referências bibliográficas
├── style.cls   # Estilo do documento em LaTeX
└── texcomp     # Script para compilação
```

## 💾 Como Testar a Aplicação

Para executar a aplicação e visualizar os métodos em ação:

1. Acesse o diretório `code`:
   ```sh
   cd code
   ```
2. Instale as dependências necessárias:
   ```sh
   ./install.sh
   ```
3. Execute a aplicação:
   ```sh
   ./run.sh
   ```

A interface gráfica permitirá visualizar cada método aplicando-o a diferentes
funções e parâmetros.

## 📄 Como Compilar e Editar o Artigo

Para compilar o artigo, utilize o script `texcomp`:
```sh
./texcomp main.tex
```
Isso gerará o arquivo `main.pdf` atualizado.

Para editar e recompilar automaticamente o artigo no Neovim, utilize:
```sh
./latexide main.tex
```
Isso abrirá o editor e ativará a recompilação automática sempre que houver
alterações em qualquer arquivo `.tex`.

---

📖 Para mais detalhes sobre a implementação, consulte o artigo (`main.pdf`).

## 📜 Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo
[`LICENSE`](./LICENSE) para mais detalhes.
