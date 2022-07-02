from tkinter import *
from tkinter import messagebox

class complexNumber:
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary

    def add(self, r, i):
        return complexNumber(self.real + r,self.imaginary + i)


    def subtract(self, r, i):
        return complexNumber(self.real - r, self.imaginary - i)


    def multiply(self, r, i):
        return complexNumber(self.real * r - self.imaginary * i, self.real * i + self.imaginary * r)


    def showNumber(self):
        return (self.real, self.imaginary)


    def conjugate(self):
        return complexNumber(self.real, - self.imaginary)


def convertToString(complex):
    real = complex.real
    imaginary = complex.imaginary
    if imaginary > 0:
        text = str(real) + " + j" + str(imaginary)
    elif imaginary < 0:
        text = str(real) + " - j" + str(-imaginary)
    else:
        text = str(real)
    return text


def multiply(num1, num2):
    real = num2.real
    imaginary = num2.imaginary
    return num1.multiply(real,imaginary)


def subtract(num1, num2):
    real = num2.real
    imaginary = num2.imaginary
    return num1.subtract(real, imaginary)


def add(num1, num2):
    real = num2.real
    imaginary = num2.imaginary
    return num1.add(real, imaginary)


def divide(num1, num2):
    real = num2.real
    imaginary = num2.imaginary
    denominator = 1/(real**2 + imaginary**2)
    result = num1.multiply(real, -imaginary)
    result = result.multiply(denominator, 0)
    return result


def convertToComplex(string):
    string = string.lower()
    string = string.replace(" ","")
    if string.find("j") == -1:
        real = float(string)
        return complexNumber(real, 0)
    for i in range(len(string)):
        if string[i] == "j":
            break
    if i == 0 or i==1:
        imaginary = string.replace("j", "")
        imaginary = float(imaginary)
        return complexNumber(0, imaginary)
    real = string[:i-1]
    imaginary = string[i-1:]
    imaginary = imaginary.replace("j", "")
    real = float(real)
    imaginary = float(imaginary)
    return complexNumber(real, imaginary)


def subMatrix(matrix, row, column):
    newMatrix = []
    newRow = []
    for i in range(len(matrix)):
        if i == row:
            continue
        for j in range(len(matrix[i])):
            if j == column:
                continue
            newRow.append(matrix[i][j])
        newMatrix.append(newRow)
        newRow = []
    return newMatrix


def determinate(matrix):
    if len(matrix[0]) == 2:
        return subtract(multiply(matrix[0][0], matrix[1][1]), multiply(matrix[0][1], matrix[1][0]))
    else:
        sum = complexNumber(0, 0)
        for i in range(len(matrix[0])):
            sum = add(sum, multiply(matrix[0][i].multiply((-1)**i, 0), determinate(subMatrix(matrix, 0, i))))
        return sum


def replaceMatrix(matrixA, matrixB, column):
    matrixC = []
    row = []
    for i in range(len(matrixA)):
        for j in range(len(matrixA[i])):
            if j == column:
                row.append(matrixB[i])
                continue
            row.append(matrixA[i][j])
        matrixC.append(row)
        row = []
    return matrixC


def solve(matrix):
    coefficientMatrix = []
    constants = []
    for i in range(len(matrix)):
        coefficientMatrix.append(matrix[i][:-1])
        constants.append(matrix[i][-1])
    delta = determinate(coefficientMatrix)
    deltas = []
    for i in range(len(coefficientMatrix[0])):
        deltas.append(determinate(replaceMatrix(coefficientMatrix, constants, i)))
    for i in range(len(deltas)):
        deltas[i] = divide(deltas[i], delta)
    return deltas


def printComplexList(list):
    for i in list:
        print(i.showNumber())


body = Tk()
body.geometry("350x100")
body.title("CSES")


def createInterface(variables):
    def calculate(variables):
        try:
            matrix = []
            print(inputEntries)
            for i in range(variables):
                row = []
                for j in range(variables+1):
                    row.append(convertToComplex(inputEntries[i][j].get()))
                matrix.append(row)
            values = solve(matrix)
            for i in range(len(values)):
                values[i] = convertToString(values[i])
            text = ""
            for i in range(len(values)):
                text += "X" + str(i) + " = " + values[i] + "\n"
            messagebox.showinfo("Solved!", text)
        except:
            messagebox.showerror("Error", "Wrong Inputs")
        return
    geometry = str((variables)*300) + "x" + str(variables*50)
    body.geometry(geometry)
    inputEntries = []
    calculateButton = Button(body, text="Calculate", command=lambda:calculate(variables))
    calculateButton.grid(row=variables, column=(variables*2), padx=10, pady=10)
    for i in range(variables):
        row = []
        for j in range(variables + 1):
            row.append(Entry(body))
        inputEntries.append(row)
    counter = 0
    for i in range(variables):
        counter = 0
        for j in range(1, (variables)*2, 2):
            if counter == variables - 1:
                text = "X" + str(counter) + " = "
            else:
                text = "X" + str(counter) + " + "
            Label(body, text=text).grid(row=i, column=j)
            counter += 1
    for i in range(variables):
        counter = 0
        for j in range(0, (variables+1)*2, 2):
            inputEntries[i][counter].grid(row=i, column=j, padx=10, pady= 10)
            counter+=1
    return


def start():
    try:
        variables = mainEntry.get()
        variables = int(variables)
        titleLabel.destroy()
        mainEntry.destroy()
        runButton.destroy()
        createInterface(variables)
    except:
        messagebox.showerror("Error", "Wrong Input")


titleLabel = Label(body, text="Enter the number of variables", padx=10, pady=10)
titleLabel.grid(row=0, column=0)
mainEntry = Entry(body)
mainEntry.grid(row=0, column=1, padx=10, pady=10)
runButton = Button(body, text="Run", command=start)
runButton.grid(row=1, column=1, padx=10, pady=10)
body.mainloop()