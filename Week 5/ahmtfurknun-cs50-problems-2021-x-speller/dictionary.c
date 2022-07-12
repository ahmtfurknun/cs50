// Implements a dictionary's functionality

#include <stdbool.h>
#include "dictionary.h"
#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 676;

unsigned int h;
int count = 0;
// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO

    h = hash(word);
    node *current = table[h];
    while (current != NULL)
    {
        if (strcasecmp(word, current->word) == 0)
        {
            return true;
        }
        current = current->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    if (strlen(word) == 1)
    {
        int ha = (tolower(word[0]) - 'a') * 26;
        return ha;
    }
    else
    {
        int ha = (tolower(word[0]) - 'a') * 26 + tolower(word[1]) - 'a'; 
        return ha;
    }
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return 1;
    }
    char word[LENGTH + 1];
    
    while (fscanf(file, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return 1;
        }
        strcpy(n->word, word);
        h = hash(word);
        n->next = table[h];
        table[h] = n;
        count++;
        
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (count != 0)
    {
        return count;
    }
    else
    {
        return 0;
    }
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *current = table[i];
        while (current != NULL)
        {
            node *tmp = current;
            current = current -> next;
            free(tmp);
        }
    }
    return true;
}
