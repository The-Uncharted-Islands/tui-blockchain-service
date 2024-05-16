def handle_page(page, pageSize):
    if page > 0:
        page = page - 1
    if page < 0:
        page = 0
    if pageSize > 100:
        pageSize = 100
    return page, pageSize
