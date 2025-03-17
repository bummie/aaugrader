#include <stdio.h>

int main(int argc, char* argv[]) {
  printf( " ▗▄▖  ▗▄▖ ▗▖ ▗▖         ▗▄▄▖▗▄▄▖  ▗▄▖ ▗▄▄▄  ▗▄▄▄▖▗▄▄▖ \n");
  printf( "▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌        ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌  █ ▐▌   ▐▌ ▐▌\n");
  printf( "▐▛▀▜▌▐▛▀▜▌▐▌ ▐▌        ▐▌▝▜▌▐▛▀▚▖▐▛▀▜▌▐▌  █ ▐▛▀▀▘▐▛▀▚▖\n");
  printf( "▐▌ ▐▌▐▌ ▐▌▝▚▄▞▘        ▝▚▄▞▘▐▌ ▐▌▐▌ ▐▌▐▙▄▄▀ ▐▙▄▄▖▐▌ ▐▌\n");
  printf( "                                                      \n");
  printf( "(C) 2025                                              \n");

  printf("This program returns the grades for the specified user.\n");

  char username[20];
  scanf("%s", username);

  printf("Hello %s", username);
  
  return 0;
}
