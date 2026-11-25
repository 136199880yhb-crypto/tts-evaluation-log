import csv
import sys
from pathlib import Path

REQUIRED = {
    "test_id",
    "text_id",
    "text",
    "voice_id",
    "output_file",
    "result",
}

VALID_RESULTS = {"pass", "fail", "review"}


def validate(path):
    errors = []
    seen = set()

    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        if not reader.fieldnames:
            return ["Missing CSV header"]

        missing = REQUIRED - set(reader.fieldnames)

        if missing:
            return [f"Missing columns: {sorted(missing)}"]

        for line, row in enumerate(reader, start=2):
            test_id = row["test_id"].strip()

            if not test_id:
                errors.append(f"Line {line}: empty test_id")
            elif test_id in seen:
                errors.append(
                    f"Line {line}: duplicate test_id {test_id}"
                )

            seen.add(test_id)

            for field in ("text_id", "text", "voice_id", "output_file"):
                if not row[field].strip():
                    errors.append(f"Line {line}: empty {field}")

            result = row["result"].strip().lower()

            if result not in VALID_RESULTS:
                errors.append(f"Line {line}: invalid result {result}")

    return errors


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate.py evaluation.csv")
        sys.exit(2)

    path = Path(sys.argv[1])

    if not path.is_file():
        print(f"File not found: {path}")
        sys.exit(2)

    errors = validate(path)

    if errors:
        print("\n".join(errors))
        sys.exit(1)

    print("CSV validation passed.")
