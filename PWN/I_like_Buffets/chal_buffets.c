#include <stdio.h>
#include <stdlib.h>

#define MAX_CHAR_LENGTH 300
#define max_rand 16

void print_flag(){ // interesting function no?
  FILE* f = fopen("flag.txt","r");
  if(f == NULL){
    printf("Oops current directory has no flag\n");
    return;
  }
  char flag[MAX_CHAR_LENGTH];
  if(fgets(flag,MAX_CHAR_LENGTH,f) != NULL){
    printf("%s",flag);
    return; 
  }
}


int main(){ 
  setvbuf(stdout, NULL, _IONBF, 0);

  char Username[MAX_CHAR_LENGTH];
  unsigned int customer_id = 0; 
  long long int session_id = rand() % max_rand; //aha the session_ids are random (or are they?) 
try_again:
  printf("Enter you Customer ID : ");
  scanf("%d",&customer_id);
  printf("Enter your Username : ");
  scanf("%s",Username );
  if(session_id == -60452921414551197 ){ // my session_id ranges only from 0 to 15 , no chance u can hack it :)
    printf("Admin Access Panel:\n");
    printf("Here is your flag:\n"); 
    print_flag(); 
  }
  else{
    printf("Oops , nothing there for a measly 'User' to do\n"); // users are useless ;-;
    printf("Press Cntrl+C to exit the loop ,else try another customer_id and Username.\n");
    goto try_again;
  }
  return 0;
}
