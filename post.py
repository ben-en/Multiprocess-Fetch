
def storybook():
    # Needs to be rewritten because it was moved
            from bs4 import BeautifulSoup
            rows = []
            items = []
            labels = []
            final_list = []
            html = open(join(path, md5, 'index.html'), 'r')
            try:
                soup = BeautifulSoup(html)
            finally:
                html.close()
            main_div = (soup.find("div", { "class" : "book_review book_"
                                           "details_page" }))
            for child in main_div.find_all("div", { "class" : "field-label" }):
                labels.append(child.get_text())
            for child in main_div.find_all("div", { "class" : "field-items" }):
                items.append(child.get_text())
            for i in range(0, len(labels)):
                rows.append('<b>' + labels[i].strip() + '</b>' + ' ' +
                            items[i].strip())
            img = '<img src="./thumbnail.%s">' % thumb[-3:]
            download = '<a href="./%s.PDF">%s Click here to download this '\
                       'story!</a>' % (down_name, img)
            final_list.append('''
<!DOCTYPE html>
<meta charset="utf-8"/>
<meta content="text/html; charset='utf-8'" name="http-equiv"/>
<div id="readabilityBody">
<div class="mw-content-ltr" dir="ltr" id="mw-content-text" lang="en">
''')
            final_list.append('<html>')
            final_list.append('<head>' + '\n' + '<title>' + meta['title'] +
                              '</title>' + '</head>')
            final_list.append('<body>')
            final_list.append('<h1>' + meta['title'] + '</h1>')
            final_list.append(download)
            for row in rows:
                final_list.append('<br/>')
                final_list.append(row)
            final_list.append('</div>\n</div>')
            final_list.append('</body>')
            final_list.append('</html>')
            final = '\n'.join(final_list)
            html = open(join(path, md5, 'index.html'), 'w')
            try:
                html.write(final)
            finally:
                html.close()
