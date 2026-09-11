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


def github_path(path: Path) -> str:
    """Convert a repository path into a GitHub-friendly relative URL."""
    return "./" + "/".join(quote(part) for part in path.parts)


def main():
    content = """# 🎨 Daily Design Challenge

A new design every day.

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

        # Find weekdays
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

            if not dates:
                continue

            content += f"### {escape(weekday.name)}\n\n"

            for date in dates:

                # Find images directly inside the date directory
                images = sorted(
                    file
                    for file in date.iterdir()
                    if file.is_file()
                    and file.suffix.lower() in IMAGE_EXTENSIONS
                )

                # Ignore empty date directories
                if not images:
                    continue

                content += f"#### {escape(date.name)}\n\n"

                # Clicking an image opens that day's directory
                day_url = github_path(date)

                # Display all designs from the same day side-by-side
                content += "<table><tr>\n"

                for image in images:
                    image_url = github_path(image)

                    content += (
                        "<td>"
                        f'<a href="{day_url}">'
                        f'<img src="{image_url}" width="200">'
                        "</a>"
                        "</td>\n"
                    )

                content += "</tr></table>\n\n"

        content += "</details>\n\n"

    README.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()