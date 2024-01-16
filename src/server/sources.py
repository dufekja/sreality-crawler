
BODY = lambda body : f"""
        <html>
            <head><title>Crawled content</title></head>
            <body>{body}</body>
        </html>
    """

PROPERTY_ITEM = lambda title, img_url : f"""
        <div class='property'>
            <h2>{title}</h2>
            <img src="{img_url}">
        </div>
    """