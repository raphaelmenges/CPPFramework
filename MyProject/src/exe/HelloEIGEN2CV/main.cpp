#include <iostream>
#include <Eigen/Dense>
#include <opencv2/core/eigen.hpp>

int main()
{
	cv::Mat_<float> a = cv::Mat_<float>::ones(2, 2);
	Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic> b;
	cv::cv2eigen(a, b);
}