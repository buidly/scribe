import pygit2

from . import exceptions


def get_tags_references(repo: pygit2.Repository) -> list[str]:
    """Fetches all tags from github repo"""
    refs = repo.references
    tags = [ref for ref in refs if ref.startswith("refs/tags/")]

    return tags


def get_current_branch(repo: pygit2.Repository) -> str:
    """Fetches the current branch from repo"""
    return repo.head.name


def checkout_tag_branch(repo: pygit2.Repository, tag_name: str) -> None:
    tags = get_tags_references(repo)
    selected_tag: str | None = None
    for t in tags:
        if t.removeprefix("refs/tags/") == tag_name:
            selected_tag = t
            break

    if not selected_tag:
        raise exceptions.TagNotFound

    repo.checkout(selected_tag, strategy=pygit2.GIT_CHECKOUT_FORCE)


def checkout_branch(repo: pygit2.Repository, branch_name: str) -> None:
    repo.checkout(branch_name, strategy=pygit2.GIT_CHECKOUT_FORCE)
