import os
import sys
from subprocess import call

def get_diff_view(pdf1, pdf2):
    '''
    Compares pdf1 with pdf2 and and opens up a viewer
    '''
    result =  call(["diff-pdf", '--view', pdf1, pdf2])

if __name__ == '__main__':
    '''
    None the rest
    '''
    release, usecase = sys.argv[1:3]
    pdf1 = os.path.join('kgs', usecase + '.pdf')
    pdf2 = os.path.join(release, usecase +'.pdf')
    if os.path.exists(pdf1) and os.path.exists(pdf2):
        get_diff_view(pdf1, pdf2)
    else:
        if not os.path.exists(pdf1):
            print 'There is no matching file in kgs (' + pdf1 + ')'
        if not os.path.exists(pdf2):
            print 'There is no matching file in ' + release + ' (' + pdf1 + ')'
