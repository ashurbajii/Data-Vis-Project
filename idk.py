import pandas as pd
import re

output_file = "data_quality_issues_report.xlsx"

valid_location_ids = zones["Location ID"]

calc_total = (
    td["fare_amount"].fillna(0) +
    td["extra"].fillna(0) +
    td["mta_tax"].fillna(0) +
    td["tip_amount"].fillna(0) +
    td["tolls_amount"].fillna(0) +
    td["improvement_surcharge"].fillna(0) +
    td["congestion_surcharge"].fillna(0) +
    td["Airport_fee"].fillna(0) +
    td["cbd_congestion_fee"].fillna(0)
)

issues = {
    "Invalid VendorID": ~td["VendorID"].isin([1, 2, 6, 7]),
    "Missing VendorID": td["VendorID"].isna(),

    "Missing pickup/dropoff time": td["tpep_pickup_datetime"].isna() | td["tpep_dropoff_datetime"].isna(),
    "Invalid pickup date": (td["tpep_pickup_datetime"] < pd.Timestamp("2025-01-01")) | (td["tpep_pickup_datetime"] >= pd.Timestamp("2025-04-01")),
    "Invalid dropoff date": (td["tpep_dropoff_datetime"] < pd.Timestamp("2025-01-01")) | (td["tpep_dropoff_datetime"] >= pd.Timestamp("2025-04-01")),
    "Dropoff before pickup": td["tpep_dropoff_datetime"] <= td["tpep_pickup_datetime"],

    "Missing passenger count": td["passenger_count"].isna(),
    "Zero passenger count": td["passenger_count"] == 0,
    "Too many passengers": td["passenger_count"] >= 7,
    "Negative passengers": td["passenger_count"] < 0,

    "Missing trip distance": td["trip_distance"].isna(),
    "Zero trip distance": td["trip_distance"] == 0,
    "Negative trip distance": td["trip_distance"] < 0,
    "Unrealistic trip distance": td["trip_distance"] >= 80,

    "Invalid RatecodeID": (~td["RatecodeID"].isin([1, 2, 3, 4, 5, 6, 99])) & td["RatecodeID"].notna(),
    "Missing RatecodeID": td["RatecodeID"].isna(),

    "Invalid store flag": (~td["store_and_fwd_flag"].isin(["Y", "N"])) & td["store_and_fwd_flag"].notna(),
    "Missing store flag": td["store_and_fwd_flag"].isna(),

    "Missing PULocationID": td["PULocationID"].isna(),
    "Missing DOLocationID": td["DOLocationID"].isna(),
    "Invalid PULocationID": (~td["PULocationID"].isin(valid_location_ids)) & td["PULocationID"].notna(),
    "Invalid DOLocationID": (~td["DOLocationID"].isin(valid_location_ids)) & td["DOLocationID"].notna(),

    "Missing payment type": td["payment_type"].isna(),
    "Invalid payment type": (~td["payment_type"].isin([0, 1, 2, 3, 4, 5, 6])) & td["payment_type"].notna(),

    "Missing fare amount": td["fare_amount"].isna(),
    "Negative fare amount": td["fare_amount"] < 0,

    "Missing extra": td["extra"].isna(),
    "Negative extra": td["extra"] < 0,

    "Missing mta tax": td["mta_tax"].isna(),
    "Negative mta tax": td["mta_tax"] < 0,

    "Invalid tip amount": (td["tip_amount"] < 0) | ((td["payment_type"] != 1) & (td["tip_amount"] > 0)),

    "Missing improvement surcharge": td["improvement_surcharge"].isna(),
    "Invalid improvement surcharge": td["improvement_surcharge"] != 1,

    "Missing congestion surcharge": td["congestion_surcharge"].isna(),
    "Negative congestion surcharge": td["congestion_surcharge"] < 0,

    "Missing total amount": td["total_amount"].isna(),
    "Invalid total amount": (td["total_amount"] < 0) | (abs(td["total_amount"] - calc_total) > 0.01),

    "Missing airport fee": td["Airport_fee"].isna(),
    "Invalid airport fee": (td["Airport_fee"] < 0) | ((td["Airport_fee"] != 0) & (~td["PULocationID"].isin([1, 132]))),

    "Missing cbd fee": td["cbd_congestion_fee"].isna(),
    "Negative cbd fee": td["cbd_congestion_fee"] < 0,
}

summary_rows = []

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    for issue_name, mask in issues.items():
        mask = mask.fillna(False)
        count = int(mask.sum())

        summary_rows.append({
            "Issue": issue_name,
            "Total rows with issue": count
        })

        sample = td.loc[mask].head(5).copy()

        safe_sheet_name = re.sub(r"[\[\]\:\*\?\/\\]", "", issue_name)[:31]

        info = pd.DataFrame({
            "Issue": [issue_name],
            "Total rows with issue": [count]
        })

        info.to_excel(writer, sheet_name=safe_sheet_name, index=False, startrow=0)
        sample.to_excel(writer, sheet_name=safe_sheet_name, index=False, startrow=4)

    summary = pd.DataFrame(summary_rows).sort_values(
        by="Total rows with issue",
        ascending=False
    )

    summary.to_excel(writer, sheet_name="Summary", index=False)

print(f"Excel report created: {output_file}")