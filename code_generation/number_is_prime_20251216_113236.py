import math
# Checks if a number is prime.
# 
# Args:
#     n (int): The number to check.
# 
# Returns:
#     bool: True if the number is prime, False otherwise.
def is_prime(n: int) -> bool:
    # Numbers less than or equal to 1 are not prime.
    if n <= 1:
        return False
    # 2 is the only even prime number.
    if n == 2:
        return True
    # All other even numbers are not prime.
    if n % 2 == 0:
        return False
    # Only need to check up to the square root of n.
    # This is because a larger factor of the number would be a multiple of a smaller factor that has already been checked.
    for d in range(3, math.isqrt(n) + 1, 2):
        if n % d == 0:
            return False
    return True
# Main function to test the is_prime function.
def main():
    try:
        # Get user input and convert it to an integer.
        num = int(input("Enter a number: "))
        # Check if the number is prime and print the result.
        if is_prime(num):
            print(f"{num} is prime")
        else:
            print(f"{num} is not prime")
    except ValueError:
        # Handle cases where the user input is not an integer.
        print("Invalid input. Please enter an integer.")
# Run the main function if the script is run directly.
if __name__ == "__main__":
    main()