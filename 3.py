Scale=int(input("Please input the approximate scale of the stories: "))
User_story=[[0,0,0] for i in range(Scale)]#[story,keyword,tag]

#从文件中读取
import os
import sys
filename=input("\nPlease input filename: ")
filepath=os.path.split(os.path.realpath(sys.argv[0]))[0]+"\\"+filename
lines=-1 #story的数量
with open(filepath,'r',encoding='UTF-8') as file_object:
    while True:
        story=file_object.readline()
        lines+=1
        User_story[lines][0]=story
        User_story[lines][2]=lines#tag
        if not story:
            break
print("\nComplete!")

#筛选出指定词性的单词，然后手动找出关键词
import nltk
while True:#指定关键词的词性,名词或动词
    noun_or_verb=input("\nPlease input NN for noun or VB for verb: ")
    if noun_or_verb=="NN" or noun_or_verb=="VB":
        break
print("\nStart choosing keyword for each story! Please ensure the spelling is correct!")
for i in range(lines):
    location=0
    for j in User_story[i][0]:#截取"I "之后的关键内容
        location+=1
        if j=='I' and (User_story[i][0][location]==' ' or User_story[i][0][location]=='\''):
            story=User_story[i][0][location+1:]
            break
    tokens=nltk.word_tokenize(story)
    pos_tags=nltk.pos_tag(tokens)
    print("\n")
    print(lines-i-1,end='')
    print(" left...")#进度条
    print("\n"+User_story[i][0])#打印出原始story供手动找关键词时参考
    if noun_or_verb=="NN":#关键词词性为名词
        for word,pos in pos_tags:#打印出所有名词
            if(pos=='NN' or pos=='NNS' or pos=='NNP' or pos=='NNPS'):
                print(word,pos)
    else:#关键词词性为动词
        for word,pos in pos_tags:#打印出所有动词
            if(pos=='VB' or pos=='VBD' or pos=='VBG' or pos=='VBN' 
                or pos=='VBP' or pos=='VBZ'):
                print(word,pos)
    User_story[i][1]=input("\nPlease input the keyword: ")#手动输入关键词
print("\nComplete!")

#输入两个单词，返回两个单词的最大相似度函数
from nltk.corpus import wordnet 
def __wup_word_similer(word1,word2):
    '''
    用wordnet求词间最大相似度
    :param word1:
    :param word2:
    :return:
    '''
    max_similer=0
    synSet1=wordnet.synsets(word1)
    synSet2=wordnet.synsets(word2)
    for syn1 in synSet1:
        for syn2 in synSet2:
            currentDistance=syn1.wup_similarity(syn2)
            if (currentDistance==None):
                continue
            if currentDistance>max_similer:
                max_similer=currentDistance
    return max_similer

#聚类
print("\nStart clustering!")
amount=[0 for i in range(lines)]#产生的类的数量
audit_records=[[0,0,0] for i in range(lines*5)]#[word1,word2,Y/N],审核记录
amount_of_records=0
for i in range(lines):
    tag=i
    for j in range(lines):#找出与之相似度最高的
        similer=__wup_word_similer(User_story[i][1],User_story[j][1])
        if i!=j and similer==1.0:
            if User_story[i][1]==User_story[j][1]:
                yes_or_no="Y"
            else:#对聚类进行审核
                if amount_of_records==0:
                    print("\nDo you think \""+User_story[i][1]+"\" and \""+User_story[j][1]+"\" belong to the same category?")
                    yes_or_no=input("Y/N: ")
                    audit_records[0][0]=User_story[i][1]
                    audit_records[0][1]=User_story[j][1]
                    audit_records[0][2]=yes_or_no
                    amount_of_records+=1                    
                else:
                    counter=0
                    for k in range(amount_of_records):
                        if (User_story[i][1]==audit_records[k][0] and User_story[j][1]==audit_records[k][1]) or (User_story[i][1]==audit_records[k][1] and User_story[j][1]==audit_records[k][0]):
                            yes_or_no=audit_records[k][2]
                            break
                        else:
                            counter+=1
                    if counter==amount_of_records:
                        print("\nDo you think \""+User_story[i][1]+"\" and \""+User_story[j][1]+"\" belong to the same category?")
                        yes_or_no=input("Y/N: ")
                        audit_records[amount_of_records][0]=User_story[i][1]
                        audit_records[amount_of_records][1]=User_story[j][1]
                        audit_records[amount_of_records][2]=yes_or_no
                        amount_of_records+=1
            if yes_or_no=="Y":
                tag=User_story[j][2]
                break
    User_story[i][2]=tag
    amount[tag]+=1
print("\nComplete!")
               
#生成文件
location=-1
for i in filename:
    location+=1
    if i=='.':
        filename=filename[0:location]
filename=filename+"_"+noun_or_verb+".txt"
filepath=os.path.split(os.path.realpath(sys.argv[0]))[0]+"\\"+filename#生成文件路径
print("\nGenerating output file:"+filename+"......")
with open(filepath,'w',encoding='UTF-8') as file_object:
    tag=-1
    for i in amount:
        tag+=1
        if i>0:
            tags=[0 for k in range(i)]#存储标签
            amount_of_tags=0            
            stories=[0 for k in range(i)]#存储story
            amount_of_stories=0
            for j in range(lines):
                if User_story[j][2]==tag:
                    stories[amount_of_stories]=User_story[j][0]+"\n"#存入story
                    amount_of_stories+=1
                    if not amount_of_tags:
                        tags[amount_of_tags]=User_story[j][1]#存入标签
                        amount_of_tags+=1
                        tag_name=tags[0] 
                        if i==1:
                            break
                    else:
                        counter=0
                        for k in range(amount_of_tags):
                            if User_story[j][1]==tags[k]:
                                break
                            else:
                                counter+=1
                        if counter==amount_of_tags:
                            tags[amount_of_tags]=User_story[j][1]#存入标签
                            amount_of_tags+=1
            for k in range(1,amount_of_tags):
                tag_name+=" & "+tags[k]
            file_object.write("*"*30+"\n")#分割线
            file_object.write(tag_name+"\n")#写入标签
            file_object.write("*"*30+"\n")
            for k in range(amount_of_stories):
                file_object.write(stories[k])#写入story
            file_object.write("\n\n")
print("\nComplete!")