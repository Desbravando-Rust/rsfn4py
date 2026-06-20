# 🦀🐍 Rust Functions for Python (rsfn4py)

[![Run Tests](https://github.com/Desbravando-Rust/rsfn4py/actions/workflows/test.yml/badge.svg)](https://github.com/Desbravando-Rust/rsfn4py/actions/workflows/test.yml)
![Release](https://github.com/Desbravando-Rust/rsfn4py/actions/workflows/release.yml/badge.svg)
![Python Versions](https://img.shields.io/pypi/pyversions/rsfn4py.svg?cacheSeconds=60)

Uma coleção de módulos de alta performance escritos em **Rust** para serem consumidos nativamente em projetos **Python**, focando em processamento rápido e baixo consumo de memória.

O primeiro módulo desta biblioteca traz validação de **CNPJ** (incluindo o novo formato alfanumérico da IN RFB 2.119/2022, válido a partir de julho de 2026) e **CPF**, processados em Rust e expostos para Python com foco em alto throughput.

---

## 🚀 Recursos

- **Performance Extrema**: Algoritmos matemáticos e *parsing* de strings otimizados usando iterators do Rust.
- **Cobertura de Documentos Fiscais**: Validação de CNPJ (numérico e alfanumérico) e CPF, com tratamento de máscara e entradas inválidas.
- **Novo Padrão RFB**: Suporte nativo ao cálculo de DV (Dígito Verificador) do CNPJ utilizando a tabela ASCII, aceitando tanto os CNPJs antigos (somente números) quanto o novo formato alfanumérico.
- **Integração PyO3**: A biblioteca é exportada como um C-Extension (`cdylib`), funcionando como um pacote Python comum sem necessidade de configurações complexas por parte de quem a utiliza.
- **Fallback em Python**: Inclui a mesma implementação em Python puro para casos de teste, comparação ou ambientes restritos.

---

## 📦 Instalação

Você pode instalar o pacote diretamente via `pip`:

```bash
pip install rsfn4py
```

*(O pacote já distribui wheels pré-compilados para Linux, macOS e Windows nas versões mais recentes do Python).*

---

## 💻 Como Usar

O uso é idêntico a qualquer outra biblioteca Python. As funções de validação limpam a entrada e aplicam o cálculo de DV para cada documento.

```python
from rsfn4py import (
	validate_cnpj_rust,
	validate_cnpj_python,
	validate_cpf_rust,
	validate_cpf_python,
)

cnpj_valido = "12.345.678/0001-95"
novo_cnpj_alfanumerico = "12ABC34501DE35"
cnpj_invalido = "11.111.111/1111-11"

cpf_valido = "529.982.247-25"
cpf_invalido = "111.111.111-11"

# Validação ultra-rápida em Rust (Recomendado para produção)
print(validate_cnpj_rust(cnpj_valido))           # Saída: True
print(validate_cnpj_rust(novo_cnpj_alfanumerico))  # Saída: True
print(validate_cnpj_rust(cnpj_invalido))         # Saída: False

# Implementação em Python puro (Para comparação ou fallback)
print(validate_cnpj_python(cnpj_valido))         # Saída: True

# CPF em Rust e Python
print(validate_cpf_rust(cpf_valido))             # Saída: True
print(validate_cpf_rust(cpf_invalido))           # Saída: False
print(validate_cpf_python(cpf_valido))           # Saída: True
```

---

## 🪪 Validação de CPF

O **CPF** (Cadastro de Pessoas Físicas) é o documento de identificação fiscal de pessoas físicas no Brasil, composto por 11 dígitos numéricos, sendo os dois últimos dígitos verificadores.

### Exemplos de uso

```python
from rsfn4py import validate_cpf_rust, validate_cpf_python

# Aceita entrada com ou sem máscara (pontos e traço)
validate_cpf_rust("529.982.247-25")  # True  — CPF válido com máscara
validate_cpf_rust("52998224725")     # True  — CPF válido sem máscara
validate_cpf_rust("529.982.247-26")  # False — Dígito verificador inválido
validate_cpf_rust("111.111.111-11")  # False — Sequência conhecidamente inválida

# Fallback em Python puro
validate_cpf_python("529.982.247-25")  # True
```

### Algoritmo de validação do CPF

1. Remove a máscara (pontos e traço), ficando com 11 dígitos.
2. Rejeita sequências com todos os dígitos iguais (ex.: `111.111.111-11`).
3. **Primeiro dígito verificador**: multiplica os 9 primeiros dígitos pelos pesos 10 a 2, soma os produtos, calcula o resto da divisão por 11 e aplica a regra: resto < 2 → dígito = 0, senão dígito = 11 − resto.
4. **Segundo dígito verificador**: repete o processo com os 10 primeiros dígitos e pesos 11 a 2.
5. Compara os dígitos calculados com os dois últimos da entrada.

---

## 🏢 Validação de CNPJ

O **CNPJ** (Cadastro Nacional da Pessoa Jurídica) é o documento de identificação fiscal de empresas no Brasil. Possui 14 caracteres, sendo os dois últimos dígitos verificadores.

A partir de **julho de 2026**, a Receita Federal passa a emitir CNPJs no novo formato **alfanumérico** (IN RFB 2.119/2022). Esta biblioteca suporta ambos os formatos simultaneamente.

### Exemplos de uso

```python
from rsfn4py import validate_cnpj_rust, validate_cnpj_python

# Formato numérico tradicional — com e sem máscara
validate_cnpj_rust("12.345.678/0001-95")   # True  — CNPJ numérico com máscara
validate_cnpj_rust("12345678000195")        # True  — CNPJ numérico sem máscara
validate_cnpj_rust("11.111.111/1111-11")   # False — Sequência inválida

# Novo formato alfanumérico (IN RFB 2.119/2022, a partir de julho de 2026)
validate_cnpj_rust("12ABC34501DE35")        # True  — Exemplo oficial SERPRO sem máscara
validate_cnpj_rust("12.ABC.345/01DE-35")   # True  — Exemplo oficial SERPRO com máscara

# Fallback em Python puro
validate_cnpj_python("12.345.678/0001-95") # True
```

### Estrutura do CNPJ

| Posições | Conteúdo | Formato antigo | Novo formato (jul/2026) |
| :---: | :--- | :---: | :---: |
| 1–8 | Raiz (empresa) | Numérico | **Alfanumérico** |
| 9–12 | Ordem (filial) | Numérico | **Alfanumérico** |
| 13–14 | Dígitos verificadores | Numérico | Numérico |

Os CNPJs existentes (apenas numéricos) permanecem válidos. O formato alfanumérico será emitido somente para novas inscrições a partir de julho de 2026. Os dois formatos coexistirão indefinidamente.

### Algoritmo de validação do CNPJ (numérico e alfanumérico)

O cálculo dos dígitos verificadores segue o algoritmo oficial do SERPRO, adaptado para suportar letras:

1. Remove a máscara (pontos, barra e traço).
2. Converte cada caractere para seu valor numérico: dígitos valem seu próprio valor (0–9); letras valem seu código ASCII menos 48 (A=10, B=11, …, Z=35).
3. **Primeiro dígito verificador**: aplica os pesos `[5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]` sobre os 12 primeiros caracteres convertidos. Soma os produtos, calcula o resto da divisão por 11: resto < 2 → dígito = 0, senão dígito = 11 − resto.
4. **Segundo dígito verificador**: aplica os pesos `[6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]` sobre os 12 primeiros caracteres convertidos mais o primeiro dígito calculado. Mesma regra de resto.
5. Compara os dígitos calculados com os dois últimos da entrada.

### Exemplo de cálculo — CNPJ alfanumérico `12ABC34501DE35` (SERPRO)

**Conversão dos caracteres** (`12ABC34501DE`):

| Char | 1 | 2 | A | B | C | 3 | 4 | 5 | 0 | 1 | D | E |
| :---: | - | - | -- | -- | -- | - | - | - | - | - | -- | -- |
| Valor | 1 | 2 | 10 | 11 | 12 | 3 | 4 | 5 | 0 | 1 | 13 | 14 |

**Primeiro dígito verificador**:

| Pesos | 5 | 4 | 3 | 2 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
| :--- | - | - | -- | -- | --- | -- | -- | -- | - | - | -- | -- |
| Produto | 5 | 8 | 30 | 22 | 108 | 24 | 28 | 30 | 0 | 4 | 39 | 28 |

Somatório: **459** → Resto de 459 ÷ 11 = **8** → Dígito = 11 − 8 = **3**

**Segundo dígito verificador**:

| Pesos | 6 | 5 | 4 | 3 | 2 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |
| :--- | - | - | -- | -- | -- | - | - | - | -- | - | - | -- | - |
| (inclui o primeiro dígito 3 na última posição) | | | | | | | | | | | | | |

Somatório: **424** → Resto de 424 ÷ 11 = **6** → Dígito = 11 − 6 = **5**

**Resultado**: `12.ABC.345/01DE-`**35** ✅

---

## ⚡ Benchmark

Executando `make bench` com **100.000 validações por cenário** (CPF e CNPJ), os resultados recentes foram:

**Análise 1: Tempo de execução (s)**

| Documento | Python | Rust |
| :--- | ---: | ---: |
| CNPJ | 0,684318s | **0,063321s** |
| CPF | 0,713108s | **0,039088s** |

**Análise 2: Throughput (validações/segundo)**

| Documento | Python | Rust |
| :--- | ---: | ---: |
| CNPJ | 146.131/s | **1.579.264/s** |
| CPF | 140.231/s | **2.558.310/s** |

**Speedup Rust sobre Python**

| Documento | Ganho |
| :--- | ---: |
| CNPJ | **10,81x** |
| CPF | **18,24x** |

---

## 🛠️ Setup Local e Desenvolvimento

Se você deseja clonar o repositório para contribuir ou adicionar novos serviços em Rust, siga o passo a passo abaixo.

### Pré-requisitos
- [Rust & Cargo](https://rustup.rs/) (Instalador `rustup`)
- Python 3.8+

### 1. Preparando o Ambiente

Clone o repositório e crie um ambiente virtual (venv):

```bash
git clone https://github.com/Desbravando-Rust/rsfn4py.git
cd rsfn4py

python -m venv .venv
source .venv/bin/activate  # No Windows use: .venv\Scripts\activate
```

### 2. Instalando Dependências de Build

Utilizamos o **Maturin** como *build system* para compilar o código Rust e linká-lo ao Python.

```bash
pip install -U pip pytest maturin
```

### 3. Compilando o Código Rust Localmente

Para compilar o módulo C-Extension de forma transparente e já instalá-lo no seu `.venv`, basta rodar:

```bash
maturin develop --release
```
*O parâmetro `--release` aplica as otimizações completas do compilador Rust. Se omitido, a compilação será mais rápida, porém a execução será mais lenta (modo debug).*

### 4. Executando os Testes

Com os bindings instalados localmente, execute o `pytest` para validar o comportamento do módulo nativo contra os casos de teste:

```bash
pytest -v tests/
```

### 5. Executando Benchmark (CPF + CNPJ)

O projeto possui um alvo pronto no `Makefile` para comparar implementacoes Rust (PyO3) e Python puro nas validacoes de CPF e CNPJ, com duas analises:

1. Tempo de execucao total.
2. Throughput (validacoes por segundo).

Execucao padrao (100.000 validacoes por cenario):

```bash
make bench
```

Executar com outro volume:

```bash
make bench TOTAL_VALIDACOES=500000
```

Exemplo de saida:

```text
Benchmark CPF/CNPJ - Rust vs Python
Total de validacoes por cenario: 100000

Analise 1: Tempo de execucao (s)
--------------------------------
Documento | Implementacao | Tempo (s)
----------+---------------+----------
CNPJ      | Python        | 0,684318
CNPJ      | Rust          | 0,063321
CPF       | Python        | 0,713108
CPF       | Rust          | 0,039088

Analise 2: Throughput (validacoes/segundo)
------------------------------------------
Documento | Implementacao | Throughput
----------+---------------+-----------
CNPJ      | Python        | 146.131
CNPJ      | Rust          | 1.579.264
CPF       | Python        | 140.231
CPF       | Rust          | 2.558.310
```

---

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usá-lo, modificá-lo e distribuí-lo. Veja o arquivo `LICENSE` para mais detalhes.
