

def get_arr_dependency(index, array):
    for i in range(0,len(array)):
        if array[i][1] == index:
            import pdb; pdb.set_trace()
            resul_arr = get_arr_dependency(index, array)
        else:
            return 0

def main():
    array = load_task_dependency("resource.ra")
    g = { k: [] for k in range(1, len(array) +1 )}
    for i in range(0, len(array)):
        temp = []
        temp = get_arr_dependency(i, array)
        # g[i][1] = temp 
        print(temp)
    return 0
  

def load_task_dependency(localFileName):
    with open(localFileName, mode='r') as infile:
        content = infile.read().splitlines()
    arr = []
    for row in content:
        if row[0] != ' ':  # HEADERS
            continue
        if row == " EOF":
            break

        x, y = row.split(' ')[1:3]
        arr.append([int(x), int(y)])
    return arr

if __name__ == '__main__':
    main()
