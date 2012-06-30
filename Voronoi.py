import sys, os
sys.path.insert( 0, r'\Users\ksuvee\Documents\Density_project\objreader' )

from Grid import *
from primitives import Vector2
import numpy as np
import pylab as plt

class Voronoi:
    """ A class to partition world space into Voronoi region with agent's radius constraint """
    def __init__( self, minCorner, size, resolution  ):
        """ frame is a list of agent in the world at that point in time; worldGrid"""
        self.minCorner = minCorner
        self.size = size
        self.resolution = resolution
        # Store shortest distance initally every cells has infinitely far away from agents
        self.distGrid = DataGrid( minCorner, size, resolution, 10000. )
        # Store index indicating who own the grid initially all the cells don't have any owner
        self.ownerGrid = DataGrid( minCorner, size, resolution, -1 )
    
    def distField( self, points, testPoint ):
       '''computes the distance to testPoint of all the positions defined in points.

        @param points:  an NxNx2 numpy array such that [i,j,:] is the x & y positions of the
                    cell at (i, j)
        @param testPoint: an 2x1 numpy array of the test point.
        @returns an NxNx1 numpy array of the distances to testPoint.
        '''
       testPoint.shape = (1, 1, 2)
       disp = points - testPoint
       dist = np.sqrt( np.sum( disp * disp, axis=2 ) )
       return dist
    
    def computeVoronoi( self, worldGrid, frame, agentRadius=1 ):
        ''' Compute Voronoi region for particular frame
        @param worldGrid: discrete world in grid form
        @param frame: a NX2 storing agents' position
        @agentRaidus: uniform agenet radius for each one
        '''
        if (frame.shape[0] != 0):
            centers = worldGrid.getCenters()
            # Calculate distance from agent[0] to eery cell in the grid
            pos = frame[0,:]
            # Swapping the x,y to map the with the color
            self.distGrid.cells[:,:] = self.distField( centers, np.array((pos[1],pos[0])) )
            # if the distance is with in agent's radius then the cell belong to agent[0]
            region = self.distGrid.cells <= agentRadius
            # Assign the cell's owner to be agent[0]
            self.ownerGrid.cells[ region ] = 0
            for i in xrange( 1, frame.shape[0] ):
                pos = frame[i, :]
                workDist = self.distField( centers, np.array((pos[1],pos[0])) )
                region = (self.distGrid.cells > workDist) & (workDist <= agentRadius)
                self.distGrid.cells[ region] = workDist[ region ]
                self.ownerGrid.cells[ region ] = i
            
    def computeVoronoiDensity( self, worldGrid, frame, agentRadius=1 ):
        ''' Compute Voronoi region for each agent and then calculate density in that region'''
        # Compute Voronoi region for current frame
        # Store density in each cell of Voronoi region using 1/A
        densityGrid = Grid( self.minCorner, self.size, self.resolution, initVal=0 )
        self.computeVoronoi( worldGrid, frame, agentRadius)
##        plt.imshow(  self.ownerGrid.cells[::-1, :] )
##        plt.show()
        for i in xrange( 0, frame.shape[0] ):
            areaMask = self.ownerGrid.cells == i
            area = areaMask.sum()
            densityGrid.cells[areaMask] = (1./area)
##            print "area " + str(area)
##            print "den " + str(1./area)
##            print densityGrid.cells[areaMask]
##            print "  "
        return densityGrid

def main():
    MIN_CORNER = Vector2(-5.0, -5.0)
    SIZE = Vector2(10.0, 10.0)
    RES = Vector2(11,13)

    worldGrid = Grid( MIN_CORNER, SIZE, RES, Vector2(0,3.2), Vector2(-6,6), 1000.0 )

    frame = np.array( ( (0, 0),
                        (-0.3, 0),
                         ( 1, 4 ),
                         ( 2.5, -1 ),
                         (-2, 1),
                         (3,3),
                         (4.5, -4.5)
                     )
                   )
    agentRadius = 1.0
    v = Voronoi( MIN_CORNER,SIZE, RES )
    v.computeVoronoiDensity( worldGrid, frame, agentRadius )
    plt.imshow(  v.ownerGrid.cells[::-1, :] )
    plt.show()
    
if __name__ == '__main__':
    main()

        
        
        
        
