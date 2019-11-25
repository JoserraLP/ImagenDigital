// for OpenCV2
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/objdetect/objdetect.hpp"
#include "opencv2/gpu/gpu.hpp"
#include "opencv2/highgui/highgui.hpp"

using namespace cv;
using namespace std;

int main(int argc, char* argv[])
{
	Mat src_img, template_img;
	Mat result_mat;
	Mat debug_img;

	template_img = imread("lena_eye.jpg", CV_LOAD_IMAGE_GRAYSCALE);
	if (template_img.data == NULL) {
		//cout<<"cv::imread() failed."<<endl;;
		return -1;
	}
	imshow("Template Image",template_img);

	src_img = imread("lena.jpg", CV_LOAD_IMAGE_GRAYSCALE);
	if (src_img.data == NULL) {
		//cout<<"cv::imread() failed.."<<endl;
		return -1;
	}
	cvtColor(src_img, debug_img, CV_GRAY2BGR);
        // method: CV_TM_SQDIFF, CV_TM_SQDIFF_NORMED, CV_TM _CCORR, CV_TM_CCORR_NORMED, CV_TM_CCOEFF, CV_TM_CCOEFF_NORMED
		int match_method = CV_TM_CCORR_NORMED;
		matchTemplate(src_img, template_img, result_mat, match_method);
		normalize(result_mat, result_mat, 0, 1, NORM_MINMAX, -1, Mat());
		double minVal; double maxVal; 
		Point minLoc, maxLoc, matchLoc;
		minMaxLoc(result_mat, &minVal, &maxVal, &minLoc, &maxLoc, Mat() );
		if( match_method  == CV_TM_SQDIFF || match_method == CV_TM_SQDIFF_NORMED )  matchLoc = minLoc;
		else matchLoc = maxLoc;

		rectangle(
			debug_img,
			matchLoc,
			Point(matchLoc.x + template_img.cols , matchLoc.y + template_img.rows),
			CV_RGB(255,0,0),
			3);
                
		imshow("Match Template", debug_img);

		int c = waitKey();
		//if (c == 27) break;
	return 0;
}
