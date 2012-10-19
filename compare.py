from subprocess import call
import os
import datetime
import sys

# TODO: 
#  - Check if all files are tested from KGS
#  - Check if all files in release corresponds to a
#    file in KGS

def get_diff_result(pdf1, pdf2):
    '''
    Compares pdf1 with pdf2
    Returns 0 for no difference
    Returns 1 for difference
    '''
    return call(["diff-pdf", pdf1, pdf2])

def get_diff_pdf(pdf1, pdf2, diffpdf):
    '''
    Compares pdf1 with pdf2 and creates a resulting pdf in as diffpdf
    Returns a list with a result code and a path or error description
    0 = successfully created
    1 = failure
    '''
    result =  call(["diff-pdf", '--output-diff=' + diffpdf, pdf1, pdf2])
    #print diffpdf + ', ' + pdf1 + ', ' + pdf2 
    if os.path.isfile(diffpdf):
        return (0, diffpdf)
    else:
        return (1, 'Unknown error. No file created...')

def get_kgs_files():
    '''
    Returns all PDF file paths from the known good set folder
    '''
    import glob    
    path = os.path.join('./kgs', '*.pdf')
    files = glob.glob(path)
    return files    

def render_template(entries):
    '''
    Gets all PDF file paths from the known good set folder
    '''
    from jinja2 import Environment, PackageLoader

    env = Environment(loader=PackageLoader('config', 'templates'))
    template = env.get_template('show_entries.html')
    return template.render(entries=entries, time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

if __name__ == '__main__':
    '''
    Cluttered main method. Needs to be splitted up.
    '''
    import shutil
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print '(C) Copyright 2012 Swedwise AB'
    print 'Starting ' + start_time
    release_folder = sys.argv[1:2]
    result_folder = os.path.join(release_folder[0] + '_result')
    files = get_kgs_files()
    entries = []
    for file in files:
        head, tail = os.path.split(file)
        usecase = tail.split('.')[0]
        print 'Evaluating use case ' + usecase
        pdf2 = os.path.join(release_folder[0], tail)
        pdf_diff_filename = 'diff_' + tail
        pdf_diff = os.path.join(result_folder, pdf_diff_filename)
        diff_result = get_diff_result(file, pdf2)
        if diff_result:
            result_string = 'DIFF'
            if not os.path.exists(result_folder):
                os.makedirs(result_folder)
            get_diff_pdf(file, pdf2, pdf_diff)

            entry = dict(usecase=usecase, kgsfile=file, result=result_string, report=pdf_diff_filename) 
        else:
            result_string = 'OK'
            entry = dict(usecase=usecase, kgsfile=file, result=result_string) 
        entries.append(entry)
        print '  ' + result_string
    
    report_file = os.path.join(result_folder, 'report.html')
    print 'Creating report ' + report_file

    f = open(report_file, 'w')
    report_data = render_template(entries)
    f.write(report_data)
    shutil.copy(os.path.join('config', 'static', 'style.css'), os.path.join(result_folder, 'style.css'))
    shutil.copy(os.path.join('config', 'static', 'pdf.png'), os.path.join(result_folder, 'pdf.png'))
    end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print 'Finnished ' + end_time




