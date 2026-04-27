import pickle as x
import json as y
total_subcodes = tuple()


class student(list):
    def __init__(self, data):
        super().__init__(data)
        self.roll = self[0]
        self.name = self[1]
        self.gender = self[2]
        self.subjects = self[3]
        self.percentage = self[4]
        self.stream = self[5]


class students_subject(dict):
    def __init__(self, code, marks, grade):
        self.code = code
        self.marks = marks
        self.grade = grade
        self[code] = (marks, grade)


def make_all_st_data_list(path):

    with open(path, 'r') as f:
        data = [i.split() for i in f.readlines()]
    all_st_data = list()
    row = None
    for i in data:
        if i:
            if i[0].isnumeric():
                if i[0] > '100':
                    row = i
                    all_st_data.append(row)
                elif i[0] <= '100':
                    row.extend(i)
            if i[0] == 'TOTAL':
                with open('Present_st_data.json','w') as f:
                    i = ' '.join(i)
                    l = (''.join([j for j in i if j.isalnum() or j in ': '])).split()
                    ind = 0
                    dic = dict()
                    for i in range(len(l)):
                        if l[i] == ':' :
                            dic['_'.join(l[ind:i])] = int(l[i+1])
                            ind = i+2
                    y.dump(dic,f)
    return all_st_data
#['21689767', 'F', 'ADYA', 'CHOUDHARY', '301', '042', '043', '044', '048', '049', 'A1', 'A2', 'A1', 'PASS', '075', 'C1', '059', 'C2', '054', 'D1', '081', 'B1', '084', 'B1', '086', 'C2']
def make_list_data_in_obj_format(all_st_dt_lst):
    global total_subcodes
    ourformat_list = list()
    for l in all_st_dt_lst:

        name = ' '.join(l[l.index('M')+1:l.index('301')]) if 'M' in l else  ' '.join(l[l.index('F')+1:l.index('301')]) if 'F' in l else None
        gender = 'Male' if 'M' in l else 'Female' if 'F' in l else 'Other'
        roll = l[0]
        if 'PASS' in l:
            status = (l.index('PASS'))
            sub_codes = l[ l.index('301') : status - 3]
            subjects = tuple()
            i,j =0,1
            for it in sub_codes:
                if it not in total_subcodes:
                    total_subcodes += (it,)
                subjects +=  (students_subject(it,(l[ status + 1:])[i],(l[ status + 1 : ]) [j]),)            
                i += 2
                j += 2
    
        elif 'COMP' in l:
            status = (l.index('COMP'))
            sub_codes = l[ l.index('301') : status - 3]
            subjects = tuple()
            i,j =0,1
            for it in sub_codes:
                subjects +=  (students_subject(it,(l[ status + 3:])[i],(l[ status + 3 : ]) [j]),)            
                i += 2
                j += 2
        
        percentage = (sum([int(i.marks) for i in subjects[:5]])/500)*100
        stream = 'SCI' if '042' in sub_codes else 'COM' if '055' in sub_codes else 'HUM' if '028' in sub_codes else 'HUM'
        temp_l = student([roll,name,gender,subjects,percentage,stream])
        ourformat_list.append(temp_l)
    return ourformat_list

def writing_to_binary_file(path):
    global total_subcodes
    with open(path[:-3]+'bin','wb') as f:
        data = make_all_st_data_list(path)
        intem_data = make_list_data_in_obj_format(data)
        x.dump(intem_data,f)
    with open('prsnt_sb_cds.json','w') as f:
        y.dump({'present_subcodes':total_subcodes},f)
    return path[:-3]+'bin'

def read_file(path):
    with open(path[:-3]+'bin','rb') as f:
        data = x.load(f)
    return data

