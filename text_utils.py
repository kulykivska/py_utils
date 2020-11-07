import re


def get_all_frontend_urls_from_html(
        html: str,
        frontend_url: str = 'http://localhost:4200',
) -> list[str]:
    r = re.compile('(?<=href=").*?(?=")')
    return [link for link in r.findall(html) if frontend_url in link]
