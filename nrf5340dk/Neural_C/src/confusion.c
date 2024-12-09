#include <zephyr/kernel.h>
#include <math.h>
#include "confusion.h"
#include "adc.h"
#include <zephyr/logging/log.h>
#include "model_weights_and_stats.h"


/* 
  K-means algorithm should provide 6 center points with
  3 values x,y,z. Let's test measurement system with known
  center points. I.e. x,y,z are supposed to have only values
  1 = down and 2 = up
  
  CP matrix is thus the 6 center points got from K-means algoritm
  teaching process. This should actually come from include file like
  #include "KmeansCenterPoints.h"
  
  And measurements matrix is just fake matrix for testing purpose
  actual measurements are taken from ADC when accelerator is connected.
*/ 

int CP[6][3]={
	                     {1,0,0},
						 {2,0,0},
						 {0,1,0},
						 {0,2,0},
						 {0,0,1},
						 {0,0,2}
};

int measurements[6][3]={
	                     {1,0,0},
						 {2,0,0},
						 {0,1,0},
						 {0,2,0},
						 {0,0,1},
						 {0,0,2}
};

int CM[6][6]= {0};


LOG_MODULE_REGISTER(my_module, LOG_LEVEL_DBG); 

void printConfusionMatrix(void)
{
	printk("Confusion matrix = \n");
	printk("   cp1 cp2 cp3 cp4 cp5 cp6\n");
	for(int i = 0;i<6;i++)
	{
		printk("cp%d %d   %d   %d   %d   %d   %d\n",i+1,CM[i][0],CM[i][1],CM[i][2],CM[i][3],CM[i][4],CM[i][5]);
	}
}
void dense_layer(float* input, int input_size, int output_size, float* output) {
    for (int i = 0; i <output_size; i++) {
        output[i] = layer_1_biases[i];
        LOG_DBG("Neuron %d, Initial bias: %.6f", i, layer_1_biases[i]);

        
        for (int j = 0; j <input_size; j++) {
            
            output[i] += input[j] * layer_1_weights[j * output_size + i];
            
        }
        LOG_DBG("Final Output for Neuron %d: %.6f", i, output[i]);
    }
}
void softmax(float* input, int size) {
    float max_val = input[0];
    for (int i = 1; i < size; i++) {
        if (input[i] > max_val) {
            max_val = input[i];
        }
    }

    float sum_exp = 0.0f;
    for (int i = 0; i < size; i++) {
        input[i] = expf(input[i] - max_val); 
        sum_exp += input[i];
    }

    for (int i = 0; i < size; i++) {
        input[i] /= sum_exp; 
    }
}
int predict_label_from_input(float* input_data, int input_size) {
    float output[6]; 
    LOG_DBG("Input data: x = %.6f, y = %.6f, z = %.6f", input_data[0], input_data[1], input_data[2]);
    dense_layer(input_data, input_size, 6, output); 
      for (int i = 0; i < 6; i++) {
        LOG_DBG("output[%d] = %.6f", i, output[i]);
    }

    softmax(output, 6); 

    
    int label = 0;
    float max_output = output[0];
    for (int i = 1; i < 6; i++) {
        if (output[i] > max_output) {
            max_output = output[i];
            label = i;
        }
    }

    
    printk("Softmax probabilities:\n");
    for (int i = 0; i < 6; i++) {
        LOG_DBG("output[%d] = %.6f", i, output[i]);
    }

    printf("Predicted label: %d\n", label);
    return label;
}
void makeHundredFakeClassifications(void)
{
   /*******************************************
   Jos ja toivottavasti kun teet toteutuksen paloissa eli varmistat ensin,
   että etäisyyden laskenta 6 keskipisteeseen toimii ja osaat valita 6 etäisyydestä
   voittajaksi sen lyhyimmän etäisyyden, niin silloin voit käyttää tätä aliohjelmaa
   varmistaaksesi, että etäisuuden laskenta ja luokittelu toimii varmasti tunnetulla
   itse keksimälläsi sensoridatalla ja itse keksimilläsi keskipisteillä.
   *******************************************/
   printk("Make your own implementation for this function if you need this\n");
}

void makeOneClassificationAndUpdateConfusionMatrix(int direction)
{
   /**************************************
   Tee toteutus tälle ja voit tietysti muuttaa tämän aliohjelman sellaiseksi,
   että se tekee esim 100 kpl mittauksia tai sitten niin, että tätä funktiota
   kutsutaan 100 kertaa yhden mittauksen ja sen luokittelun tekemiseksi.
   **************************************/
   for(int i=0; i<100; i++)
    {
        struct Measurement m = readADCValue(); 

        float input_data[3] = {m.x,m.y,m.z};
        int predictedClass= predict_label_from_input(input_data, 3);




        CM[direction][predictedClass]++;

    }
   
   printk("Make your own implementation for this function if you need this\n");
}

int calculateDistanceToAllCentrePointsAndSelectWinner(int x,int y,int z)
{
   /***************************************
   Tämän aliohjelma ottaa yhden kiihtyvyysanturin mittauksen x,y,z,
   laskee etäisyyden kaikkiin 6 K-means keskipisteisiin ja valitsee
   sen keskipisteen, jonka etäisyys mittaustulokseen on lyhyin.
   ***************************************/
   
   printk("Make your own implementation for this function if you need this\n");
   return 0;
}

void resetConfusionMatrix(void)
{
	for(int i=0;i<6;i++)
	{ 
		for(int j = 0;j<6;j++)
		{
			CM[i][j]=0;
		}
	}
}

