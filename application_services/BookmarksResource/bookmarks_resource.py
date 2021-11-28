from application_services.BaseApplicationResource import BaseRDBApplicationResource
from database_services.RDBService import RDBService


class BookmarksResource(BaseRDBApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_bookmarks(cls, template, limit, offset):
        bookmarks = dict()
        bookmarks['data'] = RDBService.find_by_template("bookmarkDB", "bookmarks", template, limit, offset)
        bookmarks['link'] = [
            {'rel': 'prev', 'href': f"/bookmarks?limit={limit}&offset={int(offset)-int(limit)}"},
            {'rel': 'self', 'href': f"/bookmarks?limit={limit}&offset={offset}"},
            {'rel': 'next', 'href': f"/bookmarks?limit={limit}&offset={int(offset)+int(limit)}"},
        ]

        for i, data in enumerate(bookmarks['data']):
            links = [
                {'rel': "post", "href": f"/posts/{data['post_id']}"}
            ]

            bookmarks['data'][i]['links'] = links

        return bookmarks

    @classmethod
    def create(cls, user_id, post_id):
        new_bookmark = dict()
        new_bookmark['user_id'] = user_id
        new_bookmark['post_id'] = post_id
        res = RDBService.create("bookmarkDB", "bookmarks", new_bookmark)
        return res

    @classmethod
    def delete(cls, user_id, post_id):
        template = dict()
        template['user_id'] = user_id
        template['post_id'] = post_id
        res = RDBService.delete("bookmarkDB", "bookmarks", template)
        return res

    @classmethod
    def is_bookmarked(cls, user_id, post_id):
        template = dict()
        template['user_id'] = user_id
        template['post_id'] = post_id
        res = RDBService.count("bookmarkDB", "bookmarks", template)
        return res