#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *getUsername() {
  printf("Username: ");
  char username[80];
  scanf("%s", username);

  char *wordd = malloc(strlen(username) + 1);
  strncpy(wordd, username, strlen(username) + 1);
  
  return wordd;
}

void printGrades(char *username, char *input) {
  char *copy = strdup(input);
  if (copy == NULL) {
    exit(1);
  }

  char dest[40] = {0};
  strcpy(dest, copy + strlen(username) + 1);

  char *token = strtok(dest, ";");
  while (token != NULL) {
    printf("\t%s\n", token);
    token = strtok(NULL, ";");
  }

  free(copy);
}

bool findUser(char *username, char *input) {
  char *copy = strdup(input);
  if (copy == NULL) {
    exit(1);
  }

  char *token = strtok(copy, ":");
  while (token != NULL) {
    if (strcmp(token, username) == 0) {
      free(copy);
      return true;
    }

    token = strtok(NULL, ":");
  }

  free(copy);
  return false;
}

// Takes username as input
// Reads users grades from grades.txt
void retrieveGrades(char *username) {
  FILE *fp;
  char gradesLine[100];

  char shell[] = "/bin/sh";
  char command[] = "cat";
  char fileNameGrades[] = "grades.txt";

  char finalCommand[40];
  sprintf(finalCommand, "%s -c \"%s %s\"", shell, command, fileNameGrades);
  fp = popen(finalCommand, "r");
  if (fp == NULL) {
    printf("Failed to run command\n");
    exit(1);
  }

  bool userFound = false;
  while (!userFound && fgets(gradesLine, sizeof(gradesLine), fp) != NULL) {
    if (!findUser(username, gradesLine)) {
      continue;
    }

    printGrades(username, gradesLine);
    userFound = true;
  }

  if (!userFound) {
    printf("Username: %s not found!\n", username);
  }

  pclose(fp);
}

int main(int argc, char *argv[]) {
  printf(" ▗▄▖  ▗▄▖ ▗▖ ▗▖    ▗▄▄▖▗▄▄▖  ▗▄▖ ▗▄▄▄  ▗▄▄▄▖▗▄▄▖ \n");
  printf("▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌   ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌  █ ▐▌   ▐▌ ▐▌\n");
  printf("▐▛▀▜▌▐▛▀▜▌▐▌ ▐▌   ▐▌▝▜▌▐▛▀▚▖▐▛▀▜▌▐▌  █ ▐▛▀▀▘▐▛▀▚▖\n");
  printf("▐▌ ▐▌▐▌ ▐▌▝▚▄▞▘   ▝▚▄▞▘▐▌ ▐▌▐▌ ▐▌▐▙▄▄▀ ▐▙▄▄▖▐▌ ▐▌\n");
  printf("                                                 \n");
  printf("(C) 2025                                         \n");

  printf("This program returns the grades for the specified user.\n");

  char *username = getUsername();
  printf("Let's find your grades %s!\n", username);

  retrieveGrades(username);
  return 0;
}
