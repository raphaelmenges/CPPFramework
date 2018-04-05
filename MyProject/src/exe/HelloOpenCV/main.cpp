#include <HelloOpenCVLib/HelloOpenCVLib.h>
#include <opencv2/core/utility.hpp>
#include <opencv2/opencv.hpp>
#include <iostream>

int main(int argc, const char* argv[])
{
	std::cout << "Welcome to OpenCV " << HelloOpenCVLib::get_version() << std::endl;

	cv::Mat img, gray;
	img = cv::imread(std::string(RES_PATH) + "/test/nero.png", cv::IMREAD_COLOR);

	cv::cvtColor(img, gray, cv::COLOR_BGR2GRAY);
	cv::GaussianBlur(gray, gray, cv::Size(7, 7), 1.5);
	cv::Canny(gray, gray, 0, 50);

#ifndef HEADLESS
	{
		cv::imshow("img", img);
		cv::imshow("edges", gray);
		cv::waitKey();
	}
#endif
	
	return 0;
}