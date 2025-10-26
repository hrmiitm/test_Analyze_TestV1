#!/usr/bin/env python3
"""
Data Analysis Script
Reads data.csv and performs revenue analysis and emits JSON to stdout.
"""

import pandas as pd
import json
import sys


def main():
    try:
        df = pd.read_csv("data.csv")
    except FileNotFoundError:
        print(json.dumps({"error": "data.csv not found"}))
        sys.exit(1)

    # Ensure the Revenue column exists and is numeric
    if "Revenue" not in df.columns:
        print(json.dumps({"error": "Revenue column missing"}))
        sys.exit(1)

    df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce").fillna(0)

    # Total revenue (fixed variable name and ensured numeric conversion)
    total_revenue = df["Revenue"].sum()

    # Average revenue by region and product
    region_revenue = df.groupby("Region")["Revenue"].mean().to_dict()
    product_revenue = df.groupby("Product")["Revenue"].mean().to_dict()

    # Top performing region (safe for empty DF)
    top_region = None
    if len(df) > 0:
        try:
            top_region = df.groupby("Region")["Revenue"].sum().idxmax()
        except Exception:
            top_region = None

    results = {
        "total_revenue": float(total_revenue),
        "avg_revenue_by_region": {k: float(v) for k, v in region_revenue.items()},
        "avg_revenue_by_product": {k: float(v) for k, v in product_revenue.items()},
        "top_region": top_region,
        "total_records": int(len(df)),
    }

    # Print JSON to stdout so CI can redirect to result.json
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
