# -*- coding:utf-8 -*-
# Select Term Module
import os
import sys
import xmlParser
import kernel
import tempfile
from smb.SMBConnection import SMBConnection

reload(sys)
sys.setdefaultencoding('utf-8')

def select_term_question(keyword,fileObj,outputFile):
    xmltree = xmlParser.xmlparse(fileObj)
    quesList = xmlParser.keyword_position(xmltree,keyword)
    for eachQues in quesList:
        try:
            answer = question_solve(eachQues)
        except:
            continue
        if answer=='':
            continue

        xmlParser.add_answer(eachQues,answer)
        #print

    xmlParser.write_xml(xmltree,outputFile)

def question_solve(question):
    questionDict = xmlParser.selectTerm_parse(question)
    if no_use_check(questionDict):
        return ''

    answer = question_answer(questionDict)
    return answer

def question_answer(questionDict):
    return kernel.answer(questionDict)

def no_use_check(question):
    '''
    for each in question:
        print each,question[each]
    '''
    if question['body']==[] or question['options']==[]:
        return True
    return False

def file_connection():
    IP = sys.argv[1]
    shareName = sys.argv[2]
    inputFile = sys.argv[3]
    port = 139
    conn = SMBConnection("","","","")
    conn.connect(IP,port)
    fileObj = tempfile.NamedTemporaryFile()

    conn.retrieveFile(shareName,inputFile,fileObj)
    return fileObj
    
def test(keyword):
    paperPath = '../papers/'
    fileNames = os.listdir(paperPath)
    for f_name in fileNames:
        print 'processing',f_name
        outName = './output/'+f_name.split('.')[0]+'out.xml'
        select_term_question(keyword,paperPath+f_name,outName)
        #print

if __name__=='__main__':
    
    #outputFile = sys.argv[4]
    outputFile = sys.argv[2]

    #fileObj = file_connection()
    fileObj = sys.argv[1]
    xmltree = xmlParser.xmlparse(fileObj)


    keyword = ['填入','词语']
    #test(keyword)
    select_term_question(keyword,fileObj,outputFile)
    #select_term_question(keyword,fileObj,outputFile)
    #fileObj.close()
