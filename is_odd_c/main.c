#include <stdio.h>

int is_odd(unsigned int i);

int main(int argc, char const *argv[])
{
    unsigned int num;
    printf("Enter a number: ");
    scanf("%u", &num);
    if (is_odd(num))
        printf("%u is odd\n", num);
    else
        printf("%u is even\n", num);
    return 0;
}
