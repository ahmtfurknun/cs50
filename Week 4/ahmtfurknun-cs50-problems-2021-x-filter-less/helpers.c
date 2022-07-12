#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            if (image[i][j].rgbtBlue == image[i][j].rgbtRed && image[i][j].rgbtRed == image[i][j].rgbtGreen)
            {
                continue;
            }
            else
            {
                int average = round(((float)image[i][j].rgbtBlue + (float)image[i][j].rgbtRed + (float)image[i][j].rgbtGreen) / 3);
                image[i][j].rgbtBlue = average;
                image[i][j].rgbtRed = average;
                image[i][j].rgbtGreen = average;
            }
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = image[i][j].rgbtRed;
            int blue = image[i][j].rgbtBlue;
            int green = image[i][j].rgbtGreen;


            int sred = round(.393 * red + .769 * green + .189 * blue);
            int sgreen = round(.349 * red + .686 * green + .168 * blue);
            int sblue = round(.272 * red + .534 * green + .131 * blue);
            if (sred > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = sred;
            }

            if (sgreen > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = sgreen;
            }

            if (sblue > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = sblue;
            }
        }
    }


    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            int tempr = image[i][j].rgbtRed;
            image[i][j].rgbtRed = image[i][width - (j + 1)].rgbtRed;
            image[i][width - (j + 1)].rgbtRed = tempr;

            int tempg = image[i][j].rgbtGreen;
            image[i][j].rgbtGreen = image[i][width - (j + 1)].rgbtGreen;
            image[i][width - (j + 1)].rgbtGreen = tempg;

            int tempb = image[i][j].rgbtBlue;
            image[i][j].rgbtBlue = image[i][width - (j + 1)].rgbtBlue;
            image[i][width - (j + 1)].rgbtBlue = tempb;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = 0;
            int green = 0;
            int blue = 0;
            int count = 0;
            
            for (int ii = -1; ii < 2; ii++)
            {
                for (int jj = -1; jj < 2; jj++)
                {
                    if ((i + ii) != height && (j + jj) != width && (i + ii) != -1 && (j + jj) != -1)
                    {
                        red += temp[i + ii][j + jj].rgbtRed;
                        green += temp[i + ii][j + jj].rgbtGreen;
                        blue += temp[i + ii][j + jj].rgbtBlue;
                        count++;
                    }
                }
            }
            
            image[i][j].rgbtRed = (int)(round((float)red / count));
            image[i][j].rgbtGreen = (int)(round((float)green / count));
            image[i][j].rgbtBlue = (int)(round((float)blue / count));

            
        }
    }

    return;
}
