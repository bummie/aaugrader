#include <stdio.h>
#include <stdlib.h>

int retrieveGrades(char *username){
  FILE *fp;
  char output[1035];

  char shell[] = "/bin/sh -c";
  char command[] = "cat";
  char fileNameGrades[] = "grades.txt";

  char finalCommand[40];
  sprintf(finalCommand, "%s \"%s %s \"", shell, command, fileNameGrades);
  fp = popen(finalCommand, "r");
  if (fp == NULL) {
    printf("Failed to run command\n" );
    exit(1);
  }

  while (fgets(output, sizeof(output), fp) != NULL) {
    printf("%s", output);
  }

  pclose(fp);

  return 0;
}

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

  printf("Let's find your grades %s!\n", username);

  retrieveGrades(username);
  return 0;
}
