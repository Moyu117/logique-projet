#include <stdio.h>
#include <stdlib.h>
#include <string.h>  

int main() {
    FILE *file = fopen("output.txt", "r");
    if (file == NULL) {
        perror("Error opening file");
        return EXIT_FAILURE;
    }

    int variables, clauses, num;
    char buffer[1024];

    while (fgets(buffer, sizeof(buffer), file)) {
        if (buffer[0] == 'c') {
            continue;  
        }
        if (buffer[0] == 'p') {
            sscanf(buffer, "p cnf %d %d", &variables, &clauses);
            break;
        }
    }

    printf("(");
    int firstClause = 1;


    while (fgets(buffer, sizeof(buffer), file)) {
        if (buffer[0] == 'c') {
            continue;  
        }

        if (!firstClause) {
            printf(")∧(");
        }
        firstClause = 0;

        char* token = strtok(buffer, " ");
        int firstVar = 1;
        while (token != NULL) {
            num = atoi(token);
            if (num == 0) {
                break;
            }

            if (!firstVar) {
                printf("V");
            }
            firstVar = 0;

            if (num > 0) {
                printf("L%d", num);
            } else {
                printf("¬L%d", -num);
            }
            token = strtok(NULL, " ");
        }
    }
    printf(")");

    fclose(file);
    return 0;
}
