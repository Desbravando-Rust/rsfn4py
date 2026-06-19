# 🦀🐍 Rust Functions for Python (rsfn4py)

[![Run Tests](https://github.com/Desbravando-Rust/rsfn4py/actions/workflows/test.yml/badge.svg)](https://github.com/Desbravando-Rust/rsfn4py/actions/workflows/test.yml)
![Release](https://github.com/Desbravando-Rust/rsfn4py/actions/workflows/release.yml/badge.svg)
![Python Versions](https://img.shields.io/pypi/pyversions/rsfn4py)

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