# beta distribution
import numpy as np
import scipy.stats as ss
from matplotlib import pyplot as plt

plt.style.use( 'seaborn' )
plt.rcParams['figure.figsize'] = ( 12, 8 )

plt.figure( 1 )
x = np.linspace( 0, 1, 5000 )

# bandit machine 01
a1 = 16 # success
b1 = 4 # fail
y = ss.beta.pdf( x, a1, b1 )
plt.plot( x, y, color='red', lw=2, ls='-', alpha=0.5, label='Bandit Machine 01' )

# bandit machine 02
a2 = 8 # success
b2 = 12  # fail
y = ss.beta.pdf( x, a2, b2 )
plt.plot( x, y, color='blue', lw=2, ls='-', alpha=0.5, label='Bandit Machine 02' )
#plt.legend( loc=0, prop={'size': 20});
plt.show();
