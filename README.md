# 🦀🐍 Rust Functions for Python (rsfn4py)

![CI/CD Tests](https://github.com/seu-usuario/rust-services-for-python/actions/workflows/test.yml/badge.svg)
![Release](https://github.com/seu-usuario/rust-services-for-python/actions/workflows/release.yml/badge.svg)
![Python Versions](https://img.shields.io/pypi/pyversions/rust-services-for-python)

Uma coleção de módulos de alta performance escritos em **Rust** para serem consumidos nativamente em projetos **Python**, focando em processamento rápido e baixo consumo de memória.

O primeiro módulo desta biblioteca traz a validação do **Novo CNPJ Alfanumérico** (IN RFB 2.119/2022, válido a partir de julho de 2026), processado em Rust com um ganho de performance de aproximadamente **25x** em comparação à implementação em Python puro.

---

## 🚀 Recursos

- **Performance Extrema**: Algoritmos matemáticos e *parsing* de strings otimizados usando iterators do Rust.
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

O uso é idêntico a qualquer outra biblioteca Python. A função de validação automaticamente limpa a string (removendo pontos, barras e traços) e faz a validação matemática.

```python
from rust_services_for_python import validate_cnpj_rust, validate_cnpj_python

cnpj_valido = "12.345.678/0001-95"
novo_cnpj_alfanumerico = "12ABC34501DE35"
cnpj_invalido = "11.111.111/1111-11"

# Validação ultra-rápida em Rust (Recomendado para produção)
print(validate_cnpj_rust(cnpj_valido))           # Saída: True
print(validate_cnpj_rust(novo_cnpj_alfanumerico))  # Saída: True
print(validate_cnpj_rust(cnpj_invalido))         # Saída: False

# Implementação em Python puro (Para comparação ou fallback)
print(validate_cnpj_python(cnpj_valido))         # Saída: True
```

---

## ⚡ Benchmark

Em testes rodando lotes de **100.000 validações** mistas (CNPJs formatados, não formatados e alfanuméricos), a extensão em Rust apresentou uma eficiência drástica no ecossistema CPython:

| Linguagem | Tempo de Execução | Validações por Segundo |
| :--- | :--- | :--- |
| **Python Puro** | ~ 0.475s | ~ 210.000 req/s |
| **Rust (PyO3)** | **~ 0.019s** | **~ 5.250.000 req/s** |

---

## 🛠️ Setup Local e Desenvolvimento

Se você deseja clonar o repositório para contribuir ou adicionar novos serviços em Rust, siga o passo a passo abaixo.

### Pré-requisitos
- [Rust & Cargo](https://rustup.rs/) (Instalador `rustup`)
- Python 3.8+

### 1. Preparando o Ambiente

Clone o repositório e crie um ambiente virtual (venv):

```bash
git clone https://github.com/seu-usuario/rust-services-for-python.git
cd rust-services-for-python

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

---

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usá-lo, modificá-lo e distribuí-lo. Veja o arquivo `LICENSE` para mais detalhes.