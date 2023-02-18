import random



def fitness(individual, target):
    """
    Prend en entrée une chaîne individuelle et la chaîne cible, et retourne le nombre de caractères qui
    correspondent entre les deux
    """
    return sum(1 for expected, actual in zip(target, individual)
            if expected == actual)


def get_fitness(genes, target):
    """
    Evalue l'aptitude de la chaîne générée
    """
    fitness = sum(1 for expected, actual in zip(target, genes) if expected == actual)
    return fitness


def generate_individual(self, length, gene_set, get_fitness):
    """
    Génère aléatoirement une chaîne individuelle en utilisant les caractères dans gene_set
    """
    genes = [random.choice(gene_set) for _ in range(length)]
    fitness = get_fitness(genes)
    return genes, fitness


def mutate(individual, gene_set, get_fitness):
    """
    Modifie une chaîne individuelle en remplaçant aléatoirement un caractère par un autre caractère dans gene_set
    """
    child_genes = list(individual[0])
    index = random.randrange(0, len(child_genes))
    new_gene, alternate = random.sample(gene_set, 2)
    child_genes[index] = alternate if new_gene == child_genes[index] else new_gene
    fitness = get_fitness(child_genes)
    return child_genes, fitness


def crossover(parent_1, parent_2):
    """
    Crée deux nouveaux individus en combinant les chaînes des parents. Le point de coupure est choisi aléatoirement
    """
    if len(parent_1[0]) <= 1:
        return parent_1
    index = random.randrange(1, len(parent_1[0]))
    
    child_1 = (parent_1[0][:index] + parent_2[0][index:], parent_1[1])
    child_2 = (parent_2[0][:index] + parent_1[0][index:], parent_2[1])
    return child_1, child_2


def get_best(get_fitness, target_len, optimal_fitness, gene_set, display, max_generations, crossover_rate):
    """
    Implémente le processus de programmation génétique. Elle génère aléatoirement des chaînes individuelles, les modifie par mutation ou croisement, et garde toujours la chaîne la plus apte.
    """
    random.seed()
    best_parent = generate_individual(target_len, gene_set, get_fitness)
    display(best_parent)
    if best_parent[1] >= optimal_fitness:
        return best_parent
    
    if random.random() < crossover_rate:
        child_1, child_2 = crossover(best_parent, generate_individual(target_len, gene_set, get_fitness))
        child_1 = mutate(child_1, gene_set, get_fitness)
        child_2 = mutate(child_2, gene_set, get_fitness)
        if child_1[1] > best_parent[1]:
            best_parent = child_1
            display(best_parent)
            if best_parent[1] >= optimal_fitness:
                return best_parent
        if child_2[1] > best_parent[1]:
            best_parent = child_2
            display(best_parent)
            if best_parent[1] >= optimal_fitness:
                return best_parent
    else:
        child = mutate(best_parent, gene_set, get_fitness)
        if child[1] > best_parent[1]:
            best_parent = child
            display(best_parent)
            if best_parent[1] >= optimal_fitness:
                return best_parent
    return best_parent


"""def main():
    gene_set = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!."
    target = "Hello, World!"
    target_len = len(target)
    optimal_fitness = len(target)

    def display(individual):
        genes = ''.join(individual[0])
        print(f"{genes}\t{individual[1]}")

    best = get_best(lambda x: fitness(x, target), target_len, optimal_fitness, gene_set, display, max_generations=1000,
                    crossover_rate=0.5)
    print(f"Best individual: {''.join(best[0])}\tFitness: {best[1]}")


if __name__ == '__main__':
    main()
"""
