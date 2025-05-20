#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
#include <signal.h>
#include <openssl/evp.h>
#include <cjson/cJSON.h>

#define SHA256_DIGEST_LENGTH 32
#define MAX_TRACE 128


const char *trace_log[MAX_TRACE];
int trace_index = 0;

static unsigned char hash[32] = {0};

void hook(const char *func_name) {
    EVP_MD_CTX *ctx = EVP_MD_CTX_new();
    if (!ctx) {
        perror("EVP_MD_CTX_new");
        exit(1);
    }

    if (EVP_DigestInit_ex(ctx, EVP_sha256(), NULL) != 1) {
        perror("EVP_DigestInit_ex");
        exit(1);
    }

    if (EVP_DigestUpdate(ctx, hash, 32) != 1) {
        perror("EVP_DigestUpdate(hash)");
        exit(1);
    }

    if (EVP_DigestUpdate(ctx, func_name, strlen(func_name)) != 1) {
        perror("EVP_DigestUpdate(func_name)");
        exit(1);
    }

    if (EVP_DigestFinal_ex(ctx, hash, NULL) != 1) {
        perror("EVP_DigestFinal_ex");
        exit(1);
    }

    EVP_MD_CTX_free(ctx);

    // Log to file
    FILE *log_file = fopen("hook.txt", "a");
    if (log_file != NULL) {
        fprintf(log_file, "%s\n", func_name);
        fclose(log_file);
    } else {
        perror("fopen hook.txt");
    }
}


char *hash_to_hex(const unsigned char *hash_val) {
    char *hex_output = malloc(SHA256_DIGEST_LENGTH * 2 + 1);
    if (!hex_output) return NULL;

    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        sprintf(hex_output + i * 2, "%02x", hash_val[i]);
    }
    hex_output[SHA256_DIGEST_LENGTH * 2] = '\0';
    return hex_output;
}


int is_hash_trusted(const char *hash_hex, const char *filename) {
    FILE *f = fopen(filename, "r");
    if (!f) return 0;

    fseek(f, 0, SEEK_END);
    long len = ftell(f);
    rewind(f);

    char *data = malloc(len + 1);
    fread(data, 1, len, f);
    data[len] = '\0';
    fclose(f);

    cJSON *root = cJSON_Parse(data);
    free(data);
    if (!root) return 0;

    int trusted = 0;
    for (int i = 0; i < cJSON_GetArraySize(root); i++) {
        cJSON *entry = cJSON_GetArrayItem(root, i);
        cJSON *final_hash = cJSON_GetObjectItem(entry, "final_hash");
        if (final_hash && strcmp(final_hash->valuestring, hash_hex) == 0) {
            trusted = 1;
            break;
        }
    }

    cJSON_Delete(root);
    return trusted;
}

void print_trace_log() {
    printf("Execution Trace:\n");
    for (int i = 0; i < trace_index; ++i) {
        printf("  %s\n", trace_log[i]);
    }
}

void on_exit_handler() {
    hook("EXIT_OK");
    print_trace_log();
    char *final_hex = hash_to_hex(hash);
    printf("Final Hash: %s\n", final_hex);

    if (!is_hash_trusted(final_hex, "trusted_cfg.json")) {
        printf("❌ ALERT: Untrusted control flow detected!\n");
        free(final_hex);
        exit(1);
    } else {
        printf("✅ Control flow integrity verified.\n");
        free(final_hex);
    }
}

void sig_handler(int sig) {
    fprintf(stderr, "\nCaught signal %d (possible attack or forced exit)\n", sig);
    print_trace_log();
    printf("Final Hash: %s\n", hash_to_hex(hash));
    _exit(1);
}

void setup_signal_handlers() {
    signal(SIGINT, sig_handler);
    signal(SIGTERM, sig_handler);
    signal(SIGSEGV, sig_handler);
}

// ---- Program Logic Starts Here ----

char *getUsername() {
    hook("getUsername");

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
    hook("printGrades");

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
    hook("findUser");

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
    hook("retrieveGrades");

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
    memset(hash, 0, SHA256_DIGEST_LENGTH);
    hook("main");

    atexit(on_exit_handler);
    setup_signal_handlers();

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
