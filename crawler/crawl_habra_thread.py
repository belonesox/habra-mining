from copy import deepcopy
from igraph import *

sys.path.append('../lib')
import MiscUtils as ut

def get_comment_tree(postpath):
    url_to_parse = 'http://habrahabr.ru/' + postpath
    root    = ut.doc4url(url_to_parse)
    if not root:
        return None

    author  = root.xpath('//div[@class="author"]/a')[0].text
    print author
    
    comment_root_tree = {}
    
    def dfs_process(node, tree):
        print node.get('id')
        comments = node.xpath('.//div[@id="comments" or @class="reply_comments"]')[0]
        for comment in comments.xpath('./div[@class="comment_item"]'):
            author = comment.xpath('.//a[@class="username"]')[0].text
            print author
            child_tree = {}
            dfs_process(comment, child_tree)
            tree[author] = deepcopy(child_tree)
    
    dfs_process(root, comment_root_tree)
    comment_tree = {author: comment_root_tree}
    print 'tree:', comment_tree
    
    thedir = os.path.join('../data/posts', os.path.split(postpath)[0])
    ut.createdir(thedir)
    
    filename = os.path.join('../data/posts', postpath) + '.dat'
    ut.data2pickle(comment_tree, filename)


def main():
    get_comment_tree('blogs/pm/137345')
    
if __name__ == '__main__':
    main()



#comment_tree = {author: {}}

#def process_comment(node):


#layout = G.layout_kamada_kawai()
#svgname = "graph.svg"           
#plot(G, svgname, layout=layout) 
