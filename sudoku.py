import copy
import tkinter
import tkinter.font


def possible(y, x, n):
    global first
    # n is the number we want to fill in

    # 1st
    # check if n already existed in vertical (y) axis
    # if exists, return False (not possible)
    for i in range(9):
        if first[y][i] == n:
            return False

    # 2nd
    # check horizontal (x) axis
    for i in range(9):
        if first[i][x] == n:
            return False

    # 3rd
    # check the 3x3 local grid
    x0 = (x//3)*3
    y0 = (y//3)*3
    for i in range(3):
        for j in range(3):
            if first[y0 + i][x0 + j] == n:
                return False

    # return true if pass all 3 checks.
    return True


def solveex():
    global first
    global matrix_iterations
    for y in range(9):
        for x in range(9):
            # Find blank positions in the grid (value = 0)
            if first[y][x] == 0:
                # Loop n from 1-9
                for n in range(1, 10):
                    if possible(y, x, n):
                        first[y][x] = n
                        iteration = copy.deepcopy(first)
                        matrix_iterations.append(iteration)
                        solveex() #calls itself again to begin with the new position

                        # This is where backtracking happens
                        # Reset the latest position back to 0 and try with new n value
                        first[y][x] = 0
                return
    # print(numpy.matrix(first))


def get_matrix_pos():
    global final_matrix
    currentint = 0
    while currentint < final_matrix + 1:
        yield currentint
        currentint += 1


def find_solution():
    for index, matrix in enumerate(matrix_iterations):
        if all(matrix[8]):  # if there are no zero values in last list, the solution is found
            final_iteration = index
            return final_iteration


def update_grid():
    global matrix_pos
    global nonzero_positions
    try:
        iteration = next(matrix_pos)
        current_matrix = matrix_iterations[iteration]
        for i in range(9):
            for j in range(9):
                if not int(f"{i}{j}") in nonzero_positions and current_matrix[i][j] != 0:
                    label_dict[f"my_label{i}{j}"].config(text=f"{current_matrix[i][j]}", font=sudoko_font,
                                                         background='white', fg='blue')
        iteration_label.config(text=f"Current run: {iteration}")
        c.after(algorhitm_speed, update_grid)
    except StopIteration:
        stop_label.place(x=200, y=s_height+50)
        #stop_label.configure(state='normal')



def init_solver():
    global matrix_pos
    global final_matrix
    #global iteration_label
    iteration_label.place(x=250, y=s_height+10)
    #iteration_label.configure(state='normal')
    submitbutton.place_forget()
    #submitbutton.configure(state='disabled')

    for text in label_dict:
        if not label_dict[text].get("1.0", "end-1c") == '': #check if no number has been assigned
            nonzero_positions.append(int(text[8:]))
            first[int(text[8])][int(text[9])] = int(label_dict[text].get("1.0", "end-1c"))
        label_dict[text].destroy()
    # print(nonzero_positions)
    # print(numpy.matrix(first))


    for i in range(9):
        for j in range(9):
            label_dict[f"my_label{i}{j}"] = tkinter.Label(c)
            y_pos = ((s_height/9)*i+(s_height/9)*(i+1))/2 - 17
            x_pos = ((s_width/9)*j+(s_width/9)*(j+1))/2 - 10
            label_dict[f"my_label{i}{j}"].place(x=x_pos, y=y_pos)
            if int(f"{i}{j}") in nonzero_positions:
                label_dict[f"my_label{i}{j}"].config(text=f"{first[i][j]}", font=sudoko_font,
                                                     background='white', fg='black')
            else:
                label_dict[f"my_label{i}{j}"].config(text=f"{first[i][j]}", font=sudoko_font,
                                                  background='white', fg='white')

    solveex()
    print(len(matrix_iterations))
    final_matrix = find_solution()
    if final_matrix is None:
        iteration_label.place_forget()
        submitbutton.place_forget()
        sudoko_font.config(size=16)
        error_message = tkinter.Label(c, text="The sudoku is unsolveable, please press restart and insert correct numbers"
                                        , font=sudoko_font,
                                        background='white', fg='black')
        error_message.place(x=50, y=s_height+20)
        return

    print(final_matrix)
    # print(numpy.matrix(matrix_iterations[final_matrix]))
    matrix_pos = get_matrix_pos()
    c.after(1000, update_grid)
    c.mainloop()


def restart():
    global first, nonzero_positions, matrix_iterations, label_dict
    #submitbutton.configure(state='normal')
    submitbutton.place(x=s_width/6.5, y=s_height+10)
    iteration_label.place_forget()
    stop_label.place_forget()
    nonzero_positions = []
    matrix_iterations = []
    label_dict = {}

    first = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    #iteration_label.configure(state='disabled')
    for i in range(10):
        if i == 0:
            c.create_line([((s_height/9)*i, 0), ((s_height/9)*i, s_width)], tag='grid_line', width=20)
            c.create_line([(0, (s_width/9)*i), (s_height, (s_width/9)*i)], tag='grid_line', width=20)
        elif i % 3 == 0:
            c.create_line([((s_height/9)*i, 0), ((s_height/9)*i, s_width+5)], tag='grid_line', width=10)
            c.create_line([(0, (s_width/9)*i), (s_height+5, (s_width/9)*i)], tag='grid_line', width=10)
        else:
            c.create_line([((s_height/9)*i, 0), ((s_height/9)*i, s_width)], tag='grid_line', width=5)
            c.create_line([(0, (s_width/9)*i), (s_height, (s_width/9)*i)], tag='grid_line', width=5)
        c.pack(fill=tkinter.BOTH, expand=True)

    for i in range(9):
        for j in range(9):
            label_dict[f"init_num{j}{i}"] = tkinter.Text(c, font=sudoko_font, background='white', fg='black',
                                                         height=1, width=2)
            label_dict[f"init_num{j}{i}"].place(x=(s_height/28)+((s_height/9.1)*i), y=(s_height/28)+((s_height/9.1)*j))





# first_ex = [[5, 3, 0, 0, 7, 0, 0, 1, 0],
#             [6, 0, 0, 1, 0, 5, 0, 0, 0],
#             [0, 9, 8, 0, 0, 0, 0, 6, 0],
#             [8, 0, 0, 0, 6, 0, 0, 0, 3],
#             [4, 0, 0, 8, 0, 3, 0, 0, 1],
#             [7, 0, 0, 0, 2, 0, 0, 0, 6],
#             [0, 6, 0, 0, 0, 0, 2, 8, 0],
#             [0, 0, 0, 4, 1, 9, 0, 0, 5],
#             [0, 0, 0, 0, 8, 0, 0, 7, 9]]

if __name__ == "__main__":

    algorhitm_speed = 5
    first = []
    mainWindow = tkinter.Tk()
    mainWindow.title("Sudoku_solver")
    mainWindow.geometry('610x700')
    s_height = 600
    s_width = 600
    sudoko_font = tkinter.font.Font(size=22)
    c = tkinter.Canvas(mainWindow, height=s_height, width=s_width, bg='white')
    submitbutton = tkinter.Button(c, text="Press to solve sudoku", font=sudoko_font
                                  , width=25, command=init_solver)
    iteration_label = tkinter.Label(mainWindow, text=f"Current run: {0}", font=sudoko_font,
                                    background='white', fg='black')
    stop_label = tkinter.Label(c, text="The algorithm has finished", font=sudoko_font,
                               background='white', fg='black')
    restart_button = tkinter.Button(c, text="Press to restart", background='white', fg='blue', command=restart)
    restart_button.place(x=10, y=s_height+70)

    restart()

    c.mainloop()









