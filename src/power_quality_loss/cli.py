"""Interfaz de línea de comandos."""

from __future__ import annotations

import argparse
import json
from typing import Sequence

import pandas as pd

from .ieee519 import assess_percentage
from .legacy import calculate_legacy_imbalance
from .model import train_xgboost
from .quality import audit_measurements


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pqloss")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser("audit-data", help="Audita una exportación CSV")
    audit.add_argument("csv")

    row = subparsers.add_parser("legacy-row", help="Reproduce el cálculo de desbalance")
    row.add_argument("--voltages", nargs=3, type=float, required=True, metavar=("VA", "VB", "VC"))
    row.add_argument("--currents", nargs=3, type=float, required=True, metavar=("IA", "IB", "IC"))
    row.add_argument("--power-factor", type=float, required=True)

    assess = subparsers.add_parser("assess", help="Compara THD/TDD con límites suministrados")
    assess.add_argument("--voltage-thd", type=float)
    assess.add_argument("--voltage-thd-limit", type=float)
    assess.add_argument("--current-tdd", type=float)
    assess.add_argument("--current-tdd-limit", type=float)

    train = subparsers.add_parser("train", help="Entrena XGBoost")
    train.add_argument("csv")
    train.add_argument("--model-output", default="models/xgboost_model.json")
    train.add_argument("--report-output", default="reports/model-report.json")
    train.add_argument("--test-fraction", type=float, default=0.2)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)

    if args.command == "audit-data":
        result = audit_measurements(pd.read_csv(args.csv))
    elif args.command == "legacy-row":
        result = calculate_legacy_imbalance(
            args.voltages, args.currents, args.power_factor
        ).to_dict()
    elif args.command == "assess":
        pairs = (
            ("voltage_thd_pct", args.voltage_thd, args.voltage_thd_limit),
            ("current_tdd_pct", args.current_tdd, args.current_tdd_limit),
        )
        result = [
            assess_percentage(metric, measured, limit).to_dict()
            for metric, measured, limit in pairs
            if measured is not None and limit is not None
        ]
        if not result:
            raise SystemExit("Debe suministrar una medición y su límite")
    else:
        result = train_xgboost(
            args.csv,
            args.model_output,
            args.report_output,
            args.test_fraction,
        )

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
