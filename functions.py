import json


def get_json(file):
    with open(file, "r", encoding="utf-8") as f:

        return json.load(f)


def get_comments(data, count=False):
    """
    if count=False\n
    __dict{ 'post_id': list[ comments ] };\n
    if count=True\n
    __dict{ 'post_id': list[ number of comments ] }\n
    :param data: list
    :param count: bool
    :return: dict
    """

    comments = {}
    com_num = {}

    for user in data:
        if user.get("post_id") not in comments:
            comments[user["post_id"]] = []
        for num in comments:
            if num == user["post_id"]:
                comments[num].append(user["comment"])

    if not count:
        return comments

    if count:
        for com in comments:
            com_num[com] = len(comments.get(com))

        return com_num


def get_posts(data, word, search_for):

    sett = get_json("data/search_settings.json")
    limit = sett["limit"]
    found_posts = []

    for post in data:
        if sett["case-sensitive"]:
            if str(word).lower() in str(post[search_for]).lower():
                post["content"] = get_post_with_tags_link(post["content"])
                found_posts.append(post)

        else:
            if str(word) in str(post[search_for]):
                post["content"] = get_post_with_tags_link(post["content"])
                found_posts.append(post)

        if len(found_posts) >= limit:
            break

    return found_posts


def get_posts_with_comments(posts, comments):

    for post in posts:
        for key, value in comments.items():
            if post["pk"] == key:
                post["comment"] = value
            elif post["pk"] not in comments.keys():
                post["comment"] = 0

    return posts


def get_post_with_tags_link(content):

    post = content.split(" ")

    for index, word in enumerate(post):
        if word.startswith("#"):
            tagname = word[1:]
            post[index] = f"<a href='/tag/{tagname}'>{word}</a>"

    return " ".join(post)


def get_bookmarks(data, json_file):

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
