# -*- coding:utf-8 -*-
# XML Extract
from xml.etree import ElementTree

# parse for xml file
def xmlparse(filename):
    return ElementTree.parse(filename)

# find pron question and return text
def pron_parse(question):
    quesDict = {}
    quesDict['id'] = question.attrib['id']
    quesDict['ques'] = question.find('text').text
    quesbody = []
    point = []

    for each in question.iterfind('select/option'):
        #print 'each',each.tag,each.attrib
        #print 'text',''.join(each.itertext()).replace('$$','\t')
        #print 'point',
        pointList = []
        for eachpoint in each.findall('point'):
            #print eachpoint.text,
            pointList.append(eachpoint.text)
        #print
        #quesDict[each.attrib['value']] = ''.join(each.itertext()).replace('$$',' ')
        #quesDict[each.attrib['value']+'point'] = pointList
        quesbody.append(''.join(each.itertext()))
        point.append(pointList)

    quesDict['body'] = quesbody
    quesDict['point'] = point
    return quesDict

# find select term and return question text
def selectTerm_parse(question):
    quesDict = {}
    quesDict['id'] = question.attrib['id']

    body = []
    for each in question.findall('text/label'):
        #print each.tag,each.attrib,each.text
        body.append(each.text)
    quesDict['body'] = body
    options = []
    for each in question.iterfind('select/option'):
        #print 'each',each.tag,each.attrib,each.text.replace('$$','\t')
        #quesDict[each.attrib['value']] = ''.join(each.text).replace('$$','\t')
        options.append(''.join(each.text))
    quesDict['options'] = options

    #print quesDict
    return quesDict

def error_sent_parse(question):
    quesDict = {}
    try:
        quesDict['text'] = question.find('text').text
    except:
        pass
    try:
        quesDict['constraint'] = question.find('analysis/constraints/constraint').text
    except:
        pass
    try:
        quesDict['trigger'] = question.find('analysis/triggers/trigger').text
    except:
        pass
    try:
        quesDict['number'] = question.find('analysis/constraints/number').text
    except:
        pass
    options = []
    for each in question.iterfind('select/option'):
         options.append(each.text)
    quesDict['options'] = options

    return quesDict

def add_answer(question,answer):
    answerNode = create_node("answer",{"org":"HIT"},answer)
    add_child_node(question,answerNode)

def create_node(tag,propertyMap,content):
    element = ElementTree.Element(tag,propertyMap)
    element.text = content
    return element

def write_xml(xmltree,outputfile):
    xmltree.write(outputfile,encoding="utf-8",xml_declaration=True)

def add_child_node(question,answerNode):
    question.append(answerNode)

# Return position by keyword in xmlTree
def keyword_position(xmltree,keyword):
    quesList = []
    for ques in xmltree.iterfind('section/questions/question'):
        try:
            quesText = ques.find('text').text

            allFlag = True
            for eachKey in keyword:
                if eachKey not in quesText:
                    allFlag = False

            if allFlag==True:
                quesList.append(ques)
                #print 'tag',ques.tag,'attrib',ques.attrib,'text',ques.find('text').text
        except:
            pass

    #print quesList
    return quesList

# Return position by keyword and triggers in xmlTree
def keyword_position_trigger_or(xmltree,keyword):
    quesList = []
    for ques in xmltree.iterfind('section/questions/question'):
        try:
            #print 'ques',ques
            #print ques.tag,ques.attrib
            quesText = ques.find('analysis/triggers/trigger').text
            #print 'quesText',quesText

            for eachKey in keyword:
                if eachKey in quesText:
                    quesList.append(ques)
                    break
                #print 'tag',ques.tag,'attrib',ques.attrib,'text',ques.find('text').text
        except:
            pass

    #print quesList
    return quesList
