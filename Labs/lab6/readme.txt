----------------------------------------------------------------------------------------------------

It is clear the multithreading has improved the performance of the program. Every time we double 
the number of threads, the user time is approximately halved. There is a *very minor* tradeoff: 
creating threads takes processing power and thus time, so we do see a slight increase in user time 
as we create more threads. However, the benefits of threading far outweigh the cons, as seen in the 
results below:

time ./srt 1-test.ppm >1-test.ppm.tmp

real 0m40.976s
user 0m40.969s
sys  0m0.001s
mv 1-test.ppm.tmp 1-test.ppm
time ./srt 2-test.ppm >2-test.ppm.tmp

real 0m21.426s
user 0m42.652s
sys  0m0.002s
mv 2-test.ppm.tmp 2-test.ppm
time ./srt 4-test.ppm >4-test.ppm.tmp

real 0m11.169s
user 0m44.338s
sys  0m0.002s
mv 4-test.ppm.tmp 4-test.ppm
time ./srt 8-test.ppm >8-test.ppm.tmp

real 0m5.745s
user 0m44.503s
sys  0m0.001s

----------------------------------------------------------------------------------------------------

In order to implement multithreading, I needed to do more than just put main into my pthreads
function. A few implementations needed to be modified in order for my multithreaded implentation of
the program to run correctly. I go over the issues I had in implementing multithreading below:


(1) I originally did not modify the implementation of writing out the pixels to disk. Because of
this, the actual output was different form the output needed. This is most likely because
multithreading is not necessarily synchronized. Thus, the output would be printed in the wrong
order. In order to fix this issue, I realized that I needed to take into account the fact that
multithreading is not synchronized and thus a new implementation of writing the output is needed. I
found that the easiest was to do so was the following:

Declare a global variable called pixvals, which holds the value of every pixel. I declared it
globally because each element (i.e. each pixel) is assigned a value in threadWork, but outputted
in main:

float pixvals[width][height][3];



Modify the for-loop where scaled_color[i] is modified such that caps is enforced, and is replaced
with real gamma, by adding a line to assign each element of pixvals the value of its corresponding
pixel:

for( int i=0; i<3; i++) {
                scaled_color[i] = max( min(scaled_color[i], 255), 0);
                pixvals[px][py][i] = scaled_color[i];
            }



Remove the original implementation of outputting the values of each pixel in threadWork. Instead,
put a new implementation in main. We do so because of the asynchronous nature of multithreading
with pthreads. The idea is to assign pixvals all the values first and then printing everything out
in the end:

int i, j;
    for(i = 0; i < width; i++) {
        for(j = 0; j < height; j++) {
              printf("%.0f %.0f %.0f\n", pixvals[i][j][0], pixvals[i][j][1], pixvals[i][j][2]);
          }
        printf("\n");
      }

There are other ways to modify the original implementation. One way to do so is to implement
semaphores. However, I chose to modify the implmentation in the way that I did because I found it
to be the easiest way to do so. I have little experience with using semaphores. Using them would
require using functions that I am unfamiliar with and figuring out where they need to go. Therefore,
I chose simply to declare a global array to hold all the values and print them all at the end.

----------

(2) I originally created a struct that stored the arguments needed for the multithreading function.
The struct looked like this:

struct threadArgs {
       int nthreads;
       int n;
       scene_t scene;
};

I found that passing in a struct complicated the multithreading implementation because I needed to
cast and dereference the struct and the variables within the struct. I also ran into a lot of
compiler errors as I did not completely understand how to declare or use structs, dereference struct
pointers, or cast void pointers into struct pointers. I did not want to deal with those issues.

Instead, I decided to declare nthreads and scene globally, so that I could use those variables in
both my main and my multithreading function, threadWork. I found that this was much easier than
passing in a struct pointer (casted as a void pointer) in pthread_create.

----------------------------------------------------------------------------------------------------
