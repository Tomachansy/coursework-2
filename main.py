from flask import Flask, request, render_template, redirect
from functions import get_json, get_comments, get_posts, get_posts_with_comments, get_bookmarks


COMMENT_PATH = get_json("data/comments.json")
POST_PATH = get_json("data/posts.json")
bookmark_json_file = "data/bookmarks.json"
BOOKMARK_PATH = get_json(bookmark_json_file)

comments_count = get_comments(COMMENT_PATH, True)
comments = get_comments(COMMENT_PATH)


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def index_page():
    user_posts = get_posts(POST_PATH, "", "poster_name")
    posts = get_posts_with_comments(user_posts, comments_count)
    return render_template("index.html", posts=posts, book_count=len(BOOKMARK_PATH))


@app.route('/post/<int:postid>')
def post_by_id(postid):
    post_id = get_posts(POST_PATH, postid, "pk")
    results = get_posts_with_comments(post_id, comments_count)
    return render_template("post.html", results=results, post_comments=COMMENT_PATH)


@app.route('/search')
def search_page():
    search = request.args.get("s")

    if search:
        post_search = get_posts(POST_PATH, search, "content")
        results = get_posts_with_comments(post_search, comments_count)
        return render_template("search.html", results=results, count=len(results))
    else:
        return render_template("search.html")


@app.route('/users/<username>')
def page_by_username(username):
    user_posts = get_posts(POST_PATH, username, "poster_name")
    results = get_posts_with_comments(user_posts, comments_count)
    return render_template("user-feed.html", results=results)


@app.route('/tag/<tagname>')
def page_by_tag(tagname):
    content = get_posts(POST_PATH, f"#{tagname}", "content")
    results = get_posts_with_comments(content, comments_count)
    return render_template("tag.html", results=results, tagname=tagname)


@app.route('/bookmarks/add/<int:postid>')
def add_bookmarks(postid):
    if postid not in BOOKMARK_PATH:
        BOOKMARK_PATH.append(postid)
        get_bookmarks(BOOKMARK_PATH, bookmark_json_file)
    return redirect("/", code=302)


@app.route('/bookmarks/remove/<int:postid>')
def remove_bookmarks(postid):
    if postid in BOOKMARK_PATH:
        BOOKMARK_PATH.remove(postid)
        get_bookmarks(BOOKMARK_PATH, bookmark_json_file)
    return redirect("/", code=302)


@app.route('/bookmarks')
def bookmarks_page():
    posts = []
    for postid in BOOKMARK_PATH:
        user_posts = get_posts(POST_PATH, postid, "pk")
        post = get_posts_with_comments(user_posts, comments_count)
        posts.append(post)
    return render_template("bookmarks.html", posts=posts)


if __name__ == "__main__":
    app.run()
