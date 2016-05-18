# kernel method for select term
import re
import random
import os
from Config import *
from pyltp import Segmentor

segmentor = Segmentor()
segmentor.load('./model/cws.model')

def answer(questionDict):
    ### return answer for select term question
    '''
    for each in questionDict:
        print each,questionDict[each]
    '''

    candidateTermList = generate_candidate_term(questionDict['options'])
    compareSentenceList = generate_compare_sentence(questionDict['body'],candidateTermList)
    scoreList = rnnlm_score(compareSentenceList)
    answer = find_best_option(questionDict['options'],candidateTermList,scoreList)
    #print 'answer',answer
    return answer

def generate_candidate_term(optionList):
    ### generatee candidata term
    ### return candidate term list. [[A1,A2],[B1,B2],[C1,C2]]
    optionList = option_list_regular(optionList)
    candidateTermList = []
    # insert empty list for sentence length
    for i in range(len(optionList[0])):
        candidateTermList.append([])

    # insert candidate term
    for i in range(len(optionList)):
        for j in range(len(optionList[i])):
            if optionList[i][j] not in candidateTermList[j]:
                candidateTermList[j].append(optionList[i][j])

    #print candidateTermList
    return candidateTermList

def generate_compare_sentence(sentenceList,candidateTermList):
    ### generate compare sentence
    ### return compare sentence list, [[senA1,senA2],[senB1,senB2],[senC1,senC2]]
    compareSentenceList = []
    for i in range(len(sentenceList)):
        compareSentenceList.append(single_compare_sentence(sentenceList[i],candidateTermList[i]))

    '''
    for eachCompare in compareSentenceList:
        for sentence in eachCompare:
            print sentence
    '''
    return compareSentenceList

def rnnlm_score(compareSentenceList):
    ### calculate rnnlm score, return correct index list
    write_sentence_into_file(compareSentenceList)
    score_list = get_rnnlm_result_from_file()
    return score_list

def write_sentence_into_file(compareSentenceList):
    ### write compare sentence into file
    # write sentence string to file
    fw = open(tmpfile,'w+')
    fileStr = ''
    for i in range(len(compareSentenceList)):
        for j in range(len(compareSentenceList[i])):
            fileStr += sentence_segmentor(compareSentenceList[i][j].encode('utf-8'))+'\n'
    fw.write(fileStr) 
    fw.close()
    # test RNNLM
    rnnlm_test() 

def sentence_segmentor(sentence):
    ### segmentor for sentence
    words = segmentor.segment(sentence)
    return ' '.join(words)

def rnnlm_test():
    ### rnnlm test
    cmd = [rnnpath + '/rnnlm','-rnnlm',rnnmodel,'-test',tmpfile,'-nbest','>',scorepath+'/score.txt']
    os.system(' '.join(cmd))
    print ' '.join(cmd)

def get_rnnlm_result_from_file():
    ### get rnnlm result from file. return score list 
    scorefile = scorepath+'/score.txt'
    fp = open(scorefile)
    score_list = []
    for line in fp.readlines():
        try:
            score_list.append(float(line))
        except:
            pass

    fp.close()
    #print score_list
    return score_list

def find_best_option(optionList,candidateTermList,scoreList):
    ### find best option, given correct index list and candidate term list
    ### return question answer . 'A'

    # find correct term
    correctTermList = []
    startPos = 0
    for i in range(len(candidateTermList)):
        candidateTermNum = len(candidateTermList[i])
        endPos = startPos+candidateTermNum
        scoreRange = scoreList[startPos:endPos] 
        maxIndex = scoreRange.index(max(scoreRange))
        #print 'startPos',startPos,'endPos',endPos,
        #print 'score list',scoreList[startPos:endPos],'maxIndex',maxIndex
        correctTermList.append(candidateTermList[i][maxIndex])
        startPos = endPos
    
    # calculate correct number for every option
    correctNumList = []
    for optionIndex in range(len(optionList)):
        correctNum = 0
        for termIndex in range(len(correctTermList)):
            if optionList[optionIndex][termIndex]== correctTermList[termIndex]:
                correctNum+=1
        correctNumList.append(correctNum)

    # find max number
    MaxIndex = []
    for i in range(len(correctNumList)):
        if correctNumList[i]==max(correctNumList):
            MaxIndex.append(i)

    return list_index_to_answerChar(random.choice(MaxIndex))

def list_index_to_answerChar(index):
    return chr(index+65)

def single_compare_sentence(sentence,termlist):
    ### insert term in sentence
    ### return compare sentence list, [senA1,senA2]
    compareSenList = []
    orignSen = re.sub(r'[_]+','$',sentence)
    for i in range(len(termlist)):
        compareSenList.append(orignSen.replace('$',termlist[i]))
    return compareSenList

def option_list_regular(optionList):
    ### option list regular, remove useless character
    for i in range(len(optionList)):
        optionList[i] = optionList[i].replace('\t','').replace('\r','').replace('\n','').split('$$')
    return optionList
