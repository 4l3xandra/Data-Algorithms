#include <stdio.h>

int main() {
    // Variable declaration
    double temperatures[10];
    double sum = 0.0;
    double maxTemperature = -1.0; // Initialize with a negative value
    int maxTemperatureCity = 0;
    int countOver40 = 0;

    // Input temperatures for each city
    for (int i = 0; i < 10; ++i) {
        do {
            printf("Enter the maximum summer temperature for city %d: ", i + 1);
            scanf("%lf", &temperatures[i]);

            // Defensive programming check
            if (temperatures[i] < 20 || temperatures[i] > 50) {
                printf("Please enter a value between 20 and 50.\n");
            }
        } while (temperatures[i] < 20 || temperatures[i] > 50);

        // Calculate average temperature
        sum += temperatures[i];

        // Check for maximum temperature and city number
        if (temperatures[i] > maxTemperature) {
            maxTemperature = temperatures[i];
            maxTemperatureCity = i + 1;
        }

        // Check for temperatures over 40 degrees
        if (temperatures[i] > 40) {
            ++countOver40;
        }
    }

    // Calculate average temperature
    double averageTemperature = sum / 10;

    // Print results
    printf("The average of the maximum temperatures is: %lf\n", averageTemperature);
    printf("The number of cities with temperatures over 40 degrees is: %d\n", countOver40);
    printf("The maximum temperature of the summer is: %lf in city %d\n", maxTemperature, maxTemperatureCity);

    return 0;
}
