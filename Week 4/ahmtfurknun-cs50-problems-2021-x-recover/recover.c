#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Error! Unable to open");
        return 1;        
    }
    uint8_t buffer[512];
    int count = 0;
    FILE *outp;
    while (fread(buffer, 512, 1, file))
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (count != 0)
            {
                fclose(outp);
            }
            
            char fname[8];
            sprintf(fname, "%03i.jpg", count++);
            outp = fopen(fname, "w");
            if (outp == NULL)
            {
                return 1;
            }
            fwrite(buffer, 512, 1, outp);
        }
        else if (count != 0)
        {
            fwrite(buffer, 512, 1, outp);
        }
        
    }
    fclose(file);
    fclose(outp);
    return 0;
}