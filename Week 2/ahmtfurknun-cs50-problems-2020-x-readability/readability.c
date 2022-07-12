#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    string text = get_string("Text: ");

    int letter = 0;
    int word = 1;
    int sentence = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            letter++;
        }
    }

    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == ' ' && text[i + 1] != ' ')
        {
            word++;
        }
    }

    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            sentence++;
        }
    }
    float L = 100 * (float) letter / word;
    float S = 100 * (float) sentence / word;
    float index = 0.0588 * L - 0.296 * S - 15.8;

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }

    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }

    else
    {
        int grade = round(index);
        printf("Grade %i\n", grade);
    }

}