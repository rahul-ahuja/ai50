import sys
from collections import deque, defaultdict
from crossword import *

#todo: if stuck for too long, try out these efficiency on scheduling demo problem, 
#assignment is {variable: word (not list of words)} but self.domain has {variable: list of words}


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        #print(self.domains)
        #v1 = Variable(6, 5, 'across', 6)
        #v2 = Variable(1, 7, 'down', 7)
        #print(self.crossword.neighbors(v2))
        #print(self.domains[v1])
        #print(self.domains[v2])
        #print(self.revise(v1, v2))
        #print(self.domains[v1])
        #print(self.domains[v2])

        self.ac3()
        #print(self.domains)
        return self.backtrack(dict())


    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        
        #raise NotImplementedError
        """
        for word in self.crossword.words:
            for variable in self.crossword.variables:
                if len(word) != variable.length:
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.
        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        #raise NotImplementedError
        revised = False
        if y not in self.crossword.neighbors(x):
            #print('no overlap')
            return revised  # No overlap, no need to revise
        else:
            i, j = self.crossword.overlaps[x, y]
            #print('i, j: ', i, j)

        x_words_set = self.domains[x].copy()
        
        for x_word in x_words_set:
            arc_consistent = False
            for y_word in self.domains[y]:
                if x_word[i] == y_word[j]:
                    arc_consistent = True
                    break
                
            if not arc_consistent:
                self.domains[x].remove(x_word)
                revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        #raise NotImplementedError
    
        if arcs is None:
            queue = deque()
            for x in self.crossword.variables:
                for y in self.crossword.neighbors(x):
                    queue.append((x, y))
        else:
            queue = deque(arcs)
    
        while queue:
            x, y = queue.popleft()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.append((z, x))
        return True
    

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        #raise NotImplementedError
        if len(self.crossword.variables) != len(assignment):
            return False
        
        for variable in assignment:
            if len(assignment[variable]) == 0:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        
        """
        #raise NotImplementedError
        words_set = set()
        for variable, word in assignment.items():
            if word in words_set:
                return False
            words_set.add(word)
            if len(word) != variable.length:
                return False
            for neighbor_variable in self.crossword.neighbors(variable):
                i, j = self.crossword.overlaps[variable, neighbor_variable]
                if neighbor_variable in assignment:
                    word2 = assignment[neighbor_variable]
                    if word[i] != word2[j]:
                        return False
            
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        
        #raise NotImplementedError        
        """
        domain_count = {word:0 for word in self.domains[var]}
        for neighbor_var in self.crossword.neighbors(var):
            if neighbor_var in assignment:
                i, j = self.crossword.overlaps[var, neighbor_var]
                for word in self.domains[var]:
                    for neighbor_word in self.domains[neighbor_var]:
                        if word[i] != neighbor_word[j]:
                            domain_count[word] -= 1
        ordered_domain = sorted(domain_count.items(), key= lambda x:x[1])

        return [x[0] for x in ordered_domain]
        #return self.domains[var]        


    def remain_values_degrees(self, variables: list) -> dict:
        return {variable: (len(self.domains[variable]), 
                           -len(self.crossword.neighbors(variable))) for variable in variables}


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        
        #raise NotImplementedError
        """    
        unassigned_variables = []
        for variable in self.crossword.variables:
            if variable not in assignment:
                unassigned_variables.append(variable)

        if not unassigned_variables:
            return None
        

        rv_degrees = self.remain_values_degrees(unassigned_variables)
        mrv_degrees = sorted(rv_degrees.items(), key=lambda x: (x[1][0], x[1][1]))
        return mrv_degrees[0][0]
    
        #for variable in self.crossword.variables:
        #    if variable not in assignment:
        #        return variable
        #return None

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        if self.assignment_complete(assignment):
            return assignment
        
        #print('assignment: ', assignment)
        variable = self.select_unassigned_variable(assignment)
        #print(variable)
        for value in self.order_domain_values(variable, assignment):
            new_assignment = assignment.copy()
            new_assignment[variable] = value
            #print('new assignment: ', new_assignment)
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
                #pass

        return None
        #raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    #print(crossword.words)
    #print(crossword.variables)
    
    creator = CrosswordCreator(crossword)
    #v1 = crossword.variables.pop()
    #print(v1)
    #v2 = crossword.variables.pop()
    #print(creator.domains[v1])
    #print(creator.domains[v2])
    #print(creator.revise(v1, v2))
    assignment = creator.solve()
    # Print result
    
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)
    
if __name__ == "__main__":
    main()
