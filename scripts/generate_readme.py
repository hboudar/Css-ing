from pathlib import Path
from html import escape
from urllib.parse import quote


ROOT = Path(".")
README = ROOT / "README.md"

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
}

WEEKDAYS = {
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun",
}

WEEKDAY_ORDER = {
    "Mon": 0,
    "Tue": 1,
    "Wed": 2,
    "Thu": 3,
    "Fri": 4,
    "Sat": 5,
    "Sun": 6,
}


def github_path(*parts) -> str:
    """Convert path components into a GitHub-friendly relative URL."""
    return "./" + "/".join(quote(str(part)) for part in parts)


def main():
    content = """# 🎨 Daily Design Challenge

A daily CSS challenge inspired by **CSS Battle** — creating a new design from scratch every day using HTML and CSS.

The goal is simple: **one day, one design, one new CSS technique.**

Each challenge focuses on recreating shapes, illustrations, patterns, and creative UI designs while improving my CSS skills, experimenting with different techniques, and finding increasingly clever ways to achieve visual results with minimal code.

### What you'll find here

* 🎯 A new CSS design every day
* 🧩 Creative challenges inspired by CSS Battle
* 💡 Experiments with CSS shapes, positioning, gradients, shadows, and more
* 📈 A record of my progress and improvement over time

This repository is both a **CSS playground and a daily learning journey**.

Let's see how far CSS can go. 🚀


"""

    # Find month directories
    months = sorted(
        directory
        for directory in ROOT.iterdir()
        if directory.is_dir()
        and directory.name not in {
            ".git",
            ".github",
            "scripts",
        }
    )

    for month in months:
        content += "<details>\n"
        content += f"<summary>📅 {escape(month.name)}</summary>\n\n"

        # Find weekdays in chronological order
        weekdays = sorted(
            (
                directory
                for directory in month.iterdir()
                if directory.is_dir()
                and directory.name in WEEKDAYS
            ),
            key=lambda day: WEEKDAY_ORDER[day.name],
        )

        for weekday in weekdays:

            # Find date directories
            dates = sorted(
                (
                    directory
                    for directory in weekday.iterdir()
                    if directory.is_dir()
                    and directory.name.isdigit()
                ),
                key=lambda date: int(date.name),
            )

            # Keep only dates containing images
            date_images = []

            for date in dates:
                images = sorted(
                    file
                    for file in date.iterdir()
                    if file.is_file()
                    and file.suffix.lower() in IMAGE_EXTENSIONS
                )

                if images:
                    date_images.append((date, images))

            # Skip empty weekdays
            if not date_images:
                continue

            # Weekday heading
            date_names = ", ".join(
                f"{date.name}/{month.name.split()[0]}"
                for date, _ in date_images
            )

            content += (
                f"### {escape(weekday.name)}: "
                f"{escape(date_names)}\n\n"
            )

            # One table for the entire weekday
            content += "<table>\n<tr>\n"

            for date, images in date_images:
                day_url = github_path(
                    month.name,
                    weekday.name,
                    date.name,
                )

                for image in images:
                    image_url = github_path(
                        month.name,
                        weekday.name,
                        date.name,
                        image.name,
                    )

                    content += (
                        "<td>"
                        f'<a href="{day_url}">'
                        f'<img src="{image_url}" width="200">'
                        "</a>"
                        "</td>\n"
                    )

            content += "</tr>\n</table>\n\n"

        content += "</details>\n\n"

    README.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()