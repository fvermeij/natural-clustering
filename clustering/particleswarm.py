__author__ = 'Fenno'

from clustering import Clustering
from app.score import score, getlabels
from numpy.random import randint, rand
from numpy import zeros, shape, max, argmax, copy


class ParticleSwarmCluster(Clustering):

    def __init__(self, n_particles=10, n_iterations=1000, w=0.72, c1=1.49, c2=1.49, norm=2):
        self.n_particles = n_particles
        self.n_iterations = n_iterations
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.norm = norm

    def cluster(self, data, n_clusters):

        n, d = shape(data)
        locations = zeros((self.n_particles, n_clusters, d))
        bestlocations = copy(locations)

        for i in range(self.n_particles):
            for j in range(n_clusters):
                locations[i, j, :] = data[randint(n), :]  # Initialize cluster centers to random datapoints

        velocities = zeros((self.n_particles, n_clusters, d))

        bestscores = [score(data, centroids=locations[i, :, :], norm=self.norm) for i in range(self.n_particles)]
        sbestlocation = locations[argmax(bestscores), :, :]
        sbestscore = max(bestscores)

        for i in range(self.n_iterations):
            if i % 100 == 0:
                print "Iteration", i, "best score:", sbestscore
            for j in range(self.n_particles):
                r = rand(n_clusters, d)
                s = rand(n_clusters, d)
                velocities[j, :, :] = (self.w * velocities[j, :, :]) + \
                                      (self.c1 * r * (bestlocations[j, :, :] - locations[j, :, :])) + \
                                      (self.c2 * s * (sbestlocation - locations[j, :, :]))
                locations[j, :, :] = locations[j, :, :] + velocities[j, :, :]
                currentscore = score(data, centroids=locations[j, :, :], norm=self.norm)
                if currentscore < bestscores[j]:
                    bestscores[j] = currentscore
                    bestlocations[j, :, :] = locations[j, :, :]
                    if currentscore < sbestscore:
                        sbestscore = currentscore
                        sbestlocation = locations[j, :, :]

        return getlabels(data, centroids=sbestlocation, norm=self.norm)
