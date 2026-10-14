from converter import convert_to_npr, get_rates

def build_report(expenses):
    if len(expenses) == 0:
        return "No expenses yet."

    rates = get_rates()

    categories = {}

    currencies = {}

    skipped = 0

    for e in expenses:
        npr = convert_to_npr(e["amount"], e["currency"], rates)
        if npr is None:
            skipped = skipped + 1
            continue

        category = e["category"]
        if category not in categories:
            categories[category] = {"total": 0, "count": 0}
        categories[category]["total"] = categories[category]["total"] + npr
        categories[category]["count"] = categories[category]["count"] + 1

        currency = e["currency"]
        if currency in currencies:
            currencies[currency] = currencies[currency] + e["amount"]
        else:
            currencies[currency] = e["amount"]

    grand_total = 0
    for category in categories:
        grand_total = grand_total + categories[category]["total"]

    sorted_categories = sorted(categories.items(), key=lambda item: item[1]["total"], reverse=True)

    lines = ["--- Spending by Category ---"]
    for category, info in sorted_categories:
        if grand_total > 0:
            percent = info["total"] / grand_total * 100
        else:
            percent = 0
        lines.append(
            f"{category}: {round(info['total'], 2)} NPR "
            f"({round(percent, 1)}%, {info['count']} expenses)"
        )
    lines.append(f"Grand Total: {round(grand_total, 2)} NPR")

    lines.append("")
    lines.append("--- Spent in Each Currency ---")
    for currency, amount in currencies.items():
        lines.append(f"{currency}: {round(amount, 2)}")

    if skipped > 0:
        lines.append("")
        lines.append(f"{skipped} expense(s) could not be converted and were left out.")

    return "\n".join(lines)


def category_report(expenses):
    print()
    print(build_report(expenses))
