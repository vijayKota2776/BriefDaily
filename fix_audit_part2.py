import os

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)

detail_code = read_file('lib/features/article/article_detail_screen.dart')
detail_code = detail_code.replace(
    "final bookmarkedIds = ref.watch(bookmarkProvider);",
    "final bookmarkedArticles = ref.watch(bookmarkProvider);"
)
detail_code = detail_code.replace(
    "final isBookmarked = bookmarkedIds.contains(article.id);",
    "final isBookmarked = bookmarkedArticles.any((a) => a.id == article.id);"
)
detail_code = detail_code.replace("toggleBookmark(article.id)", "toggleBookmark(article)")
write_file('lib/features/article/article_detail_screen.dart', detail_code)

    "final bookmarkedIds = ref.watch(bookmarkProvider);",
    "final bookmarkedArticles = ref.watch(bookmarkProvider);"
)
    "final isBookmarked = bookmarkedIds.contains(article.id);",
    "final isBookmarked = bookmarkedArticles.any((a) => a.id == article.id);"
)
    "Text(\n                    '${article.source} · ${article.readingTime} min',",
    "Text(\n                    '${article.source} · ${timeago.format(article.publishedAt)} · ${article.readingTime} min',"
)
print("Part 2 done")
