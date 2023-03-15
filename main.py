import sys
import random
from evol import Population, Evolution
from PIL import Image, ImageDraw, ImageChops

Max = 255 * 200 * 200
Target = Image.open("3b.png")
Target.load()


def make_polygon(n):
    #0 <= R|G|B < 256, 30 <= A <= 60, 10 <= x|y < 190
    rgba = (random.randint(0,256), random.randint(0,256), random.randint(0,256), random.randint(30,60))
    polygon = []
    polygon.append(rgba)
    for i in range (0, n):
        (x, y) = (random.randint(10, 190), random.randint(10, 190))
        polygon.append((x,y))
    return (polygon)

def initialise_polygons(n):
    return [make_polygon(n) for i in range(100)]

def draw(polygon):
    image = Image.new("RGB", (200, 200))
    canvas = ImageDraw.Draw(image, "RGBA")
    #print(polygon)
    canvas.polygon(polygon[1:], fill=polygon[0])
    return image

def select_polygons(polygons):
    return [random.choice()]



def evaluate(solution):
    #print(solution)
    image = draw(solution)
    #image.show()
    diff = ImageChops.difference(image, Target)
    hist = diff.convert("L").histogram()
    count = sum(i * n for i, n in enumerate(hist))
    #print((Max-count) / Max)
    return (Max-count) / Max


def mutate(solution, sigma):
    if random.random() < 0.5:
        # mutate points
        polygon = solution
        print(polygon)
        for i in range(0, len(polygon)):
            for j in range(0, len(polygon[i])):
                print(polygon[i][j])
                if i == 0 and j != 3:
                    polygon[i][j] = random.randint(0,256)
                elif j == 3:
                    polygon[i][j] = random.randint(30,60)
                else:
                    polygon[i][j] = random.randint(10, 190)



    return solution

def get_solution(population):
    solution = []
    for i in range(0, 100):
        solution.append(population[i].chromosome)
    return solution



def run(generations=50, seed=31):
    random.seed(seed)

    evo = (Evolution()
           .survive(fraction=1)
           .mutate(mutate_function=mutate, sigma=1)
           .evaluate())

    population = Population(chromosomes=initialise_polygons(3), eval_function=evaluate)
    print(population)
    #img = draw(population)
    #img.show()
    #solutionimg = draw(get_solution(population))
    #solutionimg.show()


    for i in range(generations):
        population = population.evolve(evo, n=1)
        #print(f"the best score found: {max([i.fitness for i in population])}")

    print(population)







def func_to_optimise(xy):
    """
    This is the function we want to optimise (maximize)
    """
    print(xy)
    x, y = xy
    return -(1 - x) ** 2 - (2 - y ** 2) ** 2

def random_start():
    """
    This function generates a random (x,y) coordinate
    """
    return (random.random() - 0.5) * 20, (random.random() - 0.5) * 20

def pick_random_parents(pop):
    """
    This is how we are going to select parents from the population
    """
    mom = random.choice(pop)
    dad = random.choice(pop)
    return mom, dad

def make_child(mom, dad):
    """
    This function describes how two candidates combine into a
    new candidate. Note that the output is a tuple, just like
    the output of `random_start`. We leave it to the developer
    to ensure that chromosomes are of the same type.
    """
    child_x = (mom[0] + dad[0]) / 2
    child_y = (mom[1] + dad[1]) / 2
    return child_x, child_y

def add_noise(chromosome, sigma):
    """
    This is a function that will add some noise to the chromosome.
    """
    new_x = chromosome[0] + (random.random() - 0.5) * sigma
    new_y = chromosome[1] + (random.random() - 0.5) * sigma
    return new_x, new_y

pop = Population(chromosomes=[random_start() for _ in range(200)],
                 eval_function=func_to_optimise, maximize=True)



# We define a sequence of steps to change these candidates
evo1 = (Evolution()
        .survive(fraction=0.5)
        .breed(parent_picker=pick_random_parents, combiner=make_child)
        .mutate(mutate_function=add_noise, sigma=1))

# We define another sequence of steps to change these candidates
evo2 = (Evolution()
        .survive(n=1)
        .breed(parent_picker=pick_random_parents, combiner=make_child)
        .mutate(mutate_function=add_noise, sigma=0.2))

# We are combining two evolutions into a third one.
# You don't have to but this approach demonstrates
# the flexibility of the library.
evo3 = (Evolution()
        .repeat(evo1, n=50)
        .repeat(evo2, n=10)
        .evaluate())

# This is inelegant but it works.
for i in range(0):
    pop = pop.evolve(evo3, n=5)
    print(pop)
    print(f"the best score found: {max([i.fitness for i in pop])}")



run()