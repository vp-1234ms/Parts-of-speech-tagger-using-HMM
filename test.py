import sys
from decimal import *
import codecs

tag_set = set()
word_set = set()

def parse_traindata():
    fin = "model/hmmmodel.txt"
    output_file = "outputs/hmmmoutput.txt"
    transition_prob = {}
    emission_prob = {}
    tag_list = []
    tag_count ={}
    global tag_set
    try:
        input_file = codecs.open(fin,mode ='r', encoding="utf-8")
        lines = input_file.readlines()
        flag = False
        for line in lines:
            line = line.strip('\n')
            if line != "Emission Model":
                i = line[::-1]
                key_insert = line[:-i.find(":")-1]
                value_insert = line.split(":")[-1]

                # for transition probabilities #
                if flag == False:
                    transition_prob[key_insert] = value_insert
                    if (key_insert.split("~tag~")[0] not in tag_list) and (key_insert.split("~tag~")[0] != "start"):
                        tag_list.append(key_insert.split("~tag~")[0])

                else:
                    # for emission probabilities #
                    emission_prob[key_insert] = value_insert
                    val = key_insert.split("/")[-1]
                    j = key_insert[::-1]
                    word = key_insert[:-j.find("/")-1].lower()
                    word_set.add(word)
                    if val in tag_count:
                        tag_count[val] +=1
                    else:
                        tag_count[val] = 1
                    tag_set.add(val)

            else:
                flag = True
                continue

        input_file.close()
        return tag_list, transition_prob, emission_prob, tag_count, word_set

    except IOError:
        fo = codecs.open(output_file, mode='w',encoding="utf-8")
        fo.write("File not found: {}".format(fin))
        fo.close()
        sys.exit()


def viterbi_algorithm(sentence, tag_list, transition_prob, emission_prob, tag_count, word_set):
    global tag_set
    sentence = sentence.strip("\n")
    word_list = sentence.split(" ")
    current_prob = {}
    
    # Smoothing value for missing transitions
    smoothing_value = Decimal("1e-5")  # Or any small probability value you prefer
    
    for tag in tag_list:
        tp = Decimal(transition_prob.get("start~tag~" + tag, smoothing_value))
        em = Decimal(emission_prob.get(word_list[0].lower() + "/" + tag, smoothing_value))
        current_prob[tag] = tp * em

    if len(word_list) == 1:
        max_path = max(current_prob, key=current_prob.get)
        return max_path
    else:
        for i in range(1, len(word_list)):
            previous_prob = current_prob
            current_prob = {}
            locals()['dict{}'.format(i)] = {}
            previous_tag = ""
            for tag in tag_list:
                if word_list[i].lower() in word_set:
                    em = Decimal(emission_prob.get(word_list[i].lower() + "/" + tag, smoothing_value))
                else:
                    em = Decimal(1) / (tag_count[tag] + len(word_set))
                
                max_prob, previous_state = max(
                    (Decimal(previous_prob[prev_tag]) *
                     Decimal(transition_prob.get(prev_tag + "~tag~" + tag, smoothing_value)) * em, prev_tag)
                    for prev_tag in previous_prob
                )
                
                current_prob[tag] = max_prob
                locals()['dict{}'.format(i)][previous_state + "~" + tag] = max_prob
                previous_tag = previous_state

            if i == len(word_list) - 1:
                max_path = ""
                last_tag = max(current_prob, key=current_prob.get)
                max_path = max_path + last_tag + " " + previous_tag
                for j in range(len(word_list) - 1, 0, -1):
                    for key in locals()['dict{}'.format(j)]:
                        data = key.split("~")
                        if data[-1] == previous_tag:
                            max_path = max_path + " " + data[0]
                            previous_tag = data[0]
                            break
                result = max_path.split()
                result.reverse()
                return " ".join(result)



tag_list, transition_model, emission_model, tag_count, word_set = parse_traindata()
fin = sys.argv[1]
input_file = codecs.open(fin, mode='r', encoding="utf-8")
fout = codecs.open("outputs/hmmoutput.txt",mode='w',encoding="utf-8")
for sentence in input_file.readlines():
    path = viterbi_algorithm(sentence, tag_list, transition_model, emission_model,tag_count, word_set)
    sentence = sentence.strip("\n")
    word = sentence.split(" ")
    tag = path.split(" ")
    for j in range(0,len(word)):
        if j == len(word)-1:
            fout.write(word[j] + "/" + tag[j]+ u'\n')
        else:
            fout.write(word[j] + "/" + tag[j] + " ")


predicted = codecs.open("outputs/hmmoutput.txt", mode ='r', encoding="utf-8")
expected = codecs.open("test_data/test_tagged.txt", mode ='r', encoding="utf-8")

c = 0
total = 0
for line_pred in predicted.readlines():
    u = line_pred.split(" ")
    a = expected.readline().split(" ")

    total += len(u)
    
    if len(u) != len(a):
        continue 
    
    for i in range(len(u)):
        if a[i] != u[i]:
            c += 1

print("Wrong Predictions = ", c)
print("Total Predictions = ", total)
print("Accuracy is = ", 100 - (c / total * 100), "%")

