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


def github_path(path: Path) -> str:
    """Convert a repository path into a GitHub-friendly relative URL."""
    return "./" + "/".join(quote(part) for part in path.parts)


def main():
    content = """# 🎨 Daily Design Challenge

A new design every day.

"""

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
        content += f"<details>\n"
        content += f"<summary>📅 {escape(month.name)}</summary>\n\n"

        days = sorted(
            directory
            for directory in month.iterdir()
            if directory.is_dir()
        )

        for day in days:
            images = sorted(
                file
                for file in day.iterdir()
                if file.is_file()
                and file.suffix.lower() in IMAGE_EXTENSIONS
            )

            if not images:
                continue

            content += f"### {escape(day.name)}\n\n"

            day_url = github_path(day)

            for image in images:
                image_url = github_path(image)

                content += (
                    f'<a href="{day_url}">'
                    f'<img src="{image_url}" width="200">'
                    f'</a>\n'
                )

            content += "\n"

        content += "</details>\n\n"

    README.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()