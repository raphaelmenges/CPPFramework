#include "HelloIndirectLib.h"
#include <HelloLib/HelloLib.h>

int HelloIndirectLib::get_the_answer_indirect()
{
	return HelloLib::get_the_answer() + 1;
}