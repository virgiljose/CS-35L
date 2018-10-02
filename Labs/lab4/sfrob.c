#include <stdio.h>
#include <stdlib.h>

// compare function to compare two frobnicated strings
int frobcmp(const char * a, const char * b) {

  // idea is to XOR each byte of data with 00101010 (or 42)

  // do comparison one character at a time
  while(1) {
    // Comparison tests
    // check whether either a or b reached space
    if (*a == ' ' && *b == ' ') { return 0; }
    else if (*a == ' ') { return -1; }
    else if (*b == ' ') { return 1; }
    // if not, compare current character of a and b
    else if((*a ^ 42) < (*b ^ 42)) { return -1; }
    else if((*b ^ 42) < (*a ^ 42)) { return 1; }
    else { a++; b++; }
  } 
  return 0;
}


// wrapper function for frobcmp (which casts void pointers as ints then returns result of fromcmp)
 int wrapfrobcmp(const void * va, const void * vb) { 
   const char * a = *(const char **) va;
   const char * b = *(const char **) vb;
   return frobcmp(a, b);
}

// helper function for checking whether there is a memory allocation error
void checkErr(void * ptr) {
  if(ptr == NULL) {
    fprintf(stderr, "Memory reallocation error");
    exit(1);
  }
}

// this function receives input from standard input and returns an array of strings containing the input
void sfrob() {
  
  char currChar;                    // holds one character at a time
  char * word;                      // holds one word at a time
  char ** wordArr;                  // holds the string of words

  word = malloc(sizeof(char));
  wordArr = malloc(sizeof(char*));
  
  int wordIndex = 0;
  int wordArrIndex = 0;

  while(!ferror(stdin) && !feof(stdin)) {

    // read character from input
    currChar = getchar();
    // check for errors in reading from input
    if(ferror(stdin)) {
	fprintf(stderr, "Error reading input");
	exit(1);
    }
    // check for case where user enters SPACE without entering anything else
    if (currChar == ' ' && wordIndex == 0) { continue; } // if user enters space but word is empty 

    // dynamically allocate space for character and add to word
    word = realloc(word, (wordIndex+1)*sizeof(char));
    word[wordIndex] = currChar;
    wordIndex++;
    // check for errors in memory reallocation for array 'word'
    checkErr(word);

    // when the end of the word is reached, dynamically allocate space in wordArr and put that word into wordArr
    if(currChar == ' ') {
      wordArr = realloc(wordArr, (wordArrIndex+1)*sizeof(char*));
      wordArr[wordArrIndex] = word;
      wordArrIndex++;
      checkErr(wordArr);

      word = (char*)malloc(0);
      wordIndex = 0;
    }
  }

  // case where EOF is reached at end of word (and array), in place of SPACE
  if(wordIndex > 0) {
	currChar = ' ';
        word = realloc(word, (wordIndex+1)*sizeof(char));
	word[wordIndex] = currChar;
	wordIndex++;
	checkErr(word);

	wordArr = realloc(wordArr, (wordArrIndex+1)*sizeof(char*));
	wordArr[wordArrIndex] = word;
	checkErr(wordArr);
	wordArrIndex++;

	word = (char*)malloc(0);
	wordIndex = 0;
  }


  // free char array as we no longer need it beyond this point
  free(word);

  int (*cmpptr)(const void *, const void *);
  cmpptr = &wrapfrobcmp;

  qsort(wordArr, wordArrIndex, sizeof(char*), cmpptr);

  int i, j;

  for(i = 0; i < wordArrIndex; i++) {
    for(j = 0; wordArr[i][j] != ' '; j++)
      putchar(wordArr[i][j]);
    putchar(' ');
  }

  // free word array as we no longer need it beyond this point
  free(wordArr);
}

int main() {
  sfrob();
}
