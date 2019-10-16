#ifndef CARA_H_
#define CARA_H_

typedef struct {
	float x;
	float y;
	float z;
} TNormal;


class Cara {
	int a,b,c;
	TNormal normal;

public:
	Cara();
	Cara(int vA, int vB,int vC);
	Cara(int vA, int vB,int vC,TNormal normal);
	int getA();
	void setA(int a);
	int getB();
	void setB(int b);
	int getC();
	void setC(int c);
	TNormal getNormal();
	void setNormal(TNormal normal);
	float getNormalX();
	float getNormalY();
	float getNormalZ();
	~Cara();
};

#endif /* CARA_H_ */
