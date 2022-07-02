#include <math.h>
#include <stdio.h>

extern "C" { 

static double interpolate( double val, double y0, double x0, double y1, double x1 ) {
  return (val-x0)*(y1-y0)/(x1-x0) + y0;
}

static double blue( double grayscale ) {
  if ( grayscale < -0.33 ) return 1.0;
  else if ( grayscale < 0.33 ) return interpolate( grayscale, 1.0, -0.33, 0.0, 0.33 );
  else return 0.0;
}

static double green( double grayscale ) {
  if ( grayscale < -1.0 ) return 0.0; // unexpected grayscale value
  if  ( grayscale < -0.33 ) return interpolate( grayscale, 0.0, -1.0, 1.0, -0.33 );
  else if ( grayscale < 0.33 ) return 1.0;
  else if ( grayscale <= 1.0 ) return interpolate( grayscale, 1.0, 0.33, 0.0, 1.0 );
  else return 1.0; // unexpected grayscale value
}

static double red( double grayscale ) {
  if ( grayscale < -0.33 ) return 0.0;
  else if ( grayscale < 0.33 ) return interpolate( grayscale, 0.0, -0.33, 1.0, 0.33 );
  else return 1.0;
}

void heatmap_viz(const float* input, unsigned char* output, int width, int height, float min, float max)
{
    int size=width*height;

    for (int i = 0; i < size; ++i) {
        const float* inpixel = &(input[i]);
        unsigned char* outpixel = &(output[i*3]);

        float value = ((*inpixel)-min)/(max-min)*2.0-1.0;
        if(value>1) value=1;
        if(value<-1) value=-1;
        float r = 255.0*red(value);
        if(r<0) r=0;
        if(r>255) r=255;
        float g = 255.0*green(value);
        if(g<0) g=0;
        if(g>255) g=255;
        float b = 255.0*blue(value);
        if(b<0) b=0;
        if(b>255) b=255;
        outpixel[0] = (unsigned char)r;
        outpixel[1] = (unsigned char)g;
        outpixel[2] = (unsigned char)b;
    }
}

}

