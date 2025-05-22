# S7 - Natural Computation: Estimation of Distribution Algorithms for the Traveling Salesman Problem

This repository contains the practical work and results from the "S7 - Natural Computation" seminar, part of the Master's Degree in Artificial Intelligence (MUIA) at the Polytechnic University of Madrid (UPM). The seminar was imparted by Pedro Larrañaga, Alfonso Rodriguez Patón and Alfonso Mateos.

The project explores the application of Estimation of Distribution Algorithms (EDAs) using the EDAspy library to solve the classic Traveling Salesman Problem (TSP).

## Table of Contents
1.  [Introduction](#introduction)
2.  [Key Concepts](#key-concepts)
    *   [Estimation of Distribution Algorithms (EDAs)](#estimation-of-distribution-algorithms-edas)
    *   [Traveling Salesman Problem (TSP)](#traveling-salesman-problem-tsp)
    *   [EDAspy Library](#edaspy-library)
3.  [Implementation Details](#implementation-details)
    *   [Virtualization](#virtualization)
    *   [TSP Instances (`tsp95lib`)](#tsp-instances-tsp95lib)
    *   [Problem Representation](#problem-representation)
4.  [Results](#results)
    *   [Hyperparameter Exploration](#hyperparameter-exploration)
    *   [Comparison with Other EDAs](#comparison-with-other-edas)
5.  [Conclusions](#conclusions)
6.  [References](#references)
7.  [Authors](#authors)

## Introduction

This project focuses on applying and exploring Estimation of Distribution Algorithms (EDAs) for the Traveling Salesman Problem (TSP), a well-known combinatorial optimization challenge. The work utilizes the open-source Python library `EDAspy` to implement and test various EDA variants.

## Key Concepts

### Estimation of Distribution Algorithms (EDAs)

EDAs are a class of evolutionary computation algorithms that replace traditional genetic operators (like crossover and mutation) with the learning and sampling of a probabilistic model. The core idea is to capture the dependency structure between variables in high-quality solutions found so far and use this information to generate new, promising solutions.

A typical EDA cycle includes:
1.  **Initialization:** Generating an initial population.
2.  **Evaluation:** Assessing the quality (cost or fitness) of each individual.
3.  **Selection:** Choosing the best individuals from the population.
4.  **Probabilistic Model Learning:** Building a model from the selected individuals to represent the distribution of high-quality solutions.
5.  **Sampling:** Generating a new population by sampling from the learned probabilistic model.
6.  **Stop Condition:** Terminating the algorithm when a criterion is met.

EDAs can handle various variable types (binary, categorical, continuous) and model dependencies with different levels of complexity.

### Traveling Salesman Problem (TSP)

The TSP is a classic NP-hard combinatorial optimization problem. Given a list of cities and the distances between each pair of cities, the goal is to find the shortest possible route that visits each city exactly once and returns to the origin city. Due to its computational difficulty, TSP serves as a common benchmark for optimization algorithms, including EDAs.

### EDAspy Library

`EDAspy` is an open-source Python library designed to simplify the implementation and experimentation with EDAs. It provides a modular and extensible framework, allowing researchers and developers to easily apply different EDA variants to optimization problems. While primarily focused on continuous optimization, `EDAspy` also includes implementations for binary and categorical variables.

Key EDA implementations available in `EDAspy` include:
*   `UMDAd`: Univariate Marginal Distribution Algorithm (binary)
*   `UMDAc`: Univariate Marginal Distribution Algorithm (continuous)
*   `UnivariateKEDA`: Univariate Kernel Estimation of Distribution Algorithm (continuous)
*   `UMDAcat`: Univariate Marginal Distribution Algorithm (categorical)
*   `EGNA`: Estimation of Gaussian Distribution Algorithm (continuous, Gaussian Bayesian Network)
*   `EMNA`: Estimation of Multivariate Normal Algorithm (continuous, Multivariate Normal distribution)
*   `SPEDA`: Semiparametric Estimation of Distribution Algorithm (multivariate, KDE and Gaussians)
*   `MultivariateKEDA`: Special case of SPEDA using only KDE
*   `EBNA`: Estimation of Bayesian Network Algorithm (categorical, Bayesian Network)
*   `BOA`: Bayesian Optimization Algorithm (categorical, Bayesian Network with specific scoring)
*   `PBIL`: Population-based Incremental Learning (modification of UMDA)

## Implementation Details

### Virtualization

For reproducibility of results, a virtualized environment created with Anaconda was used during development. The specific environment configuration is provided in the `environment.yml` file.

### TSP Instances (`tsp95lib`)

To standardize performance measurement, the `tsp95lib` library [Reinelt, 1991] was utilized. This library offers a collection of TSP instances, many with known optimal costs and varying complexities (from 70 to 2392 cities). The following instances were used for testing:

| `problem_name` | `optimal_cost` | `size` |
| :------------- | :------------- | :----- |
| `st70`         | 675            | 70     |
| `pr76`         | 108159         | 76     |
| `rd100`        | 7910           | 100    |
| `lin105`       | 14379          | 105    |
| `tsp225`       | 3916           | 225    |
| `pcb442`       | 50778          | 442    |
| `pr1002`       | 259045         | 1002   |
| `pr2392`       | 378032         | 2392   |

### Problem Representation

To apply continuous EDAs to the permutational nature of TSP, a continuous vector representation was adopted. A route is encoded as a vector `v = [v_0, v_1, ..., v_{N-1}]`, where `N` is the number of cities. Each position `i` in `v` is uniquely associated with a city, and its continuous value `v_i` represents a "priority" or "preference" for that city.

The decoding process to transform `v` into a valid TSP permutation is as follows:
1.  Create a list of pairs `(continuous_value, city_index)`.
2.  Sort this list of pairs based on their `continuous_value`.
3.  The permutation of cities (the route) is then obtained by taking the `city_index` values in the sorted order. The city with the lowest `v_i` becomes the first city in the route, and so on.

This representation guarantees the generation of valid permutations (no repeated or omitted cities), simplifying the optimization process and enabling the use of continuous EDAs like `UMDAc`, `EGNA`, and `EMNA` from `EDAspy`.

## Results

### Hyperparameter Exploration

The impact of two key hyperparameters of the `UMDAc` algorithm (`size_gen` - population size, and `alpha` - selection percentage) was explored using the `st70` TSP instance (optimal cost: 675).

*   **`size_gen` (Population Size):** Demonstrated a significant positive impact on solution quality. Insufficient `size_gen` (e.g., 10 or 20) led to substantially higher costs, as a small population limits the sample space and hinders the probabilistic model's ability to represent the distribution of high-quality solutions effectively.
*   **`alpha` (Selection Percentage):** Influenced selective pressure.
    *   Very low `alpha` (e.g., 0.1 or 0.2), especially with a small `size_gen`, resulted in poor performance and premature convergence to suboptimal regions.
    *   Intermediate to high `alpha` values (approximately 0.4 to 0.8) consistently yielded better results, striking a balance between exploiting the best solutions and exploring the search space.

The study confirmed the stochastic nature of these algorithms, highlighting that a single run might not always find the optimal solution even with appropriate parameters.

### Comparison with Other EDAs

A comparison was made between `UMDAc` (univariate, assumes variable independence) and `EMNA` (multivariate, models variable dependencies) using the continuous representation on the `st70` instance.

Contrary to theoretical expectations (where `EMNA` might be more suitable due to its ability to model dependencies), `UMDAc` consistently produced better quality solutions within the explored parameter space for this specific instance. `EMNA` was observed to often get stuck prematurely in local optima. This suggests that the practical performance of multivariate models can depend significantly on the problem instance, the chosen representation, and the robustness of the specific algorithm implementation.

## Conclusions

This practical work successfully applied and explored `EDAspy`'s Estimation of Distribution Algorithms for the Traveling Salesman Problem, a classic combinatorial optimization challenge.

Key findings include:
*   The viability of using a continuous vector representation with an ordering-based decoding process was validated for adapting the TSP's permutational structure to continuous optimization algorithms available in `EDAspy`. This approach ensures the generation of valid permutations.
*   Hyperparameter exploration for `UMDAc` on the `st70` instance emphasized the critical importance of `size_gen` (population size) and `alpha` (selection parameter). A sufficiently large population and intermediate-to-high `alpha` values are essential for optimal performance, balancing exploitation and exploration. The stochastic nature of EDAs and the need for parameter tuning for each problem were confirmed.
*   An unexpected result emerged from the comparison between `UMDAc` (univariate) and `EMNA` (multivariate); `UMDAc` consistently achieved better solutions for the `st70` instance. This indicates that while multivariate models may offer greater theoretical potential by modeling dependencies, their practical performance can heavily rely on the specific problem instance, the chosen representation, and the robustness of the algorithm's implementation.

Overall, the experience with `EDAspy` for TSP reinforces the understanding of EDA mechanisms, the crucial role of problem representation, and the necessity of empirical experimentation to validate algorithm behavior on specific instances.

## References

*   Mühlenbein, H., and Paass, G. (1996). "From recombination of genes to the estimation of distributions i. binary parameters." In *International conference on parallel problem solving from nature*, pages 178-187. Springer.
*   Reinelt, G. (1991). "Tsplib—a traveling salesman problem library." *ORSA Journal on Computing*, 3(4):376-384.
*   Soloviev, V. P., Larrañaga, P., and Bielza, C. (2024). "Edaspy: An extensible python package for estimation of distribution algorithms." *Neurocomputing*, 598:128043.

## Authors

*   Kevin Oscar Arce Vera (kevin.avera@alumnos.upm.es)

**MUIA - Máster Universitario en Inteligencia Artificial**
**Mayo 2025**