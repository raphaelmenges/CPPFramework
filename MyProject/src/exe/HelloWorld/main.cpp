//!  Hello World main. 
/*!
Project to check whether the framework compiles. Makes use of internal libraries.
*/

#include <iostream>
#include <string>
#include <HelloLib/HelloLib.h>
#include <HelloIndirectLib/HelloIndirectLib.h>

//! Main function.
/*!
\return The program result.
*/
int main()
{
	std::cout
		<< "Hello World. The answer is: " << std::to_string(HelloLib::get_the_answer()) // use of HelloLib library
		<< ". And the indirect answer is: " << std::to_string(HelloIndirectLib::get_the_answer_indirect()) // use of HelloLib library through 
		<< std::endl;
	char input;
	std::cin >> input;
	return 0;
}