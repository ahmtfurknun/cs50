#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float dollars;
    do
    {
        dollars = get_float("Change owed: ");
    }
    while (dollars < 0);

    int cents = round(dollars * 100);

    int quarters = 0;
    int dimes = 0;
    int nickels = 0;
    int pennies = 0;

    while (cents >= 25)
    {
        quarters = quarters + 1;
        cents = cents - 25;
    }

    while (cents >= 10)
    {
        dimes = dimes + 1;
        cents = cents - 10;
    }

    while (cents >= 5)
    {
        nickels = nickels + 1;
        cents = cents - 5;
    }

    while (cents >= 1)
    {
        pennies = pennies + 1;
        cents = cents - 1;
    }


    int tot = quarters + dimes + nickels + pennies;
    printf("%i\n", tot);
}