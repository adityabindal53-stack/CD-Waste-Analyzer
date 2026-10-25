import csv
import os

print("========================================")
print("      C&D WASTE ANALYZER")
print("========================================")
print("Starting C&D Waste Analyzer...")

input_file = "waste_logs.csv"
output_file = "final_analysis.txt"

zone_totals = {}
categories = set()
total_volume = 0
total_recycled = 0
valid_records = 0

try:
    if not os.path.exists(input_file):
        raise FileNotFoundError

    with open(input_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        required_columns = {
            "Date", "Zone", "Site_ID",
            "Category", "Volume", "Recycled"
        }

        if not reader.fieldnames or not required_columns.issubset(reader.fieldnames):
            raise ValueError("CSV headings are missing or incorrect.")

        for row in reader:
            try:
                zone = row["Zone"].strip()
                category = row["Category"].strip()
                site_id = row["Site_ID"].strip()
                volume = float(row["Volume"])
                recycled = float(row["Recycled"])

                if not zone or not category or not site_id:
                    raise ValueError

                if volume < 0 or recycled < 0 or recycled > volume:
                    raise ValueError

                zone_totals[zone] = zone_totals.get(zone, 0) + volume
                categories.add(category)
                total_volume += volume
                total_recycled += recycled
                valid_records += 1

            except (ValueError, TypeError):
                print("Warning: Skipping an invalid CSV row.")

    if valid_records == 0:
        raise ValueError("No valid records found.")

    percentage = (
        total_recycled / total_volume * 100
        if total_volume > 0 else 0
    )

    with open(output_file, "w", encoding="utf-8") as report:
        report.write("C&D WASTE ANALYSIS REPORT\n")
        report.write("=========================\n\n")
        report.write(f"Valid records processed: {valid_records}\n")
        report.write(f"Total recorded volume: {total_volume:.2f}\n")
        report.write(f"Total recycled amount: {total_recycled:.2f}\n")
        report.write(f"Recycled percentage: {percentage:.2f}%\n\n")

        report.write("ZONE-WISE TOTALS\n")
        report.write("----------------\n")
        for zone, volume in zone_totals.items():
            report.write(f"{zone}: {volume:.2f}\n")

        report.write("\nUNIQUE WASTE CATEGORIES\n")
        report.write("----------------------\n")
        for category in sorted(categories):
            report.write(f"{category}\n")

        report.write(
            "\nNote: Input units were not specified.\n"
        )
        report.write(
            "The 20,000 sq.m threshold and 5% recycled-content "
            "target cannot be verified from the available columns.\n"
        )

    print(f"Valid records processed: {valid_records}")
    print(f"Report successfully saved as {output_file}")
    print("Analysis completed successfully!")

except FileNotFoundError:
    print("Error: waste_logs.csv not found.")
    print("Keep both files in the same folder.")

except (ValueError, OSError, csv.Error) as error:
    print(f"Error: Could not process the data. {error}")