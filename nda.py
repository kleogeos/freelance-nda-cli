#!/usr/bin/env python3
"""Generate a plain-language mutual NDA (HTML) from a JSON file. Zero dependencies."""
import argparse
import html
import json
import sys

DISCLAIMER = (
    "This is a general-purpose template, not legal advice. It covers the basics "
    "of a mutual non-disclosure agreement for a straightforward freelance "
    "discovery call or project discussion. For high-value, cross-border, or "
    "especially sensitive engagements, have a licensed attorney in your "
    "jurisdiction review or draft the agreement instead."
)


def esc(s):
    return html.escape(str(s))


def render(data):
    party_a = data["party_a"]
    party_b = data["party_b"]
    purpose = data.get("purpose", "discussing a potential freelance engagement")
    term_years = data.get("term_years", 2)
    mutual = data.get("mutual", True)
    governing_law = data.get("governing_law", "")
    exclusions = data.get("exclusions", [
        "information that is or becomes publicly available through no fault of the receiving party",
        "information the receiving party already lawfully knew before disclosure",
        "information independently developed without using the disclosing party's confidential information",
        "information required to be disclosed by law or court order, with prompt notice to the other party where legally permitted",
    ])

    exclusions_items = "\n".join(f"<li>{esc(e)}</li>" for e in exclusions)

    if mutual:
        obligation_text = (
            f"Both {esc(party_a)} and {esc(party_b)} may disclose confidential "
            "information to each other, and both agree to the same obligations "
            "below as both a disclosing and a receiving party."
        )
        title = "Mutual Non-Disclosure Agreement"
    else:
        obligation_text = (
            f"{esc(party_a)} (\"Disclosing Party\") may disclose confidential "
            f"information to {esc(party_b)} (\"Receiving Party\"), who agrees to "
            "the obligations below."
        )
        title = "Non-Disclosure Agreement"

    return f"""<!doctype html><html><head><meta charset="utf-8">
<title>{title} — {esc(party_a)} & {esc(party_b)}</title>
<style>
body{{font-family:-apple-system,Arial,sans-serif;max-width:680px;margin:40px auto;color:#1a1a1a;line-height:1.5}}
h1{{font-size:22px}}
h2{{font-size:16px;margin-top:28px;color:#333}}
.meta{{color:#666;font-size:14px}}
.disclaimer{{background:#fff8e6;border:1px solid #f0d58c;border-radius:6px;padding:12px 16px;font-size:13px;color:#664d03;margin-top:24px}}
.sig{{margin-top:40px;display:flex;gap:40px}}
.sig div{{flex:1;border-top:1px solid #999;padding-top:6px;font-size:13px;color:#666}}
@media print{{body{{margin:0}} .disclaimer{{background:none}}}}
</style></head><body>
<h1>{title}</h1>
<p class="meta">Between <b>{esc(party_a)}</b> and <b>{esc(party_b)}</b><br>
Purpose: {esc(purpose)}</p>

<h2>1. Confidential information</h2>
<p>{obligation_text} "Confidential information" means any non-public business, technical, or financial information disclosed in connection with the purpose above, whether in writing, verbally, or by inspection.</p>

<h2>2. Obligations</h2>
<p>The receiving party agrees to: use confidential information only for the purpose above; not disclose it to third parties without written consent; and protect it with at least the same care used for its own confidential information, but no less than reasonable care.</p>

<h2>3. Exclusions</h2>
<p>Confidential information does not include information that:</p>
<ul>{exclusions_items}</ul>

<h2>4. Term</h2>
<p>This agreement stays in effect for {esc(term_years)} year(s) from the date of signing. Confidentiality obligations for information disclosed during that period survive the term's end.</p>

<h2>5. No obligation to proceed</h2>
<p>Signing this agreement does not obligate either party to enter into any further business relationship, contract, or transaction.</p>

{"<h2>6. Governing law</h2><p>This agreement is governed by the laws of " + esc(governing_law) + ".</p>" if governing_law else ""}

<div class="sig">
<div>{esc(party_a)}<br>Date: ____________</div>
<div>{esc(party_b)}<br>Date: ____________</div>
</div>

<p class="disclaimer">{esc(DISCLAIMER)}</p>
</body></html>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", help="JSON NDA file (see example.json)")
    ap.add_argument("-o", "--output", help="output HTML file (default: stdout)")
    args = ap.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    for required in ("party_a", "party_b"):
        if required not in data:
            print(f"error: missing required field '{required}'", file=sys.stderr)
            sys.exit(1)

    out = render(data)
    if args.output:
        with open(args.output, "w") as f:
            f.write(out)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)


if __name__ == "__main__":
    main()
