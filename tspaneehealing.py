from scipy import *


def Distance(R1, R2):
    return sqrt((R1[0]-R2[0])**2+(R1[1]-R2[1])**2)

def TotalDistance(place, R):
    dist=0
    for i in range(len(place)-1):
        dist += Distance(R[place[i]],R[place[i+1]])
    dist += Distance(R[place[-1]],R[place[0]])
    return dist
    
def reverse(place, n):
    ncp = len(place)
    nn = (1+ ((n[1]-n[0]) % ncp))/2 # half the lenght of the segment to be reversed
    # the segment is reversed in the following way n[0]<->n[1], n[0]+1<->n[1]-1, n[0]+2<->n[1]-2,...
    # Start at the ends of the segment and swap pairs of cities, moving towards the center.
    for j in range(nn):
        k = (n[0]+j) % ncp
        l = (n[1]-j) % ncp
        (place[k],place[l]) = (place[l],place[k])  # swap
    
def replace(place, n):
    ncp = len(place)
    
    newplace=[]
    # Segment in the range n[0]...n[1]
    for j in range( (n[1]-n[0])%ncp + 1):
        newplace.append(place[ (j+n[0])%ncp ])
    # is followed by segment n[5]...n[2]
    for j in range( (n[2]-n[5])%ncp + 1):
        newplace.append(place[ (j+n[5])%ncp ])
    # is followed by segment n[3]...n[4]
    for j in range( (n[4]-n[3])%ncp + 1):
        newplace.append(place[ (j+n[3])%ncp ])
    return newplace



if __name__=='__main__':

    nplace = 5        # Number of cities to visit
    maxTsteps = 5    # Temperature is lowered not more than maxTsteps
    Tstart = 0.2       # Starting temperature - has to be high enough
    fCool = 0.9        # Factor to multiply temperature at each cooling step
    maxSteps = 10*nplace     # Number of steps at constant temperature
    maxAccepted = 10*nplace   # Number of accepted steps at constant temperature

    Preverse = 0.5      # How often to choose reverse/transpose trial move

    # Choosing place coordinates
    R=[]  # coordinates of cities are choosen randomly
    for i in range(nplace):
        R.append( [rand(),rand()] )
    R = array(R)

    # The index table -- the order the cities are visited.
    place = range(nplace)
    # Distance of the travel at the beginning
    dist = TotalDistance(place, R)

    # Stores points of a move
    n = zeros(6, dtype=int)  #Returns with Zero Array implemented in scipy only
    ncp = len(R) # number of cities
    
    T = Tstart # temperature


    print "Simmulated Annehealing result after cooling in each step"    
    for t in range(maxTsteps):  # Over temperature

        accepted = 0
        for i in range(maxSteps): # At each temperature, many Monte Carlo steps
            
            while True: # Will find two random cities sufficiently close by
                # Two cities n[0] and n[1] are choosen at random
                n[0] = int((ncp)*rand())     # select one place
                n[1] = int((ncp-1)*rand())   # select another place, but not the same
                if (n[1] >= n[0]): n[1] += 1   #
                if (n[1] < n[0]): (n[0],n[1]) = (n[1],n[0]) # swap, because it must be: n[0]<n[1]
                nn = (n[0]+ncp -n[1]-1) % ncp  # number of cities not on the segment n[0]..n[1]
                if nn>=3: break
        
            # We want to have one index before and one after the two cities
            # The order hence is [n2,n0,n1,n3]
            n[2] = (n[0]-1) % ncp  # index before n0  
            n[3] = (n[1]+1) % ncp  # index after n2               
            if Preverse > rand(): 
                # We need to return to the path if cost is greater
                # Finding the distance betwen  those points ie the cost to reverse the path between place[n[0]]-place[n[1]]
                de = Distance(R[place[n[2]]],R[place[n[1]]]) + Distance(R[place[n[3]]],R[place[n[0]]]) - Distance(R[place[n[2]]],R[place[n[0]]]) - Distance(R[place[n[3]]],R[place[n[1]]])
                
                if de<0 or exp(-de/T)>rand(): 
                    accepted += 1
                    dist += de
                    reverse(place, n)
            else:
                # Here we transpose a segment
                nc = (n[1]+1+ int(rand()*(nn-1)))%ncp  # Another point outside n[0],n[1] segment.
                n[4] = nc
                n[5] = (nc+1) % ncp
        
                # Cost to transpose a segment
                de = -Distance(R[place[n[1]]],R[place[n[3]]]) - Distance(R[place[n[0]]],R[place[n[2]]]) - Distance(R[place[n[4]]],R[place[n[5]]])
                de += Distance(R[place[n[0]]],R[place[n[4]]]) + Distance(R[place[n[1]]],R[place[n[5]]]) + Distance(R[place[n[2]]],R[place[n[3]]])
                
                if de<0 or exp(-de/T)>rand(): 
                    accepted += 1
                    dist += de
                    place = replace(place, n)
                    
            if accepted > maxAccepted: break

#        print "Simmulated Annehealing result after cooling in each step"            
        print "Temprature =%f , distance= %f , accepted steps= %d" %(T, dist, accepted)
        T *= fCool             # The system is cooled down
        if accepted == 0: break  # If the path does not want to change any more, we can stop place
