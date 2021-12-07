Scale=120
User_story=[[0,0,0] for i in range(Scale)]#[story,keyword,tag]

#从文件中读取
filepath=input("Please input filepath: ")
lines=-1#story的数量
with open(filepath,'r',encoding='UTF-8') as file_object:
    file_object.readline()#忽略文件第一行的“beforeCluster,As a,I want to”
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
        if j=='I' and User_story[i][0][location]==' ':
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
    User_story[i][1]=input("Please input the keyword: ")#手动输入关键词
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
print("\nJust a moment! Clustering......")
amount=[0 for i in range(lines)]#产生的类的数量
for i in range(lines):
    most_similer=0
    tag=i
    for j in range(lines):#找出与之相似度最高的
        similer=__wup_word_similer(User_story[i][1],User_story[j][1])
        if i!=j and similer>most_similer:
            most_similer=similer
            tag=User_story[j][2]
    User_story[i][2]=tag
    amount[tag]+=1
               
#生成文件
filename=input("\nPlease input filename for the output: ")
with open(filename,'w',encoding='utf-8') as file_object:
    tag=-1
    for i in amount:
        tag+=1
        flag=0
        if i>0:
            file_object.write("\n")
            for j in range(lines):
                if User_story[j][2]==tag:
                    if not flag:
                        file_object.write(User_story[j][1]+"\n")
                        #写入聚类的标签，仅供参考，最后需要手动修改
                        flag=1
                    file_object.write(User_story[j][0]+"\n")#写入story
print("\nComplete!")