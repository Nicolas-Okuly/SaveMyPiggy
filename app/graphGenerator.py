import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os, sys

matplotlib.use('Agg')

from matplotlib import rcParams

# Get the absolute path to the resource, for PyInstaller
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

rcParams["font.weight"] = "bold"
rcParams["font.size"] = 16

# Graph generator class
class GraphGenerator():
    def incvexpGraph(self, income: float, expense: float):
        '''
            Create and style the income vs outcome bar graph
            then save it to app/views/graphs as incomevexpense.svg
        '''
        plt.figure(figsize=(6, 3))
        plt.barh(["Expense", "Income"], [expense, income], color=["darkred", "green"])
        plt.title("Income vs. Expenses", fontweight="bold")
        plt.xlabel("U.S. dollars", fontweight="bold")
        plt.tight_layout()
        plt.savefig(resource_path("views/graphs/incomevexpense.svg"), transparent=True)
        plt.clf()
        plt.close()

    def ExpenseCatPie(self, trans: list, categories: list):
        '''
            Turn the list of expenses, mapped to the list, into a 
            functional pie chart
        '''
        y = np.array(trans)
        rcParams["font.weight"] = "normal"
        plt.pie(y, labels=categories)
        # plt.title("Expenses Chart", fontweight="bold")
        plt.tight_layout()
        plt.savefig(resource_path("views/graphs/expense-pie.svg"), transparent=True)
        plt.clf()
        plt.close()

    def IncomeCatPie(self, trans: list, categories: list):
        '''
            Turn the list of income, mapped to the list, into a
            function pie chart
        '''
        y = np.array(trans)
        rcParams["font.weight"] = "normal"
        plt.pie(y, labels=categories)
        # plt.title("Income Chart", fontweight="bold")
        plt.tight_layout()
        plt.savefig(resource_path("views/graphs/income-pie.svg"), transparent=True)
        plt.clf()
        plt.close()