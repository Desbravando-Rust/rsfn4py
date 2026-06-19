from __future__ import annotations

import argparse
import time
from dataclasses import dataclass
from typing import Callable

from rsfn4py import (
    validate_cnpj_python,
    validate_cnpj_rust,
    validate_cpf_python,
    validate_cpf_rust,
)


@dataclass
class BenchResult:
    documento: str
    implementacao: str
    total_validacoes: int
    tempo_segundos: float

    @property
    def throughput(self) -> float:
        if self.tempo_segundos <= 0:
            return 0.0
        return self.total_validacoes / self.tempo_segundos


def run_benchmark(func: Callable[[str], bool], casos: list[str], total_validacoes: int) -> float:
    start = time.perf_counter()
    quantidade_casos = len(casos)

    for i in range(total_validacoes):
        func(casos[i % quantidade_casos])

    end = time.perf_counter()
    return end - start


def format_num(value: float, decimals: int = 3) -> str:
    return f"{value:,.{decimals}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def print_table(title: str, headers: list[str], rows: list[list[str]]) -> None:
    print(f"\n{title}")
    print("-" * len(title))

    widths = [len(h) for h in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            widths[idx] = max(widths[idx], len(cell))

    line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    sep = "-+-".join("-" * widths[i] for i in range(len(headers)))
    print(line)
    print(sep)
    for row in rows:
        print(" | ".join(row[i].ljust(widths[i]) for i in range(len(headers))))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Benchmark de validacao CPF/CNPJ: Rust (PyO3) vs Python puro"
    )
    parser.add_argument(
        "--total-validacoes",
        type=int,
        default=100_000,
        help="Quantidade total de validacoes por cenario (default: 100000)",
    )
    args = parser.parse_args()

    total_validacoes = args.total_validacoes

    cnpj_casos = [
        "12.345.678/0001-95",
        "12345678000195",
        "12ABC34501DE35",
        "11.111.111/1111-11",
        "12.345.678/0001-00",
        "NONSENSE",
    ]

    cpf_casos = [
        "529.982.247-25",
        "52998224725",
        "111.111.111-11",
        "529.982.247-24",
        "NONSENSE",
    ]

    print("Benchmark CPF/CNPJ - Rust vs Python")
    print(f"Total de validacoes por cenario: {total_validacoes}")

    cenarios = [
        ("CNPJ", "Python", validate_cnpj_python, cnpj_casos),
        ("CNPJ", "Rust", validate_cnpj_rust, cnpj_casos),
        ("CPF", "Python", validate_cpf_python, cpf_casos),
        ("CPF", "Rust", validate_cpf_rust, cpf_casos),
    ]

    # Warmup para reduzir impacto de inicializacao/cache no primeiro run
    for _, _, func, casos in cenarios:
        run_benchmark(func, casos, 5_000)

    resultados: list[BenchResult] = []
    for documento, implementacao, func, casos in cenarios:
        tempo = run_benchmark(func, casos, total_validacoes)
        resultados.append(
            BenchResult(
                documento=documento,
                implementacao=implementacao,
                total_validacoes=total_validacoes,
                tempo_segundos=tempo,
            )
        )

    tempo_rows = [
        [
            r.documento,
            r.implementacao,
            format_num(r.tempo_segundos, 6),
        ]
        for r in resultados
    ]
    print_table(
        "Analise 1: Tempo de execucao (s)",
        ["Documento", "Implementacao", "Tempo (s)"],
        tempo_rows,
    )

    throughput_rows = [
        [
            r.documento,
            r.implementacao,
            format_num(r.throughput, 0),
        ]
        for r in resultados
    ]
    print_table(
        "Analise 2: Throughput (validacoes/segundo)",
        ["Documento", "Implementacao", "Throughput"],
        throughput_rows,
    )

    speedups: list[list[str]] = []
    for doc in ["CNPJ", "CPF"]:
        py = next(
            r for r in resultados if r.documento == doc and r.implementacao == "Python"
        )
        rs = next(
            r for r in resultados if r.documento == doc and r.implementacao == "Rust"
        )
        ganho = py.tempo_segundos / rs.tempo_segundos if rs.tempo_segundos > 0 else 0.0
        speedups.append([doc, f"{ganho:.2f}x"])

    print_table(
        "Speedup Rust sobre Python",
        ["Documento", "Ganho"],
        speedups,
    )


if __name__ == "__main__":
    main()
