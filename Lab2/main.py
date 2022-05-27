def reformatClause(clause):  # xóa các khoảng trắng dư
    arr = clause.split()
    return ' '.join(arr)


def readFile(fileName):
    with open(fileName) as f:
        a = f.readline()
        a = reformatClause(a)
        n = int(f.readline())

        KB = []
        for i in range(n):
            clause = f.readline()
            clause = reformatClause(clause)
            KB.append(clause)

    return a, KB


def negative(a):
    arr = a.split()  # lấy các literal và từ khóa trong a
    for i in range(len(arr)):
        if i % 2 == 0:  # vị trí các literal
            if len(arr[i]) == 2:  # literal âm
                arr[i] = arr[i][1]
            else:  # literal dương
                arr[i] = '-' + arr[i]
        else:  # vị trí các từ khóa OR
            arr[i] = 'AND'
    return ' '.join(arr)


def getLiteral(clause):
    tmp = clause.replace('OR', ' ')
    tmp = tmp.split()
    return tmp


def sortLiterals(clause):
    arr = getLiteral(clause)
    for i in range(len(arr) - 1):
        for j in range(i + 1, len(arr)):
            tmp1 = arr[i]
            tmp2 = arr[j]

            if len(arr[i]) == 2:
                tmp1 = arr[i][1]
            if len(arr[j]) == 2:
                tmp2 = arr[j][1]

            if tmp1 > tmp2:
                arr[i], arr[j] = arr[j], arr[i]

    if len(arr) > 1:
        return ' OR '.join(arr)
    return ' '.join(arr)


def checkUseful(clause):
    tmp = getLiteral(clause)

    for i in range(len(tmp) - 1):
        for j in range(i + 1, len(tmp)):
            if tmp[i] == negative(tmp[j]):
                return False
    return True


def deleteDuplicateLiteral(clause):
    tmp = getLiteral(clause)
    newClause = tmp.copy()
    for i in range(len(tmp) - 1):
        for j in range(i + 1, len(tmp)):
            if tmp[i] == tmp[j]:
                newClause.remove(tmp[i])

    if len(newClause) > 1:
        return ' OR '.join(newClause)
    return ' '.join(newClause)


def PL_RESOLVE(clause1, clause2):
    result = []

    tmp1 = getLiteral(clause1)
    tmp2 = getLiteral(clause2)

    for literal1 in tmp1:
        for literal2 in tmp2:
            if literal1 == negative(literal2):
                tmpClause1 = tmp1.copy()
                tmpClause1.remove(literal1)
                tmpClause2 = tmp2.copy()
                tmpClause2.remove(literal2)
                tmpClause = tmpClause1 + tmpClause2

                if len(tmpClause) > 1:
                    resultClause = ' OR '.join(tmpClause)
                else:
                    resultClause = ' '.join(tmpClause)

                if len(resultClause) > 2:
                    resultClause = deleteDuplicateLiteral(resultClause)
                    resultClause = sortLiterals(resultClause)
                    if checkUseful(resultClause):
                        result.append(resultClause)
                else:
                    result.append(resultClause)
    return result


def PL_RESOLUTION(KB, a, fileName):
    f = open(fileName, 'w')
    clauses = []
    clauses.extend(KB)

    nega_a = negative(a)
    negaClauses = []
    if len(a) > 2:
        arr = nega_a.split(' AND ')
        negaClauses.extend(arr)
    else:
        negaClauses.append(nega_a)  # a là literal

    for clause in negaClauses:
        if clause not in clauses:
            clauses.append(clause)

    pos = 1
    count = 1
    while True:
        new = []
        for i in range(len(clauses) - 1):
            if count == 1:
                idx = i + pos
            else:
                idx = pos
            for j in range(idx, len(clauses)):
                resolvents = PL_RESOLVE(clauses[i], clauses[j])
                for resolvent in resolvents:
                    if resolvent not in clauses and resolvent not in new:
                        new.extend(resolvents)

        f.write(str(len(new)) + '\n')
        if len(new) == 0:
            f.write("NO")
            f.close()
            return False

        for i in new:
            if i == '':
                f.write('{}')
            f.write(i + '\n')

        if '' in new:
            f.write("YES")
            f.close()
            return True

        pos = len(clauses)
        count += 1

        clauses.extend(new)


if __name__ == '__main__':
    inputFileName = ['./input/input1.txt',
                     './input/input2.txt',
                     './input/input3.txt',
                     './input/input4.txt',
                     './input/input5.txt',
                     './input/input6.txt']
    outputFileName = ['./output/output1.txt',
                      './output/output2.txt',
                      './output/output3.txt',
                      './output/output4.txt',
                      './output/output5.txt',
                      './output/output6.txt']

    for i in range(len(inputFileName)):
        a, KB = readFile(inputFileName[i])
        PL_RESOLUTION(KB, a, outputFileName[i])
