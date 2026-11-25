# Stop Guessing Which AI Voice Take Is Better: A Reproducible TTS Evaluation Log

A voice that sounds impressive in a 10-second demo is not necessarily the right voice for a real project.

The problem is that most informal TTS comparisons are difficult to reproduce. People change the text, switch voices, adjust settings, and then decide which result sounds better. Several variables change at once, so the conclusion is nearly useless.

This repository provides a small, reproducible way to document and compare AI-generated voiceovers.

It does not rank voice providers or claim that subjective listening can be reduced to one objective score.

## What this repository does

- Records the exact text used for each generation.
- Tracks voice and configuration identifiers.
- Separates test conditions from listening observations.
- Makes failed attempts visible instead of deleting them.
- Helps developers reproduce a previous generation workflow.

## Repository structure

```
tts-evaluation-log/
├── README.md
├── evaluation_template.csv
├── validate.py
└── examples/
    └── sample_evaluation.csv
```

## 1. Define a test case

Every comparison should begin with an identical text input.

For example:

```
The package arrived yesterday.
I haven't opened it yet.
Could you check the delivery address?
```

Do not change the script between takes.

If you want to evaluate different speaking styles, keep the text constant and record the configuration separately.

## 2. Use a structured evaluation log

Suggested CSV columns:

| Field | Purpose |
| --- | --- |
| test_id | Unique test identifier |
| text_id | Identifier for the source text |
| text | Exact generation input |
| voice_id | Selected voice identifier |
| speed | Speed configuration |
| voice_action | Selected voice action |
| pause_level | Selected pause level |
| style_instruction | Style instruction used |
| output_file | Generated audio filename |
| result | pass / fail / review |
| observation | Human listening notes |

The important distinction is between configuration and observation.

"Voice A sounds better" is an opinion.

"Voice A preserves the intended speaker distinction in the final question" is a more useful observation.

## 3. Add a simple CSV validator

Save this as `validate.py`:

```python
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

            for field in ("text_id", "text",
                          "voice_id", "output_file"):
                if not row[field].strip():
                    errors.append(
                        f"Line {line}: empty {field}"
                    )

            result = row["result"].strip().lower()

            if result not in VALID_RESULTS:
                errors.append(
                    f"Line {line}: invalid result {result}"
                )

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
```

Run it:

```
python validate.py examples/sample_evaluation.csv
```

Expected successful output:

```
CSV validation passed.
```

This checks the evaluation log structure, not the quality of the audio.

## 4. What should actually be evaluated?

I would separate listening evaluation into five dimensions:

- **Pronunciation**: Are the words understandable?
- **Consistency**: Does the output maintain a coherent voice?
- **Expression**: Does the delivery fit the intended context?
- **Timing**: Does the audio fit the available video duration?
- **Usability**: Can the recording be used without another generation?

Use a simple pass/fail/review decision for each dimension. Avoid pretending that an arbitrary numerical score represents universal audio quality.

## 5. Testing with a browser-based tool

One possible test environment is VoxClone (https://web666.cc).

It is a free, browser-based TTS and voice-cloning tool that does not require registration.

Its documented capabilities include:

- 318 voices
- 142 accents
- 10 voice actions
- 5 pause levels
- 6 natural-language style instructions
- Voice cloning from a 5-second reference recording

These capabilities provide several configuration dimensions for an evaluation log.

They do not establish that one voice or configuration is universally better than another.

## Limitations

This repository does not:

- Measure acoustic similarity automatically.
- Establish objective human-preference scores.
- Guarantee identical output across repeated generations.
- Access private provider APIs.
- Claim that different providers use equivalent configuration parameters.

The goal is narrower: make comparisons traceable, repeatable as test procedures, and honest about what was actually evaluated.

## Contribution guidelines

When submitting an evaluation:

- Include the original text.
- Include the configuration.
- Preserve failed attempts.
- Identify subjective observations as subjective.
- Never submit invented benchmark numbers.
- Distinguish missing data from a failed test.

A comparison that openly documents its limitations is more useful than another leaderboard with unexplained scores.

The best voice is not the one that wins a demo. It is the one that survives the actual production requirements.

## Topics

`text-to-speech` `tts` `voice-cloning` `audio-evaluation` `python` `reproducibility`
