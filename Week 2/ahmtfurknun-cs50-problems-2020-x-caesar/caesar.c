#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        for (int i = 0; i < strlen(argv[1]); i++)
        {
            if (!isdigit(argv[1][i]))
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
    }
    int key = atoi(argv[1]);

    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int i = 0, n = strlen(plaintext) ; i < n; i++)
    {
        if (plaintext[i] >= 'a' && plaintext[i] <= 'z')
        {
            printf("%c", (((plaintext[i] - 'a') + key) % 26) + 'a');
        }
        else if (plaintext[i] >= 'A' && plaintext[i] <= 'Z')
        {
            printf("%c", (((plaintext[i] - 'A') + key) % 26) + 'A');
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }
    printf("\n");
}