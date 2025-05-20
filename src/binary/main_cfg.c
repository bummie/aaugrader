#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

void on_exit_handler() {
    fprintf(stderr, "%s\n", "EXIT_OK");
}

char *getUsername() {
   fprintf(stderr, "%s\n", "getUsername");

    printf("Semester: ");
    char semester[10];
    scanf("%s", semester);
    printf(semester);

    printf("\nUsername: ");
    char username[80];
    scanf("%s", username);

    if (strlen(username) > 10) {
        printf("Username is too long!\n");
        return "bad_username";
    }

    char *heapUsername = malloc(10);
    strncpy(heapUsername, username, strlen(username) + 1);
    return heapUsername;
}

void printGrades(char *username, char *input) {
    fprintf(stderr, "%s\n", "printGrades");

    char *copy = strdup(input);
    if (copy == NULL) exit(1);

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
    fprintf(stderr, "%s\n", "findUser");

    char *copy = strdup(input);
    if (copy == NULL) exit(1);

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

void retrieveGrades(char *username) {
    fprintf(stderr, "%s\n", "retrieveGrades");

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
        if (!findUser(username, gradesLine)) continue;
        printGrades(username, gradesLine);
        userFound = true;
    }

    if (!userFound) {
        printf("Username: %s not found!\n", username);
    }

    pclose(fp);
}

int main(int argc, char *argv[]) {
    fprintf(stderr, "%s\n", "main");
    atexit(on_exit_handler);

    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    printf(" ▗▄▖  ▗▄▖ ▗▖ ▗▖    ▗▄▄▖▗▄▄▖  ▗▄▖ ▗▄▄▄  ▗▄▄▄▖▗▄▄▖ \n");
    printf("▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌   ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌  █ ▐▌   ▐▌ ▐▌\n");
    printf("▐▛▀▜▌▐▛▀▜▌▐▌ ▐▌   ▐▌▝▜▌▐▛▀▚▖▐▛▀▜▌▐▌  █ ▐▛▀▀▘▐▛▀▚▖\n");
    printf("▐▌ ▐▌▐▌ ▐▌▝▚▄▞▘   ▝▚▄▞▘▐▌ ▐▌▐▌ ▐▌▐▙▄▄▀ ▐▙▄▄▖▐▌ ▐▌\n");
    printf("                                                 \n");
    printf("(C) 2025                                         \n");

    printf("This program returns the grades for the specified user.\n");
    

    char *username = getUsername();
    retrieveGrades(username);

    return 0;
}