#include <iostream>
#include <string>
#include <HelloLib/HelloLib.h>

int main()
{
	std::cout << "Hello World. The answer is: " << std::to_string(get_the_answer()) << std::endl;
	char input;
	std::cin >> input;
	return 0;
}