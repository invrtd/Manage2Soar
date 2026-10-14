"""Views for the unlisted public-site preview.

The preview renders a redesigned public site entirely from bundled content
(``preview.content``) so it never touches live CMS rows or the live base
templates. It is not linked anywhere and every page is marked ``noindex``; the
``public-preview`` branch itself is the on/off switch.
"""

from django.shortcuts import render
from django.urls import reverse

from .content import PAGE_MAP, PAGES


def _base_context(request, slug, title, content):
    preview_base = reverse("public_preview_home")
    content = content.replace("%%BASE%%", preview_base)
    feedback_url = reverse("cms:feedback")
    return {
        "page_title": title,
        "content": content,
        "preview_base": preview_base,
        "nav_pages": PAGES,
        "current_slug": slug,
        "is_home": slug == "home",
        "feedback_url": f"{feedback_url}?from={request.get_full_path()}",
    }


def home(request):
    title, content = PAGE_MAP["home"]
    return render(
        request,
        "preview/base.html",
        _base_context(request, "home", title, content),
    )


def page(request, slug):
    if slug not in PAGE_MAP:
        from django.http import Http404

        raise Http404("Not found")
    title, content = PAGE_MAP[slug]
    return render(
        request,
        "preview/base.html",
        _base_context(request, slug, title, content),
    )
