#include <stdio.h>
#include <cs50.h>

int get_positive_int(void);

int main(void)
{
    int height = get_positive_int();
    for (int line = 0; line < height; line++)
    {
        for (int space = 0; space < height - line - 1; space++)
        {
            printf(" ");
        }
        for (int j = 0; j <= line ; j++)
        {
            printf("#");
        }
        printf("\n");
    }

}

int get_positive_int(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);
    return height;
}